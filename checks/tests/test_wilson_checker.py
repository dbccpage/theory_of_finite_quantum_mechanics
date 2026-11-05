"""Wilson checker receipt, exact-fixture and failure-protocol regression tests.

AuthorityEffect: None. Independent matrix oracles reside in the shared support
and first-25 regression suites; this suite verifies their checker integration.
"""
from __future__ import annotations

from collections.abc import Callable
import contextlib
from fractions import Fraction
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

from hypothesis import given, settings, strategies as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_review_repairs import load
from checker_support.boundary import cli, evaluate

STEM = "check_tfq_1050_fqcd_wilson_dirac_gamma5_hermiticity"


class WilsonCheckerTests(unittest.TestCase):
    def test_complete_receipt_and_repeatability(self) -> None:
        module = load(STEM)
        first, second = module.check(), module.check()
        self.assertEqual(first, second)
        self.assertEqual(first, {"record_id": "TFQ-1050", "dag_node": "FQCD-WILSON-DIRAC-GAMMA5-HERMITICITY",
                                "authority_effect": "None", "total_checks": 110, "failed_checks": 0,
                                "failures": [], "all_passed": True})
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(cli(module.main), 0)
        self.assertEqual(json.loads(output.getvalue()), first)

    @settings(max_examples=80, derandomize=True, deadline=None, database=None)
    @given(statuses=st.lists(st.booleans(), max_size=30))
    def test_generated_named_cases_are_counted_without_loss(self, statuses: list[bool]) -> None:
        module = load(STEM)
        def supplied_cases(record: Callable[[str, bool], None]) -> None:
            for index, status in enumerate(statuses):
                record(f"generated-{index}", status)
        # Full matrix assembly is exercised separately; this property isolates accounting.
        with patch.object(module, "check_chiral_links", supplied_cases), patch.object(module, "assembled_operator_checks", return_value=True):
            receipt = module.check()
        failures = [f"generated-{index}" for index, status in enumerate(statuses) if not status]
        self.assertEqual(receipt["total_checks"], 18+len(statuses))
        self.assertEqual(receipt["failed_checks"], len(failures))
        self.assertEqual(receipt["failures"], failures)
        self.assertIs(receipt["all_passed"], not failures)

    def test_malformed_statuses_and_duplicate_ids_are_refused(self) -> None:
        module = load(STEM)
        for invalid in (1, 0, None, "passed", [], Fraction(1), object()):
            def malformed(record: Callable[..., None]) -> None:
                record("malformed", invalid)
            with patch.object(module, "check_chiral_links", malformed):
                result = evaluate(module.check)
                self.assertFalse(result.ok)
                if result.error is None:
                    self.fail("invalid status lost its failure")
                self.assertEqual(result.error.kind, "input")
        def duplicates(record: Callable[[str, bool], None]) -> None:
            record("same", True)
            record("same", False)
        with patch.object(module, "check_chiral_links", duplicates):
            result = evaluate(module.check)
            self.assertFalse(result.ok)
            if result.error is None:
                self.fail("duplicate id lost its failure")
            self.assertEqual(result.error.kind, "duplicate")

    def test_assembled_matrix_fault_is_a_failed_case_and_nonzero_cli(self) -> None:
        module = load(STEM)
        with patch.object(module, "assembled_operator_checks", return_value=False):
            receipt = module.check()
            self.assertEqual(receipt["total_checks"], 110)
            self.assertEqual(receipt["failed_checks"], 1)
            self.assertEqual(receipt["failures"], ["assembled_four_spin_colored_operator"])
            self.assertIs(receipt["all_passed"], False)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(cli(module.main), 1)
            self.assertEqual(json.loads(output.getvalue()), receipt)

    def test_direct_determinant_fault_cannot_hide_behind_polynomial(self) -> None:
        module = load(STEM)
        with patch.object(module, "direct_wilson_determinant", return_value=Fraction(123456)):
            receipt = module.check()
        self.assertEqual(receipt["failed_checks"], 13)
        self.assertIn("nonunit_determinant_counterexample", receipt["failures"])
        self.assertFalse(receipt["all_passed"])

    def test_section_obligations_are_exact_booleans_and_named(self) -> None:
        module = load(STEM)
        for operation, expected in ((module.check_chiral_links, 92), (module.check_determinant_examples, 18)):
            rows: list[tuple[str, bool]] = []
            operation(lambda name, status: rows.append((name, status)))
            self.assertEqual(len(rows), expected)
            self.assertEqual(len({name for name, _ in rows}), expected)
            self.assertTrue(all(type(status) is bool and status for _, status in rows))
            self.assertTrue(all(type(name) is str and name for name, _ in rows))

    def test_cancellation_and_resource_failures_keep_distinct_semantics(self) -> None:
        module = load(STEM)
        with patch.object(module, "assembled_operator_checks", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                cli(module.main)
        errors = io.StringIO()
        with patch.object(module, "assembled_operator_checks", side_effect=OSError("injected resource failure")):
            with contextlib.redirect_stderr(errors):
                self.assertEqual(cli(module.main), 1)
        self.assertEqual(json.loads(errors.getvalue())["kind"], "resource")
        self.assertTrue(module.check()["all_passed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
