"""Simplicial complex structures, orientation, and boundary matrices.

Origin: code/python/src/homology/simplicial.py
Claim: consecutive boundary matrices of a complex satisfy ∂_{k-1} ∂_k = 0 over Q.
AuthorityEffect: None.
"""
from dataclasses import dataclass
from fractions import Fraction
from typing import List, Sequence, Tuple

from ..linear_algebra import ExactMatrix
from .errors import DimensionMismatchError


@dataclass(frozen=True)
class Simplex:
    dim: int
    vertices: Tuple[int, ...]

    @classmethod
    def create(cls, vertices: List[int]) -> "Simplex":
        if any(isinstance(vertex, bool) or not isinstance(vertex, int) for vertex in vertices):
            raise DimensionMismatchError("simplex vertices must be ints")
        if len(set(vertices)) != len(vertices):
            raise DimensionMismatchError(f"simplex vertices are not distinct: {vertices}")
        ordered = tuple(sorted(vertices))
        return cls(dim=len(ordered) - 1, vertices=ordered)

    def faces(self) -> Tuple["Simplex", ...]:
        if self.dim == 0:
            return ()
        return tuple(
            Simplex(self.dim - 1, self.vertices[:i] + self.vertices[i + 1 :])
            for i in range(len(self.vertices))
        )


@dataclass
class SimplicialComplex:
    simplices: List[Simplex]

    def dimension(self) -> int:
        return max((s.dim for s in self.simplices), default=0)

    def of_dimension(self, dim: int) -> List[Simplex]:
        return [simplex for simplex in self.simplices if simplex.dim == dim]

    def boundary_matrix(self, dim: int) -> ExactMatrix:
        """Oriented ∂_dim : C_dim → C_{dim-1}. Columns follow of_dimension order."""
        if dim < 1:
            raise DimensionMismatchError("the 0-boundary is the zero map out of an empty group")
        domain = self.of_dimension(dim)
        codomain = self.of_dimension(dim - 1)
        index = {simplex.vertices: row for row, simplex in enumerate(codomain)}
        rows = []
        for _ in codomain:
            rows.append([Fraction(0) for _ in domain])
        for col, simplex in enumerate(domain):
            for omit, face in enumerate(simplex.faces()):
                if face.vertices not in index:
                    raise DimensionMismatchError(f"face {face.vertices} is missing from the complex")
                rows[index[face.vertices]][col] = Fraction(1 if omit % 2 == 0 else -1)
        if not codomain and domain:
            return ExactMatrix(0, len(domain), [])
        if not domain:
            return ExactMatrix(len(codomain), 0, [])
        return ExactMatrix.from_rows(rows)


def filled_triangle() -> SimplicialComplex:
    """Vertices, edges, and the single 2-simplex on {0,1,2}."""
    simplices = [Simplex.create([i]) for i in range(3)]
    simplices.extend(Simplex.create(list(edge)) for edge in ((0, 1), (0, 2), (1, 2)))
    simplices.append(Simplex.create([0, 1, 2]))
    return SimplicialComplex(simplices)


def boundary_square_defect(complex: SimplicialComplex, dim: int) -> Fraction:
    """Sum of absolute entries of ∂_{dim-1} ∂_dim."""
    if dim < 2:
        raise DimensionMismatchError("a boundary square needs dimension at least 2")
    product = complex.boundary_matrix(dim - 1) * complex.boundary_matrix(dim)
    defect = Fraction(0)
    for entry in product.data:
        defect += abs(Fraction(entry))
    return defect


def triangle_boundary_square() -> Fraction:
    return boundary_square_defect(filled_triangle(), 2)
