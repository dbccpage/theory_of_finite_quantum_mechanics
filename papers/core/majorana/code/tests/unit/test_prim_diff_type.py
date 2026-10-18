r"""
Unit tests for PrimitiveDifference kernel (omega_engine/type/primitive_difference.py).
Backing: Lean 4 OmegaCore.PrimitiveDifference.
"""

import pytest
from omega_engine.crates.type.primitive_difference import (
    PointedPrimitiveDifference,
    PrimitiveDifference,
    PrimitiveDifferenceJudgment,
    ResidualClass,
)


def test_primitive_difference_basic():
    # Difference of integers delta(x, y) = x - y, Zero(b) = (b == 0)
    pd = PrimitiveDifference[int, int](delta=lambda x, y: x - y, zero=lambda b: b == 0)

    assert pd.delta(5, 3) == 2
    assert pd.zero_rel(5, 5) is True
    assert pd.zero_rel(5, 3) is False

    c1 = pd.class_of(5)
    c2 = pd.class_of(5)
    c3 = pd.class_of(3)

    assert c1 == c2
    assert c1 != c3


def test_delta_congruence_and_factorization():
    pd = PrimitiveDifference[int, int](delta=lambda x, y: (x % 2) - (y % 2), zero=lambda b: b == 0)

    # Parity equivalence: x ~ x' iff x % 2 == x' % 2
    c0 = pd.class_of(2)
    c1 = pd.class_of(3)

    assert pd.delta_factor(c1, c0) == 1

    # Check DeltaCongruent on tuples
    tuples = [(2, 4, 3, 5)]  # 2~4 (both even), 3~5 (both odd) => delta(2, 3) == delta(4, 5)
    assert pd.delta_congruent(tuples) is True


def test_invariant_factorization():
    pd = PrimitiveDifference[int, int](delta=lambda x, y: (x % 2) - (y % 2), zero=lambda b: b == 0)

    # Function phi(x) = x % 2 is invariant
    phi = lambda x: x % 2
    assert pd.invariant_congruent(phi, [(2, 4), (1, 3)]) is True

    # Function psi(x) = x is NOT invariant
    psi = lambda x: x
    assert pd.invariant_congruent(psi, [(2, 4)]) is False


def test_pointed_primitive_difference():
    ppd = PointedPrimitiveDifference[int, int](
        delta=lambda x, y: x - y, zero_pred=lambda b: b == 0, zero_element=0
    )

    c0 = ppd.class_of(0)
    c5 = ppd.class_of(5)

    assert ppd.is_zero_class(c0) is True
    assert ppd.is_zero_class(c5) is False


