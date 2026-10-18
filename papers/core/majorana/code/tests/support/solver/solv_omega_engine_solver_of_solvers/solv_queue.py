"""Residual work queue under Prime 002 continuation."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Optional

from .problem import ObstructionProblem


@dataclass
class ResidualQueue:
    """Finite residual queue; does not continue without external CanContinue."""

    _items: Deque[ObstructionProblem] = field(default_factory=deque)

    def push(self, problem: ObstructionProblem) -> None:
        self._items.append(problem)

    def pop(self) -> Optional[ObstructionProblem]:
        if not self._items:
            return None
        return self._items.popleft()

    def __len__(self) -> int:
        return len(self._items)
