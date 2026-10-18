"""Solver registry: problem class → solver_id (no ranking via Φ₁)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Sequence


@dataclass
class SolverRegistry:
    """Maps residual classes to ordered solver ids (declarative, not scored)."""

    _map: Dict[str, List[str]] = field(default_factory=dict)

    def register(self, residual_class: str, solver_ids: Sequence[str]) -> None:
        self._map[residual_class] = list(solver_ids)

    def solvers_for(self, residual_class: str) -> List[str]:
        return list(self._map.get(residual_class, ()))
