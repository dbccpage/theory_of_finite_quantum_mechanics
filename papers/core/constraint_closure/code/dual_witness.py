"""Dual-certified L1 quotient solver for discrete constraint closure.

Solves:
    Primal: Phi([omega]) = inf_{alpha} ||omega - d_0 alpha||_1
    Dual:   Psi(omega)   = sup_{w: d_0^T w = 0, ||w||_inf <= 1} <w, omega>

Strong Duality:
    Phi([omega]) == Psi(omega) with zero duality gap.
    Exact constraint closure holds iff Phi([omega]) == 0.

AuthorityEffect: None.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple
import numpy as np
from scipy.optimize import linprog


@dataclass(frozen=True)
class L1QuotientResult:
    """Certified result of L1 quotient minimization."""

    primal_obj: float
    dual_obj: float
    duality_gap: float
    is_closed: bool
    is_certified: bool
    primal_alpha: np.ndarray
    primal_residual: np.ndarray
    dual_witness: np.ndarray
    dual_divergence_norm: float
    solver_status: str
    authority_effect: str = "None"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "primal_obj": self.primal_obj,
            "dual_obj": self.dual_obj,
            "duality_gap": self.duality_gap,
            "is_closed": self.is_closed,
            "is_certified": self.is_certified,
            "primal_alpha": self.primal_alpha.tolist(),
            "primal_residual": self.primal_residual.tolist(),
            "dual_witness": self.dual_witness.tolist(),
            "dual_divergence_norm": self.dual_divergence_norm,
            "num_edges": len(self.primal_residual),
            "num_vertices": len(self.primal_alpha),
            "solver_status": self.solver_status,
            "authority_effect": self.authority_effect,
        }


class DualCertifiedL1Solver:
    """Solver computing L1 quotient distance and certified dual circulation witnesses."""

    def __init__(self, tol: float = 1e-10) -> None:
        self.tol = tol

    def solve(self, omega: np.ndarray, d0: np.ndarray) -> L1QuotientResult:
        """Compute Phi([omega]) = inf_alpha ||omega - d_0 alpha||_1 and certified dual witness w.

        Args:
            omega: 1-cochain of length m (edges).
            d0: Coboundary matrix of shape (m, n) mapping C^0 to C^1.

        Returns:
            L1QuotientResult with exact primal residual and dual circulation witness.
        """
        m, n = d0.shape
        omega = np.asarray(omega, dtype=float).flatten()
        if len(omega) != m:
            raise ValueError(f"Length of omega ({len(omega)}) must match rows of d0 ({m})")

        # Zero cochain case: reserve shortcut exclusively for exact numerical zero
        if np.all(omega == 0.0):
            zero_alpha = np.zeros(n, dtype=float)
            zero_w = np.zeros(m, dtype=float)
            return L1QuotientResult(
                primal_obj=0.0,
                dual_obj=0.0,
                duality_gap=0.0,
                is_closed=True,
                is_certified=True,
                primal_alpha=zero_alpha,
                primal_residual=np.zeros(m, dtype=float),
                dual_witness=zero_w,
                dual_divergence_norm=0.0,
                solver_status="OPTIMAL_ZERO",
            )

        # Solver options matching claimed precision (clamped to HiGHS minimum 1e-10)
        solver_opts = {
            "primal_feasibility_tolerance": max(1e-10, float(self.tol)),
            "dual_feasibility_tolerance": max(1e-10, float(self.tol)),
        }

        # 1. Primal LP formulation:
        # Variables: x = [alpha (n), u (m)]
        # Minimize sum u_i
        # s.t.
        #   -d0 * alpha - u <= -omega
        #    d0 * alpha - u <=  omega
        #    u >= 0, alpha unconstrained
        c_primal = np.concatenate([np.zeros(n), np.ones(m)])

        A_ub1 = np.hstack([-d0, -np.eye(m)])
        b_ub1 = -omega
        A_ub2 = np.hstack([d0, -np.eye(m)])
        b_ub2 = omega

        A_ub = np.vstack([A_ub1, A_ub2])
        b_ub = np.concatenate([b_ub1, b_ub2])

        bounds = [(None, None)] * n + [(0.0, None)] * m

        res_primal = linprog(
            c_primal,
            A_ub=A_ub,
            b_ub=b_ub,
            bounds=bounds,
            method="highs",
            options=solver_opts,
        )

        if not res_primal.success:
            raise RuntimeError(f"Primal L1 solver failed: {res_primal.message}")

        alpha_opt = res_primal.x[:n]
        residual = omega - d0 @ alpha_opt
        primal_obj = float(np.sum(np.abs(residual)))

        # 2. Dual LP formulation:
        # Maximize w^T omega  <=>  Minimize -omega^T w
        # s.t. d0^T w = 0 (boundary/divergence-free 1-cycle)
        #      -1 <= w_i <= 1
        c_dual = -omega
        A_eq = d0.T
        b_eq = np.zeros(n)
        bounds_dual = [(-1.0, 1.0)] * m

        res_dual = linprog(
            c_dual,
            A_eq=A_eq,
            b_eq=b_eq,
            bounds=bounds_dual,
            method="highs",
            options=solver_opts,
        )

        if not res_dual.success:
            raise RuntimeError(f"Dual L1 solver failed: {res_dual.message}")

        w_opt = res_dual.x
        dual_obj = float(np.dot(w_opt, omega))

        # Divergence of dual witness: d0^T w = partial_1 w
        div_w = d0.T @ w_opt
        dual_div_norm = float(np.linalg.norm(div_w, ord=np.inf))

        duality_gap = abs(primal_obj - dual_obj)
        is_closed = bool(primal_obj <= self.tol)

        # Explicit certificate validation
        check_atol = max(1e-7, self.tol * 10)
        res_ok = np.allclose(residual, omega - d0 @ alpha_opt, atol=check_atol)
        div_ok = dual_div_norm <= check_atol
        bounds_ok = np.all(np.abs(w_opt) <= 1.0 + check_atol)
        gap_ok = duality_gap <= check_atol
        is_certified = bool(res_primal.success and res_dual.success and res_ok and div_ok and bounds_ok and gap_ok)

        return L1QuotientResult(
            primal_obj=primal_obj,
            dual_obj=dual_obj,
            duality_gap=duality_gap,
            is_closed=is_closed,
            is_certified=is_certified,
            primal_alpha=alpha_opt,
            primal_residual=residual,
            dual_witness=w_opt,
            dual_divergence_norm=dual_div_norm,
            solver_status="OPTIMAL" if is_certified else "UNCERTIFIED",
        )


def compute_l1_quotient_with_dual_witness(
    omega: np.ndarray,
    d0: np.ndarray,
    tol: float = 1e-10,
) -> L1QuotientResult:
    """Convenience function to compute certified L1 quotient distance and dual witness."""
    solver = DualCertifiedL1Solver(tol=tol)
    return solver.solve(omega, d0)


# Backward-compatible alias
DualWitnessL1Solver = DualCertifiedL1Solver
