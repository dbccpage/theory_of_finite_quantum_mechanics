"""Prime −1: candidate packet proposal stage. AuthorityEffect: None."""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..type.prime.candidate_packet import CandidatePacket


def propose_candidate(
    *,
    artifact_id: str,
    locus_id: str,
    problem_family: str,
    carrier_proposal: Optional[str] = None,
    observer_proposal: Optional[str] = None,
    primitive_difference_proposal: Optional[str] = None,
    zero_rel_proposal: Optional[str] = None,
    witness_available: bool = False,
    adapter_confidence: str = "unknown",
    metadata: Optional[Dict[str, Any]] = None,
) -> CandidatePacket:
    """Emit a CandidatePacket; never admits and never enters DdaTrace."""
    return CandidatePacket(
        artifact_id=artifact_id,
        locus_id=locus_id,
        problem_family=problem_family,
        carrier_proposal=carrier_proposal,
        observer_proposal=observer_proposal,
        primitive_difference_proposal=primitive_difference_proposal,
        zero_rel_proposal=zero_rel_proposal,
        witness_available=witness_available,
        adapter_confidence=adapter_confidence,
        metadata=dict(metadata or {}),
    )
