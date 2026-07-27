#!/usr/bin/env python3
"""Build a balanced HGVS -> GRCh38 VCF truth set using Ensembl Variant Recoder.

ClinVar is used only as a large, reproducible source of transcript HGVS inputs.
The expected VCF alleles come exclusively from Ensembl Variant Recoder.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Iterator


SCHEMA_VERSION = "1.1"
DEFAULT_SERVER = "https://rest.ensembl.org"
ACCESSION_TO_CHROM = {
    accession: str(index + 1)
    for index, accession in enumerate(
        (
            "NC_000001.11", "NC_000002.12", "NC_000003.12", "NC_000004.12",
            "NC_000005.10", "NC_000006.12", "NC_000007.14", "NC_000008.11",
            "NC_000009.12", "NC_000010.11", "NC_000011.10", "NC_000012.12",
            "NC_000013.11", "NC_000014.9", "NC_000015.10", "NC_000016.10",
            "NC_000017.11", "NC_000018.10", "NC_000019.10", "NC_000020.11",
            "NC_000021.9", "NC_000022.11",
        )
    )
} | {"NC_000023.11": "X", "NC_000024.10": "Y", "NC_012920.1": "MT"}
CHROM_TO_ACCESSION = {chrom: accession for accession, chrom in ACCESSION_TO_CHROM.items()}


def open_text(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", newline="")
    return path.open("r", encoding="utf-8", newline="")


def canonical_header(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lstrip("#").lower())


def read_tsv(path: Path) -> Iterator[dict[str, str]]:
    with open_text(path) as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if not reader.fieldnames:
            raise ValueError(f"{path}: header is missing")
        normalized = [canonical_header(name) for name in reader.fieldnames]
        for raw in reader:
            yield {
                normalized[index]: (raw.get(name) or "").strip()
                for index, name in enumerate(reader.fieldnames)
            }


def first(row: dict[str, str], *names: str) -> str:
    for name in names:
        value = row.get(canonical_header(name), "")
        if value:
            return value
    return ""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def json_hash(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def vcf_key(value: dict[str, Any]) -> tuple[str, int, str, str]:
    return (
        str(value["chrom"]).removeprefix("chr"),
        int(value["pos"]),
        str(value["ref"]).upper(),
        str(value["alt"]).upper(),
    )


def expected_vcf_from_summary(row: dict[str, str]) -> dict[str, Any] | None:
    """Read a location for candidate filtering only; it is never used as truth."""
    if first(row, "Assembly") not in {"GRCh38", "GRCh38.p14"}:
        return None
    contig = first(row, "ChromosomeAccession")
    pos = first(row, "PositionVCF")
    ref = first(row, "ReferenceAlleleVCF")
    alt = first(row, "AlternateAlleleVCF")
    if (
        not (contig and pos.isdigit() and ref and alt)
        or ref == "-"
        or alt == "-"
        or not re.fullmatch(r"[ACGTN]+", ref, re.IGNORECASE)
        or not re.fullmatch(r"[ACGTN]+", alt, re.IGNORECASE)
    ):
        return None
    return {"chrom": contig, "pos": int(pos), "ref": ref.upper(), "alt": alt.upper()}


def supported_hgvs_type(value: str) -> bool:
    lowered = value.lower()
    if any(token in lowered for token in ("non-validated", "uncertain", "previous", "other", "protein")):
        return False
    return "coding" in lowered or "non-coding" in lowered or "noncoding" in lowered


def category(hgvs: str) -> str:
    body = hgvs.split(":", 1)[-1]
    if body.startswith("n."):
        context = "noncoding"
    elif re.search(r"(?:c|n)\.(?:\*|-)", body):
        context = "utr"
    elif re.search(r"\d+[+-]\d+", body):
        context = "intronic"
    else:
        context = "coding"
    if "delins" in body:
        operation = "delins"
    elif "dup" in body:
        operation = "dup"
    elif "ins" in body:
        operation = "ins"
    elif "del" in body:
        operation = "del"
    elif ">" in body:
        operation = "substitution"
    else:
        operation = "other"
    return f"{context}_{operation}"


def load_candidates(variant_summary: Path, hgvs_file: Path) -> tuple[list[dict[str, Any]], Counter]:
    """Join pinned ClinVar tables to obtain diverse, versioned HGVS inputs."""
    locations: dict[str, dict[str, Any]] = {}
    stats: Counter = Counter()
    for row in read_tsv(variant_summary):
        stats["variant_summary_rows"] += 1
        variation_id = first(row, "VariationID")
        location = expected_vcf_from_summary(row)
        if not variation_id or not location:
            continue
        if variation_id in locations and vcf_key(locations[variation_id]["vcf"]) != vcf_key(location):
            locations[variation_id]["conflicting_location"] = True
            continue
        locations[variation_id] = {
            "vcf": location,
            "gene": first(row, "GeneSymbol"),
            "allele_id": first(row, "AlleleID"),
            "variant_type": first(row, "Type"),
        }

    expressions: dict[str, list[tuple[str, str]]] = defaultdict(list)
    genomic: dict[str, set[str]] = defaultdict(set)
    for row in read_tsv(hgvs_file):
        stats["hgvs_rows"] += 1
        variation_id = first(row, "VariationID")
        hgvs_type = first(row, "TypeOfHGVS", "Type_of_HGVS", "Type")
        nucleotide = first(row, "NucleotideExpression", "NucleotideHGVS", "HGVS")
        if not variation_id or not nucleotide:
            continue
        if re.match(r"^NC_\d+\.\d+:g\.", nucleotide):
            genomic[variation_id].add(nucleotide)
        if supported_hgvs_type(hgvs_type) and re.match(
            r"^(?:NM_|NR_|ENST)\d+\.\d+:[cn]\.", nucleotide
        ):
            expressions[variation_id].append((nucleotide, hgvs_type))

    candidates: list[dict[str, Any]] = []
    seen_inputs: set[str] = set()
    for variation_id, values in expressions.items():
        location = locations.get(variation_id)
        if not location or location.get("conflicting_location"):
            continue
        matching_genomic = {
            value for value in genomic[variation_id]
            if value.startswith(location["vcf"]["chrom"] + ":g.")
        }
        if not matching_genomic:
            stats["rejected_missing_genomic_hgvs"] += len(values)
            continue
        for hgvs, hgvs_type in values:
            if hgvs in seen_inputs:
                stats["rejected_duplicate_input"] += 1
                continue
            seen_inputs.add(hgvs)
            candidates.append(
                {
                    "variation_id": variation_id,
                    "input": hgvs,
                    "hgvs_type": hgvs_type,
                    "genomic_hgvs": matching_genomic,
                    **location,
                    "category": category(hgvs),
                }
            )
    stats["candidates"] = len(candidates)
    return candidates, stats


def balanced_order(candidates: list[dict[str, Any]], seed: int) -> list[dict[str, Any]]:
    """Return a deterministic round-robin order across all non-empty categories."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for candidate in candidates:
        groups[candidate["category"]].append(candidate)
    rng = random.Random(seed)
    for values in groups.values():
        values.sort(key=lambda value: (int(value["variation_id"]), value["input"]))
        rng.shuffle(values)

    result: list[dict[str, Any]] = []
    offsets = {name: 0 for name in groups}
    while True:
        added = False
        for name in sorted(groups):
            offset = offsets[name]
            if offset < len(groups[name]):
                result.append(groups[name][offset])
                offsets[name] += 1
                added = True
        if not added:
            return result


def select_balanced(candidates: list[dict[str, Any]], per_category: int, seed: int) -> list[dict[str, Any]]:
    """Compatibility helper retained for callers of the previous builder."""
    counts: Counter = Counter()
    selected = []
    for candidate in balanced_order(candidates, seed):
        if counts[candidate["category"]] < per_category:
            selected.append(candidate)
            counts[candidate["category"]] += 1
    return sorted(selected, key=lambda value: (value["category"], int(value["variation_id"]), value["input"]))


class ResponseCache:
    def __init__(self, path: Path | None):
        self.path = path
        self.values: dict[str, Any] = {}
        if path and path.exists():
            with path.open(encoding="utf-8") as handle:
                for line in handle:
                    if line.strip():
                        record = json.loads(line)
                        self.values[record["key"]] = record["value"]

    def get(self, key: str) -> Any | None:
        return self.values.get(key)

    def put(self, key: str, value: Any) -> None:
        if key in self.values:
            return
        self.values[key] = value
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps({"key": key, "value": value}, ensure_ascii=False, sort_keys=True) + "\n")


def api_post(url: str, ids: list[str], timeout: float, attempts: int = 4) -> Any:
    body = json.dumps({"ids": ids}, ensure_ascii=False).encode()
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "hgvs-variant-recoder-truth-builder/1.1",
        },
        method="POST",
    )
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.load(response)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            retryable = not isinstance(exc, urllib.error.HTTPError) or exc.code == 429 or exc.code >= 500
            if not retryable or attempt + 1 == attempts:
                break
            retry_after = exc.headers.get("Retry-After") if isinstance(exc, urllib.error.HTTPError) else None
            time.sleep(float(retry_after) if retry_after else 2**attempt)
    raise RuntimeError(f"POST failed after {attempts} attempts: {url}: {last_error}")


def response_input(value: Any) -> str | None:
    if isinstance(value, dict):
        if isinstance(value.get("input"), str):
            return value["input"]
        for child in value.values():
            found = response_input(child)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = response_input(child)
            if found:
                return found
    return None


def fetch_recoder(
    inputs: list[str],
    server: str,
    species: str,
    batch_size: int,
    timeout: float,
    cache: ResponseCache,
    mode: str,
) -> dict[str, Any]:
    query = urllib.parse.urlencode({"vcf_string": 1, "fields": "hgvsg,hgvsc,spdi"})
    url = f"{server.rstrip('/')}/variant_recoder/{urllib.parse.quote(species)}?{query}"
    result: dict[str, Any] = {}
    missing: list[str] = []
    for hgvs in inputs:
        key = f"{url}:{hgvs}"
        cached = cache.get(key)
        if cached is None:
            missing.append(hgvs)
        else:
            result[hgvs] = cached
    if mode == "cache":
        for hgvs in missing:
            result[hgvs] = {"cache_error": "cache_miss", "input": hgvs}
        return result

    def fetch_batch(batch: list[str]) -> dict[str, Any]:
        response = api_post(url, batch, timeout)
        if not isinstance(response, list):
            # Variant Recoder returns {"error": ...} when every ID in a request
            # is invalid. Bisect to preserve valid records and identify the
            # individual bad inputs without trusting an error as a gold value.
            if len(batch) == 1:
                return {batch[0]: response}
            middle = len(batch) // 2
            return {**fetch_batch(batch[:middle]), **fetch_batch(batch[middle:])}
        # The documented response is one element per input. Prefer the echoed
        # input, but retain positional association for warning/error-only rows.
        associated: dict[str, Any] = {}
        for index, item in enumerate(response):
            echoed = response_input(item)
            if echoed in batch and echoed not in associated:
                associated[echoed] = item
            elif index < len(batch) and batch[index] not in associated:
                associated[batch[index]] = item
        return {
            hgvs: associated.get(hgvs, {"recoder_error": "missing_response", "input": hgvs})
            for hgvs in batch
        }

    for offset in range(0, len(missing), batch_size):
        batch = missing[offset:offset + batch_size]
        fetched = fetch_batch(batch)
        for hgvs, item in fetched.items():
            result[hgvs] = item
            cache.put(f"{url}:{hgvs}", item)
        if offset + batch_size < len(missing):
            time.sleep(0.1)
    return result


def iter_vcf_strings(value: Any) -> Iterator[str]:
    if isinstance(value, dict):
        raw = value.get("vcf_string")
        if isinstance(raw, str):
            yield raw
        elif isinstance(raw, list):
            yield from (item for item in raw if isinstance(item, str))
        for key, child in value.items():
            if key != "vcf_string":
                yield from iter_vcf_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_vcf_strings(child)


def parse_vcf_string(value: str) -> dict[str, Any] | None:
    """Parse both VEP's CHROM-POS-REF-ALT form and ordinary VCF columns."""
    fields = value.strip().split()
    if len(fields) >= 5 and fields[1].isdigit():
        chrom, pos, ref, alt = fields[0], fields[1], fields[3], fields[4]
    else:
        match = re.fullmatch(r"(.+?)-(\d+)-([ACGTN]+)-([ACGTN]+)", value.strip(), re.IGNORECASE)
        if not match:
            return None
        chrom, pos, ref, alt = match.groups()
    chrom = chrom.removeprefix("chr")
    accession = chrom if chrom in ACCESSION_TO_CHROM else CHROM_TO_ACCESSION.get(chrom)
    if not accession or not re.fullmatch(r"[ACGTN]+", ref, re.IGNORECASE):
        return None
    if not re.fullmatch(r"[ACGTN]+", alt, re.IGNORECASE):
        return None
    return {"chrom": accession, "pos": int(pos), "ref": ref.upper(), "alt": alt.upper()}


def extract_recoder_vcf(response: Any) -> tuple[list[dict[str, Any]], list[str]]:
    parsed: dict[tuple[str, int, str, str], dict[str, Any]] = {}
    invalid: list[str] = []
    for raw in iter_vcf_strings(response):
        value = parse_vcf_string(raw)
        if value is None:
            invalid.append(raw)
        else:
            parsed[vcf_key(value)] = value
    return [parsed[key] for key in sorted(parsed)], invalid


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def make_record(candidate: dict[str, Any], response: Any, source: dict[str, Any]) -> dict[str, Any]:
    alleles, invalid_vcf = extract_recoder_vcf(response)
    error = None if alleles else "no_parseable_primary_assembly_vcf"
    return {
        "schema_version": SCHEMA_VERSION,
        "id": f"ensembl-vr-{candidate['variation_id']}-{hashlib.sha1(candidate['input'].encode()).hexdigest()[:10]}",
        "input": candidate["input"],
        "assembly": "GRCh38",
        "category": candidate["category"],
        "expected": {
            "transcript": candidate["input"].split(":", 1)[0],
            "gene": None,
            "vcf": alleles,
            "ambiguous": len(alleles) > 1,
        },
        "confidence": "ensembl_variant_recoder" if not error else "quarantined",
        "provenance": {
            **source,
            "variation_id": candidate["variation_id"],
            "allele_id": candidate["allele_id"],
            "candidate_gene": candidate["gene"] or None,
            "clinvar_hgvs_type": candidate["hgvs_type"],
            "variant_recoder_response_sha256": json_hash(response),
            "invalid_vcf_strings": invalid_vcf,
            "error": error,
        },
    }


def choose_final(records: list[dict[str, Any]], target_count: int, seed: int) -> list[dict[str, Any]]:
    candidates = [
        {"category": record["category"], "variation_id": record["provenance"]["variation_id"],
         "input": record["input"], "record": record}
        for record in records if record["confidence"] == "ensembl_variant_recoder"
    ]
    return [value["record"] for value in balanced_order(candidates, seed)[:target_count]]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant-summary", type=Path, required=True)
    parser.add_argument("--hgvs4variation", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--quarantine", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--clinvar-release", "--release", dest="clinvar_release", required=True)
    parser.add_argument("--ensembl-release", required=True, help="Release label recorded for reproducibility")
    parser.add_argument("--server", default=DEFAULT_SERVER, help="Use an Ensembl archive REST URL to pin results")
    parser.add_argument("--species", default="homo_sapiens")
    parser.add_argument("--target-count", type=int, default=100)
    parser.add_argument("--candidate-multiplier", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20260727)
    parser.add_argument("--mode", choices=("live", "cache"), default="live")
    parser.add_argument("--cache", type=Path)
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--timeout", type=float, default=60.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.target_count < 1 or args.candidate_multiplier < 1:
        print("--target-count and --candidate-multiplier must be positive", file=sys.stderr)
        return 2
    if not 1 <= args.batch_size <= 200:
        print("--batch-size must be between 1 and the Ensembl POST limit of 200", file=sys.stderr)
        return 2

    candidates, stats = load_candidates(args.variant_summary, args.hgvs4variation)
    attempted = balanced_order(candidates, args.seed)[: args.target_count * args.candidate_multiplier]
    cache = ResponseCache(args.cache)
    try:
        responses = fetch_recoder(
            [candidate["input"] for candidate in attempted],
            args.server,
            args.species,
            args.batch_size,
            args.timeout,
            cache,
            args.mode,
        )
    except (RuntimeError, ValueError) as exc:
        print(f"Variant Recoder infrastructure error: {exc}", file=sys.stderr)
        return 2

    source = {
        "oracle": "Ensembl Variant Recoder",
        "ensembl_release": args.ensembl_release,
        "variant_recoder_server": args.server,
        "variant_recoder_options": {"species": args.species, "vcf_string": 1, "fields": "hgvsg,hgvsc,spdi"},
        "clinvar_release": args.clinvar_release,
        "variant_summary_sha256": sha256(args.variant_summary),
        "hgvs4variation_sha256": sha256(args.hgvs4variation),
    }
    processed = [make_record(candidate, responses[candidate["input"]], source) for candidate in attempted]
    gold = choose_final(processed, args.target_count, args.seed)
    gold_ids = {record["id"] for record in gold}
    quarantined = [
        record for record in processed
        if record["confidence"] == "quarantined" and record["id"] not in gold_ids
    ]
    write_jsonl(args.output, gold)
    write_jsonl(args.quarantine, quarantined)

    report = {
        "schema_version": SCHEMA_VERSION,
        "sources": source,
        "configuration": {
            "target_count": args.target_count,
            "candidate_multiplier": args.candidate_multiplier,
            "seed": args.seed,
            "mode": args.mode,
            "batch_size": args.batch_size,
        },
        "counts": {
            **stats,
            "attempted": len(attempted),
            "recoder_accepted": sum(record["confidence"] == "ensembl_variant_recoder" for record in processed),
            "written": len(gold),
            "quarantined": len(quarantined),
            "written_by_category": dict(Counter(record["category"] for record in gold)),
        },
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report["counts"], ensure_ascii=False, sort_keys=True))
    if len(gold) < args.target_count:
        print(
            f"only {len(gold)}/{args.target_count} valid cases were produced; "
            "increase --candidate-multiplier",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
