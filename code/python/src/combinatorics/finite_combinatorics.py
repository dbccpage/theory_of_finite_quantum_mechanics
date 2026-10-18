"""Exact finite combinatorics, integer partitions, finite projective/affine geometry parameters, and Weyl/MUB counts.

AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import dataclass
from itertools import product
import math
from typing import List, Tuple


class CombinatoricsBudgetError(ValueError):
    """Raised when a requested enumeration exceeds its declared budget."""


@dataclass(frozen=True)
class FiniteProjectivePlaneParams:
    """Parameters of PG(2, q) and AG(2, q) for prime power order q."""

    order_q: int
    pg_points: int
    pg_lines: int
    points_per_line: int
    ag_points: int
    ag_lines: int
    parallel_classes: int


def binomial_exact(n: int, k: int) -> int:
    """Exact binomial coefficient C(n, k) for non-negative integers."""
    if n < 0 or k < 0 or k > n:
        return 0
    return math.comb(n, k)


def enumerate_cartesian_words(alphabet_size: int, length: int, budget: int) -> List[Tuple[int, ...]]:
    """Enumerate all words in {0, ..., alphabet_size - 1}^length subject to a strict pre-checked budget."""
    if alphabet_size < 0 or length < 0 or budget < 0:
        raise ValueError("alphabet_size, length, and budget must be non-negative")
    total = 1 if length == 0 else alphabet_size**length
    if total > budget:
        raise CombinatoricsBudgetError(f"Cartesian word count {total} exceeds budget {budget}")
    return [tuple(w) for w in product(range(alphabet_size), repeat=length)]


def integer_partitions(n: int) -> List[Tuple[int, ...]]:
    """Return all non-increasing positive integer partitions of n >= 0 in lexicographic order."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return [()]

    result: List[Tuple[int, ...]] = []

    def _rec(rem: int, max_part: int, prefix: List[int]) -> None:
        if rem == 0:
            result.append(tuple(prefix))
            return
        for part in range(min(rem, max_part), 0, -1):
            prefix.append(part)
            _rec(rem - part, part, prefix)
            prefix.pop()

    _rec(n, n, [])
    return result


def finite_plane_parameters(q: int) -> FiniteProjectivePlaneParams:
    """Compute exact point/line/parallel-class counts for PG(2, q) and AG(2, q) alongside MUB count q + 1."""
    if q < 2:
        raise ValueError("Order q must be at least 2")
    pg_pts = q * q + q + 1
    return FiniteProjectivePlaneParams(
        order_q=q,
        pg_points=pg_pts,
        pg_lines=pg_pts,
        points_per_line=q + 1,
        ag_points=q * q,
        ag_lines=q * (q + 1),
        parallel_classes=q + 1,
    )


def weyl_heisenberg_displacement_count(d: int) -> Tuple[int, int]:
    """Return (d^2 total phase-space displacements, d^2 - 1 non-identity displacements) for dimension d >= 2."""
    if d < 2:
        raise ValueError("Dimension d must be at least 2")
    return (d * d, d * d - 1)
