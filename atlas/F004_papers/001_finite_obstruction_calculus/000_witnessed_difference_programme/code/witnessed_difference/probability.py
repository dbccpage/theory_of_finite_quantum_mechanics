"""Finite witness multiplicity; no chance or Born-rule interpretation."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from typing import Hashable

from .outcomes import Accepted, Outcome, RefusalCode, Refused


@dataclass(frozen=True)
class FiniteWitnessSpace:
    occurrences: tuple[Hashable, ...]

    @property
    def multiplicities(self) -> dict[Hashable, int]:
        return dict(Counter(self.occurrences))


def event_probability(
    space: FiniteWitnessSpace,
    event: frozenset[Hashable],
) -> Outcome[Fraction]:
    if not space.occurrences:
        return Refused(RefusalCode.EMPTY_SPACE, "finite normalization needs at least one occurrence")
    support = set(space.occurrences)
    if not event.issubset(support):
        return Refused(RefusalCode.EVENT_OUTSIDE_SPACE, "event names an outcome outside the finite support")
    hits = sum(1 for outcome in space.occurrences if outcome in event)
    return Accepted(Fraction(hits, len(space.occurrences)))


def disjoint_additivity(
    space: FiniteWitnessSpace,
    left: frozenset[Hashable],
    right: frozenset[Hashable],
) -> Outcome[bool]:
    if left.intersection(right):
        return Refused(RefusalCode.NOT_DISJOINT, "events overlap")
    p_left = event_probability(space, left)
    p_right = event_probability(space, right)
    p_union = event_probability(space, left.union(right))
    if isinstance(p_left, Refused):
        return p_left
    if isinstance(p_right, Refused):
        return p_right
    if isinstance(p_union, Refused):
        return p_union
    return Accepted(p_union.value == p_left.value + p_right.value)


def conditional_probability(
    space: FiniteWitnessSpace,
    event: frozenset[Hashable],
    condition: frozenset[Hashable],
) -> Outcome[Fraction]:
    event_result = event_probability(space, event)
    if isinstance(event_result, Refused):
        return event_result
    condition_probability = event_probability(space, condition)
    if isinstance(condition_probability, Refused):
        return condition_probability
    if condition_probability.value == 0:
        return Refused(RefusalCode.EMPTY_SPACE, "conditioning event has zero finite multiplicity")
    intersection = event_probability(space, event.intersection(condition))
    assert isinstance(intersection, Accepted)
    return Accepted(intersection.value / condition_probability.value)
# Executable finite evidence; AuthorityEffect: None.
