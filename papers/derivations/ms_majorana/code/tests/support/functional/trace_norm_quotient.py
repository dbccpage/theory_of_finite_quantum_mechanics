r"""
The trace-norm quotient obstruction and its operator-norm dual witnesses.

AuthorityEffect: None.

Canonical Implementation: omega_engine.crates.functional.trace_norm_quotient
"""

from __future__ import annotations
from typing import Any, Dict, List, Sequence, Tuple

import numpy as np

from omega_engine.crates.quantum_physics.primitives import dagger, trace_norm


def _hermitian_from_params(vec: np.ndarray, d: int) -> np.ndarray:
    m = np.zeros((d, d), dtype=complex)
    idx = 0
    for i in range(d):
        m[i, i] = vec[idx]
        idx += 1
    for i in range(d):
        for j in range(i + 1, d):
            m[i, j] = vec[idx] + 1j * vec[idx + 1]
            m[j, i] = vec[idx] - 1j * vec[idx + 1]
            idx += 2
    return m


def _params_per_matrix(d: int) -> int:
    return d * d


def dual_ball_slack(m: np.ndarray) -> float:
    return float(1.0 - np.max(np.linalg.svd(m, compute_uv=False)))


def trace_distance_dual_ball_slack(m: np.ndarray) -> float:
    ev = np.linalg.eigvalsh((m + dagger(m)) / 2.0)
    return float(1.0 - (ev[-1] - ev[0]))


def is_dual_feasible(
    m_edges: Sequence[np.ndarray], d0_mat: np.ndarray, atol: float = 1e-7
) -> bool:
    for m in m_edges:
        if dual_ball_slack(m) < -atol:
            return False
    n_v = d0_mat.shape[1]
    d = m_edges[0].shape[0]
    for v in range(n_v):
        acc = np.zeros((d, d), dtype=complex)
        for e, m in enumerate(m_edges):
            acc += d0_mat[e, v] * m
        if np.max(np.abs(acc)) > 1e-6:
            return False
    return True


def trace_norm_quotient(
    graph, delta_edges: Sequence[np.ndarray], max_iter: int = 400
) -> Dict[str, Any]:
    from scipy.optimize import minimize

    deltas = [np.asarray(x, dtype=complex) for x in delta_edges]
    if len(deltas) != graph.n_edges:
        raise ValueError(
            f"trace_norm_quotient: got {len(deltas)} edge matrices for {graph.n_edges} edges"
        )
    d = deltas[0].shape[0]
    if any(x.shape != (d, d) for x in deltas):
        raise ValueError("trace_norm_quotient: all edge matrices must share one dimension")

    d0 = graph.d0_matrix()
    n_v = graph.n_vertices
    per = _params_per_matrix(d)

    def residuals(params: np.ndarray) -> List[np.ndarray]:
        alphas = [
            _hermitian_from_params(params[v * per : (v + 1) * per], d) for v in range(n_v)
        ]
        out = []
        for e in range(graph.n_edges):
            d0_alpha = sum(d0[e, v] * alphas[v] for v in range(n_v))
            out.append(deltas[e] - d0_alpha)
        return out

    def objective(params: np.ndarray) -> float:
        return float(sum(trace_norm(r) for r in residuals(params)))

    raw = float(sum(trace_norm(x) for x in deltas))
    x0 = np.zeros(n_v * per)
    res = minimize(objective, x0, method="Powell", options={"maxiter": max_iter, "xtol": 1e-8, "ftol": 1e-10})

    primal = float(min(res.fun, raw))
    best_params = res.x if res.fun <= raw else x0
    opt_residuals = residuals(best_params)

    m_edges: List[np.ndarray] = []
    for r in opt_residuals:
        u, _s, vh = np.linalg.svd(r)
        m_edges.append(u @ vh)

    m_proj = _project_divergence_free(m_edges, d0, n_v, d)
    m_proj = _rescale_into_dual_ball(m_proj)

    dual_val = float(np.real(sum(np.trace(m @ x) for m, x in zip(m_proj, deltas))))
    feasible = is_dual_feasible(m_proj, d0)
    gap = primal - dual_val

    numerical_slack = 1e-9
    violated = bool(gap < -numerical_slack)
    return {
        "phi_tr": primal,
        "raw_trace_norm_sum": raw,
        "dual_value": dual_val,
        "dual_feasible": feasible,
        "duality_gap": gap,
        "weak_duality_violated": violated,
        "certified": bool(feasible and not violated and gap < 1e-4),
        "is_exact_repair": bool(primal < 1e-8),
        "note": (
            "primal solved numerically; dual exhibited as a feasible lower bound, "
            "not solved to optimality (that is an SDP)"
        ),
        "authority_effect": "None",
    }


def _project_divergence_free(
    m_edges: List[np.ndarray], d0: np.ndarray, n_v: int, d: int
) -> List[np.ndarray]:
    n_e = len(m_edges)
    stacked = np.stack([m.reshape(-1) for m in m_edges], axis=0)
    beta, *_ = np.linalg.lstsq(d0, stacked, rcond=None)
    cleaned = stacked - d0 @ beta
    return [cleaned[e].reshape(d, d) for e in range(n_e)]


def _rescale_into_dual_ball(m_edges: List[np.ndarray]) -> List[np.ndarray]:
    worst = 0.0
    for m in m_edges:
        worst = max(worst, float(np.max(np.linalg.svd(m, compute_uv=False))))
    if worst <= 1.0 or worst == 0.0:
        return m_edges
    return [m / worst for m in m_edges]


def dual_ball_diameter_identity(m: np.ndarray) -> Dict[str, Any]:
    herm = (m + dagger(m)) / 2.0
    ev = np.linalg.eigvalsh(herm)
    diam = float(ev[-1] - ev[0])
    lam_star = -0.5 * float(ev[-1] + ev[0])
    shifted = herm + lam_star * np.eye(herm.shape[0])
    op_at_star = float(np.max(np.abs(np.linalg.eigvalsh(shifted))))

    return {
        "diameter": diam,
        "optimal_shift": lam_star,
        "op_norm_at_optimal_shift": op_at_star,
        "identity_holds": bool(np.isclose(diam, 2.0 * op_at_star, atol=1e-9)),
        "authority_effect": "None",
    }


__all__ = [
    "trace_norm_quotient",
    "dual_ball_slack",
    "trace_distance_dual_ball_slack",
    "is_dual_feasible",
    "dual_ball_diameter_identity",
]



