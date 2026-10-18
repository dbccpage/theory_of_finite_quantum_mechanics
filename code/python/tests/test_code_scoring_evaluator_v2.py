"""Regressions for unsupported grades, malformed records and enforcement."""

from copy import deepcopy
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from operations.cicd import code_scoring_evaluator as scoring


def reviewed_record():
    return {
        "schema_version": "2.0.0",
        "artifact": {"path": "example.py", "language": "Python", "sha256": "a" * 64},
        "profile": "Exact", "level": "L2",
        "gates": {key: "A" for key in ("G1", "G2", "G3", "G4", "G5")},
        "composite_grade": "A", "score_token": "L2A", "is_complete": True,
        "grade_ceiling": "A", "evaluation_timestamp": "2026-10-18T22:00:00+00:00",
    }


class ScoringEvidenceTests(unittest.TestCase):
    def test_labels_and_unchecked_proofs_cannot_award_grades(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "example.lean"
            source.write_text("-- Level: L5; Origin: pinned; Claim: certificate; AuthorityEffect: None\n"
                              "-- Scope fence: does not claim physics; mutation: 100% killed\n"
                              "theorem uncompiled : False := by sorry\n", encoding="utf-8")
            record = scoring.score_source_file(source)
            self.assertEqual(record.level, "L1")
            self.assertFalse(record.is_complete)
            self.assertIsNone(record.score_token)
            self.assertTrue(all(value is None for value in record.to_schema_dict()["gates"].values()))

    def test_test_filename_and_assertions_are_not_execution_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "test_failed.py"
            source.write_text("assert False\n", encoding="utf-8")
            record = scoring.score_source_file(source)
            self.assertIsNone(record.tests.grade)
            self.assertIsNone(record.failure_safety.grade)

    def test_digest_binds_raw_crlf_bytes(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "example.rs"
            data = b"// certificate BigRational Verification\r\npub fn f() {}\r\n"
            source.write_bytes(data)
            self.assertEqual(scoring.score_source_file(source).sha256, hashlib.sha256(data).hexdigest())

    def test_missing_metric_tool_does_not_award_structure_A(self):
        with patch.object(scoring, "_HAS_LIZARD", False):
            self.assertIsNone(scoring.evaluate_gate5_structure_and_complexity(Path("x.rs"), "fn x() {}", "Rust").grade)

    def test_enforcement_refuses_incomplete_missing_and_empty_targets(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "source.py"
            source.write_text("x = 1\n", encoding="utf-8")
            for paths in ([source], [root / "missing.py"], []):
                with self.subTest(paths=paths):
                    self.assertEqual(scoring.evaluate_scoring_rubric(paths, enforced=True).status, "FAIL")

    def test_complete_reviewed_record_is_accepted(self):
        self.assertEqual(scoring.validate_record_against_schema(reviewed_record()), [])

    def test_missing_validator_does_not_report_schema_success(self):
        with patch.object(scoring, "_HAS_JSONSCHEMA", False):
            self.assertTrue(scoring.validate_record_against_schema(reviewed_record()))

    def test_malformed_record_shapes_return_errors(self):
        for record in ([], None, {"artifact": [], "gates": []}):
            with self.subTest(record=record):
                self.assertTrue(scoring.validate_record_against_schema(record))
        for replacement in ({"G1": []}, {"G1": {}}, {"G1": "Z"}):
            record = reviewed_record()
            record["gates"].update(replacement)
            self.assertTrue(scoring.validate_record_against_schema(record))

    def test_schema_and_grade_consistency_are_checked(self):
        for field, value in (("schema_version", "1.0.0"), ("is_complete", False),
                             ("score_token", "L5A"), ("grade_ceiling", "E"),
                             ("evaluation_timestamp", "not-a-date")):
            record = reviewed_record()
            record[field] = value
            with self.subTest(field=field):
                self.assertTrue(scoring.validate_record_against_schema(record))

    def test_unassessed_requires_json_null_and_consistent_minimum(self):
        record = reviewed_record()
        record["gates"]["G4"] = None
        record.update(composite_grade=None, score_token=None, is_complete=False)
        self.assertEqual(scoring.validate_record_against_schema(record), [])
        record["score_token"] = "null"
        self.assertTrue(scoring.validate_record_against_schema(record))
        record = reviewed_record()
        record["gates"]["G2"] = "C"
        self.assertTrue(scoring.validate_record_against_schema(record))

    def test_mutation_denominator_includes_inconclusive_and_unrun(self):
        record = reviewed_record()
        record["mutation_accounting"] = {
            "generated": 6, "killed": 2, "survived": 0, "demonstrably_equivalent": 1,
            "invalid": 1, "inconclusive": 1, "unrun": 1, "conservative_ratio": 0.5,
        }
        self.assertEqual(scoring.validate_record_against_schema(record), [])
        for key, value in (("generated", 5), ("conservative_ratio", 1.0), ("killed", True), ("unrun", -1)):
            broken = deepcopy(record)
            broken["mutation_accounting"][key] = value
            with self.subTest(key=key):
                self.assertTrue(scoring.validate_record_against_schema(broken))


if __name__ == "__main__":
    unittest.main()
