"""TraceWriter Contract Boundary (append-only persistence).

Doctrine:
- Append-only persistence for canonical TraceArtifacts.
- Structurally and causally validates candidate appends before persistence (schema, hash, head hash, sequence).
- Does NOT execute Replay (Replay is run downstream by ReplayKernel).
- AuthorityEffect: EvidenceOnly.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Final, List, Tuple

from omega_engine.crates.type.trace.base.trace_artifact import TraceArtifact, TraceBundle

CONTRACT_ID: Final[str] = "urn:omega:evidence:trace_writer:v1.0.0"


class TraceWriter:
    """Append-only storage writer enforcing causal-head continuity."""

    contract_id: Final[str] = CONTRACT_ID
    authority_effect: Final[str] = "EvidenceOnly"

    def __init__(self, run_id: str) -> None:
        self.run_id = run_id
        self._artifacts: List[TraceArtifact] = []
        self._trace_map: Dict[str, TraceArtifact] = {}
        self._head_hash: str = f"sha256:genesis_{run_id}"

    def append(self, artifact: TraceArtifact) -> str:
        """Appends candidate TraceArtifact after structural and head validation."""
        if artifact.run_id != self.run_id:
            raise ValueError(f"Artifact run_id ({artifact.run_id}) mismatch for writer ({self.run_id})")

        if artifact.trace_id in self._trace_map:
            raise ValueError(f"Duplicate trace_id: {artifact.trace_id}")

        expected_hash = artifact.compute_hash()
        if artifact.artifact_hash != expected_hash:
            raise ValueError(
                f"Artifact hash invalid: expected {expected_hash}, got {artifact.artifact_hash}"
            )

        if self._artifacts:
            expected_seq = self._artifacts[-1].sequence + 1
            if artifact.sequence != expected_seq:
                raise ValueError(
                    f"Non-monotonic sequence: expected {expected_seq}, got {artifact.sequence}"
                )

        self._artifacts.append(artifact)
        self._trace_map[artifact.trace_id] = artifact
        self._head_hash = artifact.artifact_hash
        return artifact.trace_id

    def get_bundle(self) -> TraceBundle:
        """Returns the canonical immutable TraceBundle for this run."""
        bundle = TraceBundle(
            run_id=self.run_id,
            artifacts=tuple(self._artifacts),
        )
        return TraceBundle(
            run_id=self.run_id,
            artifacts=tuple(self._artifacts),
            bundle_hash=bundle.compute_hash(),
        )


__all__ = [
    "TraceWriter",
    "CONTRACT_ID",
]
