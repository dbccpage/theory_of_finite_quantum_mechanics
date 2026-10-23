"""
Unit tests for Primal-Dual Duality and Quotient Solvers.
Paper: GS-002 (008_so_k_invariant_gauge_classification)
"""

import math
import numpy as np
import pytest

from carrier import GraphComplex, Cochain
from solver import MixedNormSolver, CoordinateL1Solver


def test_triangle_primal_dual_duality() -> None:
    complex_tri = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
    omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))

    solver = MixedNormSolver(complex_tri)
    cert = solver.solve(omega)

    # Primal value should be sqrt(2) ~ 1.41421356
    assert cert.primal_value == pytest.approx(math.sqrt(2.0), abs=1e-4)
    # Dual value should match primal
    assert cert.dual_value == pytest.approx(math.sqrt(2.0), abs=1e-4)
    assert cert.duality_gap == pytest.approx(0.0, abs=1e-4)

    assert cert.is_divergence_free
    assert cert.is_dual_feasible
    assert cert.is_optimal


def test_exact_repair_cochain() -> None:
    # A cochain in im(d0) must have quotient obstruction 0.0
    complex_tri = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
    alpha = np.array([[1.0, 2.0], [-1.0, 0.5], [3.0, -1.0]])
    exact_omega = complex_tri.coboundary_d0(alpha)

    solver = MixedNormSolver(complex_tri)
    cert = solver.solve(exact_omega)

    assert cert.primal_value == pytest.approx(0.0, abs=1e-5)
    assert cert.duality_gap == pytest.approx(0.0, abs=1e-5)
    assert cert.is_divergence_free


def test_weighted_primal_dual() -> None:
    # With edge weights [1.0, 2.0, 3.0], minimal weight is 1.0
    complex_tri = GraphComplex.create_cycle_graph(
        cycle_len=3, stalk_dim=2, edge_weights=[1.0, 2.0, 3.0]
    )
    omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))

    solver = MixedNormSolver(complex_tri)
    cert = solver.solve(omega)

    assert cert.primal_value == pytest.approx(1.0 * math.sqrt(2.0), abs=1e-4)
    assert cert.duality_gap == pytest.approx(0.0, abs=1e-4)
    assert cert.is_optimal


def test_theta_graph_multi_cycle_duality() -> None:
    # Theta graph: 2 vertices, 3 parallel edges
    theta = GraphComplex.create_theta_graph(stalk_dim=2)
    # Edge 0 has (1, 0), Edge 1 has (0, 1), Edge 2 has (0, 0)
    omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))

    solver = MixedNormSolver(theta)
    cert = solver.solve(omega)

    assert cert.is_divergence_free
    assert cert.is_dual_feasible
    assert cert.duality_gap < 1e-4


def test_coordinate_l1_solver_and_mismatch_error() -> None:
    complex_tri = GraphComplex.create_cycle_graph(cycle_len=3, stalk_dim=2)
    omega = Cochain(np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]]))

    l1_solver = CoordinateL1Solver(complex_tri)
    l1_res = l1_solver.solve(omega)

    # Coordinate L1 on triangle gives 2.0
    assert l1_res["primal_value"] == pytest.approx(2.0, abs=1e-5)
    assert l1_res["is_optimal"]

    # Test shape mismatch in MixedNormSolver
    mismatch_omega = Cochain(np.zeros((2, 2)))
    mixed_solver = MixedNormSolver(complex_tri)
    with pytest.raises(ValueError, match="does not match complex"):
        mixed_solver.solve(mismatch_omega)
