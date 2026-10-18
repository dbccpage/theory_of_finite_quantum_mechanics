from __future__ import annotations
"""Barcode shell over a persistence diagram."""

from dataclasses import field
from dataclasses import dataclass
from typing import List, Optional
from .persistence_diagram import PersistenceDiagram


@dataclass
class Bar:
    birth: float
    death: Optional[float]
    dimension: int


@dataclass
class Barcode:
    bars: List[Bar] = field(default_factory=list)

    @classmethod
    def from_diagram(cls, diagram: PersistenceDiagram) -> "Barcode":
        return cls(bars=[Bar(p.birth, p.death, p.dimension) for p in diagram.points])



