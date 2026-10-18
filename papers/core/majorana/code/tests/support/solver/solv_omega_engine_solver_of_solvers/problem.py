"""Declared obstruction problem (no matrix math)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class ObstructionProblem:
    """Carrier and residual class references only — no d0/d1 assembly."""

    problem_id: str
    carrier_ref: str
    residual_class: str
    scope: str
    budget: float = 1.0
    degree_window: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)
    authority_effect: str = "None"
