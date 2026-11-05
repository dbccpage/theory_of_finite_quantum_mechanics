"""Owned binary empirical distributions and finite support-descent queries.

AuthorityEffect: None. Signalling is allowed; each local row is an exact
nonnegative distribution. Matching covers have at most4096 candidate families.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product

from .boundary import Violation, evaluate
from .domains import integer, rational, sequence
from .measurement_scenario import Assignment, Context, Distribution, MeasurementScenario, cochain, sections
from .outcome import Outcome


def _mass(values: tuple[Q, ...]) -> Q:
    total = Q(0)
    for value in values:
        total = rational(total+value, "probability mass sum")
    return total


def _joined(contexts: tuple[Context, ...], choices: tuple[Assignment, ...], size: int) -> Assignment | None:
    values: dict[int, int] = {}
    for context, assignment in zip(contexts, choices):
        for index, value in zip(context, assignment):
            if index in values and values[index] != value:
                return None
            values[index] = value
    return tuple(values[index] for index in range(size))


@dataclass(frozen=True, slots=True, init=False)
class EmpiricalModel:
    """Owns a scenario and canonical local probability rows, without assuming gluing."""
    scenario: MeasurementScenario
    weights: tuple[tuple[Q, ...], ...]

    def __init__(self, scenario: object, distributions: object) -> None:
        if type(scenario) is not MeasurementScenario:
            raise Violation("input", "measurement scenario required")
        tables = sequence(distributions, "empirical distributions", len(scenario.contexts), 16)
        rows = tuple(cochain(table, len(context)) for table, context in zip(tables, scenario.contexts))
        for row in rows:
            if any(value < 0 for value in row) or _mass(row) != 1:
                raise Violation("input", "each empirical row must be a nonnegative distribution of mass1")
        object.__setattr__(self, "scenario", scenario)
        object.__setattr__(self, "weights", rows)

    def distributions(self) -> tuple[Distribution, ...]:
        return tuple(dict(zip(sections(len(context)), row)) for context, row in zip(self.scenario.contexts, self.weights))

    def stacked(self) -> tuple[Q, ...]:
        return tuple(value for row in self.weights for value in row)

    def _supports(self) -> tuple[frozenset[Assignment], ...]:
        return tuple(frozenset(key for key, value in zip(sections(len(context)), row) if value > 0)
                     for context, row in zip(self.scenario.contexts, self.weights))

    def _support_globals(self) -> tuple[Assignment, ...]:
        supports = self._supports()
        return tuple(g for g in self.scenario.globals
                     if all(tuple(g[index] for index in context) in support for context, support in zip(self.scenario.contexts, supports)))

    def support_globals(self) -> Outcome[tuple[Assignment, ...]]:
        return evaluate(self._support_globals)

    def _mixture(self, other: object) -> EmpiricalModel:
        if type(other) is not EmpiricalModel or other.scenario != self.scenario:
            raise Violation("input", "mixture requires the identical measurement scenario")
        rows = tuple(tuple(rational(rational(a+b, "mixture sum")/2, "mixture weight") for a, b in zip(left, right))
                     for left, right in zip(self.weights, other.weights))
        tables = tuple(dict(zip(sections(len(context)), row)) for context, row in zip(self.scenario.contexts, rows))
        return EmpiricalModel(self.scenario, tables)

    def mixture(self, other: object) -> Outcome[EmpiricalModel]:
        return evaluate(self._mixture, other)

    def _cover(self, cover: object) -> tuple[Context, ...]:
        contexts = tuple(self.scenario._positions(context) for context in sequence(cover, "matching cover", maximum=16))
        if not contexts or any(not context for context in contexts):
            raise Violation("input", "matching cover must have nonempty patches")
        if len({frozenset(context) for context in contexts}) != len(contexts):
            raise Violation("duplicate", "matching cover patches must be distinct")
        if set(index for context in contexts for index in context) != set(range(self.scenario.n)):
            raise Violation("input", "matching cover must cover every measurement")
        return contexts

    def _admissible(self, context: Context, supports: tuple[frozenset[Assignment], ...]) -> tuple[Assignment, ...]:
        inside = tuple((tuple(context.index(index) for index in original), support)
                       for original, support in zip(self.scenario.contexts, supports) if set(original) <= set(context))
        return tuple(value for value in sections(len(context))
                     if all(tuple(value[index] for index in indices) in support for indices, support in inside))

    def _matching_families(self, cover: object) -> tuple[int, int, int, int]:
        contexts = self._cover(cover)
        supports = self._supports()
        local = tuple(self._admissible(context, supports) for context in contexts)
        if any(not choices for choices in local):
            return 0, 0, 0, 0
        count = 1
        for choices in local:
            count = integer(count*len(choices), "matching family candidates", 0, 4096)
        global_support = frozenset(self._support_globals())
        families = unique = 0
        for choices in product(*local):
            joined = _joined(contexts, choices, self.scenario.n)
            if joined is not None:
                families += 1
                unique += int(joined in global_support)
        return families, unique, 0, families-unique

    def matching_families(self, cover: object) -> Outcome[tuple[int, int, int, int]]:
        return evaluate(self._matching_families, cover)
