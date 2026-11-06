"""
Unit Test Suite: General k-Simplicial Homology Bisimulation
Lean 4 Kernel Certificates <-> SQL Bareiss Gaussian Elimination CTEs
AuthorityEffect: None.
"""

import sys
from pathlib import Path

code_dir = Path(__file__).resolve().parent.parent / "code"
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from homology_cte_evaluator import HomologyCTEEvaluator
from k_simplex_bisimulation_bridge import KSimplexBisimulationBridge


def test_lean4_k_simplex_formal_compilation():
    bridge = KSimplexBisimulationBridge()
    assert bridge.verify_lean_compilation() is True
    bridge.close()


def test_sql_cte_boundary_nilpotence_all_dimensions():
    evaluator = HomologyCTEEvaluator(in_memory=True)
    # Build Delta^3 (has dim 0, 1, 2, 3)
    for v in ["0", "1", "2", "3"]:
        evaluator.add_simplex(0, v, [v])
    for u, v in [("0", "1"), ("0", "2"), ("0", "3"), ("1", "2"), ("1", "3"), ("2", "3")]:
        evaluator.add_simplex(1, f"{u}-{v}", [u, v])
    for u, v, w in [("0", "1", "2"), ("0", "1", "3"), ("0", "2", "3"), ("1", "2", "3")]:
        evaluator.add_simplex(2, f"{u}-{v}-{w}", [u, v, w])
    evaluator.add_simplex(3, "0-1-2-3", ["0", "1", "2", "3"])
    evaluator.build_boundaries()

    # d_1 ∘ d_2 = 0
    report_d2 = evaluator.verify_nilpotence(2)
    assert report_d2["nilpotence_holds"] is True
    assert report_d2["violations_count"] == 0

    # d_2 ∘ d_3 = 0
    report_d3 = evaluator.verify_nilpotence(3)
    assert report_d3["nilpotence_holds"] is True
    assert report_d3["violations_count"] == 0
    evaluator.close()


def test_sql_bareiss_gaussian_elimination_ranks():
    evaluator = HomologyCTEEvaluator(in_memory=True)
    # Build Delta^3
    for v in ["0", "1", "2", "3"]:
        evaluator.add_simplex(0, v, [v])
    for u, v in [("0", "1"), ("0", "2"), ("0", "3"), ("1", "2"), ("1", "3"), ("2", "3")]:
        evaluator.add_simplex(1, f"{u}-{v}", [u, v])
    for u, v, w in [("0", "1", "2"), ("0", "1", "3"), ("0", "2", "3"), ("1", "2", "3")]:
        evaluator.add_simplex(2, f"{u}-{v}-{w}", [u, v, w])
    evaluator.add_simplex(3, "0-1-2-3", ["0", "1", "2", "3"])
    evaluator.build_boundaries()

    r1 = evaluator.compute_boundary_rank(1)
    r2 = evaluator.compute_boundary_rank(2)
    r3 = evaluator.compute_boundary_rank(3)

    assert r1 == 3
    assert r2 == 3
    assert r3 == 1
    evaluator.close()


def test_s1_circle_homology_bisimulation():
    bridge = KSimplexBisimulationBridge()
    cert = bridge.evaluate_complex_bisimulation("S1_Circle")
    assert cert.is_bisimilar is True
    assert cert.sql_betti == [1, 1]
    assert cert.sql_euler == 0
    assert cert.betti_numbers_matched is True
    assert cert.euler_poincare_matched is True
    bridge.close()


def test_s2_sphere_homology_bisimulation():
    bridge = KSimplexBisimulationBridge()
    cert = bridge.evaluate_complex_bisimulation("S2_Sphere")
    assert cert.is_bisimilar is True
    assert cert.sql_betti == [1, 0, 1]
    assert cert.sql_euler == 2
    assert cert.betti_numbers_matched is True
    assert cert.euler_poincare_matched is True
    bridge.close()


def test_delta3_tetrahedron_homology_bisimulation():
    bridge = KSimplexBisimulationBridge()
    cert = bridge.evaluate_complex_bisimulation("Delta3_Tetrahedron")
    assert cert.is_bisimilar is True
    assert cert.sql_betti == [1, 0, 0, 0]
    assert cert.sql_euler == 1
    assert cert.betti_numbers_matched is True
    assert cert.euler_poincare_matched is True
    bridge.close()


def test_euler_poincare_invariance_property():
    bridge = KSimplexBisimulationBridge()
    for name in ["S1_Circle", "S2_Sphere", "Delta3_Tetrahedron"]:
        cert = bridge.evaluate_complex_bisimulation(name)
        assert cert.euler_poincare_matched is True
        assert cert.lean_euler == cert.sql_euler
    bridge.close()


def test_perturbation_falsification_guard():
    """
    Perturbs an orientation sign in the relational boundary table.
    Asserts that the SQL nilpotence CTE detects the violation and the bridge fails closed.
    """
    bridge = KSimplexBisimulationBridge()
    bridge.load_complex_s2()
    # Invert sign of one face boundary entry
    c = bridge.evaluator.conn.cursor()
    c.execute("""
        UPDATE boundary_entries
        SET weight = 1
        WHERE dim = 2 AND face_id = '0-2' AND simplex_id = '0-1-2';
    """)
    bridge.evaluator.conn.commit()

    nilp_report = bridge.evaluator.verify_nilpotence(2)
    assert nilp_report["nilpotence_holds"] is False
    assert nilp_report["violations_count"] > 0
    bridge.close()
