"""OESOS cascade receipts (EvidenceOnly / None)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple


@dataclass(frozen=True)
class StageRecord:
    stage: str
    solver_id: str
    status: str
    residual_mass: float
    detail: Dict[str, Any] = field(default_factory=dict)
    authority_effect: str = "None"


@dataclass
class CascadeReceipt:
    problem_id: str
    stages: List[StageRecord] = field(default_factory=list)
    terminal_status: str = "NOT_STARTED"
    authority_effect: str = "None"

    def record(self, rec: StageRecord) -> None:
        self.stages.append(rec)

    def stage_names(self) -> Tuple[str, ...]:
        return tuple(s.stage for s in self.stages)
