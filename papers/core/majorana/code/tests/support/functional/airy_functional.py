"""Airy critical-equation residual functional.

Computes |lambda * (z^2 - 1)| over all slots.
AuthorityEffect: None.
"""

from __future__ import annotations

import math
from typing import Sequence, Tuple

from ..carrier.airy_carrier import AiryCriticalCarrierV1
from ..state.airy_state import AiryCriticalStateV1


def evaluate_airy_critical_residuals(
    carrier: AiryCriticalCarrierV1,
    state: AiryCriticalStateV1,
) -> Tuple[Tuple[float, ...], float]:
    """Evaluate critical equation residuals for each slot and return (residuals, max_residual)."""
    lam = carrier.lambda_scalar.to_complex()
    residuals = tuple(
        abs(lam * (value * value - 1.0)) for value in state.complex_values()
    )
    maximum = max(residuals) if residuals else 0.0
    if not math.isfinite(maximum):
        raise ValueError("Airy critical residual must be finite")
    return residuals, maximum
