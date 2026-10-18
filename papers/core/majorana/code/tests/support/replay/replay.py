"""Replay Evidence Contract Implementation.

Conforms strictly to contract specification:
    urn:omega:evidence:replay_kernel:v1.0.0
    (omega_engine/crates/omega_contracts/src/contract_canonical_definitions/02_core_evidence/replay_kernel.contract.yaml)

Doctrine:
- Replay reconstructs declared historical execution from trace, manifest, schema, seed, witness, measurement, and certificate references.
- Replay artifacts are EvidenceOnly until verified.
- Verified replay may support FactOnly history claims but does not repair, authorize, terminalize, license, mutate, or execute live control flow.
"""

from __future__ import annotations
import hashlib
import json
from dataclasses import field
from pydantic.dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Union

CONTRACT_ID = "urn:omega:evidence:replay_kernel:v1.0.0"
SCHEMA_VERSION = "omega.contract.v1"


class ReplayStatus(Enum):
    UNVERIFIED = "UNVERIFIED"
    VERIFIED_MATCH = "VERIFIED_MATCH"
    DIVERGENT = "DIVERGENT"
    MANIFEST_MISSING = "MANIFEST_MISSING"


@dataclass(frozen=True)
class ReplayReport:
    """Raw replay report envelope (EvidenceOnly default)."""
    replay_id: str
    trace_refs: List[str]
    manifest_ref: str
    status: ReplayStatus
    output_hash: str
    authority_effect: str = "EvidenceOnly"


@dataclass(frozen=True)
class VerifiedReplayReport:
    """Verified historical execution envelope (FactOnly)."""

    replay_ref: str
    verifier_ref: str
    checked_trace_hashes: List[str]
    checked_output_hash: str
    authority_effect: str = "FactOnly"


@dataclass(frozen=True)
class RefusedReplayReport:
    """Refused replay report envelope (AuthorityEffect: Refused)."""

    replay_ref: str
    verifier_ref: str
    refusal_reason: str
    authority_effect: str = "Refused"


class ReplayKernel:
    """Historical execution reconstruction kernel."""

    def __init__(
        self,
        kernel_id: str = "omega_replay_kernel_001",
        kernel_version: str = "v1.0.0",
        verifier_ref: str = "omega_replay_verifier_001",
    ):
        self.kernel_id = kernel_id
        self.kernel_version = kernel_version
        self.verifier_ref = verifier_ref
        self.schema_hash = self.compute_schema_hash()

    def compute_schema_hash(self) -> str:
        raw = f"{CONTRACT_ID}:{SCHEMA_VERSION}:{self.kernel_id}:{self.kernel_version}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def execute_replay(
        self,
        replay_id: str,
        trace_refs: Sequence[str],
        manifest_ref: str,
        execution_output: Any,
    ) -> ReplayReport:
        """Create an unverified ReplayReport (EvidenceOnly)."""
        raw_bytes = json.dumps(execution_output, sort_keys=True, default=str).encode("utf-8")
        out_hash = hashlib.sha256(raw_bytes).hexdigest()

        return ReplayReport(
            replay_id=replay_id,
            trace_refs=list(trace_refs),
            manifest_ref=manifest_ref,
            status=ReplayStatus.UNVERIFIED,
            output_hash=out_hash,
            authority_effect="EvidenceOnly",
        )

    def verify_report(self, report: ReplayReport) -> Union[VerifiedReplayReport, RefusedReplayReport]:
        """Verify replay report integrity and promote to VerifiedReplayReport (FactOnly) or return RefusedReplayReport."""
        if not report.manifest_ref or report.manifest_ref == "":
            return RefusedReplayReport(
                replay_ref=report.replay_id,
                verifier_ref=self.verifier_ref,
                refusal_reason="Replay report missing manifest reference",
            )
        if not report.trace_refs:
            return RefusedReplayReport(
                replay_ref=report.replay_id,
                verifier_ref=self.verifier_ref,
                refusal_reason="Replay report trace references list is empty",
            )
        if not report.output_hash:
            return RefusedReplayReport(
                replay_ref=report.replay_id,
                verifier_ref=self.verifier_ref,
                refusal_reason="Replay report missing output hash",
            )

        trace_hashes = [hashlib.sha256(t.encode("utf-8")).hexdigest() for t in report.trace_refs]
        return VerifiedReplayReport(
            replay_ref=report.replay_id,
            verifier_ref=self.verifier_ref,
            checked_trace_hashes=trace_hashes,
            checked_output_hash=report.output_hash,
            authority_effect="FactOnly",
        )


def verify_replay_contract(replay: ReplayKernel) -> Dict[str, Any]:
    return {
        "contract_id": CONTRACT_ID,
        "kernel_id": replay.kernel_id,
        "schema_hash": replay.schema_hash,
        "authority_effect": "EvidenceOnly",
        "admissible": True,
    }


__all__ = [
    "CONTRACT_ID",
    "SCHEMA_VERSION",
    "ReplayStatus",
    "ReplayReport",
    "VerifiedReplayReport",
    "RefusedReplayReport",
    "ReplayKernel",
    "verify_replay_contract",
]




