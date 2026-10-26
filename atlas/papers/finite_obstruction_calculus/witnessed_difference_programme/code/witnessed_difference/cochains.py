"""Exact finite graph and 2-complex cochain operations."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from typing import Hashable, Mapping

from .exact import as_fraction, l1
from .outcomes import Accepted, Outcome, RefusalCode, Refused

Vertex = Hashable
Edge = tuple[Vertex, Vertex]
Face = tuple[Vertex, Vertex, Vertex]


@dataclass(frozen=True)
class FiniteComplex:
    vertices: tuple[Vertex, ...]
    edges: tuple[Edge, ...]
    faces: tuple[Face, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "vertices", tuple(self.vertices))
        object.__setattr__(self, "edges", tuple(tuple(edge) for edge in self.edges))
        object.__setattr__(self, "faces", tuple(tuple(face) for face in self.faces))
        if len({frozenset(face) for face in self.faces}) != len(self.faces):
            raise ValueError("duplicate or reoriented duplicate faces require distinct cell identifiers")
        labels = set(self.vertices)
        if len(labels) != len(self.vertices):
            raise ValueError("vertices must be unique")
        if any(u == v or u not in labels or v not in labels for u, v in self.edges):
            raise ValueError("each edge needs distinct endpoints in the carrier")
        undirected = {frozenset(edge) for edge in self.edges}
        if len(undirected) != len(self.edges):
            raise ValueError("duplicate or reverse-duplicate edges are not allowed")
        for face in self.faces:
            if len(set(face)) != 3 or any(vertex not in labels for vertex in face):
                raise ValueError("faces need three distinct carrier vertices")
            a, b, c = face
            if not all(frozenset(edge) in undirected for edge in ((a, b), (b, c), (a, c))):
                raise ValueError("each face boundary edge must be present")


def d0(complex_: FiniteComplex, potential: Mapping[Vertex, int | str | Fraction]) -> dict[Edge, Fraction]:
    if set(potential) != set(complex_.vertices):
        raise ValueError("potential must define every vertex exactly once")
    return {(u, v): as_fraction(potential[v]) - as_fraction(potential[u]) for u, v in complex_.edges}


def _edge_value(values: Mapping[Edge, int | str | Fraction], u: Vertex, v: Vertex) -> Fraction:
    if (u, v) in values:
        return as_fraction(values[(u, v)])
    if (v, u) in values:
        return -as_fraction(values[(v, u)])
    raise ValueError(f"missing cochain value for edge {u!r}-{v!r}")


def d1(complex_: FiniteComplex, cochain: Mapping[Edge, int | str | Fraction]) -> dict[Face, Fraction]:
    _validate_cochain(complex_, cochain)
    return {
        (a, b, c): _edge_value(cochain, a, b)
        + _edge_value(cochain, b, c)
        - _edge_value(cochain, a, c)
        for a, b, c in complex_.faces
    }


def _validate_cochain(complex_: FiniteComplex, cochain: Mapping[Edge, object]) -> None:
    admitted = {frozenset(edge) for edge in complex_.edges}
    supplied: set[frozenset[Vertex]] = set()
    for edge in cochain:
        if not isinstance(edge, tuple) or len(edge) != 2:
            raise ValueError("cochain keys must be oriented edge pairs")
        undirected = frozenset(edge)
        if len(undirected) != 2 or undirected not in admitted or undirected in supplied:
            raise ValueError("cochain must define one orientation of every admitted edge exactly once")
        supplied.add(undirected)
    if supplied != admitted or len(cochain) != len(admitted):
        raise ValueError("cochain must define every admitted edge exactly once")


def is_closed(complex_: FiniteComplex, cochain: Mapping[Edge, int | str | Fraction]) -> bool:
    return all(value == 0 for value in d1(complex_, cochain).values())


def solve_potential(
    complex_: FiniteComplex,
    cochain: Mapping[Edge, int | str | Fraction],
) -> Outcome[dict[Vertex, Fraction]]:
    """Solve d0(phi)=cochain componentwise, returning a cycle counter-witness."""

    _validate_cochain(complex_, cochain)
    adjacency: dict[Vertex, list[tuple[Vertex, Fraction]]] = {v: [] for v in complex_.vertices}
    for u, v in complex_.edges:
        value = _edge_value(cochain, u, v)
        adjacency[u].append((v, value))
        adjacency[v].append((u, -value))
    potential: dict[Vertex, Fraction] = {}
    for root in complex_.vertices:
        if root in potential:
            continue
        potential[root] = Fraction(0)
        queue: deque[Vertex] = deque([root])
        while queue:
            source = queue.popleft()
            for target, increment in adjacency[source]:
                expected = potential[source] + increment
                if target not in potential:
                    potential[target] = expected
                    queue.append(target)
                elif potential[target] != expected:
                    return Refused(
                        RefusalCode.NOT_EXACT,
                        f"cycle inconsistency at {source!r}->{target!r}: "
                        f"expected {expected}, found {potential[target]}",
                    )
    return Accepted(potential)


def cochain_l1(complex_: FiniteComplex, cochain: Mapping[Edge, int | str | Fraction]) -> Fraction:
    _validate_cochain(complex_, cochain)
    return l1(_edge_value(cochain, *edge) for edge in complex_.edges)


def finite_quotient_l1(
    complex_: FiniteComplex,
    cochain: Mapping[Edge, int | str | Fraction],
    candidate_potentials: tuple[Mapping[Vertex, int | str | Fraction], ...],
) -> Outcome[tuple[Fraction, dict[Vertex, Fraction]]]:
    """Minimize ||cochain-d0(phi)||_1 over an explicit finite candidate set."""

    if not candidate_potentials:
        return Refused(RefusalCode.BUDGET_REQUIRED, "a nonempty finite candidate set is required")
    _validate_cochain(complex_, cochain)
    scored: list[tuple[Fraction, tuple[Fraction, ...], dict[Vertex, Fraction]]] = []
    for candidate in candidate_potentials:
        normalized = {vertex: as_fraction(value) for vertex, value in candidate.items()}
        coboundary = d0(complex_, normalized)
        residual = {
            edge: _edge_value(cochain, *edge) - _edge_value(coboundary, *edge)
            for edge in complex_.edges
        }
        key = tuple(normalized[vertex] for vertex in complex_.vertices)
        scored.append((cochain_l1(complex_, residual), key, normalized))
    mass, _, witness = min(scored, key=lambda item: (item[0], item[1]))
    return Accepted((mass, witness))
# Executable finite evidence; AuthorityEffect: None.
