"""Bounded exact path enumeration and finite history sums."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .exact import as_fraction
from .outcomes import Accepted, Outcome, RefusalCode, Refused


@dataclass(frozen=True)
class WeightedEdge:
    source: str
    target: str
    weight: Fraction

    def __post_init__(self) -> None:
        if not isinstance(self.source, str) or not self.source:
            raise ValueError("history edge source must be a named vertex")
        if not isinstance(self.target, str) or not self.target:
            raise ValueError("history edge target must be a named vertex")
        object.__setattr__(self, "weight", as_fraction(self.weight))


@dataclass(frozen=True)
class FiniteHistoryGraph:
    vertices: tuple[str, ...]
    edges: tuple[WeightedEdge, ...]

    def __post_init__(self) -> None:
        if type(self.vertices) is not tuple or type(self.edges) is not tuple:
            raise ValueError("history vertices and edges must be immutable tuples")
        if (
            not self.vertices
            or any(not isinstance(vertex, str) or not vertex for vertex in self.vertices)
            or len(set(self.vertices)) != len(self.vertices)
        ):
            raise ValueError("history vertices must be nonempty and unique")
        labels = set(self.vertices)
        pairs: set[tuple[str, str]] = set()
        for edge in self.edges:
            if not isinstance(edge, WeightedEdge):
                raise ValueError("history edges must be WeightedEdge values")
            if edge.source not in labels or edge.target not in labels:
                raise ValueError("history edge leaves the finite carrier")
            pair = (edge.source, edge.target)
            if pair in pairs:
                raise ValueError("parallel history edges need explicit distinct labels")
            pairs.add(pair)

    def adjacency(self) -> dict[str, tuple[WeightedEdge, ...]]:
        result: dict[str, list[WeightedEdge]] = {vertex: [] for vertex in self.vertices}
        for edge in self.edges:
            result[edge.source].append(edge)
        return {vertex: tuple(sorted(edges, key=lambda item: (item.target, item.weight)))
                for vertex, edges in result.items()}


def enumerate_paths(
    graph: FiniteHistoryGraph,
    start: str,
    end: str,
    max_steps: int | None,
) -> Outcome[tuple[tuple[str, ...], ...]]:
    if type(max_steps) is not int or max_steps < 0:
        return Refused(RefusalCode.BUDGET_REQUIRED, "a non-negative finite path budget is required")
    if start not in graph.vertices or end not in graph.vertices:
        return Refused(RefusalCode.OUTSIDE_CARRIER, "path endpoint lies outside the history carrier")
    adjacency = graph.adjacency()
    frontier: list[tuple[str, ...]] = [(start,)]
    found: list[tuple[str, ...]] = []
    for _ in range(max_steps + 1):
        next_frontier: list[tuple[str, ...]] = []
        for path in frontier:
            if path[-1] == end:
                found.append(path)
            if len(path) - 1 < max_steps:
                next_frontier.extend(path + (edge.target,) for edge in adjacency[path[-1]])
        frontier = next_frontier
    return Accepted(tuple(sorted(found, key=lambda path: (len(path), path))))


def path_weight(graph: FiniteHistoryGraph, path: tuple[str, ...]) -> Outcome[Fraction]:
    if not path:
        return Refused(RefusalCode.INVALID_INPUT, "a path must contain at least one vertex")
    if any(vertex not in graph.vertices for vertex in path):
        return Refused(RefusalCode.OUTSIDE_CARRIER, "path contains a vertex outside the history carrier")
    weights = {(edge.source, edge.target): as_fraction(edge.weight) for edge in graph.edges}
    product = Fraction(1)
    for edge in zip(path, path[1:]):
        if edge not in weights:
            return Refused(RefusalCode.MISSING_EDGE, f"path uses missing edge {edge!r}")
        product *= weights[edge]
    return Accepted(product)


def finite_history_sum(
    graph: FiniteHistoryGraph,
    start: str,
    end: str,
    max_steps: int | None,
) -> Outcome[Fraction]:
    paths = enumerate_paths(graph, start, end, max_steps)
    if isinstance(paths, Refused):
        return paths
    total = Fraction(0)
    for path in paths.value:
        weight = path_weight(graph, path)
        # enumerate_paths only emits edges from graph.adjacency, so a missing
        # edge here would be an internal invariant violation rather than a
        # user-facing refusal case.
        assert isinstance(weight, Accepted)
        total += weight.value
    return Accepted(total)


def cancellation_report(terms: tuple[int | str | Fraction, ...]) -> dict[str, object]:
    exact = tuple(as_fraction(term) for term in terms)
    return {
        "aggregate_zero": sum(exact, start=Fraction(0)) == 0,
        "pointwise_zero": all(term == 0 for term in exact),
        "term_count": len(exact),
    }
# Executable finite evidence; AuthorityEffect: None.
