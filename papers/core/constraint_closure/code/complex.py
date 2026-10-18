"""Simplicial complex topology, boundary/coboundary matrices, and canonical manifolds.

AuthorityEffect: None.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple
import numpy as np


@dataclass
class SimplicialComplex:
    """Finite simplicial complex with cells indexed by dimension k."""

    max_dim: int
    cells: Dict[int, List[Tuple[int, ...]]] = field(default_factory=dict)
    _boundary_cache: Dict[int, np.ndarray] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._close_under_faces()

    def _close_under_faces(self) -> None:
        """Ensure the complex is downward closed under taking faces."""
        for d in range(self.max_dim, 0, -1):
            if d not in self.cells:
                self.cells[d] = []
            lower_d = d - 1
            if lower_d not in self.cells:
                self.cells[lower_d] = []
            existing_lower = set(self.cells[lower_d])
            for cell in self.cells[d]:
                for i in range(len(cell)):
                    face = tuple(cell[:i] + cell[i + 1 :])
                    if face not in existing_lower:
                        self.cells[lower_d].append(face)
                        existing_lower.add(face)

        for d in self.cells:
            self.cells[d] = sorted(list(set(tuple(sorted(c)) for c in self.cells[d])))

    @property
    def num_vertices(self) -> int:
        return len(self.cells.get(0, []))

    @property
    def num_edges(self) -> int:
        return len(self.cells.get(1, []))

    @property
    def num_faces(self) -> int:
        return len(self.cells.get(2, []))

    @property
    def num_tetrahedra(self) -> int:
        return len(self.cells.get(3, []))

    def euler_characteristic(self) -> int:
        """Compute Euler characteristic chi = sum_{k=0}^D (-1)^k N_k."""
        chi = 0
        for d in range(self.max_dim + 1):
            chi += ((-1) ** d) * len(self.cells.get(d, []))
        return chi

    def boundary_matrix(self, k: int) -> np.ndarray:
        """Assemble boundary operator matrix partial_k: C_k -> C_{k-1}."""
        if k in self._boundary_cache:
            return self._boundary_cache[k]

        simplices_k = self.cells.get(k, [])
        simplices_km1 = self.cells.get(k - 1, [])

        num_k = len(simplices_k)
        num_km1 = len(simplices_km1)

        if num_k == 0 or num_km1 == 0:
            mat = np.zeros((num_km1, num_k), dtype=float)
            self._boundary_cache[k] = mat
            return mat

        face_index = {face: idx for idx, face in enumerate(simplices_km1)}
        mat = np.zeros((num_km1, num_k), dtype=float)

        for col_j, cell in enumerate(simplices_k):
            for i in range(len(cell)):
                face = tuple(cell[:i] + cell[i + 1 :])
                sign = (-1) ** i
                if face in face_index:
                    row_i = face_index[face]
                    mat[row_i, col_j] += sign

        self._boundary_cache[k] = mat
        return mat

    def coboundary_matrix(self, k: int) -> np.ndarray:
        """Assemble coboundary operator matrix d_k: C^k -> C^{k+1}.

        By definition, d_k = (partial_{k+1})^T.
        """
        return self.boundary_matrix(k + 1).T

    def verify_nilpotency(self, k: int) -> bool:
        """Verify partial_{k-1} o partial_k == 0 and d_k o d_{k-1} == 0."""
        b_k = self.boundary_matrix(k)
        b_km1 = self.boundary_matrix(k - 1)
        if b_km1.shape[0] == 0 or b_k.shape[1] == 0:
            return True
        prod = b_km1 @ b_k
        return bool(np.allclose(prod, 0.0, atol=1e-12))

    def star(self, simplex: Tuple[int, ...], target_dim: int) -> List[Tuple[int, ...]]:
        """Return all simplices of dimension target_dim containing simplex."""
        s_set = set(simplex)
        results = []
        for cell in self.cells.get(target_dim, []):
            if s_set.issubset(set(cell)):
                results.append(cell)
        return results


def build_simplex_boundary_complex(d: int) -> SimplicialComplex:
    """Build the boundary complex of a (d+1)-simplex, which is a triangulated d-sphere S^d.

    d=2: Boundary of 3-simplex (tetrahedron) -> 4 vertices, 6 edges, 4 triangles.
    d=3: Boundary of 4-simplex -> 5 vertices, 10 edges, 10 triangles, 5 tetrahedra.
    d=4: Boundary of 5-simplex -> 6 vertices, 15 edges, 20 triangles, 15 tetrahedra, 6 4-simplices.
    """
    verts = list(range(d + 2))
    cells: Dict[int, List[Tuple[int, ...]]] = {}
    for dim in range(d + 1):
        cells[dim] = [tuple(c) for c in itertools.combinations(verts, dim + 1)]
    return SimplicialComplex(max_dim=d, cells=cells)


def build_4simplex_boundary_3sphere() -> SimplicialComplex:
    """Triangulated 3-sphere as the boundary of a regular 4-simplex.

    5 vertices, 10 edges, 10 triangles, 5 tetrahedra.
    Euler characteristic: chi(S^3) = 5 - 10 + 10 - 5 = 0.
    """
    return build_simplex_boundary_complex(3)


def build_5simplex_boundary_4sphere() -> SimplicialComplex:
    """Triangulated 4-sphere as the boundary of a 5-simplex.

    6 vertices, 15 edges, 20 triangles, 15 tetrahedra, 6 4-simplices.
    Euler characteristic: chi(S^4) = 6 - 15 + 20 - 15 + 6 = 2.
    """
    return build_simplex_boundary_complex(4)


def build_flat_torus_2d(n_x: int = 3, n_y: int = 3) -> SimplicialComplex:
    """Build a triangulated 2D flat torus with periodic boundary conditions.

    Every vertex has valency 6.
    Euler characteristic: chi(T^2) = V - E + F = 0.
    """
    if n_x < 3 or n_y < 3:
        raise ValueError("Flat torus triangulation requires at least 3x3 grid to avoid multigraph")

    def v_id(x: int, y: int) -> int:
        return (x % n_x) * n_y + (y % n_y)

    vertices = list(range(n_x * n_y))
    faces = []

    for x in range(n_x):
        for y in range(n_y):
            v00 = v_id(x, y)
            v10 = v_id(x + 1, y)
            v01 = v_id(x, y + 1)
            v11 = v_id(x + 1, y + 1)

            faces.append(tuple(sorted((v00, v10, v11))))
            faces.append(tuple(sorted((v00, v11, v01))))

    cells = {
        0: [(v,) for v in vertices],
        2: list(set(faces)),
    }
    return SimplicialComplex(max_dim=2, cells=cells)
