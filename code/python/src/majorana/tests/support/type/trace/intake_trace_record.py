"""IntakeTraceRecord domain type (OE001-01). AuthorityEffect: None."""

from __future__ import annotations

from dataclasses import dataclass
from ..prime.candidate_packet import CandidatePacket


@dataclass(frozen=True)
class IntakeTraceRecord:
    raw_artifact_hash: str
    candidate_locus: str
    candidate_packet: CandidatePacket
    intake_adapter_status: str
    enters_dda_trace: bool = False
    authority_effect: str = "None"
