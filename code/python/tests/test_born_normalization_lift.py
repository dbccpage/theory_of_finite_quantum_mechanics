"""Lev Landau Invariant & Unit Tests for QM-020 Born Normalization & Hilbert Lift.

Verifies:
1. Pure L1 probability distribution converts to unit L2 Hilbert amplitude.
2. Born rule normalization redundancy under phase variation.
3. Exact rational purity calculation and consistency checks.
4. Seamless evaluation in `src.qm.born_normalization`.
5. Property-based tests across higher-dimensional finite probability simplices
   with random phase profiles under Hypothesis.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from hypothesis import assume, given, settings, strategies as st
import numpy as np
import pytest

from src.qm.born_normalization import (
    BornNormalizationError,
    PaperEvaluator,
    exact_born_purity,
    l1_to_l2_amplitude_lift,
    verify_born_normalization,
)


def test_qm020_evaluators_pass():
    """Verify PaperEvaluator yields consistent passing certificates."""
    ev = PaperEvaluator()
    res = ev.evaluate()
    assert res["paper_id"] == "qm_020_born_normalization_and_conditional_hilbert_lift"
    assert res["status"] == "EVALUATED_PASS"
    assert res["born_normalization"] is True
    assert res["exact_purity"] == Fraction(5, 8)
    assert pytest.approx(res["sample_l2_norm_sq"], 1e-9) == 1.0


def test_l1_to_l2_amplitude_lift():
    """Verify discrete L1 probability distribution converts to unit L2 complex amplitude."""
    rho = np.array([3.0, 1.0])
    phases = np.array([0.0, np.pi / 2])
    psi = l1_to_l2_amplitude_lift(rho, phases)

    assert pytest.approx(abs(psi[0]), 1e-6) == np.sqrt(0.75)
    assert pytest.approx(abs(psi[1]), 1e-6) == 0.5
    assert verify_born_normalization(psi)


def test_exact_born_purity_and_refusals():
    """Verify exact purity on rational distributions and typed error refusals."""
    purity = exact_born_purity([Fraction(1, 2), Fraction(1, 2)])
    assert purity == Fraction(1, 2)

    pure = exact_born_purity([1, 0, 0])
    assert pure == Fraction(1, 1)

    # Refuse negative weights
    with pytest.raises(ValueError, match="non-negative"):
        exact_born_purity([-1, 2])

    # Refuse zero total mass
    with pytest.raises(ValueError, match="positive sum"):
        exact_born_purity([0, 0])


def test_amplitude_lift_refusals():
    """Verify typed domain refusals on unadmitted inputs."""
    with pytest.raises(ValueError, match="non-negative"):
        l1_to_l2_amplitude_lift(np.array([-0.5, 1.5]))

    with pytest.raises(ValueError, match="positive sum"):
        l1_to_l2_amplitude_lift(np.array([0.0, 0.0]))

    with pytest.raises(ValueError, match="shape"):
        l1_to_l2_amplitude_lift(np.array([0.5, 0.5]), phases=np.array([0.0]))


# ============================================================================
# Property-Based Tests Across Higher-Dimensional Simplices & Phase Profiles
# ============================================================================


@settings(max_examples=100, deadline=None)
@given(
    weights=st.lists(
        st.floats(min_value=0.0, max_value=1e5, allow_nan=False, allow_infinity=False),
        min_size=2,
        max_size=50,
    ),
    seed_offset=st.integers(min_value=0, max_value=10000),
)
def test_pbt_simplex_born_normalization_and_phase_invariance(weights: list[float], seed_offset: int):
    """Property: For any finite simplex of dimension d in [2, 50],
    the conditional L1-to-L2 Hilbert lift satisfies Born normalization,
    and Born readout probabilities are strictly phase-invariant.
    """
    arr = np.array(weights, dtype=float)
    total = float(np.sum(arr))
    assume(total > 1e-9)

    d = len(arr)
    rng = np.random.default_rng(seed=seed_offset + int(abs(total * 1000) % 2**31))
    phases = rng.uniform(-np.pi, np.pi, size=d)

    psi_phased = l1_to_l2_amplitude_lift(arr, phases)
    psi_unphased = l1_to_l2_amplitude_lift(arr)

    # 1. Born normalization sum_k |psi_k|^2 == 1 holds under both configurations
    assert verify_born_normalization(psi_phased, atol=1e-7)
    assert verify_born_normalization(psi_unphased, atol=1e-7)

    # 2. Born probabilities match the normalized L1 simplex distribution
    prob_phased = np.abs(psi_phased) ** 2
    prob_unphased = np.abs(psi_unphased) ** 2
    expected_prob = arr / total

    np.testing.assert_allclose(prob_phased, expected_prob, atol=1e-7, rtol=1e-7)
    np.testing.assert_allclose(prob_unphased, expected_prob, atol=1e-7, rtol=1e-7)

    # 3. Readout probabilities are strictly invariant to coordinate phase shifts
    np.testing.assert_allclose(prob_phased, prob_unphased, atol=1e-9)


@settings(max_examples=100, deadline=None)
@given(
    weights=st.lists(
        st.floats(min_value=0.0, max_value=1e4, allow_nan=False, allow_infinity=False),
        min_size=2,
        max_size=40,
    ),
    scale=st.floats(min_value=1e-4, max_value=1e4, allow_nan=False, allow_infinity=False),
)
def test_pbt_simplex_ray_invariance(weights: list[float], scale: float):
    """Property: Scaling sector weights w -> c * w for any positive scalar c > 0
    leaves the normalized Hilbert lift amplitude profile invariant.
    """
    arr = np.array(weights, dtype=float)
    total = float(np.sum(arr))
    assume(total > 1e-9)

    psi_original = l1_to_l2_amplitude_lift(arr)
    psi_scaled = l1_to_l2_amplitude_lift(scale * arr)

    np.testing.assert_allclose(np.abs(psi_original), np.abs(psi_scaled), atol=1e-9)


@settings(max_examples=100, deadline=None)
@given(
    int_weights=st.lists(
        st.integers(min_value=0, max_value=1000),
        min_size=2,
        max_size=30,
    )
)
def test_pbt_exact_rational_purity_bounds(int_weights: list[int]):
    """Property: For any integer simplex weights with positive total mass,
    exact rational purity gamma_2 = sum (w_i / mass)^2 lies strictly in [1/d, 1],
    with gamma_2 == 1 iff the state is rank-1 pure, and gamma_2 == 1/d for uniform weights.
    """
    total = sum(int_weights)
    assume(total > 0)

    d = len(int_weights)
    purity = exact_born_purity(int_weights)

    # Purity must lie in [1/d, 1]
    assert Fraction(1, d) <= purity <= Fraction(1, 1)

    non_zero_count = sum(1 for w in int_weights if w > 0)
    if non_zero_count == 1:
        assert purity == Fraction(1, 1)
    else:
        assert purity < Fraction(1, 1)

    # Uniform distribution attains lower bound 1/d
    if len(set(int_weights)) == 1 and int_weights[0] > 0:
        assert purity == Fraction(1, d)
