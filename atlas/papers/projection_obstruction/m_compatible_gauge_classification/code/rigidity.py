"""Hahn-Banach rank-one rigidity and maximal End_b(V) symmetry for GS-001.

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Callable, Sequence
import numpy as np

from norms import exact_induced_operator_norm

Gauge = Callable[[np.ndarray], float]


def rank_one_map(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Construct Euclidean rank-one operator T = (v (x) u) / ||u||_2^2.

    Ensures T @ u = v for any non-zero vectors u, v in R^n.
    """
    u_arr = np.asarray(u, dtype=float).ravel()
    v_arr = np.asarray(v, dtype=float).ravel()

    if u_arr.shape != v_arr.shape:
        raise ValueError("u and v must have matching dimensions")
    u_norm_sq = float(np.sum(u_arr**2))
    if u_norm_sq <= 1e-15:
        raise ValueError("Source vector u must be non-zero")

    return np.outer(v_arr, u_arr) / u_norm_sq


def construct_hahn_banach_rank_one(
    u: np.ndarray, v: np.ndarray, gauge: Gauge, gauge_type: str = "l2"
) -> np.ndarray:
    """Construct Hahn-Banach rank-one operator T = (v (x) y^T) / y(u) where y is a dual vector.

    Shows j(T u) = j(v) and ||T||_{j -> j} = j(v) / j(u).
    """
    u_arr = np.asarray(u, dtype=float).ravel()
    v_arr = np.asarray(v, dtype=float).ravel()

    j_u = gauge(u_arr)
    if j_u <= 1e-15:
        raise ValueError("Source vector u must be non-zero")

    g_type = gauge_type.lower()
    if g_type == "l2":
        # Dual vector y = u / ||u||_2
        y = u_arr / float(np.linalg.norm(u_arr, 2))
    elif g_type == "l1":
        # Dual vector y = sign(u)
        y = np.sign(u_arr)
    elif g_type == "linf":
        # Dual vector y = e_k where |u_k| = ||u||_inf
        k = int(np.argmax(np.abs(u_arr)))
        y = np.zeros_like(u_arr)
        y[k] = np.sign(u_arr[k])
    else:
        # Default Euclidean dual
        y = u_arr / float(np.linalg.norm(u_arr, 2))

    y_u = float(np.dot(y, u_arr))
    if abs(y_u) <= 1e-15:
        raise ValueError("Dual pairing y(u) is zero")

    return np.outer(v_arr, y) / y_u


def is_maximal_end_compatible(
    gauge: Gauge, dimension: int, probe_operators: Sequence[np.ndarray] | None = None
) -> bool:
    """Verify compatibility j(T x) <= ||T|| j(x) under End_b(V) operators."""
    if probe_operators is None:
        # Standard rank-one probes, projections, and rotations
        r45 = np.array(
            [
                [1.0 / np.sqrt(2.0), -1.0 / np.sqrt(2.0)],
                [1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)],
            ]
        )
        probe_operators = [
            np.eye(dimension),
            r45 if dimension == 2 else np.eye(dimension),
            np.diag([1.0, 0.0] + [1.0] * (dimension - 2)),
            np.array([[0.0, 1.0], [1.0, 0.0]] + [[0.0, 0.0]] * (dimension - 2)),
        ]

    for T in probe_operators:
        arr = np.asarray(T, dtype=float)
        if arr.shape != (dimension, dimension):
            continue
        op_norm = exact_induced_operator_norm(arr, "l2", "l2")
        x_samples = [np.ones(dimension), np.array([1.0, 0.0] + [0.0] * (dimension - 2))]
        for x_sample in x_samples:
            if gauge(arr @ x_sample) > op_norm * gauge(x_sample) + 1e-9:
                return False

    return True
