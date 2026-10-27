"""
Unit and Integration Tests for Exact SOCP Solver and Certifier.
Paper: GS-002 (008_so_k_invariant_gauge_classification)
"""

import math
import numpy as np
import pytest

from carrier import GraphComplex, Cochain
from solver import MixedNormSolver
from socp_certifier import (
    ExactSOCPCertifier,
    SOCPDualityCertificate,
)


def test_exact_socp_certifier_triangle_basic() -> None:
    complex_tri = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
    omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))

    certifier = ExactSOCPCertifier(complex_tri, tol=1e-7)
    cert = certifier.certify(omega)

    assert isinstance(cert, SOCPDualityCertificate)
    assert cert.primal_value == pytest.approx(math.sqrt(2.0), abs=1e-7)
    assert cert.dual_value == pytest.approx(math.sqrt(2.0), abs=1e-7)
    assert cert.duality_gap == pytest.approx(0.0, abs=1e-7)
    assert cert.divergence_norm == pytest.approx(0.0, abs=1e-7)
    assert cert.max_dual_norm_violation == pytest.approx(0.0, abs=1e-7)
    assert cert.is_divergence_free
    assert cert.is_dual_feasible
    assert cert.is_zero_gap
    assert cert.is_optimal
    assert cert.solver_method == "cycle_closed_form"


def test_exact_socp_certifier_weighted_triangle() -> None:
    # Non-uniform weights [2.0, 5.0, 1.5]
    complex_tri = GraphComplex.create_cycle_graph(
        cycle_len=3, stalk_dim=2, edge_weights=[2.0, 5.0, 1.5]
    )
    omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]))
    # S(omega) = (2.0, 2.0), ||S||_2 = 2 * sqrt(2)
    # min_e w_e = 1.5 => exact value = 1.5 * 2 * sqrt(2) = 3 * sqrt(2) ~ 4.242640687

    certifier = ExactSOCPCertifier(complex_tri, tol=1e-7)
    cert = certifier.certify(omega)

    expected = 3.0 * math.sqrt(2.0)
    assert cert.primal_value == pytest.approx(expected, abs=1e-7)
    assert cert.dual_value == pytest.approx(expected, abs=1e-7)
    assert cert.duality_gap < 1e-7
    assert cert.is_optimal


def test_exact_socp_certifier_different_stalk_dims() -> None:
    for k in [1, 2, 3, 5]:
        g = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=k)
        # Uniform 1-vector on edge 0, zero elsewhere
        data = np.zeros((3, k))
        data[0, :] = 1.0
        omega = Cochain(data)

        certifier = ExactSOCPCertifier(g, tol=1e-7)
        cert = certifier.certify(omega)

        expected = math.sqrt(float(k))
        assert cert.primal_value == pytest.approx(expected, abs=1e-7)
        assert cert.dual_value == pytest.approx(expected, abs=1e-7)
        assert cert.duality_gap < 1e-7
        assert cert.is_optimal


def test_exact_socp_vs_fallback_lbfgs() -> None:
    complex_tri = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
    omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))

    solver = MixedNormSolver(complex_tri)
    cert_exact = solver.solve(omega, exact=True)
    cert_approx = solver.solve(omega, exact=False)

    assert cert_exact.primal_value == pytest.approx(math.sqrt(2.0), abs=1e-7)
    assert cert_approx.primal_value == pytest.approx(math.sqrt(2.0), abs=1e-3)
    assert cert_exact.duality_gap < 1e-7
    assert cert_approx.duality_gap < 1e-3


def test_exact_socp_tree_graph_no_cycles() -> None:
    # Tree graph: 3 vertices, 2 edges: (0, 1), (1, 2)
    tree = GraphComplex(
        num_vertices=3, edges=[(0, 1), (1, 2)], stalk_dim=2, edge_weights=[1.0, 2.0]
    )
    omega = Cochain(np.array([[1.0, 2.0], [-0.5, 1.5]]))

    certifier = ExactSOCPCertifier(tree, tol=1e-7)
    cert = certifier.certify(omega)

    # Any cochain on a tree is an exact coboundary => quotient is 0.0
    assert cert.primal_value == pytest.approx(0.0, abs=1e-7)
    assert cert.dual_value == pytest.approx(0.0, abs=1e-7)
    assert cert.duality_gap == pytest.approx(0.0, abs=1e-7)
    assert cert.is_optimal


def test_exact_socp_multicomponent_graph() -> None:
    # Two disjoint triangles: vertices 0..2 and 3..5
    edges = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]
    faces = [[(0, 1), (1, 1), (2, 1)], [(3, 1), (4, 1), (5, 1)]]
    g = GraphComplex(
        num_vertices=6, edges=edges, faces=faces, stalk_dim=2, edge_weights=[1.0] * 6
    )
    # Circulation (1, 1) on first triangle, (2, 0) on second triangle
    data = np.zeros((6, 2))
    data[0] = [1.0, 0.0]
    data[1] = [0.0, 1.0]
    data[3] = [2.0, 0.0]
    omega = Cochain(data)

    certifier = ExactSOCPCertifier(g, tol=1e-7)
    cert = certifier.certify(omega)

    # Disjoint sum of quotient obstructions: sqrt(2) + 2.0 ~ 3.41421356
    expected = math.sqrt(2.0) + 2.0
    assert cert.primal_value == pytest.approx(expected, abs=1e-6)
    assert cert.dual_value == pytest.approx(expected, abs=1e-6)
    assert cert.duality_gap < 1e-6
    assert cert.is_optimal


def test_exact_socp_shape_validation() -> None:
    g = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
    certifier = ExactSOCPCertifier(g)

    with pytest.raises(ValueError, match="does not match complex"):
        certifier.certify(Cochain(np.zeros((4, 2))))
    with pytest.raises(ValueError, match="does not match complex"):
        certifier.certify(Cochain(np.zeros((3, 3))))


def test_carrier_dual_coboundary_and_orientations_validation() -> None:
    g = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
    phi = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
    div = g.dual_coboundary_d0_star(phi)
    assert div.shape == (3, 2)
    with pytest.raises(ValueError, match="must be"):
        g.dual_coboundary_d0_star(Cochain(np.zeros((4, 2))))
    with pytest.raises(ValueError, match="Orientations length"):
        GraphComplex.create_cycle_graph(cycle_len=3, orientations=[1, 1])
    with pytest.raises(ValueError, match="Orientation sign must be"):
        GraphComplex.create_cycle_graph(cycle_len=3, orientations=[1, 0, 1])


def test_socp_cycle_without_face_and_zero_circ() -> None:
    # Cycle without face: with_face=False
    g_noface = GraphComplex.create_cycle_graph(
        cycle_len=3, stalk_dim=2, with_face=False
    )
    omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))
    cert = ExactSOCPCertifier(g_noface).certify(omega)
    assert cert.is_optimal
    assert cert.primal_value == pytest.approx(math.sqrt(2.0), abs=1e-7)

    # Simple cycle with zero circulation -> routes to _solve_zero_circulation
    exact_omega = Cochain(np.zeros((3, 2)))
    cert_zero = ExactSOCPCertifier(g_noface).certify(exact_omega)
    assert cert_zero.primal_value == pytest.approx(0.0, abs=1e-7)
    assert cert_zero.is_optimal

    # Invalid orientation length in certify
    with pytest.raises(ValueError, match="Orientations length must match"):
        ExactSOCPCertifier(g_noface).certify(omega, orientations=[1, 1])


def test_non_simple_cycles_detection() -> None:
    # Graph with m == n == 4, but degrees not all 2
    edges = [(0, 1), (0, 2), (0, 3), (1, 2)]
    g_deg = GraphComplex(num_vertices=4, edges=edges, stalk_dim=2)
    omega = Cochain(np.ones((4, 2)))
    cert = ExactSOCPCertifier(g_deg).certify(omega)
    assert cert.is_optimal
    assert cert.solver_method == "numerical_socp_subspace"

    # Graph with m == n == 4, but disconnected (two 2-cycles)
    edges_disconn = [(0, 1), (1, 0), (2, 3), (3, 2)]
    g_disconn = GraphComplex(num_vertices=4, edges=edges_disconn, stalk_dim=2)
    cert_disconn = ExactSOCPCertifier(g_disconn).certify(Cochain(np.ones((4, 2))))
    assert cert_disconn.is_optimal
    assert cert_disconn.solver_method == "numerical_socp_subspace"


def test_fallback_lbfgs_zero_residual_and_scaling() -> None:
    # Fallback solve(exact=False) with zero residual edge and scaling trigger
    g = GraphComplex.create_cycle_graph(
        cycle_len=3, stalk_dim=2, edge_weights=[1.0, 2.0, 3.0]
    )
    omega = Cochain(np.array([[1.0, 0.0], [0.0, 0.0], [0.0, 0.0]]))
    solver = MixedNormSolver(g)
    cert = solver.solve(omega, exact=False)
    assert cert.is_divergence_free
    assert cert.is_dual_feasible
