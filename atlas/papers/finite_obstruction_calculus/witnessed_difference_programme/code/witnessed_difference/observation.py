# Executable finite evidence; AuthorityEffect: None.
"""General observation receipts and the narrower accepted E-observation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .outcomes import Accepted, AuthorityEffect, Outcome, RefusalCode, Refused
from .witness import Registration, WitnessReceipt, verify_witness


class EvaluatorStanding(str, Enum):
    ACCEPTING = "accepting"
    NON_ACCEPTING = "non_accepting"


class EvaluatorStatus(str, Enum):
    ACCEPT = "Accept"
    REJECT = "Reject"
    REFUSE = "Refuse"
    UNDETERMINED = "Undetermined"


@dataclass(frozen=True)
class Interaction:
    poles: tuple[str, ...]
    registration_carrier_id: str
    mark_capacity: bool = True

    def __post_init__(self) -> None:
        if (
            not isinstance(self.poles, tuple)
            or len(self.poles) < 2
            or any(not isinstance(pole, str) or not pole for pole in self.poles)
        ):
            raise ValueError("interaction needs at least two distinct named poles")
        if len(set(self.poles)) != len(self.poles):
            raise ValueError("interaction needs at least two distinct named poles")
        if (
            not isinstance(self.registration_carrier_id, str)
            or not self.registration_carrier_id
            or self.registration_carrier_id not in self.poles
        ):
            raise ValueError("interaction must name the registration carrier among its poles")
        if type(self.mark_capacity) is not bool:
            raise ValueError("mark_capacity must be a boolean")


@dataclass(frozen=True)
class EvaluatorResult:
    evaluator_id: str
    status: EvaluatorStatus
    standing: EvaluatorStanding

    def __post_init__(self) -> None:
        if not isinstance(self.evaluator_id, str) or not self.evaluator_id:
            raise ValueError("evaluator_id is required")
        if not isinstance(self.status, EvaluatorStatus):
            raise ValueError("status must be an EvaluatorStatus")
        if not isinstance(self.standing, EvaluatorStanding):
            raise ValueError("standing must be an EvaluatorStanding")


@dataclass(frozen=True)
class ObservationReceipt:
    """A record of an attempt, including rejection, refusal, or missing stages."""

    interaction: Interaction | None
    registration: Registration | None
    witness: WitnessReceipt | None
    evaluator_result: EvaluatorResult | None
    authority_effect: AuthorityEffect = AuthorityEffect.NONE

    def __post_init__(self) -> None:
        if self.authority_effect is not AuthorityEffect.NONE:
            raise ValueError("observation receipts cannot carry an authority effect")


@dataclass(frozen=True)
class AcceptedObservation:
    """An E-observation whose full ladder and Accept status were checked."""

    receipt: ObservationReceipt
    authority_effect: AuthorityEffect = AuthorityEffect.NONE

    def __post_init__(self) -> None:
        if self.authority_effect is not AuthorityEffect.NONE:
            raise ValueError("accepted observations cannot carry an authority effect")
        refusal = _observation_refusal(self.receipt)
        if refusal is not None:
            raise ValueError(f"invalid accepted observation: {refusal.code.value}")

    @property
    def interaction(self) -> Interaction:
        assert self.receipt.interaction is not None
        return self.receipt.interaction

    @property
    def registration(self) -> Registration:
        assert self.receipt.registration is not None
        return self.receipt.registration

    @property
    def witness(self) -> WitnessReceipt:
        assert self.receipt.witness is not None
        return self.receipt.witness

    @property
    def evaluator_result(self) -> EvaluatorResult:
        assert self.receipt.evaluator_result is not None
        return self.receipt.evaluator_result


def _observation_refusal(receipt: ObservationReceipt) -> Refused | None:
    if not isinstance(receipt, ObservationReceipt):
        return Refused(RefusalCode.INVALID_INPUT, "observation receipt has the wrong type")
    if receipt.authority_effect is not AuthorityEffect.NONE:
        return Refused(
            RefusalCode.CLAIM_STATUS_FIREWALL,
            "observation receipt carries an authority effect",
        )
    interaction = receipt.interaction
    registration = receipt.registration
    witness = receipt.witness
    result = receipt.evaluator_result
    if not isinstance(interaction, Interaction) or not interaction.mark_capacity:
        return Refused(RefusalCode.NO_INTERACTION, "no mark-capable interaction was supplied")
    if not isinstance(registration, Registration) or not registration.retained:
        return Refused(RefusalCode.NO_REGISTRATION, "no retained registration was supplied")
    if interaction.registration_carrier_id != registration.carrier_id:
        return Refused(
            RefusalCode.COUPLING_MISMATCH,
            "the mark-capable interaction is not bound to the supplied registration carrier",
        )
    if not isinstance(witness, WitnessReceipt):
        return Refused(RefusalCode.NO_WITNESS, "no replayable witness was supplied")
    if witness.registration != registration:
        return Refused(RefusalCode.DIGEST_MISMATCH, "witness does not bind the supplied registration")
    witness_check = verify_witness(witness, registration.mark)
    if isinstance(witness_check, Refused):
        return witness_check
    if not isinstance(result, EvaluatorResult) or result.status is not EvaluatorStatus.ACCEPT:
        status = "missing" if not isinstance(result, EvaluatorResult) else result.status.value
        return Refused(RefusalCode.NO_ACCEPTING_EVALUATOR, f"evaluator status is {status}, not Accept")
    if result.standing is not EvaluatorStanding.ACCEPTING:
        return Refused(RefusalCode.NON_ACCEPTING_STANDING, "Accept lacks evaluator standing")
    if result.evaluator_id != witness.reaccess.evaluator_id:
        return Refused(RefusalCode.EVALUATOR_MISMATCH, "witness and evaluator result use different evaluators")
    return None


def classify_observation(receipt: ObservationReceipt) -> Outcome[AcceptedObservation]:
    refusal = _observation_refusal(receipt)
    if refusal is not None:
        return refusal
    return Accepted(AcceptedObservation(receipt))
