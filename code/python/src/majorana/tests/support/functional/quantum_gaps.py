import numpy as np

from omega_engine.crates.functional.norms import l1
from omega_engine.crates.operator.transforms.quantum_maps import squared_modulus_map


def _check_matrix_vector(U_A, U_B, psi):
    U_A = np.asarray(U_A)
    U_B = np.asarray(U_B)
    psi = np.asarray(psi)
    if U_A.ndim != 2 or U_A.shape[0] != U_A.shape[1]:
        raise ValueError("U_A must be a square 2D matrix")
    if U_B.shape != U_A.shape:
        raise ValueError("U_A and U_B must have the same shape")
    if psi.ndim != 1 or psi.shape[0] != U_A.shape[1]:
        raise ValueError("psi must be a 1D vector matching the operator dimension")
    for name, arr in (("U_A", U_A), ("U_B", U_B), ("psi", psi)):
        if not np.all(np.isfinite(arr)):
            raise ValueError(f"{name} must contain only finite values")
    return U_A, U_B, psi


def commutator_gap(U_A: np.ndarray, U_B: np.ndarray, psi: np.ndarray) -> tuple:
    """K(A,B;psi) = || |U_B U_A psi|^2 - |U_A U_B psi|^2 ||_1.

    Representation-dependent diagnostic gap (depends on the chosen operator
    representation), NOT a quantum-authority result.
    """
    U_A, U_B, psi = _check_matrix_vector(U_A, U_B, psi)
    psi_ab = U_B @ (U_A @ psi)
    psi_ba = U_A @ (U_B @ psi)
    p_ab = squared_modulus_map(psi_ab)
    p_ba = squared_modulus_map(psi_ba)
    K = l1(p_ab - p_ba)
    return K, p_ab, p_ba


def commutator_gap_density(U_A: np.ndarray, U_B: np.ndarray, rho: np.ndarray) -> float:
    """K(A,B;rho) = || diag(U_B U_A rho U_A† U_B†) - diag(U_A U_B rho U_B† U_A†) ||_1

    Representation-dependent diagnostic gap, NOT a quantum-authority result.
    """
    U_A = np.asarray(U_A)
    U_B = np.asarray(U_B)
    rho = np.asarray(rho)
    if U_A.ndim != 2 or U_A.shape[0] != U_A.shape[1]:
        raise ValueError("U_A must be a square 2D matrix")
    if U_B.shape != U_A.shape:
        raise ValueError("U_A and U_B must have the same shape")
    if rho.shape != U_A.shape:
        raise ValueError("rho must match the operator shape")
    for name, arr in (("U_A", U_A), ("U_B", U_B), ("rho", rho)):
        if not np.all(np.isfinite(arr)):
            raise ValueError(f"{name} must contain only finite values")
    rho_AB = U_B @ U_A @ rho @ U_A.conj().T @ U_B.conj().T
    rho_BA = U_A @ U_B @ rho @ U_B.conj().T @ U_A.conj().T
    p_AB = np.diag(rho_AB).real
    p_BA = np.diag(rho_BA).real
    return l1(p_AB - p_BA)


class TransportAmplitude:
    @staticmethod
    def expected_edge_contribution(n_samples: int = 100000) -> float:
        theta = np.linspace(0, 2 * np.pi, n_samples)
        dt = 2 * np.pi / n_samples
        integrand = np.maximum(0, np.cos(theta))
        return np.sum(integrand) * dt / (2 * np.pi)

    @staticmethod
    def expected_cycle_amplitude() -> float:
        return 3.0 / np.pi

    @staticmethod
    def spectral_amplitude(transport_operator: np.ndarray) -> float:
        evals, _ = np.linalg.eig(transport_operator)
        return float(np.sum(np.abs(evals)))

    @staticmethod
    def get_physical_transport_operator(n: int = 3) -> np.ndarray:
        from omega_engine.crates.linear_algebra_theory.transport import MinimalCyclicTransport

        S = MinimalCyclicTransport(n).shift_operator()
        return S / np.pi



