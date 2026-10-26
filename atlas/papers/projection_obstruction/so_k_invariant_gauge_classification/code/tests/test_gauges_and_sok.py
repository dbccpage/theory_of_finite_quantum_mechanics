"""
Unit tests for Stalk Gauges and SO(k) Group Invariance Audits.
Paper: GS-002 (so_k_invariant_gauge_classification)
"""

import math
import numpy as np
import pytest

from gauges import (
    EuclideanGauge,
    CoordinateL1Gauge,
    LpGauge,
    AnisotropicGauge,
    make_so2_rotation,
    make_random_sok_rotation,
    make_signed_permutation,
    audit_so_k_invariance,
    audit_sphere_constancy,
)


def test_gauge_instantiation_and_evaluation() -> None:
    v = np.array([3.0, -4.0])

    euc = EuclideanGauge(scale=2.0)
    assert euc(v) == pytest.approx(2.0 * 5.0)

    l1 = CoordinateL1Gauge(scale=1.5)
    assert l1(v) == pytest.approx(1.5 * 7.0)

    lp = LpGauge(p=3.0, scale=1.0)
    expected_lp = (3.0**3 + 4.0**3) ** (1.0 / 3.0)
    assert lp(v) == pytest.approx(expected_lp)

    linf = LpGauge(p=math.inf, scale=1.0)
    assert linf(v) == pytest.approx(4.0)

    # Anisotropic
    a_mat = np.array([[2.0, 0.0], [0.0, 1.0]])
    aniso = AnisotropicGauge(a_mat)
    # A @ [3, -4] = [6, -4], norm = sqrt(36 + 16) = sqrt(52)
    assert aniso(v) == pytest.approx(math.sqrt(52.0))


def test_gauge_exceptions() -> None:
    with pytest.raises(ValueError, match="Scale must be strictly positive"):
        EuclideanGauge(scale=0.0)
    with pytest.raises(ValueError, match="Scale must be strictly positive"):
        CoordinateL1Gauge(scale=-1.0)
    with pytest.raises(ValueError, match="p must be >= 1.0"):
        LpGauge(p=0.5)
    with pytest.raises(ValueError, match="Scale must be strictly positive"):
        LpGauge(p=2.0, scale=0.0)
    with pytest.raises(ValueError, match="Matrix A must be square"):
        AnisotropicGauge(np.zeros((2, 3)))
    with pytest.raises(ValueError, match="Matrix A must have full column rank"):
        AnisotropicGauge(np.zeros((2, 2)))


def test_rotations_and_permutations() -> None:
    # SO(2)
    r = make_so2_rotation(math.pi / 2.0)
    v = np.array([1.0, 0.0])
    rot_v = r @ v
    np.testing.assert_allclose(rot_v, [0.0, 1.0], atol=1e-7)

    # Random SO(k)
    for k in [1, 2, 4]:
        r_k = make_random_sok_rotation(k)
        assert r_k.shape == (k, k)
        # Check orthogonality: R.T @ R == I
        np.testing.assert_allclose(r_k.T @ r_k, np.eye(k), atol=1e-6)
        # Check det == 1
        assert np.linalg.det(r_k) == pytest.approx(1.0, abs=1e-5)

    # Signed permutation
    p_mat = make_signed_permutation(3)
    assert p_mat.shape == (3, 3)
    np.testing.assert_allclose(p_mat.T @ p_mat, np.eye(3), atol=1e-6)


def test_audit_so_k_invariance_and_sphere_constancy() -> None:
    # Euclidean is SO(k)-invariant and sphere-constant
    euc = EuclideanGauge(1.0)
    audit_euc = audit_so_k_invariance(euc, dim=3, num_samples=30)
    assert audit_euc["is_so_k_invariant"]
    assert audit_euc["max_deviation"] < 1e-6

    sphere_euc = audit_sphere_constancy(euc, dim=3, radius=2.5, num_samples=30)
    assert sphere_euc["is_sphere_constant"]
    assert sphere_euc["mean_value"] == pytest.approx(2.5, abs=1e-5)

    # Coordinate L1 fails SO(k) invariance and sphere constancy
    l1 = CoordinateL1Gauge(1.0)
    audit_l1 = audit_so_k_invariance(l1, dim=2, num_samples=30)
    assert not audit_l1["is_so_k_invariant"]
    assert audit_l1["max_deviation"] > 0.1

    sphere_l1 = audit_sphere_constancy(l1, dim=2, radius=1.0, num_samples=30)
    assert not sphere_l1["is_sphere_constant"]
    assert sphere_l1["spread"] > 0.1
