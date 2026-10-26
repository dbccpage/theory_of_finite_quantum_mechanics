"""Happy-path tests for CODA-Q exact rational enclosures and sample collision.

Invariant: nested √2 enclosures verify by squared endpoints, midpoint error is
bounded by half-width, and the two-signal sample collision disagrees at 1/2.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any, cast

import pytest
from coda_q_core import (
    RationalSequence,
    SampledSignal,
    enclosure_endpoint_sequence,
    enclosure_error,
    enclosure_error_bound,
    is_cauchy_from,
    midpoint,
    nested_sqrt2_enclosures,
    profile_values,
    query_collides_on_profile,
    reproduce_sqrt2_picture,
    same_profile,
    sequences_close_from,
    sqrt_step,
    two_signal_sample_collision,
)
from continuum import Enclosure, sqrt2_enclosure


def test_package_evaluator_passes() -> None:
    import coda_q_core
    import continuum

    assert hasattr(coda_q_core, "midpoint")
    assert hasattr(coda_q_core, "sqrt_step")
    assert hasattr(coda_q_core, "reproduce_sqrt2_picture")
    assert hasattr(coda_q_core, "two_signal_sample_collision")
    assert hasattr(continuum, "Enclosure")
    assert hasattr(continuum, "sqrt2_enclosure")


def test_midpoint_and_error_bound_on_ordered_rationals() -> None:
    # Invariant: midpoint and half-width are exact on an ordered rational interval.
    lo, hi = Fraction(1), Fraction(2)
    assert midpoint(lo, hi) == Fraction(3, 2)
    assert enclosure_error_bound(lo, hi) == Fraction(1, 2)
    assert enclosure_error(lo, hi, Fraction(3, 2)) == Fraction(0)
    assert enclosure_error(lo, hi, lo) == Fraction(1, 2)
    assert enclosure_error(lo, hi, hi) == Fraction(1, 2)
    assert midpoint("1", 2) == Fraction(3, 2)


def test_sqrt_step_and_nested_enclosures() -> None:
    # Invariant: one bisection preserves the √2 enclosure and halves the width.
    lo, hi = sqrt_step(Fraction(1), Fraction(2))
    assert (lo, hi) == (Fraction(1), Fraction(3, 2))
    assert lo**2 <= 2 <= hi**2

    lo2, hi2 = sqrt_step(lo, hi)
    assert (lo2, hi2) == (Fraction(5, 4), Fraction(3, 2))
    assert lo2**2 <= 2 <= hi2**2

    encs = nested_sqrt2_enclosures(3)
    assert len(encs) == 4
    assert encs[0].lower == Fraction(1)
    assert encs[0].upper == Fraction(2)
    assert encs[1].lower == lo
    assert encs[1].upper == hi
    for enc in encs:
        assert enc.verifies_sqrt2() is True
        assert enc.midpoint**2 != 2
        assert enclosure_error(enc.lower, enc.upper, enc.midpoint) <= enc.error_bound


def test_continuum_sqrt2_enclosure() -> None:
    enc0 = sqrt2_enclosure(0)
    assert enc0.lower == Fraction(1)
    assert enc0.upper == Fraction(2)
    assert enc0.midpoint == Fraction(3, 2)
    assert enc0.error_bound == Fraction(1, 2)
    assert enc0.verifies_sqrt2() is True

    enc5 = sqrt2_enclosure(5)
    assert enc5.verifies_sqrt2() is True
    assert enc5.error_bound == Fraction(1, 2**6)
    assert enc5.lower <= enc5.midpoint <= enc5.upper
    assert enc5.midpoint**2 != 2

    with pytest.raises(ValueError, match="steps must be a nonnegative integer"):
        sqrt2_enclosure(-1)
    with pytest.raises(TypeError, match="got float"):
        Enclosure(cast(Any, 0.5), cast(Any, 1.5))
    with pytest.raises(TypeError, match="got float"):
        Enclosure(Fraction(1), cast(Any, 1.5))
    assert Enclosure(Fraction(1), Fraction(2)).midpoint_certified_exact_sqrt2() is False


def test_endpoint_sequences_and_picture() -> None:
    lowers = enclosure_endpoint_sequence(4, "lower")
    uppers = enclosure_endpoint_sequence(4, "upper")
    mids = enclosure_endpoint_sequence(4, "midpoint")
    assert lowers.terms[0] == Fraction(1)
    assert uppers.terms[0] == Fraction(2)
    assert mids.terms[0] == Fraction(3, 2)
    picture = reproduce_sqrt2_picture(5)
    assert picture["steps"] == 5
    assert picture["verifies"] is True
    assert picture["midpoint_self_distance"] <= picture["error_bound"]
    assert picture["width"] == picture["upper"] - picture["lower"]
    assert picture["midpoint"] ** 2 != 2


def test_cauchy_and_close_sequences_on_nested_midpoints() -> None:
    # Invariant: nested midpoints become Cauchy; a spread sequence is not.
    mids = enclosure_endpoint_sequence(6, "midpoint")
    assert is_cauchy_from(mids, 3, Fraction(1, 8)) is True
    later = RationalSequence(terms=mids.terms[3:])
    assert sequences_close_from(mids, later, 0, Fraction(1)) is True
    spread = RationalSequence(terms=(Fraction(0), Fraction(1), Fraction(0)))
    assert is_cauchy_from(spread, 0, Fraction(1, 2)) is False
    other = RationalSequence(terms=(Fraction(0), Fraction(2), Fraction(0)))
    assert sequences_close_from(spread, other, 0, Fraction(1, 2)) is False
    assert spread.distance_at(other, 1) == Fraction(1)


def test_two_signal_sample_collision() -> None:
    # Invariant: f=0 and g=t(t-1) agree on {0,1} and differ at 1/2.
    collision = two_signal_sample_collision()
    zero = Fraction(0)
    one = Fraction(1)
    half = Fraction(1, 2)
    assert collision["profile"] == (zero, zero)
    assert collision["query_f"] == zero
    assert collision["query_g"] == half * (half - one)
    assert collision["collides"] is True

    f = SampledSignal("zero", {zero: zero, one: zero, half: zero})
    g = SampledSignal("t(t-1)", {zero: zero, one: zero, half: half * (half - one)})
    assert same_profile(f, g, (zero, one)) is True
    assert profile_values(f, (zero, one)) == (zero, zero)
    assert query_collides_on_profile(f, g, (zero, one), half) is True
    assert query_collides_on_profile(f, f, (zero, one), half) is False


def test_generate_figures(tmp_path: Path) -> None:
    from generate_figures import generate_fig1

    target = tmp_path / "fig1_authority_descent.png"
    out_path = generate_fig1(target)
    assert out_path.exists()
    assert out_path.name == "fig1_authority_descent.png"
