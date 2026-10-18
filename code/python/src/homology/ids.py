"""Simplex identifiers: dimension plus one distinct integer vertices.

Origin: lean4/H024FourSimplexSpinfoamS4.lean, which states that a 4-simplex
has 5 vertices. That is the dim + 1 vertex count for an abstract simplex.
Claim: urn:omega:fqm:homology:simplex-vertex-count:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_simplex_ids.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: This file does not certify 4-simplex spin admissibility, the
10 triangular faces, or any physical spin-foam amplitude.
"""

from __future__ import annotations

from dataclasses import dataclass

from .errors import DimensionMismatchError


def _fail(invariant: str, **parameters: object) -> DimensionMismatchError:
    return DimensionMismatchError(invariant, parameters)


def _require_dim(dim: object) -> int:
    if isinstance(dim, bool) or not isinstance(dim, int) or dim < 0:
        raise _fail("simplex dimension must be a nonnegative int", received=type(dim).__name__)
    return dim


def _require_vertex(vertex: object, index: int) -> int:
    if isinstance(vertex, float):
        raise _fail("float refused at the public boundary", index=index, received="float")
    if isinstance(vertex, bool) or not isinstance(vertex, int):
        raise _fail("simplex vertices must be ints", index=index, received=type(vertex).__name__)
    return vertex


def _require_vertices(dim: int, vertices: object) -> tuple[int, ...]:
    if isinstance(vertices, (str, bytes)) or not isinstance(vertices, tuple):
        raise _fail("simplex vertices must be a tuple", received=type(vertices).__name__)
    if len(vertices) != dim + 1:
        raise _fail("simplex vertex count must be dim + 1", dim=dim, length=len(vertices))
    parsed = tuple(_require_vertex(vertex, index) for index, vertex in enumerate(vertices))
    if len(set(parsed)) != len(parsed):
        raise _fail("simplex vertices are not distinct", vertices=str(parsed))
    return parsed


@dataclass(frozen=True)
class SimplexId:
    """An abstract simplex. The vertex tuple has length dim + 1 and no repeats."""

    dim: int
    vertices: tuple[int, ...]

    def __post_init__(self) -> None:
        checked_dim = _require_dim(self.dim)
        checked = _require_vertices(checked_dim, self.vertices)
        object.__setattr__(self, "dim", checked_dim)
        object.__setattr__(self, "vertices", checked)


@dataclass(frozen=True)
class ComplexId:
    """A named complex. The name is a nonempty string."""

    name: str

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name:
            raise _fail("complex id requires a nonempty name", received=type(self.name).__name__)


def triangle_simplex_ids() -> tuple[SimplexId, ...]:
    """The three vertices, three edges, and one face of the standard 2-simplex."""
    vertices = tuple(SimplexId(0, (index,)) for index in range(3))
    edges = (SimplexId(1, (0, 1)), SimplexId(1, (0, 2)), SimplexId(1, (1, 2)))
    face = (SimplexId(2, (0, 1, 2)),)
    identified = vertices + edges + face
    if len(identified) != 7:
        raise _fail("triangle census lost a simplex", count=len(identified))
    return identified


__all__ = [
    "ComplexId",
    "SimplexId",
    "triangle_simplex_ids",
]
