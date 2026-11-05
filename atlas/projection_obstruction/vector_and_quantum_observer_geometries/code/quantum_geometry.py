"""
Quantum Observer Geometries, Trace-Norm Stalks, and Helstrom Dual Solvers.
Paper: GS-003 (vector_and_quantum_observer_geometries)
AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List, Union
import numpy as np
from scipy.optimize import minimize

from cochain_complex import GraphComplex, Cochain
from exceptions import NonHermitianOperatorError, DimensionMismatchError


class HermitianOperator:
    """Utilities for traceless Hermitian operators in Herm_0(C^d)."""

    # Pauli matrices for d = 2
    SIGMA_0 = np.eye(2, dtype=complex)
    SIGMA_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    SIGMA_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
    SIGMA_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    PAULI_VECTOR = [SIGMA_X, SIGMA_Y, SIGMA_Z]

    @staticmethod
    def check_hermitian(mat: np.ndarray, tol: float = 1e-7) -> None:
        """Assert matrix is Hermitian; raise NonHermitianOperatorError if violated."""
        if not isinstance(mat, np.ndarray):
            mat = np.asarray(mat)
        if mat.ndim != 2 or mat.shape[0] != mat.shape[1]:
            raise DimensionMismatchError(
                f"Matrix must be square 2D, got shape {mat.shape}"
            )
        diff = mat - mat.conj().T
        err = float(np.max(np.abs(diff)))
        if err > tol:
            raise NonHermitianOperatorError(
                f"Operator is non-Hermitian: ||X - X^dag||_max = {err:.2e} > {tol:.2e}"
            )

    @staticmethod
    def check_traceless(mat: np.ndarray, tol: float = 1e-7) -> bool:
        """Check if operator is traceless within numerical tolerance."""
        tr = float(np.abs(np.trace(mat)))
        return tr <= tol

    @classmethod
    def schatten_norm(
        cls, mat: np.ndarray, p: Union[int, float] = 1, check: bool = True
    ) -> float:
        """
        Compute Schatten p-norm ||mat||_p = (sum_i sigma_i^p)^{1/p}.
        For p=1: trace norm ||mat||_1 = sum_i sigma_i.
        For p=2: Frobenius norm ||mat||_2 = sqrt(sum_i sigma_i^2).
        For p=inf: operator norm ||mat||_inf = max_i sigma_i.
        """
        if check:
            cls.check_hermitian(mat)
        s = np.linalg.svdvals(mat)
        if p == 1:
            return float(np.sum(s))
        elif p == 2:
            return float(np.sqrt(np.sum(s**2)))
        elif p == np.inf or p == "inf":
            return float(np.max(s)) if len(s) > 0 else 0.0
        else:
            return float(np.power(np.sum(np.power(s, p)), 1.0 / p))

    @classmethod
    def trace_distance(cls, mat: np.ndarray, check: bool = True) -> float:
        """Quantum trace-distance gauge j_Q(X) = 0.5 * ||X||_1."""
        return 0.5 * cls.schatten_norm(mat, p=1, check=check)

    @classmethod
    def to_bloch_vector(cls, mat: np.ndarray, check: bool = True) -> np.ndarray:
        """
        Extract Bloch vector v in R^3 for a 2x2 traceless Hermitian operator X = v . sigma.
        v_k = 0.5 * Tr(X sigma_k).
        """
        if check:
            cls.check_hermitian(mat)
        if mat.shape != (2, 2):
            raise DimensionMismatchError(
                f"Bloch vector mapping only defined for d=2, got shape {mat.shape}"
            )
        v = np.zeros(3, dtype=float)
        for k in range(3):
            v[k] = 0.5 * float(np.real(np.trace(mat @ cls.PAULI_VECTOR[k])))
        return v

    @classmethod
    def from_bloch_vector(cls, v: np.ndarray) -> np.ndarray:
        """Construct 2x2 traceless Hermitian operator X = v . sigma from v in R^3."""
        v_arr = np.asarray(v, dtype=float).flatten()
        if len(v_arr) != 3:
            raise DimensionMismatchError(
                f"Expected 3-element Bloch vector, got length {len(v_arr)}"
            )
        return v_arr[0] * cls.SIGMA_X + v_arr[1] * cls.SIGMA_Y + v_arr[2] * cls.SIGMA_Z

    @staticmethod
    def gell_mann_basis(d: int) -> List[np.ndarray]:
        """
        Construct generalized Gell-Mann basis for Herm_0(C^d).
        Returns d^2 - 1 traceless Hermitian matrices normalized so Tr(lambda_a lambda_b) = 2 delta_{ab}.
        """
        basis: List[np.ndarray] = []

        # 1. Symmetric generators: E_{j,k} + E_{k,j} for 1 <= j < k <= d
        for j in range(d):
            for k in range(j + 1, d):
                m = np.zeros((d, d), dtype=complex)
                m[j, k] = 1.0
                m[k, j] = 1.0
                basis.append(m)

        # 2. Anti-symmetric generators: -i(E_{j,k} - E_{k,j}) for 1 <= j < k <= d
        for j in range(d):
            for k in range(j + 1, d):
                m = np.zeros((d, d), dtype=complex)
                m[j, k] = -1.0j
                m[k, j] = 1.0j
                basis.append(m)

        # 3. Diagonal generators: sqrt(2 / (l*(l+1))) * (sum_{j=1}^l E_{j,j} - l E_{l+1,l+1})
        for l in range(1, d):
            m = np.zeros((d, d), dtype=complex)
            norm = np.sqrt(2.0 / (l * (l + 1)))
            for j in range(l):
                m[j, j] = norm
            m[l, l] = -l * norm
            basis.append(m)

        return basis


@dataclass(frozen=True)
class QuantumDualityCertificate:
    """Certificate of primal and dual optimality for quantum trace-norm quotient obstruction."""

    primal_value: float
    dual_value: float
    duality_gap: float
    primal_repair: Cochain
    residual_cochain: Cochain
    dual_witness: Cochain
    divergence_norm: float
    max_spectral_norm_violation: float
    is_divergence_free: bool
    is_dual_feasible: bool
    is_optimal: bool
    details: Dict[str, Any]


class QuantumQuotientSolver:
    """
    Solves the quantum trace-distance quotient obstruction functional:
        Phi_Q([delta]) = inf_{phi in C^0_Q} sum_e w_e * 0.5 * ||delta_e - (d0 phi)_e||_1
    and evaluates the dual Helstrom witness:
        Psi_Q(delta) = sup_{varphi in C^1_Q} sum_e Re(Tr(varphi_e delta_e))
        s.t. d0^* varphi = 0, ||varphi_e||_inf <= w_e / 2.
    """

    def __init__(self, complex: GraphComplex, tol: float = 1e-4) -> None:
        self.complex = complex
        self.tol = tol

    def solve(
        self,
        delta: Cochain,
        max_iter: int = 500,
        check_hermitian: bool = True,
    ) -> QuantumDualityCertificate:
        """
        Solve quantum quotient obstruction problem using basis expansion over Herm_0(C^d).
        """
        if delta.degree != 1 or delta.num_cells != self.complex.num_edges:
            raise DimensionMismatchError(
                f"Delta cochain mismatch: cells={delta.num_cells}, deg={delta.degree} vs edges={self.complex.num_edges}"
            )
        if not delta.is_operator:
            raise ValueError(
                "QuantumQuotientSolver requires operator cochains (ndim=3)."
            )

        m = self.complex.num_edges
        n = self.complex.num_vertices
        d = delta.stalk_dim
        weights = self.complex.edge_weights
        delta_data = delta.data

        if check_hermitian:
            for e in range(m):
                HermitianOperator.check_hermitian(delta_data[e])

        # Basis for Herm_0(C^d)
        basis = HermitianOperator.gell_mann_basis(d)
        num_gen = len(basis)  # d^2 - 1

        # We gauge-fix vertex 0 = 0. Parameterize phi(1)..phi(n-1):
        # params shape ((n - 1) * num_gen,)
        num_free_verts = max(1, n - 1)

        def make_phi(params_flat: np.ndarray) -> np.ndarray:
            p = params_flat.reshape((num_free_verts, num_gen))
            phi_arr = np.zeros((n, d, d), dtype=complex)
            for u in range(num_free_verts):
                mat = np.zeros((d, d), dtype=complex)
                for a in range(num_gen):
                    mat += 0.5 * p[u, a] * basis[a]
                phi_arr[u + 1] = mat
            return phi_arr

        def primal_objective(params_flat: np.ndarray) -> float:
            phi_arr = make_phi(params_flat)
            total = 0.0
            for e, (u, v) in enumerate(self.complex.edges):
                d0_phi = phi_arr[v] - phi_arr[u]
                res = delta_data[e] - d0_phi
                s = np.linalg.svdvals(res)
                total += weights[e] * 0.5 * float(np.sum(s))
            return total

        init_params = np.zeros(num_free_verts * num_gen, dtype=float)
        opt_res = minimize(
            fun=primal_objective,
            x0=init_params,
            method="Powell",
            options={"maxiter": max_iter, "ftol": 1e-9, "xtol": 1e-9},
        )

        opt_phi_arr = make_phi(opt_res.x)
        primal_repair_cochain = Cochain(opt_phi_arr, degree=0)
        d0_repair = self.complex.d0(primal_repair_cochain)
        residual_arr = delta_data - d0_repair.data
        residual_cochain = Cochain(residual_arr, degree=1)

        primal_val = float(residual_cochain.trace_norm(weights=weights))

        # Construct Candidate Dual Helstrom Witness varphi:
        # At optimum, a subgradient of 0.5 * ||R_e||_1 is 0.5 * U sgn(Sigma) V^dag
        candidate_dual = np.zeros((m, d, d), dtype=complex)
        for e in range(m):
            mat = residual_arr[e]
            s = np.linalg.svdvals(mat)
            if float(np.sum(s)) > 1e-8:
                u_mat, s_vec, vh_mat = np.linalg.svd(mat)
                # sgn(mat) = u @ vh for Hermitian
                sgn = u_mat @ vh_mat
                # ensure Hermitian
                sgn = 0.5 * (sgn + sgn.conj().T)
                candidate_dual[e] = 0.5 * weights[e] * sgn
            else:
                candidate_dual[e] = np.zeros((d, d), dtype=complex)

        # Project candidate_dual onto divergence-free subspace d0^* varphi = 0
        # d0^* varphi at vertex u is sum_{e: target=u} varphi_e - sum_{e: source=u} varphi_e
        # In matrix entries (d x d), this is independent per component:
        # (d0.T @ d0) B_{j,k} = d0.T candidate_{j,k}
        d0 = self.complex.d0_matrix
        laplacian = d0.T @ d0
        projected_dual = np.zeros_like(candidate_dual)

        for j in range(d):
            for k in range(d):
                rhs = d0.T @ candidate_dual[:, j, k]
                beta, _, _, _ = np.linalg.lstsq(laplacian, rhs, rcond=None)
                projected_dual[:, j, k] = candidate_dual[:, j, k] - d0 @ beta

        # Symmetrize each projected_dual[e] to ensure exact Hermiticity
        for e in range(m):
            projected_dual[e] = 0.5 * (projected_dual[e] + projected_dual[e].conj().T)

        # Scale projected_dual if spectral norm exceeds w_e / 2: ||varphi_e||_inf <= w_e / 2
        spec_norms = np.array(
            [
                HermitianOperator.schatten_norm(
                    projected_dual[e], p=np.inf, check=False
                )
                for e in range(m)
            ]
        )
        max_allowed = 0.5 * weights
        ratios = np.zeros(m, dtype=float)
        for e in range(m):
            if max_allowed[e] > 1e-12:
                ratios[e] = spec_norms[e] / max_allowed[e]
        max_ratio = float(np.max(ratios)) if len(ratios) > 0 else 0.0
        if max_ratio > 1.0:
            projected_dual = projected_dual / max_ratio
            spec_norms = spec_norms / max_ratio

        dual_witness_cochain = Cochain(projected_dual, degree=1)
        dual_val = float(
            sum(np.real(np.trace(projected_dual[e] @ delta_data[e])) for e in range(m))
        )

        # Check divergence d0^* varphi
        div_cochain = self.complex.d0_adjoint(dual_witness_cochain)
        max_div = float(
            max(
                HermitianOperator.schatten_norm(div_cochain[u], p=np.inf, check=False)
                for u in range(n)
            )
        )
        max_ball_viol = float(np.max(np.maximum(0.0, spec_norms - max_allowed)))
        gap = abs(primal_val - dual_val)

        is_div_free = max_div <= self.tol
        is_ball_feas = max_ball_viol <= 1e-6
        is_optimal = gap <= self.tol and is_div_free and is_ball_feas

        return QuantumDualityCertificate(
            primal_value=primal_val,
            dual_value=dual_val,
            duality_gap=gap,
            primal_repair=primal_repair_cochain,
            residual_cochain=residual_cochain,
            dual_witness=dual_witness_cochain,
            divergence_norm=max_div,
            max_spectral_norm_violation=max_ball_viol,
            is_divergence_free=is_div_free,
            is_dual_feasible=is_ball_feas,
            is_optimal=is_optimal,
            details={
                "iterations": opt_res.nit,
                "message": opt_res.message,
                "success": opt_res.success,
            },
        )

    def cycle_analytic_quotient(self, delta: Cochain) -> float:
        """
        Analytical cycle quotient obstruction for a simple directed cycle.
        Phi_Q([delta]) = (min_e w_e) * 0.5 * ||sum_e delta_e||_1.
        """
        c = np.sum(delta.data, axis=0)
        min_w = float(np.min(self.complex.edge_weights))
        return min_w * 0.5 * HermitianOperator.schatten_norm(c, p=1)
