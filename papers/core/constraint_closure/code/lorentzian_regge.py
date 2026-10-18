"""4D Lorentzian Regge Simplicial Complex under Adaptive Subdivision.

Implements discrete Lorentzian simplicial geometry on (1+3) Minkowski spacetime:
- Minkowski metric eta = diag(-1, 1, 1, 1).
- Invariant interval s_e^2 = -(Delta t)^2 + (Delta x)^2 + (Delta y)^2 + (Delta z)^2.
- Edge signature classification: spacelike (s^2 > 0), timelike (s^2 < 0), null (s^2 = 0).
- Downward-closed 4D simplicial complex with operator nilpotency (partial^2 = 0, d^2 = 0).
- Canonical 1-to-5 stellar Pachner subdivision inserting interior barycenter vertices.
- Simplicial edge bisection.
- Discrete Bianchi identity operator d_2: C^2 -> C^3.

AuthorityEffect: None.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple
import numpy as np


@dataclass
class Lorentzian4Complex:
    """Finite 4D Lorentzian simplicial complex with Minkowski vertex coordinates."""

    vertices: Dict[int, np.ndarray] = field(default_factory=dict)
    four_simplices: List[Tuple[int, ...]] = field(default_factory=list)
    tol: float = 1e-10

    cells: Dict[int, List[Tuple[int, ...]]] = field(default_factory=dict, init=False)
    _boundary_cache: Dict[int, np.ndarray] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.rebuild_topology()

    def rebuild_topology(self) -> None:
        """Rebuild downward-closed cell dictionaries and clear operator caches."""
        self._boundary_cache.clear()
        self.cells = {0: [], 1: [], 2: [], 3: [], 4: []}

        canon_4 = sorted(list(set(tuple(sorted(s)) for s in self.four_simplices)))
        self.four_simplices = canon_4
        self.cells[4] = list(canon_4)

        c3 = set()
        for s in self.cells[4]:
            for i in range(5):
                c3.add(tuple(sorted(s[:i] + s[i + 1 :])))
        self.cells[3] = sorted(list(c3))

        c2 = set()
        for s in self.cells[3]:
            for i in range(4):
                c2.add(tuple(sorted(s[:i] + s[i + 1 :])))
        self.cells[2] = sorted(list(c2))

        c1 = set()
        for s in self.cells[2]:
            for i in range(3):
                c1.add(tuple(sorted(s[:i] + s[i + 1 :])))
        self.cells[1] = sorted(list(c1))

        c0 = sorted(list(set((v,) for v in self.vertices.keys())))
        self.cells[0] = c0

    @property
    def num_vertices(self) -> int:
        return len(self.cells.get(0, []))

    @property
    def num_edges(self) -> int:
        return len(self.cells.get(1, []))

    @property
    def num_triangles(self) -> int:
        return len(self.cells.get(2, []))

    @property
    def num_faces(self) -> int:
        return self.num_triangles

    @property
    def num_tetrahedra(self) -> int:
        return len(self.cells.get(3, []))

    @property
    def num_four_simplices(self) -> int:
        return len(self.cells.get(4, []))

    def euler_characteristic(self) -> int:
        """Compute Euler characteristic chi = N_0 - N_1 + N_2 - N_3 + N_4."""
        return (
            self.num_vertices
            - self.num_edges
            + self.num_triangles
            - self.num_tetrahedra
            + self.num_four_simplices
        )


    def edge_vector(self, edge: Tuple[int, int]) -> np.ndarray:
        """Displacement 4-vector Delta x = x_v - x_u."""
        u, v = edge
        return self.vertices[v] - self.vertices[u]

    def edge_squared_interval(self, edge: Tuple[int, int]) -> float:
        """Compute Lorentzian invariant interval s_e^2 = -(Delta t)^2 + |Delta x|^2.

        Uses Minkowski metric convention eta = diag(-1, +1, +1, +1).
        """
        dx = self.edge_vector(edge)
        dt2 = float(dx[0] ** 2)
        dr2 = float(np.sum(dx[1:] ** 2))
        return dr2 - dt2

    def is_spacelike(self, edge: Tuple[int, int]) -> bool:
        """True if edge interval is spacelike: s_e^2 > tol."""
        return self.edge_squared_interval(edge) > self.tol

    def is_timelike(self, edge: Tuple[int, int]) -> bool:
        """True if edge interval is timelike: s_e^2 < -tol."""
        return self.edge_squared_interval(edge) < -self.tol

    def is_null(self, edge: Tuple[int, int]) -> bool:
        """True if edge interval is null/lightlike: |s_e^2| <= tol."""
        return abs(self.edge_squared_interval(edge)) <= self.tol

    def edge_signature_counts(self) -> Dict[str, int]:
        """Count edges by Lorentzian signature category."""
        counts = {"spacelike": 0, "timelike": 0, "null": 0}
        for edge in self.cells.get(1, []):
            if self.is_spacelike(edge):
                counts["spacelike"] += 1
            elif self.is_timelike(edge):
                counts["timelike"] += 1
            else:
                counts["null"] += 1
        return counts


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
                face = tuple(sorted(cell[:i] + cell[i + 1 :]))
                sign = (-1) ** i
                if face in face_index:
                    row_i = face_index[face]
                    mat[row_i, col_j] += sign

        self._boundary_cache[k] = mat
        return mat

    def coboundary_matrix(self, k: int) -> np.ndarray:
        """Assemble coboundary operator matrix d_k = (partial_{k+1})^T: C^k -> C^{k+1}."""
        return self.boundary_matrix(k + 1).T

    def verify_nilpotency(self, k: int) -> bool:
        """Verify partial_{k-1} o partial_k == 0 and d_k o d_{k-1} == 0."""
        b_k = self.boundary_matrix(k)
        b_km1 = self.boundary_matrix(k - 1)
        if b_km1.shape[0] == 0 or b_k.shape[1] == 0:
            return True
        prod = b_km1 @ b_k
        return bool(np.allclose(prod, 0.0, atol=1e-12))

    def boundary_tetrahedra(self) -> Set[Tuple[int, ...]]:
        """Identify boundary 3-simplices that belong to exactly one 4-simplex."""
        tetra_counts: Dict[Tuple[int, ...], int] = {}
        for s in self.cells.get(4, []):
            for i in range(5):
                t = tuple(sorted(s[:i] + s[i + 1 :]))
                tetra_counts[t] = tetra_counts.get(t, 0) + 1
        return {t for t, count in tetra_counts.items() if count == 1}


    def bianchi_flux(self, curvature_2cochain: np.ndarray) -> np.ndarray:
        """Evaluate discrete Bianchi 3-flux: d_2 omega_R on tetrahedra C_3.

        By definition, for any exact 2-cochain omega = d_1 beta, d_2 omega == 0.
        """
        d2 = self.coboundary_matrix(2)
        curvature_2cochain = np.asarray(curvature_2cochain, dtype=float).flatten()
        if len(curvature_2cochain) != self.num_triangles:
            raise ValueError(
                f"Curvature cochain length ({len(curvature_2cochain)}) must match triangles ({self.num_triangles})"
            )
        return d2 @ curvature_2cochain

    def verify_bianchi_identity(self, curvature_2cochain: np.ndarray) -> Dict[str, Any]:
        """Verify d_2 omega_R == 0 and return residual norms."""
        flux = self.bianchi_flux(curvature_2cochain)
        l1_norm = float(np.sum(np.abs(flux)))
        linf_norm = float(np.max(np.abs(flux))) if len(flux) > 0 else 0.0
        return {
            "is_satisfied": linf_norm < self.tol,
            "total_l1_flux": l1_norm,
            "max_linf_flux": linf_norm,
            "authority_effect": "None",
        }


    def stellar_subdivide(self, simplex_idx: int) -> Tuple[int, List[Tuple[int, ...]]]:
        """Perform 1-to-5 stellar subdivision (Pachner move 1 -> 5) on 4-simplex.

        Replaces target 4-simplex sigma = (v0, v1, v2, v3, v4) with five daughter
        4-simplices formed by connecting its boundary tetrahedra to an interior
        barycenter vertex v_new.

        Preserves:
        - All boundary tetrahedra of sigma.
        - Downward simplicial closure.
        - Exact boundary operator nilpotency.
        """
        if simplex_idx < 0 or simplex_idx >= self.num_four_simplices:
            raise IndexError(f"Simplex index {simplex_idx} out of range [0, {self.num_four_simplices})")

        target = self.cells[4][simplex_idx]

        new_v_id = max(self.vertices.keys()) + 1 if self.vertices else 0
        target_coords = [self.vertices[v] for v in target]
        barycenter = np.mean(target_coords, axis=0)
        self.vertices[new_v_id] = barycenter

        new_four_simplices = [s for i, s in enumerate(self.four_simplices) if i != simplex_idx]
        daughters = []
        for i in range(5):
            daughter = tuple(sorted(target[:i] + target[i + 1 :] + (new_v_id,)))
            daughters.append(daughter)
            new_four_simplices.append(daughter)

        self.four_simplices = new_four_simplices
        self.rebuild_topology()
        return new_v_id, daughters

    def bisect_edge(self, edge: Tuple[int, int]) -> int:
        """Perform simplicial edge bisection on target edge e = (u, v).

        Inserts midpoint vertex v_mid = (x_u + x_v)/2 and splits all incident
        simplices into two child simplices of equal dimension.
        """
        u, v = sorted(edge)
        if (u, v) not in self.cells.get(1, []):
            raise ValueError(f"Edge ({u}, {v}) not present in simplicial complex")

        new_v_id = max(self.vertices.keys()) + 1 if self.vertices else 0
        midpoint = 0.5 * (self.vertices[u] + self.vertices[v])
        self.vertices[new_v_id] = midpoint

        new_fours = []
        for s in self.four_simplices:
            if u in s and v in s:
                s_set = set(s)
                s1 = tuple(sorted((s_set - {v}) | {new_v_id}))
                s2 = tuple(sorted((s_set - {u}) | {new_v_id}))
                new_fours.extend([s1, s2])
            else:
                new_fours.append(s)

        self.four_simplices = new_fours
        self.rebuild_topology()
        return new_v_id


def build_canonical_lorentzian_4simplex(
    t_span: float = 2.0,
    spatial_scale: float = 1.0,
) -> Lorentzian4Complex:
    """Build a single 4-simplex with mixed timelike and spacelike edges in R^{1,3}.

    v0: (0, 0, 0, 0)
    v1: (t_span/2, spatial_scale, 0, 0)
    v2: (t_span/2, 0, spatial_scale, 0)
    v3: (t_span/2, 0, 0, spatial_scale)
    v4: (t_span, 0, 0, 0) -> timelike edge (0, 4) with s^2 = -t_span^2 < 0.
    """
    vertices = {
        0: np.array([0.0, 0.0, 0.0, 0.0]),
        1: np.array([0.5 * t_span, spatial_scale, 0.0, 0.0]),
        2: np.array([0.5 * t_span, 0.0, spatial_scale, 0.0]),
        3: np.array([0.5 * t_span, 0.0, 0.0, spatial_scale]),
        4: np.array([t_span, 0.0, 0.0, 0.0]),
    }
    sigma = (0, 1, 2, 3, 4)
    return Lorentzian4Complex(vertices=vertices, four_simplices=[sigma])


def build_two_adjacent_lorentzian_4simplices(
    t_span: float = 2.0,
    spatial_scale: float = 1.0,
) -> Lorentzian4Complex:
    """Build two 4-simplices glued along a common boundary tetrahedron.

    Simplex 1: (0, 1, 2, 3, 4)
    Simplex 2: (1, 2, 3, 4, 5) where v5 is reflected spatially.
    Common hinge interface is the tetrahedron (1, 2, 3, 4).
    """
    vertices = {
        0: np.array([0.0, 0.0, 0.0, 0.0]),
        1: np.array([0.5 * t_span, spatial_scale, 0.0, 0.0]),
        2: np.array([0.5 * t_span, 0.0, spatial_scale, 0.0]),
        3: np.array([0.5 * t_span, 0.0, 0.0, spatial_scale]),
        4: np.array([t_span, 0.0, 0.0, 0.0]),
        5: np.array([0.5 * t_span, -spatial_scale, -spatial_scale, -spatial_scale]),
    }
    s1 = (0, 1, 2, 3, 4)
    s2 = (1, 2, 3, 4, 5)
    return Lorentzian4Complex(vertices=vertices, four_simplices=[s1, s2])
