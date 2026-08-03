#!/usr/bin/env python3
"""Build an HGVS -> normalized GRCh38 VCF truth set from ClinVar."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any


TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from build_truth_set import (  # noqa: E402
    INPUT_KINDS,
    SCHEMA_VERSION,
    balanced_order,
    load_candidates,
    sha256,
    vcf_key,
    write_jsonl,
)


def normalize_vcfs(
    candidates: list[dict[str, Any]],
    reference_fasta: Path,
    bcftools: str,
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    """Left-align and normalize candidate VCF alleles with bcftools."""
    candidate_by_id = {f"candidate-{index}": candidate for index, candidate in enumerate(candidates)}
    with tempfile.TemporaryDirectory(prefix="clinvar-truth-") as temporary_dir:
        input_vcf = Path(temporary_dir) / "clinvar.vcf"
        with input_vcf.open("w", encoding="utf-8") as handle:
            handle.write("##fileformat=VCFv4.3\n")
            for contig in sorted({vcf_key(candidate["vcf"])[0] for candidate in candidates}):
                handle.write(f"##contig=<ID={contig}>\n")
            handle.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
            for record_id, candidate in candidate_by_id.items():
                chrom, pos, ref, alt = vcf_key(candidate["vcf"])
                handle.write(f"{chrom}\t{pos}\t{record_id}\t{ref}\t{alt}\t.\tPASS\t.\n")

        command = [
            bcftools,
            "norm",
            "--fasta-ref",
            str(reference_fasta),
            "--check-ref",
            "x",
            "--multiallelics",
            "-any",
            "--output-type",
            "v",
            str(input_vcf),
        ]
        completed = subprocess.run(command, text=True, capture_output=True, check=False)

    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "no diagnostic output"
        raise RuntimeError(f"bcftools norm failed with exit code {completed.returncode}: {detail}")

    normalized: dict[str, dict[tuple[str, int, str, str], dict[str, Any]]] = {}
    invalid_output_rows: list[str] = []
    for line in completed.stdout.splitlines():
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) < 5 or fields[2] not in candidate_by_id:
            invalid_output_rows.append(line)
            continue
        chrom, pos, record_id, ref, alt_field = fields[:5]
        if not pos.isdigit():
            invalid_output_rows.append(line)
            continue
        for alt in alt_field.split(","):
            value = {
                "chrom": chrom.removeprefix("chr"),
                "pos": int(pos),
                "ref": ref.upper(),
                "alt": alt.upper(),
            }
            if not re.fullmatch(r"[ACGTN]+", value["ref"], re.IGNORECASE) or not re.fullmatch(
                r"[ACGTN]+", value["alt"], re.IGNORECASE
            ):
                invalid_output_rows.append(line)
                continue
            normalized.setdefault(record_id, {})[vcf_key(value)] = value

    by_input = {
        candidate_by_id[record_id]["input"]: [values[key] for key in sorted(values)]
        for record_id, values in normalized.items()
    }
    diagnostics = {
        "bcftools_stderr": completed.stderr.strip(),
        "invalid_output_rows": invalid_output_rows,
        "input_records": len(candidates),
        "output_records": sum(len(values) for values in normalized.values()),
    }
    return by_input, diagnostics


def resolved_transcript(candidate: dict[str, Any]) -> str | None:
    if candidate["input_kind"].startswith("gene_"):
        mane = candidate["mane_select"]
        return mane["refseq_nuc"] if mane else None
    return candidate["source_clinvar_hgvs"].split(":", 1)[0]


def make_clinvar_record(
    candidate: dict[str, Any],
    normalized_vcf: list[dict[str, Any]],
    source: dict[str, Any],
) -> dict[str, Any]:
    error = None if normalized_vcf else "bcftools_norm_rejected_or_missing"
    raw_vcf = {
        "chrom": candidate["vcf"]["chrom"],
        "pos": candidate["vcf"]["pos"],
        "ref": candidate["vcf"]["ref"],
        "alt": candidate["vcf"]["alt"],
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "id": f"clinvar-{candidate['variation_id']}-{hashlib.sha1(candidate['input'].encode()).hexdigest()[:10]}",
        "input": candidate["input"],
        "input_kind": candidate["input_kind"],
        "assembly": "GRCh38",
        "category": candidate["category"],
        "expected": {
            "transcript": resolved_transcript(candidate),
            "gene": candidate["gene"] if candidate["input_kind"].startswith("gene_") else None,
            "vcf": normalized_vcf,
            "ambiguous": len(normalized_vcf) > 1,
        },
        "confidence": "clinvar_bcftools_normalized" if not error else "quarantined",
        "provenance": {
            **source,
            "variation_id": candidate["variation_id"],
            "allele_id": candidate["allele_id"],
            "candidate_gene": candidate["gene"] or None,
            "clinvar_hgvs_type": candidate["hgvs_type"],
            "input_kind": candidate["input_kind"],
            "clinvar_source_hgvs": candidate["source_clinvar_hgvs"],
            "mane_select": candidate["mane_select"],
            "clinvar_vcf_before_normalization": raw_vcf,
            "error": error,
        },
    }


def choose_final(records: list[dict[str, Any]], target_count: int, seed: int) -> list[dict[str, Any]]:
    candidates = [
        {
            "category": record["category"],
            "input_kind": record["input_kind"],
            "variation_id": record["provenance"]["variation_id"],
            "input": record["input"],
            "record": record,
        }
        for record in records
        if record["confidence"] == "clinvar_bcftools_normalized"
    ]
    return [value["record"] for value in balanced_order(candidates, seed)[:target_count]]


def bcftools_version(executable: str) -> str:
    completed = subprocess.run(
        [executable, "--version"],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or f"cannot run {executable}")
    return completed.stdout.splitlines()[0].strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant-summary", type=Path, required=True)
    parser.add_argument("--hgvs4variation", type=Path, required=True)
    parser.add_argument("--mane-summary", type=Path, required=True)
    parser.add_argument("--reference-fasta", type=Path, required=True)
    parser.add_argument("--clinvar-release", required=True)
    parser.add_argument("--mane-release", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--quarantine", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--target-count", type=int, default=100)
    parser.add_argument("--candidate-multiplier", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20260727)
    parser.add_argument("--bcftools", default="bcftools")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.target_count < 1 or args.candidate_multiplier < 1:
        print("--target-count and --candidate-multiplier must be positive", file=sys.stderr)
        return 2
    if not args.reference_fasta.is_file():
        print(f"reference FASTA not found: {args.reference_fasta}", file=sys.stderr)
        return 2
    if args.reference_fasta.suffix == ".gz":
        print("reference FASTA must be uncompressed for indexed random access", file=sys.stderr)
        return 2
    executable = shutil.which(args.bcftools)
    if not executable:
        print(f"bcftools executable not found: {args.bcftools}", file=sys.stderr)
        return 2

    attempt_limit = args.target_count * args.candidate_multiplier
    candidates, stats = load_candidates(
        args.variant_summary,
        args.hgvs4variation,
        args.mane_summary,
        limit_per_group=attempt_limit,
        seed=args.seed,
    )
    attempted = balanced_order(candidates, args.seed)[:attempt_limit]
    try:
        version = bcftools_version(executable)
        normalized, diagnostics = normalize_vcfs(attempted, args.reference_fasta, executable)
    except RuntimeError as exc:
        print(f"VCF normalization error: {exc}", file=sys.stderr)
        return 2

    source = {
        "oracle": "ClinVar VCF columns normalized with bcftools",
        "clinvar_release": args.clinvar_release,
        "mane_release": args.mane_release,
        "variant_summary_sha256": sha256(args.variant_summary),
        "hgvs4variation_sha256": sha256(args.hgvs4variation),
        "mane_summary_sha256": sha256(args.mane_summary),
        "reference_fasta_sha256": sha256(args.reference_fasta),
        "bcftools_version": version,
        "normalization_options": ["--fasta-ref", "--check-ref x", "--multiallelics -any"],
    }
    processed = [
        make_clinvar_record(candidate, normalized.get(candidate["input"], []), source)
        for candidate in attempted
    ]
    gold = choose_final(processed, args.target_count, args.seed)
    quarantined = [record for record in processed if record["confidence"] == "quarantined"]
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
        },
        "normalization": diagnostics,
        "counts": {
            **stats,
            "attempted": len(attempted),
            "normalized": sum(record["confidence"] == "clinvar_bcftools_normalized" for record in processed),
            "written": len(gold),
            "quarantined": len(quarantined),
            "written_by_input_kind": dict(Counter(record["input_kind"] for record in gold)),
            "written_by_category": dict(Counter(record["category"] for record in gold)),
        },
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
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
