"""Injected-fault mutants for CODA-Q decision procedures.

Each mutant locally redefines one production decision. Tests assert that the
mutant disagrees with the real oracle on a known packet, so the suite kills
the fault if it is ever injected into production.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Sequence, cast

import pytest
from coda_q_core import (
    RationalSequence,
    SampledSignal,
    _validate_exact_int,
    _validate_exact_rational,
    is_cauchy_from,
    midpoint,
    query_collides_on_profile,
    two_signal_sample_collision,
)
from continuum import Enclosure, sqrt2_enclosure


def _zero_and_quadratic() -> tuple[SampledSignal, SampledSignal]:
    zero = Fraction(0)
    one = Fraction(1)
    half = Fraction(1, 2)
    left = SampledSignal("zero", {zero: zero, one: zero, half: zero})
    right = SampledSignal("t(t-1)", {zero: zero, one: zero, half: half * (half - one)})
    return left, right


def mutant_promote_incomplete_or_mismatched_to_standing(
    left: SampledSignal,
    right: SampledSignal,
    profile_nodes: Sequence[Any],
    query_node: Any,
) -> bool:
    """Promote a query mismatch to standing even when the profile is incomplete or disagrees."""
    del profile_nodes
    try:
        return left.evaluate_at(query_node) != right.evaluate_at(query_node)
    except KeyError:
        return True


def mutant_is_cauchy_skip_spread_guard(seq: RationalSequence, start: Any, epsilon: Any) -> bool:
    """Skip the pairwise Cauchy halt and report the finite list as Cauchy."""
    n0 = _validate_exact_int(start, "start")
    eps = _validate_exact_rational(epsilon, "epsilon")
    if eps <= 0:
        raise ValueError("epsilon must be positive")
    if n0 >= len(seq.terms):
        raise ValueError("start out of range")
    return True


def mutant_midpoint_skip_order_guard(lo: Any, hi: Any) -> Fraction:
    """Skip the lo ≤ hi halt guard and still return a midpoint."""
    left = _validate_exact_rational(lo, "lo")
    right = _validate_exact_rational(hi, "hi")
    return (left + right) / 2


def mutant_validate_accept_float(val: Any, name: str) -> Fraction:
    """Accept IEEE 754 floats by converting them instead of refusing."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an exact rational or integer, got bool")
    if isinstance(val, float):
        return Fraction(val).limit_denominator()
    dtype = getattr(val, "dtype", None)
    if dtype is not None and "float" in str(dtype).lower():
        return Fraction(val).limit_denominator()
    return _validate_exact_rational(val, name)


def mutant_sqrt2_enclosure_accept_float(steps: Any) -> Enclosure:
    """Accept IEEE 754 float step counts by truncating them instead of refusing."""
    if isinstance(steps, bool):
        raise ValueError("steps must be a nonnegative integer")
    if isinstance(steps, float):
        steps = int(steps)
    return sqrt2_enclosure(steps)


def mutant_claim_midpoint_exact_without_width(enc: Enclosure) -> bool:
    """Claim the enclosure midpoint is exactly sqrt(2) whenever the interval verifies."""
    return enc.verifies_sqrt2()


def _real_float_rational_outcome(val: Any) -> Any:
    try:
        return _validate_exact_rational(val, "x")
    except TypeError as exc:
        if "float" in str(exc):
            return "refused_float"
        raise


def _real_float_steps_outcome(steps: Any) -> Any:
    try:
        return sqrt2_enclosure(steps)
    except ValueError as exc:
        if "nonnegative integer" in str(exc):
            return "refused_non_int"
        raise


def _real_midpoint_outcome(lo: Any, hi: Any) -> Any:
    try:
        return midpoint(lo, hi)
    except ValueError as exc:
        if "lo must be" in str(exc):
            return "refused_unordered"
        raise


def test_mutant_promote_incomplete_or_mismatched_killed() -> None:
    # Invariant: a missing query sample or a mismatched profile is not a collision.
    left, right = _zero_and_quadratic()
    zero, one, half = Fraction(0), Fraction(1), Fraction(1, 2)

    incomplete = SampledSignal("no-query", {zero: zero, one: zero})
    with pytest.raises(KeyError, match="has no sample"):
        query_collides_on_profile(left, incomplete, (zero, one), half)
    mutant_incomplete = mutant_promote_incomplete_or_mismatched_to_standing(
        left, incomplete, (zero, one), half
    )
    assert mutant_incomplete is True

    mismatched = SampledSignal("off-profile", {zero: zero, one: one, half: half})
    real_mismatch = query_collides_on_profile(left, mismatched, (zero, one), half)
    mutant_mismatch = mutant_promote_incomplete_or_mismatched_to_standing(
        left, mismatched, (zero, one), half
    )
    assert real_mismatch is False
    assert mutant_mismatch is True
    assert mutant_mismatch is not real_mismatch

    real_ok = query_collides_on_profile(left, right, (zero, one), half)
    mutant_ok = mutant_promote_incomplete_or_mismatched_to_standing(left, right, (zero, one), half)
    assert real_ok is True
    assert mutant_ok is True
    assert two_signal_sample_collision()["collides"] is True

    real_same = query_collides_on_profile(left, left, (zero, one), half)
    mutant_same = mutant_promote_incomplete_or_mismatched_to_standing(left, left, (zero, one), half)
    assert real_same is False
    assert mutant_same is False


def test_mutant_skip_halt_guard_killed() -> None:
    # Invariant: a spread sequence is not Cauchy; an unordered interval is not a midpoint.
    spread = RationalSequence(terms=(Fraction(0), Fraction(1), Fraction(0)))
    real_cauchy = is_cauchy_from(spread, 0, Fraction(1, 2))
    mutant_cauchy = mutant_is_cauchy_skip_spread_guard(spread, 0, Fraction(1, 2))
    assert real_cauchy is False
    assert mutant_cauchy is True
    assert mutant_cauchy is not real_cauchy

    tight = RationalSequence(terms=(Fraction(1), Fraction(1), Fraction(1)))
    assert is_cauchy_from(tight, 0, Fraction(1, 10)) is True
    assert mutant_is_cauchy_skip_spread_guard(tight, 0, Fraction(1, 10)) is True

    with pytest.raises(ValueError, match="epsilon must be positive"):
        is_cauchy_from(spread, 0, 0)
    with pytest.raises(ValueError, match="epsilon must be positive"):
        mutant_is_cauchy_skip_spread_guard(spread, 0, 0)

    real_mid = _real_midpoint_outcome(2, 1)
    mutant_mid = mutant_midpoint_skip_order_guard(2, 1)
    assert real_mid == "refused_unordered"
    assert mutant_mid == Fraction(3, 2)
    assert mutant_mid != real_mid
    assert midpoint(1, 2) == mutant_midpoint_skip_order_guard(1, 2)


def test_mutant_accept_float_killed() -> None:
    # Invariant: floats are refused; a mutant that converts them disagrees.
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        _validate_exact_rational(0.25, "x")
    with pytest.raises(ValueError, match="steps must be a nonnegative integer"):
        sqrt2_enclosure(cast(Any, 2.0))

    real_half = _real_float_rational_outcome(0.25)
    mutant_half = mutant_validate_accept_float(0.25, "x")
    assert real_half == "refused_float"
    assert mutant_half == Fraction(1, 4)
    assert mutant_half != real_half

    real_two = _real_float_steps_outcome(2.0)
    mutant_two = mutant_sqrt2_enclosure_accept_float(2.0)
    assert real_two == "refused_non_int"
    assert mutant_two == sqrt2_enclosure(2)
    assert mutant_two != real_two

    real_int = _validate_exact_rational(2, "x")
    mutant_int = mutant_validate_accept_float(2, "x")
    assert real_int == Fraction(2)
    assert mutant_int == real_int
    assert mutant_sqrt2_enclosure_accept_float(3) == sqrt2_enclosure(3)

    with pytest.raises(TypeError, match="got bool"):
        _validate_exact_rational(False, "x")
    with pytest.raises(TypeError, match="got bool"):
        mutant_validate_accept_float(False, "x")
    with pytest.raises(ValueError, match="steps must be a nonnegative integer"):
        mutant_sqrt2_enclosure_accept_float(True)


def test_mutant_midpoint_exact_without_width_killed() -> None:
    # Invariant: a verifying enclosure does not certify that its midpoint equals sqrt(2).
    enc = sqrt2_enclosure(8)
    real = enc.midpoint_certified_exact_sqrt2()
    mutant = mutant_claim_midpoint_exact_without_width(enc)
    assert enc.verifies_sqrt2() is True
    assert enc.error_bound == Fraction(1, 2**9)
    assert enc.error_bound > 0
    assert enc.midpoint**2 != 2
    assert enc.lower**2 <= 2 <= enc.upper**2
    assert real is False
    assert mutant is True
    assert mutant is not real

    degenerate = Enclosure(Fraction(2), Fraction(2))
    assert degenerate.error_bound == 0
    assert degenerate.verifies_sqrt2() is False
    assert degenerate.midpoint_certified_exact_sqrt2() is False
    assert mutant_claim_midpoint_exact_without_width(degenerate) is False
