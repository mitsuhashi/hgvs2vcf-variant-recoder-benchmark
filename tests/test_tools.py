#!/usr/bin/env python3

import importlib.util
import io
import json
import sys
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
    def test_fixture_join_and_filter(self):
        candidates, stats = builder.load_candidates(
            ROOT / "tests/fixtures/variant_summary.txt",
            ROOT / "tests/fixtures/hgvs4variation.txt",
        )
        self.assertEqual(1, len(candidates))
        case = candidates[0]
        self.assertEqual("NM_000603.4:c.894T>G", case["input"])
        self.assertEqual(
            ("NC_000007.14", 150999023, "T", "G"),
            builder.vcf_key(case["vcf"]),
        )
        self.assertEqual({"NC_000007.14:g.150999023T>G"}, case["genomic_hgvs"])
        self.assertEqual("coding_substitution", case["category"])
        self.assertEqual(1, stats["candidates"])

    def test_protein_and_old_build_are_not_candidates(self):
        candidates, _ = builder.load_candidates(
            ROOT / "tests/fixtures/variant_summary.txt",
            ROOT / "tests/fixtures/hgvs4variation.txt",
        )
        self.assertTrue(all(":p." not in case["input"] for case in candidates))
        self.assertTrue(all(case["vcf"]["chrom"] != "NC_000007.13" for case in candidates))

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
            {"category": "a", "variation_id": str(index), "input": f"a{index}"}
            for index in range(4)
        ] + [
            {"category": "b", "variation_id": str(index + 10), "input": f"b{index}"}
            for index in range(4)
        ]
        ordered = builder.balanced_order(candidates, seed=1)
        self.assertEqual(["a", "b", "a", "b"], [value["category"] for value in ordered[:4]])

    def test_fetch_recoder_uses_post_and_associates_echoed_input(self):
        class FakeResponse(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                self.close()

        def fake_urlopen(request, timeout):
            self.assertEqual("POST", request.method)
            self.assertIn("vcf_string=1", request.full_url)
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
        self.assertTrue(evaluator.compare_case(self.case, observed, True)["passed"])

    def test_coordinate_difference_is_reported(self):
        observed = {
            "transcript": "NM_000603.4",
            "vcf": [{"chrom": "NC_000007.14", "pos": 150999024, "ref": "T", "alt": "G"}],
            "ambiguous": False,
        }
        result = evaluator.compare_case(self.case, observed, False)
        self.assertFalse(result["passed"])
        self.assertIn("vcf", result["differences"])

    def test_post_batch_contract(self):
        class FakeResponse(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                self.close()

        def fake_urlopen(request, timeout):
            self.assertEqual("POST", request.method)
            self.assertEqual(2, timeout)
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


if __name__ == "__main__":
    unittest.main()
