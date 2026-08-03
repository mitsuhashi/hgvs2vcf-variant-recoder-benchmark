#!/usr/bin/env python3
"""Build a balanced HGVS -> GRCh38 VCF truth set using Ensembl Variant Recoder.

ClinVar is used only as a reproducible source for three input forms:
GENE:p., GENE:c., and unversioned NM_:c.  Expected VCF alleles come
exclusively from Ensembl Variant Recoder.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import gzip
import hashlib
import heapq
import http.client
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


SCHEMA_VERSION = "1.2"
DEFAULT_SERVER = "https://rest.ensembl.org"
INPUT_KINDS = ("gene_hgvsp", "gene_hgvsc", "refseq_hgvsc")
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
        fieldnames = None
        for line in handle:
            if "\t" in line:
                fieldnames = next(csv.reader([line], delimiter="\t"))
                break
        if not fieldnames:
            raise ValueError(f"{path}: header is missing")
        reader = csv.DictReader(handle, delimiter="\t", fieldnames=fieldnames)
        normalized = [canonical_header(name) for name in fieldnames]
        for raw in reader:
            yield {
                normalized[index]: (raw.get(name) or "").strip()
                for index, name in enumerate(fieldnames)
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


def candidate_contig_from_summary(row: dict[str, str]) -> str | None:
    """Read only the primary-assembly contig used to join candidate HGVS rows."""
    if first(row, "Assembly") not in {"GRCh38", "GRCh38.p14"}:
        return None
    contig = first(row, "ChromosomeAccession")
    return contig if contig in ACCESSION_TO_CHROM else None


def supported_transcript_hgvs_type(value: str) -> bool:
    lowered = value.lower()
    if any(token in lowered for token in ("non-validated", "uncertain", "previous", "other", "protein")):
        return False
    return "coding" in lowered or "non-coding" in lowered or "noncoding" in lowered


def supported_protein_hgvs_type(value: str) -> bool:
    lowered = value.lower()
    if any(token in lowered for token in ("non-validated", "uncertain", "previous", "other")):
        return False
    return "protein" in lowered


def valid_gene_symbol(value: str) -> bool:
    return bool(value and value != "-" and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", value))


def load_mane_select(path: Path) -> dict[str, dict[str, str]]:
    """Load one pinned MANE summary and index MANE Select rows by gene symbol."""
    result: dict[str, dict[str, str]] = {}
    for row in read_tsv(path):
        if first(row, "MANE_status", "MANE status") != "MANE Select":
            continue
        symbol = first(row, "symbol", "GeneSymbol")
        refseq_nuc = first(row, "RefSeq_nuc")
        refseq_prot = first(row, "RefSeq_prot")
        ensembl_nuc = first(row, "Ensembl_nuc")
        if not valid_gene_symbol(symbol) or not refseq_nuc:
            continue
        result[symbol] = {
            "refseq_nuc": refseq_nuc,
            "refseq_prot": refseq_prot,
            "ensembl_nuc": ensembl_nuc,
        }
    return result


def category(hgvs: str) -> str:
    body = hgvs.split(":", 1)[-1]
    if body.startswith("p."):
        context = "protein"
    elif body.startswith("n."):
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
    elif ">" in body or (
        body.startswith("p.") and re.search(r"p\.[A-Za-z*]{3}\d+[A-Za-z*]{3}", body)
    ):
        operation = "substitution"
    else:
        operation = "other"
    return f"{context}_{operation}"


def load_candidates(
    variant_summary: Path,
    hgvs_file: Path,
    mane_summary: Path,
    *,
    limit_per_group: int | None = None,
    seed: int = 0,
) -> tuple[list[dict[str, Any]], Counter]:
    """Join ClinVar tables and derive the three supported Variant Recoder inputs."""
    mane_select = load_mane_select(mane_summary)
    locations: dict[str, dict[str, Any]] = {}
    stats: Counter = Counter({"mane_select_genes": len(mane_select)})
    for row in read_tsv(variant_summary):
        stats["variant_summary_rows"] += 1
        variation_id = first(row, "VariationID")
        contig = candidate_contig_from_summary(row)
        if not variation_id or not contig:
            continue
        if variation_id in locations and locations[variation_id]["contig"] != contig:
            locations[variation_id]["conflicting_location"] = True
            continue
        locations[variation_id] = {
            "contig": contig,
            "gene": first(row, "GeneSymbol"),
            "allele_id": first(row, "AlleleID"),
            "variant_type": first(row, "Type"),
        }

    transcript_expressions: dict[str, list[tuple[str, str]]] = defaultdict(list)
    protein_expressions: dict[str, list[tuple[str, str]]] = defaultdict(list)
    genomic: dict[str, set[str]] = defaultdict(set)
    for row in read_tsv(hgvs_file):
        stats["hgvs_rows"] += 1
        variation_id = first(row, "VariationID")
        hgvs_type = first(row, "TypeOfHGVS", "Type_of_HGVS", "Type")
        nucleotide = first(row, "NucleotideExpression", "NucleotideHGVS", "HGVS")
        protein = first(row, "ProteinExpression", "ProteinHGVS")
        if not protein and supported_protein_hgvs_type(hgvs_type):
            # Compatibility with older four-column exports and local fixtures.
            protein = nucleotide
        # Rows without a usable GRCh38 VCF location can never become candidates.
        # Filtering them here avoids retaining millions of irrelevant HGVS rows.
        if not variation_id or variation_id not in locations:
            continue
        if nucleotide and re.match(r"^NC_\d+\.\d+:g\.", nucleotide):
            genomic[variation_id].add(nucleotide)
        if nucleotide and supported_transcript_hgvs_type(hgvs_type) and re.match(
            r"^(?:NM_|NR_|ENST)\d+\.\d+:[cn]\.", nucleotide
        ):
            transcript_expressions[variation_id].append((nucleotide, hgvs_type))
        if protein and (
            supported_transcript_hgvs_type(hgvs_type)
            or supported_protein_hgvs_type(hgvs_type)
        ) and re.match(
            r"^(?:NP_|ENSP)\d+\.\d+:p\.", protein
        ):
            protein_expressions[variation_id].append((protein, hgvs_type))

    candidates: list[dict[str, Any]] = []
    retained: dict[tuple[str, str], list[tuple[int, str, dict[str, Any]]]] = defaultdict(list)
    seen_inputs: set[str] = set()

    def retain(candidate: dict[str, Any]) -> None:
        if limit_per_group is None:
            candidates.append(candidate)
            return
        group = (candidate["input_kind"], candidate["category"])
        priority = int.from_bytes(
            hashlib.sha256(f"{seed}\0{candidate['input']}".encode()).digest(),
            "big",
        )
        item = (-priority, candidate["input"], candidate)
        heap = retained[group]
        if len(heap) < limit_per_group:
            heapq.heappush(heap, item)
        elif priority < -heap[0][0]:
            heapq.heapreplace(heap, item)

    def process_variation(
        variation_id: str,
        transcripts: list[tuple[str, str]],
        proteins: list[tuple[str, str]],
        genomic_hgvs: set[str],
    ) -> None:
        location = locations.pop(variation_id, None)
        if not location or location.get("conflicting_location"):
            return
        matching_genomic = {
            value for value in genomic_hgvs
            if value.startswith(location["contig"] + ":g.")
        }
        if not matching_genomic:
            stats["rejected_missing_genomic_hgvs"] += (
                len(transcripts) + len(proteins)
            )
            return

        derived: list[tuple[str, str, str, str]] = []
        gene = location["gene"]
        mane = mane_select.get(gene)
        for source_hgvs, hgvs_type in transcripts:
            accession, body = source_hgvs.split(":", 1)
            if body.startswith("c.") and mane and accession == mane["refseq_nuc"]:
                derived.append((f"{gene}:{body}", "gene_hgvsc", source_hgvs, hgvs_type))
            unversioned = re.fullmatch(r"(NM_\d+)\.\d+:(c\..+)", source_hgvs)
            if unversioned:
                derived.append(
                    (
                        f"{unversioned.group(1)}:{unversioned.group(2)}",
                        "refseq_hgvsc",
                        source_hgvs,
                        hgvs_type,
                    )
                )
        if mane and mane["refseq_prot"]:
            for source_hgvs, hgvs_type in proteins:
                accession, body = source_hgvs.split(":", 1)
                if accession == mane["refseq_prot"]:
                    derived.append((f"{gene}:{body}", "gene_hgvsp", source_hgvs, hgvs_type))

        for hgvs, input_kind, source_hgvs, hgvs_type in derived:
            if hgvs in seen_inputs:
                stats["rejected_duplicate_input"] += 1
                continue
            seen_inputs.add(hgvs)
            candidate = {
                "variation_id": variation_id,
                "input": hgvs,
                "input_kind": input_kind,
                "source_clinvar_hgvs": source_hgvs,
                "oracle_hgvs": source_hgvs if input_kind.startswith("gene_") else hgvs,
                "mane_select": mane if input_kind.startswith("gene_") else None,
                "hgvs_type": hgvs_type,
                "genomic_hgvs": matching_genomic,
                **location,
                "category": category(hgvs),
            }
            stats["candidates"] += 1
            stats[f"candidates_{input_kind}"] += 1
            retain(candidate)

    # Pop processed entries so the large HGVS indexes shrink throughout the
    # join instead of remaining live while candidate dictionaries are built.
    while transcript_expressions:
        variation_id, transcripts = transcript_expressions.popitem()
        process_variation(
            variation_id,
            transcripts,
            protein_expressions.pop(variation_id, []),
            genomic.pop(variation_id, set()),
        )
    while protein_expressions:
        variation_id, proteins = protein_expressions.popitem()
        process_variation(
            variation_id,
            [],
            proteins,
            genomic.pop(variation_id, set()),
        )

    genomic.clear()
    locations.clear()
    seen_inputs.clear()

    if limit_per_group is not None:
        candidates = [item[2] for heap in retained.values() for item in heap]
        stats["retained_candidates"] = len(candidates)
    for name in INPUT_KINDS:
        stats.setdefault(f"candidates_{name}", 0)
    return candidates, stats


def balanced_order(candidates: list[dict[str, Any]], seed: int) -> list[dict[str, Any]]:
    """Balance input forms first, then variant categories within each form."""
    input_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for candidate in candidates:
        input_groups[candidate.get("input_kind", "")].append(candidate)
    rng = random.Random(seed)

    def order_categories(values: list[dict[str, Any]]) -> list[dict[str, Any]]:
        category_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for value in values:
            category_groups[value["category"]].append(value)
        for category_values in category_groups.values():
            category_values.sort(key=lambda value: (int(value["variation_id"]), value["input"]))
            rng.shuffle(category_values)
        ordered: list[dict[str, Any]] = []
        offsets = {name: 0 for name in category_groups}
        while True:
            added = False
            for name in sorted(category_groups):
                offset = offsets[name]
                if offset < len(category_groups[name]):
                    ordered.append(category_groups[name][offset])
                    offsets[name] += 1
                    added = True
            if not added:
                return ordered

    queues = {name: order_categories(values) for name, values in input_groups.items()}
    result: list[dict[str, Any]] = []
    offsets = {name: 0 for name in queues}
    while True:
        added = False
        for name in sorted(queues):
            offset = offsets[name]
            if offset < len(queues[name]):
                result.append(queues[name][offset])
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


class ApiPostError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        timed_out: bool = False,
        bad_request: bool = False,
        transient: bool = False,
    ):
        super().__init__(message)
        self.timed_out = timed_out
        self.bad_request = bad_request
        self.transient = transient


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
    attempts_made = 0
    timed_out = False
    bad_request = False
    for attempt in range(attempts):
        attempts_made = attempt + 1
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.load(response)
        except (
            urllib.error.URLError,
            TimeoutError,
            json.JSONDecodeError,
            http.client.RemoteDisconnected,
        ) as exc:
            last_error = exc
            bad_request = isinstance(exc, urllib.error.HTTPError) and exc.code == 400
            timed_out = isinstance(exc, TimeoutError) or isinstance(
                getattr(exc, "reason", None), TimeoutError
            )
            retryable = not isinstance(exc, urllib.error.HTTPError) or exc.code == 429 or exc.code >= 500
            # A large valid batch can exceed the REST response timeout. Let the
            # caller bisect it immediately; singleton requests still get retries.
            if timed_out:
                break
            if not retryable or attempts_made == attempts:
                break
            retry_after = exc.headers.get("Retry-After") if isinstance(exc, urllib.error.HTTPError) else None
            time.sleep(float(retry_after) if retry_after else 2**attempt)
    raise ApiPostError(
        f"POST failed after {attempts_made} attempt(s): {url}: {last_error}",
        timed_out=timed_out,
        bad_request=bad_request,
        transient=retryable,
    )


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


def recoder_request_url(server: str, species: str, hgvs: str) -> str:
    fields = "hgvsc" if re.match(r"^NM_\d+:[cn]\.", hgvs) else "spdi"
    query = urllib.parse.urlencode({"vcf_string": 1, "fields": fields})
    return f"{server.rstrip('/')}/variant_recoder/{urllib.parse.quote(species)}?{query}"


def fetch_recoder(
    inputs: list[str],
    server: str,
    species: str,
    batch_size: int,
    timeout: float,
    cache: ResponseCache,
    mode: str,
    workers: int = 1,
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    missing_by_url: dict[str, list[str]] = defaultdict(list)
    for hgvs in inputs:
        # Only unversioned RefSeq inputs need hgvsc to discover the transcript
        # version chosen by Variant Recoder. spdi keeps every other response
        # small while vcf_string remains available through its own option.
        url = recoder_request_url(server, species, hgvs)
        key = f"{url}:{hgvs}"
        cached = cache.get(key)
        if cached is None:
            missing_by_url[url].append(hgvs)
        else:
            result[hgvs] = cached
    if mode == "cache":
        for missing in missing_by_url.values():
            for hgvs in missing:
                result[hgvs] = {"cache_error": "cache_miss", "input": hgvs}
        return result

    def fetch_batch(url: str, batch: list[str]) -> dict[str, Any]:
        try:
            response = api_post(url, batch, timeout)
        except ApiPostError as exc:
            if exc.transient and not exc.timed_out:
                return {
                    hgvs: {
                        "error": str(exc),
                        "input": hgvs,
                        "transient_error": True,
                    }
                    for hgvs in batch
                }
            if not (exc.timed_out or exc.bad_request):
                raise
            if len(batch) == 1:
                return {
                    batch[0]: {
                        "error": str(exc),
                        "input": batch[0],
                        "transient_error": exc.timed_out,
                    }
                }
            middle = len(batch) // 2
            return {
                **fetch_batch(url, batch[:middle]),
                **fetch_batch(url, batch[middle:]),
            }
        if not isinstance(response, list):
            # Variant Recoder returns {"error": ...} when every ID in a request
            # is invalid. Bisect to preserve valid records and identify the
            # individual bad inputs without trusting an error as a gold value.
            if len(batch) == 1:
                return {batch[0]: response}
            middle = len(batch) // 2
            return {
                **fetch_batch(url, batch[:middle]),
                **fetch_batch(url, batch[middle:]),
            }
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

    def store_fetched(url: str, fetched: dict[str, Any]) -> None:
        for hgvs, item in fetched.items():
            result[hgvs] = item
            if not (isinstance(item, dict) and item.get("transient_error")):
                cache.put(f"{url}:{hgvs}", item)

    for url, missing in missing_by_url.items():
        batches = [
            missing[offset:offset + batch_size]
            for offset in range(0, len(missing), batch_size)
        ]
        if workers == 1:
            for index, batch in enumerate(batches):
                store_fetched(url, fetch_batch(url, batch))
                if index + 1 < len(batches):
                    time.sleep(0.1)
            continue
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(fetch_batch, url, batch) for batch in batches]
            for future in concurrent.futures.as_completed(futures):
                fetched = future.result()
                store_fetched(url, fetched)
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


def iter_named_strings(value: Any, field: str) -> Iterator[str]:
    if isinstance(value, dict):
        raw = value.get(field)
        if isinstance(raw, str):
            yield raw
        elif isinstance(raw, list):
            yield from (item for item in raw if isinstance(item, str))
        for key, child in value.items():
            if key != field:
                yield from iter_named_strings(child, field)
    elif isinstance(value, list):
        for child in value:
            yield from iter_named_strings(child, field)


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


def resolved_refseq_transcript(candidate: dict[str, Any], response: Any) -> str | None:
    if candidate["input_kind"].startswith("gene_"):
        mane = candidate["mane_select"]
        return mane["refseq_nuc"] if mane else None
    accession, _ = candidate["input"].split(":", 1)
    pattern = re.compile(rf"^{re.escape(accession)}\.\d+:")
    matches = sorted(value for value in iter_named_strings(response, "hgvsc") if pattern.match(value))
    return matches[0].split(":", 1)[0] if matches else None


def make_record(
    candidate: dict[str, Any],
    input_response: Any,
    oracle_response: Any,
    source: dict[str, Any],
) -> dict[str, Any]:
    input_alleles, input_invalid_vcf = extract_recoder_vcf(input_response)
    alleles, invalid_vcf = extract_recoder_vcf(oracle_response)
    error = None
    if not input_alleles:
        error = "input_has_no_parseable_primary_assembly_vcf"
    elif not alleles:
        error = "mane_or_refseq_has_no_parseable_primary_assembly_vcf"
    elif candidate["input_kind"].startswith("gene_"):
        input_keys = {vcf_key(value) for value in input_alleles}
        oracle_keys = {vcf_key(value) for value in alleles}
        if not oracle_keys.issubset(input_keys):
            error = "mane_vcf_not_returned_for_gene_input"
    transcript = resolved_refseq_transcript(candidate, oracle_response)
    if not error and not transcript:
        error = "resolved_transcript_not_found"
    return {
        "schema_version": SCHEMA_VERSION,
        "id": f"ensembl-vr-{candidate['variation_id']}-{hashlib.sha1(candidate['input'].encode()).hexdigest()[:10]}",
        "input": candidate["input"],
        "input_kind": candidate["input_kind"],
        "assembly": "GRCh38",
        "category": candidate["category"],
        "expected": {
            "transcript": transcript,
            "gene": candidate["gene"] if candidate["input_kind"].startswith("gene_") else None,
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
            "input_kind": candidate["input_kind"],
            "clinvar_source_hgvs": candidate["source_clinvar_hgvs"],
            "oracle_hgvs": candidate["oracle_hgvs"],
            "mane_select": candidate["mane_select"],
            "variant_recoder_response_sha256": json_hash(input_response),
            "variant_recoder_oracle_response_sha256": json_hash(oracle_response),
            "input_invalid_vcf_strings": input_invalid_vcf,
            "invalid_vcf_strings": invalid_vcf,
            "error": error,
        },
    }


def choose_final(records: list[dict[str, Any]], target_count: int, seed: int) -> list[dict[str, Any]]:
    candidates = [
        {"category": record["category"], "input_kind": record["input_kind"],
         "variation_id": record["provenance"]["variation_id"], "input": record["input"],
         "record": record}
        for record in records if record["confidence"] == "ensembl_variant_recoder"
    ]
    return [value["record"] for value in balanced_order(candidates, seed)[:target_count]]


def candidate_cache_signature(
    variant_summary: Path,
    hgvs_file: Path,
    mane_summary: Path,
    attempt_limit: int,
    seed: int,
) -> dict[str, Any]:
    def identity(path: Path) -> dict[str, Any]:
        stat = path.stat()
        return {
            "path": str(path.resolve()),
            "size": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
        }

    return {
        "version": 2,
        "attempt_limit": attempt_limit,
        "seed": seed,
        "variant_summary": identity(variant_summary),
        "hgvs4variation": identity(hgvs_file),
        "mane_summary": identity(mane_summary),
    }


def load_candidate_cache(
    path: Path | None,
    signature: dict[str, Any],
) -> tuple[list[dict[str, Any]], Counter] | None:
    if not path or not path.is_file():
        return None
    try:
        cached = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if cached.get("signature") != signature:
        return None
    attempted = cached.get("attempted")
    stats = cached.get("stats")
    if not isinstance(attempted, list) or not isinstance(stats, dict):
        return None
    for candidate in attempted:
        if not isinstance(candidate, dict):
            return None
        candidate["genomic_hgvs"] = set(candidate.get("genomic_hgvs", []))
    return attempted, Counter(stats)


def write_candidate_cache(
    path: Path | None,
    signature: dict[str, Any],
    attempted: list[dict[str, Any]],
    stats: Counter,
) -> None:
    if not path:
        return
    serializable = []
    for candidate in attempted:
        value = dict(candidate)
        value["genomic_hgvs"] = sorted(candidate.get("genomic_hgvs", []))
        serializable.append(value)
    payload = {
        "signature": signature,
        "stats": dict(stats),
        "attempted": serializable,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant-summary", type=Path, required=True)
    parser.add_argument("--hgvs4variation", type=Path, required=True)
    parser.add_argument("--mane-summary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--quarantine", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--clinvar-release", "--release", dest="clinvar_release", required=True)
    parser.add_argument("--ensembl-release", required=True, help="Release label recorded for reproducibility")
    parser.add_argument("--mane-release", required=True, help="Pinned MANE release used for gene-symbol inputs")
    parser.add_argument("--server", default=DEFAULT_SERVER, help="Use an Ensembl archive REST URL to pin results")
    parser.add_argument("--species", default="homo_sapiens")
    parser.add_argument("--target-count", type=int, default=100)
    parser.add_argument("--candidate-multiplier", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20260727)
    parser.add_argument("--mode", choices=("live", "cache"), default="live")
    parser.add_argument("--cache", type=Path)
    parser.add_argument("--candidate-cache", type=Path)
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--workers", type=int, default=1)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.target_count < 1 or args.candidate_multiplier < 1:
        print("--target-count and --candidate-multiplier must be positive", file=sys.stderr)
        return 2
    if not 1 <= args.batch_size <= 200:
        print("--batch-size must be between 1 and the Ensembl POST limit of 200", file=sys.stderr)
        return 2
    if not 1 <= args.workers <= 8:
        print("--workers must be between 1 and 8", file=sys.stderr)
        return 2

    attempt_limit = args.target_count * args.candidate_multiplier
    candidate_signature = candidate_cache_signature(
        args.variant_summary,
        args.hgvs4variation,
        args.mane_summary,
        attempt_limit,
        args.seed,
    )
    cached_candidates = load_candidate_cache(args.candidate_cache, candidate_signature)
    if cached_candidates:
        attempted, stats = cached_candidates
    else:
        candidates, stats = load_candidates(
            args.variant_summary,
            args.hgvs4variation,
            args.mane_summary,
            limit_per_group=attempt_limit,
            seed=args.seed,
        )
        attempted = balanced_order(candidates, args.seed)[:attempt_limit]
        write_candidate_cache(
            args.candidate_cache,
            candidate_signature,
            attempted,
            stats,
        )
    cache = ResponseCache(args.cache)
    def is_cached(hgvs: str) -> bool:
        url = recoder_request_url(args.server, args.species, hgvs)
        return cache.get(f"{url}:{hgvs}") is not None

    missing_counterparts = []
    for candidate in attempted:
        input_hgvs = candidate["input"]
        oracle_hgvs = candidate["oracle_hgvs"]
        input_cached = is_cached(input_hgvs)
        oracle_cached = is_cached(oracle_hgvs)
        if input_cached and not oracle_cached:
            missing_counterparts.append(oracle_hgvs)
        elif oracle_cached and not input_cached:
            missing_counterparts.append(input_hgvs)
    paired_inputs = [
        hgvs
        for candidate in attempted
        for hgvs in (candidate["oracle_hgvs"], candidate["input"])
    ]
    query_inputs = list(dict.fromkeys(missing_counterparts + paired_inputs))
    try:
        responses = fetch_recoder(
            query_inputs,
            args.server,
            args.species,
            args.batch_size,
            args.timeout,
            cache,
            args.mode,
            args.workers,
        )
    except (RuntimeError, ValueError) as exc:
        print(f"Variant Recoder infrastructure error: {exc}", file=sys.stderr)
        return 2

    source = {
        "oracle": "Ensembl Variant Recoder",
        "ensembl_release": args.ensembl_release,
        "variant_recoder_server": args.server,
        "variant_recoder_options": {
            "species": args.species,
            "vcf_string": 1,
            "fields": {
                "unversioned_refseq": "hgvsc",
                "other_inputs": "spdi",
            },
        },
        "clinvar_release": args.clinvar_release,
        "mane_release": args.mane_release,
        "variant_summary_sha256": sha256(args.variant_summary),
        "hgvs4variation_sha256": sha256(args.hgvs4variation),
        "mane_summary_sha256": sha256(args.mane_summary),
    }
    processed = [
        make_record(
            candidate,
            responses[candidate["input"]],
            responses[candidate["oracle_hgvs"]],
            source,
        )
        for candidate in attempted
    ]
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
            "input_kinds": list(INPUT_KINDS),
            "seed": args.seed,
            "mode": args.mode,
            "batch_size": args.batch_size,
            "workers": args.workers,
        },
        "counts": {
            **stats,
            "attempted": len(attempted),
            "variant_recoder_queries": len(query_inputs),
            "recoder_accepted": sum(record["confidence"] == "ensembl_variant_recoder" for record in processed),
            "written": len(gold),
            "quarantined": len(quarantined),
            "written_by_input_kind": dict(Counter(record["input_kind"] for record in gold)),
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
