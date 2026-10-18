"""Prime stage operations and re-exported types."""

from __future__ import annotations

from ..type.prime import (
    DECLARATION_STEPS,
    AdapterCheck,
    AdapterStatus,
    AdmissionDecision,
    AdmissionKind,
    AntiCheatFlags,
    CanContinueInput,
    CanContinueResult,
    CandidatePacket,
    DeclarationPacket,
    LossEntry,
    LossLedger,
)
from ..type.trace import IntakeTraceRecord
from ..trace.intake_trace import IntakeTrace

from .prime_minus_one import propose_candidate
from .prime_000 import admit_declaration
from .prime_001 import check_adapter
from .prime_002 import can_continue

__all__ = (
    "DECLARATION_STEPS",
    "AdapterCheck",
    "AdapterStatus",
    "AdmissionDecision",
    "AdmissionKind",
    "AntiCheatFlags",
    "CanContinueInput",
    "CanContinueResult",
    "CandidatePacket",
    "DeclarationPacket",
    "IntakeTrace",
    "IntakeTraceRecord",
    "LossEntry",
    "LossLedger",
    "admit_declaration",
    "can_continue",
    "check_adapter",
    "propose_candidate",
)
