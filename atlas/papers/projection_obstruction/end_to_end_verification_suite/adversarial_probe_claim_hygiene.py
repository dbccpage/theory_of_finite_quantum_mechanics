"""Adversarial Falsification Probe for Claim Hygiene Auditor.
Directly probes claim_hygiene_auditor.py with negative controls.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pytest

from end_to_end_verification_suite.checks.claim_hygiene_auditor import (
    audit_claim_hygiene_in_file,
    audit_all_packages_claim_hygiene,
    is_allowed_context,
    HygieneViolation,
    ClaimHygieneReport,
)
from end_to_end_verification_suite.config import CLAIM_HYGIENE_FORBIDDEN_WORDS, PackageSpec


def test_each_forbidden_word():
    print("[TEST 1] Probing all 14 forbidden words individually...")
    for word in CLAIM_HYGIENE_FORBIDDEN_WORDS:
        with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False, encoding="utf-8") as tf:
            tf.write(f"This construction {word} the main outcome without doubt.\n")
            tf_path = Path(tf.name)
        try:
            violations = audit_claim_hygiene_in_file("TEST_PKG", tf_path)
            assert len(violations) >= 1, f"Auditor failed to catch forbidden word: {word}"
            assert violations[0].matched_word == word.lower()
            print(f"  [PASS] Caught '{word}': {violations[0].line_context}")
        finally:
            tf_path.unlink(missing_ok=True)


def test_case_insensitivity():
    print("\n[TEST 2] Probing case variations (UPPER, Title, mIxEd)...")
    test_cases = ["PROVES", "Guarantees", "mAtHeMaTiCaLlY vErIfIeS", "FLAWLESS", "wEaPoNiZeD"]
    for word in test_cases:
        with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False, encoding="utf-8") as tf:
            tf.write(f"Header: {word} is unearned.\n")
            tf_path = Path(tf.name)
        try:
            violations = audit_claim_hygiene_in_file("TEST_PKG", tf_path)
            assert len(violations) >= 1, f"Auditor failed to catch case variant: {word}"
            print(f"  [PASS] Caught case variant '{word}'")
        finally:
            tf_path.unlink(missing_ok=True)


def test_allowed_vs_forbidden_contexts():
    print("\n[TEST 3] Probing allowed mathematical exceptions vs forbidden variants...")
    allowed_samples = [
        "satisfies the universal product lower bound on product states",
        "forms a universal cover for the fiber",
        "satisfies the universal property of quotient complexes",
        "relation: \"proves\"",
        "proves under declared assumptions that the defect is positive",
        "J. C. Cresswell, \"Universal entanglement timescale for Rényi entropies,\"",
    ]
    for sample in allowed_samples:
        with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False, encoding="utf-8") as tf:
            tf.write(f"{sample}\n")
            tf_path = Path(tf.name)
        try:
            violations = audit_claim_hygiene_in_file("TEST_PKG", tf_path)
            assert len(violations) == 0, f"False positive on allowed phrase: {sample} -> {violations}"
            print(f"  [PASS] Allowed phrase permitted: '{sample[:50]}...'")
        finally:
            tf_path.unlink(missing_ok=True)

    forbidden_unhedged = [
        "Theorem 5.1 proves the defect bound directly.",
        "This metric is universal across all physical manifolds.",
        "It is impossible to find a counterexample.",
        "The proof is flawless and requires no further checks.",
        "This is weaponized claim verification.",
    ]
    for sample in forbidden_unhedged:
        with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False, encoding="utf-8") as tf:
            tf.write(f"{sample}\n")
            tf_path = Path(tf.name)
        try:
            violations = audit_claim_hygiene_in_file("TEST_PKG", tf_path)
            assert len(violations) >= 1, f"Failed to flag unhedged usage: {sample}"
            print(f"  [PASS] Unhedged phrase correctly flagged: '{sample}'")
        finally:
            tf_path.unlink(missing_ok=True)


def test_estate_level_aggregation_and_fail_closed():
    print("\n[TEST 4] Probing estate-level aggregation and fail-closed property...")
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        manuscript = tdp / "test_manuscript.md"
        manuscript.write_text("This result clearly proves everything.\n", encoding="utf-8")
        
        mock_spec = PackageSpec(
            pkg_id="999",
            name="999_mock_package",
            path=tdp,
            manuscript_name="test_manuscript.md",
            pytest_command=[],
            deposit_verifier_command=[],
        )
        report = audit_all_packages_claim_hygiene({"999": mock_spec})
        assert not report.passed, "Report must fail when violations are present"
        assert report.violations_count == 2, f"Expected 2 violations ('clearly', 'proves'), got {report.violations_count}"
        assert report.total_files_scanned == 1
        assert report.clean_files_count == 0
        print(f"  [PASS] Estate aggregation detected {report.violations_count} violations and marked passed=False")


if __name__ == "__main__":
    test_each_forbidden_word()
    test_case_insensitivity()
    test_allowed_vs_forbidden_contexts()
    test_estate_level_aggregation_and_fail_closed()
    print("\n>>> ALL CLAIM HYGIENE FALSIFICATION PROBES PASSED CLEANLY <<<")
