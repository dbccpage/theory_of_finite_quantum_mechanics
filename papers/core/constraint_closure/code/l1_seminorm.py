"""Local l1_seminorm definitions for paper 002.

AuthorityEffect: None.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import numpy as np


@dataclass(frozen=True)
class EdgeCochain:
    """1-cochain representation on graph edges."""

    values: np.ndarray

    def __post_init__(self):
        if not isinstance(self.values, np.ndarray):
            object.__setattr__(self, "values", np.asarray(self.values, dtype=float))

    def l1_norm(self, weights: np.ndarray | None = None) -> float:
        w = np.ones_like(self.values) if weights is None else np.asarray(weights, dtype=float)
        return float(np.sum(w * np.abs(self.values)))


__all__ = ["EdgeCochain"]
