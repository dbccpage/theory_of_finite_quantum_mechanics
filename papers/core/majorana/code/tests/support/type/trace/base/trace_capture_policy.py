"""TraceCapturePolicy Contract Value Object.

Doctrine:
- Policy configuration specifying recording level, retention, and redactions.
- AuthorityEffect: None.
- emits: [].
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Final, Tuple

CONTRACT_ID: Final[str] = "urn:omega:evidence:trace_capture_policy:v1.0.0"


@dataclass(frozen=True, slots=True)
class TraceCapturePolicy:
    """Immutable recording/retention/redaction policy configuration."""

    policy_id: str = "default_policy"
    capture_level: str = "full"  # "full", "minimal", "off"
    retention_days: int = 30
    redact_fields: Tuple[str, ...] = ()
    authority_effect: str = "None"


__all__ = [
    "TraceCapturePolicy",
    "CONTRACT_ID",
]
