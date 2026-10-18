"""ReplayKernel Contract Boundary (replay verification over canonical traces).

Doctrine:
- ReplayKernel verifies causal trace integrity over canonical TraceArtifacts.
- Replay depends on TraceArtifact; TraceArtifact does NOT depend on Replay.
- Emits CheckedTraceRecord carrying FactOnly authority after verification.
"""

from __future__ import annotations
import hashlib
from typing import Final, Union

from omega_engine.crates.type.trace.base.trace_artifact import (
    CheckedTraceRecord,
    RefusedTraceRecord,
    TraceArtifact,
)

CONTRACT_ID: Final[str] = "urn:omega:evidence:replay_kernel:v1.0.0"


class ReplayKernel:
    """Historical trace replay and causal verification kernel."""

    contract_id: Final[str] = CONTRACT_ID
    authority_effect: Final[str] = "FactOnly"

    def __init__(self, kernel_id: str = "replay_kernel_001") -> None:
        self.kernel_id = kernel_id

    def verify_trace(
        self, artifact: TraceArtifact, schema_ref: str = "trace_schema_v1"
    ) -> CheckedTraceRecord | RefusedTraceRecord:
        """Verify artifact hash and causal integrity."""
        expected_hash = artifact.compute_hash()
        if not artifact.artifact_hash or artifact.artifact_hash != expected_hash:
            return RefusedTraceRecord(
                trace_ref=artifact.trace_id,
                schema_ref=schema_ref,
                refusal_reason=f"Artifact hash mismatch: expected {expected_hash}, got {artifact.artifact_hash}",
            )

        causal_raw = f"{artifact.artifact_hash}:{schema_ref}:{artifact.sequence}"
        causal_hash = f"sha256:{hashlib.sha256(causal_raw.encode('utf-8')).hexdigest()}"
        return CheckedTraceRecord(
            trace_ref=artifact.trace_id,
            schema_ref=schema_ref,
            checked_causal_chain_hash=causal_hash,
            authority_effect="FactOnly",
        )


__all__ = [
    "ReplayKernel",
    "CONTRACT_ID",
]
