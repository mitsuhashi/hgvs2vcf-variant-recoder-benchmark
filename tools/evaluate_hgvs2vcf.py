#!/usr/bin/env python3
"""Evaluate HGVS-to-VCF HTTP responses against a JSONL truth set."""

from __future__ import annotations

import argparse
import html
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
}
USER_AGENT = "hgvs2vcf-variant-recoder-benchmark/1.0"


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


def response_vcf(result: dict[str, Any]) -> list[dict[str, Any]]:
    """Convert hgvs2vcf-marshal output to the evaluator's VCF row format."""
    if "error" in result:
        return []
    candidates = result.get("candidates")
    results = candidates if isinstance(candidates, list) else [result]
    rows = []
    for item in results:
        vcf = item.get("vcf")
        if not isinstance(vcf, dict):
            raise ValueError("conversion result does not contain a VCF object")
        rows.append(
            {
                # The truth set uses RefSeq genomic accessions, not chromosome labels.
                "chrom": item.get("genomic_accession", vcf.get("chromosome")),
                "pos": vcf["position"],
                "ref": vcf["reference"],
                "alt": vcf["alternate"],
            }
        )
    return rows


def normalize_response(result: dict[str, Any]) -> dict[str, Any]:
    if "error" in result:
        return {"error": result["error"]}
    return {"vcf": response_vcf(result)}


def post_cdot_batch(base_url: str, inputs: list[str], timeout: float) -> list[dict[str, Any]]:
    request = urllib.request.Request(
        base_url.rstrip("/") + "/decode",
        data=json.dumps({"hgvs": inputs}, ensure_ascii=False).encode(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.load(response)
    if not isinstance(payload, list):
        raise ValueError("POST /decode did not return a JSON array")
    return payload


def post_marshal_batch(
    base_url: str,
    inputs: list[str],
    timeout: float,
    assembly: str = "GRCh38",
) -> list[dict[str, Any]]:
    request = urllib.request.Request(
        base_url.rstrip("/") + "/v1/convert-batch",
        data=json.dumps({"assembly": assembly, "hgvs": inputs}, ensure_ascii=False).encode(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.load(response)
    if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
        raise ValueError("POST /v1/convert-batch did not return a JSON results array")
    return [normalize_response(result) for result in payload["results"]]


def post_batch(
    api_type: str,
    base_url: str,
    inputs: list[str],
    timeout: float,
    assembly: str = "GRCh38",
) -> list[dict[str, Any]]:
    if api_type == "cdot":
        return post_cdot_batch(base_url, inputs, timeout)
    if api_type == "marshal":
        return post_marshal_batch(base_url, inputs, timeout, assembly)
    raise ValueError(f"unsupported API type: {api_type}")


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


def compare_case(case: dict[str, Any], observed: dict[str, Any]) -> dict[str, Any]:
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
    return {
        "id": case["id"],
        "input": case["input"],
        "category": case.get("category", "uncategorized"),
        "passed": not differences,
        "differences": differences,
        "observed": observed,
    }


def summarize_results(results: list[dict[str, Any]], elapsed_seconds: float) -> dict[str, Any]:
    passed = sum(result["passed"] for result in results)
    category_counts: dict[str, Counter] = {}
    for result in results:
        counts = category_counts.setdefault(result["category"], Counter())
        counts["passed" if result["passed"] else "failed"] += 1
    return {
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "pass_rate": passed / len(results) if results else 0.0,
        "elapsed_seconds": elapsed_seconds,
        "by_category": {
            name: {"passed": counts["passed"], "failed": counts["failed"]}
            for name, counts in category_counts.items()
        },
    }


def html_breakable(value: Any, chunk_size: int = 24) -> str:
    text = str(value)
    return "<wbr>".join(
        html.escape(text[offset : offset + chunk_size])
        for offset in range(0, len(text), chunk_size)
    )


def html_code(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, (dict, list, tuple)):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return f"<code>{html_breakable(value)}</code>"


def markdown_vcf(rows: Iterable[dict[str, Any]]) -> str:
    values = []
    for row in rows:
        locus = html.escape(f"{row['chrom']}:{row['pos']}")
        ref = html_breakable(row["ref"])
        alt = html_breakable(row["alt"])
        values.append(f"<code>{locus}<br>REF: {ref}<br>ALT: {alt}</code>")
    if not values:
        return "—"
    return "<br><br>".join(values)


def markdown_vcf_results(expected: dict[str, Any], observed: dict[str, Any]) -> tuple[str, str]:
    expected_vcf = markdown_vcf(expected.get("vcf", []))
    if "error" in observed:
        observed_vcf = f"Error:<br>{html_code(observed['error'])}"
    else:
        observed_vcf = markdown_vcf(observed.get("vcf", []))
    return expected_vcf, observed_vcf


def markdown_differences(differences: dict[str, Any]) -> str:
    values = []
    for name, difference in sorted(differences.items()):
        if name == "error":
            values.append("API error")
        elif name == "vcf":
            values.append("VCF mismatch")
        else:
            values.append(
                f"<strong>{html.escape(name)}</strong><br>"
                f"expected: {html_code(difference.get('expected'))}<br>"
                f"observed: {html_code(difference.get('observed'))}"
            )
    return "<br><br>".join(values) or "—"


def markdown_report(
    summary: dict[str, Any],
    cases: list[dict[str, Any]],
    results: list[dict[str, Any]],
) -> str:
    lines = [
        "# HGVS to VCF evaluation",
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
    case_results = list(zip(cases, results))

    lines.extend(
        [
            "",
            "## Successful results",
            "",
        ]
    )
    successful = [(case, result) for case, result in case_results if result["passed"]]
    if not successful:
        lines.append("- None.")
    successful_categories = sorted({result["category"] for _, result in successful})
    for category_index, category in enumerate(successful_categories):
        if category_index:
            lines.append("")
        lines.extend([f"### {html.escape(category)}", ""])
        category_results = [item for item in successful if item[1]["category"] == category]
        for result_index, (case, result) in enumerate(category_results):
            if result_index:
                lines.append("")
            expected_vcf, observed_vcf = markdown_vcf_results(case["expected"], result["observed"])
            lines.extend(
                [
                    f"- **HGVS:** {html_code(case['input'])}",
                    f"  - **Variant Recoder:**<br>{expected_vcf}",
                    f"  - **hgvs2vcf:**<br>{observed_vcf}",
                ]
            )

    lines.extend(
        [
            "",
            "## Failed results",
            "",
        ]
    )
    failed = [(case, result) for case, result in case_results if not result["passed"]]
    if not failed:
        lines.append("- None.")
    failed_categories = sorted({result["category"] for _, result in failed})
    for category_index, category in enumerate(failed_categories):
        if category_index:
            lines.append("")
        lines.extend([f"### {html.escape(category)}", ""])
        category_results = [item for item in failed if item[1]["category"] == category]
        for result_index, (case, result) in enumerate(category_results):
            if result_index:
                lines.append("")
            expected_vcf, observed_vcf = markdown_vcf_results(case["expected"], result["observed"])
            differences = markdown_differences(result["differences"])
            lines.extend(
                [
                    f"- **HGVS:** {html_code(case['input'])}",
                    f"  - **Variant Recoder:**<br>{expected_vcf}",
                    f"  - **hgvs2vcf:**<br>{observed_vcf}",
                    f"  - **Difference:** {differences}",
                ]
            )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--truth-set", type=Path, required=True)
    parser.add_argument("--api-type", choices=("cdot", "marshal"), default="marshal")
    parser.add_argument("--base-url")
    parser.add_argument("--json-report", type=Path, required=True)
    parser.add_argument("--markdown-report", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--allow-non-gold", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_url = args.base_url or "https://hgvs2vcf.togovar.org"
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
            responses = post_batch(
                args.api_type,
                base_url,
                [x["input"] for x in batch],
                args.timeout,
                batch[0].get("assembly", "GRCh38"),
            )
            if len(responses) != len(batch):
                raise ValueError(f"batch at offset {offset}: got {len(responses)} responses for {len(batch)} inputs")
            results.extend(compare_case(case, observed) for case, observed in zip(batch, responses))
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        print(f"evaluation infrastructure error: {exc}", file=sys.stderr)
        return 2
    elapsed = time.monotonic() - started
    summary = summarize_results(results, elapsed)
    summary["api_type"] = args.api_type
    summary["base_url"] = base_url
    output = {"summary": summary, "results": results}
    args.json_report.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_report.parent.mkdir(parents=True, exist_ok=True)
    args.json_report.write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    failures = [result for result in results if not result["passed"]]
    args.markdown_report.write_text(markdown_report(summary, cases, results), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
