"""Comprehensive Unit Tests for coordinate_wise_additivity core theorems, axioms, and counterexamples."""

from fractions import Fraction

import numpy as np
import pytest
from coord_additivity import (
    EdgeOrbitDiagnostic,
    anisotropic_l1,
    ce1_l2_fails_additivity,
    ce2_anisotropic_fails_symmetry,
    ce3_max_fails_additivity,
    ce4_orbit_weights_do_not_collapse,
    ce5_lp_power_fails_homogeneity,
    coord_l1,
    coord_l1_exact,
    coord_l2,
    coord_linf,
    decompose_additive_basis,
    decompose_additive_basis_exact,
    is_absolutely_homogeneous,
    is_coord_permutation_symmetric,
    is_disjoint_coord_additive,
    is_disjoint_coord_additive_exact,
    theorem1_holds,
    theorem1_predict,
    theorem1_weight,
    uniform_collapse,
)


def test_coord_l1_and_homogeneity():
    """Verify coordinate l1, absolute homogeneity, and basis decomposition."""
    v = np.array([3.0, -4.0])
    assert coord_l1(v) == 7.0
    assert coord_l1(v, weight=2.0) == 14.0
    assert coord_l2(v) == 5.0
    assert coord_linf(v) == 4.0

    # Absolute homogeneity for coord_l1
    assert is_absolutely_homogeneous(coord_l1, v, [-2.0, -1.0, 0.5, 3.0])

    # Absolute homogeneity failure for quadratic function
    assert not is_absolutely_homogeneous(lambda x: float(np.sum(x**2)), v, [2.0])

    # Basis decomposition
    weights = decompose_additive_basis(coord_l1, 2)
    assert weights == [1.0, 1.0]


def test_exact_rational_computations():
    """Verify exact rational arithmetic representations."""
    x = [Fraction(3, 2), Fraction(-4, 3)]
    res = coord_l1_exact(x, weight=Fraction(2, 1))
    assert res == Fraction(17, 3)

    weights_exact = decompose_additive_basis_exact(lambda v: coord_l1_exact(v, Fraction(3, 1)), 3)
    assert weights_exact == [Fraction(3, 1), Fraction(3, 1), Fraction(3, 1)]

    # Exact disjoint additivity
    coeffs = [Fraction(1, 2), Fraction(-3, 4), Fraction(5, 6)]
    assert is_disjoint_coord_additive_exact(coord_l1_exact, coeffs)


def test_anisotropic_l1():
    """Verify anisotropic l1 calculation and dimension mismatch validation."""
    v = np.array([3.0, 4.0])
    assert anisotropic_l1(v) == 11.0

    with pytest.raises(ValueError, match="dimension mismatch"):
        anisotropic_l1(np.array([1.0, 2.0, 3.0]), a=(1.0, 2.0))


def test_permutation_symmetry():
    """Verify symmetry check distinguishes isotropic vs anisotropic norms and enforces k<=4."""
    v = np.array([3.0, 4.0])
    assert is_coord_permutation_symmetric(coord_l1, v)
    assert is_coord_permutation_symmetric(coord_l2, v)

    # Anisotropic L1 is not symmetric when coordinates are swapped
    assert not is_coord_permutation_symmetric(anisotropic_l1, v)

    # Dimension > 4 error raise
    with pytest.raises(ValueError, match=r"only k<=4 supported"):
        is_coord_permutation_symmetric(coord_l1, np.ones(5))


def test_disjoint_coord_additivity():
    """Verify H3 disjoint coordinate additivity check."""
    assert is_disjoint_coord_additive(coord_l1, k=3)
    assert is_disjoint_coord_additive(anisotropic_l1, k=2)
    assert not is_disjoint_coord_additive(coord_l2, k=2)


def test_theorem1_and_predictions():
    """Verify Theorem 1 weight extraction, prediction, and theorem_holds checks."""
    k = 2
    w = theorem1_weight(coord_l1, k)
    assert w == 1.0

    v = np.array([3.0, -4.0])
    assert theorem1_predict(v, w) == 7.0

    probes = [np.array([1.0, 2.0]), np.array([-3.0, 4.0])]
    ok, w_ret = theorem1_holds(coord_l1, probes)
    assert ok and w_ret == 1.0

    # Test failure case for non-l1 norm (e.g. l2)
    ok_fail, _ = theorem1_holds(coord_l2, probes)
    assert not ok_fail

    # No probes cannot provide even finite evidence.
    with pytest.raises(ValueError, match="at least one probe"):
        theorem1_holds(coord_l1, [])


def test_edge_orbit_diagnostic():
    """Test EdgeOrbitDiagnostic orbit-weighted aggregation and dimension validation."""
    diag = EdgeOrbitDiagnostic(orbit_of_edge=(0, 1, 0), orbit_weights=(2.0, 5.0))
    e0 = np.array([1.0, 2.0])
    e1 = np.array([3.0, 0.0])
    e2 = np.array([0.0, -4.0])

    tot = diag.total([e0, e1, e2])
    assert np.isclose(tot, 29.0)

    # Exact total
    tot_exact = diag.total_exact([[Fraction(1), Fraction(2)], [Fraction(3), Fraction(0)], [Fraction(0), Fraction(-4)]])
    assert tot_exact == Fraction(29)

    with pytest.raises(ValueError, match="edge count mismatch"):
        diag.total([e0, e1])

    with pytest.raises(ValueError, match="edge count mismatch"):
        diag.total_exact([[Fraction(1)]])


def test_counterexamples():
    """Verify CE1 through CE5 counterexample witnesses."""
    assert ce1_l2_fails_additivity()
    assert ce2_anisotropic_fails_symmetry()
    assert ce3_max_fails_additivity()
    assert ce4_orbit_weights_do_not_collapse()
    assert ce5_lp_power_fails_homogeneity(p=2.0)
    assert ce5_lp_power_fails_homogeneity(p=0.5)


def test_uniform_collapse():
    """Test uniform_collapse factor extraction."""
    # Uniform weights
    tot, alpha = uniform_collapse([2.0, 2.0], [3.0, 4.0])
    assert np.isclose(tot, 14.0)
    assert alpha == 2.0

    # Non-uniform weights
    tot2, alpha2 = uniform_collapse([1.0, 3.0], [3.0, 4.0])
    assert np.isclose(tot2, 15.0)
    assert alpha2 is None

    # Empty weights
    tot3, alpha3 = uniform_collapse([], [])
    assert tot3 == 0.0 and alpha3 is None


def test_zero_weight_seminorm_boundary():
    """Test the boundary case of vanishing weight w_e = 0."""
    w0 = 0.0
    v = np.array([5.0, -12.0])
    assert coord_l1(v, weight=w0) == 0.0
    # Seminorm holds trivially
    probes = [v, np.array([1.0, 0.0])]
    ok, w_ret = theorem1_holds(lambda x: coord_l1(x, weight=0.0), probes)
    assert ok and w_ret == 0.0
