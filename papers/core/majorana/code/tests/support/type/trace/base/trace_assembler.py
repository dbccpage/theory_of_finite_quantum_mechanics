"""TraceAssembler Contract Boundary (sole TraceSignal -> TraceArtifact boundary).

Doctrine:
- Sole boundary allowed to construct TraceArtifacts from TraceSignals.
- Owned by the Runtime-hosted Trace Coordinator.
- Validates signal schema, binds run_id, assigns trace_id, assigns monotonic sequence, binds parent refs.
- Sets source_ref (component) and recorder_ref (TraceAssembler identity).
- CANNOT interpret domain semantics, compute Phi, certify, authorize, or mutate state.
"""

from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass
from typing import Final, Tuple

from omega_engine.crates.type.trace.base.trace_artifact import TraceArtifact
from omega_engine.crates.type.trace.base.trace_signal import TraceSignal

CONTRACT_ID: Final[str] = "urn:omega:evidence:trace_assembler:v1.0.0"


class TraceAssembler:
    """Sole boundary converting ephemeral TraceSignals into canonical TraceArtifacts."""

    contract_id: Final[str] = CONTRACT_ID
    authority_effect: Final[str] = "EvidenceOnly"

    def __init__(self, assembler_id: str = "trace_assembler_001") -> None:
        self.assembler_id = assembler_id
        self._sequence_counter: int = 0

    def fuse(
        self,
        signal: TraceSignal,
        run_id: str,
        parent_trace_refs: Tuple[str, ...] = (),
    ) -> TraceArtifact:
        """Fuse a TraceSignal into a canonical TraceArtifact."""
        if not signal.source_ref or not signal.event_kind:
            raise ValueError("TraceSignal must have non-empty source_ref and event_kind")

        self._sequence_counter += 1
        seq = self._sequence_counter

        trace_raw = json.dumps(
            {
                "run_id": run_id,
                "sequence": seq,
                "source_ref": signal.source_ref,
                "event_kind": signal.event_kind,
                "correlation_ref": signal.correlation_ref,
            },
            sort_keys=True,
        )
        trace_id = f"trc_{hashlib.sha256(trace_raw.encode('utf-8')).hexdigest()[:16]}"

        unhashed = TraceArtifact(
            trace_id=trace_id,
            run_id=run_id,
            sequence=seq,
            source_ref=signal.source_ref,
            recorder_ref=self.assembler_id,
            event_kind=signal.event_kind,
            input_boundary_refs=signal.input_boundary_refs,
            output_boundary_refs=signal.output_boundary_refs,
            parent_trace_refs=parent_trace_refs,
            payload=dict(signal.payload),
            authority_effect="EvidenceOnly",
        )

        artifact_hash = unhashed.compute_hash()

        return TraceArtifact(
            trace_id=trace_id,
            run_id=run_id,
            sequence=seq,
            source_ref=signal.source_ref,
            recorder_ref=self.assembler_id,
            event_kind=signal.event_kind,
            input_boundary_refs=signal.input_boundary_refs,
            output_boundary_refs=signal.output_boundary_refs,
            parent_trace_refs=parent_trace_refs,
            payload=dict(signal.payload),
            artifact_hash=artifact_hash,
            authority_effect="EvidenceOnly",
        )


__all__ = [
    "TraceAssembler",
    "CONTRACT_ID",
]
