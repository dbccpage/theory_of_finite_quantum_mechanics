"""Simplicial complex structures and orientation."""
from dataclasses import dataclass
from typing import List, Tuple

@dataclass(frozen=True)
class Simplex:
    dim: int
    vertices: Tuple[int, ...]

    @classmethod
    def create(cls, vertices: List[int]) -> "Simplex":
        sv = tuple(sorted(vertices))
        return cls(dim=len(sv) - 1, vertices=sv)

@dataclass
class SimplicialComplex:
    simplices: List[Simplex]

    def dimension(self) -> int:
        return max((s.dim for s in self.simplices), default=0)
