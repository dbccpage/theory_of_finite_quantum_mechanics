"""Finite evidence beside, never in place of, the general theorem dispositions."""

from __future__ import annotations

from ffi import NativeMeasurementUnavailable, measurement_call
from finite_inputs import local_zero_models, measurement_requests


def build_finite_certificates() -> dict:
    records = {}
    for name, request in measurement_requests().items():
        try:
            cert = measurement_call("measurement_evaluate", request)
            if cert["request"] != request:
                raise ValueError("native certificate is not bound to the submitted request")
            records[name] = {"status": "verified", "certificate": cert}
        except NativeMeasurementUnavailable as exc:
            records[name] = {"status": "refused", "reason": str(exc)}
    try:
        from local_persistent_zero import encode_certificate, propose_local_zero
        for name, model in local_zero_models().items():
            records[name] = {"status": "verified", "certificate": encode_certificate(propose_local_zero(model))}
    except ImportError:
        for name in ("commuting_boundary", "rotating_polynomial"):
            records[name] = {"status": "refused", "reason": "SYMPY_UNAVAILABLE"}
    return records
