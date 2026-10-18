"""Identifier types for chain complexes, simplices, and homology carriers.

Origin: code/python/src/homology/ids.py
Claim: a simplex identifier has exactly dim + 1 distinct vertices.
AuthorityEffect: None.
"""
from dataclasses import dataclass
from typing import Tuple

from .errors import DimensionMismatchError


def _check_vertices(dim: int, vertices: Tuple[int, ...]) -> None:
    if isinstance(dim, bool) or not isinstance(dim, int) or dim < 0:
        raise DimensionMismatchError(f"simplex dimension must be a nonnegative int, got {dim!r}")
    if len(vertices) != dim + 1:
        raise DimensionMismatchError(f"simplex of dimension {dim} needs {dim + 1} vertices, got {len(vertices)}")
    if any(isinstance(vertex, bool) or not isinstance(vertex, int) for vertex in vertices):
        raise DimensionMismatchError("simplex vertices must be ints")
    if len(set(vertices)) != len(vertices):
        raise DimensionMismatchError(f"simplex vertices are not distinct: {vertices}")


@dataclass(frozen=True)
class SimplexId:
    dim: int
    vertices: Tuple[int, ...]

    def __post_init__(self) -> None:
        _check_vertices(self.dim, self.vertices)


@dataclass(frozen=True)
class ComplexId:
    name: str

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name:
            raise DimensionMismatchError("complex id requires a nonempty name")


def triangle_simplex_ids() -> Tuple[SimplexId, ...]:
    """The three vertices, three edges, and one face of the standard 2-simplex."""
    vertices = tuple(SimplexId(0, (i,)) for i in range(3))
    edges = (SimplexId(1, (0, 1)), SimplexId(1, (0, 2)), SimplexId(1, (1, 2)))
    face = (SimplexId(2, (0, 1, 2)),)
    identified = vertices + edges + face
    if sum(1 for item in identified if len(item.vertices) == item.dim + 1) != 7:
        raise DimensionMismatchError("triangle census lost a simplex")
    return identified
