"""Bounded exact cotree polynomials and the supplied five-edge graph.

AuthorityEffect: None. Edge positions distinguish parallel edges and loops.
No QED coefficients, fine-structure constant or continuum interval is derived.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path as _Path
import sys as _sys

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import integer, sequence
from checker_support.outcome import Outcome

Edge = tuple[int, int]
EDGES: tuple[Edge, ...] = ((0, 1), (0, 2), (1, 3), (2, 3), (1, 2))
WEIGHTS = (2, 3, 5, 7, 11)
TREES = (7, 11, 13, 14, 21, 22, 25, 26)


def _bounded(value: object) -> int:
    exact = integer(value, "integer weight or intermediate")
    if exact.bit_length() > 4096:
        raise Violation("resource", "cotree integer exceeds4096 bits")
    return exact


def _vertex(value: object, count: int) -> int:
    vertex = integer(value, "vertex", 0)
    if vertex >= count:
        raise Violation("input", "edge endpoint outside vertex carrier")
    return vertex


def _edge(value: object, count: int) -> Edge:
    first, second = sequence(value, "edge", 2)
    return _vertex(first, count), _vertex(second, count)


@dataclass(frozen=True, slots=True, init=False)
class CotreeGraph:
    """Owned indexed multigraph:1..16 vertices,0..12 edges, signed integer weights."""
    vertex_count: int
    edges: tuple[Edge, ...]

    def __init__(self, vertex_count: object, edges: object) -> None:
        count = integer(vertex_count, "vertex count", 1, 16)
        owned = tuple(_edge(edge, count) for edge in sequence(edges, "edges", maximum=12))
        object.__setattr__(self, "vertex_count", count)
        object.__setattr__(self, "edges", owned)

    def _mask(self, value: object) -> int:
        mask = integer(value, "edge mask", 0)
        if mask >= 1 << len(self.edges):
            raise Violation("input", "mask contains absent edge bits")
        return mask

    def _weights(self, values: object) -> tuple[int, ...]:
        return tuple(_bounded(value) for value in sequence(values, "weights", len(self.edges), 12))

    def _components(self, mask: int) -> int:
        labels = list(range(self.vertex_count))
        for index, (first, second) in enumerate(self.edges):
            if mask & (1 << index):
                before, after = labels[second], labels[first]
                labels = [after if label == before else label for label in labels]
        return len(set(labels))

    def components(self, mask: object) -> Outcome[int]:
        return evaluate(lambda: self._components(self._mask(mask)))

    def _trees(self) -> tuple[int, ...]:
        return tuple(mask for mask in range(1 << len(self.edges))
                     if mask.bit_count() == self.vertex_count-1 and self._components(mask) == 1)

    def tree_masks(self) -> Outcome[tuple[int, ...]]:
        return evaluate(self._trees)

    def _product(self, mask: int, weights: tuple[int, ...]) -> int:
        value = 1
        for index, weight in enumerate(weights):
            if mask & (1 << index) == 0:
                value = _bounded(value*weight)
        return value

    def _cotree_product(self, mask: object, weights: object) -> int:
        admitted = self._mask(mask)
        return self._product(admitted, self._weights(weights))

    def cotree_product(self, mask: object, weights: object) -> Outcome[int]:
        return evaluate(self._cotree_product, mask, weights)

    def _cotree_sum(self, weights: object) -> int:
        owned = self._weights(weights)
        total = 0
        for mask in self._trees():
            total = _bounded(total+self._product(mask, owned))
        return total

    def cotree_sum(self, weights: object) -> Outcome[int]:
        return evaluate(self._cotree_sum, weights)


def run(mask: object) -> int:
    graph = CotreeGraph(4, EDGES)
    return graph._components(graph._mask(mask))


def prod(mask: object, weights: object) -> int:
    return CotreeGraph(4, EDGES)._cotree_product(mask, weights)


def verify(cases: Cases) -> None:
    if type(cases) is not Cases:
        raise Violation("input", "Cases recorder required")
    graph = CotreeGraph(4, EDGES)
    listed = tuple(mask for mask in range(32) if mask.bit_count() == 3)
    cases.require(listed == (7, 11, 13, 14, 19, 21, 22, 25, 26, 28), "three-edge census")
    for mask in listed:
        cases.require(run(mask) == (1 if mask in TREES else 2), "component count")
    cases.require(graph._trees() == TREES, "spanning-tree census")
    for mask, expected in zip(TREES, (77, 55, 33, 22, 21, 14, 15, 10)):
        cases.require(prod(mask, WEIGHTS) == expected, "individual cotree monomial")
    cases.require(graph._cotree_sum(WEIGHTS) == 247, "weighted cotree sum")
    cases.require(graph._cotree_sum((1,)*5) == 8, "unit cotree sum")


def main() -> None:
    cases = Cases()
    verify(cases)
    print(json.dumps({"status": "passed", "checks": cases.checks, "trees": TREES,
                      "cotree_sum": 247, "unit_sum": 8, "scope": "supplied graph; no QED interval"}))


if __name__ == "__main__":
    raise SystemExit(cli(main))
