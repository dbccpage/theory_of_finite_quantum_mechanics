"""Boundary operator matrix representations.

Origin: code/python/src/homology/boundary.py
Claim: the oriented boundary of a triangle satisfies ∂1 ∂2 = 0 by matrix multiplication.
AuthorityEffect: None.
"""
from fractions import Fraction

from ..linear_algebra import ExactMatrix
from .errors import DimensionMismatchError


class BoundaryOperator:
    def __init__(self, matrix: ExactMatrix):
        self.matrix = matrix

    def apply(self, vec):
        if len(vec) != self.matrix.cols:
            raise DimensionMismatchError(
                f"boundary expects a {self.matrix.cols}-chain, got length {len(vec)}"
            )
        return self.matrix.mul_vec(vec)


def triangle_boundaries() -> tuple:
    """Return ∂1 (vertices × edges) and ∂2 (edges × one face) for the standard 2-simplex."""
    edge = ExactMatrix.from_rows(
        [
            [Fraction(-1), Fraction(-1), Fraction(0)],
            [Fraction(1), Fraction(0), Fraction(-1)],
            [Fraction(0), Fraction(1), Fraction(1)],
        ]
    )
    face = ExactMatrix.from_rows(
        [
            [Fraction(1)],
            [Fraction(-1)],
            [Fraction(1)],
        ]
    )
    return edge, face


def triangle_boundary_defect() -> Fraction:
    """Sum of absolute entries of ∂1 ∂2. Orientation makes the sum identically zero."""
    edge, face = triangle_boundaries()
    product = edge * face
    defect = Fraction(0)
    for entry in product.data:
        defect += abs(Fraction(entry))
    return defect
