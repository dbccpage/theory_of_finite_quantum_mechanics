"""Cross-multiplication order certificate on exact rationals.

Origin: lean4/H001Rats.lean definition qrel (integer pairs modulo
cross-multiplication) and theorem qrel_equivalence.
Claim: urn:omega:fqm:h001:cross-sign-certificate:v1
AuthorityEffect: None
Mutation-Kills: 9 non-equivalent source mutants, executed by code/python/tests/test_ordered.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 7; AST Sonar cognitive complexity max 6; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 7.
Scope Fence: This file does not construct the H001 StarRingPack, does not
order Q(i), does not identify the carrier with Lean.Rat, and does not
inherit an authority grant from a passing sign certificate.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence

from .matrix import ExactMatrix
from .scalars import GaussianRational, Q, q


class OrderError(ValueError):
    """One violated order invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object]) -> None:
        self.invariant = invariant
        self.parameters = dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _refuse(invariant: str, **parameters: object) -> OrderError:
    return OrderError(invariant, parameters)


def _pair_to_fraction(value: tuple[object, ...], role: str) -> Fraction:
    if len(value) != 2:
        raise _refuse("rational pair must have length 2", role=role, length=len(value))
    numer, denom = value
    if isinstance(numer, bool) or isinstance(denom, bool):
        raise _refuse("boolean refused inside a rational pair", role=role)
    if type(numer) is not int or type(denom) is not int:
        raise _refuse(
            "rational pair entries must be exact integers",
            role=role,
            numerator_type=type(numer).__name__,
            denominator_type=type(denom).__name__,
        )
    if denom == 0:
        raise _refuse("rational denominator is zero", role=role, numerator=numer)
    return Fraction(numer, denom)


def require_rational(value: object, role: str) -> Fraction:
    """Accept int or Fraction only. Float, bool, and Q(i) are refused."""
    if isinstance(value, float):
        raise _refuse("float refused at the public boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _refuse("boolean refused where a rational was required", role=role)
    if isinstance(value, GaussianRational):
        raise _refuse("Q(i) is outside the order of Q", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    if isinstance(value, tuple):
        return _pair_to_fraction(value, role)
    raise _refuse("value is not an exact rational", role=role, received=type(value).__name__)


def as_fraction(value: object) -> Fraction:
    """Public boundary used by older callers. Floats are refused."""
    return require_rational(value, "value")


def _require_sequence(values: object, role: str) -> Sequence[object]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise _refuse(
            "expected a finite sequence of exact rationals",
            role=role,
            received=type(values).__name__,
        )
    return values


def _normalize_denominator(numerator: Fraction, denominator: Fraction, role: str) -> tuple[Fraction, Fraction]:
    if denominator == 0:
        raise _refuse("cross-multiplication requires a nonzero denominator", role=role)
    if denominator < 0:
        return (-numerator, -denominator)
    return (numerator, denominator)


def _sign(gap: Fraction) -> int:
    if gap > 0:
        return 1
    if gap < 0:
        return -1
    return 0


@dataclass(frozen=True)
class CrossSignCertificate:
    """Witness that sign(a/b - c/d) equals sign(a*d - b*c) after denominators are positive."""

    left_numerator: Fraction
    left_denominator: Fraction
    right_numerator: Fraction
    right_denominator: Fraction
    gap: Fraction
    sign: int


def certify_cross_sign(
    numerator_left: object,
    denominator_left: object,
    numerator_right: object,
    denominator_right: object,
) -> CrossSignCertificate:
    """Return the cross-multiplication gap. qrel holds exactly when the gap is zero."""
    left_numerator = require_rational(numerator_left, "left_numerator")
    left_denominator = require_rational(denominator_left, "left_denominator")
    right_numerator = require_rational(numerator_right, "right_numerator")
    right_denominator = require_rational(denominator_right, "right_denominator")
    left_numerator, left_denominator = _normalize_denominator(
        left_numerator, left_denominator, "left_denominator"
    )
    right_numerator, right_denominator = _normalize_denominator(
        right_numerator, right_denominator, "right_denominator"
    )
    gap = left_numerator * right_denominator - left_denominator * right_numerator
    return CrossSignCertificate(
        left_numerator,
        left_denominator,
        right_numerator,
        right_denominator,
        gap,
        _sign(gap),
    )


def cross_sign(
    numerator_left: object,
    denominator_left: object,
    numerator_right: object,
    denominator_right: object,
) -> int:
    """Sign of a/b - c/d from a*d - b*c, with denominators made positive first."""
    return certify_cross_sign(
        numerator_left, denominator_left, numerator_right, denominator_right
    ).sign


def compare(left: object, right: object) -> int:
    """Return -1, 0, or 1 by the sign of left - right."""
    return cross_sign(left, 1, right, 1)


@dataclass(frozen=True)
class SumOfSquaresCertificate:
    """Witness that the returned total is the sum of the recorded rational squares."""

    squares: tuple[Fraction, ...]
    total: Fraction


def certify_sum_of_squares(values: object) -> SumOfSquaresCertificate:
    sequence = _require_sequence(values, "squares")
    squares = tuple(
        require_rational(item, f"squares[{index}]") ** 2 for index, item in enumerate(sequence)
    )
    total = Fraction(0)
    for square in squares:
        total += square
    return SumOfSquaresCertificate(squares, total)


def sum_of_squares(values: object) -> Fraction:
    """Return the sum of rational squares. The total is nonnegative by construction."""
    return certify_sum_of_squares(values).total


def _adjacent_sign(left: Fraction, right: Fraction) -> int:
    return cross_sign(left.numerator, left.denominator, right.numerator, right.denominator)


def _require_adjacent(parsed: Sequence[Fraction]) -> None:
    for index in range(len(parsed) - 1):
        sign = _adjacent_sign(parsed[index], parsed[index + 1])
        if sign > 0:
            raise _refuse("adjacent rationals are not nondecreasing", index=index, sign=sign)


def require_nondecreasing(values: object) -> tuple[Fraction, ...]:
    """Accept the sequence only when each adjacent cross-sign is not positive."""
    sequence = _require_sequence(values, "ordered")
    parsed = tuple(require_rational(item, f"ordered[{index}]") for index, item in enumerate(sequence))
    _require_adjacent(parsed)
    return parsed


def _insert(ordered: list[Fraction], index: int) -> None:
    current = ordered[index]
    slot = index
    while slot > 0 and compare(ordered[slot - 1], current) > 0:
        ordered[slot] = ordered[slot - 1]
        slot -= 1
    ordered[slot] = current


def _insertion_sort(ordered: list[Fraction]) -> None:
    for index in range(1, len(ordered)):
        _insert(ordered, index)


def sorted_fractions(values: object) -> list[Fraction]:
    """Insertion-sort by the exact comparator, then recheck adjacent cross-signs."""
    sequence = _require_sequence(values, "values")
    ordered = [require_rational(item, f"values[{index}]") for index, item in enumerate(sequence)]
    _insertion_sort(ordered)
    _require_adjacent(ordered)
    return ordered


__all__ = [
    "ExactMatrix",
    "GaussianRational",
    "Q",
    "q",
    "OrderError",
    "CrossSignCertificate",
    "SumOfSquaresCertificate",
    "as_fraction",
    "require_rational",
    "compare",
    "certify_cross_sign",
    "cross_sign",
    "certify_sum_of_squares",
    "sum_of_squares",
    "require_nondecreasing",
    "sorted_fractions",
]
