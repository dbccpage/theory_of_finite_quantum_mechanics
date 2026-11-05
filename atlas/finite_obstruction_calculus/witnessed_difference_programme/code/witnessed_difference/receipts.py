"""Canonical content-bound receipts; verification always reuses supplied artifacts."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from .exact import canonical_data
from .outcomes import Accepted, AuthorityEffect, Outcome, RefusalCode, Refused


def canonical_json(value: Any) -> str:
    return json.dumps(canonical_data(value), ensure_ascii=True, separators=(",", ":"), sort_keys=True)


def content_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Receipt:
    subject: str
    input_digest: str
    output_digest: str
    claim_ids: tuple[str, ...]
    implementation_version: str
    receipt_digest: str
    authority_effect: AuthorityEffect = AuthorityEffect.NONE

    def __post_init__(self) -> None:
        if self.authority_effect is not AuthorityEffect.NONE:
            raise ValueError("receipts cannot carry an authority effect")


def _receipt_body(
    subject: str,
    input_digest: str,
    output_digest: str,
    claim_ids: tuple[str, ...],
    implementation_version: str,
) -> dict[str, object]:
    return {
        "authority_effect": AuthorityEffect.NONE.value,
        "claim_ids": list(claim_ids),
        "implementation_version": implementation_version,
        "input_digest": input_digest,
        "output_digest": output_digest,
        "subject": subject,
    }


def make_receipt(
    subject: str,
    inputs: Any,
    output: Any,
    claim_ids: tuple[str, ...],
    *,
    implementation_version: str = "0.1.0",
) -> Outcome[Receipt]:
    if (
        not isinstance(subject, str)
        or not subject
        or not isinstance(implementation_version, str)
        or not implementation_version
        or type(claim_ids) is not tuple
        or not claim_ids
        or any(not isinstance(item, str) or not item for item in claim_ids)
    ):
        return Refused(RefusalCode.INVALID_INPUT, "subject, version, and nonempty claim ids are required")
    normalized_claims = tuple(sorted(set(claim_ids)))
    try:
        input_digest = content_hash(inputs)
        output_digest = content_hash(output)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError):
        return Refused(
            RefusalCode.INVALID_INPUT,
            "receipt inputs and output must be canonicalizable",
        )
    body = _receipt_body(subject, input_digest, output_digest, normalized_claims, implementation_version)
    return Accepted(
        Receipt(
            subject,
            input_digest,
            output_digest,
            normalized_claims,
            implementation_version,
            content_hash(body),
        )
    )


def verify_receipt(receipt: Receipt, inputs: Any, output: Any) -> Outcome[bool]:
    if not isinstance(receipt, Receipt):
        return Refused(RefusalCode.INVALID_INPUT, "receipt has the wrong type")
    if receipt.authority_effect is not AuthorityEffect.NONE:
        return Refused(RefusalCode.CLAIM_STATUS_FIREWALL, "receipt carries an authority effect")
    body = _receipt_body(
        receipt.subject,
        receipt.input_digest,
        receipt.output_digest,
        receipt.claim_ids,
        receipt.implementation_version,
    )
    if receipt.receipt_digest != content_hash(body):
        return Refused(RefusalCode.RECEIPT_MISMATCH, "receipt body was modified")
    try:
        input_digest = content_hash(inputs)
        output_digest = content_hash(output)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError):
        return Refused(
            RefusalCode.INVALID_INPUT,
            "receipt inputs and output must be canonicalizable",
        )
    if receipt.input_digest != input_digest:
        return Refused(RefusalCode.DIGEST_MISMATCH, "input artifact differs from receipt")
    if receipt.output_digest != output_digest:
        return Refused(RefusalCode.DIGEST_MISMATCH, "output artifact differs from receipt")
    return Accepted(True)
# Executable finite evidence; AuthorityEffect: None.
