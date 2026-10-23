"""Refusal and boundary tests for coda_q_core and continuum.

Invariant: floats, bools, unordered intervals, empty packets of samples, and
out-of-range Cauchy starts refuse. Each case asserts an exact exception or
False outcome.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, cast

import pytest
from coda_q_core import (
    RationalSequence,
    SampledSignal,
    _validate_exact_int,
    _validate_exact_rational,
    enclosure_endpoint_sequence,
    enclosure_error,
    enclosure_error_bound,
    is_cauchy_from,
    midpoint,
    nested_sqrt2_enclosures,
    query_collides_on_profile,
    reproduce_sqrt2_picture,
    sequences_close_from,
    sqrt_step,
)
from continuum import Enclosure, sqrt2_enclosure


class _IntWithFloatDtype(int):
    dtype = "float64"


class _ValueWithFloatDtype:
    dtype = "float32"


def test_validate_exact_rational_refuses_float_bool_and_junk() -> None:
    # Invariant: scalar inputs are int/Fraction/digit-string; floats and bools raise.
    with pytest.raises(TypeError, match="got bool"):
        _validate_exact_rational(True, "x")
    with pytest.raises(TypeError, match="got bool"):
        midpoint(False, 1)
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        _validate_exact_rational(0.5, "x")
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        midpoint(1.0, 2)
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        _validate_exact_rational(_ValueWithFloatDtype(), "x")
    with pytest.raises(TypeError, match="got list"):
        _validate_exact_rational([1], "x")
    with pytest.raises(TypeError, match="could not be converted"):
        _validate_exact_rational("not-a-fraction", "x")
    with pytest.raises(TypeError, match="could not be converted"):
        _validate_exact_rational("1/0", "x")
    assert _validate_exact_rational(Fraction(3, 2), "x") == Fraction(3, 2)
    assert _validate_exact_rational(4, "x") == Fraction(4)
    assert _validate_exact_rational("5/2", "x") == Fraction(5, 2)


def test_validate_exact_int_refuses_float_bool_and_negative() -> None:
    with pytest.raises(TypeError, match="got bool"):
        _validate_exact_int(True, "steps")
    with pytest.raises(TypeError, match="got float"):
        _validate_exact_int(1.0, "steps")
    with pytest.raises(TypeError, match="got str"):
        _validate_exact_int("2", "steps")
    with pytest.raises(TypeError, match="must be an integer"):
        _validate_exact_int(_IntWithFloatDtype(1), "steps")
    with pytest.raises(ValueError, match="must be non-negative"):
        _validate_exact_int(-1, "steps")
    with pytest.raises(ValueError, match="must be non-negative"):
        nested_sqrt2_enclosures(-1)
    assert _validate_exact_int(0, "steps") == 0
    assert len(nested_sqrt2_enclosures(0)) == 1


def test_unordered_interval_is_refused() -> None:
    # Invariant: lo ≤ hi is a hard guard on midpoint, width, error, and step.
    with pytest.raises(ValueError, match="lo must be"):
        midpoint(2, 1)
    with pytest.raises(ValueError, match="lo must be"):
        enclosure_error_bound(2, 1)
    with pytest.raises(ValueError, match="lo must be"):
        enclosure_error(2, 1, 1)
    with pytest.raises(ValueError, match="lo must be"):
        sqrt_step(2, 1)
    with pytest.raises(ValueError, match="enclosure lower must"):
        Enclosure(Fraction(2), Fraction(1))


def test_enclosure_error_requires_point_inside() -> None:
    with pytest.raises(ValueError, match="x must lie in"):
        enclosure_error(1, 2, 3)
    with pytest.raises(ValueError, match="x must lie in"):
        enclosure_error(1, 2, 0)
    assert enclosure_error(1, 2, 1) == Fraction(1, 2)


def test_sqrt_step_rejects_negative_lower() -> None:
    with pytest.raises(ValueError, match="lo must be nonnegative"):
        sqrt_step(-1, 1)
    keep_upper = sqrt_step(Fraction(1), Fraction(2))
    assert keep_upper == (Fraction(1), Fraction(3, 2))
    keep_lower = sqrt_step(Fraction(1), Fraction(3, 2))
    assert keep_lower == (Fraction(5, 4), Fraction(3, 2))


def test_rational_sequence_rejects_bad_terms_and_index() -> None:
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        RationalSequence(terms=cast(Any, (0.5, 1)))
    seq = RationalSequence(terms=cast(Any, (0, 1, 2)))
    other = RationalSequence(terms=cast(Any, (0, 4)))
    with pytest.raises(ValueError, match="index out of range"):
        seq.distance_at(other, 2)
    with pytest.raises(ValueError, match="index out of range"):
        seq.distance_at(other, 5)
    with pytest.raises(TypeError, match="got bool"):
        seq.distance_at(other, cast(Any, True))
    assert seq.distance_at(other, 1) == Fraction(3)


def test_cauchy_and_close_guards() -> None:
    seq = RationalSequence(terms=(Fraction(0), Fraction(1)))
    with pytest.raises(ValueError, match="epsilon must be positive"):
        is_cauchy_from(seq, 0, 0)
    with pytest.raises(ValueError, match="epsilon must be positive"):
        is_cauchy_from(seq, 0, Fraction(-1, 10))
    with pytest.raises(ValueError, match="start out of range"):
        is_cauchy_from(seq, 2, Fraction(1, 2))
    with pytest.raises(ValueError, match="epsilon must be positive"):
        sequences_close_from(seq, seq, 0, 0)
    with pytest.raises(ValueError, match="start out of range"):
        sequences_close_from(seq, seq, 2, Fraction(1, 2))
    short = RationalSequence(terms=(Fraction(0),))
    with pytest.raises(ValueError, match="start out of range"):
        sequences_close_from(seq, short, 1, Fraction(1, 2))
    assert is_cauchy_from(seq, 0, Fraction(2)) is True
    assert is_cauchy_from(seq, 1, Fraction(1, 10)) is True
    assert sequences_close_from(seq, seq, 0, Fraction(1, 10)) is True


def test_endpoint_sequence_rejects_unknown_which() -> None:
    with pytest.raises(ValueError, match="which must be"):
        enclosure_endpoint_sequence(1, "sideways")
    assert enclosure_endpoint_sequence(1, "lower").terms[1] == sqrt2_enclosure(1).lower
    assert enclosure_endpoint_sequence(1, "upper").terms[1] == sqrt2_enclosure(1).upper
    assert enclosure_endpoint_sequence(1, "midpoint").terms[1] == sqrt2_enclosure(1).midpoint


def test_reproduce_picture_and_float_steps_refused() -> None:
    with pytest.raises(TypeError, match="got float"):
        reproduce_sqrt2_picture(cast(Any, 2.0))
    picture = reproduce_sqrt2_picture()
    assert picture["steps"] == 5
    assert picture["verifies"] is True
    assert picture["error_bound"] > 0


def test_sampled_signal_refuses_float_and_missing_node() -> None:
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        SampledSignal("bad", cast(Any, {0: 0.5}))
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        SampledSignal("bad", cast(Any, {0.5: 0}))
    signal = SampledSignal("unit", cast(Any, {0: 0, 1: 1}))
    with pytest.raises(KeyError, match="has no sample"):
        signal.evaluate_at(Fraction(1, 2))
    assert signal.evaluate_at(1) == Fraction(1)


def test_query_collision_false_when_profile_differs() -> None:
    zero = Fraction(0)
    one = Fraction(1)
    half = Fraction(1, 2)
    left = SampledSignal("a", {zero: zero, one: zero, half: zero})
    right = SampledSignal("b", {zero: zero, one: one, half: half})
    assert query_collides_on_profile(left, right, (zero, one), half) is False
    twin = SampledSignal("c", {zero: zero, one: zero, half: zero})
    assert query_collides_on_profile(left, twin, (zero, one), half) is False


def test_sqrt2_enclosure_refuses_non_integer_steps() -> None:
    with pytest.raises(ValueError, match="steps must be a nonnegative integer"):
        sqrt2_enclosure(cast(Any, 1.0))
    with pytest.raises(ValueError, match="steps must be a nonnegative integer"):
        sqrt2_enclosure(cast(Any, True))
    with pytest.raises(ValueError, match="steps must be a nonnegative integer"):
        sqrt2_enclosure(-2)


def test_enclosure_verifies_sqrt2_only_when_endpoints_bracket() -> None:
    assert Enclosure(Fraction(2), Fraction(3)).verifies_sqrt2() is False
    assert Enclosure(Fraction(0), Fraction(1)).verifies_sqrt2() is False
    enc = sqrt2_enclosure(4)
    assert enc.verifies_sqrt2() is True
    assert enc.error_bound > 0
    assert enc.midpoint**2 != 2
