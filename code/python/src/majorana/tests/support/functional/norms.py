import numpy as np


def lp_norm(x: np.ndarray, p: float) -> float:
    """Computes the Lp 'norm' of x for p > 0.

    For 0 < p < 1 this is a quasi-norm (the triangle inequality / norm-status
    path does not apply); see ``lp_subadditivity`` and ``verify_inequality``,
    which require p >= 1. Empty input yields 0.0 by convention.
    """
    if not (p > 0):
        raise ValueError("p must be > 0")
    x = np.asarray(x, dtype=float)
    if x.size == 0:
        return 0.0
    if not np.all(np.isfinite(x)):
        raise ValueError("x must contain only finite values")
    return float(np.sum(np.abs(x) ** p) ** (1.0 / p))


from omega_engine.crates.functional.l1_norm import l1  

__all__ = ["lp_norm", "l1", "lp_subadditivity", "normalize", "verify_inequality"]


def lp_subadditivity(
    x: np.ndarray, y: np.ndarray, p: float, allow_quasi_norm: bool = False
) -> tuple[float, float]:
    """Proposition 3.1: Nonlinear aggregation for p >= 1.
    Returns (norm(x+y, p), norm(x, p) + norm(y, p)) for disjoint sectors.

    The subadditivity (triangle-inequality) interpretation requires p >= 1.
    Pass ``allow_quasi_norm=True`` to compute the p < 1 quasi-norm values
    anyway (the inequality interpretation no longer holds)."""
    if p < 1 and not allow_quasi_norm:
        raise ValueError(
            "p must be >= 1 for the norm path (set allow_quasi_norm=True for quasi-norms)"
        )
    joint = np.concatenate([x, y])
    norm_joint = lp_norm(joint, p)
    norm_sum = lp_norm(x, p) + lp_norm(y, p)
    return norm_joint, norm_sum


def normalize(psi: np.ndarray) -> np.ndarray:
    """Normalize a state vector to unit L2 norm."""
    psi = np.asarray(psi)
    if not np.all(np.isfinite(psi)):
        raise ValueError("psi must contain only finite values.")
    n = np.linalg.norm(psi)
    if n == 0:
        raise ValueError("Cannot normalize zero vector.")
    return psi / n


def verify_inequality(vector: np.ndarray) -> bool:
    """Evaluates the strict norm inequality linking the microscopic discrete structure to classical phenomenologies:
    ||x||_1 >= ||x||_2 >= ||x||_infty"""
    v1 = np.linalg.norm(vector, 1)
    v2 = np.linalg.norm(vector, 2)
    vinf = np.linalg.norm(vector, np.inf)
    tol = 1e-12
    return bool((v1 >= v2 - tol) and (v2 >= vinf - tol))



