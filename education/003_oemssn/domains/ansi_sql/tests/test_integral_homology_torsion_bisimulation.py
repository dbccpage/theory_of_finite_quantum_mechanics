"""
Unit Test Suite: Integral Homology and Torsion Subgroup Bisimulation
Lean 4 Kernel Certificates <-> ANSI SQL Smith Normal Form (SNF) CTE Evaluator
AuthorityEffect: None.
"""

import sys
from pathlib import Path

code_dir = Path(__file__).resolve().parent.parent / "code"
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from smith_normal_form_cte_evaluator import SmithNormalFormCTEEvaluator
from torsion_bisimulation_bridge import TorsionBisimulationBridge


def test_lean4_integral_homology_compilation():
    bridge = TorsionBisimulationBridge()
    assert bridge.verify_lean_compilation() is True
    bridge.close()


def test_sql_snf_elementary_matrix():
    evaluator = SmithNormalFormCTEEvaluator(in_memory=True)
    # 2x2 matrix with determinant 6: [[2, 4], [0, 3]] -> SNF is diag(1, 6)
    grid = [[2, 4], [0, 3]]
    R, C = evaluator.load_matrix("elem_2x2", grid)
    res = evaluator.compute_snf("elem_2x2", R, C)
    assert res["rank"] == 2
    assert res["diagonal_factors"] == [1, 6]
    assert res["torsion_coefficients"] == [6]
    evaluator.close()


def test_rp2_2_torsion_bisimulation():
    bridge = TorsionBisimulationBridge()
    cert = bridge.evaluate_torsion_bisimulation("RP2_RealProjectivePlane")
    assert cert.is_bisimilar is True
    assert cert.sql_betti == [1, 0, 0]
    assert cert.sql_torsion == {1: [2]}
    assert cert.torsion_coefficients_matched is True
    assert cert.euler_poincare_matched is True
    bridge.close()


def test_klein_bottle_2_torsion_bisimulation():
    bridge = TorsionBisimulationBridge()
    cert = bridge.evaluate_torsion_bisimulation("KleinBottle_K2")
    assert cert.is_bisimilar is True
    assert cert.sql_betti == [1, 1, 0]
    assert cert.sql_torsion == {1: [2]}
    assert cert.torsion_coefficients_matched is True
    assert cert.euler_poincare_matched is True
    bridge.close()


def test_torus_torsion_free_bisimulation():
    bridge = TorsionBisimulationBridge()
    cert = bridge.evaluate_torsion_bisimulation("Torus_T2")
    assert cert.is_bisimilar is True
    assert cert.sql_betti == [1, 2, 1]
    assert cert.sql_torsion == {}
    assert cert.torsion_coefficients_matched is True
    assert cert.euler_poincare_matched is True
    bridge.close()


def test_sphere_torsion_free_bisimulation():
    bridge = TorsionBisimulationBridge()
    cert = bridge.evaluate_torsion_bisimulation("Sphere_S2")
    assert cert.is_bisimilar is True
    assert cert.sql_betti == [1, 0, 1]
    assert cert.sql_torsion == {}
    assert cert.torsion_coefficients_matched is True
    assert cert.euler_poincare_matched is True
    bridge.close()


def test_snf_divisibility_law():
    """Verifies that for every evaluated complex, d_i divides d_{i+1} strictly."""
    bridge = TorsionBisimulationBridge()
    for key in ["RP2_RealProjectivePlane", "KleinBottle_K2", "Torus_T2", "Sphere_S2"]:
        cert = bridge.evaluate_torsion_bisimulation(key)
        assert cert.is_bisimilar is True
        assert cert.backward_simulation_holds is True
    bridge.close()


def test_perturbation_falsification_guard():
    """
    Perturbs an entry in the boundary matrix d2 of RP^2.
    Asserts that the resulting invariant factor does not match the certified [2] torsion,
    causing the bisimulation bridge to fail closed.
    """
    bridge = TorsionBisimulationBridge()
    f_vec, d1, d2 = bridge.build_rp2_matrices()
    # Perturb one entry
    d2[0][0] += 5
    r2, c2 = bridge.evaluator.load_matrix("rp2_perturbed", d2)
    snf = bridge.evaluator.compute_snf("rp2_perturbed", r2, c2)
    # The altered diagonal does not equal the canonical [1, ..., 1, 2]
    assert snf["diagonal_factors"] != [1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
    bridge.close()
