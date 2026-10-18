"""Phase fiber over a rational point of the circle, multiplied in Q(i).

Origin: code/python/src/qm/campaigns/phase_fiber.py
Claim: (3/5 + 4/5 i) and (5/13 + 12/13 i) each have norm 1, and so does their product.
AuthorityEffect: None.
"""
from fractions import Fraction

from ...linear_algebra.scalars import GaussianRational


class PhaseFiberError(Exception):
    """A phase representative left the unit circle."""


def unit_product() -> Fraction:
    first = GaussianRational(Fraction(3, 5), Fraction(4, 5))
    second = GaussianRational(Fraction(5, 13), Fraction(12, 13))
    if first.norm_sq() != 1 or second.norm_sq() != 1:
        raise PhaseFiberError("a phase representative is not on the unit circle")
    product = first * second
    norm = product.norm_sq()
    if norm != 1:
        raise PhaseFiberError(f"fiber product has norm {norm}")
    return norm
