"""
Higher-Order Simplicial Cohomology (k >= 3) on Regge Simplicial Complexes
AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e)

Mechanizes:
1. Higher-Order Simplicial Chain Complex (C_k, partial_k) for k in {0, 1, 2, 3, 4}:
   - C_0: Vertices (N0)
   - C_1: Edges (N1)
   - C_2: Triangles (N2)
   - C_3: Tetrahedra (N3)
   - C_4: 4-simplices (N4)
2. Stokes Boundary Nilpotency for k >= 3:
   - B_2 * B_3 = 0 (edges x tetrahedra via triangles)
   - B_3 * B_4 = 0 (triangles x 4-simplices via tetrahedra)
3. Stokes Coboundary Nilpotency:
   - delta_2 o delta_1 = 0
   - delta_3 o delta_2 = 0
4. Combinatorial Hodge Laplacians:
   - Delta_k = B_k^T * B_k + B_{k+1} * B_{k+1}^T for k in {0, 1, 2, 3, 4}
   - Harmonic cochain space dim(ker Delta_k) = beta_k
5. Topological Invariance under 1->5, 2->4, and 3->3 Pachner Bistellar Surgeries:
   - Preserves Euler characteristic chi = N0 - N1 + N2 - N3 + N4
   - Preserves Betti numbers beta_k and boundary nilpotency.
"""

from __future__ import annotations

import itertools
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Optional, Set, Tuple

import numpy as np


@dataclass(frozen=True)
class HigherOrderReggeReceipt:
    """Certified receipt of higher-order simplicial boundary nilpotency and cohomology."""

    num_vertices: int
    num_edges: int
    num_triangles: int
    num_tetrahedra: int
    num_four_simplices: int
    euler_characteristic: int
    is_b1_b2_nilpotent: bool
    is_b2_b3_nilpotent: bool
    is_b3_b4_nilpotent: bool
    is_delta1_delta0_nilpotent: bool
    is_delta2_delta1_nilpotent: bool
    is_delta3_delta2_nilpotent: bool
    betti_numbers: Tuple[int, int, int, int, int]
    hodge_laplacian_ranks: Tuple[int, int, int, int, int]
    pachner_surgery_applied: Optional[str] = None
    authority_effect: str = "None"

    @property
    def is_all_nilpotent(self) -> bool:
        return (
            self.is_b1_b2_nilpotent
            and self.is_b2_b3_nilpotent
            and self.is_b3_b4_nilpotent
            and self.is_delta1_delta0_nilpotent
            and self.is_delta2_delta1_nilpotent
            and self.is_delta3_delta2_nilpotent
        )


class HigherOrderSimplicialComplex:
    """
    Combinatorial 4D Regge Simplicial Manifold supporting higher-order
    chain complexes C_0, C_1, C_2, C_3, C_4 and Pachner moves.
    """

    def __init__(self, four_simplices: Optional[Set[Tuple[int, ...]]] = None):
        if four_simplices is None:
            # Seed: standard 4-sphere S^4 as boundary of a 5-simplex (6 vertices, 6 4-simplices)
            self.four_simplices: Set[Tuple[int, ...]] = {
                tuple(sorted(c)) for c in itertools.combinations(range(6), 5)
            }
        else:
            self.four_simplices = {tuple(sorted(s)) for s in four_simplices}

    @property
    def vertices(self) -> List[int]:
        return sorted({v for s in self.four_simplices for v in s})

    @property
    def num_vertices(self) -> int:
        return len(self.vertices)

    @property
    def edges(self) -> List[Tuple[int, int]]:
        edge_set = {
            tuple(sorted(e)) for s in self.four_simplices for e in itertools.combinations(s, 2)
        }
        return sorted(edge_set)

    @property
    def num_edges(self) -> int:
        return len(self.edges)

    @property
    def triangles(self) -> List[Tuple[int, int, int]]:
        tri_set = {
            tuple(sorted(t)) for s in self.four_simplices for t in itertools.combinations(s, 3)
        }
        return sorted(tri_set)

    @property
    def num_triangles(self) -> int:
        return len(self.triangles)

    @property
    def tetrahedra(self) -> List[Tuple[int, int, int, int]]:
        tet_set = {
            tuple(sorted(t)) for s in self.four_simplices for t in itertools.combinations(s, 4)
        }
        return sorted(tet_set)

    @property
    def num_tetrahedra(self) -> int:
        return len(self.tetrahedra)

    @property
    def four_simplices_list(self) -> List[Tuple[int, ...]]:
        return sorted(self.four_simplices)

    @property
    def num_four_simplices(self) -> int:
        return len(self.four_simplices)

    @property
    def euler_characteristic(self) -> int:
        """Euler characteristic chi = N0 - N1 + N2 - N3 + N4."""
        return (
            self.num_vertices
            - self.num_edges
            + self.num_triangles
            - self.num_tetrahedra
            + self.num_four_simplices
        )

    # -------------------------------------------------------------------------
    # Pachner Bistellar Moves in 4D
    # -------------------------------------------------------------------------

    def apply_1_to_5_move(self) -> bool:
        """
        1->5 Pachner move: Stellar subdivision of a 4-simplex.
        Inserts new vertex, replaces 1 4-simplex with 5 4-simplices.
        Delta N0 = +1, Delta N4 = +4, Delta chi = 0.
        """
        if not self.four_simplices:
            return False
        s0 = sorted(self.four_simplices)[0]
        new_v = max(self.vertices) + 1
        self.four_simplices.remove(s0)
        for tet in itertools.combinations(s0, 4):
            self.four_simplices.add(tuple(sorted(tet + (new_v,))))
        return True

    def apply_2_to_4_move(self) -> bool:
        """
        2->4 Pachner bistellar move:
        Finds two 4-simplices s1, s2 sharing a common interior tetrahedron t = s1 cap s2.
        Replaces {s1, s2} with 4 simplices by inserting transverse edge (u, v).
        Delta N4 = +2, Delta chi = 0.
        """
        tet_to_simplices = defaultdict(list)
        for s in self.four_simplices:
            for tet in itertools.combinations(s, 4):
                tet_to_simplices[tuple(sorted(tet))].append(s)

        for tet, simplices in tet_to_simplices.items():
            if len(simplices) == 2:
                s1, s2 = simplices
                u_set = set(s1) - set(tet)
                v_set = set(s2) - set(tet)
                if len(u_set) == 1 and len(v_set) == 1:
                    u = next(iter(u_set))
                    v = next(iter(v_set))
                    transverse_edge = tuple(sorted((u, v)))
                    if transverse_edge not in self.edges:
                        self.four_simplices.remove(s1)
                        self.four_simplices.remove(s2)
                        for face in itertools.combinations(tet, 3):
                            new_s = tuple(sorted(face + (u, v)))
                            self.four_simplices.add(new_s)
                        return True
        return False

    def apply_3_to_3_move(self) -> bool:
        """
        3->3 Pachner bistellar topological flip:
        Replaces 3 4-simplices sharing an interior triangle with 3 sharing the dual triangle.
        Delta N4 = 0, Delta chi = 0.
        """
        tri_to_simplices = defaultdict(list)
        for s in self.four_simplices:
            for tri in itertools.combinations(s, 3):
                tri_to_simplices[tuple(sorted(tri))].append(s)

        for tri, simplices in tri_to_simplices.items():
            if len(simplices) == 3:
                all_v = set().union(*simplices)
                opp = all_v - set(tri)
                if len(opp) == 3:
                    dual_tri = tuple(sorted(opp))
                    if dual_tri not in self.triangles:
                        for s in list(simplices):
                            self.four_simplices.remove(s)
                        for edge in itertools.combinations(tri, 2):
                            new_s = tuple(sorted(edge + dual_tri))
                            self.four_simplices.add(new_s)
                        return True
        return False

    # -------------------------------------------------------------------------
    # Exact Simplicial Boundary Matrices
    # -------------------------------------------------------------------------

    def build_boundary_matrices(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Constructs exact integer boundary matrices B_1, B_2, B_3, B_4.
        Standard simplicial orientation:
        partial [v_0, ..., v_p] = sum_{i=0}^p (-1)^i [v_0, ..., hat{v}_i, ..., v_p]
        """
        verts = self.vertices
        edges = self.edges
        tris = self.triangles
        tets = self.tetrahedra
        fours = self.four_simplices_list

        v_map = {v: i for i, v in enumerate(verts)}
        e_map = {e: j for j, e in enumerate(edges)}
        t_map = {t: k for k, t in enumerate(tris)}
        tet_map = {tet: m for m, tet in enumerate(tets)}
        {f: n for n, f in enumerate(fours)}

        n0, n1, n2, n3, n4 = len(verts), len(edges), len(tris), len(tets), len(fours)

        # B_1: C_1 -> C_0 (N0 x N1)
        b1 = np.zeros((n0, n1), dtype=np.int64)
        for j, (u, v) in enumerate(edges):
            b1[v_map[v], j] += 1
            b1[v_map[u], j] -= 1

        # B_2: C_2 -> C_1 (N1 x N2)
        b2 = np.zeros((n1, n2), dtype=np.int64)
        for k, tri in enumerate(tris):
            # faces: (v1, v2) with +1, (v0, v2) with -1, (v0, v1) with +1
            b2[e_map[(tri[1], tri[2])], k] += 1
            b2[e_map[(tri[0], tri[2])], k] -= 1
            b2[e_map[(tri[0], tri[1])], k] += 1

        # B_3: C_3 -> C_2 (N2 x N3)
        b3 = np.zeros((n2, n3), dtype=np.int64)
        for m, tet in enumerate(tets):
            # partial [v0, v1, v2, v3] = sum_{i=0}^3 (-1)^i face_i
            faces_3 = [
                (tet[1], tet[2], tet[3]),  # i=0, sign +1
                (tet[0], tet[2], tet[3]),  # i=1, sign -1
                (tet[0], tet[1], tet[3]),  # i=2, sign +1
                (tet[0], tet[1], tet[2]),  # i=3, sign -1
            ]
            for i, f in enumerate(faces_3):
                sign = 1 if i % 2 == 0 else -1
                b3[t_map[f], m] += sign

        # B_4: C_4 -> C_3 (N3 x N4)
        b4 = np.zeros((n3, n4), dtype=np.int64)
        for n, four in enumerate(fours):
            # partial [v0, v1, v2, v3, v4] = sum_{i=0}^4 (-1)^i tet_i
            faces_4 = [
                (four[1], four[2], four[3], four[4]),  # i=0, sign +1
                (four[0], four[2], four[3], four[4]),  # i=1, sign -1
                (four[0], four[1], four[3], four[4]),  # i=2, sign +1
                (four[0], four[1], four[2], four[4]),  # i=3, sign -1
                (four[0], four[1], four[2], four[3]),  # i=4, sign +1
            ]
            for i, f in enumerate(faces_4):
                sign = 1 if i % 2 == 0 else -1
                b4[tet_map[f], n] += sign

        return b1, b2, b3, b4

    # -------------------------------------------------------------------------
    # Hodge Laplacians & Betti Numbers
    # -------------------------------------------------------------------------

    def compute_hodge_laplacians(
        self,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Computes combinatorial Hodge Laplacians Delta_k = B_k^T B_k + B_{k+1} B_{k+1}^T.
        Delta_0 = B_1 B_1^T
        Delta_1 = B_1^T B_1 + B_2 B_2^T
        Delta_2 = B_2^T B_2 + B_3 B_3^T
        Delta_3 = B_3^T B_3 + B_4 B_4^T
        Delta_4 = B_4^T B_4
        """
        b1, b2, b3, b4 = self.build_boundary_matrices()

        d0 = b1 @ b1.T
        d1 = b1.T @ b1 + b2 @ b2.T
        d2 = b2.T @ b2 + b3 @ b3.T
        d3 = b3.T @ b3 + b4 @ b4.T
        d4 = b4.T @ b4

        return d0, d1, d2, d3, d4

    def compute_betti_numbers(self) -> Tuple[int, int, int, int, int]:
        """
        Computes exact simplicial cohomology Betti numbers beta_k = dim H^k.
        Uses rank decomposition: beta_k = dim ker B_k - rank B_{k+1}.
        """
        b1, b2, b3, b4 = self.build_boundary_matrices()

        r1 = int(np.linalg.matrix_rank(b1))
        r2 = int(np.linalg.matrix_rank(b2))
        r3 = int(np.linalg.matrix_rank(b3))
        r4 = int(np.linalg.matrix_rank(b4))

        n0 = self.num_vertices
        n1 = self.num_edges
        n2 = self.num_triangles
        n3 = self.num_tetrahedra
        n4 = self.num_four_simplices

        # beta_0 = dim ker B_0 - rank B_1 = n0 - r1 (since B_0 = 0)
        beta_0 = n0 - r1
        # beta_1 = dim ker B_1 - rank B_2 = (n1 - r1) - r2
        beta_1 = (n1 - r1) - r2
        # beta_2 = dim ker B_2 - rank B_3 = (n2 - r2) - r3
        beta_2 = (n2 - r2) - r3
        # beta_3 = dim ker B_3 - rank B_4 = (n3 - r3) - r4
        beta_3 = (n3 - r3) - r4
        # beta_4 = dim ker B_4 - rank B_5 = (n4 - r4) - 0 (since B_5 = 0)
        beta_4 = n4 - r4

        return (beta_0, beta_1, beta_2, beta_3, beta_4)

    # -------------------------------------------------------------------------
    # Comprehensive Audit Receipt
    # -------------------------------------------------------------------------

    def evaluate_higher_order_cohomology(
        self, surgery_label: Optional[str] = None
    ) -> HigherOrderReggeReceipt:
        """
        Executes formal audit of higher-order simplicial boundary nilpotency (k >= 3)
        and cohomology invariance on the 4D Regge simplicial manifold.
        """
        b1, b2, b3, b4 = self.build_boundary_matrices()

        # Boundary nilpotency products
        p12 = b1 @ b2
        p23 = b2 @ b3
        p34 = b3 @ b4

        is_b1_b2_nil = bool(np.all(p12 == 0))
        is_b2_b3_nil = bool(np.all(p23 == 0))
        is_b3_b4_nil = bool(np.all(p34 == 0))

        # Coboundary nilpotency (delta_k = B_{k+1}^T)
        # delta_1 o delta_0 = B_2^T B_1^T = (B_1 B_2)^T
        is_d1_d0_nil = bool(np.all(b2.T @ b1.T == 0))
        # delta_2 o delta_1 = B_3^T B_2^T = (B_2 B_3)^T
        is_d2_d1_nil = bool(np.all(b3.T @ b2.T == 0))
        # delta_3 o delta_2 = B_4^T B_3^T = (B_3 B_4)^T
        is_d3_d2_nil = bool(np.all(b4.T @ b3.T == 0))

        d0, d1, d2, d3, d4 = self.compute_hodge_laplacians()
        hodge_ranks = (
            int(np.linalg.matrix_rank(d0)),
            int(np.linalg.matrix_rank(d1)),
            int(np.linalg.matrix_rank(d2)),
            int(np.linalg.matrix_rank(d3)),
            int(np.linalg.matrix_rank(d4)),
        )

        betti = self.compute_betti_numbers()

        return HigherOrderReggeReceipt(
            num_vertices=self.num_vertices,
            num_edges=self.num_edges,
            num_triangles=self.num_triangles,
            num_tetrahedra=self.num_tetrahedra,
            num_four_simplices=self.num_four_simplices,
            euler_characteristic=self.euler_characteristic,
            is_b1_b2_nilpotent=is_b1_b2_nil,
            is_b2_b3_nilpotent=is_b2_b3_nil,
            is_b3_b4_nilpotent=is_b3_b4_nil,
            is_delta1_delta0_nilpotent=is_d1_d0_nil,
            is_delta2_delta1_nilpotent=is_d2_d1_nil,
            is_delta3_delta2_nilpotent=is_d3_d2_nil,
            betti_numbers=betti,
            hodge_laplacian_ranks=hodge_ranks,
            pachner_surgery_applied=surgery_label,
            authority_effect="None",
        )
