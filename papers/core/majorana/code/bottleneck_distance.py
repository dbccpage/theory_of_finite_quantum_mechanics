from __future__ import annotations
"""Bottleneck distance shell (tiny diagrams)."""

from typing import Optional
from .persistence_diagram import PersistenceDiagram, PersistencePoint


def diagonal_cost(p: PersistencePoint) -> float:
    if p.death is None:
        return float("inf")
    return abs(p.death - p.birth) / 2.0


def bottleneck_distance(
    a: PersistenceDiagram, b: PersistenceDiagram
) -> Optional[float]:
    pa = list(a.finite_only())
    pb = list(b.finite_only())
    if len(pa) > 8 or len(pb) > 8:
        return None
    if not pa and not pb:
        return 0.0
    if pa == pb:
        return 0.0
    return max((diagonal_cost(p) for p in pa + pb), default=0.0)

