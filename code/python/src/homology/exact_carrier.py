"""Exact rational carrier for the filled triangle.

Origin: code/python/src/homology/exact_carrier.py
Claim: the triangle carrier has rank(d0) = 2, rank(d1) = 1, and dim H1 = 0.
AuthorityEffect: None. ExactCarrier remains the Carrier alias.
"""
from fractions import Fraction

from ..linear_algebra import ExactMatrix
from .carrier import Carrier

ExactCarrier = Carrier


def triangle_carrier() -> Carrier:
    """Coboundary matrices of the 2-simplex, in the Carrier shape convention."""
    delta0 = ExactMatrix.from_rows(
        [
            [Fraction(-1), Fraction(1), Fraction(0)],
            [Fraction(-1), Fraction(0), Fraction(1)],
            [Fraction(0), Fraction(-1), Fraction(1)],
        ]
    )
    delta1 = ExactMatrix.from_rows([[Fraction(1), Fraction(-1), Fraction(1)]])
    return Carrier(3, 3, 1, delta0, delta1)


def triangle_betti() -> tuple:
    """Return (rank d0, rank d1, dim H1), each computed from the carrier."""
    carrier = triangle_carrier()
    rank0 = carrier.rank_d0()
    rank1 = carrier.rank_d1()
    betti = carrier.dim_h1()
    if betti != (carrier.dim1 - rank1) - rank0:
        raise ValueError("dim H1 disagrees with rank-nullity on the triangle")
    return rank0, rank1, betti
