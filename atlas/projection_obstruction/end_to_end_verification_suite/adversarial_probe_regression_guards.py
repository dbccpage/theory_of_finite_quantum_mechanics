"""Adversarial Falsification Probe for Republication Review Regression Guards.
Directly probes test_republication_review_regressions.py and r1_r10_checker.py failure paths with negative controls.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
import pytest

# Ensure proper sys.path
ESTATE_ROOT = Path(__file__).resolve().parent.parent
PO000_DIR = ESTATE_ROOT / "projection_obstruction_paper"
sys.path.insert(0, str(ESTATE_ROOT))
sys.path.insert(0, str(PO000_DIR / "code"))

from end_to_end_verification_suite.checks.r1_r10_checker import (
    audit_r1_po033_scope,
    audit_r2_sibling_reference_table,
    audit_r3_test_isolation,
    audit_r4_url_pin_ref36,
    audit_r5_ledger_migration,
    audit_r10_house_language_and_formatting,
)
from end_to_end_verification_suite.checks.bibliography_checker import check_bibliography
from end_to_end_verification_suite.checks.anchor_checker import check_proof_anchors


def test_guard_r1_po033_falsification():
    print("[REGRESSION GUARD 1] Probing R1 (PO-033 scope attribution) failure paths...")
    real_path = PO000_DIR / "projection_obstruction.md"
    orig_text = real_path.read_text(encoding="utf-8")

    # 1. Nominal check passes
    rep_nom = audit_r1_po033_scope(orig_text)
    assert rep_nom.passed, f"Nominal R1 audit failed: {rep_nom.violations}"

    # 2. Mutate manuscript to omit HEURISTIC_UNCERTIFIED (both upper and lower case)
    mutated_text_1 = re.sub(r"heuristic_uncertified", "CERTIFIED_SOLVER", orig_text, flags=re.IGNORECASE)
    rep_fail_1 = audit_r1_po033_scope(mutated_text_1)
    assert not rep_fail_1.passed, "R1 guard failed to catch missing HEURISTIC_UNCERTIFIED!"
    assert any("HEURISTIC_UNCERTIFIED" in v for v in rep_fail_1.violations)
    print("  [PASS] Caught missing HEURISTIC_UNCERTIFIED")

    # 3. Mutate manuscript to insert forbidden overclaim "quadrature certification"
    mutated_text_2 = orig_text + "\nProvides full quadrature certification for all lattices.\n"
    rep_fail_2 = audit_r1_po033_scope(mutated_text_2)
    assert not rep_fail_2.passed, "R1 guard failed to catch forbidden 'quadrature certification'!"
    assert any("quadrature certification" in v for v in rep_fail_2.violations)
    print("  [PASS] Caught injected 'quadrature certification'")


def test_guard_r2_phantom_packages_and_pins():
    print("\n[REGRESSION GUARD 2] Probing R2 (phantom packages & commit pins) failure paths...")
    real_path = PO000_DIR / "projection_obstruction.md"
    orig_text = real_path.read_text(encoding="utf-8")

    # 1. Inject phantom package PO-004
    mutated_1 = orig_text + "\nSee PO-004 for shear retraction proofs.\n"
    rep_fail_1 = audit_r2_sibling_reference_table(mutated_1)
    assert not rep_fail_1.passed, "R2 guard failed to catch phantom PO-004!"
    assert any("PO-004" in v for v in rep_fail_1.violations)
    print("  [PASS] Caught phantom package 'PO-004'")

    # 2. Inject phantom package PO-005
    mutated_2 = orig_text + "\nRefer to PO-005 for intermediate charts.\n"
    rep_fail_2 = audit_r2_sibling_reference_table(mutated_2)
    assert not rep_fail_2.passed, "R2 guard failed to catch phantom PO-005!"
    assert any("PO-005" in v for v in rep_fail_2.violations)
    print("  [PASS] Caught phantom package 'PO-005'")

    # 3. Remove historical commit pins
    mutated_3 = orig_text.replace("90e6231546", "0000000000").replace("d44f760555", "1111111111")
    rep_fail_3 = audit_r2_sibling_reference_table(mutated_3)
    assert not rep_fail_3.passed, "R2 guard failed to catch missing historical commit pins!"
    assert any("historical revision" in v for v in rep_fail_3.violations)
    print("  [PASS] Caught missing historical commit pins")


def test_guard_r4_url_pin_falsification():
    print("\n[REGRESSION GUARD 3] Probing R4 (Reference 36 URL pin) failure paths...")
    real_path = PO000_DIR / "projection_obstruction.md"
    orig_text = real_path.read_text(encoding="utf-8")

    # Corrupt Reference 36 commit pin and path
    mutated = orig_text.replace("4bdf074", "deadbeef").replace("4a4fd192f", "deadbeef")
    rep_fail = audit_r4_url_pin_ref36(mutated)
    assert not rep_fail.passed, "R4 guard failed to catch corrupted URL pin!"
    assert any("Reference [36]" in v or "invalid" in v for v in rep_fail.violations)
    print("  [PASS] Caught corrupted Reference 36 URL pin")


def test_guard_r5_proof_anchors_falsification():
    print("\n[REGRESSION GUARD 4] Probing R5 (proof anchors & claim dependencies) failure paths...")
    import tempfile
    real_deps = PO000_DIR / "docs" / "claim_dependencies.json"
    orig_deps_text = real_deps.read_text(encoding="utf-8")
    deps_data = json.loads(orig_deps_text)

    # 1. Probe audit_r5_ledger_migration with un-reconciled broken anchor
    broken_deps = orig_deps_text.replace('"disposition": "omitted"', '"disposition": "local"').replace('"disposition": "imported', '"disposition": "local')
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        (tdp / "docs").mkdir()
        (tdp / "docs" / "claim_dependencies.json").write_text(broken_deps, encoding="utf-8")
        rep_fail = audit_r5_ledger_migration(tdp)
        assert not rep_fail.passed, "R5 guard failed to catch broken anchor without omitted/imported disposition!"
        assert any("Broken local anchor" in v for v in rep_fail.violations)
        print("  [PASS] Caught broken local anchor when active in claim_dependencies.json")

    # 2. Probe check_proof_anchors with corrupted local proof anchor
    for claim in deps_data["claims"]:
        if claim.get("disposition") in (None, "local"):
            claim["proof_anchor"] = "**Theorem 999.99 (Nonexistent Phantom Anchor)**"
            break
    corrupted_deps = json.dumps(deps_data)
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        (tdp / "projection_obstruction.md").write_text((PO000_DIR / "projection_obstruction.md").read_text(encoding="utf-8"), encoding="utf-8")
        (tdp / "docs").mkdir()
        (tdp / "docs" / "claim_dependencies.json").write_text(corrupted_deps, encoding="utf-8")
        res = check_proof_anchors(tdp)
        assert not res.passed, "check_proof_anchors failed to catch Nonexistent Phantom Anchor!"
        assert any("Nonexistent Phantom Anchor" in u.get("anchor", "") for u in res.unresolved_anchors)
        print("  [PASS] check_proof_anchors caught Nonexistent Phantom Anchor")


def test_guard_r10_scaffolding_and_formatting():
    print("\n[REGRESSION GUARD 5] Probing R10 (scaffolding & malformed LaTeX) failure paths...")
    real_path = PO000_DIR / "projection_obstruction.md"
    orig_text = real_path.read_text(encoding="utf-8")

    # 1. Inject legacy scaffolding term
    mutated_1 = orig_text + "\n## Sovereign Mathematical Scope\n"
    rep_fail_1 = audit_r10_house_language_and_formatting(mutated_1)
    assert not rep_fail_1.passed, "R10 guard failed to catch legacy scaffolding term!"
    assert any("Sovereign Mathematical Scope" in v for v in rep_fail_1.violations)
    print("  [PASS] Caught legacy scaffolding term 'Sovereign Mathematical Scope'")

    # 2. Inject malformed LaTeX ^3$
    mutated_2 = orig_text + "\nScale is under a ^3$ term.\n"
    rep_fail_2 = audit_r10_house_language_and_formatting(mutated_2)
    assert not rep_fail_2.passed, "R10 guard failed to catch malformed '^3$'!"
    assert any("^3$" in v for v in rep_fail_2.violations)
    print("  [PASS] Caught malformed LaTeX '^3$'")


def test_guard_bibliography_orphan_falsification():
    print("\n[REGRESSION GUARD 6] Probing Bibliography orphan reference failure path...")
    import tempfile
    real_path = PO000_DIR / "projection_obstruction.md"
    orig_text = real_path.read_text(encoding="utf-8")

    # Add orphan reference [99] in References section
    mutated = orig_text + "\n99. J. Doe, \"Orphan Reference Never Cited in Body,\" Phys. Rev. X (2026).\n"
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        (tdp / "projection_obstruction.md").write_text(mutated, encoding="utf-8")
        bib_res = check_bibliography(tdp)
        assert not bib_res.passed, "Bibliography checker failed to catch orphan reference [99]!"
        assert 99 in bib_res.orphan_references
        print(f"  [PASS] Caught orphan reference {bib_res.orphan_references}")


if __name__ == "__main__":
    test_guard_r1_po033_falsification()
    test_guard_r2_phantom_packages_and_pins()
    test_guard_r4_url_pin_falsification()
    test_guard_r5_proof_anchors_falsification()
    test_guard_r10_scaffolding_and_formatting()
    test_guard_bibliography_orphan_falsification()
    print("\n>>> ALL REGRESSION GUARD FALSIFICATION PROBES PASSED CLEANLY <<<")
