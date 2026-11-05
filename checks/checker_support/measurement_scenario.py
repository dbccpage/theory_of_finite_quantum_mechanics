"""Owned finite binary measurement covers and exact signed marginalization.

AuthorityEffect: None. At most6 measurements,16 contexts and4096 incidence
entries. Query subsets retain their declared coordinate order.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
from typing import cast

from .boundary import Violation, evaluate
from .domains import integer, rational, sequence
from .outcome import Outcome

Assignment = tuple[int, ...]
Context = tuple[int, ...]
Distribution = dict[Assignment, Q]


def assignment(value: object, size: int) -> Assignment:
    values = tuple(integer(entry, "binary outcome", 0) for entry in sequence(value, "assignment", size, 6))
    if any(entry > 1 for entry in values):
        raise Violation("input", "binary outcomes must be0 or1")
    return values


def sections(size: int) -> tuple[Assignment, ...]:
    count = integer(size, "section arity", 0, 6)
    return tuple(product((0, 1), repeat=count))


def cochain(value: object, size: int) -> tuple[Q, ...]:
    if type(value) is not dict:
        raise Violation("input", "cochain must be a dictionary")
    mapping = cast(dict[object, object], value)
    if len(mapping) > 64:
        raise Violation("resource", "cochain exceeds64 entries")
    for key in mapping:
        if type(key) is not tuple:
            raise Violation("input", "cochain keys must be assignment tuples")
        assignment(key, size)
    keys = sections(size)
    if set(mapping) != set(keys):
        raise Violation("input", "cochain must contain exactly every local assignment")
    return tuple(rational(mapping[key], "cochain weight") for key in keys)


@dataclass(frozen=True, slots=True, init=False)
class MeasurementScenario:
    """Owns an ordered family of distinct nonempty increasing contexts covering M."""
    n: int
    contexts: tuple[Context, ...]

    def __init__(self, n: object, contexts: object) -> None:
        size = integer(n, "measurement count", 1, 6)
        outer = sequence(contexts, "contexts", maximum=16)
        owned = tuple(self._admit_positions(context, size) for context in outer)
        if not owned or any(not context for context in owned):
            raise Violation("input", "measurement cover and contexts must be nonempty")
        if any(context != tuple(sorted(context)) for context in owned):
            raise Violation("input", "scenario contexts must be increasing")
        if len(set(owned)) != len(owned):
            raise Violation("duplicate", "scenario contexts must be distinct")
        if set(position for context in owned for position in context) != set(range(size)):
            raise Violation("input", "scenario contexts must cover every measurement")
        object.__setattr__(self, "n", size)
        object.__setattr__(self, "contexts", owned)

    @staticmethod
    def _admit_positions(value: object, size: int) -> Context:
        positions = tuple(integer(entry, "measurement index", 0) for entry in sequence(value, "positions", maximum=6))
        if any(index >= size for index in positions):
            raise Violation("input", "measurement index outside carrier")
        if len(set(positions)) != len(positions):
            raise Violation("duplicate", "measurement positions must be distinct")
        return positions

    @property
    def globals(self) -> tuple[Assignment, ...]:
        return sections(self.n)

    def _positions(self, value: object) -> Context:
        return self._admit_positions(value, self.n)

    def _sections(self, positions: object) -> tuple[Assignment, ...]:
        return sections(len(self._positions(positions)))

    def sections(self, positions: object) -> Outcome[tuple[Assignment, ...]]:
        return evaluate(self._sections, positions)

    def _restrict(self, value: object, positions: object) -> Assignment:
        full, subset = assignment(value, self.n), self._positions(positions)
        return tuple(full[index] for index in subset)

    def restrict(self, value: object, positions: object) -> Outcome[Assignment]:
        return evaluate(self._restrict, value, positions)

    def rows(self) -> tuple[tuple[int, Assignment], ...]:
        return tuple((index, value) for index, context in enumerate(self.contexts) for value in sections(len(context)))

    def _incidence(self) -> tuple[tuple[Q, ...], ...]:
        count = sum(1 << len(context) for context in self.contexts)
        integer(count*(1 << self.n), "incidence entries", 0, 4096)
        assignments = self.globals
        return tuple(tuple(Q(int(tuple(g[index] for index in self.contexts[k]) == value)) for g in assignments)
                     for k, value in self.rows())

    def incidence(self) -> Outcome[tuple[tuple[Q, ...], ...]]:
        return evaluate(self._incidence)

    def _marginal(self, values: object, positions: object, subset: object) -> Distribution:
        parent, child = self._positions(positions), self._positions(subset)
        if not set(child) <= set(parent):
            raise Violation("input", "marginal target must be contained in its parent")
        weights = cochain(values, len(parent))
        indices = tuple(parent.index(index) for index in child)
        result = {key: Q(0) for key in sections(len(child))}
        for key, weight in zip(sections(len(parent)), weights):
            restricted = tuple(key[index] for index in indices)
            result[restricted] = rational(result[restricted]+weight, "marginal sum")
        return result

    def marginal(self, values: object, positions: object, subset: object) -> Outcome[Distribution]:
        return evaluate(self._marginal, values, positions, subset)
