"""Finite witnessed succession, duration classes, and clock adequacy."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Hashable, Mapping

from .cochains import Edge, FiniteComplex, is_closed, solve_potential
from .exact import as_fraction
from .outcomes import Accepted, Outcome, RefusalCode, Refused


@dataclass(frozen=True)
class Occurrence:
    label: Hashable
    index: int

    def __post_init__(self) -> None:
        try:
            hash(self.label)
        except TypeError as exc:
            raise ValueError("occurrence labels must be hashable") from exc
        if type(self.index) is not int or self.index < 0:
            raise ValueError("occurrence indices must be non-negative integers")


def occurrence_chain(labels: tuple[Hashable, ...]) -> tuple[Occurrence, ...]:
    if not labels:
        raise ValueError("an occurrence chain must be nonempty")
    return tuple(Occurrence(label, index) for index, label in enumerate(labels))


def duration_sum(weights: tuple[int | str | Fraction, ...]) -> Outcome[Fraction]:
    try:
        exact = tuple(as_fraction(weight) for weight in weights)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError):
        return Refused(
            RefusalCode.INVALID_INPUT,
            "duration weights must be exact rational scalars",
        )
    if any(weight <= 0 for weight in exact):
        return Refused(RefusalCode.INVALID_INPUT, "duration weights must be strictly positive")
    return Accepted(sum(exact, start=Fraction(0)))


class DurationClass(str, Enum):
    EXACT = "Exact"
    CLOSED_NON_EXACT = "ClosedNonExact"
    ACTIVE_CLOSURE_FAILURE = "ActiveClosureFailure"
    EXACTNESS_UNDETERMINED = "ExactnessUndetermined"


@dataclass(frozen=True)
class DurationClassification:
    kind: DurationClass
    detail: str


def classify_duration(
    complex_: FiniteComplex,
    cochain: Mapping[Edge, int | str | Fraction],
    *,
    exactness_budget: bool = True,
) -> DurationClassification:
    if not is_closed(complex_, cochain):
        return DurationClassification(DurationClass.ACTIVE_CLOSURE_FAILURE, "d1(cochain) is nonzero")
    if not exactness_budget:
        return DurationClassification(DurationClass.EXACTNESS_UNDETERMINED, "exactness check was not admitted")
    potential = solve_potential(complex_, cochain)
    if isinstance(potential, Accepted):
        return DurationClassification(DurationClass.EXACT, "an exact vertex potential was reconstructed")
    return DurationClassification(DurationClass.CLOSED_NON_EXACT, potential.detail)


@dataclass(frozen=True)
class ClockProfile:
    unit: str
    denominator: int
    covered_occurrences: frozenset[int]
    required_occurrences: frozenset[int]
    coupling_verified: bool


def check_clock(profile: ClockProfile) -> Outcome[bool]:
    if (
        not isinstance(profile.unit, str)
        or not profile.unit
        or type(profile.denominator) is not int
        or profile.denominator <= 0
    ):
        return Refused(RefusalCode.INVALID_INPUT, "clock needs a unit and positive denominator")
    occurrence_sets = (profile.covered_occurrences, profile.required_occurrences)
    if any(
        not isinstance(items, frozenset)
        or any(type(item) is not int or item < 0 for item in items)
        for items in occurrence_sets
    ):
        return Refused(
            RefusalCode.INVALID_INPUT,
            "clock occurrence sets must contain non-negative integer indices",
        )
    if type(profile.coupling_verified) is not bool:
        return Refused(RefusalCode.INVALID_INPUT, "clock coupling flag must be boolean")
    if not profile.required_occurrences.issubset(profile.covered_occurrences):
        return Refused(RefusalCode.OUTSIDE_CARRIER, "clock does not cover every required occurrence")
    if not profile.coupling_verified:
        return Refused(RefusalCode.REACCESS_FAILED, "clock coupling was not re-verified")
    return Accepted(True)
# Executable finite evidence; AuthorityEffect: None.
