"""T01-T05: Convex body duality and unit ball scaling tests for GS-001.

Verifies Minkowski functional round trips, exact unit ball scaling B_j = c^{-1} B_2^k,
exact induced norms, and anisotropic rotation counterexamples.
"""

import sys
from pathlib import Path
import numpy as np
import pytest

_pkg = Path(__file__).resolve().parents[1]
if str(_pkg / "code") not in sys.path:
    sys.path.insert(0, str(_pkg / "code"))

from norms import (
    l1,
    l2,
    linf,
    anisotropic_gauge,
    exact_induced_operator_norm,
    sample_lower_bound_induced_norm,
)
from convex import (
    minkowski_functional,
    unit_ball_scaling,
    polytope_unit_ball_membership,
)


def test_t01_minkowski_round_trip():
    """T01: Minkowski functional round trip j_B_j(x) = j(x) for l1, l2, linf, and anisotropic norms."""
    x = np.array([3.0, -4.0])

    # l2 norm round trip
    j_l2 = minkowski_functional(x, lambda v: l2(v) <= 1.0)
    assert np.isclose(j_l2, 5.0, atol=1e-5)

    # l1 norm round trip
    j_l1 = minkowski_functional(x, lambda v: l1(v) <= 1.0)
    assert np.isclose(j_l1, 7.0, atol=1e-5)

    # linf norm round trip
    j_linf = minkowski_functional(x, lambda v: linf(v) <= 1.0)
    assert np.isclose(j_linf, 4.0, atol=1e-5)

    # Anisotropic norm round trip
    j_anis = minkowski_functional(x, lambda v: anisotropic_gauge(v, (1.0, 2.0)) <= 1.0)
    assert np.isclose(j_anis, 11.0, atol=1e-5)


def test_t02_unit_ball_scaling():
    """T02: Verify correct unit ball scaling B_j = c^{-1} B_2^k for j(x) = c ||x||_2."""
    c = 2.5
    dim = 3
    res = unit_ball_scaling(c, dim)

    assert res["radius_of_unit_ball"] == 0.4
    assert np.isclose(res["volume_scaling_factor"], 0.4**3)

    with pytest.raises(ValueError, match="strictly positive"):
        unit_ball_scaling(-1.0, dim)


def test_t03_exact_induced_operator_norms():
    """T03: Test exact induced operator norms ||T||_{domain -> codomain}."""
    T = np.array([[1.0, -2.0], [3.0, 4.0]])

    # l1 -> l1: max column sum = max(1+3, 2+4) = 6.0
    assert exact_induced_operator_norm(T, "l1", "l1") == 6.0

    # linf -> linf: max row sum = max(1+2, 3+4) = 7.0
    assert exact_induced_operator_norm(T, "linf", "linf") == 7.0

    # l2 -> l2: spectral norm
    val_l2 = exact_induced_operator_norm(T, "l2", "l2")
    assert np.isclose(val_l2, np.linalg.norm(T, 2))

    # l1 -> linf: max absolute entry = 4.0
    assert exact_induced_operator_norm(T, "l1", "linf") == 4.0

    # linf -> l1: exact vertex evaluation
    val_inf_1 = exact_induced_operator_norm(T, "linf", "l1")
    assert val_inf_1 >= 7.0

    with pytest.raises(ValueError, match="Unsupported norm pair"):
        exact_induced_operator_norm(T, "l2", "linf")


def test_t04_anisotropic_45_degree_rotation_counterexample():
    """T04: Anisotropic 45-degree Euclidean rotation counterexample.

    Demonstrates that Euclidean orthogonal matrices are NOT norm 1 for anisotropic gauges!
    For a(x) = |x1| + 2|x2| and 45-degree rotation R, e1 gives a(Re1)/a(e1) = 3 / sqrt(2) = 2.1213.
    """
    R = np.array(
        [
            [1.0 / np.sqrt(2.0), -1.0 / np.sqrt(2.0)],
            [1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)],
        ]
    )
    e1 = np.array([1.0, 0.0])

    val_e1 = anisotropic_gauge(e1, (1.0, 2.0))
    val_Re1 = anisotropic_gauge(R @ e1, (1.0, 2.0))
    ratio = val_Re1 / val_e1

    # Ratio is 3 / sqrt(2) = 2.1213203435596426
    assert np.isclose(ratio, 3.0 / np.sqrt(2.0))

    # Sample lower bound reflects ratio > 2.0
    lb, _ = sample_lower_bound_induced_norm(
        R, lambda v: anisotropic_gauge(v, (1.0, 2.0)), n_samples=100
    )
    assert lb > 2.0


def test_t05_polytope_unit_ball_membership():
    """T05: Test polytope unit ball membership predicate."""
    x_in = np.array([0.5, 0.2])
    x_out = np.array([2.0, 2.0])

    assert polytope_unit_ball_membership(x_in, l1)
    assert not polytope_unit_ball_membership(x_out, l1)


def test_probe_minkowski_boundary_normalization_and_discontinuity():
    """Verify boundary normalization and detection of discontinuity in Minkowski probe."""
    from convex import probe_minkowski_boundary_continuity

    # 1. Non-unit boundary vector is automatically normalized (covers line 87)
    non_unit_vec = np.array([2.0, 0.0])  # l2 norm is 2.0
    res = probe_minkowski_boundary_continuity(l2, non_unit_vec, epsilons=(1e-6,), tol=1e-5)
    assert res["continuous"] is True
    assert np.isclose(res["base_val"], 1.0, atol=1e-4)

    # 2. Strict tol tighter than numerical precision triggers continuous = False (covers line 114)
    res_tight = probe_minkowski_boundary_continuity(
        l2, np.array([1.0, 0.0]), epsilons=(1e-6,), tol=1e-15
    )
    assert res_tight["continuous"] is False

