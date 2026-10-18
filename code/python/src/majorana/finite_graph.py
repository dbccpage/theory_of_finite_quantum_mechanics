from __future__ import annotations
r"""
Declared finite graph carrier: NumPy 2-truncated cochain complex C^0 -> C^1 -> C^2.

AuthorityEffect: None.
"""


from dataclasses import field
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

import numpy as np


@dataclass(frozen=True)
class FiniteGraph:
    r"""A finite 2-truncated cochain carrier.

    `vertices` can be a sequence of vertex labels OR an integer number of vertices.
    """

    vertices: Sequence | int
    edges: Sequence[Tuple]
    faces: Sequence[Tuple] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if isinstance(self.vertices, int):
            n = self.vertices
            if n < 1:
                raise ValueError("graph needs at least one vertex")
            object.__setattr__(self, "vertices", list(range(n)))
        for tail, head in self.edges:
            if not (0 <= tail < len(self.vertices) and 0 <= head < len(self.vertices)):
                raise ValueError("edge endpoint is outside the vertex carrier")
            if tail == head:
                raise ValueError("loops are outside this oriented graph model")


    @property
    def n_vertices(self) -> int:
        return len(self.vertices)

    @property
    def n_edges(self) -> int:
        return len(self.edges)

    @property
    def n_faces(self) -> int:
        return len(self.faces)

    def _vertex_index(self) -> Dict:
        return {v: i for i, v in enumerate(self.vertices)}

    def d0_matrix(self) -> np.ndarray:
        r"""The |E| x |V| coboundary matrix, d0[e, tail] = -1, d0[e, head] = +1."""
        vidx = self._vertex_index()
        mat = np.zeros((self.n_edges, self.n_vertices), dtype=float)
        for i, (u, v) in enumerate(self.edges):
            if u not in vidx or v not in vidx:
                raise ValueError(f"edge {(u, v)} references a vertex not in the carrier")
            mat[i, vidx[u]] -= 1.0
            mat[i, vidx[v]] += 1.0
        return mat

    def d0(self, alpha: Sequence[float] | np.ndarray) -> np.ndarray:
        r"""(d0 \alpha)_{(u,v)} = \alpha_v - \alpha_u."""
        a = np.asarray(alpha, dtype=float)
        if a.shape != (self.n_vertices,):
            raise ValueError(f"d0: expected {self.n_vertices} vertex values, got {a.shape}")
        return self.d0_matrix() @ a

    def d1_matrix(self) -> np.ndarray:
        r"""The |F| x |E| face coboundary matrix with orientation signs."""
        oriented: Dict[Tuple, int] = {}
        for i, (u, v) in enumerate(self.edges):
            oriented[(u, v)] = i + 1
            oriented.setdefault((v, u), -(i + 1))

        mat = np.zeros((self.n_faces, self.n_edges), dtype=float)
        for f_idx, cycle in enumerate(self.faces):
            k = len(cycle)
            for j in range(k):
                pair = (cycle[j], cycle[(j + 1) % k])
                signed = oriented.get(pair)
                if signed is None:
                    raise ValueError(
                        f"face {cycle} uses {pair}, which is not an edge of the carrier"
                    )
                mat[f_idx, abs(signed) - 1] += float(np.sign(signed))
        return mat

    def d1(self, omega: Sequence[float] | np.ndarray) -> np.ndarray:
        r"""Face curvature K_f = (d1 \omega)_f."""
        w = np.asarray(omega, dtype=float)
        if w.shape != (self.n_edges,):
            raise ValueError(f"d1: expected {self.n_edges} edge values, got {w.shape}")
        return self.d1_matrix() @ w

    def verify_nilpotency(self, atol: float = 1e-12) -> bool:
        r"""Checks d1 . d0 = 0 on this carrier."""
        if self.n_faces == 0:
            return True
        return bool(np.allclose(self.d1_matrix() @ self.d0_matrix(), 0.0, atol=atol))

    def cycle_rank(self) -> int:
        r"""\beta_1 = |E| - rank(d0) --- combinatorial cycle rank."""
        if self.n_edges == 0:
            return 0
        return int(self.n_edges - np.linalg.matrix_rank(self.d0_matrix()))


def triangle() -> FiniteGraph:
    r"""The one-face triangle: three vertices, three edges, \beta_1 = 1."""
    return FiniteGraph(vertices=[0, 1, 2], edges=[(0, 1), (1, 2), (2, 0)], faces=[(0, 1, 2)])


def path_graph(n: int) -> FiniteGraph:
    r"""A tree on n vertices: no cycles."""
    if n < 2:
        raise ValueError("path_graph: need at least 2 vertices")
    return FiniteGraph(vertices=list(range(n)), edges=[(i, i + 1) for i in range(n - 1)])



