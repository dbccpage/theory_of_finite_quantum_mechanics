"""Prime types package under type/prime."""

from .adapter import AdapterCheck, AdapterStatus, LossEntry, LossLedger
from .candidate_packet import CandidatePacket
from .continuation import AntiCheatFlags, CanContinueInput, CanContinueResult
from .declaration import (
    DECLARATION_STEPS,
    AdmissionDecision,
    AdmissionKind,
    DeclarationPacket,
)

__all__ = (
    "AdapterCheck",
    "AdapterStatus",
    "AdmissionDecision",
    "AdmissionKind",
    "AntiCheatFlags",
    "CanContinueInput",
    "CanContinueResult",
    "CandidatePacket",
    "DECLARATION_STEPS",
    "DeclarationPacket",
    "LossEntry",
    "LossLedger",
)
