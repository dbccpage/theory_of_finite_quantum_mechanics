"""
Completely Positive Trace-Preserving (CPTP) Channels and Cochain Monotonicity.
Paper: GS-003 (006_vector_and_quantum_observer_geometries)
AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np

from cochain_complex import GraphComplex, Cochain
from quantum_geometry import HermitianOperator, QuantumQuotientSolver
from exceptions import (
    NonCPTPChannelError,
    IntertwiningViolationError,
    DimensionMismatchError,
)


@dataclass(frozen=True)
class KrausChannel:
    """
    Quantum channel in Kraus representation:
        E(X) = sum_k K_k X K_k^dag.
    """

    kraus_operators: List[np.ndarray]

    def __post_init__(self) -> None:
        if not self.kraus_operators:
            raise ValueError("Kraus channel must have at least one Kraus operator.")
        d0, d1 = self.kraus_operators[0].shape
        if d0 != d1:
            raise DimensionMismatchError(
                f"Kraus operators must be square, got {d0}x{d1}"
            )
        for idx, k_mat in enumerate(self.kraus_operators):
            if k_mat.shape != (d0, d0):
                raise DimensionMismatchError(
                    f"Kraus operator {idx} shape {k_mat.shape} != first operator shape {(d0, d0)}"
                )

    @property
    def dimension(self) -> int:
        return self.kraus_operators[0].shape[0]

    def completeness_operator(self) -> np.ndarray:
        """Compute sum_k K_k^dag K_k."""
        d = self.dimension
        s = np.zeros((d, d), dtype=complex)
        for k_mat in self.kraus_operators:
            s += k_mat.conj().T @ k_mat
        return s

    def is_trace_preserving(self, tol: float = 1e-7) -> bool:
        """Check if sum_k K_k^dag K_k = I within tolerance."""
        s = self.completeness_operator()
        diff = s - np.eye(self.dimension, dtype=complex)
        err = float(np.max(np.abs(diff)))
        return err <= tol

    def is_trace_decreasing(self, tol: float = 1e-7) -> bool:
        """Check if sum_k K_k^dag K_k <= I strictly (sub-unital / post-selected)."""
        s = self.completeness_operator()
        eigvals = np.linalg.eigvalsh(s)
        max_eig = float(np.max(eigvals))
        min_eig = float(np.min(eigvals))
        # max_eig <= 1 + tol, and at least one eigenvalue < 1 - tol
        return max_eig <= 1.0 + tol and min_eig < 1.0 - tol

    def is_trace_increasing(self, tol: float = 1e-7) -> bool:
        """Check if sum_k K_k^dag K_k has eigenvalues > 1 + tol (amplifying / non-contractive)."""
        s = self.completeness_operator()
        eigvals = np.linalg.eigvalsh(s)
        return float(np.max(eigvals)) > 1.0 + tol

    def assert_cptp(self, tol: float = 1e-7) -> None:
        """Assert channel is strictly CPTP; raise NonCPTPChannelError if violated."""
        if not self.is_trace_preserving(tol=tol):
            s = self.completeness_operator()
            err = float(np.max(np.abs(s - np.eye(self.dimension))))
            raise NonCPTPChannelError(
                f"Channel violates CPTP trace preservation: ||sum K^dag K - I||_max = {err:.2e} > {tol:.2e}"
            )

    def apply(self, mat: np.ndarray) -> np.ndarray:
        """Apply channel E(X) = sum_k K_k X K_k^dag."""
        out = np.zeros_like(mat, dtype=complex)
        for k_mat in self.kraus_operators:
            out += k_mat @ mat @ k_mat.conj().T
        # Symmetrize if input was Hermitian to maintain numerical Hermiticity
        diff = mat - mat.conj().T
        if np.max(np.abs(diff)) < 1e-9:
            out = 0.5 * (out + out.conj().T)
        return out

    def contractivity_ratio(self, mat: np.ndarray) -> float:
        """Compute ||E(X)||_1 / ||X||_1 for a traceless operator."""
        norm_in = HermitianOperator.schatten_norm(mat, p=1, check=False)
        if norm_in < 1e-12:
            return 1.0
        out = self.apply(mat)
        norm_out = HermitianOperator.schatten_norm(out, p=1, check=False)
        return norm_out / norm_in

    # ---------------- Factory Methods ----------------

    @classmethod
    def unitary(cls, u_mat: np.ndarray) -> KrausChannel:
        """Unitary channel E(X) = U X U^dag."""
        # Verify unitarity
        d = u_mat.shape[0]
        diff = u_mat.conj().T @ u_mat - np.eye(d)
        if np.max(np.abs(diff)) > 1e-7:
            raise ValueError("Input matrix is not unitary.")
        return cls(kraus_operators=[np.asarray(u_mat, dtype=complex)])

    @classmethod
    def depolarizing(cls, d: int, p: float) -> KrausChannel:
        """
        Depolarizing channel on C^d with parameter p in [0, 1]:
            E(rho) = (1 - p) rho + p * (I / d) * Tr(rho).
        For d = 2 (qubit), uses standard 4-Kraus Pauli representation.
        """
        if not (0.0 <= p <= 1.0):
            raise ValueError(f"Depolarizing parameter p must be in [0, 1], got {p}")

        if d == 2:
            # Pauli channel representation:
            # K0 = sqrt(1 - 3p/4) I, K1 = sqrt(p/4) X, K2 = sqrt(p/4) Y, K3 = sqrt(p/4) Z
            k0 = np.sqrt(1.0 - 0.75 * p) * np.eye(2, dtype=complex)
            k1 = np.sqrt(0.25 * p) * HermitianOperator.SIGMA_X
            k2 = np.sqrt(0.25 * p) * HermitianOperator.SIGMA_Y
            k3 = np.sqrt(0.25 * p) * HermitianOperator.SIGMA_Z
            return cls(kraus_operators=[k0, k1, k2, k3])
        else:
            # Replacement-channel Kraus for E(X) = (1-p) X + p (I/d) Tr(X).
            # Weight sqrt(p/d^2) on the same matrix units contracts traceless X by 1-p/d.
            kraus_list: List[np.ndarray] = [np.sqrt(1.0 - p) * np.eye(d, dtype=complex)]
            weight = np.sqrt(p / d)
            for j in range(d):
                for k in range(d):
                    e_jk = np.zeros((d, d), dtype=complex)
                    e_jk[j, k] = 1.0
                    kraus_list.append(weight * e_jk)
            return cls(kraus_operators=kraus_list)

    @classmethod
    def amplitude_damping(cls, gamma: float) -> KrausChannel:
        """
        Qubit amplitude damping channel with decay probability gamma in [0, 1]:
            K0 = [[1, 0], [0, sqrt(1-gamma)]], K1 = [[0, sqrt(gamma)], [0, 0]].
        """
        if not (0.0 <= gamma <= 1.0):
            raise ValueError(f"Gamma must be in [0, 1], got {gamma}")
        k0 = np.array([[1.0, 0.0], [0.0, np.sqrt(1.0 - gamma)]], dtype=complex)
        k1 = np.array([[0.0, np.sqrt(gamma)], [0.0, 0.0]], dtype=complex)
        return cls(kraus_operators=[k0, k1])

    @classmethod
    def phase_damping(cls, lambda_param: float) -> KrausChannel:
        """
        Qubit phase damping (dephasing) channel with lambda_param in [0, 1]:
            K0 = [[1, 0], [0, sqrt(1-lambda)]], K1 = [[0, 0], [0, sqrt(lambda)]].
        """
        if not (0.0 <= lambda_param <= 1.0):
            raise ValueError(f"Lambda must be in [0, 1], got {lambda_param}")
        k0 = np.array([[1.0, 0.0], [0.0, np.sqrt(1.0 - lambda_param)]], dtype=complex)
        k1 = np.array([[0.0, 0.0], [0.0, np.sqrt(lambda_param)]], dtype=complex)
        return cls(kraus_operators=[k0, k1])

    @classmethod
    def non_contractive_perturbation(
        cls, base_channel: KrausChannel, scale: float = 1.2
    ) -> KrausChannel:
        """Scale Kraus operators by sqrt(scale) > 1, creating a trace-increasing, non-contractive map."""
        if scale <= 1.0:
            raise ValueError(
                "Scale must be > 1.0 to produce a non-contractive channel."
            )
        perturbed = [np.sqrt(scale) * k for k in base_channel.kraus_operators]
        return cls(kraus_operators=perturbed)

    @classmethod
    def post_selected(cls, projector: np.ndarray) -> KrausChannel:
        """
        Post-selected quantum measurement E(rho) = P rho P^dag (trace-decreasing).
        """
        p_mat = np.asarray(projector, dtype=complex)
        return cls(kraus_operators=[p_mat])

    def population_shadow(self) -> np.ndarray:
        """
        Compute the column-stochastic population shadow matrix K(gamma' | gamma):
            K_{i, j} = sum_k |(K_k)_{i, j}|^2.
        For any input state rho, the output diagonal is related to the input by:
            p'_i = sum_j K_{i, j} p_j + sum_j sum_{l != j} sum_k (K_k)_{i, j} (K_k*)_{i, l} rho_{j, l}.
        When the input is diagonal (rho = diag(p)), p' = K @ p.
        Because sum_k K_k^dag K_k = I, each column sums to 1: sum_i K_{i, j} = 1.
        (Absorbed from QM_082 / ENC-1127).
        """
        d = self.dimension
        k_mat = np.zeros((d, d), dtype=float)
        for op in self.kraus_operators:
            k_mat += np.abs(op) ** 2
        return k_mat


class CochainMorphism:
    """
    Cochain morphism between quantum cochain complexes:
        Lambda^0: C^0_Q -> C'^0_Q
        Lambda^1: C^1_Q -> C'^1_Q
    satisfying coboundary intertwining: Lambda^1 d0 = d0' Lambda^0.
    """

    def __init__(
        self,
        vertex_channels: List[KrausChannel],
        edge_channels: List[KrausChannel],
    ) -> None:
        self.vertex_channels = list(vertex_channels)
        self.edge_channels = list(edge_channels)
        self.num_vertices = len(self.vertex_channels)
        self.num_edges = len(self.edge_channels)

    @classmethod
    def uniform(
        cls, graph_complex: GraphComplex, channel: KrausChannel
    ) -> CochainMorphism:
        """Construct uniform stalkwise cochain morphism using the same channel on all cells."""
        channel.assert_cptp()
        v_ch = [channel] * graph_complex.num_vertices
        e_ch = [channel] * graph_complex.num_edges
        return cls(vertex_channels=v_ch, edge_channels=e_ch)

    def apply_to_cochain(self, cochain: Cochain) -> Cochain:
        """Apply morphism to cochain of degree 0 or 1."""
        if not cochain.is_operator:
            raise ValueError("CochainMorphism applies to operator cochains.")
        if cochain.degree == 0:
            if cochain.num_cells != self.num_vertices:
                raise DimensionMismatchError(
                    f"Cells {cochain.num_cells} != vertices {self.num_vertices}"
                )
            out_data = np.zeros_like(cochain.data)
            for u in range(self.num_vertices):
                out_data[u] = self.vertex_channels[u].apply(cochain.data[u])
            return Cochain(out_data, degree=0)
        elif cochain.degree == 1:
            if cochain.num_cells != self.num_edges:
                raise DimensionMismatchError(
                    f"Cells {cochain.num_cells} != edges {self.num_edges}"
                )
            out_data = np.zeros_like(cochain.data)
            for e in range(self.num_edges):
                out_data[e] = self.edge_channels[e].apply(cochain.data[e])
            return Cochain(out_data, degree=1)
        else:
            raise NotImplementedError(f"Degree {cochain.degree} not supported.")

    def verify_intertwining(
        self,
        graph_complex: GraphComplex,
        tol: float = 1e-7,
        strict: bool = False,
    ) -> Tuple[bool, float]:
        """
        Verify that Lambda^1 (d0 phi) = d0 (Lambda^0 phi) for all basis elements in C^0_Q.
        Returns (is_intertwined, max_violation_norm).
        If strict=True and condition fails, raises IntertwiningViolationError.
        """
        if (
            graph_complex.num_vertices != self.num_vertices
            or graph_complex.num_edges != self.num_edges
        ):
            raise DimensionMismatchError("Complex dimensions do not match morphism.")

        d = self.vertex_channels[0].dimension
        basis = HermitianOperator.gell_mann_basis(d)
        max_err = 0.0

        # Test on every vertex u and generator a
        for u in range(self.num_vertices):
            for gen in basis:
                phi_arr = np.zeros((self.num_vertices, d, d), dtype=np.complex128)
                phi_arr[u] = gen
                phi_c = Cochain(phi_arr, degree=0)

                # LHS: Lambda^1 (d0 phi)
                d0_phi = graph_complex.d0(phi_c)
                lhs = self.apply_to_cochain(d0_phi)

                # RHS: d0 (Lambda^0 phi)
                lam0_phi = self.apply_to_cochain(phi_c)
                rhs = graph_complex.d0(lam0_phi)

                diff = lhs.data - rhs.data
                err = float(np.max(np.abs(diff)))
                if err > max_err:
                    max_err = err

        is_intertwined = max_err <= tol
        if strict and not is_intertwined:
            raise IntertwiningViolationError(
                f"Intertwining condition Lambda^1 d0 = d0' Lambda^0 violated: max diff {max_err:.2e} > {tol:.2e}"
            )
        return is_intertwined, max_err

    def verify_quotient_monotonicity(
        self,
        solver: QuantumQuotientSolver,
        delta: Cochain,
        tol: float = 1e-4,
    ) -> Tuple[bool, float, float]:
        """
        Evaluate CPTP quotient monotonicity:
            Phi_Q'([Lambda^1 delta]) <= Phi_Q([delta]).
        Returns (is_monotone, phi_before, phi_after).
        """
        cert_before = solver.solve(delta)
        phi_before = cert_before.primal_value

        delta_transformed = self.apply_to_cochain(delta)
        cert_after = solver.solve(delta_transformed)
        phi_after = cert_after.primal_value

        is_monotone = phi_after <= phi_before + tol
        return is_monotone, phi_before, phi_after


def verify_stochastic_l1_contraction(
    kernel: np.ndarray,
    vec: np.ndarray,
    tol: float = 1e-9,
) -> Tuple[bool, float, float]:
    """
    Verify classical l1 contraction for a column-stochastic kernel S:
        ||S x||_1 <= ||x||_1.
    Returns (is_contractive, norm_before, norm_after).
    (Absorbed from QM_082 / ENC-1055).
    """
    k = np.asarray(kernel, dtype=float)
    col_sums = np.sum(k, axis=0)
    if not np.allclose(col_sums, 1.0, atol=tol):
        raise ValueError(f"Kernel is not column-stochastic: column sums = {col_sums}")
    if np.any(k < -tol):
        raise ValueError("Kernel is not column-stochastic: contains negative entries.")

    x = np.asarray(vec, dtype=float)
    sx = k @ x
    norm_before = float(np.sum(np.abs(x)))
    norm_after = float(np.sum(np.abs(sx)))
    return (norm_after <= norm_before + tol), norm_before, norm_after
