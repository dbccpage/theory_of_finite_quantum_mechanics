"""CochainCarrier to Network representation adapter."""

from __future__ import annotations

from typing import Any

from ..carrier.cochain_carrier import CochainCarrier


def carrier_to_network(carrier: CochainCarrier) -> Any:
    """Adapt a CochainCarrier domain entity into a numerical Network object."""
    try:
        from ..residuals.network_residual import Network
    except ImportError:
        from omega_engine.residuals.network_residual import Network
    return Network(
        nodes=list(carrier.nodes),
        edges=list(carrier.edges),
        faces=list(carrier.faces),
    )
