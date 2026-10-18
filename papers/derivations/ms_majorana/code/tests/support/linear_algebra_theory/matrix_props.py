import numpy as np


def is_row_sparse(U: np.ndarray, tol: float = 1e-10) -> bool:
    """Checks if a matrix has at most one non-zero entry per row."""
    for row in U:
        if np.sum(np.abs(row) > tol) > 1:
            return False
    return True


def check_descent_compatibility(
    U: np.ndarray, c: np.ndarray, num_trials: int = 100
) -> bool:
    """Checks if output moduli are independent of input phases."""
    from omega_engine.crates.operator.transforms.quantum_maps import squared_modulus_map

    base_out = squared_modulus_map(U @ c)
    n = len(c)
    for trial in range(num_trials):
        phases = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False) + (
            trial * np.pi / max(1, num_trials)
        )
        c_prime = np.abs(c) * np.exp(1j * phases)
        out = squared_modulus_map(U @ c_prime)
        if not np.allclose(base_out, out):
            return False
    return True



