#!/usr/bin/env python3
"""Evaluate hgvs2vcf-cdot-lmdb HTTP responses against a JSONL truth set."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


GOLD_CONFIDENCES = {
    "ensembl_variant_recoder",
    "clinvar_bcftools_normalized",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            record = json.loads(line)
            if "id" not in record or "input" not in record or "expected" not in record:
                raise ValueError(f"{path}:{line_number}: id, input and expected are required")
            records.append(record)
    return records


def post_batch(base_url: str, inputs: list[str], timeout: float) -> list[dict[str, Any]]:
    request = urllib.request.Request(
        base_url.rstrip("/") + "/decode",
        data=json.dumps({"hgvs": inputs}, ensure_ascii=False).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.load(response)
    if not isinstance(payload, list):
        raise ValueError(f"POST /decode returned {type(payload).__name__}, expected a JSON array")
    return payload


def normalized_vcf(rows: Iterable[dict[str, Any]]) -> list[tuple[str, int, str, str]]:
    values = []
    for row in rows:
        values.append(
            (
                str(row["chrom"]).removeprefix("chr"),
                int(row["pos"]),
                str(row["ref"]).upper(),
                str(row["alt"]).upper(),
            )
        )
    return sorted(values)


def compare_case(case: dict[str, Any], observed: dict[str, Any], check_gene: bool) -> dict[str, Any]:
    expected = case["expected"]
    differences: dict[str, Any] = {}
    if "error" in expected:
        if "error" not in observed:
            differences["error"] = {"expected": expected["error"], "observed": None}
    elif "error" in observed:
        differences["error"] = {"expected": None, "observed": observed["error"]}
    else:
        expected_vcf = normalized_vcf(expected.get("vcf", []))
        observed_vcf = normalized_vcf(observed.get("vcf", []))
        if expected_vcf != observed_vcf:
            differences["vcf"] = {"expected": expected_vcf, "observed": observed_vcf}
        if expected.get("transcript") is not None and expected["transcript"] != observed.get("transcript"):
            differences["transcript"] = {
                "expected": expected["transcript"],
                "observed": observed.get("transcript"),
            }
        if "ambiguous" in expected and bool(expected["ambiguous"]) != bool(observed.get("ambiguous")):
            differences["ambiguous"] = {
                "expected": bool(expected["ambiguous"]),
                "observed": bool(observed.get("ambiguous")),
            }
        if check_gene and expected.get("gene") is not None and expected["gene"] != observed.get("gene"):
            differences["gene"] = {"expected": expected["gene"], "observed": observed.get("gene")}
    return {
        "id": case["id"],
        "input": case["input"],
        "category": case.get("category", "uncategorized"),
        "passed": not differences,
        "differences": differences,
        "observed": observed,
    }


def markdown_report(summary: dict[str, Any], failures: list[dict[str, Any]]) -> str:
    lines = [
        "# hgvs2vcf-cdot-lmdb evaluation",
        "",
        f"- Total: {summary['total']}",
        f"- Passed: {summary['passed']}",
        f"- Failed: {summary['failed']}",
        f"- Pass rate: {summary['pass_rate']:.2%}",
        f"- Elapsed: {summary['elapsed_seconds']:.3f} s",
        "",
        "## Results by category",
        "",
        "| Category | Passed | Failed | Pass rate |",
        "|---|---:|---:|---:|",
    ]
    for category, counts in sorted(summary["by_category"].items()):
        total = counts["passed"] + counts["failed"]
        lines.append(f"| {category} | {counts['passed']} | {counts['failed']} | {counts['passed'] / total:.2%} |")
    lines.extend(["", "## Failures", ""])
    if not failures:
        lines.append("None.")
    else:
        lines.extend(["| ID | Input | Differences |", "|---|---|---|"])
        for failure in failures:
            diff = json.dumps(failure["differences"], ensure_ascii=False, sort_keys=True).replace("|", "\\|")
            lines.append(f"| {failure['id']} | `{failure['input']}` | `{diff}` |")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--truth-set", type=Path, required=True)
    parser.add_argument("--base-url", default="http://localhost:4567")
    parser.add_argument("--json-report", type=Path, required=True)
    parser.add_argument("--markdown-report", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--check-gene", action="store_true")
    parser.add_argument("--allow-non-gold", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cases = load_jsonl(args.truth_set)
    if not args.allow_non_gold:
        non_gold = [x["id"] for x in cases if x.get("confidence") not in GOLD_CONFIDENCES]
        if non_gold:
            print(f"truth set contains {len(non_gold)} non-gold case(s); use --allow-non-gold only for fixtures", file=sys.stderr)
            return 2
    started = time.monotonic()
    results = []
    try:
        for offset in range(0, len(cases), args.batch_size):
            batch = cases[offset : offset + args.batch_size]
            responses = post_batch(args.base_url, [x["input"] for x in batch], args.timeout)
            if len(responses) != len(batch):
                raise ValueError(f"batch at offset {offset}: got {len(responses)} responses for {len(batch)} inputs")
            results.extend(compare_case(case, observed, args.check_gene) for case, observed in zip(batch, responses))
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        print(f"evaluation infrastructure error: {exc}", file=sys.stderr)
        return 2
    elapsed = time.monotonic() - started
    passed = sum(result["passed"] for result in results)
    category_counts: dict[str, Counter] = {}
    for result in results:
        counts = category_counts.setdefault(result["category"], Counter())
        counts["passed" if result["passed"] else "failed"] += 1
    summary = {
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "pass_rate": passed / len(results) if results else 0.0,
        "elapsed_seconds": elapsed,
        "by_category": {
            name: {"passed": counts["passed"], "failed": counts["failed"]} for name, counts in category_counts.items()
        },
    }
    output = {"summary": summary, "results": results}
    args.json_report.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_report.parent.mkdir(parents=True, exist_ok=True)
    args.json_report.write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    failures = [result for result in results if not result["passed"]]
    args.markdown_report.write_text(markdown_report(summary, failures), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
