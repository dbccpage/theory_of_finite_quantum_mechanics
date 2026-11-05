"""Finite polytope and Minkowski functional duality correspondence for GS-001.

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Callable, Sequence, Dict
import numpy as np

Gauge = Callable[[np.ndarray], float]
MembershipPredicate = Callable[[np.ndarray], bool]


def minkowski_functional(
    x: np.ndarray, is_in_body: MembershipPredicate, tol: float = 1e-7
) -> float:
    """Minkowski functional j_B(x) = inf { lambda > 0 : x in lambda B } for a convex body B.

    Uses bisection search over scale parameter lambda.
    """
    v = np.asarray(x, dtype=float).ravel()
    if np.allclose(v, 0.0):
        return 0.0

    # Binary search bounds
    low = 0.0
    high = 1.0

    # Expand high bound until high * B contains x
    while not is_in_body(v / high):
        high *= 2.0
        if high > 1e12:
            raise ValueError("Vector x outside scaling horizon of convex body B")

    for _ in range(60):
        mid = (low + high) / 2.0
        if is_in_body(v / mid):
            high = mid
        else:
            low = mid
        if (high - low) < min(tol, 1e-12):
            break

    return float(high)


def unit_ball_scaling(c: float, dimension: int) -> dict[str, str | float]:
    """Correct unit ball scaling relation for j(x) = c ||x||_2.

    The unit ball B_j = { x : j(x) <= 1 } is c^{-1} B_2^k, NOT c B_2^k!
    """
    if c <= 0:
        raise ValueError("Gauge scaling factor c must be strictly positive")
    return {
        "scaling_factor": c,
        "dimension": dimension,
        "radius_of_unit_ball": 1.0 / c,
        "volume_scaling_factor": (1.0 / c) ** dimension,
        "formula": f"B_j = (1/{c}) * B_2^{dimension}",
    }


def polytope_unit_ball_membership(x: np.ndarray, gauge: Gauge) -> bool:
    """Predicate indicating whether x is in unit ball B_j = { x : j(x) <= 1 }."""
    return bool(gauge(x) <= 1.0 + 1e-12)


def probe_minkowski_boundary_continuity(
    gauge: Gauge,
    boundary_vector: np.ndarray,
    epsilons: Sequence[float] = (1e-8, 1e-6, 1e-4),
    tol: float = 1e-6,
) -> Dict[str, float | bool]:
    r"""Invasive boundary probe (FI-007-4): evaluate continuity of Minkowski functional near boundary.

    Probes x_in = (1 - eps) * x and x_out = (1 + eps) * x for x in \partial K (where gauge(x) = 1.0).
    Asserts continuity:
      |j(x_in) - (1 - eps)| < tol
      |j(x_out) - (1 + eps)| < tol
      |j(x_out) - j(x_in) - 2*eps| < tol
    """
    x0 = np.asarray(boundary_vector, dtype=float)
    base_val = gauge(x0)
    if not np.isclose(base_val, 1.0, atol=1e-5):
        # Normalize to boundary
        x0 = x0 / base_val

    is_in_body = lambda v: polytope_unit_ball_membership(v, gauge)
    j_base = minkowski_functional(x0, is_in_body, tol=tol)

    results: Dict[str, float | bool] = {
        "base_val": float(j_base),
        "continuous": True,
    }

    for eps in epsilons:
        x_in = (1.0 - eps) * x0
        x_out = (1.0 + eps) * x0

        j_in = minkowski_functional(x_in, is_in_body, tol=tol)
        j_out = minkowski_functional(x_out, is_in_body, tol=tol)

        dev_in = abs(j_in - (1.0 - eps))
        dev_out = abs(j_out - (1.0 + eps))
        dev_gap = abs((j_out - j_in) - 2.0 * eps)

        results[f"dev_in_{eps}"] = float(dev_in)
        results[f"dev_out_{eps}"] = float(dev_out)
        results[f"dev_gap_{eps}"] = float(dev_gap)

        threshold = tol
        if dev_in > threshold or dev_out > threshold or dev_gap > threshold:
            results["continuous"] = False

    return results
