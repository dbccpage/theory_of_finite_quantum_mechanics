"""Chains over exact fields.

Origin: code/python/src/homology/chain.py
Claim: the edge cycle (1, −1, 1) on a triangle is the boundary of the face, and its vertex boundary is 0.
AuthorityEffect: None.
"""
from dataclasses import dataclass
from fractions import Fraction
from typing import List, Sequence

from ..linear_algebra import Q
from .boundary import triangle_boundaries
from .errors import DimensionMismatchError


@dataclass
class Chain:
    dim: int
    coefficients: List[Q]

    def total(self) -> Fraction:
        if self.dim < 0:
            raise DimensionMismatchError(f"chain dimension must be nonnegative, got {self.dim}")
        total = Fraction(0)
        for coeff in self.coefficients:
            total += Fraction(coeff)
        return total


def vertex_boundary(edge_coefficients: Sequence[object]) -> List[Fraction]:
    """Apply ∂1 of the triangle to a 1-chain on the three edges."""
    edge, _face = triangle_boundaries()
    if len(edge_coefficients) != edge.cols:
        raise DimensionMismatchError(
            f"triangle edge chain has length 3, got {len(edge_coefficients)}"
        )
    return [Fraction(value) for value in edge.mul_vec([Fraction(coeff) for coeff in edge_coefficients])]


def face_cycle_boundary() -> List[Fraction]:
    """Boundary of the fundamental 1-cycle ∂[0,1,2] = e01 − e02 + e12."""
    return vertex_boundary([Fraction(1), Fraction(-1), Fraction(1)])
