"""
Unit tests for 2-Cell Mixed Closure Bound and Operator Norm Engine.
Paper: GS-002 (008_so_k_invariant_gauge_classification)
"""

import numpy as np
import pytest

from carrier import GraphComplex, Cochain
from closure import ClosureBoundEvaluator


def test_triangle_closure_bound_evaluation() -> None:
    # Triangle complex with 1 face bounded by all 3 edges
    g = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
    evaluator = ClosureBoundEvaluator(g)

    # In single triangle cycle, each edge belongs to 1 face with weight 1.0 => op norm is 1.0
    op_norm = evaluator.compute_operator_norm()
    assert op_norm == pytest.approx(1.0)

    # Defect cochain
    omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
    res = evaluator.evaluate(omega)

    # Gamma = ||d1 omega||_2 = ||(1,0) + (0,1) + (0,0)||_2 = ||(1,1)||_2 = sqrt(2)
    # Phi = sqrt(2)
    # Gamma <= op_norm * Phi is satisfied exactly with equality!
    assert res.is_bound_satisfied
    assert res.gamma_closure_defect == pytest.approx(np.sqrt(2.0), abs=1e-4)
    assert res.phi_quotient_obstruction == pytest.approx(np.sqrt(2.0), abs=1e-4)
    assert res.closure_ratio == pytest.approx(1.0, abs=1e-4)
    assert not res.is_exact_repair


def test_theta_graph_closure_bound() -> None:
    theta = GraphComplex.create_theta_graph(stalk_dim=2)
    evaluator = ClosureBoundEvaluator(theta)

    # In theta graph:
    # Edges 0 and 2 belong to 1 face, Edge 1 belongs to both faces f0 and f1!
    # For Edge 1, sum_f u_f |(d1)_{f,1}| = 1 + 1 = 2!
    # Operator norm should be 2.0!
    op_norm = evaluator.compute_operator_norm()
    assert op_norm == pytest.approx(2.0)

    # Test sharp achiever
    achiever = evaluator.construct_sharp_achiever()
    # Edge 1 should have the mass
    assert np.linalg.norm(achiever.data[1]) == pytest.approx(1.0)

    res = evaluator.evaluate(achiever)
    assert res.is_bound_satisfied


def test_exact_repair_zero_closure() -> None:
    g = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
    evaluator = ClosureBoundEvaluator(g)

    # Exact repair h = d0 alpha
    alpha = np.array([[1.0, -1.0], [2.0, 3.0], [0.0, 1.0]])
    exact_h = g.coboundary_d0(alpha)

    res = evaluator.evaluate(exact_h)
    assert res.is_bound_satisfied
    assert res.is_exact_repair
    assert res.gamma_closure_defect == pytest.approx(0.0, abs=1e-5)
    assert res.phi_quotient_obstruction == pytest.approx(0.0, abs=1e-5)
    assert res.closure_ratio is None


def test_closure_exceptions() -> None:
    # Invalid complex where d1 @ d0 != 0
    # Let edges be 0->1, 1->0, face has sign +1 on edge 0 and +1 on edge 1 (not a closed boundary)
    edges = [(0, 1), (1, 0)]
    # Make d1 d0 != 0 explicitly: face has only edge 0
    faces_bad = [[(0, 1)]]
    bad_complex = GraphComplex(num_vertices=2, edges=edges, faces=faces_bad)
    with pytest.raises(ValueError, match="not a valid chain complex"):
        ClosureBoundEvaluator(bad_complex)

    # Empty faces
    no_faces = GraphComplex(num_vertices=2, edges=[(0, 1)], faces=[])
    eval_no_faces = ClosureBoundEvaluator(no_faces)
    assert eval_no_faces.compute_operator_norm() == 0.0
    empty_achiever = eval_no_faces.construct_sharp_achiever()
    assert np.all(empty_achiever.data == 0.0)

    # Shape mismatch on evaluate
    g = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
    evaluator = ClosureBoundEvaluator(g)
    with pytest.raises(ValueError, match="does not match complex edges"):
        evaluator.evaluate(Cochain(np.zeros((2, 2))))
