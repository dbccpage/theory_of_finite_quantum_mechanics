from __future__ import annotations
"""Vietoris–Rips shell."""

from dataclasses import dataclass
from typing import List
from .filtration import Filtration, FilteredSimplex


@dataclass
class PointCloud:
    n_points: int
    distances: List[float]

    def distance(self, i: int, j: int) -> float:
        return self.distances[i * self.n_points + j]


def vietoris_rips_filtration(
    cloud: PointCloud, max_dim: int, radius: float
) -> Filtration:
    simplices: List[FilteredSimplex] = []
    n = cloud.n_points
    for i in range(n):
        simplices.append(FilteredSimplex([i], 0.0, 0))
    if max_dim >= 1:
        for i in range(n):
            for j in range(i + 1, n):
                d = cloud.distance(i, j)
                if d <= radius:
                    simplices.append(FilteredSimplex([i, j], d, 1))
    simplices.sort(key=lambda s: (s.value, s.dimension, s.vertices))
    return Filtration(simplices=simplices, max_dimension=min(max_dim, 1))


