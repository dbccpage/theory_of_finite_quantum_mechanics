"""Coboundary operator representations.

Origin: code/python/src/homology/coboundary.py
Claim: the coboundary is the transpose of the boundary, and δ1 δ0 = 0 on the triangle.
AuthorityEffect: None.
"""
from fractions import Fraction

from ..linear_algebra import ExactMatrix
from .boundary import triangle_boundaries
from .errors import DimensionMismatchError


class CoboundaryOperator:
    def __init__(self, boundary_matrix: ExactMatrix):
        self.matrix = boundary_matrix.transpose()

    def apply(self, vec):
        if len(vec) != self.matrix.cols:
            raise DimensionMismatchError(
                f"coboundary expects a {self.matrix.cols}-cochain, got length {len(vec)}"
            )
        return self.matrix.mul_vec(vec)


def triangle_coboundaries() -> tuple:
    """Return δ0 = ∂1^T and δ1 = ∂2^T."""
    edge, face = triangle_boundaries()
    return edge.transpose(), face.transpose()


def triangle_coboundary_defect() -> Fraction:
    """Sum of absolute entries of δ1 δ0."""
    delta0, delta1 = triangle_coboundaries()
    product = delta1 * delta0
    defect = Fraction(0)
    for entry in product.data:
        defect += abs(Fraction(entry))
    return defect
