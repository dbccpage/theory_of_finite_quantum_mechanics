"""Cascade stages (orchestration names only)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional


class StageKind(str, Enum):
    FOUNDATION = "foundation"
    RESIDUAL_REPAIR = "residual_repair"
    CELL_PROPOSE = "cell_propose"
    WINDOW_LIFT = "window_lift"
    TERMINAL = "terminal"


@dataclass(frozen=True)
class CascadeStage:
    """A named cascade stage. ``handler`` may call math packages; stage owns none."""

    kind: StageKind
    solver_id: str
    handler: Optional[Callable[..., object]] = None
