from __future__ import annotations
"""Persistence diagram shell."""

from dataclasses import field
from dataclasses import dataclass
from typing import List, Optional, Iterator


@dataclass
class PersistencePoint:
    birth: float
    death: Optional[float]
    dimension: int

    @staticmethod
    def finite(birth: float, death: float, dimension: int) -> "PersistencePoint":
        return PersistencePoint(birth, death, dimension)

    def persistence(self) -> Optional[float]:
        return None if self.death is None else self.death - self.birth


@dataclass
class PersistenceDiagram:
    points: List[PersistencePoint] = field(default_factory=list)

    def finite_only(self) -> Iterator[PersistencePoint]:
        return (p for p in self.points if p.death is not None)



