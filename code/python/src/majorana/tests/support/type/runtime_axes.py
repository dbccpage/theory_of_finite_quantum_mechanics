"""Four-axis runtime enums and DDA alphabet (OE-010).

AuthorityEffect: None.
Canonical home: type/runtime_axes (not dda/).
"""

from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Optional


class DiagnosticClass(str, enum.Enum):
    ExactClass = "ExactClass"
    ClosedResidual = "ClosedResidual"
    ActiveClosureFailure = "ActiveClosureFailure"
    DetectorInadequate = "DetectorInadequate"
    NotComputed = "NotComputed"


class RoutingTerminal(str, enum.Enum):
    ShapeChecked = "ShapeChecked"
    CheckPassed = "CheckPassed"
    Repair = "Repair"
    Refusal = "Refusal"
    OracleNeeded = "OracleNeeded"
    NoRule = "NoRule"
    BudgetUnknown = "BudgetUnknown"
    RequiresLift = "RequiresLift"


class ExtensionStatus(str, enum.Enum):
    NoExtensionNeeded = "NoExtensionNeeded"
    ExtensionRequested = "ExtensionRequested"
    LicensedLift = "LicensedLift"
    ExtensionRefused = "ExtensionRefused"


class AuthorityStatus(str, enum.Enum):
    NoneStatus = "None"
    ContractScopedOnly = "ContractScopedOnly"
    ExternalHumanPromotionRequired = "ExternalHumanPromotionRequired"


class DdaLetter(str, enum.Enum):
    """OE-010 operational alphabet A_DDA = {E,R,C,I,Λ,D,M,T}."""

    E = "E"
    R = "R"
    C = "C"
    I = "I"
    LAMBDA = "Λ"
    D = "D"
    M = "M"
    T = "T"


class DdaDialect(str, enum.Enum):
    LEGACY_V1 = "legacy-v1"
    OEARS_V1 = "oears-v1"
    EXPERIMENTAL_Z_V1 = "experimental-z-v1"


class ExperimentalDdaLetter(str, enum.Enum):
    Z = "Z"


class CohomologicalStatus(str, enum.Enum):
    ExactRepair = "ExactRepair"
    ClosedSurvivor = "ClosedSurvivor"
    ActiveClosureFailure = "ActiveClosureFailure"


@dataclass(frozen=True)
class DdaStepReceipt:
    step_id: str
    letter: DdaLetter
    input_state_hash: str
    output_state_hash: str
    carrier_hash: str
    diagnostic_before: str
    diagnostic_after: str
    required_witness: str
    witness_hash: str
    refusal_reason: Optional[str] = None
    authority_effect: str = "None"
