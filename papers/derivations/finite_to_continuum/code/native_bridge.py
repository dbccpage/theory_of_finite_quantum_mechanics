"""Finite Track 2 requests through the canonical Rust host, preserving its envelope.

Native refusal is a completed dispatch outcome with success=False. Transport errors
are Err(Refusal). Mathematical kernels never fall back to Python implementations.
"""

from collections.abc import Mapping
from typing import Any

from omega_engine_operations.domain.rop.result import Refusal, Result
from omega_engine_operating_system.adapters.rust_host.ffi import RustSymbolGameHost


def evaluate_finite_bridge(
    request: Any, *, host: RustSymbolGameHost | None = None
) -> Result[Mapping[str, Any], Refusal]:
    """Return input-bound, non-authoritative finite evidence or a typed refusal."""
    return (host or RustSymbolGameHost()).invoke_runtime("continuum_evaluate", request)
