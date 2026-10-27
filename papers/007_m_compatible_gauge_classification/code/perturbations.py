"""Invasive injection and break-and-recover mechanics for GS-001.

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Callable, Sequence, Tuple, Dict
import numpy as np

Gauge = Callable[[np.ndarray], float]


# ============================================================================
# 1. INVASIVE FAULT INJECTIONS
# ============================================================================


def inject_non_contractive_operator(
    T: np.ndarray, dilation_factor: float = 1.5
) -> np.ndarray:
    """Dilate an operator by factor > 1 to inject non-contractive behaviour."""
    if dilation_factor <= 1.0:
        raise ValueError(f"dilation_factor must be > 1.0, got {dilation_factor}")
    return np.asarray(T, dtype=float) * dilation_factor


def inject_anisotropic_shear(dimension: int, shear: float = 0.5) -> np.ndarray:
    """Inject anisotropic shear breaking orthogonal / reflection symmetry."""
    if dimension < 2:
        raise ValueError("Dimension must be at least 2")
    m = np.eye(dimension)
    m[0, 1] = shear
    return m


def inject_negative_edge_weights(
    weights: Sequence[float], corrupted_idx: int = 0, corrupted_val: float = -2.0
) -> list[float]:
    """Inject invalid non-positive edge weight into a weight vector."""
    w = list(weights)
    if corrupted_idx < 0 or corrupted_idx >= len(w):
        raise IndexError(f"Index {corrupted_idx} out of range for length {len(w)}")
    if corrupted_val > 0:
        raise ValueError("Corrupted value must be <= 0 to test failure")
    w[corrupted_idx] = corrupted_val
    return w


def inject_nan_edge_weights(
    weights: Sequence[float], corrupted_idx: int = 0
) -> list[float]:
    """Inject NaN edge weight into a weight vector (FI-007-1)."""
    w = list(weights)
    if corrupted_idx < 0 or corrupted_idx >= len(w):
        raise IndexError(f"Index {corrupted_idx} out of range for length {len(w)}")
    w[corrupted_idx] = float("nan")
    return w


def inject_inf_edge_weights(
    weights: Sequence[float], corrupted_idx: int = 0, inf_val: float = float("inf")
) -> list[float]:
    """Inject infinite edge weight into a weight vector (FI-007-1)."""
    w = list(weights)
    if corrupted_idx < 0 or corrupted_idx >= len(w):
        raise IndexError(f"Index {corrupted_idx} out of range for length {len(w)}")
    if not np.isinf(inf_val):
        raise ValueError("inf_val must be infinite")
    w[corrupted_idx] = inf_val
    return w


def inject_presheaf_restriction_defect(
    restrictions: Dict[Tuple[int, int], np.ndarray],
    edge: Tuple[int, int],
    noise_scale: float = 0.5,
    seed: int = 42,
) -> Dict[Tuple[int, int], np.ndarray]:
    """Perturb a restriction map R_{uv} to break presheaf path coherence (FI-007-5)."""
    if edge not in restrictions:
        raise KeyError(f"Edge {edge} not in restrictions dictionary")
    perturbed = dict(restrictions)
    r = np.asarray(restrictions[edge], dtype=float)
    rng = np.random.default_rng(seed)
    noise = rng.normal(size=r.shape)
    perturbed[edge] = r + noise_scale * noise
    return perturbed


def inject_non_hermitian_noise(
    X: np.ndarray, noise_scale: float = 0.2, seed: int = 42
) -> np.ndarray:
    """Inject skew-Hermitian perturbation breaking Hermitian symmetry: X_bad = X + i * noise."""
    arr = np.asarray(X, dtype=complex)
    n = arr.shape[0]
    rng = np.random.default_rng(seed)
    # Generate skew-Hermitian noise: S = A - A^\dagger
    a = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    skew = (a - a.conj().T) / 2.0
    return arr + noise_scale * skew


def inject_trace_leakage(X: np.ndarray, leak: float = 0.5) -> np.ndarray:
    """Inject non-zero trace into an H_n^0 trace-zero matrix."""
    arr = np.asarray(X, dtype=complex)
    n = arr.shape[0]
    return arr + (leak / n) * np.eye(n, dtype=complex)


def inject_cptp_dilation(
    kraus_ops: Sequence[np.ndarray], factor: float = 1.3
) -> list[np.ndarray]:
    """Dilate Kraus operators so sum K_i^dagger K_i != I (violates trace preservation)."""
    return [np.asarray(k, dtype=complex) * np.sqrt(factor) for k in kraus_ops]


# ============================================================================
# 2. BREAK DIAGNOSTICS & AUDITING
# ============================================================================


def audit_gauge_compatibility_violation(
    gauge: Gauge, T: np.ndarray, x: np.ndarray, op_norm: float
) -> Tuple[bool, float]:
    """Evaluate whether j(T x) <= ||T|| j(x).

    Returns (is_compliant, excess_violation).
    """
    j_x = gauge(x)
    j_tx = gauge(T @ x)
    allowed = op_norm * j_x
    excess = max(0.0, j_tx - allowed)
    return (excess <= 1e-9, excess)


def audit_cptp_trace_preservation(
    kraus_ops: Sequence[np.ndarray], atol: float = 1e-8
) -> Tuple[bool, float]:
    """Verify sum K_i^dagger K_i = I. Returns (is_trace_preserving, max_entry_deviation)."""
    if not kraus_ops:
        return False, 1.0
    n = kraus_ops[0].shape[0]
    total = np.zeros((n, n), dtype=complex)
    for k in kraus_ops:
        arr = np.asarray(k, dtype=complex)
        total += arr.conj().T @ arr
    diff = total - np.eye(n, dtype=complex)
    max_dev = float(np.max(np.abs(diff)))
    return (max_dev <= atol, max_dev)


# ============================================================================
# 3. RECOVERY & SANITIZATION MECHANISMS
# ============================================================================


def recover_hermitian_trace_zero(X: np.ndarray) -> np.ndarray:
    """Project corrupted matrix back onto H_n^0 (Hermitian, trace-zero).

    X_rec = (X + X^dagger)/2 - (Tr(X + X^dagger)/(2n)) * I
    """
    arr = np.asarray(X, dtype=complex)
    n = arr.shape[0]
    herm = (arr + arr.conj().T) / 2.0
    tr = np.trace(herm)
    return herm - (tr / n) * np.eye(n, dtype=complex)


def recover_positive_weights(
    weights: Sequence[float], default_weight: float = 1.0
) -> list[float]:
    """Sanitize and recover corrupted edge weights by rectifying <= 0, NaN, or Inf entries."""
    if np.isnan(default_weight) or np.isinf(default_weight) or default_weight <= 0:
        raise ValueError("default_weight must be positive and finite")
    recovered = []
    for w in weights:
        try:
            w_flt = float(w)
            if np.isnan(w_flt) or np.isinf(w_flt) or w_flt <= 0:
                recovered.append(default_weight)
            else:
                recovered.append(w_flt)
        except (ValueError, TypeError):
            recovered.append(default_weight)
    return recovered


def recover_cptp_trace_preservation(
    kraus_ops: Sequence[np.ndarray],
) -> list[np.ndarray]:
    """Normalize Kraus operators so sum K_i^dagger K_i = I via inverse square root."""
    if not kraus_ops:
        raise ValueError("kraus_ops cannot be empty")
    n = kraus_ops[0].shape[0]
    total = np.zeros((n, n), dtype=complex)
    for k in kraus_ops:
        arr = np.asarray(k, dtype=complex)
        total += arr.conj().T @ arr

    # Compute S^{-1/2}
    evals, evecs = np.linalg.eigh(total)
    evals_inv_sqrt = np.where(evals > 1e-12, 1.0 / np.sqrt(evals), 0.0)
    s_inv_sqrt = evecs @ np.diag(evals_inv_sqrt) @ evecs.conj().T

    # Corrected Kraus operators: K'_i = K_i @ S^{-1/2}
    return [k @ s_inv_sqrt for k in kraus_ops]
