"""Port of ``omega_solvers/src/network_simplex/solution.rs``."""

from __future__ import annotations
from dataclasses import field
from dataclasses import dataclass
from typing import List


@dataclass
class NetworkSimplexSolution:
    objective: int
    flow: List[int] = field(default_factory=list)
    potential: List[int] = field(default_factory=list)
    reduced_costs: List[int] = field(default_factory=list)



