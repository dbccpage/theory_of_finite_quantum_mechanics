"""
Analytical Single-Cycle and Multi-Cycle Solutions and Separation Formulas.
Paper: GS-002 (so_k_invariant_gauge_classification)
"""

from __future__ import annotations
import math
from typing import Dict, Any, List, Optional, Tuple
import numpy as np

from carrier import Cochain
from gauges import StalkGauge


def compute_cycle_circulation(
    omega: Cochain, orientations: Optional[List[int] | np.ndarray] = None
) -> np.ndarray:
    """
    Compute total circulation vector S(omega) = sum_{e in C} eps_e * omega_e
    under general signed edge orientations eps_e in {+1, -1}.
    """
    if orientations is None:
        return np.sum(omega.data, axis=0)
    ori_list = list(orientations)
    if len(ori_list) != omega.num_cells:
        raise ValueError(
            f"Orientations length {len(ori_list)} does not match cochain cells {omega.num_cells}"
        )
    for x in ori_list:
        if not (isinstance(x, (int, np.integer)) and not isinstance(x, bool) and x in (+1, -1)):
            raise ValueError(
                f"Orientation sign must be +1 or -1 (got {x}); Orientations must be in {{+1, -1}}."
            )
    eps = np.array(ori_list, dtype=float)
    return np.sum(eps[:, None] * omega.data, axis=0)


def single_cycle_quotient_analytical(
    omega: Cochain,
    gauge: StalkGauge,
    edge_weights: Optional[np.ndarray | List[float]] = None,
    orientations: Optional[List[int] | np.ndarray] = None,
) -> float:
    """
    Evaluate exact quotient norm on a single directed cycle under general signed orientations:
        Phi_{j,w}([omega]) = (min_e w_e) * j(S(omega)).
    """
    if edge_weights is not None:
        w_arr = np.asarray(edge_weights, dtype=float)
        if w_arr.ndim != 1 or w_arr.shape != (omega.num_cells,):
            raise ValueError(
                f"Edge weights must have exact 1D shape ({omega.num_cells},); Edge weights length must match {omega.num_cells}, got shape {w_arr.shape}."
            )
        if not np.all(np.isfinite(w_arr)):
            raise ValueError("Edge weights must be finite.")
        if np.any(w_arr <= 0):
            raise ValueError(
                "Edge weights must be strictly positive (Slater condition violated: w_e <= 0)."
            )
        w_min = float(np.min(w_arr))
    else:
        w_min = 1.0

    circ = compute_cycle_circulation(omega, orientations=orientations)
    base_val = gauge(circ)
    return float(w_min * base_val)


def analyze_triangle_separation(
    edge_weights: Optional[List[float] | np.ndarray] = None,
) -> Dict[str, Any]:
    """
    Analyze the finite triangle separation (Theorem 5.2 / GS-002):
    V = {0, 1, 2}, E = {(0,1), (1,2), (2,0)}
    omega_{01} = (1, 0), omega_{12} = (0, 1), omega_{20} = (0, 0)
    Total circulation c = (1, 1).
    """
    if edge_weights is None:
        w = np.array([1.0, 1.0, 1.0], dtype=float)
    else:
        w = np.asarray(edge_weights, dtype=float)
        if w.ndim != 1 or w.shape != (3,):
            raise ValueError(
                f"analyze_triangle_separation requires exactly 3 edge weights with 1D shape (3,), got {w.shape}."
            )
        if not np.all(np.isfinite(w)):
            raise ValueError("Edge weights must be finite.")
        if np.any(w <= 0):
            raise ValueError("Edge weights must be strictly positive.")

    w_min = float(np.min(w))

    circ = np.array([1.0, 1.0])
    phi_11 = w_min * float(np.sum(np.abs(circ)))  # 2 * w_min
    phi_21 = w_min * float(np.linalg.norm(circ))  # sqrt(2) * w_min

    ratio = phi_11 / phi_21 if phi_21 > 0 else 0.0
    squared_ratio = (phi_11**2) / (phi_21**2) if phi_21 > 0 else 0.0

    return {
        "circulation": circ.tolist(),
        "edge_weights": w.tolist(),
        "w_min": w_min,
        "phi_11_coordinate_l1": phi_11,
        "phi_21_euclidean_so2": phi_21,
        "ratio": ratio,
        "squared_ratio": squared_ratio,
        "is_separated": abs(phi_11 - phi_21) > 1e-6,
    }


def analyze_dimension_scaling(
    dimensions: List[int], edge_count: int = 3
) -> List[Dict[str, Any]]:
    """
    Analyze observer separation as stalk dimension k increases for uniform diagonal defect:
        S(omega) = (1, 1, ..., 1) in R^k.
        Phi_{1,1} = k
        Phi_{2,1} = sqrt(k)
        Ratio = sqrt(k).
    """
    if isinstance(edge_count, bool) or not isinstance(edge_count, (int, np.integer)) or edge_count < 1:
        raise ValueError(f"edge_count must be integer >= 1 (got {edge_count}).")
    results = []
    for k in dimensions:
        if isinstance(k, bool) or not isinstance(k, (int, np.integer)) or k < 1:
            raise ValueError(f"Stalk dimension k must be positive integer >= 1 (got {k}).")
        circ = np.ones(k)
        phi_11 = float(np.sum(np.abs(circ)))
        phi_21 = float(np.linalg.norm(circ))
        ratio = phi_11 / phi_21
        results.append(
            {
                "dimension_k": k,
                "phi_11": phi_11,
                "phi_21": phi_21,
                "discrepancy_ratio": ratio,
                "theoretical_sqrt_k": math.sqrt(k),
            }
        )
    return results


def compute_holonomy(
    connection_matrices: List[np.ndarray],
    orientations: Optional[List[int] | np.ndarray] = None,
) -> np.ndarray:
    """
    Compute cycle holonomy H_C = prod_{i=1}^m R_i^{eps_i} for edge connection matrices R_i in SO(k).
    Traverses along directed cycle order with verified SO(k) properties and orientations in {+1, -1}.
    """
    if len(connection_matrices) == 0:
        raise ValueError("Must provide at least one connection matrix")

    # Validate first matrix
    r0 = np.asarray(connection_matrices[0], dtype=float)
    if r0.ndim != 2 or r0.shape[0] != r0.shape[1]:
        raise ValueError("Connection matrices must be square 2D matrices.")
    k = r0.shape[0]

    # Validate orientations
    if orientations is None:
        eps = [1] * len(connection_matrices)
    else:
        ori_list = list(orientations)
        if len(ori_list) != len(connection_matrices):
            raise ValueError("Orientations count must match connection matrices count")
        for i, x in enumerate(ori_list):
            if not (isinstance(x, (int, np.integer)) and not isinstance(x, bool) and x in (+1, -1)):
                raise ValueError(
                    f"Orientation sign must be exactly +1 or -1 (got {x}); Orientation sign at index {i} must be +1 or -1; Orientations must be in {{+1, -1}}."
                )
        eps = [int(x) for x in ori_list]

    # Strict validation of each SO(k) matrix and orientation sign
    for idx, (mat_raw, sign) in enumerate(zip(connection_matrices, eps, strict=True)):
        r = np.asarray(mat_raw, dtype=float)
        if r.shape != (k, k):
            raise ValueError(
                f"Connection matrix at index {idx} has shape {r.shape}; expected ({k}, {k})."
            )
        if not np.all(np.isfinite(r)):
            raise ValueError(f"Connection matrix at index {idx} contains non-finite values.")
        # Orthogonality check: R^T R = I
        if not np.allclose(r.T @ r, np.eye(k), atol=1e-5):
            raise ValueError(f"Connection matrix at index {idx} is not orthogonal (R^T @ R != I).")
        # Special orthogonality: det(R) = +1
        det_val = float(np.linalg.det(r))
        if abs(det_val - 1.0) > 1e-4:
            raise ValueError(f"Connection matrix at index {idx} has det={det_val:.4f}; must be +1 for SO(k).")
        if sign not in (+1, -1):
            raise ValueError(
                f"Orientation sign must be exactly +1 or -1 (got {sign}); Orientation sign at index {idx} must be +1 or -1; Orientations must be in {{+1, -1}}."
            )

    h = np.eye(k, dtype=float)
    for r_mat, sign in zip(connection_matrices, eps, strict=True):
        mat = r_mat if sign == 1 else r_mat.T
        h = mat @ h
    return h


def apply_vertex_gauge_transformation(
    connection_matrices: List[np.ndarray],
    vertex_gauges: List[np.ndarray],
    edges: List[Tuple[int, int]],
) -> List[np.ndarray]:
    """
    Apply genuine vertex gauge transformation g_v in SO(k) to edge connections:
        R'_{uv} = g_v @ R_{uv} @ g_u.T
    For a closed cycle, this conjugates cycle holonomy: H'_C = g_{v_0} @ H_C @ g_{v_0}.T,
    strictly preserving its eigenvalues, trace, and rotation angle.
    """
    if len(connection_matrices) != len(edges):
        raise ValueError("Number of connection matrices must match number of edges.")
    if len(connection_matrices) == 0:
        raise ValueError("Must provide at least one connection matrix.")

    r0 = np.asarray(connection_matrices[0], dtype=float)
    if r0.ndim != 2 or r0.shape[0] != r0.shape[1]:
        raise ValueError("Connection matrices must be square 2D matrices.")
    k = r0.shape[0]

    for v_idx, g_raw in enumerate(vertex_gauges):
        g = np.asarray(g_raw, dtype=float)
        if g.shape != (k, k):
            raise ValueError(f"Vertex gauge {v_idx} has shape {g.shape}; expected ({k}, {k}).")
        if not np.all(np.isfinite(g)):
            raise ValueError(f"Vertex gauge {v_idx} contains non-finite values.")
        if not np.allclose(g.T @ g, np.eye(k), atol=1e-5):
            raise ValueError(f"Vertex gauge {v_idx} is not orthogonal (g^T @ g != I).")
        det_g = float(np.linalg.det(g))
        if abs(det_g - 1.0) > 1e-4:
            raise ValueError(f"Vertex gauge {v_idx} has det={det_g:.4f}; must be +1 for SO(k).")

    for e_idx, r_raw in enumerate(connection_matrices):
        r = np.asarray(r_raw, dtype=float)
        if r.shape != (k, k):
            raise ValueError(f"Connection matrix {e_idx} has shape {r.shape}; expected ({k}, {k}).")
        if not np.all(np.isfinite(r)):
            raise ValueError(f"Connection matrix {e_idx} contains non-finite values.")
        if not np.allclose(r.T @ r, np.eye(k), atol=1e-5):
            raise ValueError(f"Connection matrix {e_idx} is not orthogonal (R^T @ R != I).")
        det_r = float(np.linalg.det(r))
        if abs(det_r - 1.0) > 1e-4:
            raise ValueError(f"Connection matrix {e_idx} has det={det_r:.4f}; must be +1 for SO(k).")

    transformed = []
    for edge, r_uv in zip(edges, connection_matrices, strict=True):
        if not isinstance(edge, (tuple, list)) or len(edge) != 2:
            raise ValueError(f"Edge must be a 2-tuple of vertex indices, got {edge}.")
        u, v = edge
        if not (isinstance(u, (int, np.integer)) and not isinstance(u, bool) and
                isinstance(v, (int, np.integer)) and not isinstance(v, bool)):
            raise ValueError(
                f"Edge endpoints must be integers, got ({type(u).__name__}, {type(v).__name__})."
            )
        if not (0 <= u < len(vertex_gauges) and 0 <= v < len(vertex_gauges)):
            raise ValueError(
                f"Edge ({u}, {v}) refers to vertex out of bounds for vertex_gauges (count={len(vertex_gauges)})."
            )
        g_u = np.asarray(vertex_gauges[u], dtype=float)
        g_v = np.asarray(vertex_gauges[v], dtype=float)
        r_mat = np.asarray(r_uv, dtype=float)
        r_prime = g_v @ r_mat @ g_u.T
        transformed.append(r_prime)
    return transformed
