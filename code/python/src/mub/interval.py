"""Exact rational interval arithmetic for MUB(6) verification.

AuthorityEffect: None.
stated region only; mints no authority.

This module provides certified interval arithmetic over exact rationals (fractions.Fraction).
Every lower and upper bound is represented without floating-point approximations.
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, Sequence, Tuple


class RationalInterval:
    """Certified interval [lo, hi] over the rational field Q."""

    __slots__ = ("lo", "hi")

    def __init__(self, lo: Fraction | int, hi: Fraction | int | None = None) -> None:
        if hi is None:
            hi = lo
        self.lo = lo if isinstance(lo, Fraction) else Fraction(lo)
        self.hi = hi if isinstance(hi, Fraction) else Fraction(hi)
        if self.lo > self.hi:
            raise ValueError(f"Invalid interval: lo ({self.lo}) > hi ({self.hi})")

    @classmethod
    def point(cls, r: Fraction | int) -> RationalInterval:
        """Create degenerate point interval [r, r]."""
        return cls(r, r)

    def add(self, other: RationalInterval) -> RationalInterval:
        """Interval addition: [lo1 + lo2, hi1 + hi2]."""
        return RationalInterval(self.lo + other.lo, self.hi + other.hi)

    def sub(self, other: RationalInterval) -> RationalInterval:
        """Interval subtraction: [lo1 - hi2, hi1 - lo2]."""
        return RationalInterval(self.lo - other.hi, self.hi - other.lo)

    def mul(self, other: RationalInterval) -> RationalInterval:
        """Interval multiplication: [min(products), max(products)]."""
        s_lo, s_hi = self.lo, self.hi
        o_lo, o_hi = other.lo, other.hi

        p1 = s_lo * o_lo
        p2 = s_lo * o_hi
        p3 = s_hi * o_lo
        p4 = s_hi * o_hi

        min_p = p1
        if p2 < min_p:
            min_p = p2
        if p3 < min_p:
            min_p = p3
        if p4 < min_p:
            min_p = p4

        max_p = p1
        if p2 > max_p:
            max_p = p2
        if p3 > max_p:
            max_p = p3
        if p4 > max_p:
            max_p = p4

        return RationalInterval(min_p, max_p)

    def sq(self) -> RationalInterval:
        """Interval square: {x^2 : x in [lo, hi]}."""
        zero = Fraction(0, 1)
        if self.lo >= zero:
            return RationalInterval(self.lo * self.lo, self.hi * self.hi)
        elif self.hi <= zero:
            return RationalInterval(self.hi * self.hi, self.lo * self.lo)
        else:
            sq_lo = self.lo * self.lo
            sq_hi = self.hi * self.hi
            max_sq = sq_lo if sq_lo >= sq_hi else sq_hi
            return RationalInterval(zero, max_sq)

    def width(self) -> Fraction:
        """Width of interval hi - lo."""
        return self.hi - self.lo

    def contains(self, r: Fraction | int) -> bool:
        """True iff r in [lo, hi]."""
        frac = r if isinstance(r, Fraction) else Fraction(r)
        return self.lo <= frac <= self.hi

    def overlaps_interior(self, other: RationalInterval) -> bool:
        """True iff the open interiors (lo1, hi1) and (lo2, hi2) intersect."""
        return max(self.lo, other.lo) < min(self.hi, other.hi)

    def is_strictly_positive(self) -> bool:
        """True iff lo > 0."""
        return self.lo > Fraction(0, 1)

    def __repr__(self) -> str:
        return f"[{self.lo}, {self.hi}]"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RationalInterval):
            return False
        return self.lo == other.lo and self.hi == other.hi

    def __hash__(self) -> int:
        return hash((self.lo, self.hi))


VectorBox = Tuple[RationalInterval, ...]

BasisBox = Tuple[VectorBox, ...]


def box_volume(vbox: VectorBox) -> Fraction:
    """Exact 12-dimensional volume of a VectorBox."""
    vol = Fraction(1, 1)
    for iv in vbox:
        vol *= iv.width()
    return vol


def boxes_overlap_interior(a: VectorBox, b: VectorBox) -> bool:
    """True iff the 12-dimensional open interiors of box a and box b intersect."""
    for i in range(len(a)):
        if not a[i].overlaps_interior(b[i]):
            return False
    return True
