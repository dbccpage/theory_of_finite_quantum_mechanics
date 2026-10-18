import numpy as np

from omega_engine.crates.operator.transforms.quantum_maps import squared_modulus_map


def l1_probability(weights: np.ndarray) -> np.ndarray:
    """Normalize nonnegative L1 weights into a probability vector."""
    weights = np.asarray(weights, dtype=float)
    if weights.ndim != 1:
        raise ValueError("weights must be a 1D array.")
    if np.any(weights < 0):
        raise ValueError("weights must be non-negative.")
    total = float(np.sum(weights))
    if total <= 0:
        raise ValueError("total weight must be positive.")
    return weights / total


def born_rule(amplitudes: np.ndarray) -> np.ndarray:
    """Apply a DECLARED squared-modulus map to an amplitude vector.

    This APPLIES the representation rule p_i = |a_i|^2 / sum|a_j|^2; it does
    NOT derive or justify the Born rule. The squared-modulus map is taken as
    given (a representation choice), not proven.
    """
    amplitudes = np.asarray(amplitudes)
    if not np.all(np.isfinite(amplitudes)):
        raise ValueError("amplitudes must contain only finite values.")
    probs = np.asarray(squared_modulus_map(amplitudes), dtype=float)
    if probs.ndim != 1:
        raise ValueError("squared-modulus output must be a 1D vector.")
    if np.any(probs < 0):
        raise ValueError("descent_map returned negative weights.")
    total = np.sum(probs)
    if total <= 0:
        raise ValueError("descent_map returned zero total weight.")
    return probs / total



