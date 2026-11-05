"""Owned finite rational Cech complex with replayable quotient-norm witnesses.

AuthorityEffect: None. Uses a bounded binary scenario; each cochain degree has
at most4096 coordinates. No assertion about probabilistic contextuality follows.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations
from typing import cast

from .boundary import Violation, evaluate, require
from .domains import integer, rational, sequence
from .measurement_scenario import Context, Distribution, MeasurementScenario, cochain, sections
from .outcome import Outcome

Edge = tuple[int, int]
Triangle = tuple[int, int, int]
EdgeValues = dict[Edge, tuple[Q, ...]]


@dataclass(frozen=True, slots=True, init=False)
class CechComplex:
    """Orientation i<j<k, with delta0=restriction(i)-restriction(j)."""
    scenario: MeasurementScenario
    edges: tuple[Edge, ...]
    triangles: tuple[Triangle, ...]

    def __init__(self, scenario: object) -> None:
        if type(scenario) is not MeasurementScenario:
            raise Violation("input", "measurement scenario required")
        edges = tuple(pair for pair in combinations(range(len(scenario.contexts)), 2)
                      if set(scenario.contexts[pair[0]]) & set(scenario.contexts[pair[1]]))
        triangles = tuple(triple for triple in combinations(range(len(scenario.contexts)), 3)
                          if set(scenario.contexts[triple[0]]) & set(scenario.contexts[triple[1]]) & set(scenario.contexts[triple[2]]))
        object.__setattr__(self, "scenario", scenario)
        object.__setattr__(self, "edges", edges)
        object.__setattr__(self, "triangles", triangles)
        for simplices in (tuple((i,) for i in range(len(scenario.contexts))), edges, triangles):
            integer(sum(1 << len(self._overlap(simplex)) for simplex in simplices), "cochain coordinates", 0, 4096)

    def _overlap(self, simplex: tuple[int, ...]) -> Context:
        shared = set(self.scenario.contexts[simplex[0]])
        for index in simplex[1:]:
            shared.intersection_update(self.scenario.contexts[index])
        return tuple(sorted(shared))

    def _zero(self, values: object) -> tuple[Distribution, ...]:
        tables = sequence(values, "zero cochain", len(self.scenario.contexts), 16)
        rows = tuple(cochain(table, len(context)) for table, context in zip(tables, self.scenario.contexts))
        return tuple(dict(zip(sections(len(context)), row)) for context, row in zip(self.scenario.contexts, rows))

    def _one(self, values: object) -> EdgeValues:
        if type(values) is not dict:
            raise Violation("input", "one cochain must be a dictionary")
        mapping = cast(dict[object, object], values)
        if len(mapping) > 120:
            raise Violation("resource", "one cochain exceeds120 edges")
        for key in mapping:
            if type(key) is not tuple:
                raise Violation("input", "one-cochain keys must be edge tuples")
            for index in sequence(key, "edge", 2, 2):
                integer(index, "edge index", 0)
        if set(mapping) != set(self.edges):
            raise Violation("input", "one cochain must have exactly the nerve edges")
        return {edge: tuple(rational(value, "one-cochain weight") for value in sequence(mapping[edge], "edge vector", 1 << len(self._overlap(edge)), 64)) for edge in self.edges}

    def _delta0(self, values: object) -> EdgeValues:
        zero = self._zero(values)
        result = {}
        for edge in self.edges:
            i, j = edge
            overlap = self._overlap(edge)
            first = self.scenario._marginal(zero[i], self.scenario.contexts[i], overlap)
            second = self.scenario._marginal(zero[j], self.scenario.contexts[j], overlap)
            result[edge] = tuple(rational(first[key]-second[key], "coboundary difference") for key in sections(len(overlap)))
        return result

    def delta0(self, values: object) -> Outcome[EdgeValues]:
        return evaluate(self._delta0, values)

    def _edge_restriction(self, values: EdgeValues, edge: Edge, target: Context) -> Distribution:
        parent = self._overlap(edge)
        return self.scenario._marginal(dict(zip(sections(len(parent)), values[edge])), parent, target)

    def _delta1(self, values: object) -> dict[Triangle, tuple[Q, ...]]:
        one = self._one(values)
        result = {}
        for triangle in self.triangles:
            i, j, k = triangle
            overlap = self._overlap(triangle)
            first = self._edge_restriction(one, (j, k), overlap)
            second = self._edge_restriction(one, (i, k), overlap)
            third = self._edge_restriction(one, (i, j), overlap)
            result[triangle] = tuple(rational(rational(first[key]-second[key])+third[key]) for key in sections(len(overlap)))
        return result

    def delta1(self, values: object) -> Outcome[dict[Triangle, tuple[Q, ...]]]:
        return evaluate(self._delta1, values)

    def _pairing(self, left: EdgeValues, right: EdgeValues) -> Q:
        total = Q(0)
        for edge in self.edges:
            for a, b in zip(left[edge], right[edge]):
                total = rational(total+rational(a*b), "cochain pairing sum")
        return total

    def _annihilates(self, dual: EdgeValues) -> bool:
        for index, context in enumerate(self.scenario.contexts):
            for local in sections(len(context)):
                total = Q(0)
                for edge in self.edges:
                    if index in edge:
                        overlap = self._overlap(edge)
                        key = tuple(local[context.index(position)] for position in overlap)
                        offset = sections(len(overlap)).index(key)
                        sign = 1 if index == edge[0] else -1
                        total = rational(total+sign*dual[edge][offset], "dual coboundary coefficient")
                if total != 0:
                    return False
        return True

    def _quotient_value(self, omega: object, alpha: object, phi: object) -> Q:
        cochain_value, zero, dual = self._one(omega), self._zero(alpha), self._one(phi)
        require(all(abs(value) <= 1 for vector in dual.values() for value in vector), "quotient dual sup norm exceeds1")
        require(self._annihilates(dual), "quotient dual does not annihilate coboundaries")
        image = self._delta0(zero)
        upper = Q(0)
        for edge in self.edges:
            for value, shift in zip(cochain_value[edge], image[edge]):
                upper = rational(upper+abs(rational(value-shift)), "quotient residual norm")
        lower = self._pairing(dual, cochain_value)
        require(lower == upper, "quotient primal and dual bounds disagree")
        return upper

    def quotient_value(self, omega: object, alpha: object, phi: object) -> Outcome[Q]:
        return evaluate(self._quotient_value, omega, alpha, phi)
