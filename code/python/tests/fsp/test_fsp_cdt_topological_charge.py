"""Unit and integration tests for 4D CDT Topological Charge Fluctuations & Instanton Susceptibility.
AuthorityEffect: None.

Tests:
1. Lean 4 formalization of Section 19 topological charge and WDW constraint theorems.
2. Lean 4 formalization of GenesisFspBridge (16 Genesis-to-FSP deduction stages).
3. Declarative YAML contract conformance (CDT-TOPO-CHARGE-NF).
4. Exact integer Atiyah-Singer topological charge quantization Q = (1/2) Tr(gamma_5 a D_rat) = n_+ - n_-.
5. Semiclassical instanton tunneling preserving WDW constraint (TopologicalTunnelingWdwCertified).
6. Quantum foam tearing breaching WDW Hamiltonian constraint (TopologicalSusceptibilityWdwBreachObstruction).
7. Instanton susceptibility finite-size thermodynamic volume scaling.
8. SQLite relational audit view ViewCdtTopologicalChargeAudit integrity across regimes.
"""

from pathlib import Path
import subprocess
import numpy as np
import pytest
import sys
import yaml

repo_root = next((p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").is_file()), Path(__file__).resolve().parents[3])
tower_dir = repo_root / "papers" / "core" / "fsp"
code_dir = repo_root / "code" / "python" / "src" / "fsp"
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from src.fsp.cdt_topological_charge_evaluator import (
    CdtTopologicalChargeEvaluator,
    CdtMonteCarloConfiguration,
)


def test_lean4_topological_charge_theorems():
    """Validates that Lean 4 Section 19 compiles and defines all topological charge theorems."""
    lean_file = tower_dir / "lean4" / "regge_wdw_core.lean"
    assert lean_file.exists(), f"Lean file not found: {lean_file}"

    content = lean_file.read_text(encoding="utf-8")
    assert "TopologicalChargeIntegerPredicate" in content
    assert "topological_charge_integer_index" in content
    assert "TopologicalSusceptibilityScalingPredicate" in content
    assert "topological_susceptibility_volume_scaling" in content
    assert "WdwConstraintPreservationPredicate" in content
    assert "instantons_preserve_wdw_constraint" in content
    assert "TopologicalSusceptibilityWdwBreachObstruction" in content

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
    assert "swap_invariant_blind" in content
    assert "discrete_stokes_cancellation" in content
    assert "grassmann_berezin_determinant_identity" in content
    assert "bqnf_quotient_bounds_average_sign" in content

    result = subprocess.run(["lean", str(bridge_file)], capture_output=True, text=True)
    assert result.returncode == 0, f"GenesisFspBridge.lean compilation failed: {result.stderr}"


def test_yaml_contract_schema():
    """Validates that nf.physics.cdt_topological_charge.yaml conforms to normal form schema."""
    yaml_file = tower_dir / "normal_forms" / "nf.physics.cdt_topological_charge.yaml"
    assert yaml_file.exists(), f"Contract not found: {yaml_file}"

    data = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
    assert data["identity"]["id"] == "nf.physics.cdt_topological_charge"
    assert data["identity"]["short_name"] == "CDT-TOPO-CHARGE-NF"
    assert "TopologicalTunnelingWdwCertified" in data["terminal_routes"]
    assert "TopologicalSusceptibilityWdwBreachObstruction" in data["terminal_routes"]
    assert "TopologicalChargeNonIntegerAnomaly" in data["terminal_routes"]
    assert "InstantonSusceptibilityDivergenceDefect" in data["terminal_routes"]


def test_topological_charge_integer_quantization():
    """Validates exact integer Atiyah-Singer topological charge quantization."""
    evaluator = CdtTopologicalChargeEvaluator(in_memory=True)
    test_charges = [-2, -1, 0, 1, 2]

    for target_q in test_charges:
        d_rat, gamma_5, n_pos, n_neg = evaluator.build_synthetic_instanton_operator(
            num_vertices=6, target_Q=target_q, is_tearing=False
        )
        trace_val = float(np.real(np.trace(gamma_5 @ d_rat)))
        q_calc = 0.5 * trace_val
        assert abs(q_calc - target_q) < 1e-5, f"Expected Q={target_q}, got {q_calc}"
        assert n_pos - n_neg == target_q, f"Zero mode mismatch for Q={target_q}"

    evaluator.close()


def test_semiclassical_instanton_tunneling_certified():
    """Validates that smooth semiclassical instanton ensembles preserve WDW constraint."""
    evaluator = CdtTopologicalChargeEvaluator(in_memory=True)
    res = evaluator.evaluate_instanton_susceptibility_ensemble(
        ensemble_id="ens_semiclassical_test",
        geometry_regime="SMOOTH_SEMICLASSICAL",
        num_configs=20,
        volume_scale=64,
        seed=123,
    )

    assert res["classification"] == "TopologicalTunnelingWdwCertified"
    assert res["instanton_tunneling_permitted"] == 1
    assert res["max_wdw_defect"] <= 1e-8
    assert res["audit_verdict"] == "TOPOLOGICAL_TUNNELING_WDW_CERTIFIED"
    assert res["all_charges_integer"] is True
    assert res["instanton_susceptibility"] > 0.0

    evaluator.close()


def test_quantum_foam_tearing_wdw_breach_detected():
    """Validates that violent quantum geometry tearing breaches WDW Hamiltonian constraint."""
    evaluator = CdtTopologicalChargeEvaluator(in_memory=True)
    res = evaluator.evaluate_instanton_susceptibility_ensemble(
        ensemble_id="ens_tearing_test",
        geometry_regime="QUANTUM_FOAM_TEARING",
        num_configs=20,
        volume_scale=64,
        seed=456,
    )

    assert res["classification"] == "TopologicalSusceptibilityWdwBreachObstruction"
    assert res["instanton_tunneling_permitted"] == 0
    assert res["max_wdw_defect"] > 1e-8
    assert res["audit_verdict"] == "WDW_CONSTRAINT_BREACH_OBSTRUCTION_DETECTED"
    assert res["all_charges_integer"] is True

    evaluator.close()


def test_instanton_susceptibility_finite_volume_scaling():
    """Validates thermodynamic volume scaling of instanton susceptibility chi_t."""
    evaluator = CdtTopologicalChargeEvaluator(in_memory=True)
    scaling_res = evaluator.evaluate_volume_scaling(
        volumes=[32, 64, 128, 256],
        num_configs_per_vol=30,
    )

    assert scaling_res["is_thermodynamically_stable"] is True
    assert 0.0 < scaling_res["mean_susceptibility"] < 1.0
    for chi in scaling_res["susceptibilities"]:
        assert chi > 0.0, f"Instanton susceptibility {chi} was non-positive"

    evaluator.close()


def test_sqlite_relational_schema_and_view_integrity():
    """Validates full relational persistence and SQL audit view across both regimes."""
    evaluator = CdtTopologicalChargeEvaluator(in_memory=True)

    # Run both ensembles
    evaluator.evaluate_instanton_susceptibility_ensemble(
        ensemble_id="ens_regime_a",
        geometry_regime="SMOOTH_SEMICLASSICAL",
        num_configs=10,
        volume_scale=48,
        seed=1,
    )
    evaluator.evaluate_instanton_susceptibility_ensemble(
        ensemble_id="ens_regime_b",
        geometry_regime="QUANTUM_FOAM_TEARING",
        num_configs=10,
        volume_scale=48,
        seed=2,
    )

    # Check database counts
    evaluator.cur.execute("SELECT COUNT(*) FROM CdtTopologicalChargeTrajectory")
    row_count = evaluator.cur.fetchone()[0]
    assert row_count == 20

    evaluator.cur.execute("SELECT COUNT(*) FROM CdtInstantonSusceptibilityAudit")
    audit_count = evaluator.cur.fetchone()[0]
    assert audit_count == 2

    evaluator.cur.execute("SELECT COUNT(*) FROM CdtTopologicalWdwSummary")
    summary_count = evaluator.cur.fetchone()[0]
    assert summary_count == 2

    # Query View
    evaluator.cur.execute("SELECT ensemble_id, topological_audit_verdict FROM ViewCdtTopologicalChargeAudit")
    rows = dict(evaluator.cur.fetchall())
    assert rows["ens_regime_a"] == "TOPOLOGICAL_TUNNELING_WDW_CERTIFIED"
    assert rows["ens_regime_b"] == "WDW_CONSTRAINT_BREACH_OBSTRUCTION_DETECTED"

    evaluator.close()
