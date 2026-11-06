"""SP5c: Wheel-disk cohomology and boundary-capacity fixtures.

Computes absolute H^1=0 for a family of wheel disks.  Passing from that
calculation to relative cohomology uses a separately supplied duality theorem;
it is not implemented by the matrices below.
Boundary capacity on C3 is 4 (not 2|E| = 6).
Microstate locking claims retracted on contractible complexes.

AuthorityEffect: None.
"""

from __future__ import annotations

import numpy as np


def build_wheel_disk(n_outer: int = 6) -> tuple[np.ndarray, np.ndarray]:
    """Build a contractible 2-disk: wheel graph with center + n_outer boundary vertices.

    Vertices: v0 (center), v1..v_n (boundary)
    Edges: radial e_i = (v0, v_i) for i=1..n, boundary e_{n+i} = (v_i, v_{i+1 mod n})
    Faces: f_i = (v0, v_i, v_{i+1 mod n}) for i=1..n
    """
    n_verts = 1 + n_outer
    n_radial = n_outer
    n_boundary = n_outer
    n_edges = n_radial + n_boundary
    n_faces = n_outer

    d0 = np.zeros((n_edges, n_verts), dtype=float)
    for i in range(n_outer):
        d0[i, 0] = -1
        d0[i, i + 1] = 1

    for i in range(n_outer):
        src = i + 1
        tgt = (i + 1) % n_outer + 1
        d0[n_radial + i, src] = -1
        d0[n_radial + i, tgt] = 1

    d1 = np.zeros((n_faces, n_edges), dtype=float)
    for i in range(n_outer):
        d1[i, i] = 1
        d1[i, n_radial + i] = 1
        d1[i, (i + 1) % n_outer] = -1

    return d0, d1


def absolute_h1_dimension(d0: np.ndarray, d1: np.ndarray) -> dict:
    """Compute dim H^1 of the supplied finite cochain complex by ranks."""
    n_edges = d0.shape[0]

    rank_d0 = np.linalg.matrix_rank(d0)
    rank_d1 = np.linalg.matrix_rank(d1)

    dim_h1 = n_edges - rank_d0 - rank_d1

    return {
        "n_edges": n_edges,
        "rank_d0": rank_d0,
        "rank_d1": rank_d1,
        "dim_H1": dim_h1,
        "is_zero": dim_h1 == 0,
    }


def boundary_capacity_triangle() -> dict:
    """Compute boundary capacity on triangle C3.

    C_∂Ω = sup_{||α||_∞ ≤ 1} ||(d0 α)|_∂Ω||_1

    On C3 (odd cycle), the supremum is 4 (not 2|E| = 6).
    """
    d0 = np.array([[-1, 1, 0], [0, -1, 1], [1, 0, -1]], dtype=float)

    max_cap = 0.0
    max_alpha = None

    for a0 in [-1, 1]:
        for a1 in [-1, 1]:
            for a2 in [-1, 1]:
                alpha = np.array([a0, a1, a2], dtype=float)
                d0_alpha = d0 @ alpha
                cap = np.sum(np.abs(d0_alpha))
                if cap > max_cap:
                    max_cap = cap
                    max_alpha = alpha.copy()

    return {
        "capacity": max_cap,
        "claimed_2E": 2 * 3,
        "capacity_is_4_not_6": abs(max_cap - 4.0) < 1e-10,
        "maximizer": max_alpha.tolist() if max_alpha is not None else None,
    }


def verify_horizon_fence() -> dict:
    """Evaluate the wheel-disk and triangle-capacity fixtures."""
    d0, d1 = build_wheel_disk(6)

    nilpotent = np.allclose(d1 @ d0, 0)

    absolute_h1 = absolute_h1_dimension(d0, d1)

    cap = boundary_capacity_triangle()

    return {
        "nilpotent": nilpotent,
        "absolute_h1": absolute_h1,
        "relative_h1_status": "requires_external_duality_transport",
        "boundary_capacity": cap,
        "scope": (
            "Absolute H1 of the supplied wheel disk is zero and the declared "
            "C3 capacity is 4. Relative H1 needs an external duality bridge."
        ),
    }
