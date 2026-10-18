"""Cochain residual functionals (Phi1 unweighted L1 mass and Gamma2 coboundary).

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Any, Dict, Tuple

from ..carrier.cochain_carrier import CochainCarrier
from ..state.cochain_state import CochainState
from ..adapter.cochain_network_adapter import carrier_to_network


def evaluate_cochain_residuals(
    carrier: CochainCarrier,
    state: CochainState,
) -> Tuple[float, float, Dict[str, Any]]:
    """Compute (phi1, gamma2, phi_result) for a CochainState."""
    try:
        from ..residuals.network_residual import curl, residual_after_gauge_fix
    except ImportError:
        from omega_engine.residuals.network_residual import curl, residual_after_gauge_fix

    network = carrier_to_network(carrier)
    values = state.as_mapping()
    phi_result = residual_after_gauge_fix(network, values, method="l1")
    phi1 = float(phi_result["residual_size"])
    gamma2 = float(sum(abs(value) for value in curl(network, values).values()))
    return phi1, gamma2, phi_result
