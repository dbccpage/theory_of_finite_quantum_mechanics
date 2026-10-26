"""
Second-Order Cone & Primal-Dual Solvers for Mixed and Coordinate Quotient Obstructions.
Paper: GS-002 (so_k_invariant_gauge_classification)
"""

from __future__ import annotations
from typing import Dict, Any, Tuple, Optional
import numpy as np
from scipy.optimize import minimize, linprog

from carrier import GraphComplex, Cochain
from socp_certifier import (
    DualityCertificate,
    SOCPCertifier,
    _validate_tolerance,
)


class MixedNormSolver:
    """
    Solves the primal quotient obstruction:
        Phi_{2,1,c}([omega]) = inf_alpha sum_e c_e ||omega_e - (d0 alpha)_e||_2
    and its dual:
        Psi_{2,1,c}(omega) = max_phi sum_e <phi_e, omega_e>
        s.t. d0^* phi = 0, ||phi_e||_2 <= c_e.
    """

    def __init__(self, complex: GraphComplex, tol: float = 1e-6) -> None:
        self.complex = complex
        self.tol = _validate_tolerance(tol)

    def solve(
        self,
        omega: Cochain,
        max_iter: int = 500,
        exact: Optional[bool] = None,
        method: str = "auto",
    ) -> DualityCertificate:
        """
        Solve mixed primal-dual obstruction problem using SOCP certifier (default)
        or smoothed L-BFGS-B formulation with dual projection.
        method: 'auto' | 'cycle_closed_form' | 'numerical' | 'smoothed_lbfgs'
        """
        if omega.shape != (self.complex.num_edges, self.complex.stalk_dim):
            raise ValueError(
                f"Omega shape {omega.shape} does not match complex {(self.complex.num_edges, self.complex.stalk_dim)}."
            )

        if exact is not None:
            if not exact:
                method = "smoothed_lbfgs"
            elif method == "auto":
                method = "auto"

        if method in ("auto", "cycle_closed_form", "numerical"):
            certifier = SOCPCertifier(self.complex, tol=self.tol)
            return certifier.certify(omega, method=method)

        if method != "smoothed_lbfgs":
            raise ValueError(
                f"Unknown solver method '{method}'; expected 'auto', 'cycle_closed_form', 'numerical', or 'smoothed_lbfgs'."
            )

        m = self.complex.num_edges
        n = self.complex.num_vertices
        k = self.complex.stalk_dim
        d0 = self.complex.d0
        weights = self.complex.edge_weights
        w_data = omega.data

        eps_smooth = 1e-12

        def primal_objective(alpha_flat: np.ndarray) -> Tuple[float, np.ndarray]:
            alpha = alpha_flat.reshape((n, k))
            residual = w_data - d0 @ alpha
            norms_sq = np.sum(residual**2, axis=1)
            smoothed_norms = np.sqrt(norms_sq + eps_smooth)
            cost = float(np.sum(weights * smoothed_norms))

            grad_res = (weights[:, None] * residual) / smoothed_norms[:, None]
            grad_alpha = -(d0.T @ grad_res)
            return cost, grad_alpha.flatten()

        alpha_init = np.zeros(n * k, dtype=float)

        res = minimize(
            fun=primal_objective,
            x0=alpha_init,
            jac=True,
            method="L-BFGS-B",
            options={"maxiter": max_iter, "gtol": 1e-8, "ftol": 1e-12},
        )

        alpha_opt = res.x.reshape((n, k))
        residual_opt = w_data - d0 @ alpha_opt
        exact_norms = np.linalg.norm(residual_opt, axis=1)
        primal_val = float(np.sum(weights * exact_norms))

        # Construct Candidate Dual Circulation
        candidate_phi = np.zeros_like(residual_opt)
        for e in range(m):
            if exact_norms[e] > 1e-9:
                candidate_phi[e] = weights[e] * (residual_opt[e] / exact_norms[e])
            else:
                candidate_phi[e] = np.zeros(k)

        laplacian = d0.T @ d0
        rhs = d0.T @ candidate_phi
        beta, _, _, _ = np.linalg.lstsq(laplacian, rhs, rcond=None)
        projected_phi = candidate_phi - d0 @ beta

        proj_norms = np.linalg.norm(projected_phi, axis=1)
        max_ratio = float(np.max(proj_norms / weights))
        if max_ratio > 1.0:
            projected_phi = projected_phi / max_ratio
            proj_norms = proj_norms / max_ratio

        dual_val = float(np.sum(projected_phi * w_data))
        div = d0.T @ projected_phi
        max_div = float(np.max(np.abs(div)))
        max_ball_viol = float(np.max(np.maximum(0.0, proj_norms - weights)))

        signed_gap = primal_val - dual_val
        gap = abs(signed_gap)
        is_div_free = max_div <= self.tol
        is_ball_feas = max_ball_viol <= self.tol
        is_optimal = gap <= self.tol and is_div_free and is_ball_feas

        is_zg = is_optimal and (gap <= self.tol)
        cert = DualityCertificate(
            primal_value=primal_val,
            dual_value=dual_val,
            duality_gap=gap,
            signed_duality_gap=signed_gap,
            primal_repair=alpha_opt,
            residual_cochain=Cochain(residual_opt, degree=1),
            dual_circulation=Cochain(projected_phi, degree=1),
            divergence_norm=max_div,
            max_dual_norm_violation=max_ball_viol,
            is_divergence_free=is_div_free,
            is_dual_feasible=is_ball_feas,
            is_optimal=is_optimal,
            details={
                "solver_message": res.message,
                "iterations": res.nit,
                "primal_success": res.success,
            },
            is_zero_gap=is_zg,
            solver_method="smoothed_lbfgs",
        )
        return cert


class CoordinateL1Solver:
    """
    Solves uncoupled coordinate-separable scalar quotient obstruction:
        Phi_{1,1,c}([omega]) = sum_j min_{alpha_j} sum_e c_e |omega_{e,j} - (d0 alpha_j)_e|
    Decoupled into k standard Linear Programs using HiGHS.
    """

    def __init__(self, complex: GraphComplex) -> None:
        self.complex = complex

    def solve(self, omega: Cochain) -> Dict[str, Any]:
        if omega.shape != (self.complex.num_edges, self.complex.stalk_dim):
            raise ValueError(
                f"Omega shape {omega.shape} does not match complex {(self.complex.num_edges, self.complex.stalk_dim)}."
            )

        m = self.complex.num_edges
        n = self.complex.num_vertices
        k = self.complex.stalk_dim
        d0 = self.complex.d0
        weights = self.complex.edge_weights
        w_data = omega.data

        total_cost = 0.0
        alpha_opt = np.zeros((n, k), dtype=float)
        residuals = np.zeros((m, k), dtype=float)

        c_obj = np.concatenate([np.zeros(n), weights])
        a_ub_top = np.hstack([d0, -np.eye(m)])
        a_ub_bot = np.hstack([-d0, -np.eye(m)])
        a_ub = np.vstack([a_ub_top, a_ub_bot])
        bounds = [(None, None)] * n + [(0.0, None)] * m

        for j in range(k):
            b_ub = np.concatenate([w_data[:, j], -w_data[:, j]])
            res = linprog(c_obj, A_ub=a_ub, b_ub=b_ub, bounds=bounds, method="highs")
            if not res.success:
                raise RuntimeError(
                    f"Linear program failed for coordinate channel {j}: {res.message}"
                )
            alpha_j = res.x[:n]
            alpha_opt[:, j] = alpha_j
            res_j = w_data[:, j] - d0 @ alpha_j
            residuals[:, j] = res_j
            total_cost += float(res.fun)

        return {
            "primal_value": total_cost,
            "primal_repair": alpha_opt,
            "residual_cochain": Cochain(residuals, degree=1),
            "is_optimal": True,
        }
