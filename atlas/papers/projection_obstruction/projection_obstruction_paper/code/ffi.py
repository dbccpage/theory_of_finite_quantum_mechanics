"""Measurement transport through the repository's canonical Rust host adapter.

No Python fallback evaluates Phi or the product-distance functional. A standalone
deposit without the native host retains an explicit capability refusal.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


class NativeMeasurementUnavailable(RuntimeError):
    pass


def measurement_call(action: str, payload: dict) -> dict:
    if os.environ.get("PO000_NATIVE_INTEGRATION") != "1":
        raise NativeMeasurementUnavailable("NATIVE_INTEGRATION_NOT_REQUESTED")
    for parent in Path(__file__).resolve().parents:
        if (parent / "omega_engine_operating_system" / "adapters" / "rust_host" / "ffi.py").is_file():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            break
    try:
        from omega_engine_operating_system.adapters.rust_host.ffi import RustSymbolGameHost
        from omega_engine_operations.domain.rop.result import Err
    except ImportError as exc:
        raise NativeMeasurementUnavailable("NATIVE_ADAPTER_UNAVAILABLE") from exc
    response = RustSymbolGameHost().invoke_runtime(action, payload)
    if isinstance(response, Err):
        raise NativeMeasurementUnavailable(response.error.code)
    outcome = response.value
    if outcome["success"] is not True:
        raise NativeMeasurementUnavailable(str(outcome["error"]))
    result = outcome["result"]
    if not isinstance(result, dict) or result.get("authority_effect") != "None":
        raise ValueError("invalid measurement outcome or authority ceiling")
    return result
