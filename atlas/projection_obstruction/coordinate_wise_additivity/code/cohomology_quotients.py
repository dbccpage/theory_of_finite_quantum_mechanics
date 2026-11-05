"""Cohomological Obstruction Quotients & EPK/LGGR Ladder for GS-000.

AuthorityEffect: None. Finite graph cochains C^0(G, R^k) -> C^1(G, R^k) and zero-difference quotients.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
from coord_additivity import EdgeOrbitDiagnostic, _dimension, _nonnegative_scalar, coord_l1


@dataclass(frozen=True)
class DirectedGraph:
    """Finite directed graph specification."""

    num_vertices: int
    edges: tuple[tuple[int, int], ...]  # tuple of (source, target) pairs

    def __post_init__(self) -> None:
        _dimension(self.num_vertices)
        for edge in self.edges:
            if len(edge) != 2:
                raise ValueError("each edge must have a source and target")
            for vertex in edge:
                _dimension(vertex)
                if vertex >= self.num_vertices:
                    raise ValueError("edge vertex must index the declared vertex set")

    @property
    def num_edges(self) -> int:
        return len(self.edges)

    def incidence_matrix(self) -> np.ndarray:
        """Construct the vertex-edge incidence boundary matrix d_0: C^0 -> C^1.

        Shape is (|E|, |V|), where row e has -1 at source(e) and +1 at target(e).
        """
        b = np.zeros((self.num_edges, self.num_vertices), dtype=float)
        for e, (u, v) in enumerate(self.edges):
            b[e, u] -= 1.0
            b[e, v] += 1.0
        return b


def coboundary_d0(graph: DirectedGraph, v: np.ndarray) -> np.ndarray:
    """Compute the 0-coboundary (d_0 v)_e = v_{target(e)} - v_{source(e)}.

    v has shape (|V|, k) or (|V|,). Output has shape (|E|, k) or (|E|,).
    """
    v_arr = _cochain_array(v, graph.num_vertices, "v")
    edges = graph.edges
    if v_arr.ndim == 1:
        out = np.zeros(graph.num_edges, dtype=float)
        for e, (src, tgt) in enumerate(edges):
            out[e] = v_arr[tgt] - v_arr[src]
        return out
    elif v_arr.ndim == 2:
        k = v_arr.shape[1]
        out = np.zeros((graph.num_edges, k), dtype=float)
        for e, (src, tgt) in enumerate(edges):
            out[e, :] = v_arr[tgt, :] - v_arr[src, :]
        return out
    else:
        raise ValueError("v must be 1D or 2D array")


def _cochain_array(value: np.ndarray, count: int, label: str) -> np.ndarray:
    if np.iscomplexobj(value):
        raise ValueError(f"{label} must be real")
    array = np.asarray(value, dtype=float)
    if array.ndim not in (1, 2):
        raise ValueError(f"{label} must be 1D or 2D")
    if array.shape[0] != count or not np.all(np.isfinite(array)):
        raise ValueError(f"{label} must have {count} finite rows")
    return array


def is_coboundary(graph: DirectedGraph, delta: np.ndarray, tol: float = 1e-9) -> tuple[bool, np.ndarray | None]:
    """Numerically test membership in im(d_0) with an absolute residual tolerance.

    Returns (True, potential v) if delta = d_0 v, else (False, None).
    """
    tol = _nonnegative_scalar(tol, "tolerance")
    b = graph.incidence_matrix()
    d_arr = _cochain_array(delta, graph.num_edges, "delta")
    # Solve B @ v = delta for each coordinate
    if d_arr.ndim == 1:
        v, residuals, rank, s = np.linalg.lstsq(b, d_arr, rcond=None)
        reconstructed = b @ v
        if np.max(np.abs(reconstructed - d_arr), initial=0.0) <= tol:
            return True, v
        return False, None
    elif d_arr.ndim == 2:
        k = d_arr.shape[1]
        v_full = np.zeros((graph.num_vertices, k), dtype=float)
        for i in range(k):
            vi, res, rank, s = np.linalg.lstsq(b, d_arr[:, i], rcond=None)
            reconstructed = b @ vi
            if np.max(np.abs(reconstructed - d_arr[:, i]), initial=0.0) > tol:
                return False, None
            v_full[:, i] = vi
        return True, v_full
    raise AssertionError("validated cochain dimension was lost")


def local_zero_difference_equiv(
    delta1: Sequence[np.ndarray],
    delta2: Sequence[np.ndarray],
    edge_weights: Sequence[float],
    tol: float = 1e-9,
) -> bool:
    """Probe per-edge readout agreement within tol; not an exact quotient relation."""
    if len(delta1) != len(delta2) or len(delta1) != len(edge_weights):
        raise ValueError("Edge count mismatch")
    tol = _nonnegative_scalar(tol, "tolerance")
    for d1, d2, w in zip(delta1, delta2, edge_weights):
        if np.shape(d1) != np.shape(d2):
            raise ValueError("coordinate dimension mismatch")
        val1 = coord_l1(d1, weight=w)
        val2 = coord_l1(d2, weight=w)
        if abs(val1 - val2) > tol:
            return False
    return True


def global_orbit_zero_difference_equiv(
    delta1: Sequence[np.ndarray],
    delta2: Sequence[np.ndarray],
    orbit_diag: EdgeOrbitDiagnostic,
    tol: float = 1e-9,
) -> bool:
    """Probe weighted-total agreement within tol; not an exact quotient relation."""
    tol = _nonnegative_scalar(tol, "tolerance")
    val1 = orbit_diag.total(list(delta1))
    val2 = orbit_diag.total(list(delta2))
    return abs(val1 - val2) <= tol


def lggr_obstruction_witness() -> dict[str, object]:
    """Compare three different carriers/relations without conflating their witnesses.

    A fixed profile respects per-edge sameness. The coarser unweighted-total
    relation can fail to determine its weighted total. A carrier of records
    (cochain, weight profile) can also forget weights. The legacy keys
    local_green and global_red refer to DIFFERENT pairs, as labeled below.
    """
    orbit_diag = EdgeOrbitDiagnostic(orbit_of_edge=(0, 1), orbit_weights=(1.0, 2.0))
    delta_1 = [np.array([3.0, 4.0]), np.array([1.0, 2.0])]
    delta_2 = [np.array([7.0, 0.0]), np.array([3.0, 0.0])]
    local_green = local_zero_difference_equiv(delta_1, delta_2, [1.0, 1.0])
    cochain_a = [np.array([7.0, 0.0]), np.array([3.0, 0.0])]
    cochain_b = [np.array([3.0, 0.0]), np.array([7.0, 0.0])]
    unweighted_equal = sum(map(coord_l1, cochain_a)) == sum(map(coord_l1, cochain_b))
    tot_a = orbit_diag.total(cochain_a)
    tot_b = orbit_diag.total(cochain_b)
    other_profile = EdgeOrbitDiagnostic((0, 1), (2.0, 2.0))
    return {
        "cochain_1": delta_1,
        "cochain_2": delta_2,
        "local_green": local_green,
        "fixed_profile_total_1": orbit_diag.total(delta_1),
        "fixed_profile_total_2": orbit_diag.total(delta_2),
        "fixed_profile_global_equal": global_orbit_zero_difference_equiv(
            delta_1, delta_2, orbit_diag
        ),
        "cochain_a": cochain_a,
        "cochain_b": cochain_b,
        "unweighted_equal": unweighted_equal,
        "coarse_pair_per_edge_equal": local_zero_difference_equiv(
            cochain_a, cochain_b, [1.0, 1.0]
        ),
        "orbit_total_a": tot_a,
        "orbit_total_b": tot_b,
        "global_red": abs(tot_a - tot_b) > 1e-12,
        "varying_profile_total_1": tot_a,
        "varying_profile_total_2": other_profile.total(cochain_a),
        "varying_profile_unweighted_edge_values": (7.0, 3.0),
    }
