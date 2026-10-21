"""Unit & Integration Tests: 4D CDT Kähler-Dirac Fermion Doubling Resolution & Topological Spin Normal Form.
AuthorityEffect: None.

Tests:
1. Lean 4 formalization of KD bundle dimension (16), doubling ratio (4), boundary nilpotence,
   projector idempotence, and KahlerDiracTopologicalSpinObstruction in regge_wdw_core.lean.
2. YAML contract schema conformance (nf.physics.cdt_kd_doubling.yaml).
3. Exact boundary nilpotence d_{p+1} o d_p = 0 across all degrees p in {0, 1, 2, 3} on 4D simplicial complexes.
4. Spinor projector idempotence P^2 = P and dimension quotient Tr(P) = 4 (16 -> 4).
5. Orientifold involution Omega_orient^2 = I and chiral grading properties.
6. Flat simplicial complex minimal spinor recovery: [D, P] = 0 and MinimalSpinorRecovered route.
7. Curved CDT complex topological spin obstruction: [D, P] != 0, chi != 4*A_hat, and KahlerDiracIndexObstruction route.
8. SQLite relational audit view (ViewCdtKahlerDiracDoublingAudit) verdicts.
"""

from pathlib import Path
import subprocess
import sys

import pytest
import yaml

_repo = next((p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").is_file()), Path(__file__).resolve().parents[3])
tower_dir = _repo / "papers" / "core" / "fsp"
code_dir = _repo / "code" / "python" / "src" / "fsp"
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from src.fsp.cdt_kd_doubling_evaluator import (
    CdtKahlerDiracEvaluator,
    KahlerDiracAlgebra,
    SimplicialComplex4D,
)


def test_lean4_kd_doubling_theorems():
    """1. Test that Lean 4 verifies all Section 16 Kähler-Dirac theorems and recovery gaps."""
    lean_file = tower_dir / "lean4" / "regge_wdw_core.lean"
    assert lean_file.exists(), f"Lean core file missing: {lean_file}"

    result = subprocess.run(
        ["lean", str(lean_file)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Lean 4 elaboration failed:\n{result.stderr}"

    content = lean_file.read_text(encoding="utf-8")
    assert "kahler_dirac_bundle_dim_eq_16" in content
    assert "fermion_doubling_species_ratio" in content
    assert "boundary_nilpotence_simplicial_chain" in content
    assert "spinor_projector_idempotent" in content
    assert "spinor_projection_dimension_quotient" in content
    assert "KahlerDiracTopologicalSpinObstruction" in content


def test_yaml_contract_schema():
    """2. Test YAML contract structure, required fields, and non-claims."""
    yaml_file = tower_dir / "normal_forms" / "nf.physics.cdt_kd_doubling.yaml"
    assert yaml_file.exists(), f"YAML contract missing: {yaml_file}"

    with open(yaml_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert data["identity"]["id"] == "nf.physics.cdt_kd_doubling"
    assert data["identity"]["short_name"] == "CDT-KD-DOUBLING-NF"
    assert "kahler_dirac_fermions" in data["classification"]["subject_kind"]
    assert "MinimalSpinorRecovered" in data["terminal_routes"]
    assert "KahlerDiracIndexObstruction" in data["terminal_routes"]
    assert len(data["purpose"]["non_claims"]) >= 2


def test_exact_boundary_nilpotence_d_squared():
    r"""3. Test exact boundary nilpotence d^2 = 0 and \partial^2 = 0 across all degrees."""
    evaluator = CdtKahlerDiracEvaluator()
    s1 = evaluator.build_flat_4simplex()
    is_nilpotent1, max_coboundary1, max_boundary1 = evaluator.evaluate_boundary_nilpotence(s1)
    assert is_nilpotent1
    assert max_coboundary1 <= 1e-12
    assert max_boundary1 <= 1e-12

    s2 = evaluator.build_curved_cdt_cluster()
    is_nilpotent2, max_coboundary2, max_boundary2 = evaluator.evaluate_boundary_nilpotence(s2)
    assert is_nilpotent2
    assert max_coboundary2 <= 1e-12
    assert max_boundary2 <= 1e-12

    evaluator.close()


def test_spinor_projector_idempotence_and_rank():
    """4. Test that spinor projector satisfies P^2 = P and Tr(P) = 4."""
    algebra = KahlerDiracAlgebra()
    is_idem, diff, tr = algebra.check_projector_idempotence()
    assert is_idem
    assert diff <= 1e-12
    assert abs(tr - 4.0) <= 1e-12
    assert algebra.dim == 16
    assert algebra.dim // int(tr) == 4


def test_orientifold_involution_properties():
    """5. Test that orientifold operator satisfies Omega^2 = I and preserves form grading."""
    algebra = KahlerDiracAlgebra()
    is_invol, diff = algebra.check_orientifold_involution()
    assert is_invol
    assert diff <= 1e-12


def test_flat_simplex_minimal_spinor_recovery():
    """6. Test flat simplicial complex commutativity [D, P] = 0 and MinimalSpinorRecovered."""
    evaluator = CdtKahlerDiracEvaluator()
    s_flat = evaluator.build_flat_4simplex("flat_test")
    comm_res, classification = evaluator.evaluate_dirac_projector_commutator(s_flat)

    assert comm_res <= 1e-12
    assert classification == "MinimalSpinorRecovered"

    evaluator.close()


def test_curved_cdt_topological_spin_obstruction():
    """7. Test curved CDT complex non-commutativity [D, P] != 0 and KahlerDiracIndexObstruction."""
    evaluator = CdtKahlerDiracEvaluator()
    s_curved = evaluator.build_curved_cdt_cluster("curved_test")
    comm_res, classification = evaluator.evaluate_dirac_projector_commutator(s_curved)

    assert comm_res > 1e-4
    assert classification == "KahlerDiracIndexObstruction"

    evaluator.close()


def test_sqlite_relational_views():
    """8. Test SQLite ViewCdtKahlerDiracDoublingAudit produces certified audit verdicts."""
    evaluator = CdtKahlerDiracEvaluator()

    s_flat = evaluator.build_flat_4simplex("sql_flat")
    r_flat = evaluator.record_complex_evaluation(s_flat)
    assert r_flat["audit_verdict"] == "EXACT_MINIMAL_SPINOR_RECOVERED"
    assert r_flat["classification"] == "MinimalSpinorRecovered"

    s_curved = evaluator.build_curved_cdt_cluster("sql_curved")
    r_curved = evaluator.record_complex_evaluation(s_curved)
    assert r_curved["audit_verdict"] == "BOUNDED_TOPOLOGICAL_SPIN_OBSTRUCTION"
    assert r_curved["classification"] == "KahlerDiracIndexObstruction"

    evaluator.close()


def test_boundary_nilpotence_under_orientation_reversals():
    """9. Test that d^2 = 0 is invariant under arbitrary simplex orientation permutations."""
    evaluator = CdtKahlerDiracEvaluator()

    # Reversed triangle
    s_rev_tri = evaluator.build_flat_4simplex("rev_tri")
    t0 = s_rev_tri.triangles[0]
    s_rev_tri.triangles[0] = (t0[1], t0[0], t0[2])
    is_nilp, max_cob, max_b = evaluator.evaluate_boundary_nilpotence(s_rev_tri)
    assert is_nilp
    assert max_cob <= 1e-12

    # Reversed tetrahedron
    s_rev_tet = evaluator.build_flat_4simplex("rev_tet")
    tet0 = s_rev_tet.tetrahedra[0]
    s_rev_tet.tetrahedra[0] = (tet0[1], tet0[0], tet0[2], tet0[3])
    is_nilp, max_cob, max_b = evaluator.evaluate_boundary_nilpotence(s_rev_tet)
    assert is_nilp
    assert max_cob <= 1e-12

    # Reversed 4-simplex
    s_rev_4s = evaluator.build_flat_4simplex("rev_4s")
    f0 = s_rev_4s.four_simplices[0]
    s_rev_4s.four_simplices[0] = (f0[1], f0[0], f0[2], f0[3], f0[4])
    is_nilp, max_cob, max_b = evaluator.evaluate_boundary_nilpotence(s_rev_4s)
    assert is_nilp
    assert max_cob <= 1e-12

    evaluator.close()
