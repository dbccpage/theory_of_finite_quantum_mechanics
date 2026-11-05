"""
Stalk Gauge Geometries and Invariance Verification.
Paper: GS-002 (so_k_invariant_gauge_classification)
"""

from __future__ import annotations
import math
from typing import Protocol, runtime_checkable, Dict, Any, Optional, List, Tuple
import numpy as np


@runtime_checkable
class StalkGauge(Protocol):
    """Protocol for local stalk gauge functions j: R^k -> [0, inf)."""

    def __call__(self, x: np.ndarray) -> float: ...


def _checked_gauge_value(gauge: StalkGauge, x: np.ndarray) -> float:
    value = gauge(x)
    if not math.isfinite(value) or value < 0:
        raise ValueError("Gauge audit requires finite nonnegative gauge values.")
    return float(value)


class EuclideanGauge:
    """j(x) = c ||x||_2 for isotropic Euclidean metric."""

    def __init__(self, scale: float = 1.0) -> None:
        if not math.isfinite(scale) or scale <= 0:
            raise ValueError(f"Scale must be strictly positive and finite (got {scale}).")
        self.scale = float(scale)

    def __call__(self, x: np.ndarray) -> float:
        x_arr = np.asarray(x, dtype=float)
        if not np.all(np.isfinite(x_arr)):
            raise ValueError("Input x must contain finite real numbers.")
        return float(self.scale * np.linalg.norm(x_arr))


class CoordinateL1Gauge:
    """j(x) = c * sum_j w_j |x_j| for coordinate-aligned L1 gauge."""

    def __init__(
        self,
        scale: float = 1.0,
        weights: Optional[np.ndarray | List[float] | Tuple[float, ...]] = None,
    ) -> None:
        if not math.isfinite(scale) or scale <= 0:
            raise ValueError(f"Scale must be strictly positive and finite (got {scale}).")
        self.scale = float(scale)
        if weights is not None:
            w = np.asarray(weights, dtype=float)
            if w.ndim != 1:
                raise ValueError(f"Weights must be 1-dimensional, got shape {w.shape}.")
            if not np.all(np.isfinite(w)):
                raise ValueError("Weights must contain finite real numbers.")
            if np.any(w <= 0):
                raise ValueError("Weights must be strictly positive.")
            self.weights: Optional[np.ndarray] = w
        else:
            self.weights = None

    def __call__(self, x: np.ndarray) -> float:
        x_arr = np.asarray(x, dtype=float)
        if not np.all(np.isfinite(x_arr)):
            raise ValueError("Input x must contain finite real numbers.")
        if self.weights is None:
            return float(self.scale * np.sum(np.abs(x_arr)))
        if len(self.weights) != len(x_arr):
            raise ValueError(
                f"Weights length ({len(self.weights)}) does not match input length ({len(x_arr)})."
            )
        return float(self.scale * np.sum(self.weights * np.abs(x_arr)))


class LpGauge:
    """j(x) = c ||x||_p."""

    def __init__(self, p: float = 2.0, scale: float = 1.0) -> None:
        if not math.isfinite(p) and not math.isinf(p):
            raise ValueError("p must be a real number or inf.")
        if p < 1.0:
            raise ValueError("p must be >= 1.0 for convex gauge.")
        if not math.isfinite(scale) or scale <= 0:
            raise ValueError(f"Scale must be strictly positive and finite (got {scale}).")
        self.p = float(p)
        self.scale = float(scale)

    def __call__(self, x: np.ndarray) -> float:
        x_arr = np.asarray(x, dtype=float)
        if not np.all(np.isfinite(x_arr)):
            raise ValueError("Input x must contain finite real numbers.")
        if math.isinf(self.p):
            return float(self.scale * np.max(np.abs(x_arr)))
        return float(self.scale * (np.sum(np.abs(x_arr) ** self.p) ** (1.0 / self.p)))


class AnisotropicGauge:
    """j(x) = ||A x||_2 for invertible / full-rank square matrix A."""

    def __init__(self, matrix_a: np.ndarray) -> None:
        self.a = np.asarray(matrix_a, dtype=float)
        if not np.all(np.isfinite(self.a)):
            raise ValueError("Matrix A must contain finite real numbers.")
        if self.a.ndim != 2 or self.a.shape[0] != self.a.shape[1]:
            raise ValueError("Matrix A must be square.")
        # Check full column rank (invertibility)
        eigs = np.linalg.eigvalsh(self.a.T @ self.a)
        if np.any(eigs <= 1e-12):
            raise ValueError("Matrix A must have full column rank.")

    def __call__(self, x: np.ndarray) -> float:
        x_arr = np.asarray(x, dtype=float)
        if not np.all(np.isfinite(x_arr)):
            raise ValueError("Input x must contain finite real numbers.")
        if len(x_arr) != self.a.shape[1]:
            raise ValueError(
                f"Input length {len(x_arr)} does not match matrix dimension {self.a.shape[1]}."
            )
        return float(np.linalg.norm(self.a @ x_arr))


# ---------------------------------------------------------------------------
# Group Action Generators & Invariance Audits
# ---------------------------------------------------------------------------


def make_so2_rotation(theta: float) -> np.ndarray:
    """Return 2x2 rotation matrix in SO(2)."""
    if isinstance(theta, bool) or not isinstance(theta, (int, float, np.number)) or not math.isfinite(float(theta)):
        raise ValueError(f"Angle theta must be a finite real number (got {theta}).")
    c, s = math.cos(float(theta)), math.sin(float(theta))
    return np.array([[c, -s], [s, c]], dtype=float)


def make_random_sok_rotation(
    k: int, rng: Optional[np.random.Generator] = None
) -> np.ndarray:
    """Sample a uniform random matrix in SO(k) via Haar-distributed QR decomposition."""
    if isinstance(k, bool) or not isinstance(k, (int, np.integer)) or k < 1:
        raise ValueError(f"k must be non-boolean integer >= 1 (got {k}).")
    if rng is None:
        rng = np.random.default_rng()
    if k == 1:
        return np.array([[1.0]])
    h = rng.normal(size=(k, k))
    q, r = np.linalg.qr(h)
    d = np.diagonal(r)
    ph = d / np.abs(d)
    q = q * ph
    if np.linalg.det(q) < 0:
        q[:, 0] = -q[:, 0]
    return q


def make_signed_permutation(
    k: int, rng: Optional[np.random.Generator] = None
) -> np.ndarray:
    """Sample an element of the hyperoctahedral group B_k."""
    if isinstance(k, bool) or not isinstance(k, (int, np.integer)) or k < 1:
        raise ValueError(f"k must be non-boolean integer >= 1 (got {k}).")
    if rng is None:
        rng = np.random.default_rng()
    p = rng.permutation(k)
    s = rng.choice([-1.0, 1.0], size=k)
    mat = np.zeros((k, k), dtype=float)
    for i in range(k):
        mat[p[i], i] = s[i]
    return mat


def audit_so_k_invariance(
    gauge: StalkGauge,
    dim: int,
    num_samples: int = 100,
    tol: float = 1e-6,
    rng: Optional[np.random.Generator] = None,
) -> Dict[str, Any]:
    """
    Probe SO(k) invariance on a finite random sample.
    Passing does not establish invariance for all rotations and vectors.
    """
    if isinstance(num_samples, bool) or not isinstance(num_samples, (int, np.integer)) or num_samples <= 0:
        raise ValueError(f"num_samples must be integer >= 1 (got {num_samples}).")
    if isinstance(dim, bool) or not isinstance(dim, (int, np.integer)) or dim < 1:
        raise ValueError(f"dim must be integer >= 1 (got {dim}).")
    if isinstance(tol, bool) or not isinstance(tol, (int, float, np.number)) or not math.isfinite(float(tol)) or float(tol) < 0:
        raise ValueError(f"tolerance must be nonnegative and finite (got {tol}).")

    if rng is None:
        rng = np.random.default_rng(42)

    max_deviation = 0.0
    samples_tested = 0
    for _ in range(num_samples):
        # Sample non-zero vector x
        x = rng.normal(size=dim)
        if np.linalg.norm(x) < 1e-8:
            continue
        r = make_random_sok_rotation(dim, rng=rng)
        rx = r @ x
        val_orig = _checked_gauge_value(gauge, x)
        val_rot = _checked_gauge_value(gauge, rx)
        samples_tested += 1
        dev = abs(val_orig - val_rot)
        if dev > max_deviation:
            max_deviation = dev

    if samples_tested == 0:
        raise ValueError("No valid rotation samples could be generated.")
    is_invariant = max_deviation <= tol
    return {
        "dim": dim,
        "is_so_k_invariant": is_invariant,
        "max_deviation": max_deviation,
        "tolerance": tol,
        "samples_tested": samples_tested,
    }


def audit_sphere_constancy(
    gauge: StalkGauge,
    dim: int,
    radius: float = 1.0,
    num_samples: int = 100,
    tol: float = 1e-6,
    rng: Optional[np.random.Generator] = None,
) -> Dict[str, Any]:
    """
    Audit whether j(x) is constant on the sphere ||x||_2 = radius.
    """
    if isinstance(num_samples, bool) or not isinstance(num_samples, (int, np.integer)) or num_samples <= 0:
        raise ValueError(f"num_samples must be integer >= 1 (got {num_samples}).")
    if isinstance(dim, bool) or not isinstance(dim, (int, np.integer)) or dim < 1:
        raise ValueError(f"dim must be integer >= 1 (got {dim}).")
    if isinstance(radius, bool) or not isinstance(radius, (int, float, np.number)) or not math.isfinite(float(radius)) or float(radius) <= 0:
        raise ValueError(f"radius must be strictly positive and finite (got {radius}).")
    if isinstance(tol, bool) or not isinstance(tol, (int, float, np.number)) or not math.isfinite(float(tol)) or float(tol) < 0:
        raise ValueError(f"tolerance must be nonnegative and finite (got {tol}).")

    if rng is None:
        rng = np.random.default_rng(42)

    values = []
    for _ in range(num_samples):
        u = rng.normal(size=dim)
        norm_u = np.linalg.norm(u)
        if norm_u < 1e-8:
            continue
        x = (radius / norm_u) * u
        values.append(_checked_gauge_value(gauge, x))

    if not values:
        raise ValueError("No valid sphere samples could be generated.")

    vals = np.array(values)
    spread = float(np.max(vals) - np.min(vals))
    mean_val = float(np.mean(vals))
    is_constant = spread <= tol

    return {
        "dim": dim,
        "radius": radius,
        "is_sphere_constant": is_constant,
        "is_constant_on_sphere": is_constant,
        "mean_value": mean_val,
        "spread": spread,
        "tolerance": tol,
        "samples_tested": len(values),
    }
