"""Retained registration, re-access, and replayable witness receipts."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from .exact import canonical_data
from .outcomes import Accepted, AuthorityEffect, Outcome, RefusalCode, Refused


def payload_digest(payload: Any) -> str:
    encoded = json.dumps(
        canonical_data(payload), ensure_ascii=True, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class Registration:
    carrier_id: str
    mark: Any
    occurrence: int
    retained: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.carrier_id, str) or not self.carrier_id:
            raise ValueError("carrier_id is required")
        if type(self.occurrence) is not int or self.occurrence < 0:
            raise ValueError("occurrence must be a non-negative integer")
        if type(self.retained) is not bool:
            raise ValueError("retained must be a boolean")

    @property
    def mark_digest(self) -> str:
        return payload_digest(self.mark)


@dataclass(frozen=True)
class ReaccessReceipt:
    evaluator_id: str
    expected_digest: str
    observed_digest: str

    def __post_init__(self) -> None:
        if not isinstance(self.evaluator_id, str) or not self.evaluator_id:
            raise ValueError("evaluator_id is required")
        for digest in (self.expected_digest, self.observed_digest):
            if not isinstance(digest, str) or len(digest) != 64:
                raise ValueError("re-access digests must be SHA-256 hex strings")
            try:
                int(digest, 16)
            except ValueError as exc:
                raise ValueError("re-access digests must be SHA-256 hex strings") from exc

    @property
    def matches(self) -> bool:
        return self.expected_digest == self.observed_digest


@dataclass(frozen=True)
class WitnessReceipt:
    registration: Registration
    reaccess: ReaccessReceipt
    receipt_digest: str
    authority_effect: AuthorityEffect = AuthorityEffect.NONE

    def __post_init__(self) -> None:
        if self.authority_effect is not AuthorityEffect.NONE:
            raise ValueError("witness receipts cannot carry an authority effect")


def _receipt_payload(registration: Registration, reaccess: ReaccessReceipt) -> dict[str, Any]:
    return {
        "carrier_id": registration.carrier_id,
        "evaluator_id": reaccess.evaluator_id,
        "expected_digest": reaccess.expected_digest,
        "observed_digest": reaccess.observed_digest,
        "occurrence": registration.occurrence,
        "retained": registration.retained,
    }


def make_witness(
    registration: Registration,
    observed_mark: Any,
    evaluator_id: str,
) -> Outcome[WitnessReceipt]:
    if not isinstance(registration, Registration):
        return Refused(RefusalCode.INVALID_INPUT, "registration has the wrong type")
    if not registration.retained:
        return Refused(RefusalCode.NOT_RETAINED, "the registration is not retained")
    if not isinstance(evaluator_id, str) or not evaluator_id:
        return Refused(RefusalCode.INVALID_INPUT, "evaluator_id is required")
    try:
        expected_digest = registration.mark_digest
        observed_digest = payload_digest(observed_mark)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError):
        return Refused(
            RefusalCode.INVALID_INPUT,
            "retained and observed marks must be canonicalizable",
        )
    reaccess = ReaccessReceipt(
        evaluator_id=evaluator_id,
        expected_digest=expected_digest,
        observed_digest=observed_digest,
    )
    if not reaccess.matches:
        return Refused(RefusalCode.REACCESS_FAILED, "re-access did not reproduce the retained mark")
    digest = payload_digest(_receipt_payload(registration, reaccess))
    return Accepted(WitnessReceipt(registration, reaccess, digest))


def verify_witness(receipt: WitnessReceipt, observed_mark: Any) -> Outcome[bool]:
    if not isinstance(receipt, WitnessReceipt):
        return Refused(RefusalCode.INVALID_INPUT, "witness receipt has the wrong type")
    if receipt.authority_effect is not AuthorityEffect.NONE:
        return Refused(RefusalCode.CLAIM_STATUS_FIREWALL, "witness receipt carries an authority effect")
    if not receipt.registration.retained:
        return Refused(RefusalCode.NOT_RETAINED, "receipt refers to an unretained mark")
    try:
        retained_digest = receipt.registration.mark_digest
        observed_digest = payload_digest(observed_mark)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError):
        return Refused(
            RefusalCode.INVALID_INPUT,
            "retained and observed marks must be canonicalizable",
        )
    if retained_digest != receipt.reaccess.expected_digest:
        return Refused(
            RefusalCode.DIGEST_MISMATCH,
            "current retained mark differs from the receipt binding",
        )
    if observed_digest != receipt.reaccess.observed_digest:
        return Refused(RefusalCode.DIGEST_MISMATCH, "artifact digest differs from the receipt")
    expected = payload_digest(_receipt_payload(receipt.registration, receipt.reaccess))
    if expected != receipt.receipt_digest or not receipt.reaccess.matches:
        return Refused(RefusalCode.RECEIPT_MISMATCH, "receipt fields do not match its digest")
    return Accepted(True)
# Executable finite evidence; AuthorityEffect: None.
