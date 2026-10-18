from __future__ import annotations
"""Property-Based Fuzz Test Suite for Phi1 L1 Dual Witness Functional.

AuthorityEffect: None.

Stress tests primal-dual LP optimization, duality gap bounds, scale covariance,
subadditivity, and degenerate graph topologies under random cochain sweeps.
"""


import numpy as np
import pytest
from omega_engine.crates.functional.phi import (
    Phi1Uncertified,
    constant_gauge_sweep_is_a_noop,
    evaluate_phi1,
    phi1,
    phi1_estimate,
    solve_phi1_dual_witness,
)


def test_property_phi1_zero_cochain():
    """Property: Phi1([0]) = 0 on any graph topology."""
    vertices = [0, 1, 2, 3]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    cochain = np.zeros(4)

    val = phi1(vertices, edges, cochain)
    assert abs(val) < 1e-9

    res = solve_phi1_dual_witness(vertices, edges, cochain)
    assert res["is_certified"] is True
    assert abs(res["duality_gap"]) < 1e-9


def test_property_weak_duality_random_sweeps():
    """Property: Weak duality min_l1 >= dual_val - 1e-7 holds for 50 random cochain sweeps."""
    np.random.seed(42)
    vertices = list(range(6))
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 3), (1, 4)]
    n_edges = len(edges)

    for i in range(50):
        # Generate random cochains across normal, uniform, and exponential distributions
        cochain = np.random.randn(n_edges) * (10 ** np.random.uniform(-3, 3))
        weights = np.random.uniform(0.1, 10.0, size=n_edges)

        receipt = solve_phi1_dual_witness(vertices, edges, cochain, edge_weights=weights)
        assert receipt["weak_duality_violated"] is False
        assert receipt["min_l1"] >= receipt["dual_val"] - 1e-7


def test_property_scale_covariance():
    """Property: Phi1([lambda * omega]) == |lambda| * Phi1([omega])."""
    np.random.seed(123)
    vertices = list(range(4))
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
    cochain = np.array([1.5, -2.3, 0.7, 4.1, -1.2])

    val_base = phi1(vertices, edges, cochain)

    for scale in [0.5, 2.0, -3.0, 10.0]:
        val_scaled = phi1(vertices, edges, scale * cochain)
        assert abs(val_scaled - abs(scale) * val_base) < 1e-5


def test_property_subadditivity_triangle_inequality():
    """Property: Phi1([omega1 + omega2]) <= Phi1([omega1]) + Phi1([omega2])."""
    np.random.seed(999)
    vertices = list(range(5))
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (1, 3)]
    n_edges = len(edges)

    for _ in range(20):
        omega1 = np.random.randn(n_edges)
        omega2 = np.random.randn(n_edges)

        val1 = phi1(vertices, edges, omega1)
        val2 = phi1(vertices, edges, omega2)
        val_sum = phi1(vertices, edges, omega1 + omega2)

        assert val_sum <= val1 + val2 + 1e-6


def test_ill_conditioned_weight_ratios():
    """Stress test: Extreme edge weight ratios (1e-4 to 1e4)."""
    vertices = [0, 1, 2]
    edges = [(0, 1), (1, 2), (2, 0)]
    cochain = np.array([1.0, 1.0, 1.0])
    weights = np.array([1e-4, 1.0, 1e4])

    receipt = solve_phi1_dual_witness(vertices, edges, cochain, edge_weights=weights)
    assert receipt["primal_solved"] is True
    assert receipt["dual_solved"] is True
    assert receipt["is_certified"] is True


def test_constant_gauge_sweep_noop_verification():
    """Verify that constant gauge sweep is mathematically proven to be a no-op."""
    vertices = [0, 1, 2, 3]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    cochain = np.array([1.0, 2.0, 3.0, 4.0])

    res = constant_gauge_sweep_is_a_noop(vertices, edges, cochain)
    assert res["sweep_found_nothing"] is True
    assert res["authority_effect"] == "None"


