"""Dual-certified L1 quotient solver for degree-2 cochains in 4D Regge calculus.

Solves:
    Primal: Phi([omega]) = inf_{beta in C^1} ||omega - d_1 beta||_1
    Dual:   Psi(omega)   = sup_{w in C^2: partial_2 w = 0, ||w||_inf <= 1} <w, omega>

Strong Duality:
    Phi([omega]) == Psi(omega) with zero duality gap.
    Exact constraint closure holds iff Phi([omega]) == 0.
    The dual witness w* is an exact divergence-free 2-cycle in Z_2(T).

AuthorityEffect: None.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple
import numpy as np
from scipy.optimize import linprog


@dataclass(frozen=True)
class Degree2L1QuotientResult:
    """Certified result of degree-2 L1 quotient minimization."""

    primal_obj: float
    dual_obj: float
    duality_gap: float
    is_closed: bool
    is_certified: bool
    primal_beta: np.ndarray
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
            "primal_beta": self.primal_beta.tolist(),
            "primal_residual": self.primal_residual.tolist(),
            "dual_witness": self.dual_witness.tolist(),
            "dual_divergence_norm": self.dual_divergence_norm,
            "num_triangles": len(self.primal_residual),
            "num_edges": len(self.primal_beta),
            "solver_status": self.solver_status,
            "authority_effect": self.authority_effect,
        }


class Degree2DualCertifiedL1Solver:
    """Solver computing degree-2 L1 quotient distance and certified dual 2-cycle witnesses."""

    def __init__(self, tol: float = 1e-10) -> None:
        self.tol = tol

    def solve(self, omega: np.ndarray, d1: np.ndarray) -> Degree2L1QuotientResult:
        """Compute Phi([omega]) = inf_beta ||omega - d_1 beta||_1 and certified dual witness w.

        Args:
            omega: 2-cochain of length N_2 (triangles/hinges).
            d1: Coboundary matrix of shape (N_2, N_1) mapping C^1 to C^2.

        Returns:
            Degree2L1QuotientResult with exact primal residual and dual 2-cycle witness.
        """
        n2, n1 = d1.shape
        omega = np.asarray(omega, dtype=float).flatten()
        if len(omega) != n2:
            raise ValueError(f"Length of omega ({len(omega)}) must match rows of d1 ({n2})")

        if np.all(omega == 0.0):
            zero_beta = np.zeros(n1, dtype=float)
            zero_w = np.zeros(n2, dtype=float)
            return Degree2L1QuotientResult(
                primal_obj=0.0,
                dual_obj=0.0,
                duality_gap=0.0,
                is_closed=True,
                is_certified=True,
                primal_beta=zero_beta,
                primal_residual=np.zeros(n2, dtype=float),
                dual_witness=zero_w,
                dual_divergence_norm=0.0,
                solver_status="OPTIMAL_ZERO",
            )

        solver_opts = {
            "primal_feasibility_tolerance": max(1e-10, float(self.tol)),
            "dual_feasibility_tolerance": max(1e-10, float(self.tol)),
        }

        c_primal = np.zeros(n1 + n2, dtype=float)
        c_primal[n1:] = 1.0

        A_ub1 = np.hstack([-d1, -np.eye(n2)])
        b_ub1 = -omega

        A_ub2 = np.hstack([d1, -np.eye(n2)])
        b_ub2 = omega

        A_ub = np.vstack([A_ub1, A_ub2])
        b_ub = np.concatenate([b_ub1, b_ub2])

        bounds = [(None, None)] * n1 + [(0.0, None)] * n2

        res_primal = linprog(
            c_primal,
            A_ub=A_ub,
            b_ub=b_ub,
            bounds=bounds,
            method="highs",
            options=solver_opts,
        )

        if not res_primal.success:
            raise RuntimeError(f"Primal degree-2 L1 solver failed: {res_primal.message}")

        beta_opt = res_primal.x[:n1]
        residual = omega - d1 @ beta_opt
        primal_obj = float(np.sum(np.abs(residual)))

        c_dual = -omega
        A_eq = d1.T
        b_eq = np.zeros(n1)
        bounds_dual = [(-1.0, 1.0)] * n2

        res_dual = linprog(
            c_dual,
            A_eq=A_eq,
            b_eq=b_eq,
            bounds=bounds_dual,
            method="highs",
            options=solver_opts,
        )

        if not res_dual.success:
            raise RuntimeError(f"Dual degree-2 L1 solver failed: {res_dual.message}")

        w_opt = res_dual.x
        dual_obj = float(np.dot(w_opt, omega))

        div_w = d1.T @ w_opt
        dual_div_norm = float(np.linalg.norm(div_w, ord=np.inf))

        duality_gap = abs(primal_obj - dual_obj)
        is_closed = bool(primal_obj <= self.tol)

        check_atol = max(1e-7, self.tol * 10)
        res_ok = np.allclose(residual, omega - d1 @ beta_opt, atol=check_atol)
        div_ok = dual_div_norm <= check_atol
        bounds_ok = np.all(np.abs(w_opt) <= 1.0 + check_atol)
        gap_ok = duality_gap <= check_atol
        is_certified = bool(res_primal.success and res_dual.success and res_ok and div_ok and bounds_ok and gap_ok)

        return Degree2L1QuotientResult(
            primal_obj=primal_obj,
            dual_obj=dual_obj,
            duality_gap=duality_gap,
            is_closed=is_closed,
            is_certified=is_certified,
            primal_beta=beta_opt,
            primal_residual=residual,
            dual_witness=w_opt,
            dual_divergence_norm=dual_div_norm,
            solver_status="OPTIMAL" if is_certified else "UNCERTIFIED",
        )


def compute_degree2_l1_quotient_with_dual_witness(
    omega: np.ndarray,
    d1: np.ndarray,
    tol: float = 1e-10,
) -> Degree2L1QuotientResult:
    """Convenience function to compute certified degree-2 L1 quotient distance and dual witness."""
    solver = Degree2DualCertifiedL1Solver(tol=tol)
    return solver.solve(omega, d1)


Degree2DualWitnessSolver = Degree2DualCertifiedL1Solver
