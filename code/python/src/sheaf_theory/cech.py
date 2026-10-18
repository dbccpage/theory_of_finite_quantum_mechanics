"""Čech cochain complex and Čech cohomology H^p(U, F) over exact rational sections.

AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from fractions import Fraction
from itertools import combinations
from typing import Dict, List, Optional, Set, Tuple


@dataclass(frozen=True)
class OpenSet:
    """Finite open set represented by its point indices."""
    points: frozenset[int]

    @classmethod
    def from_iterable(cls, items) -> OpenSet:
        return cls(frozenset(items))

    def intersection(self, other: OpenSet) -> OpenSet:
        return OpenSet(self.points.intersection(other.points))

    def is_empty(self) -> bool:
        return len(self.points) == 0

    def contains(self, x: int) -> bool:
        return x in self.points


@dataclass
class CechCochain:
    """Čech p-cochain assigning rational values to (p+1)-fold intersections."""
    degree: int
    data: Dict[Tuple[int, ...], Fraction] = field(default_factory=dict)

    def get(self, indices: Tuple[int, ...]) -> Fraction:
        sorted_idx = tuple(sorted(indices))
        return self.data.get(sorted_idx, Fraction(0))

    def is_zero(self) -> bool:
        return all(v == 0 for v in self.data.values())


def cech_coboundary_rational(cochain: CechCochain, cover: List[OpenSet]) -> CechCochain:
    """Compute Čech coboundary delta: C^p -> C^{p+1} over rational sections:

    (delta omega)(i_0, ..., i_{p+1}) = sum_{k=0}^{p+1} (-1)^k omega(i_0, ..., hat{i}_k, ..., i_{p+1})
    """
    p = cochain.degree
    p_next = p + 1
    n = len(cover)
    next_data: Dict[Tuple[int, ...], Fraction] = {}

    for indices in combinations(range(n), p_next + 1):
        # Check non-empty multi-intersection
        inter = cover[indices[0]]
        for idx in indices[1:]:
            inter = inter.intersection(cover[idx])
        if inter.is_empty():
            continue

        # Alternating sum over faces
        val = Fraction(0)
        for k in range(p_next + 1):
            face = tuple(indices[j] for j in range(p_next + 1) if j != k)
            face_val = cochain.get(face)
            if k % 2 == 1:
                val -= face_val
            else:
                val += face_val

        next_data[indices] = val

    return CechCochain(p_next, next_data)


def compute_cech_h0(cover: List[OpenSet], constant_val: Fraction) -> Optional[CechCochain]:
    """Compute Čech zeroth cohomology H^0(U, F) = ker(delta^0)."""
    data = {(i,): constant_val for i in range(len(cover))}
    c0 = CechCochain(0, data)
    d_c0 = cech_coboundary_rational(c0, cover)
    if d_c0.is_zero():
        return c0
    return None


def is_1_cocycle(cochain: CechCochain, cover: List[OpenSet]) -> bool:
    """Check if a 1-cochain satisfies the cocycle condition delta^1(g) = 0."""
    if cochain.degree != 1:
        return False
    d_c1 = cech_coboundary_rational(cochain, cover)
    return d_c1.is_zero()
