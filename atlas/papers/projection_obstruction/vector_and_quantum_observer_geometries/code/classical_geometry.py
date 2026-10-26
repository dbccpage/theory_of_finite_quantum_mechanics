"""
Classical Vector Observer Geometries and Mixed Norm Solvers.
Paper: GS-003 (vector_and_quantum_observer_geometries)
AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Tuple, Union
import numpy as np
from scipy.optimize import minimize, linprog

from cochain_complex import GraphComplex, Cochain
from exceptions import DimensionMismatchError


@dataclass(frozen=True)
class ClassicalDualityCertificate:
    """Certificate of primal and dual optimality for classical vector quotient obstruction."""

    p_norm: Union[int, float]
    primal_value: float
    dual_value: float
    duality_gap: float
    primal_repair: Cochain
    residual_cochain: Cochain
    dual_witness: Cochain
    divergence_norm: float
    max_dual_norm_violation: float
    is_divergence_free: bool
    is_dual_feasible: bool
    is_optimal: bool
    details: Dict[str, Any]


class ClassicalQuotientSolver:
    """
    Solves the gauge quotient evaluation functional for mixed norms:
        Phi_{p,1,w}([omega]) = inf_{phi in C^0} sum_e w_e ||omega_e - (d0 phi)_e||_p
    and its Fenchel dual:
        Psi_{q,inf,w}(omega) = sup_{z in C^1} <z, omega>
        s.t. d0^* z = 0, ||z_e||_q <= w_e
    where 1/p + 1/q = 1.
    """

    def __init__(self, complex: GraphComplex, tol: float = 1e-5) -> None:
        self.complex = complex
        self.tol = tol

    def solve(
        self,
        omega: Cochain,
        p: Union[int, float] = 2,
        max_iter: int = 500,
    ) -> ClassicalDualityCertificate:
        """Solve quotient problem for specified stalk norm p in {1, 2, np.inf}."""
        if omega.degree != 1 or omega.num_cells != self.complex.num_edges:
            raise DimensionMismatchError(
                f"Omega cochain mismatch: cells={omega.num_cells}, deg={omega.degree} vs edges={self.complex.num_edges}"
            )
        if omega.is_operator:
            raise ValueError("ClassicalQuotientSolver requires vector cochains.")

        if p == 2:
            return self._solve_l2(omega, max_iter=max_iter)
        elif p == 1:
            return self._solve_l1(omega)
        elif p == np.inf or p == "inf":
            return self._solve_linf(omega)
        else:
            raise NotImplementedError(
                f"Exact duality certificate not implemented for p={p}; use 1, 2, or np.inf."
            )

    def _solve_l2(
        self, omega: Cochain, max_iter: int = 500
    ) -> ClassicalDualityCertificate:
        """Solve mixed ell^1(E; ell^2) quotient problem via smoothed L-BFGS."""
        m = self.complex.num_edges
        n = self.complex.num_vertices
        k = omega.stalk_dim
        d0 = self.complex.d0_matrix
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

        # Candidate dual witness: z_e = w_e * (r_e / ||r_e||_2)
        candidate_z = np.zeros_like(residual_opt)
        for e in range(m):
            if exact_norms[e] > 1e-8:
                candidate_z[e] = weights[e] * (residual_opt[e] / exact_norms[e])

        # Project candidate_z onto divergence-free subspace d0^* z = 0
        # (d0 d0^T) is not what we want; divergence is d0^T z = 0.
        # Decomposition: z = d0 beta + z_proj => d0^T z = d0^T d0 beta => solve (d0^T d0) beta = d0^T z
        laplacian = d0.T @ d0
        rhs = d0.T @ candidate_z
        beta, _, _, _ = np.linalg.lstsq(laplacian, rhs, rcond=None)
        projected_z = candidate_z - d0 @ beta

        # Scale if projected_z exceeds ball constraints ||z_e||_2 <= w_e
        proj_norms = np.linalg.norm(projected_z, axis=1)
        ratios = proj_norms / weights
        max_ratio = float(np.max(ratios))
        if max_ratio > 1.0:
            projected_z = projected_z / max_ratio
            proj_norms = proj_norms / max_ratio

        dual_val = float(np.sum(projected_z * w_data))
        div = d0.T @ projected_z
        max_div = float(np.max(np.abs(div)))
        max_ball_viol = float(np.max(np.maximum(0.0, proj_norms - weights)))
        gap = abs(primal_val - dual_val)

        is_div_free = max_div <= self.tol
        is_ball_feas = max_ball_viol <= 1e-7
        is_optimal = gap <= self.tol and is_div_free and is_ball_feas

        return ClassicalDualityCertificate(
            p_norm=2,
            primal_value=primal_val,
            dual_value=dual_val,
            duality_gap=gap,
            primal_repair=Cochain(alpha_opt, degree=0),
            residual_cochain=Cochain(residual_opt, degree=1),
            dual_witness=Cochain(projected_z, degree=1),
            divergence_norm=max_div,
            max_dual_norm_violation=max_ball_viol,
            is_divergence_free=is_div_free,
            is_dual_feasible=is_ball_feas,
            is_optimal=is_optimal,
            details={
                "iterations": res.nit,
                "message": res.message,
                "success": res.success,
            },
        )

    def _solve_l1(self, omega: Cochain) -> ClassicalDualityCertificate:
        """Solve coordinate ell^1(E; ell^1) quotient problem via exact LP."""
        m = self.complex.num_edges
        n = self.complex.num_vertices
        k = omega.stalk_dim
        d0 = self.complex.d0_matrix
        weights = self.complex.edge_weights
        w_data = omega.data

        # Variables: [alpha_{0,0}..alpha_{n-1,k-1}, t_{0,0}..t_{m-1,k-1}]
        # Objective: sum_{e,j} w_e t_{e,j}
        c = np.concatenate([np.zeros(n * k), np.repeat(weights, k)])

        A_rows = []
        b_rows = []

        for e in range(m):
            for j in range(k):
                # -(d0 alpha)_{e,j} - t_{e,j} <= -omega_{e,j}
                row1 = np.zeros(n * k + m * k)
                for u in range(n):
                    row1[u * k + j] = -d0[e, u]
                row1[n * k + e * k + j] = -1.0
                A_rows.append(row1)
                b_rows.append(-w_data[e, j])

                # (d0 alpha)_{e,j} - t_{e,j} <= omega_{e,j}
                row2 = np.zeros(n * k + m * k)
                for u in range(n):
                    row2[u * k + j] = d0[e, u]
                row2[n * k + e * k + j] = -1.0
                A_rows.append(row2)
                b_rows.append(w_data[e, j])

        A_ub = np.array(A_rows)
        b_ub = np.array(b_rows)
        bounds = [(None, None)] * (n * k) + [(0, None)] * (m * k)

        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
        if not res.success:
            raise RuntimeError(f"Linear program failed for L1 quotient: {res.message}")

        alpha_opt = res.x[: n * k].reshape((n, k))
        residual_opt = w_data - d0 @ alpha_opt
        primal_val = float(np.sum(weights[:, None] * np.abs(residual_opt)))

        # Extract dual variables from marginals:
        # Each constraint has marginal lambda >= 0.
        # z_{e,j} = lambda_{e,j,+} - lambda_{e,j,-}
        marginals = res.ineqlin.marginals
        dual_z = np.zeros((m, k), dtype=float)
        idx = 0
        for e in range(m):
            for j in range(k):
                lam_plus = marginals[idx]
                lam_minus = marginals[idx + 1]
                dual_z[e, j] = lam_minus - lam_plus
                idx += 2

        dual_val = float(np.sum(dual_z * w_data))
        div = d0.T @ dual_z
        max_div = float(np.max(np.abs(div)))

        # Dual norm of l1 is linf: ||z_e||_inf <= w_e
        z_inf_norms = np.max(np.abs(dual_z), axis=1)
        max_ball_viol = float(np.max(np.maximum(0.0, z_inf_norms - weights)))
        gap = abs(primal_val - dual_val)

        is_div_free = max_div <= self.tol
        is_ball_feas = max_ball_viol <= 1e-7
        is_optimal = gap <= self.tol and is_div_free and is_ball_feas

        return ClassicalDualityCertificate(
            p_norm=1,
            primal_value=primal_val,
            dual_value=dual_val,
            duality_gap=gap,
            primal_repair=Cochain(alpha_opt, degree=0),
            residual_cochain=Cochain(residual_opt, degree=1),
            dual_witness=Cochain(dual_z, degree=1),
            divergence_norm=max_div,
            max_dual_norm_violation=max_ball_viol,
            is_divergence_free=is_div_free,
            is_dual_feasible=is_ball_feas,
            is_optimal=is_optimal,
            details={
                "iterations": res.nit,
                "message": res.message,
                "success": res.success,
            },
        )

    def _solve_linf(self, omega: Cochain) -> ClassicalDualityCertificate:
        """Solve ell^1(E; ell^inf) quotient problem via exact LP."""
        m = self.complex.num_edges
        n = self.complex.num_vertices
        k = omega.stalk_dim
        d0 = self.complex.d0_matrix
        weights = self.complex.edge_weights
        w_data = omega.data

        # Variables: [alpha_{0,0}..alpha_{n-1,k-1}, t_0..t_{m-1}] (1 slack per edge)
        # Objective: sum_e w_e t_e
        c = np.concatenate([np.zeros(n * k), weights])

        A_rows = []
        b_rows = []

        for e in range(m):
            for j in range(k):
                # -(d0 alpha)_{e,j} - t_e <= -omega_{e,j}
                row1 = np.zeros(n * k + m)
                for u in range(n):
                    row1[u * k + j] = -d0[e, u]
                row1[n * k + e] = -1.0
                A_rows.append(row1)
                b_rows.append(-w_data[e, j])

                # (d0 alpha)_{e,j} - t_e <= omega_{e,j}
                row2 = np.zeros(n * k + m)
                for u in range(n):
                    row2[u * k + j] = d0[e, u]
                row2[n * k + e] = -1.0
                A_rows.append(row2)
                b_rows.append(w_data[e, j])

        A_ub = np.array(A_rows)
        b_ub = np.array(b_rows)
        bounds = [(None, None)] * (n * k) + [(0, None)] * m

        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
        if not res.success:
            raise RuntimeError(
                f"Linear program failed for Linf quotient: {res.message}"
            )

        alpha_opt = res.x[: n * k].reshape((n, k))
        residual_opt = w_data - d0 @ alpha_opt
        primal_val = float(np.sum(weights * np.max(np.abs(residual_opt), axis=1)))

        marginals = res.ineqlin.marginals
        dual_z = np.zeros((m, k), dtype=float)
        idx = 0
        for e in range(m):
            for j in range(k):
                lam_plus = marginals[idx]
                lam_minus = marginals[idx + 1]
                dual_z[e, j] = lam_minus - lam_plus
                idx += 2

        dual_val = float(np.sum(dual_z * w_data))
        div = d0.T @ dual_z
        max_div = float(np.max(np.abs(div)))

        # Dual norm of linf is l1: ||z_e||_1 <= w_e
        z_l1_norms = np.sum(np.abs(dual_z), axis=1)
        max_ball_viol = float(np.max(np.maximum(0.0, z_l1_norms - weights)))
        gap = abs(primal_val - dual_val)

        is_div_free = max_div <= self.tol
        is_ball_feas = max_ball_viol <= 1e-7
        is_optimal = gap <= self.tol and is_div_free and is_ball_feas

        return ClassicalDualityCertificate(
            p_norm=np.inf,
            primal_value=primal_val,
            dual_value=dual_val,
            duality_gap=gap,
            primal_repair=Cochain(alpha_opt, degree=0),
            residual_cochain=Cochain(residual_opt, degree=1),
            dual_witness=Cochain(dual_z, degree=1),
            divergence_norm=max_div,
            max_dual_norm_violation=max_ball_viol,
            is_divergence_free=is_div_free,
            is_dual_feasible=is_ball_feas,
            is_optimal=is_optimal,
            details={
                "iterations": res.nit,
                "message": res.message,
                "success": res.success,
            },
        )

    def cycle_analytic_quotient(
        self, omega: Cochain, p: Union[int, float] = 2
    ) -> float:
        """
        Analytical cycle quotient formula for a simple cycle with edge orientations.
        Phi_{p,1,w}([omega]) = (min_e w_e) ||sum_e omega_e||_p.
        """
        c = np.sum(omega.data, axis=0)
        min_w = float(np.min(self.complex.edge_weights))
        if p == 1:
            norm_c = float(np.sum(np.abs(c)))
        elif p == 2:
            norm_c = float(np.linalg.norm(c))
        elif p == np.inf or p == "inf":
            norm_c = float(np.max(np.abs(c)))
        else:
            norm_c = float(np.power(np.sum(np.power(np.abs(c), p)), 1.0 / p))
        return min_w * norm_c
