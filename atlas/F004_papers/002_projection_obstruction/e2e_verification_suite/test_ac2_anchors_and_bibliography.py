"""Test Acceptance Criterion 2: Proof Anchors, Bibliography Completeness, and R1–R10 Regressions.

Verifies:
(a) Every local proof_anchor in projection_obstruction_claim_ledger.yaml and docs/claim_dependencies.json
    resolves in projection_obstruction.md.
(b) Every bibliography item [n] in the References section is cited in the body text of projection_obstruction.md.
(c) All R1–R10 regressions are guarded against recurrence.
(d) In-package automated tests in 000_projection_obstruction/code/tests/ execute and pass with 0 failures.

AuthorityEffect: None.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from .checks.anchor_checker import check_proof_anchors
from .checks.bibliography_checker import check_bibliography
from .checks.r1_r10_checker import audit_all_r1_r10
from .config import PO000_DIR


def test_ac2_a_every_local_proof_anchor_resolves():
    """AC2(a): Every local proof anchor in claim ledger & dependencies resolves in manuscript."""
    result = check_proof_anchors(PO000_DIR)
    assert not result.errors, f"Errors encountered during anchor check: {result.errors}"
    assert result.unresolved_count == 0, (
        f"Found {result.unresolved_count} unresolved local proof anchors in projection_obstruction.md:\n"
        + "\n".join(f"  - Claim {a['claim_id']} ({a['source']}): {a['anchor']}" for a in result.unresolved_anchors)
    )
    assert result.resolved_count > 0, "No local proof anchors found to verify."


def test_ac2_b_every_bibliography_item_is_cited_in_body():
    """AC2(b): Every reference [n] is cited in body text (zero orphan bibliography entries)."""
    result = check_bibliography(PO000_DIR)
    assert not result.errors, f"Errors in bibliography check: {result.errors}"
    assert not result.orphan_references, (
        f"Found orphan bibliography entries in References section not cited in body text: {result.orphan_references}"
    )
    assert not result.missing_definitions, (
        f"Found citations in body text missing from References section: {result.missing_definitions}"
    )
    assert result.ref36_valid, "Reference [36] historical URL pin is invalid."
    assert result.duhamel_priors_cited, "Martinazzo–Burghardt or Zoufal–Sutter–Woerner not cited."


def test_ac2_c_r1_r10_regressions_guarded():
    """AC2(c): Point-by-point verification that R1–R10 requirements are guarded against regression."""
    result = audit_all_r1_r10(PO000_DIR)
    assert not result.errors, f"Errors encountered in R1–R10 audit: {result.errors}"

    failed_reports = [r for r in result.reports.values() if not r.passed]
    if failed_reports:
        summary_lines = []
        for r in failed_reports:
            summary_lines.append(f"[{r.req_id}] {r.title}:")
            for v in r.violations:
                summary_lines.append(f"    - {v}")
        pytest.fail(f"R1–R10 regression violations detected:\n" + "\n".join(summary_lines))


def test_ac2_d_in_package_regression_tests_pass():
    """AC2(d): The automated test suite inside 000_projection_obstruction/code/tests/ passes cleanly."""
    in_pkg_test = PO000_DIR / "code" / "tests" / "test_republication_review_regressions.py"
    assert in_pkg_test.is_file(), "In-package test_republication_review_regressions.py not found"

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "code/tests/test_republication_review_regressions.py",
        "-q",
        "--disable-warnings",
        "--tb=short",
    ]
    proc = subprocess.run(cmd, cwd=PO000_DIR, capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, f"In-package regression test suite failed:\n{proc.stdout}\n{proc.stderr}"

