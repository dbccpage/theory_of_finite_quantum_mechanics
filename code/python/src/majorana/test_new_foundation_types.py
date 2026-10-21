"""Tests for newly unified foundation types in omega_types."""

from omega_engine.crates.type import (
    PrimitiveDifference,
    ResidualToleranceGate,
)


def test_primitive_difference_invariance():
    pd = PrimitiveDifference[int, int](
        delta=lambda x, y: (x % 2) - (y % 2), zero=lambda value: value == 0,
    )
    assert pd.zero_rel(2, 4)
    assert not pd.zero_rel(2, 3)

    assert pd.invariant_congruent(lambda x: x % 2, [(2, 4), (1, 3)])
    assert not pd.invariant_congruent(lambda x: x, [(2, 4)])


def test_residual_tolerance_gate():
    gate = ResidualToleranceGate(tolerance=1e-6)
    assert gate.is_closed(1e-8)
    assert not gate.is_closed(1e-4)
    assert not gate.is_closed(-1.0)



