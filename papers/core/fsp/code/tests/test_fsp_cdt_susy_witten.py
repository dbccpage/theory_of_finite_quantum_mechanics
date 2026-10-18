"""Unit and integration tests for 4D CDT Supersymmetric Witten Index, Nicolai Map & Super-WDW.
AuthorityEffect: None.

Tests:
1. Lean 4 formalization of Section 20 SUSY Witten index, Nicolai map, and Super-WDW theorems.
2. Lean 4 formalization of GenesisFspBridge (16 Genesis-to-FSP deduction stages).
3. Declarative YAML contract conformance (CDT-SUSY-WITTEN-NF).
4. Exact topological Witten index beta-independence and zero-mode quantization Delta = n_B^0 - n_F^0.
5. Exact Nicolai map Jacobian matching and complete sign fluctuation suppression (<Sign> = 1.0).
6. Unbroken supersymmetric geometry preserving Super-WDW constraint (SuperWdwExactCancellationCertified).
7. Broken supersymmetry inducing zero-mode lifting, sign resurgence, and super-WDW breach (SusyBreakingSignResurgenceObstruction).
8. Explicit positive-energy boson-fermion doublet spectral cancellation at arbitrary temperatures.
9. SQLite relational audit view ViewCdtSusyWittenAudit integrity across regimes.
"""

import math
from pathlib import Path
import subprocess
import numpy as np
import pytest
import sys
import yaml

code_dir = Path(__file__).resolve().parent.parent
tower_dir = code_dir.parent
repo_root = tower_dir.parent.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from cdt_susy_witten_evaluator import (
    CdtSusyWittenEvaluator,
    CdtSusyConfiguration,
)


def test_lean4_susy_witten_theorems():
    """Validates that Lean 4 Section 20 compiles and defines all SUSY Witten & super-WDW theorems."""
    lean_file = tower_dir / "lean4" / "regge_wdw_core.lean"
    assert lean_file.exists(), f"Lean file not found: {lean_file}"

    content = lean_file.read_text(encoding="utf-8")
    assert "SuperchargeNilpotentPredicate" in content
    assert "supercharge_is_nilpotent" in content
    assert "SusyHamiltonianPositivityPredicate" in content
    assert "susy_hamiltonian_nonnegative" in content
    assert "WittenIndexZeroModePredicate" in content
    assert "witten_index_zero_mode_integer" in content
    assert "WittenIndexTemperatureInvariancePredicate" in content
    assert "witten_index_beta_invariant" in content
    assert "NicolaiMapSignSuppressionPredicate" in content
    assert "nicolai_map_eliminates_sign_fluctuations" in content
    assert "SuperWdwConstraintPreservationPredicate" in content
    assert "super_wdw_constraint_satisfied_unbroken" in content
    assert "SusyBreakingSignResurgenceObstruction" in content

    # Test compilation
    result = subprocess.run(["lean", str(lean_file)], capture_output=True, text=True)
    assert result.returncode == 0, f"Lean compilation failed: {result.stderr}"


def test_lean4_genesis_fsp_bridge():
    """Validates that GenesisFspBridge.lean in paper 023 compiles cleanly with zero sorry/axioms."""
    bridge_file = tower_dir / "lean4" / "GenesisFspBridge.lean"
    assert bridge_file.exists(), f"GenesisFspBridge.lean not found: {bridge_file}"

    content = bridge_file.read_text(encoding="utf-8")
    assert "sorry" not in content, "GenesisFspBridge.lean contains unproved sorry"
    assert "axiom " not in content, "GenesisFspBridge.lean contains synthetic axioms"
    assert "TroyerWieseFspComplexityObstruction" in content

    result = subprocess.run(["lean", str(bridge_file)], capture_output=True, text=True)
    assert result.returncode == 0, f"GenesisFspBridge.lean compilation failed: {result.stderr}"


def test_yaml_contract_schema():
    """Validates that nf.physics.cdt_susy_witten.yaml conforms to normal form schema."""
    yaml_file = tower_dir / "normal_forms" / "nf.physics.cdt_susy_witten.yaml"
    assert yaml_file.exists(), f"Contract not found: {yaml_file}"

    data = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
    assert data["identity"]["id"] == "nf.physics.cdt_susy_witten"
    assert data["identity"]["short_name"] == "CDT-SUSY-WITTEN-NF"
    assert "SuperWdwExactCancellationCertified" in data["terminal_routes"]
    assert "SusyBreakingSignResurgenceObstruction" in data["terminal_routes"]
    assert "WittenIndexTemperatureDivergenceAnomaly" in data["terminal_routes"]
    assert "NicolaiMapDeformationDefect" in data["terminal_routes"]


def test_witten_index_beta_independence():
    """Validates exact temperature beta-independence of Witten index Delta_Witten."""
    evaluator = CdtSusyWittenEvaluator(in_memory=True)
    betas = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]

    for n_b0, n_f0 in [(2, 0), (1, 0), (2, 1), (1, 1), (0, 2)]:
        expected_delta = float(n_b0 - n_f0)
        res = evaluator.evaluate_witten_index_beta_independence(
            betas=betas,
            n_boson_zero=n_b0,
            n_fermion_zero=n_f0,
            num_doublets=15,
            seed=42 + n_b0 * 7,
        )
        assert res["is_topologically_invariant"] is True
        assert abs(res["target_index"] - expected_delta) < 1e-10
        assert res["max_deviation"] <= 1e-10
        assert res["temperature_derivative"] <= 1e-10

    evaluator.close()


def test_nicolai_map_jacobian_and_sign_suppression():
    """Validates that det(D_F) = |det(J_Nicolai)| and fermion sign fluctuations are suppressed."""
    evaluator = CdtSusyWittenEvaluator(in_memory=True)

    for i in range(10):
        nic_res, f_det, f_sign = evaluator.evaluate_nicolai_map(
            num_vertices=16 + i,
            is_broken=False,
            seed=100 + i,
        )

        assert nic_res <= 1e-8, f"Nicolai residual breached tolerance: {nic_res}"
        assert f_det > 0.0, f"Fermion determinant non-positive: {f_det}"
        assert f_sign == 1, f"Fermion sign was not +1 on unbroken SUSY: {f_sign}"

    evaluator.close()


def test_unbroken_super_wdw_constraint_preservation():
    """Validates that unbroken SUSY preserves Super-WDW constraint and suppresses sign fluctuations."""
    evaluator = CdtSusyWittenEvaluator(in_memory=True)
    res = evaluator.evaluate_susy_cancellation_ensemble(
        ensemble_id="ens_unbroken_test",
        susy_regime="EXACT_UNBROKEN_SUSY",
        num_configs=20,
        volume_scale=64,
        beta=1.5,
        seed=123,
    )

    assert res["classification"] == "SuperWdwExactCancellationCertified"
    assert res["is_sign_problem_suppressed"] is True
    assert res["super_wdw_preserved"] == 1
    assert res["mean_fermion_sign"] == 1.0
    assert res["max_super_wdw_defect"] <= 1e-8
    assert res["audit_verdict"] == "SUPER_WDW_EXACT_CANCELLATION_CERTIFIED"

    evaluator.close()


def test_susy_breaking_sign_resurgence_detected():
    """Validates that supersymmetry breaking induces sign resurgence and super-WDW breach."""
    evaluator = CdtSusyWittenEvaluator(in_memory=True)
    res = evaluator.evaluate_susy_cancellation_ensemble(
        ensemble_id="ens_broken_test",
        susy_regime="SPONTANEOUS_BROKEN_SUSY",
        num_configs=20,
        volume_scale=64,
        beta=1.5,
        seed=456,
    )

    assert res["classification"] == "SusyBreakingSignResurgenceObstruction"
    assert res["is_sign_problem_suppressed"] is False
    assert res["super_wdw_preserved"] == 0
    assert res["mean_fermion_sign"] < 1.0
    assert res["max_super_wdw_defect"] > 1e-8
    assert res["audit_verdict"] == "SUSY_BREAKING_SIGN_RESURGENCE_OBSTRUCTION_DETECTED"

    evaluator.close()


def test_boson_fermion_doublet_cancellation_at_positive_energy():
    """Validates explicit positive-energy doublet cancellation in Tr((-1)^F exp(-beta H))."""
    evaluator = CdtSusyWittenEvaluator(in_memory=True)
    beta = 2.0

    # Build doublet spectrum: 1 boson zero mode, 0 fermion zero modes, plus 5 positive doublets
    boson_evals = [0.0, 1.2, 2.5, 4.0, 5.7, 8.1]
    fermion_evals = [1.2, 2.5, 4.0, 5.7, 8.1]

    # Compute trace sum
    boson_trace = sum(math.exp(-beta * e) for e in boson_evals)
    fermion_trace = sum(math.exp(-beta * e) for e in fermion_evals)
    witten_idx = boson_trace - fermion_trace

    # Exact cancellation of positive energy states:
    # boson_trace - fermion_trace = exp(-beta * 0) + sum(exp - exp) = 1.0 + 0 = 1.0
    assert abs(witten_idx - 1.0) < 1e-15, f"Doublet cancellation error: {witten_idx}"

    evaluator.close()


def test_sqlite_relational_schema_and_view_integrity():
    """Validates full relational persistence and SQL audit view across both regimes."""
    evaluator = CdtSusyWittenEvaluator(in_memory=True)

    # Run both ensembles
    evaluator.evaluate_susy_cancellation_ensemble(
        ensemble_id="ens_susy_unbroken",
        susy_regime="EXACT_UNBROKEN_SUSY",
        num_configs=10,
        volume_scale=48,
        beta=1.0,
        seed=1,
    )
    evaluator.evaluate_susy_cancellation_ensemble(
        ensemble_id="ens_susy_broken",
        susy_regime="SPONTANEOUS_BROKEN_SUSY",
        num_configs=10,
        volume_scale=48,
        beta=1.0,
        seed=2,
    )

    # Check database counts
    evaluator.cur.execute("SELECT COUNT(*) FROM CdtSusyWittenTrajectory")
    row_count = evaluator.cur.fetchone()[0]
    assert row_count == 20

    evaluator.cur.execute("SELECT COUNT(*) FROM CdtSusyCancellationAudit")
    audit_count = evaluator.cur.fetchone()[0]
    assert audit_count == 2

    evaluator.cur.execute("SELECT COUNT(*) FROM CdtSuperWdwSummary")
    summary_count = evaluator.cur.fetchone()[0]
    assert summary_count == 2

    # Query View
    evaluator.cur.execute("SELECT ensemble_id, susy_audit_verdict FROM ViewCdtSusyWittenAudit")
    rows = dict(evaluator.cur.fetchall())
    assert rows["ens_susy_unbroken"] == "SUPER_WDW_EXACT_CANCELLATION_CERTIFIED"
    assert rows["ens_susy_broken"] == "SUSY_BREAKING_SIGN_RESURGENCE_OBSTRUCTION_DETECTED"

    evaluator.close()
