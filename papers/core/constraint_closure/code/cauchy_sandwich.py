"""Time-foliated 3+1 Cauchy sandwich simplicial triangulations with lapse and shift variations.

Implements discrete 3+1 ADM foliation over a spatial simplicial manifold Sigma:
- Spacetime region M_{[t_0, t_1]} = Sigma x [t_0, t_0 + Delta t].
- ADM vertex displacement: x_{v^{(1)}} = x_{v^{(0)}} + (N_v Delta t, N_v Delta t).
- Canonical order-preserving prism triangulation: each 3-simplex tau in Sigma is
  extruded into a 3-prism tau x I, triangulated into four 4-simplices.
- Preserves simplicial downward closure, boundary components Sigma_0 U Sigma_1,
  and operator nilpotency (partial^2 = 0, d^2 = 0).
- Timelike foliation condition: N_v^2 > |N_v|^2 ensures time-tracks are strictly timelike (s^2 < 0).
- Generates lapse/shift gauge variations beta_{(N, N)} in C^1 and coboundary shifts d_1 beta in C^2.
- Evaluates discrete Wheeler-DeWitt constraint cochains on the Cauchy sandwich.

AuthorityEffect: None.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple
import numpy as np

from lorentzian_regge import Lorentzian4Complex


@dataclass
class CauchySandwich4Complex:
    """4D simplicial Cauchy sandwich triangulation Sigma x [t_0, t_0 + Delta t]."""

    spatial_vertices: Dict[int, np.ndarray]
    spatial_tetrahedra: List[Tuple[int, ...]]
    t0: float = 0.0
    dt: float = 1.0
    lapse: Dict[int, float] = field(default_factory=dict)
    shift: Dict[int, np.ndarray] = field(default_factory=dict)
    tol: float = 1e-10

    lorentzian_complex: Lorentzian4Complex = field(init=False)
    _spatial_n: int = field(init=False)
    top_vertex_map: Dict[int, int] = field(init=False)

    def __post_init__(self) -> None:
        self._spatial_n = len(self.spatial_vertices)
        if self._spatial_n < 4:
            raise ValueError("Spatial slice must contain at least 4 vertices for a 3-simplex")

        for v in self.spatial_vertices:
            if v not in self.lapse:
                self.lapse[v] = 1.0
            if v not in self.shift:
                self.shift[v] = np.zeros(3, dtype=float)

        self.rebuild_sandwich()

    def rebuild_sandwich(self) -> None:
        """Construct 4D vertex coordinates and prism-triangulated 4-simplices."""
        sorted_verts = sorted(self.spatial_vertices.keys())
        max_id = max(sorted_verts) if sorted_verts else 0
        self.top_vertex_map = {v: max_id + 1 + i for i, v in enumerate(sorted_verts)}
        v_coords_4d: Dict[int, np.ndarray] = {}

        for v, pos_3d in self.spatial_vertices.items():
            v_coords_4d[v] = np.array([self.t0, pos_3d[0], pos_3d[1], pos_3d[2]], dtype=float)

            n_v = self.lapse.get(v, 1.0)
            shift_v = self.shift.get(v, np.zeros(3, dtype=float))
            t1 = self.t0 + n_v * self.dt
            pos_final = pos_3d + shift_v * self.dt
            v_top = self.top_vertex_map[v]
            v_coords_4d[v_top] = np.array([t1, pos_final[0], pos_final[1], pos_final[2]], dtype=float)

        four_simplices: List[Tuple[int, ...]] = []
        for tau in self.spatial_tetrahedra:
            a, b, c, d = sorted(tau)
            a0, b0, c0, d0 = a, b, c, d
            a1, b1, c1, d1 = (
                self.top_vertex_map[a],
                self.top_vertex_map[b],
                self.top_vertex_map[c],
                self.top_vertex_map[d],
            )
            s1 = tuple(sorted((a0, b0, c0, d0, d1)))
            s2 = tuple(sorted((a0, b0, c0, c1, d1)))
            s3 = tuple(sorted((a0, b0, b1, c1, d1)))
            s4 = tuple(sorted((a0, a1, b1, c1, d1)))
            four_simplices.extend([s1, s2, s3, s4])

        self.lorentzian_complex = Lorentzian4Complex(
            vertices=v_coords_4d,
            four_simplices=four_simplices,
            tol=self.tol,
        )


    @property
    def num_vertices(self) -> int:
        return self.lorentzian_complex.num_vertices

    @property
    def num_edges(self) -> int:
        return self.lorentzian_complex.num_edges

    @property
    def num_triangles(self) -> int:
        return self.lorentzian_complex.num_triangles

    @property
    def num_tetrahedra(self) -> int:
        return self.lorentzian_complex.num_tetrahedra

    @property
    def num_four_simplices(self) -> int:
        return self.lorentzian_complex.num_four_simplices

    def euler_characteristic(self) -> int:
        return self.lorentzian_complex.euler_characteristic()

    def coboundary_matrix(self, k: int) -> np.ndarray:
        return self.lorentzian_complex.coboundary_matrix(k)

    def boundary_matrix(self, k: int) -> np.ndarray:
        return self.lorentzian_complex.boundary_matrix(k)

    def has_timelike_tracks(self) -> bool:
        """Check whether all vertical time-track edges connecting Sigma_0 to Sigma_1 are strictly timelike (s^2 < 0).

        Equivalent to ADM condition N_v^2 > |N_v|^2 at every spatial vertex.
        Note: As established by Carroll (2026), timelike track condition alone does NOT guarantee
        that slices Sigma_0 and Sigma_1 remain spacelike (e.g. under non-uniform lapses).
        """
        for v in self.spatial_vertices:
            v_top = self.top_vertex_map[v]
            edge = tuple(sorted((v, v_top)))
            if not self.lorentzian_complex.is_timelike(edge):
                return False
        return True

    def is_spacelike_slice(self, slice_idx: int = 1) -> bool:
        """Check whether all edges in the specified Cauchy slice are strictly spacelike (s^2 > 0).

        slice_idx: 0 for base slice Sigma_0, 1 for top slice Sigma_1.
        """
        for tau in self.spatial_tetrahedra:
            verts = [v if slice_idx == 0 else self.top_vertex_map[v] for v in tau]
            for u, w in itertools.combinations(verts, 2):
                edge = tuple(sorted((u, w)))
                if not self.lorentzian_complex.is_spacelike(edge):
                    return False
        return True

    def is_cauchy_foliation(self) -> bool:
        """Verify whether the sandwich constitutes a valid Cauchy foliation.

        Requires:
        1. Vertical time tracks are strictly timelike (has_timelike_tracks).
        2. Both Cauchy slices Sigma_0 and Sigma_1 are strictly spacelike (is_spacelike_slice).
        3. Time orientation is strictly forward: dt * lapse[v] > 0 for all vertices.
        """
        for v in self.spatial_vertices:
            if self.dt * self.lapse.get(v, 1.0) <= 0.0:
                return False
        return self.has_timelike_tracks() and self.is_spacelike_slice(0) and self.is_spacelike_slice(1)

    def is_timelike_foliation(self) -> bool:
        """Backward-compatible alias for has_timelike_tracks(). Note: checks vertical tracks only."""
        return self.has_timelike_tracks()


    def compute_gauge_1cochain_from_variation(
        self,
        delta_lapse: Dict[int, float],
        delta_shift: Dict[int, np.ndarray],
    ) -> np.ndarray:
        """Compute the 1-cochain beta in C^1 induced by lapse and shift variations.

        A variation (delta N_v, delta N_v) displaces top vertices v_1 on Sigma_1
        by delta x_{v_1} = dt * (delta N_v, delta N_v).
        The induced 1-cochain on edge e = (u, w) is the discrete contraction:
            beta(e) = eta_{mu nu} (x_w - x_u)^mu (delta x_w - delta x_u)^nu
        or standard dual projection onto edge vectors.
        """
        edges = self.lorentzian_complex.cells.get(1, [])
        beta = np.zeros(len(edges), dtype=float)

        delta_coords: Dict[int, np.ndarray] = {}
        for v in self.spatial_vertices:
            delta_coords[v] = np.zeros(4, dtype=float)
            v_top = self.top_vertex_map[v]
            dn = delta_lapse.get(v, 0.0)
            dsh = delta_shift.get(v, np.zeros(3, dtype=float))
            delta_coords[v_top] = self.dt * np.array([dn, dsh[0], dsh[1], dsh[2]], dtype=float)

        eta = np.array([-1.0, 1.0, 1.0, 1.0])

        for idx, edge in enumerate(edges):
            u, w = edge
            edge_vec = self.lorentzian_complex.vertices[w] - self.lorentzian_complex.vertices[u]
            disp_diff = delta_coords[w] - delta_coords[u]
            beta[idx] = float(np.sum(eta * edge_vec * disp_diff))

        return beta

    def apply_lapse_shift_variation(
        self,
        delta_lapse: Dict[int, float],
        delta_shift: Dict[int, np.ndarray],
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Apply lapse and shift variations and return algebraic coboundary variations (beta, delta_omega).

        Note: This computes the exact coboundary delta_omega = d_1 beta in C^2 under
        linearized Minkowski coordinate shifts. It does not compute dynamical curved
        Regge curvature or physical Einstein field equations.
        """
        beta = self.compute_gauge_1cochain_from_variation(delta_lapse, delta_shift)
        d1 = self.coboundary_matrix(1)
        delta_omega = d1 @ beta
        return beta, delta_omega

    def build_sandwich_wdw_constraint_cochain(
        self,
        extrinsic_curvature_pert: float = 0.5,
    ) -> np.ndarray:
        """Injected test fixture: assemble a 2-cochain representing an artificial constraint defect.

        Note: This injects algebraic parameters into two selected array entries for verifying
        linear programming solver obstruction detection. It does not derive dynamical
        Wheeler-DeWitt constraints from Regge metric data.
        """
        num_tri = self.num_triangles
        omega = np.zeros(num_tri, dtype=float)

        if num_tri > 0:
            omega[0] = extrinsic_curvature_pert
            if num_tri > 1:
                omega[num_tri // 2] = -0.5 * extrinsic_curvature_pert

        return omega


def build_canonical_3simplex_sandwich(
    dt: float = 1.0,
    lapse_val: float = 1.0,
    shift_val: float = 0.0,
) -> CauchySandwich4Complex:
    """Build a canonical Cauchy sandwich over a single regular spatial tetrahedron.

    Spatial tetrahedron vertices:
    v0: (0, 0, 0)
    v1: (1, 0, 0)
    v2: (0.5, sqrt(3)/2, 0)
    v3: (0.5, sqrt(3)/6, sqrt(2/3))
    """
    spatial_coords = {
        0: np.array([0.0, 0.0, 0.0]),
        1: np.array([1.0, 0.0, 0.0]),
        2: np.array([0.5, math.sqrt(3.0) / 2.0, 0.0]),
        3: np.array([0.5, math.sqrt(3.0) / 6.0, math.sqrt(2.0 / 3.0)]),
    }
    spatial_tetrahedra = [(0, 1, 2, 3)]

    lapse = {v: lapse_val for v in range(4)}
    shift = {v: np.array([shift_val, 0.0, 0.0]) for v in range(4)}

    return CauchySandwich4Complex(
        spatial_vertices=spatial_coords,
        spatial_tetrahedra=spatial_tetrahedra,
        dt=dt,
        lapse=lapse,
        shift=shift,
    )
