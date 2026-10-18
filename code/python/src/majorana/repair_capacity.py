"""Repair capacity diagnostic helper (CODE_DEMO only).

QM_102-shaped shadow: given a declared code / homology distance d,
the classical unique-decode repair radius is t = floor((d - 1) / 2),
which always satisfies t < d / 2.

Authority fence:
- AuthorityEffect: None
- Does not mint a threshold theorem, THR-001 packet, or PROVED claim.
- Does not assert a physical surface-code distance for any complex.
"""

from __future__ import annotations

from typing import Optional, Sequence

AUTHORITY_EFFECT = "AuthorityEffect: None"


def repair_capacity_from_distance(d: int) -> int:
    """Diagnostic repair capacity t = floor((d-1)/2) for positive distance d.
    
    Refuses d <= 0 (undeclared distance is not a certificate).
    """
    if d <= 0:
        raise ValueError(
            "repair_capacity: homology/code distance d must be positive (undeclared d refuses)"
        )
    return (d - 1) // 2


def assert_repair_capacity_invariant(d: int) -> int:
    """Invariant gate: t = floor((d-1)/2) and t < d/2 (equivalently 2t < d)."""
    t = repair_capacity_from_distance(d)
    expected = (d - 1) // 2
    if t != expected:
        raise ValueError(
            f"repair_capacity: t={t} != floor((d-1)/2)={expected} for d={d}"
        )
    if 2 * t >= d:
        raise ValueError(
            f"repair_capacity: invariant broken: t={t} is not < d/2 for d={d}"
        )
    return t


def min_weight_nontrivial(cycles: Sequence[Sequence[int]]) -> Optional[int]:
    """Optional CODE_DEMO: min Hamming weight among a declared list of nontrivial closed residuals."""
    weights = [sum(b % 2 for b in c) for c in cycles if any(b % 2 == 1 for b in c)]
    return min(weights) if weights else None
