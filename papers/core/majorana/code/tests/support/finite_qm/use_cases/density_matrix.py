# AuthorityEffect: None.
from __future__ import annotations
import numpy as np

def is_valid_density_matrix(rho: np.ndarray, tol: float = 1e-9) -> bool:
    if rho.ndim != 2 or rho.shape[0] != rho.shape[1]:
        return False
    if not bool(np.allclose(rho, rho.conj().T, rtol=0.0, atol=tol)):
        return False
    if not bool(np.isclose(np.trace(rho), 1.0, rtol=0.0, atol=tol)):
        return False
    evals = np.linalg.eigvalsh(rho)
    return bool(np.all(evals >= -tol))

def born_probability(rho: np.ndarray, projection: np.ndarray) -> float:
    return float(np.real(np.trace(projection @ rho)))

def measure_and_update(rho: np.ndarray, projection: np.ndarray) -> tuple[float, np.ndarray]:
    p = born_probability(rho, projection)
    if p <= 0.0:
        return 0.0, np.zeros_like(rho)
    rho_post = (projection @ rho @ projection) / p
    return float(p), rho_post

__all__ = ['born_probability', 'is_valid_density_matrix', 'measure_and_update']
