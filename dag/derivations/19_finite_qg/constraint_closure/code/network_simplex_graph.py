"""Local Arc definition for network simplex in paper 002.

AuthorityEffect: None.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class Arc:
    """An arc in the network."""

    tail: int
    head: int
    cost: int
    lower: int = 0
    upper: Optional[int] = None
    original_edge: Optional[int] = None
    orientation_sign: int = 0


__all__ = ["Arc"]
