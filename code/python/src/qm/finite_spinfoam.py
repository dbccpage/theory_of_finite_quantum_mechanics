"""Euler characteristic of a labeled tetrahedron boundary.

Origin: lean4/Simplicial3complexCayleyEvolution.lean theorem
tetrahedron_euler_characteristic ((4 : Int) - 6 + 4 = 2).
Claim: urn:omega:fqm:spinfoam:tetrahedron-euler:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_finite_spinfoam.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: tetrahedron_euler counts the edges and triangular faces of four
distinct integer vertices and returns V - E + F after those counts are 4, 6,
and 4. certified_euler checks the labels (0, 1, 2, 3). The cited theorem is
the integer arithmetic 4 - 6 + 4 = 2. This file does not prove boundary
nilpotence, the octahedron, or the Cayley isometry in that Lean file.
"""

from __future__ import annotations

from itertools import combinations
from typing import Mapping

_WIDTH = 4
_CHI = 2
_FIXTURE: tuple[object, ...] = (0, 1, 2, 3)


class SpinfoamError(Exception):
    """One violated tetrahedron-count invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> SpinfoamError:
    return SpinfoamError(invariant, parameters)


def _require_tuple(vertices: object) -> tuple[object, ...]:
    if isinstance(vertices, (str, bytes)) or not isinstance(vertices, tuple):
        raise _fail("tetrahedron vertices are not a tuple", received=type(vertices).__name__)
    return tuple(vertices)


def _require_label(value: object, index: int) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the vertex boundary", index=index, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where an integer vertex was required", index=index)
    if type(value) is int:
        if value.bit_length() > 1024:
            raise _fail("integer exceeds 1024 bits", index=index)
        return value
    raise _fail(
        "tetrahedron vertex is not an exact integer",
        index=index,
        received=type(value).__name__,
    )


def _collect(vertices: tuple[object, ...]) -> tuple[int, ...]:
    collected: list[int] = []
    for index, value in enumerate(vertices):
        collected.append(_require_label(value, index))
    return tuple(collected)


def _require_four(vertices: tuple[int, ...]) -> tuple[int, ...]:
    if len(vertices) != _WIDTH:
        raise _fail("tetrahedron vertices are not four", length=len(vertices))
    return vertices


def _require_distinct(vertices: tuple[int, ...]) -> tuple[int, ...]:
    seen: list[int] = []
    for vertex in vertices:
        if vertex in seen:
            raise _fail("tetrahedron vertex is duplicated", vertex=vertex)
        seen.append(vertex)
    return vertices


def _pairs(vertices: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    pairs: list[tuple[int, int]] = []
    for pair in combinations(vertices, 2):
        pairs.append((pair[0], pair[1]))
    return tuple(pairs)


def _triples(vertices: tuple[int, ...]) -> tuple[tuple[int, int, int], ...]:
    triples: list[tuple[int, int, int]] = []
    for triple in combinations(vertices, 3):
        triples.append((triple[0], triple[1], triple[2]))
    return tuple(triples)


def _require_covered(
    edges: tuple[tuple[int, int], ...],
    faces: tuple[tuple[int, int, int], ...],
) -> None:
    for face in faces:
        first = (face[0], face[1])
        second = (face[0], face[2])
        third = (face[1], face[2])
        if first not in edges or second not in edges or third not in edges:
            raise _fail("a face uses an edge that was not counted", face=str(face))


def _require_counts(vertex_count: int, edge_count: int, face_count: int) -> None:
    if vertex_count != _WIDTH:
        raise _fail("vertex count is not four", count=vertex_count)
    if edge_count != 6:
        raise _fail("edge count is not six", count=edge_count)
    if face_count != _WIDTH:
        raise _fail("face count is not four", count=face_count)


def _characteristic(vertex_count: int, edge_count: int, face_count: int) -> int:
    return vertex_count - edge_count + face_count


def tetrahedron_euler(vertices: object) -> int:
    """Return V - E + F for four distinct integer vertices."""
    checked = _require_distinct(_require_four(_collect(_require_tuple(vertices))))
    edges = _pairs(checked)
    faces = _triples(checked)
    _require_covered(edges, faces)
    _require_counts(len(checked), len(edges), len(faces))
    return _characteristic(len(checked), len(edges), len(faces))


def certified_euler() -> int:
    """Euler characteristic of the labels (0, 1, 2, 3). It must be 2."""
    value = tetrahedron_euler(_FIXTURE)
    if value != _CHI:
        raise _fail("certified Euler characteristic is not two", characteristic=value)
    return value


def main() -> int:
    value = certified_euler()
    print(value)
    if value == _CHI:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
