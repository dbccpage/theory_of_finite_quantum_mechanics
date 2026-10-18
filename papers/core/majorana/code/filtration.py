from __future__ import annotations
"""Filtration shell (parity with Rust omega_homology::filtration)."""

from dataclasses import field
from dataclasses import dataclass
from typing import List


@dataclass
class FilteredSimplex:
    vertices: List[int]
    value: float
    dimension: int


@dataclass
class Filtration:
    simplices: List[FilteredSimplex] = field(default_factory=list)
    max_dimension: int = 0

    def __len__(self) -> int:
        return len(self.simplices)

    def values_nondecreasing(self) -> bool:
        return all(
            self.simplices[i].value <= self.simplices[i + 1].value
            for i in range(len(self.simplices) - 1)
        )



