"""IntakeTrace pre-admission log aggregate (OE001-01). AuthorityEffect: None."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .intake_trace_record import IntakeTraceRecord


@dataclass
class IntakeTrace:
    """Pre-admission log. Contaminating DdaTrace is a protocol bug."""

    records: List[IntakeTraceRecord] = field(default_factory=list)

    def append(self, record: IntakeTraceRecord) -> None:
        if record.enters_dda_trace:
            raise ValueError(
                "IntakeTrace protocol: enters_dda_trace must be false (OE001-01)"
            )
        self.records.append(record)

    def as_dicts(self) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        for r in self.records:
            out.append(
                {
                    "raw_artifact_hash": r.raw_artifact_hash,
                    "candidate_locus": r.candidate_locus,
                    "candidate_packet": r.candidate_packet,
                    "intake_adapter_status": r.intake_adapter_status,
                    "enters_dda_trace": r.enters_dda_trace,
                    "authority_effect": r.authority_effect,
                }
            )
        return out
