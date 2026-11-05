"""Test Acceptance Criterion 6: Point-by-Point R1–R10 Audit and Estate-Wide Claim Hygiene.

Verifies:
Point-by-point audit of R1–R10 against manuscripts and rebuilt PDFs across all 9 packages
under strict Claim Hygiene.

AuthorityEffect: None.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from .checks.claim_hygiene_auditor import audit_all_packages_claim_hygiene
from .checks.r1_r10_checker import audit_all_r1_r10
from .config import ALL_PACKAGES, EXPECTED_SIBLING_TABLE_ROWS, PO000_DIR, SIBLING_PACKAGES


def test_ac6_point_by_point_r1_r10_audit():
    """AC6: Audit R1 through R10 against PO-000 manuscript and repository assets."""
    audit_res = audit_all_r1_r10(PO000_DIR)
    assert not audit_res.errors, f"Errors during R1–R10 audit: {audit_res.errors}"

    failed_reports = [r for r in audit_res.reports.values() if not r.passed]
    if failed_reports:
        msg_lines = ["R1–R10 Point-by-Point Audit Violations:"]
        for r in failed_reports:
            msg_lines.append(f"\n[{r.req_id}] {r.title}:")
            for v in r.violations:
                msg_lines.append(f"  * {v}")
        pytest.fail("\n".join(msg_lines))


def test_ac6_cross_package_claim_hygiene():
    """AC6: Enforce strict Claim Hygiene across all 9 packages (no unearned hype verbs or forbidden words)."""
    hygiene_report = audit_all_packages_claim_hygiene(ALL_PACKAGES)
    assert hygiene_report.total_files_scanned > 0, "No files scanned for claim hygiene."

    if hygiene_report.violations:
        v_lines = ["Estate-Wide Claim Hygiene Violations:"]
        for v in hygiene_report.violations[:20]:  # Cap output to top 20
            v_lines.append(f"  * [{v.package_id}] {Path(v.file_path).name}:{v.line_number} word '{v.matched_word}' in: {v.line_context}")
        if len(hygiene_report.violations) > 20:
            v_lines.append(f"  ... and {len(hygiene_report.violations) - 20} more violations.")
        pytest.fail("\n".join(v_lines))


def test_ac6_cross_package_reference_table_consistency():
    """AC6: Validate that Authoritative Sibling Reference Table entries in PO-000 match actual sibling package titles."""
    manuscript_path = PO000_DIR / "projection_obstruction.md"
    assert manuscript_path.is_file(), "PO-000 manuscript missing"
    text = manuscript_path.read_text(encoding="utf-8")

    for row in EXPECTED_SIBLING_TABLE_ROWS:
        pkg_id = row["pkg"]
        anchor = row["anchor"]
        assert anchor in text, f"Missing sibling anchor {anchor} in PO-000 manuscript"

        spec = SIBLING_PACKAGES.get(pkg_id)
        assert spec is not None, f"Sibling package {pkg_id} not declared in config"
        assert spec.path.is_dir(), f"Sibling package directory missing: {spec.path}"
        assert (spec.path / spec.manuscript_name).is_file(), (
            f"Sibling manuscript missing for {pkg_id}: {spec.manuscript_name}"
        )
