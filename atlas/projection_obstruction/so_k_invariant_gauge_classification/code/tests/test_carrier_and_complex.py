"""
Unit tests for GraphComplex and Cochain representations.
Paper: GS-002 (so_k_invariant_gauge_classification)
"""

import numpy as np
import pytest

from carrier import GraphComplex, Cochain


def test_cochain_basics_and_operations() -> None:
    data1 = np.array([[1.0, 2.0], [3.0, 4.0]])
    data2 = np.array([[0.5, -1.0], [1.0, 2.0]])
    c1 = Cochain(data1, degree=1)
    c2 = Cochain(data2, degree=1)

    assert c1.num_cells == 2
    assert c1.stalk_dim == 2
    assert c1.shape == (2, 2)

    # Addition and subtraction
    c_add = c1 + c2
    np.testing.assert_allclose(c_add.data, data1 + data2)

    c_sub = c1 - c2
    np.testing.assert_allclose(c_sub.data, data1 - data2)

    # Negation and scalar multiplication
    c_neg = -c1
    np.testing.assert_allclose(c_neg.data, -data1)

    c_scale = 2.5 * c1
    np.testing.assert_allclose(c_scale.data, 2.5 * data1)

    # Shape mismatch error
    c_mismatch = Cochain(np.array([[1.0]]), degree=1)
    with pytest.raises(ValueError, match="Shape mismatch"):
        _ = c1 + c_mismatch
    with pytest.raises(ValueError, match="Shape mismatch"):
        _ = c1 - c_mismatch


def test_cochain_norms() -> None:
    # 1D input conversion to 2D
    c_1d = Cochain([3.0, 4.0])
    assert c_1d.shape == (2, 1)
    assert c_1d.stalk_dim == 1

    # Mixed norm L1(E; L2)
    # Cell 0: (3, 4) -> L2 = 5
    # Cell 1: (1, 1) -> L2 = sqrt(2)
    data = np.array([[3.0, 4.0], [1.0, 1.0]])
    c = Cochain(data)
    assert c.mixed_l1_l2_norm() == pytest.approx(5.0 + np.sqrt(2.0))

    # Weighted mixed norm
    w = np.array([2.0, 3.0])
    assert c.mixed_l1_l2_norm(w) == pytest.approx(2.0 * 5.0 + 3.0 * np.sqrt(2.0))

    # Weight length mismatch
    with pytest.raises(ValueError, match="Weights length"):
        c.mixed_l1_l2_norm(np.array([1.0]))

    # Coordinate L1 norm
    assert c.coordinate_l1_l1_norm() == pytest.approx((3.0 + 4.0) + (1.0 + 1.0))
    assert c.coordinate_l1_l1_norm(w) == pytest.approx(2.0 * 7.0 + 3.0 * 2.0)


def test_graph_complex_validations_and_operators() -> None:
    # Valid cycle graph
    g = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
    assert g.num_vertices == 3
    assert g.num_edges == 3
    assert g.num_faces == 1
    assert g.verify_complex()

    # Invalid weights
    with pytest.raises(ValueError, match="Edge weights must match"):
        GraphComplex(num_vertices=2, edges=[(0, 1)], edge_weights=[1.0, 2.0])
    with pytest.raises(ValueError, match="Edge weights must be strictly positive"):
        GraphComplex(num_vertices=2, edges=[(0, 1)], edge_weights=[0.0])
    with pytest.raises(ValueError, match="Face weights must match"):
        GraphComplex(
            num_vertices=2, edges=[(0, 1)], faces=[[(0, 1)]], face_weights=[1.0, 2.0]
        )
    with pytest.raises(ValueError, match="Face weights must be strictly positive"):
        GraphComplex(
            num_vertices=2, edges=[(0, 1)], faces=[[(0, 1)]], face_weights=[-1.0]
        )

    # Coboundary shape checks
    with pytest.raises(ValueError, match="Alpha shape"):
        g.coboundary_d0(np.zeros((2, 2)))  # Expected 3 vertices
    with pytest.raises(ValueError, match="Omega shape"):
        g.coboundary_d1(Cochain(np.zeros((2, 2))))  # Expected 3 edges
    with pytest.raises(ValueError, match="Phi shape"):
        g.dual_coboundary_d0_star(Cochain(np.zeros((2, 2))))  # Expected 3 edges


def test_theta_graph_construction() -> None:
    theta = GraphComplex.create_theta_graph(stalk_dim=3)
    assert theta.num_vertices == 2
    assert theta.num_edges == 3
    assert theta.num_faces == 2
    assert theta.verify_complex()

    # Exact d1 @ d0 == 0 check
    prod = theta.d1 @ theta.d0
    np.testing.assert_allclose(prod, 0.0)
