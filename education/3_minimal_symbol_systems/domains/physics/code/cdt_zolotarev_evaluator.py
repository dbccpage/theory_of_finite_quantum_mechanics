"""Finite rational and Krylov matrix-sign prototypes.
AuthorityEffect: None.
Legacy filename retained for imports. No CDT implementation, physical certificate,
or sub-cubic complexity guarantee is provided. Floating-point numerical experiments
require independent residual checks; sampled errors are not rigorous bounds.
"""

import math
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
from cdt_overlap_evaluator import CdtOverlapDiracEvaluator, SimplicialComplexGraph
from scipy.special import ellipj, ellipk


@dataclass
class ZolotarevCoefficients:
    """Floating-point elliptic rational coefficients for sgn(x) on [eps, 1]."""

    epsilon: float
    degree_m: int
    constant_d: float
    zeros: List[float]
    poles: List[float]
    residues: List[float]
    sampled_max_error: float


class ZolotarevRationalApproximation:
    """Constructs and evaluates a sampled-scale elliptic rational approximation."""

    @staticmethod
    def compute(epsilon: float, degree_m: int) -> ZolotarevCoefficients:
        """Computes a floating-point rational approximation of sgn(x) on [eps, 1].

        Uses Jacobi elliptic functions with modulus k = sqrt(1 - eps^2) to compute
        floating-point poles and zeros. The scale is fitted on 500 sample points.
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
            c_r = float(kp**2 * (sn / cn) ** 2)
            c.append(c_r)

        poles = [c[2 * l - 2] for l in range(1, m + 1)]  # c_1, c_3, ..., c_{2m-1}
        zeros = [c[2 * l - 1] for l in range(1, m + 1)]  # c_2, c_4, ..., c_{2m}

        # Determine sampled scale factor D on [eps, 1]
        x_test = np.linspace(eps, 1.0, 500)
        num = np.prod([x_test**2 + zeros[l] for l in range(m)], axis=0)
        den = np.prod([x_test**2 + poles[l] for l in range(m)], axis=0)
        vals = x_test * (num / den)
        min_v = float(np.min(vals))
        max_v = float(np.max(vals))
        D = 2.0 / (min_v + max_v)

        # Partial fraction residues:
        # R(x)/x = D * prod(x^2 + zeros) / prod(x^2 + poles) = D + sum_l residues[l] / (x^2 + poles[l])
        residues = []
        for k_idx in range(m):
            p_k = poles[k_idx]
            num_k = np.prod([zeros[l] - p_k for l in range(m)])
            den_k = np.prod([poles[l] - p_k for l in range(m) if l != k_idx])
            res_k = float(D * (num_k / den_k))
            residues.append(res_k)

        # Observed grid error, not a supremum bound.
        sampled_error = float(np.max(np.abs(D * vals - 1.0)))

        return ZolotarevCoefficients(
            epsilon=eps,
            degree_m=m,
            constant_d=D,
            zeros=zeros,
            poles=poles,
            residues=residues,
            sampled_max_error=sampled_error,
        )

    @staticmethod
    def evaluate_scalar(x: float, coeff: ZolotarevCoefficients) -> float:
        """Evaluates rational Zolotarev function R_m(x) at scalar x."""
        s = x * (
            coeff.constant_d + sum(res / (x**2 + p) for res, p in zip(coeff.residues, coeff.poles))
        )
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

            # Shifted solution updates
            for l in range(m):
                s = shifts[l]
                if k == 0:
                    zeta_next = 1.0 / (1.0 + s * alpha)
                else:
                    denom = alpha * beta_prev * (zeta_prev[l] - zeta_curr[l]) + zeta_prev[
                        l
                    ] * alpha_prev * (1.0 + s * alpha)
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

            # Check residual
            rel_res = math.sqrt(rho) / b_norm
            if rel_res < tol:
                break

        # Compute max relative residual across shifted systems
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
