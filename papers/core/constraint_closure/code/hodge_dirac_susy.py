"""SP2: Finite Hodge-Dirac fixtures on one and two filled triangles.

Implements exact construction of the Hodge-Dirac operator D on the Z2-graded
space (C^0 ⊕ C^2) ⊕ C^1, verifying D^2 = (Δ_0 ⊕ Δ_2) ⊕ Δ_1^filled.

Computed matrix identities on the single filled 2-simplex Δ^2:
  - Nilpotency: d1 d0 = 0
  - Δ_1^filled = d0 d0^T + d1^T d1 = 3 I_3
  - Even eigenvalues: {0, 3, 3, 3}
  - Odd eigenvalues: {3, 3, 3}
  - Witten index: W = 1 = χ(Δ^2)

Spectral splitting fence (two glued triangles):
  - Δ_1^filled eigenvalues: {2, 2, 4, 4, 4}, mass gap λ = 2

AuthorityEffect: None.
"""

from __future__ import annotations

import numpy as np


def build_operators_single_simplex():
    """Build d0 (3x3) and d1 (1x3) for the filled 2-simplex Δ^2.

    Vertices: v0, v1, v2
    Edges: e0=(v0,v1), e1=(v1,v2), e2=(v2,v0)
    Face: f=(v0,v1,v2) with boundary e0 + e1 + e2
    """
    d0 = np.array([[-1, 1, 0], [0, -1, 1], [1, 0, -1]], dtype=float)
    d1 = np.array([[1, 1, 1]], dtype=float)
    return d0, d1


def build_operators_glued_triangles():
    """Build d0 (5x4) and d1 (2x5) for two triangles sharing edge e0.

    Vertices: v0, v1, v2, v3
    Edges: e0=(v0,v1), e1=(v1,v2), e2=(v2,v0), e3=(v1,v3), e4=(v3,v0)
    Face f0=(v0,v1,v2): boundary e0 + e1 + e2
    Face f1=(v0,v1,v3): boundary e0 + e3 + e4
    """
    d0 = np.array(
        [
            [-1, 1, 0, 0],
            [0, -1, 1, 0],
            [1, 0, -1, 0],
            [0, -1, 0, 1],
            [1, 0, 0, -1],
        ],
        dtype=float,
    )
    d1 = np.array(
        [
            [1, 1, 1, 0, 0],
            [1, 0, 0, 1, 1],
        ],
        dtype=float,
    )
    return d0, d1


def build_dirac_operator(d0: np.ndarray, d1: np.ndarray) -> np.ndarray:
    """Build the full de Rham Dirac operator D on (C^0 ⊕ C^2) ⊕ C^1.

    D = [[0,      0,    d0^T],
         [0,      0,    d1  ],
         [d0,   d1^T,   0   ]]

    Dimensions: (n_vert + n_face) + n_edge = total
    """
    n_edge, n_vert = d0.shape
    n_face = d1.shape[0]
    n_even = n_vert + n_face
    n_total = n_even + n_edge

    D = np.zeros((n_total, n_total), dtype=float)

    D[:n_vert, n_even:] = d0.T
    D[n_vert:n_even, n_even:] = d1

    D[n_even:, :n_vert] = d0
    D[n_even:, n_vert:n_even] = d1.T

    return D


def compute_laplacians(d0: np.ndarray, d1: np.ndarray) -> dict:
    """Compute all Hodge Laplacians and their eigenvalues.

    Returns:
      Delta_0 = d0^T d0
      Delta_2 = d1 d1^T
      Delta_1_filled = d0 d0^T + d1^T d1
      eigenvalues for each
    """
    Delta_0 = d0.T @ d0
    Delta_2 = d1 @ d1.T
    Delta_1_hollow = d0 @ d0.T
    Delta_1_curl = d1.T @ d1
    Delta_1_filled = Delta_1_hollow + Delta_1_curl

    evals_0 = np.sort(np.linalg.eigvalsh(Delta_0))
    evals_2 = np.sort(np.linalg.eigvalsh(Delta_2))
    evals_1 = np.sort(np.linalg.eigvalsh(Delta_1_filled))

    evals_even = np.sort(np.concatenate([evals_0, evals_2]))

    n_zero_even = np.sum(np.abs(evals_even) < 1e-10)
    n_zero_odd = np.sum(np.abs(evals_1) < 1e-10)
    witten_index = int(n_zero_even - n_zero_odd)

    return {
        "Delta_0": Delta_0,
        "Delta_2": Delta_2,
        "Delta_1_filled": Delta_1_filled,
        "Delta_1_hollow": Delta_1_hollow,
        "Delta_1_curl": Delta_1_curl,
        "evals_0": evals_0,
        "evals_2": evals_2,
        "evals_1": evals_1,
        "evals_even": evals_even,
        "witten_index": witten_index,
    }


def verify_susy_single_simplex() -> dict:
    """Complete verification of Hodge-Dirac supersymmetry on Δ^2."""
    d0, d1 = build_operators_single_simplex()

    nilpotent = np.allclose(d1 @ d0, 0)

    laps = compute_laplacians(d0, d1)

    D = build_dirac_operator(d0, d1)
    D2 = D @ D
    n_vert = 3
    n_face = 1
    n_edge = 3
    n_even = n_vert + n_face
    D2_expected = np.block([
        [laps["Delta_0"], np.zeros((n_vert, n_face)), np.zeros((n_vert, n_edge))],
        [np.zeros((n_face, n_vert)), laps["Delta_2"], np.zeros((n_face, n_edge))],
        [np.zeros((n_edge, n_vert)), np.zeros((n_edge, n_face)), laps["Delta_1_filled"]],
    ])
    d2_matches = np.allclose(D2, D2_expected)

    self_adjoint = np.allclose(D, D.T)

    Gamma = np.diag([1] * n_even + [-1] * n_edge)
    anticommutes = np.allclose(D @ Gamma + Gamma @ D, 0)

    rank_d0 = np.linalg.matrix_rank(d0)
    dim_ker_d0_star = n_edge - rank_d0
    dim_h1_hollow = n_edge - np.linalg.matrix_rank(d0)
    rank_d1 = np.linalg.matrix_rank(d1)
    dim_h1_filled = n_edge - np.linalg.matrix_rank(d0) - rank_d1

    return {
        "nilpotent": nilpotent,
        "D2_matches_block_diagonal": d2_matches,
        "self_adjoint": self_adjoint,
        "anticommutes_with_grading": anticommutes,
        "Delta_1_filled_is_3I": np.allclose(laps["Delta_1_filled"], 3 * np.eye(3)),
        "evals_even": laps["evals_even"].tolist(),
        "evals_odd": laps["evals_1"].tolist(),
        "witten_index": laps["witten_index"],
        "h1_hollow": dim_h1_hollow,
        "h1_filled": dim_h1_filled,
    }


def verify_spectral_splitting_glued() -> dict:
    """Verify spectral splitting on two glued triangles."""
    d0, d1 = build_operators_glued_triangles()
    laps = compute_laplacians(d0, d1)
    return {
        "evals_1": np.sort(np.round(laps["evals_1"], 10)).tolist(),
        "mass_gap": float(np.min(laps["evals_1"][laps["evals_1"] > 1e-10])),
        "is_scalar_isotropic": np.allclose(
            laps["Delta_1_filled"],
            laps["Delta_1_filled"][0, 0] * np.eye(len(laps["Delta_1_filled"])),
        ),
    }
