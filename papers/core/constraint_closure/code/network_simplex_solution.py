"""Local NetworkSimplexSolution definition for network simplex in paper 002.

AuthorityEffect: None.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class NetworkSimplexSolution:
    objective: int
    flow: List[int] = field(default_factory=list)
    potential: List[int] = field(default_factory=list)
    reduced_costs: List[int] = field(default_factory=list)


__all__ = ["NetworkSimplexSolution"]
