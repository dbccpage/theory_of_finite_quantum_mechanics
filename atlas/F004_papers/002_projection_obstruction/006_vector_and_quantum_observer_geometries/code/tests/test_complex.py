"""
Tests for cochain complexes and graph complexes.
Paper: GS-003 (006_vector_and_quantum_observer_geometries)
AuthorityEffect: None.
"""

import pytest
import numpy as np

from cochain_complex import Cochain, GraphComplex
import complex as complex_alias
from exceptions import DimensionMismatchError


def test_complex_module_alias():
    assert complex_alias.Cochain is Cochain
    assert complex_alias.GraphComplex is GraphComplex


def test_cochain_basics_vector():
    data = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    c = Cochain(data, degree=1)
    assert c.degree == 1
    assert c.num_cells == 3
    assert c.stalk_dim == 2
    assert not c.is_operator
    assert len(c) == 3
    np.testing.assert_array_equal(c[0], [1.0, 2.0])

    # 1D array reshapes to (n, 1)
    c1d = Cochain([1.0, 2.0, 3.0])
    assert c1d.shape == (3, 1)
    assert c1d.stalk_dim == 1


def test_cochain_arithmetic():
    c1 = Cochain([[1.0, 0.0], [0.0, 1.0]], degree=1)
    c2 = Cochain([[0.5, 0.5], [1.0, -1.0]], degree=1)

    c_sum = c1 + c2
    np.testing.assert_allclose(c_sum.data, [[1.5, 0.5], [1.0, 0.0]])

    c_diff = c1 - c2
    np.testing.assert_allclose(c_diff.data, [[0.5, -0.5], [-1.0, 2.0]])

    c_neg = -c1
    np.testing.assert_allclose(c_neg.data, [[-1.0, 0.0], [0.0, -1.0]])

    c_mul = c1 * 3.0
    np.testing.assert_allclose(c_mul.data, [[3.0, 0.0], [0.0, 3.0]])

    c_rmul = 2.0 * c1
    np.testing.assert_allclose(c_rmul.data, [[2.0, 0.0], [0.0, 2.0]])


def test_cochain_arithmetic_errors():
    c1 = Cochain([[1.0, 0.0]], degree=1)
    c2 = Cochain([[1.0, 0.0], [0.0, 1.0]], degree=1)
    c3 = Cochain([[1.0, 0.0]], degree=0)

    with pytest.raises(DimensionMismatchError):
        _ = c1 + c2

    with pytest.raises(DimensionMismatchError):
        _ = c1 - c3

    with pytest.raises(TypeError):
        _ = c1 + 5.0

    with pytest.raises(TypeError):
        _ = c1 - 5.0


def test_cochain_mixed_norms():
    data = np.array([[3.0, 4.0], [1.0, -1.0]])
    c = Cochain(data)

    # L2 norm: sqrt(3^2+4^2) = 5, sqrt(1^2+1^2) = sqrt(2)
    assert abs(c.mixed_norm(p=2) - (5.0 + np.sqrt(2.0))) < 1e-12

    # L1 norm: |3|+|4| = 7, |1|+|-1| = 2 => 9
    assert abs(c.mixed_norm(p=1) - 9.0) < 1e-12

    # Linf norm: max(|3|,|4|) = 4, max(|1|,|-1|) = 1 => 5
    assert abs(c.mixed_norm(p=np.inf) - 5.0) < 1e-12
    assert abs(c.mixed_norm(p="inf") - 5.0) < 1e-12

    # Weighted norm
    weights = [2.0, 3.0]
    expected_w = 2.0 * 5.0 + 3.0 * np.sqrt(2.0)
    assert abs(c.mixed_norm(p=2, weights=weights) - expected_w) < 1e-12

    # Weight length mismatch
    with pytest.raises(DimensionMismatchError):
        c.mixed_norm(p=2, weights=[1.0])

    # General p=3
    norm_p3 = c.mixed_norm(p=3)
    exp_p3 = (3.0**3 + 4.0**3) ** (1 / 3) + (1.0 + 1.0) ** (1 / 3)
    assert abs(norm_p3 - exp_p3) < 1e-12


def test_cochain_operator_norms():
    sz = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    op_data = np.array([sz, 2.0 * sz])
    c_op = Cochain(op_data, degree=1)
    assert c_op.is_operator
    assert c_op.stalk_dim == 2

    # Trace distance gauge J_Q(delta) = 0.5 * ||delta_e||_1
    # ||sz||_1 = 2 => 0.5 * 2 = 1.0
    # ||2*sz||_1 = 4 => 0.5 * 4 = 2.0
    assert abs(c_op.trace_norm() - 3.0) < 1e-12

    # Weighted
    assert abs(c_op.trace_norm(weights=[2.0, 1.0]) - 4.0) < 1e-12

    with pytest.raises(DimensionMismatchError):
        c_op.trace_norm(weights=[1.0])

    # Calling mixed_norm on operator raises ValueError
    with pytest.raises(ValueError):
        c_op.mixed_norm()

    # Calling trace_norm on vector raises ValueError
    c_vec = Cochain([[1.0, 2.0]])
    with pytest.raises(ValueError):
        c_vec.trace_norm()


def test_graph_complex_validation():
    # Invalid vertex
    with pytest.raises(ValueError):
        GraphComplex(num_vertices=2, edges=[(0, 2)])

    with pytest.raises(ValueError):
        GraphComplex(num_vertices=2, edges=[(-1, 0)])

    # Invalid weights
    with pytest.raises(DimensionMismatchError):
        GraphComplex(num_vertices=2, edges=[(0, 1)], edge_weights=[1.0, 2.0])

    with pytest.raises(ValueError):
        GraphComplex(num_vertices=2, edges=[(0, 1)], edge_weights=[-1.0])

    with pytest.raises(ValueError):
        GraphComplex(num_vertices=2, edges=[(0, 1)], edge_weights=[0.0])

    # Invalid face edge
    with pytest.raises(ValueError):
        GraphComplex(num_vertices=2, edges=[(0, 1)], faces=[[(5, 1)]])


def test_graph_complex_boundary_and_laplacians():
    comp = GraphComplex.triangle_complex()
    assert comp.num_vertices == 3
    assert comp.num_edges == 3
    assert comp.num_faces == 1
    assert comp.verify_boundary_property()

    # Laplacian 0: d0^T d0
    l0 = comp.laplacian_0()
    assert l0.shape == (3, 3)
    # Check nullspace of L0 contains constant vector [1, 1, 1]
    np.testing.assert_allclose(
        l0 @ np.array([1.0, 1.0, 1.0]), [0.0, 0.0, 0.0], atol=1e-12
    )

    # Laplacian 1: d0 d0^T + d1^T d1
    l1 = comp.laplacian_1()
    assert l1.shape == (3, 3)

    # Complex without faces
    comp_nofaces = GraphComplex(num_vertices=3, edges=[(0, 1), (1, 2)])
    assert comp_nofaces.verify_boundary_property()
    l1_nofaces = comp_nofaces.laplacian_1()
    assert l1_nofaces.shape == (2, 2)


def test_graph_complex_cochain_maps():
    comp = GraphComplex.triangle_complex()

    # Vector cochain C^0 -> C^1 -> C^2
    phi_vec = Cochain([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], degree=0)
    d0_phi = comp.d0(phi_vec)
    assert d0_phi.degree == 1
    assert d0_phi.shape == (3, 2)
    # Edge (0, 1): phi(1) - phi(0) = (2, 2)
    np.testing.assert_allclose(d0_phi[0], [2.0, 2.0])
    # Edge (1, 2): phi(2) - phi(1) = (2, 2)
    np.testing.assert_allclose(d0_phi[1], [2.0, 2.0])
    # Edge (2, 0): phi(0) - phi(2) = (-4, -4)
    np.testing.assert_allclose(d0_phi[2], [-4.0, -4.0])

    # d1 d0 = 0
    d1_d0_phi = comp.d1(d0_phi)
    assert d1_d0_phi.degree == 2
    np.testing.assert_allclose(d1_d0_phi[0], [0.0, 0.0], atol=1e-12)

    # Operator cochain
    sz = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    phi_op = Cochain(np.array([sz, 2.0 * sz, 3.0 * sz]), degree=0)
    d0_phi_op = comp.d0(phi_op)
    assert d0_phi_op.is_operator
    np.testing.assert_allclose(d0_phi_op[0], sz)

    d1_d0_phi_op = comp.d1(d0_phi_op)
    np.testing.assert_allclose(d1_d0_phi_op[0], np.zeros((2, 2)), atol=1e-12)

    # Adjoint divergence d0^*
    div_vec = comp.d0_adjoint(d0_phi)
    assert div_vec.degree == 0
    assert div_vec.shape == (3, 2)

    div_op = comp.d0_adjoint(d0_phi_op)
    assert div_op.degree == 0
    assert div_op.is_operator


def test_graph_complex_map_errors():
    comp = GraphComplex.triangle_complex()
    c_bad_deg = Cochain([[1.0], [2.0], [3.0]], degree=1)
    with pytest.raises(DimensionMismatchError):
        comp.d0(c_bad_deg)

    c_bad_cells = Cochain([[1.0], [2.0]], degree=0)
    with pytest.raises(DimensionMismatchError):
        comp.d0(c_bad_cells)

    c1_bad_deg = Cochain([[1.0], [2.0], [3.0]], degree=0)
    with pytest.raises(DimensionMismatchError):
        comp.d1(c1_bad_deg)

    c1_bad_cells = Cochain([[1.0], [2.0]], degree=1)
    with pytest.raises(DimensionMismatchError):
        comp.d1(c1_bad_cells)

    with pytest.raises(DimensionMismatchError):
        comp.d0_adjoint(c1_bad_deg)

    comp_nofaces = GraphComplex(num_vertices=2, edges=[(0, 1)])
    c_edge = Cochain([[1.0]], degree=1)
    with pytest.raises(ValueError):
        comp_nofaces.d1(c_edge)
