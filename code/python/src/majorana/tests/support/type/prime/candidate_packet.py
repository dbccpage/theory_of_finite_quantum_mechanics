"""CandidatePacket domain type (OE001-01). AuthorityEffect: None."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class CandidatePacket:
    """Pre-admission proposal. Confers no validity (OE001-01)."""

    artifact_id: str
    locus_id: str
    problem_family: str
    carrier_proposal: Optional[str] = None
    observer_proposal: Optional[str] = None
    primitive_difference_proposal: Optional[str] = None
    zero_rel_proposal: Optional[str] = None
    witness_available: bool = False
    adapter_confidence: str = "unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: str = "proposed_only"
    authority_effect: str = "None"
