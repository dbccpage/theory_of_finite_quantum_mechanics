"""Replay untrusted finite records against independently selected fixture inputs.

This checker does not call the aggregate producer. It rechecks the native
functional and the full local model. Hashes bind inputs; they do not certify
laboratory coverage or grant authorization.
"""

from __future__ import annotations

from ffi import NativeMeasurementUnavailable, measurement_call
from finite_inputs import local_zero_models, measurement_requests


def verify_finite_records(records) -> list[str]:
    expected = {"separable_correlated", "three_factor", "ising_five_cycle", "commuting_boundary", "rotating_polynomial"}
    if not isinstance(records, dict) or set(records) != expected:
        return ["finite certificate inventory mismatch"]
    errors = []
    measurements = measurement_requests()
    for name, record in records.items():
        if not isinstance(record, dict):
            errors.append(f"{name}: invalid record")
            continue
        if record.get("status") == "refused":
            if set(record) != {"status", "reason"} or not isinstance(record["reason"], str) or not record["reason"]:
                errors.append(f"{name}: invalid capability refusal")
            continue  # No mathematical acceptance is attributed to a refusal.
        if set(record) != {"status", "certificate"} or record.get("status") != "verified":
            errors.append(f"{name}: invalid finite evidence status")
            continue
        try:
            cert = record["certificate"]
            if name in measurements:
                request = measurements[name]
                if cert["request"] != request:
                    raise ValueError("measurement request differs from the independently declared input")
                result = measurement_call("measurement_verify", {
                    "expected_contract": request["contract"], "certificate": cert})
                if result["accepted"] is not True or result["input_digest"] != cert["input_digest"]:
                    raise ValueError("native mathematical replay rejected the certificate")
            else:
                from local_persistent_zero import decode_certificate, verify_local_zero
                if not verify_local_zero(local_zero_models()[name], decode_certificate(cert)):
                    raise ValueError("local basis/boundary/annihilator replay rejected the certificate")
        except (NativeMeasurementUnavailable, ImportError, ValueError, TypeError, KeyError, IndexError, ZeroDivisionError) as exc:
            errors.append(f"{name}: {exc}")
    return errors
