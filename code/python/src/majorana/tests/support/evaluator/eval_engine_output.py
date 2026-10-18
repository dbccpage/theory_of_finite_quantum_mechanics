"""Structural evaluator for legacy engine-adjacent output envelopes."""

from __future__ import annotations

import hashlib
import json

from omega_engine.crates.type.engine_io import (
    CheckedEngineOutput,
    EngineOutput,
    RefusedEngineOutput,
)


def check_engine_output_hash(
    output: EngineOutput,
) -> CheckedEngineOutput | RefusedEngineOutput:
    """Check the envelope hash without recomputing domain residual geometry."""

    data_bytes = json.dumps(
        {
            "vec": output.residual_vector,
            "status": output.status,
            "task_id": output.task_id,
        },
        sort_keys=True,
    ).encode("utf-8")
    expected_hash = hashlib.sha256(data_bytes).hexdigest()
    if output.output_hash != expected_hash:
        return RefusedEngineOutput(
            output=output,
            refusal_reason=(
                f"Output hash mismatch: expected {expected_hash}, got {output.output_hash}"
            ),
        )

    verification_hash = hashlib.sha256(
        f"verify:{output.output_hash}".encode("utf-8")
    ).hexdigest()
    return CheckedEngineOutput(
        output=output,
        verification_hash=verification_hash,
        authority_effect="FactOnly",
    )


__all__ = ["check_engine_output_hash"]
