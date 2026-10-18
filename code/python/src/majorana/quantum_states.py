import numpy as np


def density(psi: np.ndarray) -> np.ndarray:
    """Return the rank-1 outer-product matrix psi psi†.

    This is a utility for experiments that use complex vector states.
    It does not derive a measurement model or Born rule.
    """
    psi = np.asarray(psi, dtype=np.complex128).reshape(-1)
    return np.outer(psi, np.conjugate(psi))

