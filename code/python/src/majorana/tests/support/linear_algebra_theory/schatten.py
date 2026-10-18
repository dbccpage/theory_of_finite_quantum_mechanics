import numpy as np
import scipy.linalg as la
from typing import Dict, List, Tuple


class SchattenExtension:
    """S3: Theorem 3.1 -- Operator-valued l1 classification."""

    @staticmethod
    def schatten_1_norm(A: np.ndarray) -> float:
        """||A||_1 = Tr|A| = sum of singular values."""
        return float(np.sum(la.svd(A, compute_uv=False)))

    @staticmethod
    def trace_distance(rho: np.ndarray, sigma: np.ndarray) -> float:
        """T(rho, sigma) = 1/2 ||rho - sigma||_1."""
        return 0.5 * SchattenExtension.schatten_1_norm(rho - sigma)

    @staticmethod
    def validate_density_matrix(rho: np.ndarray, label: str = "") -> None:
        """Verify Hermitian, trace-1, PSD."""
        assert np.allclose(rho, rho.conj().T), f"{label} not Hermitian"
        assert abs(np.trace(rho).real - 1.0) < 1e-10, f"{label} trace != 1"
        eigs = np.linalg.eigvalsh(rho)
        assert np.all(eigs >= -1e-10), f"{label} not PSD"

    @staticmethod
    def coboundary_defect(
        states: Dict[str, np.ndarray],
        edges: List[Tuple[str, str]],
    ) -> float:
        """
        I(s) = sum_e ||rho_b - rho_a||_1 (Schatten-1 coboundary norm).

        For identity restriction maps: delta_e = rho_b - rho_a.
        """
        return sum(
            SchattenExtension.schatten_1_norm(states[b] - states[a]) for a, b in edges
        )

    @staticmethod
    def verify_axiom_p1_additivity(
        states: Dict[str, np.ndarray],
        edges: List[Tuple[str, str]],
    ) -> Dict:
        """P1: Edge-wise additivity: I(s) = sum_e nu_e(delta_e)."""
        per_edge = [
            SchattenExtension.schatten_1_norm(states[b] - states[a]) for a, b in edges
        ]
        total = SchattenExtension.coboundary_defect(states, edges)
        return {
            "per_edge": per_edge,
            "total": total,
            "additive": abs(total - sum(per_edge)) < 1e-10,
        }

    @staticmethod
    def verify_axiom_p3_functoriality(A: np.ndarray, phi_op: np.ndarray) -> Dict:
        """P3: nu(Phi(delta)) <= ||Phi||_op * nu(delta)."""
        phi_A = phi_op @ A @ phi_op.conj().T
        nu_A = SchattenExtension.schatten_1_norm(A)
        nu_phi_A = SchattenExtension.schatten_1_norm(phi_A)
        phi_norm = float(np.linalg.norm(phi_op, ord=2))
        return {
            "nu_A": nu_A,
            "nu_phi_A": nu_phi_A,
            "phi_op_norm": phi_norm,
            "functorial": nu_phi_A <= phi_norm**2 * nu_A + 1e-10,
        }

