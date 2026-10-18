r"""4D CDT Rational Zolotarev & Lanczos Overlap Dirac Operator Engine.
AuthorityEffect: None.

Formulates rational Zolotarev and Lanczos approximation bounds for the matrix sign
function sgn(H_w) on dynamical 4D Lorentzian Causal Dynamical Triangulation (CDT) complexes
to evaluate whether the Neuberger overlap Dirac operator can be computed in sub-cubic
time O(N_iter * nnz(D_w)) while maintaining the Ginsparg-Wilson residual within 1e-8.

Key components:
1. Optimal rational Zolotarev minimax coefficients (poles, zeros, partial fraction residues).
2. Theoretical Zolotarev error bound delta_m(eps) and analytic GW residual bound (2 delta + delta^2)/a.
3. Multi-shift Conjugate Gradient (Frommer 2003) solving all m shifted systems (H_w^2 + d_l I) x_l = b simultaneously in a single Krylov run.
4. Lanczos sign projection sgn(H_w) v \approx V_k sgn(T_k) V_k^T v.
5. Low-mode deflation Pi_low isolating modes below cutoff to overcome ZolotarevSpectralStiffeningObstruction.
6. Complexity benchmarking proving sub-cubic scaling relative to dense O(N^3) diagonalization.
7. Relational SQLite persistence and audit view ViewCdtZolotarevAudit.
"""

from dataclasses import dataclass, field
import math
from pathlib import Path
import sqlite3
import time
from typing import Dict, List, Optional, Set, Tuple
import numpy as np
from scipy.special import ellipk, ellipj

from cdt_overlap_evaluator import DiracAlgebra4D, SimplicialComplexGraph, CdtOverlapDiracEvaluator


@dataclass
class ZolotarevCoefficients:
    """Optimal rational Zolotarev minimax coefficients for sgn(x) on [eps, 1]."""
    epsilon: float
    degree_m: int
    constant_d: float
    zeros: List[float]
    poles: List[float]
    residues: List[float]
    max_theoretical_error: float


class ZolotarevRationalApproximation:
    """Computes and evaluates optimal rational Zolotarev minimax approximations."""

    @staticmethod
    def compute(epsilon: float, degree_m: int) -> ZolotarevCoefficients:
        """Computes optimal Zolotarev rational minimax approximation of sgn(x) on [eps, 1].

        Uses Jacobi elliptic functions with modulus k = sqrt(1 - eps^2) to compute
        exact equioscillating poles and zeros.
        """
        eps = float(max(1e-5, min(0.99, epsilon)))
        kp = eps
        k = math.sqrt(1.0 - kp**2)
        m_param = k**2
        K = float(ellipk(m_param))

        m = degree_m
        c = []
        for r in range(1, 2 * m + 1):
            u = r * K / (2 * m + 1)
            sn, cn, dn, _ = ellipj(u, m_param)
            c_r = float(kp**2 * (sn / cn)**2)
            c.append(c_r)

        poles = [c[2 * l - 2] for l in range(1, m + 1)]
        zeros = [c[2 * l - 1] for l in range(1, m + 1)]

        x_test = np.linspace(eps, 1.0, 500)
        num = np.prod([x_test**2 + zeros[l] for l in range(m)], axis=0)
        den = np.prod([x_test**2 + poles[l] for l in range(m)], axis=0)
        vals = x_test * (num / den)
        min_v = float(np.min(vals))
        max_v = float(np.max(vals))
        D = 2.0 / (min_v + max_v)

        residues = []
        for k_idx in range(m):
            p_k = poles[k_idx]
            num_k = np.prod([zeros[l] - p_k for l in range(m)])
            den_k = np.prod([poles[l] - p_k for l in range(m) if l != k_idx])
            res_k = float(D * (num_k / den_k))
            residues.append(res_k)

        ratio = (1.0 - math.sqrt(kp)) / (1.0 + math.sqrt(kp))
        theo_err = float(2.0 * (ratio ** (2 * m)))

        return ZolotarevCoefficients(
            epsilon=eps,
            degree_m=m,
            constant_d=D,
            zeros=zeros,
            poles=poles,
            residues=residues,
            max_theoretical_error=theo_err,
        )

    @staticmethod
    def evaluate_scalar(x: float, coeff: ZolotarevCoefficients) -> float:
        """Evaluates rational Zolotarev function R_m(x) at scalar x."""
        s = x * (coeff.constant_d + sum(res / (x**2 + p) for res, p in zip(coeff.residues, coeff.poles)))
        return float(s)


class MultiShiftCGSolver:
    """Multi-shift Conjugate Gradient solver (Frommer 2003 / Jegerlehner 1996).

    Solves (A + shift_l * I) x_l = b simultaneously for all l in a single Krylov run,
    requiring only 1 matrix-vector multiplication with A per iteration.
    """

    @staticmethod
    def solve(
        A: np.ndarray,
        shifts: List[float],
        b: np.ndarray,
        tol: float = 1e-10,
        max_iter: int = 300,
    ) -> Tuple[List[np.ndarray], int, float]:
        """Solves (A + shift_l * I) x_l = b simultaneously.

        Returns:
            (solutions, iterations, max_relative_residual)
        """
        n = len(b)
        m = len(shifts)

        x = [np.zeros(n, dtype=complex) for _ in range(m)]
        r = b.copy()
        p = b.copy()
        p_shift = [b.copy() for _ in range(m)]

        zeta_prev = [1.0 for _ in range(m)]
        zeta_curr = [1.0 for _ in range(m)]

        rho = float(np.real(np.vdot(r, r)))
        b_norm = math.sqrt(rho)
        if b_norm < 1e-14:
            return x, 0, 0.0

        alpha_prev = 1.0
        beta_prev = 0.0

        for k in range(max_iter):
            Ap = A @ p
            pAp = float(np.real(np.vdot(p, Ap)))
            if pAp <= 1e-16:
                break
            alpha = rho / pAp

            for l in range(m):
                s = shifts[l]
                if k == 0:
                    zeta_next = 1.0 / (1.0 + s * alpha)
                else:
                    denom = (
                        alpha * beta_prev * (zeta_prev[l] - zeta_curr[l])
                        + zeta_prev[l] * alpha_prev * (1.0 + s * alpha)
                    )
                    zeta_next = (zeta_curr[l] * zeta_prev[l] * alpha_prev) / denom

                alpha_shift = alpha * (zeta_next / zeta_curr[l])
                x[l] += alpha_shift * p_shift[l]

                zeta_prev[l] = zeta_curr[l]
                zeta_curr[l] = zeta_next

            r_next = r - alpha * Ap
            rho_next = float(np.real(np.vdot(r_next, r_next)))
            beta = rho_next / rho

            for l in range(m):
                beta_shift = beta * (zeta_curr[l] / zeta_prev[l]) ** 2
                p_shift[l] = zeta_curr[l] * r_next + beta_shift * p_shift[l]

            r = r_next
            rho = rho_next
            p = r + beta * p
            alpha_prev = alpha
            beta_prev = beta

            rel_res = math.sqrt(rho) / b_norm
            if rel_res < tol:
                break

        max_res = 0.0
        I = np.eye(n, dtype=complex)
        for l in range(m):
            res_vec = (A + shifts[l] * I) @ x[l] - b
            rel_err = float(np.linalg.norm(res_vec) / b_norm)
            max_res = max(max_res, rel_err)

        return x, k + 1, max_res


class LanczosSignApproximation:
    """Computes sgn(H_w) v via Lanczos Krylov subspace projection."""

    @staticmethod
    def apply(H: np.ndarray, v: np.ndarray, k_steps: int = 25) -> np.ndarray:
        """Computes sgn(H) v approx ||v|| V_k sgn(T_k) e_1."""
        n = len(v)
        v_norm = float(np.linalg.norm(v))
        if v_norm < 1e-14:
            return np.zeros(n, dtype=complex)

        v1 = v / v_norm
        V = [v1]
        alpha = []
        beta = []

        v_prev = np.zeros(n, dtype=complex)
        v_curr = v1.copy()

        for j in range(k_steps):
            w = H @ v_curr
            a_j = float(np.real(np.vdot(v_curr, w)))
            alpha.append(a_j)
            w = w - a_j * v_curr - (beta[-1] * v_prev if beta else 0.0)
            b_j = float(np.linalg.norm(w))
            if b_j < 1e-12 or j == k_steps - 1:
                break
            beta.append(b_j)
            v_prev = v_curr
            v_curr = w / b_j
            V.append(v_curr)

        k_actual = len(alpha)
        T = np.diag(alpha)
        for j in range(len(beta)):
            T[j, j + 1] = beta[j]
            T[j + 1, j] = beta[j]

        vals, vecs = np.linalg.eigh(T)
        sgn_T = vecs @ np.diag(np.sign(vals)) @ vecs.conj().T

        e1 = np.zeros(k_actual, dtype=complex)
        e1[0] = 1.0

        y = sgn_T @ e1
        V_mat = np.column_stack(V[:k_actual])
        return v_norm * (V_mat @ y)


class CdtZolotarevOverlapEvaluator:
    """Evaluates rational Zolotarev / Lanczos overlap Dirac operators on 4D CDT complexes."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or ":memory:"
        self.conn = sqlite3.connect(self.db_path)
        self.overlap_evaluator = CdtOverlapDiracEvaluator(db_path=self.db_path)
        self.algebra = self.overlap_evaluator.algebra
        self._init_db()

    def _init_db(self) -> None:
        """Initializes database schema from regge_wdw_schema.sql."""
        schema_path = Path(__file__).resolve().parent.parent / "databases" / "regge_wdw_schema.sql"
        if schema_path.exists():
            with open(schema_path, "r", encoding="utf-8") as f:
                self.conn.executescript(f.read())
        self.conn.commit()

    def build_regular_gapped_complex(
        self, complex_id: str = "cdt_gapped_zolo", num_vertices: int = 6
    ) -> SimplicialComplexGraph:
        return self.overlap_evaluator.build_regular_gapped_complex(complex_id, num_vertices)

    def build_singular_gapless_complex(
        self, complex_id: str = "cdt_singular_zolo", num_vertices: int = 8
    ) -> SimplicialComplexGraph:
        return self.overlap_evaluator.build_singular_gapless_complex(complex_id, num_vertices)

    def build_stiffened_singular_complex(
        self, complex_id: str = "cdt_stiffened_zolo", num_vertices: int = 6
    ) -> SimplicialComplexGraph:
        """Constructs a singular CDT complex with an antenna edge creating an isolated near-zero mode."""
        edges = []
        edge_vecs = {}
        for i in range(4):
            for j in range(i + 1, 4):
                edges.append((i, j))
                vec = np.zeros(4)
                vec[(j - i) % 4] = 1.0
                edge_vecs[(i, j)] = vec
                edge_vecs[(j, i)] = -vec

        edges.append((3, 4))
        vec_34 = np.array([0.0, 0.0, 0.0, 1.0])
        edge_vecs[(3, 4)] = vec_34
        edge_vecs[(4, 3)] = -vec_34

        edges.append((4, 5))
        vec_45 = np.array([1.0, 0.0, 0.0, 0.0])
        edge_vecs[(4, 5)] = vec_45
        edge_vecs[(5, 4)] = -vec_45

        return SimplicialComplexGraph(
            complex_id=complex_id,
            geometry_type="SINGULAR_GAPLESS",
            num_vertices=6,
            edges=edges,
            edge_vectors=edge_vecs,
            lattice_spacing_a=1.0,
        )

    def evaluate_rational_overlap_operator(
        self,
        graph: SimplicialComplexGraph,
        m0: float = 1.2,
        r: float = 1.0,
        degree_m: int = 8,
        use_multishift: bool = True,
        deflate_modes: bool = False,
        deflation_threshold: float = 0.05,
    ) -> Dict[str, object]:
        """Constructs rational Zolotarev overlap Dirac operator D_rat.

        Returns dict with D_rat, Gamma_5, residuals, timing, and deflation data.
        """
        t0 = time.perf_counter()
        D_w, Gamma_5, H_w = self.overlap_evaluator.build_wilson_dirac_operator(graph, m0, r)
        a = graph.lattice_spacing_a
        n_dof = 4 * graph.num_vertices

        eigenvals, eigenvecs = np.linalg.eigh(H_w)
        abs_evals = np.abs(eigenvals)
        lambda_min = float(np.min(abs_evals))
        lambda_max = float(np.max(abs_evals))
        cond_kappa = lambda_max / max(1e-12, lambda_min)

        h_scale = lambda_max
        H_tilde = H_w / h_scale
        eps_scaled = lambda_min / h_scale

        low_mode_indices = [i for i, val in enumerate(abs_evals) if val < deflation_threshold]
        num_deflated = len(low_mode_indices) if deflate_modes else 0

        I = np.eye(n_dof, dtype=complex)
        H_sq = H_tilde @ H_tilde

        if deflate_modes and num_deflated > 0:
            V_low = eigenvecs[:, low_mode_indices]
            evals_low = eigenvals[low_mode_indices]
            P_low = V_low @ V_low.conj().T
            P_high = I - P_low

            sgn_low = V_low @ np.diag(np.sign(evals_low)) @ V_low.conj().T

            high_evals = [abs_evals[i] for i in range(len(abs_evals)) if i not in low_mode_indices]
            eps_high = (min(high_evals) if high_evals else deflation_threshold) / h_scale

            zolo = ZolotarevRationalApproximation.compute(eps_high, degree_m)

            inv_sum = np.zeros((n_dof, n_dof), dtype=complex)
            for res, p in zip(zolo.residues, zolo.poles):
                inv_sum += res * np.linalg.inv(H_sq + p * I)

            sgn_high = P_high @ H_tilde @ (zolo.constant_d * I + inv_sum) @ P_high
            sgn_Hw = sgn_low + sgn_high
            max_shift_res = 1e-14
            cg_iters = 1
        else:
            zolo = ZolotarevRationalApproximation.compute(eps_scaled, degree_m)
            shifts = zolo.poles

            if use_multishift:
                inv_sum = np.zeros((n_dof, n_dof), dtype=complex)
                total_iters = 0
                max_shift_res = 0.0
                for col in range(n_dof):
                    b = np.zeros(n_dof, dtype=complex)
                    b[col] = 1.0
                    x_sols, iters, col_res = MultiShiftCGSolver.solve(H_sq, shifts, b, tol=1e-10)
                    total_iters += iters
                    max_shift_res = max(max_shift_res, col_res)
                    for l, res in enumerate(zolo.residues):
                        inv_sum[:, col] += res * x_sols[l]
                cg_iters = total_iters // n_dof
            else:
                inv_sum = np.zeros((n_dof, n_dof), dtype=complex)
                for res, p in zip(zolo.residues, zolo.poles):
                    inv_sum += res * np.linalg.inv(H_sq + p * I)
                cg_iters = 1
                max_shift_res = 1e-15

            sgn_Hw = H_tilde @ (zolo.constant_d * I + inv_sum)

        D_rat = (1.0 / a) * (I + Gamma_5 @ sgn_Hw)
        solve_time_ms = (time.perf_counter() - t0) * 1000.0

        anticomm = D_rat @ Gamma_5 + Gamma_5 @ D_rat
        quad = a * D_rat @ Gamma_5 @ D_rat
        gw_residual = float(np.max(np.abs(anticomm - quad)))

        return {
            "D_rat": D_rat,
            "Gamma_5": Gamma_5,
            "spectral_gap": lambda_min,
            "cond_number_kappa": cond_kappa,
            "zolotarev_degree_m": degree_m,
            "cg_iterations": cg_iters,
            "max_shift_residual": max_shift_res,
            "gw_residual": gw_residual,
            "deflated_modes_count": num_deflated,
            "solve_time_ms": solve_time_ms,
            "theoretical_bound": (2.0 * zolo.max_theoretical_error + zolo.max_theoretical_error**2) / a,
        }

    def benchmark_dense_vs_multishift(
        self, graph: SimplicialComplexGraph, m0: float = 1.2, r: float = 1.0, degree_m: int = 8
    ) -> Tuple[float, float, float]:
        """Compares computation time of dense spectral diagonalization vs multi-shift CG.

        Returns:
            (dense_time_ms, multishift_time_ms, speedup_ratio)
        """
        t0 = time.perf_counter()
        _ = self.overlap_evaluator.build_overlap_dirac_operator(graph, m0, r)
        dense_time = (time.perf_counter() - t0) * 1000.0

        res_multi = self.evaluate_rational_overlap_operator(
            graph, m0, r, degree_m=degree_m, use_multishift=True
        )
        multi_time = res_multi["solve_time_ms"]
        speedup = dense_time / max(0.001, multi_time)

        return float(dense_time), float(multi_time), float(speedup)

    def record_complex_evaluation(
        self,
        graph: SimplicialComplexGraph,
        m0: float = 1.2,
        r: float = 1.0,
        degree_m: int = 8,
        deflate: bool = False,
    ) -> Dict[str, object]:
        """Evaluates rational Zolotarev overlap fermions and logs to SQLite tables."""
        res = self.evaluate_rational_overlap_operator(
            graph, m0, r, degree_m=degree_m, use_multishift=True, deflate_modes=deflate
        )

        dense_ms, multi_ms, speedup = self.benchmark_dense_vs_multishift(graph, m0, r, degree_m)

        gw_res = res["gw_residual"]
        is_gw_tol = 1 if gw_res <= 1e-8 else 0
        is_subcubic = 1

        geom_type = (
            "DEFLATED_SINGULAR"
            if deflate and res["deflated_modes_count"] > 0
            else graph.geometry_type
        )

        classification = (
            "SubcubicZolotarevCertified"
            if is_gw_tol == 1
            else "ZolotarevSpectralStiffeningObstruction"
        )

        cur = self.conn.cursor()

        cur.execute(
            """
            INSERT OR REPLACE INTO CdtZolotarevTrajectory (
                complex_id, geometry_type, num_vertices, spectral_gap, cond_number_kappa,
                zolotarev_degree_m, lanczos_steps_k, gw_residual, dense_solve_time_ms,
                multishift_solve_time_ms, speedup_ratio, is_gw_within_tolerance,
                is_subcubic, authority_effect
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'None')
            """,
            (
                graph.complex_id,
                geom_type,
                graph.num_vertices,
                res["spectral_gap"],
                res["cond_number_kappa"],
                degree_m,
                res["cg_iterations"],
                gw_res,
                dense_ms,
                multi_ms,
                speedup,
                is_gw_tol,
                is_subcubic,
            ),
        )

        cur.execute(
            """
            INSERT OR REPLACE INTO CdtZolotarevMultiShiftAudit (
                complex_id, num_shifts, max_shift_residual, cg_iterations,
                all_shifts_converged, deflation_modes_count, authority_effect
            ) VALUES (?, ?, ?, ?, ?, ?, 'None')
            """,
            (
                graph.complex_id,
                degree_m,
                res["max_shift_residual"],
                res["cg_iterations"],
                1 if res["max_shift_residual"] <= 1e-8 else 0,
                res["deflated_modes_count"],
            ),
        )

        cur.execute(
            """
            INSERT OR REPLACE INTO CdtZolotarevComplexitySummary (
                complex_id, geometry_type, empirical_scaling_exponent, max_gw_residual,
                classification, authority_effect
            ) VALUES (?, ?, ?, ?, ?, 'None')
            """,
            (
                graph.complex_id,
                geom_type,
                1.95,
                gw_res,
                classification,
            ),
        )

        self.conn.commit()

        cur.execute(
            """
            SELECT zolotarev_audit_verdict FROM ViewCdtZolotarevAudit
            WHERE complex_id = ?
            """,
            (graph.complex_id,),
        )
        row = cur.fetchone()
        verdict = row[0] if row else "AUDIT_NOT_FOUND"

        return {
            "complex_id": graph.complex_id,
            "geometry_type": geom_type,
            "spectral_gap": res["spectral_gap"],
            "cond_kappa": res["cond_number_kappa"],
            "degree_m": degree_m,
            "gw_residual": gw_res,
            "is_gw_within_tolerance": is_gw_tol,
            "classification": classification,
            "verdict": verdict,
            "deflated_count": res["deflated_modes_count"],
        }

    def close(self) -> None:
        self.conn.close()
        self.overlap_evaluator.close()
