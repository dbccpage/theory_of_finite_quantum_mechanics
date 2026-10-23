"""Typed outcomes shared by all executable witnesses."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Generic, NoReturn, TypeVar

from witnessed_difference.rop import Err, Ok, Refusal, Result

T = TypeVar("T")


class AuthorityEffect(str, Enum):
    """The only authority effect admitted by this package."""

    NONE = "None"


class RefusalCode(str, Enum):
    INVALID_INPUT = "invalid_input"
    OUTSIDE_CARRIER = "outside_carrier"
    NOT_RETAINED = "not_retained"
    DIGEST_MISMATCH = "digest_mismatch"
    REACCESS_FAILED = "reaccess_failed"
    MISSING_ADAPTER = "missing_adapter"
    ADAPTER_MISMATCH = "adapter_mismatch"
    REPORT_PROFILE_COLLAPSE = "report_profile_collapse"
    NO_INTERACTION = "no_interaction"
    COUPLING_MISMATCH = "coupling_mismatch"
    NO_REGISTRATION = "no_registration"
    NO_WITNESS = "no_witness"
    NO_ACCEPTING_EVALUATOR = "no_accepting_evaluator"
    NON_ACCEPTING_STANDING = "non_accepting_standing"
    EVALUATOR_MISMATCH = "evaluator_mismatch"
    MISSING_OBSERVATION = "missing_observation"
    MISSING_MEASURAND = "missing_measurand"
    MISSING_REPORTED_VALUE = "missing_reported_value"
    MISSING_VALUE_MAP = "missing_value_map"
    VALUE_MAP_MISMATCH = "value_map_mismatch"
    MISSING_SCALE = "missing_scale"
    MISSING_UNIT = "missing_unit"
    MISSING_CALIBRATION = "missing_calibration"
    MISSING_TRACEABILITY = "missing_traceability"
    MISSING_PROVENANCE = "missing_provenance"
    BROKEN_TRACEABILITY = "broken_traceability"
    MISSING_CHAIN_UNCERTAINTY = "missing_chain_uncertainty"
    TRACEABILITY_TYPE_CONFUSION = "traceability_type_confusion"
    OUT_OF_RANGE = "out_of_range"
    OFF_GRID = "off_grid"
    INVALID_UNCERTAINTY = "invalid_uncertainty"
    NOT_CLOSED = "not_closed"
    NOT_EXACT = "not_exact"
    BUDGET_REQUIRED = "budget_required"
    EMPTY_SPACE = "empty_space"
    EVENT_OUTSIDE_SPACE = "event_outside_space"
    NOT_DISJOINT = "not_disjoint"
    OPEN_PATH = "open_path"
    MISSING_EDGE = "missing_edge"
    NON_UNIT_PHASE = "non_unit_phase"
    SCOPE_VIOLATION = "scope_violation"
    OUTSIDE_PROFILE = "outside_profile"
    CLAIM_STATUS_FIREWALL = "claim_status_firewall"
    RECEIPT_MISMATCH = "receipt_mismatch"
    CERTIFICATE_MISMATCH = "certificate_mismatch"
    NO_RULE = "no_rule"
    NOT_REPAIR_COMPATIBLE = "not_repair_compatible"
    GRAMMAR_VIOLATION = "grammar_violation"
    INFEASIBLE = "infeasible"
    UNBOUNDED = "unbounded"
    BUDGET_EXHAUSTED = "budget_exhausted"
    NOT_INVERTIBLE = "not_invertible"
    NOT_PROJECTIVE = "not_projective"
    NOT_HERMITIAN = "not_hermitian"
    NOT_POSITIVE_SEMIDEFINITE = "not_positive_semidefinite"
    NOT_ORTHOGONAL_PROJECTOR = "not_orthogonal_projector"
    NOT_A_REDUCED_ZERO = "not_a_reduced_zero"
    NOT_INJECTIVE = "not_injective"
    NOT_SURJECTIVE = "not_surjective"
    DOES_NOT_DESCEND = "does_not_descend"
    NOT_A_DIFFERENTIAL = "not_a_differential"
    NOT_CHAIN_MAP = "not_chain_map"
    NOT_A_RETRACTION = "not_a_retraction"
    HOMOTOPY_MISMATCH = "homotopy_mismatch"


@dataclass(frozen=True)
class Accepted(Generic[T]):
    value: T
    authority_effect: AuthorityEffect = AuthorityEffect.NONE

    def __post_init__(self) -> None:
        if self.authority_effect is not AuthorityEffect.NONE:
            raise ValueError("accepted outcomes cannot carry an authority effect")

    @property
    def is_ok(self) -> bool:
        return True

    @property
    def is_err(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self.value

    def unwrap_err(self) -> NoReturn:
        raise ValueError("cannot unwrap_err from Accepted")


@dataclass(frozen=True)
class Refused:
    code: RefusalCode
    detail: str
    authority_effect: AuthorityEffect = AuthorityEffect.NONE

    def __post_init__(self) -> None:
        if self.authority_effect is not AuthorityEffect.NONE:
            raise ValueError("refused outcomes cannot carry an authority effect")

    @property
    def is_ok(self) -> bool:
        return False

    @property
    def is_err(self) -> bool:
        return True

    def unwrap(self) -> NoReturn:
        raise ValueError(f"cannot unwrap Refused: {self.code} - {self.detail}")

    def unwrap_err(self) -> Refusal:
        return self.to_refusal()

    def to_refusal(self) -> Refusal:
        raw_code = self.code.value if isinstance(self.code, RefusalCode) else str(self.code)
        return Refusal(
            code=raw_code.upper(),
            message=self.detail,
            locus="witnessed_difference.outcomes",
            details=(("authority_effect", "None"),),
        )


Outcome = Accepted[T] | Refused
__all__ = [
    "AuthorityEffect",
    "RefusalCode",
    "Accepted",
    "Refused",
    "Outcome",
    "Ok",
    "Err",
    "Refusal",
    "Result",
]
# Executable finite evidence; AuthorityEffect: None.
