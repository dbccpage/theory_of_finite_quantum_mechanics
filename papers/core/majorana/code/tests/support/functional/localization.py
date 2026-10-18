import numpy as np
from typing import List, Tuple


def adjoint_defect(g_e: np.ndarray, g_next: np.ndarray) -> np.ndarray:
    """Adjoint-based transition defect ``g_next @ g_e^H - I``.

    This uses the conjugate transpose (adjoint) ``g_e^H`` in place of the group
    inverse ``g_e^{-1}``. The two coincide ONLY for UNITARY ``g_e``; for
    non-unitary elements this is an adjoint-based defect, not a genuine group
    coboundary defect. ``g_e`` and ``g_next`` must be square and same-shaped.
    """
    g_e = np.asarray(g_e)
    g_next = np.asarray(g_next)
    if g_e.ndim != 2 or g_e.shape[0] != g_e.shape[1]:
        raise ValueError("g_e must be a square 2D matrix")
    if g_next.shape != g_e.shape:
        raise ValueError("g_e and g_next must have the same shape")
    g_e_adjoint = g_e.conj().T
    return g_next @ g_e_adjoint - np.eye(g_e.shape[0], dtype=np.complex128)


coboundary_defect = adjoint_defect


def l1_localization_functional(
    edge_elements: List[np.ndarray], edges: List[Tuple[int, int]]
) -> float:
    """Sum of Frobenius norms of adjoint-based transition defects around edges.

    NOTE: built on ``adjoint_defect`` (adjoint, not group inverse); it is a
    genuine group-coboundary cost only when all ``edge_elements`` are unitary.
    Requires one matrix per edge, all square and identically shaped.
    """
    n_edges = len(edges)
    if len(edge_elements) != n_edges:
        raise ValueError(
            f"edge_elements count {len(edge_elements)} does not match edge count {n_edges}"
        )
    if n_edges == 0:
        return 0.0
    shape0 = np.asarray(edge_elements[0]).shape
    total_cost = 0.0
    for i in range(n_edges):
        g_e = np.asarray(edge_elements[i])
        if g_e.shape != shape0:
            raise ValueError("all edge_elements must have the same shape")
        g_next = edge_elements[(i + 1) % n_edges]
        delta = adjoint_defect(g_e, g_next)
        total_cost += float(np.linalg.norm(delta, "fro"))
    return float(total_cost)


def normalized_l1_cost(raw_cost: float, rep_dim: int, n_edges: int) -> float:
    scale = n_edges * np.sqrt(2.0 * rep_dim)
    if scale < 1e-15:
        return 0.0
    return raw_cost / scale

