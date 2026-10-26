"""Backward edges of a least-ready order on the C2 diamond.

Origin: lean4/CausalOrder.lean theorem c2_past_common
(C2.rel d0 d1 and C2.rel d0 d2), theorem c2_future_common
(C2.rel d1 d3 and C2.rel d2 d3), theorem c2_causal_0_3
(C2.rel d0 d3), and theorem c2_spacelike_1_2 (d1 and d2 are spacelike).
Claim: urn:omega:fqm:dag:diamond-backward-count:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_dag_witnesses.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 5; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: backward_edge_count returns how many supplied edges point
backward in the least-ready Kahn order of the supplied vertices.
certified_diamond checks the five C2 relations above, checks that 1 and 2
are not ordered, and requires the backward count to be 0. This file does not
prove that C2 is irreflexive or transitive, and it does not claim the Möbius
value on that diamond.
"""

from __future__ import annotations

from typing import Mapping

_VERTICES: tuple[int, ...] = (0, 1, 2, 3)
_EDGES: tuple[tuple[int, int], ...] = ((0, 1), (0, 2), (1, 3), (2, 3), (0, 3))
_ZERO = 0


class DagWitnessError(Exception):
    """One violated diamond-order invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> DagWitnessError:
    return DagWitnessError(invariant, parameters)


def _require_tuple(values: object, role: str) -> tuple[object, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, tuple):
        raise _fail("values are not a tuple", role=role, received=type(values).__name__)
    return tuple(values)


def _require_vertex(value: object, index: int) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the vertex boundary", index=index, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where an integer vertex was required", index=index)
    if type(value) is int:
        return value
    raise _fail("vertex is not an exact integer", index=index, received=type(value).__name__)


def _require_pair(value: object, index: int) -> tuple[int, int]:
    if not isinstance(value, tuple) or len(value) != 2:
        raise _fail("edge is not a pair", index=index, received=type(value).__name__)
    return (_require_vertex(value[0], index), _require_vertex(value[1], index))


def _collect_vertices(values: tuple[object, ...]) -> tuple[int, ...]:
    collected: list[int] = []
    for index, value in enumerate(values):
        collected.append(_require_vertex(value, index))
    return tuple(collected)


def _require_nonempty(vertices: tuple[int, ...]) -> tuple[int, ...]:
    if len(vertices) == 0:
        raise _fail("vertices are empty")
    return vertices


def _require_distinct(vertices: tuple[int, ...]) -> tuple[int, ...]:
    seen: list[int] = []
    for vertex in vertices:
        if vertex in seen:
            raise _fail("vertex is duplicated", vertex=vertex)
        seen.append(vertex)
    return vertices


def _collect_edges(values: tuple[object, ...]) -> tuple[tuple[int, int], ...]:
    collected: list[tuple[int, int]] = []
    for index, value in enumerate(values):
        collected.append(_require_pair(value, index))
    return tuple(collected)


def _indegree(
    vertices: tuple[int, ...],
    edges: tuple[tuple[int, int], ...],
) -> dict[int, int]:
    counts = {vertex: 0 for vertex in vertices}
    for source, target in edges:
        if source not in counts or target not in counts:
            raise _fail("edge leaves the vertex set", source=source, target=target)
        counts[target] += 1
    return counts


def _sources(indegree: dict[int, int]) -> list[int]:
    ready: list[int] = []
    for vertex, degree in indegree.items():
        if degree == 0:
            ready.append(vertex)
    return sorted(ready)


def _release(
    ready: list[int],
    source: int,
    edges: tuple[tuple[int, int], ...],
    indegree: dict[int, int],
) -> None:
    released: list[int] = []
    for origin, target in edges:
        if origin != source:
            continue
        indegree[target] -= 1
        if indegree[target] == 0:
            released.append(target)
    ready.extend(sorted(released))
    ready.sort()


def _kahn(vertices: tuple[int, ...], edges: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    pending = _indegree(vertices, edges)
    ready = _sources(pending)
    order: list[int] = []
    while ready:
        source = ready.pop(0)
        order.append(source)
        _release(ready, source, edges, pending)
    if len(order) != len(vertices):
        raise _fail("the relation has a cycle", visited=len(order), vertices=len(vertices))
    return tuple(order)


def _backward(order: tuple[int, ...], edges: tuple[tuple[int, int], ...]) -> int:
    position = {vertex: index for index, vertex in enumerate(order)}
    count = 0
    for source, target in edges:
        if position[source] >= position[target]:
            count += 1
    return count


def backward_edge_count(edges: object | None = None, vertices: object | None = None) -> int:
    """Return the backward-edge count of a least-ready Kahn order."""
    chosen_vertices = _VERTICES if vertices is None else vertices
    chosen_edges = _EDGES if edges is None else edges
    parsed_vertices = _require_distinct(
        _require_nonempty(_collect_vertices(_require_tuple(chosen_vertices, "vertices")))
    )
    parsed_edges = _collect_edges(_require_tuple(chosen_edges, "edges"))
    return _backward(_kahn(parsed_vertices, parsed_edges), parsed_edges)


def _has_edge(source: int, target: int) -> bool:
    for origin, dest in _EDGES:
        if origin == source and dest == target:
            return True
    return False


def _require_relation(source: int, target: int) -> None:
    if not _has_edge(source, target):
        raise _fail("a C2 relation is missing", source=source, target=target)


def _require_spacelike(left: int, right: int) -> None:
    if _has_edge(left, right) or _has_edge(right, left):
        raise _fail("a spacelike pair is ordered", left=left, right=right)


def certified_diamond() -> int:
    """Backward count of the C2 diamond. It must be 0."""
    count = backward_edge_count()
    if count != _ZERO:
        raise _fail("certified diamond has a backward edge", count=count)
    _require_relation(0, 1)
    _require_relation(0, 2)
    _require_relation(1, 3)
    _require_relation(2, 3)
    _require_relation(0, 3)
    _require_spacelike(1, 2)
    return count


def main() -> int:
    value = certified_diamond()
    print(value)
    if value == _ZERO:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
