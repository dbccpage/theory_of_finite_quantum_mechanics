"""OESOS–DDA typed packet lifecycle + one-shot ActionLicense (Gates 5/8/9).

Strict authority fences:
  CandidatePacket → EvaluationReceipt → VerificationReceipt
       → ActionLicense | LicenseRefusal → (HostExecutor only) ApplicationReceipt → TerminalReceipt

Hard laws (canonical v0.1):
- AuthorityEffect is None / EvidenceOnly for every OESOS/DDA stage.
- Only HostExecutor (engine/) may consume an ActionLicense and perform StateTransition.
- ActionLicense itself is frozen evidence; consumption is tracked by the host ledger.
- Evaluation and verification are evidence-only and never issue a license.
- Every licensing path remains refusal-only until the external decision
  validator is implemented in P3-07D.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional, Protocol, Tuple

from .solv_obstruction_evaluator import (
    ObstructionClass,
    ObstructionReceipt,
)

SCHEMA_VERSION = "oesos.dda.lifecycle.v0.1"


def _stable_sha256(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class CandidatePacket:
    packet_id: str
    model_digest: str
    omega_digest: str
    policy_digest: str
    payload: Dict[str, Any] = field(default_factory=dict)
    schema_version: str = SCHEMA_VERSION
    authority_effect: str = "None"

    def digest(self) -> str:
        return _stable_sha256(
            {
                "packet_id": self.packet_id,
                "model_digest": self.model_digest,
                "omega_digest": self.omega_digest,
                "policy_digest": self.policy_digest,
                "payload": self.payload,
                "schema_version": self.schema_version,
            }
        )


@dataclass(frozen=True)
class EvaluationReceipt:
    candidate_digest: str
    obstruction: ObstructionReceipt
    evaluator_id: str
    schema_version: str = SCHEMA_VERSION
    authority_effect: str = "None"

    @property
    def evidence_sha256(self) -> str:
        return self.obstruction.evidence_sha256

    @property
    def classification(self) -> ObstructionClass:
        return self.obstruction.classification

    def digest(self) -> str:
        return _stable_sha256(
            {
                "candidate_digest": self.candidate_digest,
                "evidence_sha256": self.evidence_sha256,
                "classification": self.classification.value,
                "evaluator_id": self.evaluator_id,
            }
        )


@dataclass(frozen=True)
class VerificationReceipt:
    evaluation_digest: str
    evidence_sha256: str
    classification: ObstructionClass
    independently_recomputed: bool
    verifier_id: str
    match: bool
    schema_version: str = SCHEMA_VERSION
    authority_effect: str = "None"

    def digest(self) -> str:
        return _stable_sha256(
            {
                "evaluation_digest": self.evaluation_digest,
                "evidence_sha256": self.evidence_sha256,
                "classification": self.classification.value,
                "independently_recomputed": self.independently_recomputed,
                "match": self.match,
                "verifier_id": self.verifier_id,
            }
        )


class RefusalReason(str, Enum):
    NONCLOSED = "NONCLOSED"
    CLOSED_NONEXACT = "CLOSED_NONEXACT"
    INVALID_COMPLEX = "INVALID_COMPLEX"
    VERIFICATION_FAILED = "VERIFICATION_FAILED"
    POLICY_BUDGET = "POLICY_BUDGET"
    NOT_EXACT = "NOT_EXACT"
    EXTERNAL_DECISION_REQUIRED = "EXTERNAL_DECISION_REQUIRED"


@dataclass(frozen=True)
class LicenseRefusal:
    candidate_digest: str
    reason: RefusalReason
    obstruction_class: ObstructionClass
    evidence_sha256: str
    detail: str = ""
    schema_version: str = SCHEMA_VERSION
    authority_effect: str = "None"

    def digest(self) -> str:
        return _stable_sha256(
            {
                "candidate_digest": self.candidate_digest,
                "reason": self.reason.value,
                "obstruction_class": self.obstruction_class.value,
                "evidence_sha256": self.evidence_sha256,
                "detail": self.detail,
            }
        )


@dataclass(frozen=True)
class ActionLicense:
    """One-shot license evidence. Frozen forever. Consumption tracked by host ledger."""

    license_id: str
    candidate_digest: str
    evidence_sha256: str
    write_set: Tuple[str, ...]
    write_set_digest: str
    policy_digest: str
    causal_head_hash: str
    issued_for_class: ObstructionClass  # must be EXACT
    verification_digest: str
    schema_version: str = SCHEMA_VERSION
    authority_effect: str = "None"

    def __post_init__(self) -> None:
        if self.issued_for_class is not ObstructionClass.EXACT:
            raise ValueError(
                "ActionLicense may only be issued for ObstructionClass.EXACT"
            )

    def digest(self) -> str:
        return _stable_sha256(
            {
                "license_id": self.license_id,
                "candidate_digest": self.candidate_digest,
                "evidence_sha256": self.evidence_sha256,
                "write_set": list(self.write_set),
                "write_set_digest": self.write_set_digest,
                "policy_digest": self.policy_digest,
                "causal_head_hash": self.causal_head_hash,
                "issued_for_class": self.issued_for_class.value,
                "verification_digest": self.verification_digest,
            }
        )


@dataclass(frozen=True)
class ApplicationReceipt:
    """Produced only by HostExecutor after successful consume. Packet/ never claims StateTransition."""

    license_digest: str
    applied_write_set_digest: str
    host_id: str
    application_id: str
    schema_version: str = SCHEMA_VERSION
    authority_effect: str = (
        "None"  # conservative; engine/ owns true StateTransition record
    )

    def digest(self) -> str:
        return _stable_sha256(
            {
                "license_digest": self.license_digest,
                "applied_write_set_digest": self.applied_write_set_digest,
                "host_id": self.host_id,
                "application_id": self.application_id,
            }
        )


@dataclass(frozen=True)
class TerminalReceipt:
    packet_id: str
    candidate_digest: str
    obstruction_class: ObstructionClass
    evidence_sha256: str
    terminal_status: str
    license_or_refusal_digest: Optional[str]
    application_digest: Optional[str]
    license_consumed: bool
    schema_version: str = SCHEMA_VERSION
    authority_effect: str = "None"

    def __post_init__(self) -> None:
        if self.application_digest is not None or self.license_consumed:
            raise ValueError(
                "application claims are fenced until canonical apply P3-07A and "
                "Engine admission P3-07E"
            )

    def digest(self) -> str:
        return _stable_sha256(
            {
                "packet_id": self.packet_id,
                "candidate_digest": self.candidate_digest,
                "obstruction_class": self.obstruction_class.value,
                "evidence_sha256": self.evidence_sha256,
                "terminal_status": self.terminal_status,
                "license_or_refusal_digest": self.license_or_refusal_digest,
                "application_digest": self.application_digest,
                "license_consumed": self.license_consumed,
            }
        )


def issue_action_license(
    *,
    license_id: str,
    candidate: CandidatePacket,
    evaluation: EvaluationReceipt,
    verification: VerificationReceipt,
    write_set: Tuple[str, ...],
    causal_head_hash: str,
) -> ActionLicense | LicenseRefusal:
    """Return evidence-specific diagnostics, then refuse automated licensing."""
    if evaluation.classification is not ObstructionClass.EXACT:
        reason = {
            ObstructionClass.NONCLOSED: RefusalReason.NONCLOSED,
            ObstructionClass.CLOSED_NONEXACT: RefusalReason.CLOSED_NONEXACT,
            ObstructionClass.INVALID_COMPLEX: RefusalReason.INVALID_COMPLEX,
        }.get(evaluation.classification, RefusalReason.NOT_EXACT)
        return LicenseRefusal(
            candidate_digest=candidate.digest(),
            reason=reason,
            obstruction_class=evaluation.classification,
            evidence_sha256=evaluation.evidence_sha256,
            detail="classification is not EXACT",
        )
    if not (verification.match and verification.independently_recomputed):
        return LicenseRefusal(
            candidate_digest=candidate.digest(),
            reason=RefusalReason.VERIFICATION_FAILED,
            obstruction_class=evaluation.classification,
            evidence_sha256=evaluation.evidence_sha256,
            detail="verification did not independently recompute / match",
        )
    if verification.evidence_sha256 != evaluation.evidence_sha256:
        return LicenseRefusal(
            candidate_digest=candidate.digest(),
            reason=RefusalReason.VERIFICATION_FAILED,
            obstruction_class=evaluation.classification,
            evidence_sha256=evaluation.evidence_sha256,
            detail="verification evidence_sha256 mismatch",
        )
    del license_id, write_set, causal_head_hash
    return LicenseRefusal(
        candidate_digest=candidate.digest(),
        reason=RefusalReason.EXTERNAL_DECISION_REQUIRED,
        obstruction_class=evaluation.classification,
        evidence_sha256=evaluation.evidence_sha256,
        detail=(
            "evaluation and verification are evidence-only; an external "
            "decision validated by P3-07D is required"
        ),
    )


class HostExecutor(Protocol):
    def consume(self, license: ActionLicense) -> ApplicationReceipt: ...


class InMemoryHostExecutor:
    """Compatibility host fenced from consuming licenses until P3-07D/P3-07E."""

    def __init__(self, host_id: str = "in_memory_host") -> None:
        self.host_id = host_id
        self._consumed: set[str] = set()

    def consume(self, license: ActionLicense) -> ApplicationReceipt:
        del license
        raise RuntimeError(
            "ActionLicense consumption fenced until external decision validation "
            "and the canonical Engine are delivered by P3-07D/P3-07E"
        )


def build_terminal_receipt(
    *,
    packet_id: str,
    candidate: CandidatePacket,
    evaluation: EvaluationReceipt,
    license_or_refusal: ActionLicense | LicenseRefusal | None,
    application: ApplicationReceipt | None = None,
) -> TerminalReceipt:
    if application is not None:
        raise ValueError(
            "application receipts are fenced until canonical apply P3-07A and "
            "Engine admission P3-07E"
        )
    lor_digest = license_or_refusal.digest() if license_or_refusal is not None else None
    return TerminalReceipt(
        packet_id=packet_id,
        candidate_digest=candidate.digest(),
        obstruction_class=evaluation.classification,
        evidence_sha256=evaluation.evidence_sha256,
        terminal_status=evaluation.classification.value,
        license_or_refusal_digest=lor_digest,
        application_digest=None,
        license_consumed=False,
    )


__all__ = [
    "SCHEMA_VERSION",
    "CandidatePacket",
    "EvaluationReceipt",
    "VerificationReceipt",
    "RefusalReason",
    "LicenseRefusal",
    "ActionLicense",
    "ApplicationReceipt",
    "TerminalReceipt",
    "issue_action_license",
    "HostExecutor",
    "InMemoryHostExecutor",
    "build_terminal_receipt",
]
