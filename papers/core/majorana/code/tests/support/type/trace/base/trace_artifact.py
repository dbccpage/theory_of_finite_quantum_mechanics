"""Canonical TraceArtifact and Evidence Records.

Doctrine:
- TraceArtifact is the canonical immutable causal event constructed ONLY by TraceAssembler.
- source_ref identifies the originating domain component (e.g. Operator, Engine).
- recorder_ref identifies the assembling Trace Coordinator / TraceAssembler.
- Does NOT depend on ReplayKernel (Replay depends on Trace, not vice versa).
- AuthorityEffect: EvidenceOnly.
"""

from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, Final, List, Tuple

CONTRACT_ID: Final[str] = "urn:omega:evidence:trace_artifact:v1.0.0"
SCHEMA_VERSION: Final[str] = "omega.contract.v1"


@dataclass(frozen=True, slots=True)
class TraceArtifact:
    """Canonical immutable causal event record assembled by TraceAssembler."""

    trace_id: str
    run_id: str
    sequence: int
    source_ref: str
    recorder_ref: str
    event_kind: str
    input_boundary_refs: Tuple[str, ...] = ()
    output_boundary_refs: Tuple[str, ...] = ()
    parent_trace_refs: Tuple[str, ...] = ()
    payload: Dict[str, Any] = field(default_factory=dict)
    artifact_hash: str = ""
    authority_effect: str = "EvidenceOnly"

    def compute_hash(self) -> str:
        payload_data = {
            "trace_id": self.trace_id,
            "run_id": self.run_id,
            "sequence": self.sequence,
            "source_ref": self.source_ref,
            "recorder_ref": self.recorder_ref,
            "event_kind": self.event_kind,
            "input_boundary_refs": list(self.input_boundary_refs),
            "output_boundary_refs": list(self.output_boundary_refs),
            "parent_trace_refs": list(self.parent_trace_refs),
            "payload": self.payload,
            "authority_effect": self.authority_effect,
        }
        raw_bytes = json.dumps(payload_data, sort_keys=True).encode("utf-8")
        return f"sha256:{hashlib.sha256(raw_bytes).hexdigest()}"


@dataclass(frozen=True, slots=True)
class TraceBundle:
    """Canonical ordered collection of TraceArtifacts for a single run."""

    run_id: str
    artifacts: Tuple[TraceArtifact, ...] = ()
    bundle_hash: str = ""

    def compute_hash(self) -> str:
        hashes = [a.artifact_hash or a.compute_hash() for a in self.artifacts]
        raw_bytes = json.dumps({"run_id": self.run_id, "artifact_hashes": hashes}, sort_keys=True).encode("utf-8")
        return f"sha256:{hashlib.sha256(raw_bytes).hexdigest()}"


@dataclass(frozen=True, slots=True)
class CheckedTraceRecord:
    """Verified causal trace record carrying FactOnly authority after replay check."""

    trace_ref: str
    schema_ref: str
    checked_causal_chain_hash: str
    authority_effect: str = "FactOnly"


@dataclass(frozen=True, slots=True)
class RefusedTraceRecord:
    """Refused trace record envelope carrying Refused authority."""

    trace_ref: str
    schema_ref: str
    refusal_reason: str
    authority_effect: str = "Refused"


__all__ = [
    "TraceArtifact",
    "TraceBundle",
    "CheckedTraceRecord",
    "RefusedTraceRecord",
    "CONTRACT_ID",
    "SCHEMA_VERSION",
]
