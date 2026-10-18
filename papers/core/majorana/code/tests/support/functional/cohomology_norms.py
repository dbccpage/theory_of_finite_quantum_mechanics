import math
import numbers

import numpy as np
from typing import Dict, List

from omega_engine.crates.functional.l1_norm import compute_l1_norm

__all__ = ["compute_l1_norm", "compute_l2_norm", "norm_gap"]


def _check_finite_scalar(v, ctx: str) -> float:
    """Reject non-scalar (vector/complex) and non-finite cochain entries."""
    if isinstance(v, bool) or not isinstance(v, numbers.Real):
        raise TypeError(f"{ctx} expects real scalar values, got {type(v).__name__}")
    fv = float(v)
    if not math.isfinite(fv):
        raise ValueError(f"{ctx} contains a non-finite value")
    return fv


def compute_l2_norm(delta: Dict) -> float:
    """
    Compute the L2 norm of a coboundary.

    Args:
        delta: Dictionary of coboundary values

    Returns:
        L2 norm (Euclidean norm)

    Only real, finite scalar cochain values are accepted; vector-valued or
    complex entries are rejected rather than silently mishandled.
    """
    vals = [_check_finite_scalar(v, "compute_l2_norm") for v in delta.values()]
    return float(np.sqrt(sum(v * v for v in vals)))


def norm_gap(x: List[float]) -> float:
    """
    Compute the dispersion functional D(x) = |x|_1 - |x|_2.

    This measures how distributed a vector is across coordinates.
    Vanishes for sparse vectors, increases with uniformity.
    From Paper 000, Laws of Form.

    Args:
        x: Vector as list of floats

    Returns:
        Norm gap (dispersion measure)
    """
    if not x:
        return 0.0
    vals = [_check_finite_scalar(v, "norm_gap") for v in x]
    l1 = compute_l1_norm(vals)
    l2 = np.sqrt(sum(v * v for v in vals))
    return float(l1 - l2)



