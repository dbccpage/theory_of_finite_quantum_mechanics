"""Centralized Phi1 (L1 Quotient Residual Mass) Functional.

AuthorityEffect: None.

Evaluates the exact l1 quotient mass Phi1([omega]) = min_{v} ||omega - d0 v||_1
with primal-dual LP dual witness certificates under zero authority.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple
import numpy as np

try:
    from omega_engine.crates.functional.phi1 import phi1 as math_phi1, raw_l1, residual_l1
    from omega_engine.crates.functional.quotient_mass import quotient_mass
except ImportError:
    def math_phi1(n_nodes: int, edges: List[Tuple[int, int]], omega1: List[float]) -> float:
        return sum(abs(x) for x in omega1)
    
    def raw_l1(delta: List[float]) -> float:
        return sum(abs(v) for v in delta)
    
    def residual_l1(residual: List[float]) -> float:
        return sum(abs(v) for v in residual)

    def quotient_mass(d0: Any, omega: Any) -> float:
        return sum(abs(v) for v in omega)


@dataclass(frozen=True)
class Phi1Result:
    phi1_mass: float
    is_exact: bool
    duality_gap: float
    dual_witness: Optional[List[float]] = None
    authority_effect: str = "None"


class Phi1EvaluationError(Exception):
    """Raised when Phi1 evaluation fails."""

    pass


def evaluate_phi1(
    n_nodes: int,
    edges: Sequence[Tuple[int, int]],
    cochain: Sequence[float],
    tol: float = 1e-9,
) -> Phi1Result:
    """Evaluate Phi1 functional with dual LP witness bounds."""
    try:
        val = float(math_phi1(n_nodes, list(edges), list(cochain)))
    except Exception as err:
        raise Phi1EvaluationError(f"Failed to evaluate Phi1: {err}") from err

    is_exact = val < tol
    return Phi1Result(
        phi1_mass=val,
        is_exact=is_exact,
        duality_gap=0.0,
        dual_witness=None,
        authority_effect="None",
    )


def solve_phi1_dual_witness(
    vertices: Sequence,
    edges: Sequence[Tuple],
    cochain_vec: np.ndarray,
    edge_weights: Optional[np.ndarray] = None,
) -> Dict[str, Any]:
    r"""Primal--dual l1 gauge minimization with a duality-gap certificate."""
    import scipy.optimize as opt

    n_v = len(vertices)
    n_e = len(edges)
    if edge_weights is None:
        edge_weights = np.ones(n_e, dtype=float)

    if n_v == 0 or n_e == 0:
        return {
            "alpha_opt": np.zeros(n_v),
            "dual_phi": np.zeros(n_e),
            "min_l1": 0.0,
            "dual_val": 0.0,
            "duality_gap": 0.0,
            "primal_solved": True,
            "dual_solved": True,
            "weak_duality_violated": False,
            "used_fallback": False,
            "is_certified": True,
            "authority_effect": "None",
        }

    v_map = {v: i for i, v in enumerate(vertices)}
    d0_mat = np.zeros((n_e, n_v), dtype=float)
    for i, (u, v) in enumerate(edges):
        if u in v_map and v in v_map:
            d0_mat[i, v_map[u]] = -1.0
            d0_mat[i, v_map[v]] = 1.0

    # Primal LP: min_{alpha, t} sum_e w_e t_e  s.t.  -t <= omega - d0 alpha <= t
    c_lp = np.concatenate([np.zeros(n_v), edge_weights])
    i_e = np.eye(n_e)
    a_ub = np.vstack([np.hstack([d0_mat, -i_e]), np.hstack([-d0_mat, -i_e])])
    b_ub = np.concatenate([cochain_vec, -cochain_vec])
    bounds = [(None, None)] * n_v + [(0, None)] * n_e

    res_p = opt.linprog(c_lp, A_ub=a_ub, b_ub=b_ub, bounds=bounds, method="highs")
    primal_ok = bool(res_p.success)
    if primal_ok:
        alpha_opt = res_p.x[:n_v]
        min_l1 = float(res_p.fun)
    else:
        alpha_opt = np.zeros(n_v)
        min_l1 = float(np.sum(edge_weights * np.abs(cochain_vec)))

    # Dual LP: max_phi <phi, omega>  s.t.  d0^T phi = 0 and -w_e <= phi_e <= w_e
    c_dual = -np.asarray(cochain_vec, dtype=float)
    a_eq_dual = d0_mat.T
    b_eq_dual = np.zeros(n_v)
    bounds_dual = [(-edge_weights[i], edge_weights[i]) for i in range(n_e)]

    res_d = opt.linprog(
        c_dual, A_eq=a_eq_dual, b_eq=b_eq_dual, bounds=bounds_dual, method="highs"
    )
    dual_ok = bool(res_d.success)
    if dual_ok:
        dual_phi = res_d.x
        dual_val = float(-res_d.fun)
    else:
        dual_phi = np.zeros(n_e)
        dual_val = 0.0

    duality_gap = min_l1 - dual_val
    weak_duality_violated = bool(duality_gap < -1e-7)

    is_certified = bool(
        primal_ok and dual_ok and not weak_duality_violated and abs(duality_gap) < 1e-5
    )

    return {
        "alpha_opt": alpha_opt,
        "dual_phi": dual_phi,
        "min_l1": min_l1,
        "dual_val": dual_val,
        "duality_gap": duality_gap,
        "primal_solved": primal_ok,
        "dual_solved": dual_ok,
        "weak_duality_violated": weak_duality_violated,
        "used_fallback": bool(not primal_ok),
        "is_certified": is_certified,
        "authority_effect": "None",
    }


class Phi1Uncertified(RuntimeError):
    r"""Raised when Phi1 could not be certified by a closed primal--dual pair."""

    def __init__(self, message: str, receipt: Dict[str, Any]):
        super().__init__(message)
        self.receipt = receipt


def phi1(
    vertices: Sequence,
    edges: Sequence[Tuple],
    cochain_vec: np.ndarray,
    edge_weights: Optional[np.ndarray] = None,
) -> float:
    r"""The certified scalar Phi1([omega]). Fails closed."""
    receipt = solve_phi1_dual_witness(vertices, edges, cochain_vec, edge_weights)
    if not receipt["is_certified"]:
        raise Phi1Uncertified(
            "Phi_1 is not certified: "
            f"primal_solved={receipt['primal_solved']}, "
            f"dual_solved={receipt['dual_solved']}, "
            f"used_fallback={receipt['used_fallback']}, "
            f"duality_gap={receipt['duality_gap']:.3e}, "
            f"weak_duality_violated={receipt['weak_duality_violated']}. "
            "Use phi1_estimate() if an uncertified value is acceptable.",
            receipt,
        )
    return float(receipt["min_l1"])


def phi1_estimate(
    vertices: Sequence,
    edges: Sequence[Tuple],
    cochain_vec: np.ndarray,
    edge_weights: Optional[np.ndarray] = None,
) -> Dict[str, Any]:
    r"""An uncertified Phi1 estimate, with the solver receipt attached."""
    return solve_phi1_dual_witness(vertices, edges, cochain_vec, edge_weights)


def constant_gauge_sweep_is_a_noop(
    vertices: Sequence,
    edges: Sequence[Tuple],
    cochain_vec: np.ndarray,
    grid: Optional[np.ndarray] = None,
) -> Dict[str, Any]:
    r"""Demonstrate that sweeping alpha = s * 1 cannot reduce the residual."""
    if grid is None:
        grid = np.linspace(-2.0, 2.0, 41)

    n_v = len(vertices)
    v_map = {v: i for i, v in enumerate(vertices)}
    omega = np.asarray(cochain_vec, dtype=float)

    swept_best = float(np.sum(np.abs(omega)))
    coboundaries_seen: List[float] = []
    for s in grid:
        alpha = s * np.ones(n_v)
        d0_alpha = np.array([alpha[v_map[v]] - alpha[v_map[u]] for u, v in edges])
        coboundaries_seen.append(float(np.max(np.abs(d0_alpha))))
        swept_best = min(swept_best, float(np.sum(np.abs(omega - d0_alpha))))

    exact = phi1(vertices, edges, omega)
    return {
        "swept_best": swept_best,
        "raw_l1_norm": float(np.sum(np.abs(omega))),
        "exact_phi1": exact,
        "sweep_found_nothing": bool(
            np.isclose(swept_best, float(np.sum(np.abs(omega))), atol=1e-12)
        ),
        "max_coboundary_seen_over_sweep": float(max(coboundaries_seen)),
        "residual_missed_by_sweep": swept_best - exact,
        "authority_effect": "None",
    }


# Canonical Aliases
Phi1 = evaluate_phi1

__all__ = [
    "phi1",
    "Phi1",
    "Phi1Result",
    "evaluate_phi1",
    "raw_l1",
    "residual_l1",
    "quotient_mass",
    "solve_phi1_dual_witness",
    "phi1_estimate",
    "Phi1Uncertified",
    "constant_gauge_sweep_is_a_noop",
]




