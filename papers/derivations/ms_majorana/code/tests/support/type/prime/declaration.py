"""Declaration types for Prime 000 7-step declaration order (OE001-02)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional, Tuple

DECLARATION_STEPS: Tuple[str, ...] = (
    "locus_grounding",
    "carrier",
    "observer",
    "primitive_difference",
    "zero_rel",
    "witness_or_refusal",
    "optional_policy",
)


class AdmissionKind(str, Enum):
    ACCEPT_DECLARATION = "ACCEPT_DECLARATION"
    REFUSE_MISSING_CARRIER = "REFUSE_MISSING_CARRIER"
    REFUSE_MISSING_OBSERVER = "REFUSE_MISSING_OBSERVER"
    REFUSE_MISSING_WITNESS = "REFUSE_MISSING_WITNESS"
    REFUSE_MISSING_QUOTIENT = "REFUSE_MISSING_QUOTIENT"
    REFUSE_MISSING_LOCUS = "REFUSE_MISSING_LOCUS"
    REFUSE_MISSING_PRIMITIVE_DIFFERENCE = "REFUSE_MISSING_PRIMITIVE_DIFFERENCE"
    REFUSE_MISSING_ZERO_REL = "REFUSE_MISSING_ZERO_REL"
    SPLIT_PACKET = "SPLIT_PACKET"
    REQUEST_LIFT = "REQUEST_LIFT"


@dataclass(frozen=True)
class DeclarationPacket:
    """Admitted-or-refused declaration fields (post-candidate)."""

    domain: str
    locus_hash: Optional[str] = None
    carrier: Optional[str] = None
    observer: Optional[str] = None
    primitive_difference: Optional[str] = None
    zero_rel: Optional[str] = None
    witness: Optional[str] = None
    refusal_route: Optional[str] = None
    optional_policy: Optional[Dict[str, Any]] = None
    request_lift: bool = False
    request_split: bool = False


@dataclass(frozen=True)
class AdmissionDecision:
    kind: AdmissionKind
    filled_steps: Tuple[str, ...]
    reason: str
    authority_effect: str = "None"
    steps: Tuple[Dict[str, Any], ...] = ()
