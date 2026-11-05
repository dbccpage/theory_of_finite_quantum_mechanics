"""Adversarial controls for the sampled Duhamel evaluator's evidence boundary."""

from __future__ import annotations

import sys
from dataclasses import FrozenInstanceError, asdict
from fractions import Fraction
from pathlib import Path

import pytest

_code_dir = Path(__file__).resolve().parents[1]
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

from observable_duhamel import (  # noqa: E402
    DuhamelCertificationError,
    DuhamelInputError,
    Interval,
    NumericalErrorEnclosure,
    evaluate_observable_duhamel_bound,
    evaluate_observable_duhamel_detailed,
)


def test_hidden_between_sample_bump_cannot_be_an_error_certificate() -> None:
    # At distance zero the supplied weight is one. The two endpoint samples
    # both vanish, but integral_0^1 6s(1-s) ds = 3 - 2 = 1 exactly.
    result = evaluate_observable_duhamel_detailed(
        observable=(0,),
        defects_by_edge={(0, 1): lambda s: 6 * s * (1 - s)},
        time_horizon=1,
        quadrature_steps=2,
    )
    exact_integral = Fraction(6, 2) - Fraction(6, 3)
    assert result.bound_interval.upper == 0
    assert exact_integral == 1
    assert not result.bound_interval.contains(float(exact_integral))
    assert result.certificate_status == "not_certified"
    assert result.bound_interval.certificate_status == "not_certified"
    # This old sample-size flag must not be mistaken for a physical guarantee.
    assert result.is_informative is True
    assert "between-sample" in " ".join(result.certification_limitations)


@pytest.mark.parametrize(
    "evaluate", [evaluate_observable_duhamel_bound, evaluate_observable_duhamel_detailed]
)
def test_certification_request_fails_before_evaluating_untrusted_rate(evaluate) -> None:
    def rate(_time: float) -> float:
        pytest.fail("A refused certification request must not execute the rate")

    with pytest.raises(DuhamelCertificationError, match="Certified evaluation is unavailable"):
        evaluate(
            (0,), {(0, 1): rate}, 1, numerical_error=100, require_certified=True
        )


def test_noncertified_metadata_is_fixed_and_serialized() -> None:
    result = evaluate_observable_duhamel_detailed((0,), {(0, 1): 0.5}, 0.2)
    payload = asdict(result)
    assert payload["certificate_status"] == "not_certified"
    assert payload["bound_interval"]["certificate_status"] == "not_certified"
    with pytest.raises(FrozenInstanceError):
        result.certificate_status = "certified"
    with pytest.raises(FrozenInstanceError):
        result.bound_interval.certificate_status = "certified"
    with pytest.raises(TypeError):
        Interval(0, 1, certificate_status="certified")


def test_float_interval_arithmetic_preserves_noncertified_status() -> None:
    # Exact decimal sum 3/10 need not equal its binary floating computation.
    result = Interval(0.1, 0.1) + Interval(0.2, 0.2)
    assert result.lower > float(Fraction(3, 10))
    assert result.certificate_status == "not_certified"
    assert "outward rounded" in " ".join(result.certification_limitations)
    with pytest.raises(DuhamelInputError, match="exceeds upper"):
        Interval(1 + 1e-15, 1)


@pytest.mark.parametrize("value", [-1.0, float("nan"), float("inf"), True])
@pytest.mark.parametrize("representation", ["constant", "callable", "samples"])
def test_invalid_rates_are_refused_for_every_input_form(value, representation) -> None:
    spec = value
    if representation == "callable":
        spec = lambda _time: value
    elif representation == "samples":
        spec = [0.0, value]
    with pytest.raises(DuhamelInputError):
        evaluate_observable_duhamel_bound((0,), {(0, 1): spec}, 1)


def test_empty_rate_samples_are_refused() -> None:
    with pytest.raises(DuhamelInputError, match="cannot be empty"):
        evaluate_observable_duhamel_bound((0,), {(0, 1): []}, 1)


@pytest.mark.parametrize("steps", [True, 1, 2.5])
def test_quadrature_node_count_is_an_explicit_integer_contract(steps) -> None:
    with pytest.raises(DuhamelInputError, match="quadrature_steps"):
        evaluate_observable_duhamel_bound((0,), {(0, 1): 1}, 1, quadrature_steps=steps)


@pytest.mark.parametrize("value", [-1, float("nan"), float("inf"), True])
def test_error_allowances_are_finite_nonnegative_and_still_not_certificates(value) -> None:
    with pytest.raises(DuhamelInputError):
        NumericalErrorEnclosure(quadrature_error=value)
    with pytest.raises(DuhamelInputError):
        evaluate_observable_duhamel_bound((0,), {}, 1, numerical_error=value)
    assert NumericalErrorEnclosure(quadrature_error=1).certificate_status == "not_certified"


def test_boolean_certification_request_cannot_be_supplied_as_integer() -> None:
    with pytest.raises(DuhamelInputError, match="require_certified must be a boolean"):
        evaluate_observable_duhamel_bound((0,), {}, 1, require_certified=1)


def test_capped_total_does_not_subtract_allowances_from_the_convolution() -> None:
    result = evaluate_observable_duhamel_detailed((0,), {}, 1, initial_error=3)
    assert result.bound_interval.upper == 2
    assert result.influence_convolution == 0
    assert result.per_edge_contributions == {}


def test_raw_sample_convolution_and_edge_contributions_survive_the_total_cap() -> None:
    result = evaluate_observable_duhamel_detailed(
        (0,), {(0, 1): 3, (0, 2): 4}, 1,
        initial_error=0.25, numerical_error=0.5, quadrature_steps=2,
    )
    assert result.bound_interval.upper == 2
    assert result.influence_convolution == 7
    assert result.per_edge_contributions == {"(0,1)": 3, "(0,2)": 4}
    assert sum(result.per_edge_contributions.values()) == result.influence_convolution
    assert result.certificate_status == "not_certified"
