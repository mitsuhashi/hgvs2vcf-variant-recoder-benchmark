#!/usr/bin/env python3

import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


builder = load("truth_builder", "tools/build_truth_set.py")
evaluator = load("truth_evaluator", "tools/evaluate_hgvs2vcf.py")


class BuildTruthSetTests(unittest.TestCase):
    def load_fixture_candidates(self):
        return builder.load_candidates(
            ROOT / "tests/fixtures/variant_summary.txt",
            ROOT / "tests/fixtures/hgvs4variation.txt",
            ROOT / "tests/fixtures/mane_summary.txt",
        )

    def test_fixture_join_and_filter(self):
        candidates, stats = self.load_fixture_candidates()
        self.assertEqual(
            {
                "NOS3:p.Asp298Glu": "gene_hgvsp",
                "NOS3:c.894T>G": "gene_hgvsc",
                "NM_000603:c.894T>G": "refseq_hgvsc",
            },
            {case["input"]: case["input_kind"] for case in candidates},
        )
        for case in candidates:
            self.assertEqual("NC_000007.14", case["contig"])
            self.assertEqual({"NC_000007.14:g.150999023T>G"}, case["genomic_hgvs"])
        self.assertEqual("protein_substitution", next(
            case["category"] for case in candidates if case["input_kind"] == "gene_hgvsp"
        ))
        self.assertEqual(3, stats["candidates"])
        self.assertEqual(3, stats["hgvs_rows"])
        self.assertEqual(1, stats["candidates_gene_hgvsp"])
        self.assertEqual(1, stats["candidates_gene_hgvsc"])
        self.assertEqual(1, stats["candidates_refseq_hgvsc"])

    def test_inputs_use_mane_and_old_build_is_excluded(self):
        candidates, _ = self.load_fixture_candidates()
        self.assertTrue(all(not case["input"].startswith(("NP_", "NM_000603.4")) for case in candidates))
        self.assertTrue(all(
            case["mane_select"]["refseq_nuc"] == "NM_000603.4"
            for case in candidates if case["input_kind"].startswith("gene_")
        ))
        self.assertTrue(all(case["contig"] != "NC_000007.13" for case in candidates))

    def test_candidate_retention_is_bounded_per_group(self):
        variant_header = (ROOT / "tests/fixtures/variant_summary.txt").read_text(
            encoding="utf-8"
        ).splitlines()[0]
        hgvs_header = (ROOT / "tests/fixtures/hgvs4variation.txt").read_text(
            encoding="utf-8"
        ).splitlines()[4]
        with tempfile.TemporaryDirectory() as temporary_dir:
            temporary = Path(temporary_dir)
            variant_summary = temporary / "variant_summary.txt"
            hgvs = temporary / "hgvs4variation.txt"
            variant_summary.write_text(
                variant_header + "\n" +
                "12345\tsingle nucleotide variant\tone\t4846\tNOS3\tGRCh38\t"
                "NC_000007.14\t207776\n" +
                "12346\tsingle nucleotide variant\ttwo\t4846\tNOS3\tGRCh38\t"
                "NC_000007.14\t207778\n",
                encoding="utf-8",
            )
            hgvs.write_text(
                hgvs_header + "\n" +
                "NOS3\t4846\t207776\t12345\tcoding\tna\t"
                "NM_000603.4:c.894T>G\tc.894T>G\tNP_000594.2:p.Asp298Glu\t"
                "p.Asp298Glu\tYes\tNo\tNo\n" +
                "NOS3\t4846\t207776\t12345\tgenomic\tGRCh38\t"
                "NC_000007.14:g.150999023T>G\tg.150999023T>G\t-\t-\tNo\tNo\tNo\n" +
                "NOS3\t4846\t207778\t12346\tcoding\tna\t"
                "NM_000603.4:c.895A>C\tc.895A>C\tNP_000594.2:p.Asp299Ala\t"
                "p.Asp299Ala\tYes\tNo\tNo\n" +
                "NOS3\t4846\t207778\t12346\tgenomic\tGRCh38\t"
                "NC_000007.14:g.150999024A>C\tg.150999024A>C\t-\t-\tNo\tNo\tNo\n",
                encoding="utf-8",
            )
            candidates, stats = builder.load_candidates(
                variant_summary,
                hgvs,
                ROOT / "tests/fixtures/mane_summary.txt",
                limit_per_group=1,
                seed=7,
            )
        self.assertEqual(6, stats["candidates"])
        self.assertEqual(3, stats["retained_candidates"])
        self.assertEqual(3, len(candidates))
        self.assertEqual(set(builder.INPUT_KINDS), {case["input_kind"] for case in candidates})

    def test_candidate_cache_round_trip_preserves_sets_and_stats(self):
        candidate = {
            "input": "NM_000603:c.894T>G",
            "genomic_hgvs": {"NC_000007.14:g.150999023T>G"},
        }
        signature = {"version": 1, "seed": 7}
        with tempfile.TemporaryDirectory() as temporary_dir:
            path = Path(temporary_dir) / "candidates.json"
            builder.write_candidate_cache(
                path,
                signature,
                [candidate],
                builder.Counter({"candidates": 3}),
            )
            loaded = builder.load_candidate_cache(path, signature)
        self.assertIsNotNone(loaded)
        attempted, stats = loaded
        self.assertEqual(candidate, attempted[0])
        self.assertEqual(3, stats["candidates"])

    def test_parse_variant_recoder_vcf_formats(self):
        self.assertEqual(
            ("NC_000007.14", 150999023, "T", "G"),
            builder.vcf_key(builder.parse_vcf_string("7-150999023-T-G")),
        )
        self.assertEqual(
            ("NC_000023.11", 100, "A", "AT"),
            builder.vcf_key(builder.parse_vcf_string("X 100 . A AT . . .")),
        )
        self.assertIsNone(builder.parse_vcf_string("GL000220.1-10-A-G"))

    def test_extracts_all_primary_assembly_alleles(self):
        response = [
            {
                "warnings": ["example"],
                "G": {
                    "input": "NM_000603.4:c.894T>G",
                    "vcf_string": ["7-150999023-T-G", "LRG_1-1-A-G"],
                },
                "C": {
                    "input": "NM_000603.4:c.894T>G",
                    "vcf_string": "7-150999023-T-C",
                },
            }
        ]
        values, invalid = builder.extract_recoder_vcf(response)
        self.assertEqual(
            [
                ("NC_000007.14", 150999023, "T", "C"),
                ("NC_000007.14", 150999023, "T", "G"),
            ],
            [builder.vcf_key(value) for value in values],
        )
        self.assertEqual(["LRG_1-1-A-G"], invalid)

    def test_balanced_order_round_robins_categories(self):
        candidates = [
            {"input_kind": "one", "category": "a", "variation_id": str(index), "input": f"a{index}"}
            for index in range(4)
        ] + [
            {"input_kind": "two", "category": "b", "variation_id": str(index + 10), "input": f"b{index}"}
            for index in range(4)
        ]
        ordered = builder.balanced_order(candidates, seed=1)
        self.assertEqual(["one", "two", "one", "two"], [value["input_kind"] for value in ordered[:4]])

    def test_gene_record_uses_only_mane_vcf(self):
        candidates, _ = self.load_fixture_candidates()
        candidate = next(case for case in candidates if case["input_kind"] == "gene_hgvsc")
        input_response = [{
            "G": {
                "input": candidate["input"],
                "vcf_string": ["7-150999023-T-G", "7-150999024-A-C"],
            }
        }]
        mane_response = [{
            "G": {
                "input": candidate["oracle_hgvs"],
                "vcf_string": ["7-150999023-T-G"],
                "hgvsc": ["NM_000603.4:c.894T>G"],
            }
        }]
        record = builder.make_record(candidate, input_response, mane_response, {"oracle": "test"})
        self.assertEqual("NM_000603.4", record["expected"]["transcript"])
        self.assertEqual("NOS3", record["expected"]["gene"])
        self.assertEqual(
            [("NC_000007.14", 150999023, "T", "G")],
            [builder.vcf_key(value) for value in record["expected"]["vcf"]],
        )
        self.assertFalse(record["expected"]["ambiguous"])
        self.assertEqual("ensembl_variant_recoder", record["confidence"])

    def test_gene_record_rejects_mane_vcf_missing_from_gene_response(self):
        candidates, _ = self.load_fixture_candidates()
        candidate = next(case for case in candidates if case["input_kind"] == "gene_hgvsc")
        input_response = [{
            "G": {"input": candidate["input"], "vcf_string": ["7-150999024-A-C"]}
        }]
        mane_response = [{
            "G": {
                "input": candidate["oracle_hgvs"],
                "vcf_string": ["7-150999023-T-G"],
                "hgvsc": ["NM_000603.4:c.894T>G"],
            }
        }]
        record = builder.make_record(candidate, input_response, mane_response, {"oracle": "test"})
        self.assertEqual("quarantined", record["confidence"])
        self.assertEqual("mane_vcf_not_returned_for_gene_input", record["provenance"]["error"])

    def test_unversioned_refseq_resolves_version_from_recoder(self):
        candidates, _ = self.load_fixture_candidates()
        candidate = next(case for case in candidates if case["input_kind"] == "refseq_hgvsc")
        response = [{
            "G": {
                "input": candidate["input"],
                "vcf_string": ["7-150999023-T-G"],
                "hgvsc": ["NM_000603.4:c.895T>G"],
            }
        }]
        record = builder.make_record(candidate, response, response, {"oracle": "test"})
        self.assertEqual("NM_000603.4", record["expected"]["transcript"])
        self.assertEqual("ensembl_variant_recoder", record["confidence"])

    def test_fetch_recoder_uses_post_and_associates_echoed_input(self):
        class FakeResponse(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                self.close()

        def fake_urlopen(request, timeout):
            self.assertEqual("POST", request.method)
            self.assertIn("vcf_string=1", request.full_url)
            self.assertIn("fields=spdi", request.full_url)
            payload = json.loads(request.data)
            # Deliberately reverse the response to verify echoed-input matching.
            body = json.dumps(
                [{"G": {"input": value, "vcf_string": "7-1-A-G"}} for value in reversed(payload["ids"])]
            ).encode()
            return FakeResponse(body)

        with mock.patch.object(builder.urllib.request, "urlopen", side_effect=fake_urlopen):
            result = builder.fetch_recoder(
                ["one", "two"], "https://example.test", "homo_sapiens", 100, 2,
                builder.ResponseCache(None), "live",
            )
        self.assertEqual("one", builder.response_input(result["one"]))
        self.assertEqual("two", builder.response_input(result["two"]))

    def test_fetch_recoder_requests_hgvsc_for_unversioned_refseq(self):
        seen_urls = []

        def fake_api_post(url, ids, _timeout):
            seen_urls.append(url)
            return [{"G": {"input": value, "vcf_string": "7-1-A-G"}} for value in ids]

        with mock.patch.object(builder, "api_post", side_effect=fake_api_post):
            builder.fetch_recoder(
                ["NM_000603:c.894T>G", "NM_000603.4:c.894T>G"],
                "https://example.test", "homo_sapiens", 100, 2,
                builder.ResponseCache(None), "live",
            )
        self.assertEqual(2, len(seen_urls))
        self.assertTrue(any("fields=hgvsc" in url for url in seen_urls))
        self.assertTrue(any("fields=spdi" in url for url in seen_urls))

    def test_fetch_recoder_bisects_all_invalid_batch(self):
        class FakeResponse(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                self.close()

        calls = []

        def fake_urlopen(request, timeout):
            ids = json.loads(request.data)["ids"]
            calls.append(ids)
            payload = {"error": f"unable to parse {ids[0]}"}
            return FakeResponse(json.dumps(payload).encode())

        with mock.patch.object(builder.urllib.request, "urlopen", side_effect=fake_urlopen):
            result = builder.fetch_recoder(
                ["bad-one", "bad-two"], "https://example.test", "homo_sapiens",
                100, 2, builder.ResponseCache(None), "live",
            )
        self.assertEqual("unable to parse bad-one", result["bad-one"]["error"])
        self.assertEqual("unable to parse bad-two", result["bad-two"]["error"])
        self.assertEqual(3, len(calls))

    def test_fetch_recoder_bisects_timed_out_batch(self):
        calls = []

        def fake_api_post(_url, ids, _timeout):
            calls.append(ids)
            if len(ids) > 1:
                raise builder.ApiPostError("read timed out", timed_out=True)
            return [{"G": {"input": ids[0], "vcf_string": "7-1-A-G"}}]

        with mock.patch.object(builder, "api_post", side_effect=fake_api_post):
            result = builder.fetch_recoder(
                ["one", "two"], "https://example.test", "homo_sapiens",
                100, 2, builder.ResponseCache(None), "live",
            )
        self.assertEqual("one", builder.response_input(result["one"]))
        self.assertEqual("two", builder.response_input(result["two"]))
        self.assertEqual([["one", "two"], ["one"], ["two"]], calls)

    def test_fetch_recoder_bisects_http_400_and_quarantines_singleton(self):
        calls = []

        def fake_api_post(_url, ids, _timeout):
            calls.append(ids)
            if "bad" in ids:
                raise builder.ApiPostError("HTTP Error 400", bad_request=True)
            return [{"G": {"input": ids[0], "vcf_string": "7-1-A-G"}}]

        with mock.patch.object(builder, "api_post", side_effect=fake_api_post):
            result = builder.fetch_recoder(
                ["good", "bad"], "https://example.test", "homo_sapiens",
                100, 2, builder.ResponseCache(None), "live",
            )
        self.assertEqual("good", builder.response_input(result["good"]))
        self.assertIn("HTTP Error 400", result["bad"]["error"])
        self.assertEqual([["good", "bad"], ["good"], ["bad"]], calls)

    def test_fetch_recoder_quarantines_timed_out_singleton(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            cache_path = Path(temporary_dir) / "responses.jsonl"
            with mock.patch.object(
                builder,
                "api_post",
                side_effect=builder.ApiPostError("read timed out", timed_out=True),
            ):
                result = builder.fetch_recoder(
                    ["slow"], "https://example.test", "homo_sapiens",
                    100, 2, builder.ResponseCache(cache_path), "live",
                )
            self.assertFalse(cache_path.exists())
        self.assertEqual("slow", result["slow"]["input"])
        self.assertIn("read timed out", result["slow"]["error"])
        self.assertTrue(result["slow"]["transient_error"])


class EvaluateTests(unittest.TestCase):
    def setUp(self):
        self.case = {
            "id": "one",
            "input": "NM_000603.4:c.894T>G",
            "category": "coding_substitution",
            "expected": {
                "transcript": "NM_000603.4",
                "gene": "NOS3",
                "vcf": [{"chrom": "NC_000007.14", "pos": 150999023, "ref": "T", "alt": "G"}],
                "ambiguous": False,
            },
        }

    def test_equal_vcf_ignores_candidate_order(self):
        observed = {
            "transcript": "NM_000603.4",
            "gene": "NOS3",
            "vcf": [{"alt": "G", "ref": "T", "pos": 150999023, "chrom": "NC_000007.14"}],
            "ambiguous": False,
        }
        self.assertTrue(evaluator.compare_case(self.case, observed)["passed"])

    def test_transcript_difference_does_not_fail_when_vcf_matches(self):
        observed = {
            "transcript": "ENST00000296387.6",
            "gene": "CLDN19",
            "vcf": [{"chrom": "NC_000007.14", "pos": 150999023, "ref": "T", "alt": "G"}],
            "ambiguous": True,
        }
        self.assertTrue(evaluator.compare_case(self.case, observed)["passed"])

    def test_coordinate_difference_is_reported(self):
        observed = {
            "transcript": "NM_000603.4",
            "vcf": [{"chrom": "NC_000007.14", "pos": 150999024, "ref": "T", "alt": "G"}],
            "ambiguous": False,
        }
        result = evaluator.compare_case(self.case, observed)
        self.assertFalse(result["passed"])
        self.assertIn("vcf", result["differences"])

    def test_markdown_report_lists_passed_and_failed_vcfs(self):
        passed_observed = {
            "transcript": "NM_000603.4",
            "vcf": [{"chrom": "NC_000007.14", "pos": 150999023, "ref": "T", "alt": "G"}],
            "ambiguous": False,
        }
        failed_observed = {
            **passed_observed,
            "vcf": [{"chrom": "NC_000007.14", "pos": 150999024, "ref": "T", "alt": "G"}],
        }
        results = [
            evaluator.compare_case(self.case, passed_observed),
            evaluator.compare_case(self.case, failed_observed),
        ]
        summary = {
            "total": 2,
            "passed": 1,
            "failed": 1,
            "pass_rate": 0.5,
            "elapsed_seconds": 0.1,
            "by_category": {"coding_substitution": {"passed": 1, "failed": 1}},
        }
        report = evaluator.markdown_report(summary, [self.case, self.case], results)
        self.assertIn("## Successful results", report)
        self.assertIn("## Failed results", report)
        self.assertNotIn("| Category | HGVS | VCF comparison |", report)
        self.assertNotIn("| Category | HGVS | VCF comparison | Difference |", report)
        self.assertEqual(2, report.count("### coding_substitution"))
        self.assertIn("- **HGVS:** <code>NM_000603.4:c.894T&gt;G</code>", report)
        self.assertNotIn("  - **Category:**", report)
        self.assertIn("  - **Variant Recoder:**", report)
        self.assertIn("  - **hgvs2vcf:**", report)
        self.assertIn("<code>NC_000007.14:150999023<br>REF: T<br>ALT: G</code>", report)
        self.assertIn("<code>NC_000007.14:150999024<br>REF: T<br>ALT: G</code>", report)
        self.assertIn("  - **Difference:** VCF mismatch", report)

    def test_post_batch_contract(self):
        class FakeResponse(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                self.close()

        def fake_urlopen(request, timeout):
            self.assertEqual("POST", request.method)
            self.assertEqual(2, timeout)
            self.assertEqual(evaluator.USER_AGENT, request.get_header("User-agent"))
            payload = json.loads(request.data)
            body = json.dumps(
                [
                    {
                        "input": value,
                        "transcript": "NM_000603.4",
                        "vcf": [{"chrom": "NC_000007.14", "pos": 150999023, "ref": "T", "alt": "G"}],
                        "ambiguous": False,
                        "warnings": [],
                    }
                    for value in payload["hgvs"]
                ]
            ).encode()
            return FakeResponse(body)

        with mock.patch.object(evaluator.urllib.request, "urlopen", side_effect=fake_urlopen):
            response = evaluator.post_batch(
                "http://localhost:4567",
                ["NM_000603.4:c.894T>G"],
                2,
            )
            self.assertEqual(1, len(response))
            self.assertEqual("NM_000603.4:c.894T>G", response[0]["input"])

    def test_evaluate_script_passes_configuration_and_extra_arguments(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            temporary = Path(temporary_dir)
            truth_set = temporary / "gold.jsonl"
            truth_set.write_text("{}\n", encoding="utf-8")
            arguments_file = temporary / "arguments.txt"
            fake_python = temporary / "python"
            fake_python.write_text(
                "#!/usr/bin/env bash\n"
                "printf '%s\\n' \"$@\" > \"${ARGUMENTS_FILE:?}\"\n",
                encoding="utf-8",
            )
            fake_python.chmod(0o755)
            json_report = temporary / "result.json"
            markdown_report = temporary / "result.md"
            environment = {
                **os.environ,
                "PYTHON_BIN": str(fake_python),
                "ARGUMENTS_FILE": str(arguments_file),
                "TRUTH_SET": str(truth_set),
                "BASE_URL": "https://example.test/hgvs2vcf",
                "JSON_REPORT": str(json_report),
                "MARKDOWN_REPORT": str(markdown_report),
                "EVALUATION_BATCH_SIZE": "17",
                "EVALUATION_TIMEOUT": "2.5",
            }
            completed = subprocess.run(
                [ROOT / "scripts/evaluate.sh", "--allow-non-gold"],
                cwd=temporary,
                env=environment,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertEqual(
                [
                    str(ROOT / "tools/evaluate_hgvs2vcf.py"),
                    "--truth-set",
                    str(truth_set),
                    "--base-url",
                    "https://example.test/hgvs2vcf",
                    "--json-report",
                    str(json_report),
                    "--markdown-report",
                    str(markdown_report),
                    "--batch-size",
                    "17",
                    "--timeout",
                    "2.5",
                    "--allow-non-gold",
                ],
                arguments_file.read_text(encoding="utf-8").splitlines(),
            )

if __name__ == "__main__":
    unittest.main()
