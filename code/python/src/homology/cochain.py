"""Cochains over exact fields.

Origin: code/python/src/homology/cochain.py
Claim: the Kronecker pairing is Q-bilinear, and the coboundary of a coboundary on the triangle is 0.
AuthorityEffect: None.
"""
from dataclasses import dataclass
from fractions import Fraction
from typing import List, Sequence

from ..linear_algebra import Q
from .chain import Chain
from .coboundary import triangle_coboundaries
from .errors import DimensionMismatchError


@dataclass
class Cochain:
    dim: int
    coefficients: List[Q]

    def total(self) -> Fraction:
        if self.dim < 0:
            raise DimensionMismatchError(f"cochain dimension must be nonnegative, got {self.dim}")
        total = Fraction(0)
        for coeff in self.coefficients:
            total += Fraction(coeff)
        return total


def pairing(cochain: Cochain, chain: Chain) -> Fraction:
    """Sum α_i c_i. The two arguments must have the same dimension and length."""
    if cochain.dim != chain.dim or len(cochain.coefficients) != len(chain.coefficients):
        raise DimensionMismatchError(
            f"cannot pair cochain dim {cochain.dim} length {len(cochain.coefficients)}"
            f" with chain dim {chain.dim} length {len(chain.coefficients)}"
        )
    total = Fraction(0)
    for alpha, coeff in zip(cochain.coefficients, chain.coefficients):
        total += Fraction(alpha) * Fraction(coeff)
    return total


def coboundary_values(vertex_values: Sequence[object]) -> List[Fraction]:
    """δ0 of a 0-cochain on the three vertices of the triangle."""
    delta0, _delta1 = triangle_coboundaries()
    if len(vertex_values) != delta0.cols:
        raise DimensionMismatchError(f"triangle 0-cochain has length 3, got {len(vertex_values)}")
    return [Fraction(value) for value in delta0.mul_vec([Fraction(value) for value in vertex_values])]


def coboundary_square(vertex_values: Sequence[object]) -> List[Fraction]:
    """δ1 δ0 of a 0-cochain. The single face component is computed, not stored."""
    _delta0, delta1 = triangle_coboundaries()
    edge_values = coboundary_values(vertex_values)
    return [Fraction(value) for value in delta1.mul_vec(edge_values)]
