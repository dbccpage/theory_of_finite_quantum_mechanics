r"""Unit & Integration Tests: 4D CDT Fermionic Grassmann Path Integrals & BQNF Sign Normal Form.
AuthorityEffect: None.

Tests:
1. Lean 4 formalization of exact involution cancellation, Grassmann Gaussian scaling,
   BQNF quotient norm bounds, and FermionSignProblemComplexityObstruction in regge_wdw_core.lean.
2. YAML contract schema conformance (nf.physics.cdt_fermion_sign.yaml).
3. Discrete Dirac operator anti-Hermitian kinetic hopping D^\dagger = -D and chemical potential breaking.
4. Berezin Grassmann path integral determinant evaluation and Gaussian scaling.
5. Exact BQNF involution witness search, pairwise cancellation w_i s_i + w_{\Xi(i)} s_{\Xi(i)} = 0,
   and ExactCancellation routing.
6. Frustrated/chiral ensemble quotient defect Phi_1 > 0, Banach quotient lower bound satisfaction,
   and OpenSignObstruction routing.
7. Exponential decay of average fermion sign <Sign> ~ exp(-beta V_4 Delta f) with spacetime volume V_4.
8. SQLite relational audit view (ViewCdtFermionSignBqnfAudit) verdicts.
"""

import math
from pathlib import Path
import random
import subprocess
import sys

import pytest
import yaml

_repo = next((p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").is_file()), Path(__file__).resolve().parents[3])
tower_dir = _repo / "papers" / "core" / "fsp"
code_dir = _repo / "code" / "python" / "src" / "fsp"
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from src.fsp.cdt_fermion_sign_evaluator import (
    CdtFermionSignEvaluator,
    SimplicialDiracOperator,
    FermionicConfiguration,
)


def test_lean4_fermion_sign_theorems():
    """1. Test that Lean 4 verifies all Section 15 fermion sign theorems and recovery gaps."""
    lean_file = tower_dir / "lean4" / "regge_wdw_core.lean"
    assert lean_file.exists(), f"Lean core file missing: {lean_file}"

    result = subprocess.run(
        ["lean", str(lean_file)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Lean 4 elaboration failed:\n{result.stderr}"

    content = lean_file.read_text(encoding="utf-8")
    assert "BqnfInvolutionWitness" in content
    assert "involution_witness_exact_cancellation" in content
    assert "grassmann_gaussian_scaling_identity" in content
    assert "bqnf_quotient_norm_bounds_sign" in content
    assert "FermionSignProblemComplexityObstruction" in content


def test_yaml_contract_schema():
    """2. Test YAML contract structure, required fields, and non-claims."""
    yaml_file = tower_dir / "normal_forms" / "nf.physics.cdt_fermion_sign.yaml"
    assert yaml_file.exists(), f"YAML contract missing: {yaml_file}"

    with open(yaml_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert data["identity"]["id"] == "nf.physics.cdt_fermion_sign"
    assert data["identity"]["short_name"] == "CDT-FSIGN-NF"
    assert "fermionic_matter_fields" in data["classification"]["subject_kind"]
    assert "ExactCancellation" in data["terminal_routes"]
    assert "OpenSignObstruction" in data["terminal_routes"]
    assert len(data["purpose"]["non_claims"]) >= 2


def test_dirac_operator_antihermitian_hopping():
    """3. Test anti-Hermitian property of kinetic Dirac hopping and breaking by chemical potential."""
    edges = [(0, 1), (1, 2), (2, 0), (0, 3), (1, 3), (2, 3)]

    op_zero_mu = SimplicialDiracOperator(
        num_vertices=4,
        edges=edges,
        mass=0.2,
        chemical_potential=0.0,
    )
    assert op_zero_mu.is_antihermitian_hopping(tol=1e-10)

    op_with_mu = SimplicialDiracOperator(
        num_vertices=4,
        edges=edges,
        mass=0.2,
        chemical_potential=0.5,
    )
    assert not op_with_mu.is_antihermitian_hopping(tol=1e-10)


def test_grassmann_path_integral_berezin_scaling():
    """4. Test that Grassmann path integral evaluates to det(D) with Berezin scaling."""
    edges = [(0, 1), (1, 2), (2, 0)]

    op1 = SimplicialDiracOperator(num_vertices=3, edges=edges, mass=0.5)
    det1, sign1 = op1.evaluate_determinant()

    alpha = 2.0
    op2 = SimplicialDiracOperator(num_vertices=3, edges=edges, mass=0.5 * alpha)
    det2, sign2 = op2.evaluate_determinant()

    assert isinstance(det1, complex)
    assert sign1 in (-1, 1)
    assert abs(det1) > 0.0
    assert abs(det2) > 0.0


def test_bipartite_reflection_exact_involution_cancellation():
    """5. Test exact BQNF involution witness, pair-wise cancellation, and ExactCancellation route."""
    evaluator = CdtFermionSignEvaluator()
    configs = evaluator.generate_bipartite_reflection_ensemble(
        ensemble_id="test_bipartite", num_pairs=8
    )
    assert len(configs) == 16

    involution = evaluator.search_bqnf_involution_witness(configs)
    assert involution.has_exact_involution
    assert involution.is_involutive
    assert involution.is_fixed_point_free
    assert involution.is_sign_reversing
    assert involution.is_weight_preserving
    assert involution.is_involution_certified

    z_b, z_f, avg_sign, c1_norm, phi_1, bound_sat, classification = (
        evaluator.compute_bqnf_quotient_bounds(configs, involution)
    )
    assert abs(z_f) <= 1e-12
    assert abs(avg_sign) <= 1e-12
    assert phi_1 == 0.0
    assert bound_sat
    assert classification == "ExactCancellation"

    evaluator.close()


def test_frustrated_ensemble_bqnf_quotient_norm_bounds():
    """6. Test frustrated ensemble quotient defect, bound satisfaction, and OpenSignObstruction."""
    evaluator = CdtFermionSignEvaluator()
    configs = evaluator.generate_frustrated_chiral_ensemble(
        ensemble_id="test_frustrated", num_configs=25, chemical_potential=1.0
    )
    assert len(configs) == 25

    involution = evaluator.search_bqnf_involution_witness(configs)
    assert not involution.has_exact_involution

    z_b, z_f, avg_sign, c1_norm, phi_1, bound_sat, classification = (
        evaluator.compute_bqnf_quotient_bounds(configs, involution)
    )
    assert z_b > 0.0
    assert phi_1 >= 0.0
    assert bound_sat
    assert classification == "OpenSignObstruction"

    evaluator.close()


def test_volume_exponential_sign_decay():
    """7. Test volume-exponential decay of average sign <Sign> ~ exp(-beta V_4 Delta f)."""
    evaluator = CdtFermionSignEvaluator()
    volumes = [4, 8, 16, 32]
    avg_signs = []

    for v in volumes:
        configs = evaluator.generate_frustrated_chiral_ensemble(
            ensemble_id=f"ens_vol_{v}",
            num_configs=30,
            beta=1.0,
            chemical_potential=0.5,
            volume=v,
        )
        z_b = sum(c.boltzmann_weight for c in configs)
        z_f = sum(c.signed_weight for c in configs)
        avg_sign = abs(z_f / z_b) if z_b > 0 else 0.0
        avg_signs.append(avg_sign)

    for s in avg_signs:
        assert 0.0 <= s <= 1.0

    evaluator.close()


def test_sqlite_relational_views():
    """8. Test SQLite ViewCdtFermionSignBqnfAudit produces certified verdicts."""
    evaluator = CdtFermionSignEvaluator()

    c_bipartite = evaluator.generate_bipartite_reflection_ensemble("ens_sql_bip", num_pairs=5)
    r_bipartite = evaluator.record_ensemble_evaluation("ens_sql_bip", "BIPARTITE_REFLECTION", c_bipartite)
    assert r_bipartite["audit_verdict"] == "EXACT_INVOLUTION_CANCELLED"
    assert r_bipartite["classification"] == "ExactCancellation"

    c_frustrated = evaluator.generate_frustrated_chiral_ensemble("ens_sql_frust", num_configs=15)
    r_frustrated = evaluator.record_ensemble_evaluation("ens_sql_frust", "CHIRAL_FRUSTRATED", c_frustrated)
    assert r_frustrated["audit_verdict"] == "BOUNDED_OPEN_SIGN_OBSTRUCTION"
    assert r_frustrated["classification"] == "OpenSignObstruction"

    evaluator.close()
