"""Identifier types for chain complexes, simplices, and homology carriers."""
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class SimplexId:
    dim: int
    vertices: Tuple[int, ...]

@dataclass(frozen=True)
class ComplexId:
    name: str
