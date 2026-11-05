"""
Unit tests for Triangle Separation and Analytical Cycle Analytics.
Paper: GS-002 (so_k_invariant_gauge_classification)
"""

import math
import numpy as np
import pytest

from carrier import GraphComplex, Cochain
from gauges import EuclideanGauge
from cycle_analytics import (
    compute_cycle_circulation,
    single_cycle_quotient_analytical,
    analyze_triangle_separation,
    analyze_dimension_scaling,
)
from solver import MixedNormSolver


def test_triangle_separation_metrics() -> None:
    sep = analyze_triangle_separation()
    assert sep["phi_11_coordinate_l1"] == pytest.approx(2.0)
    assert sep["phi_21_euclidean_so2"] == pytest.approx(math.sqrt(2.0))
    assert sep["ratio"] == pytest.approx(math.sqrt(2.0))
    assert sep["squared_ratio"] == pytest.approx(2.0)
    assert sep["is_separated"]

    # Weighted separation
    sep_weighted = analyze_triangle_separation(edge_weights=[3.0, 4.0, 5.0])
    assert sep_weighted["w_min"] == 3.0
    assert sep_weighted["phi_11_coordinate_l1"] == pytest.approx(3.0 * 2.0)
    assert sep_weighted["phi_21_euclidean_so2"] == pytest.approx(3.0 * math.sqrt(2.0))


def test_single_cycle_analytical_vs_solver() -> None:
    # 4-cycle graph
    g4 = GraphComplex.create_cycle_graph(cycle_len=4, stalk_dim=2)
    # Omega: (1, 1) on edge 0, (2, 0) on edge 1, (0, -1) on edge 2, (1, 2) on edge 3
    # Total sum: (1+2+0+1, 1+0-1+2) = (4, 2)
    w_data = np.array([[1.0, 1.0], [2.0, 0.0], [0.0, -1.0], [1.0, 2.0]])
    omega = Cochain(w_data)

    circ = compute_cycle_circulation(omega)
    np.testing.assert_allclose(circ, [4.0, 2.0])

    euc = EuclideanGauge(1.0)
    phi_analytical = single_cycle_quotient_analytical(omega, euc)
    expected_phi = math.sqrt(4.0**2 + 2.0**2)
    assert phi_analytical == pytest.approx(expected_phi)

    # Compare with numerical solver
    solver = MixedNormSolver(g4)
    cert = solver.solve(omega)
    assert cert.primal_value == pytest.approx(expected_phi, abs=1e-4)

    # Weighted analytical evaluation
    phi_weighted = single_cycle_quotient_analytical(
        omega, euc, edge_weights=np.array([2.0, 3.0, 4.0, 5.0])
    )
    assert phi_weighted == pytest.approx(2.0 * expected_phi)


def test_dimension_scaling_and_discrepancy() -> None:
    dims = [2, 4, 9, 16]
    scaling = analyze_dimension_scaling(dims)

    for item in scaling:
        k = item["dimension_k"]
        expected_ratio = math.sqrt(k)
        assert item["phi_11"] == pytest.approx(float(k))
        assert item["phi_21"] == pytest.approx(math.sqrt(k))
        assert item["discrepancy_ratio"] == pytest.approx(expected_ratio)
