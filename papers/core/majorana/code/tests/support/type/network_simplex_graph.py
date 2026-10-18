"""Port of ``omega_solvers/src/network_simplex/graph.rs``."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class Arc:
    """An arc in the network. ``cost``/``lower``/``upper`` are integers (i128 in Rust)."""

    tail: int
    head: int
    cost: int
    lower: int = 0
    upper: Optional[int] = None
    original_edge: Optional[int] = None
    orientation_sign: int = 0


