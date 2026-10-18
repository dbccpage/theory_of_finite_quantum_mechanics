"""Strict value objects for prompt civilization and anti-skill evidence.

These objects provide deterministic wire contracts inside a trusted Python
process.  They are not a cryptographic trust boundary and never mint authority.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re
from typing import Any, cast, Mapping, TYPE_CHECKING, Tuple

from omega_engine.kernel.higher_operad.canonical import canonical_id

from omega_engine_pfp.domain import (
    MAX_CANDIDATE_BUDGET,
    MAX_OPERATION_BUDGET,
    MAX_STRING_LENGTH,
)


if TYPE_CHECKING:
    from .registry import AntiSkillRegistryV1


AUTHORITY_EFFECT_NONE = "None"
MAX_TEXT_BYTES = 128 * 1024
MAX_ITEMS = 256

_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@-]*$")


def sha256_ref(data: bytes) -> str:
    if type(data) is not bytes:
        raise TypeError("digest input must be exact bytes")
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _exact_dict(value: Any, label: str) -> dict[str, Any]:
    if type(value) is not dict or any(type(key) is not str for key in value):
        raise ValueError(f"{label} must be an exact string-keyed object")
    return cast(dict[str, Any], value)


def _fields(value: Mapping[str, Any], required: set[str], label: str) -> None:
    keys = set(value)
    missing = required - keys
    unknown = keys - required
    if missing:
        raise ValueError(f"{label} missing fields: {', '.join(sorted(missing))}")
    if unknown:
        raise ValueError(f"{label} unknown fields: {', '.join(sorted(unknown))}")


def _text(value: Any, label: str, *, allow_empty: bool = False) -> str:
    if type(value) is not str:
        raise ValueError(f"{label} must be an exact string")
    if len(value.encode("utf-8")) > MAX_TEXT_BYTES:
        raise ValueError(f"{label} exceeds the text limit")
    if not allow_empty and (not value or value.strip() != value):
        raise ValueError(f"{label} must be a nonempty normalized string")
    return value


def _identifier(value: Any, label: str) -> str:
    normalized = _text(value, label)
    if _IDENTIFIER.fullmatch(normalized) is None:
        raise ValueError(f"{label} must be a canonical identifier")
    return normalized


def _digest(value: Any, label: str) -> str:
    if type(value) is not str or _DIGEST.fullmatch(value) is None:
        raise ValueError(f"{label} must be a lowercase sha256: digest")
    return value


def _integer(
    value: Any,
    label: str,
    *,
    minimum: int = 0,
    maximum: int | None = None,
) -> int:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{label} must be an integer >= {minimum}")
    if maximum is not None and value > maximum:
        raise ValueError(f"{label} must be an integer <= {maximum}")
    return value


def _bool(value: Any, label: str) -> bool:
    if type(value) is not bool:
        raise ValueError(f"{label} must be an exact boolean")
    return value


def _string_tuple(
    value: Any,
    label: str,
    *,
    identifiers: bool = False,
    digests: bool = False,
    allow_empty_items: bool = False,
) -> tuple[str, ...]:
    if type(value) not in {list, tuple}:
        raise ValueError(f"{label} must be an array")
    if len(value) > MAX_ITEMS:
        raise ValueError(f"{label} exceeds the item limit")
    result: list[str] = []
    for index, item in enumerate(value):
        item_label = f"{label}[{index}]"
        if identifiers:
            result.append(_identifier(item, item_label))
        elif digests:
            result.append(_digest(item, item_label))
        else:
            result.append(_text(item, item_label, allow_empty=allow_empty_items))
    if len(result) != len(set(result)):
        raise ValueError(f"{label} must not contain duplicates")
    return tuple(result)


def _canonical_payload_id(domain: str, payload: Mapping[str, Any]) -> str:
    return cast(str, canonical_id(domain, dict(payload)))


@dataclass(frozen=True)
class CandidateAnnotationV1:
    failure_code: str = ""
    proposed_invariant: str = ""
    counterexamples: Tuple[str, ...] = ()
    protected_fields: Tuple[str, ...] = ()
    evidence_refs: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.failure_code:
            _identifier(self.failure_code, "failure_code")
        _text(self.proposed_invariant, "proposed_invariant", allow_empty=True)
        object.__setattr__(
            self, "counterexamples", _string_tuple(self.counterexamples, "counterexamples")
        )
        object.__setattr__(
            self,
            "protected_fields",
            _string_tuple(self.protected_fields, "protected_fields", identifiers=True),
        )
        object.__setattr__(
            self, "evidence_refs", _string_tuple(self.evidence_refs, "evidence_refs")
        )

    @property
    def is_complete(self) -> bool:
        return bool(
            self.failure_code
            and self.proposed_invariant
            and self.counterexamples
            and self.protected_fields
            and self.evidence_refs
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "failure_code": self.failure_code,
            "proposed_invariant": self.proposed_invariant,
            "counterexamples": list(self.counterexamples),
            "protected_fields": list(self.protected_fields),
            "evidence_refs": list(self.evidence_refs),
        }

    @classmethod
    def from_dict(cls, value: Any) -> "CandidateAnnotationV1":
        wire = _exact_dict(value, "candidate annotation")
        _fields(
            wire,
            {
                "failure_code",
                "proposed_invariant",
                "counterexamples",
                "protected_fields",
                "evidence_refs",
            },
            "candidate annotation",
        )
        return cls(
            failure_code=_text(wire["failure_code"], "failure_code", allow_empty=True),
            proposed_invariant=_text(
                wire["proposed_invariant"], "proposed_invariant", allow_empty=True
            ),
            counterexamples=_string_tuple(wire["counterexamples"], "counterexamples"),
            protected_fields=_string_tuple(
                wire["protected_fields"], "protected_fields", identifiers=True
            ),
            evidence_refs=_string_tuple(wire["evidence_refs"], "evidence_refs"),
        )


@dataclass(frozen=True)
class ConversationEpisodeV1:
    source_digest: str
    source_format: str
    ordinal: int
    user_label: str
    user_text: str
    assistant_label: str
    assistant_text: str
    session_id: str = ""
    task_id: str = ""
    model_id: str = ""
    annotation: CandidateAnnotationV1 = CandidateAnnotationV1()
    authority_effect: str = AUTHORITY_EFFECT_NONE
    schema_version: str = "omega.antiskill.conversation-episode.v1"
    episode_id: str = ""

    def __post_init__(self) -> None:
        _digest(self.source_digest, "source_digest")
        _identifier(self.source_format, "source_format")
        _integer(self.ordinal, "ordinal", minimum=1)
        _text(self.user_label, "user_label")
        _text(self.user_text, "user_text")
        _text(self.assistant_label, "assistant_label")
        _text(self.assistant_text, "assistant_text")
        for field, value in (
            ("session_id", self.session_id),
            ("task_id", self.task_id),
            ("model_id", self.model_id),
        ):
            _text(value, field, allow_empty=True)
        if not isinstance(self.annotation, CandidateAnnotationV1):
            raise TypeError("annotation must be CandidateAnnotationV1")
        if self.authority_effect != AUTHORITY_EFFECT_NONE:
            raise ValueError("conversation episode authority_effect must be None")
        if self.schema_version != "omega.antiskill.conversation-episode.v1":
            raise ValueError("unsupported conversation episode schema")
        expected = _canonical_payload_id(
            "omega.antiskill.conversation-episode.v1",
            self._payload(),
        )
        if self.episode_id and self.episode_id != expected:
            raise ValueError("episode_id does not match canonical content")
        object.__setattr__(self, "episode_id", expected)

    def _payload(self) -> dict[str, Any]:
        return {
            "source_digest": self.source_digest,
            "source_format": self.source_format,
            "ordinal": self.ordinal,
            "user_label": self.user_label,
            "user_text": self.user_text,
            "assistant_label": self.assistant_label,
            "assistant_text": self.assistant_text,
            "session_id": self.session_id,
            "task_id": self.task_id,
            "model_id": self.model_id,
            "annotation": self.annotation.to_dict(),
            "authority_effect": self.authority_effect,
            "schema_version": self.schema_version,
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "episode_id": self.episode_id}

    @classmethod
    def from_dict(cls, value: Any) -> "ConversationEpisodeV1":
        wire = _exact_dict(value, "conversation episode")
        _fields(
            wire,
            {
                "source_digest",
                "source_format",
                "ordinal",
                "user_label",
                "user_text",
                "assistant_label",
                "assistant_text",
                "session_id",
                "task_id",
                "model_id",
                "annotation",
                "authority_effect",
                "schema_version",
                "episode_id",
            },
            "conversation episode",
        )
        return cls(
            source_digest=_digest(wire["source_digest"], "source_digest"),
            source_format=_identifier(wire["source_format"], "source_format"),
            ordinal=_integer(wire["ordinal"], "ordinal", minimum=1),
            user_label=_text(wire["user_label"], "user_label"),
            user_text=_text(wire["user_text"], "user_text"),
            assistant_label=_text(wire["assistant_label"], "assistant_label"),
            assistant_text=_text(wire["assistant_text"], "assistant_text"),
            session_id=_text(wire["session_id"], "session_id", allow_empty=True),
            task_id=_text(wire["task_id"], "task_id", allow_empty=True),
            model_id=_text(wire["model_id"], "model_id", allow_empty=True),
            annotation=CandidateAnnotationV1.from_dict(wire["annotation"]),
            authority_effect=_text(wire["authority_effect"], "authority_effect"),
            schema_version=_text(wire["schema_version"], "schema_version"),
            episode_id=_digest(wire["episode_id"], "episode_id"),
        )


@dataclass(frozen=True)
class AntiSkillCandidateV1:
    name: str
    failure_code: str
    proposed_invariant: str
    episode_ids: Tuple[str, ...]
    context_keys: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    counterexamples: Tuple[str, ...]
    protected_fields: Tuple[str, ...]
    activation_kind: str = "human_review_required"
    status: str = "PROPOSED"
    authority_effect: str = AUTHORITY_EFFECT_NONE
    schema_version: str = "omega.antiskill.candidate.v1"
    candidate_id: str = ""

    def __post_init__(self) -> None:
        _identifier(self.name, "name")
        _identifier(self.failure_code, "failure_code")
        _text(self.proposed_invariant, "proposed_invariant")
        object.__setattr__(
            self, "episode_ids", _string_tuple(self.episode_ids, "episode_ids", digests=True)
        )
        object.__setattr__(
            self, "context_keys", _string_tuple(self.context_keys, "context_keys")
        )
        object.__setattr__(
            self, "evidence_refs", _string_tuple(self.evidence_refs, "evidence_refs")
        )
        object.__setattr__(
            self, "counterexamples", _string_tuple(self.counterexamples, "counterexamples")
        )
        object.__setattr__(
            self,
            "protected_fields",
            _string_tuple(self.protected_fields, "protected_fields", identifiers=True),
        )
        if (
            not self.episode_ids
            or not self.context_keys
            or not self.evidence_refs
            or not self.counterexamples
        ):
            raise ValueError("candidate requires episode, evidence, and counterexample data")
        if self.activation_kind != "human_review_required":
            raise ValueError("v0 candidates must require human review")
        if self.status != "PROPOSED":
            raise ValueError("candidate status must be PROPOSED")
        if self.authority_effect != AUTHORITY_EFFECT_NONE:
            raise ValueError("candidate authority_effect must be None")
        if self.schema_version != "omega.antiskill.candidate.v1":
            raise ValueError("unsupported anti-skill candidate schema")
        expected = _canonical_payload_id("omega.antiskill.candidate.v1", self._payload())
        if self.candidate_id and self.candidate_id != expected:
            raise ValueError("candidate_id does not match canonical content")
        object.__setattr__(self, "candidate_id", expected)

    def _payload(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "failure_code": self.failure_code,
            "proposed_invariant": self.proposed_invariant,
            "episode_ids": list(self.episode_ids),
            "context_keys": list(self.context_keys),
            "evidence_refs": list(self.evidence_refs),
            "counterexamples": list(self.counterexamples),
            "protected_fields": list(self.protected_fields),
            "activation_kind": self.activation_kind,
            "status": self.status,
            "authority_effect": self.authority_effect,
            "schema_version": self.schema_version,
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "candidate_id": self.candidate_id}

    @classmethod
    def from_dict(cls, value: Any) -> "AntiSkillCandidateV1":
        wire = _exact_dict(value, "anti-skill candidate")
        _fields(
            wire,
            {
                "name",
                "failure_code",
                "proposed_invariant",
                "episode_ids",
                "context_keys",
                "evidence_refs",
                "counterexamples",
                "protected_fields",
                "activation_kind",
                "status",
                "authority_effect",
                "schema_version",
                "candidate_id",
            },
            "anti-skill candidate",
        )
        return cls(
            name=_identifier(wire["name"], "name"),
            failure_code=_identifier(wire["failure_code"], "failure_code"),
            proposed_invariant=_text(wire["proposed_invariant"], "proposed_invariant"),
            episode_ids=_string_tuple(wire["episode_ids"], "episode_ids", digests=True),
            context_keys=_string_tuple(wire["context_keys"], "context_keys"),
            evidence_refs=_string_tuple(wire["evidence_refs"], "evidence_refs"),
            counterexamples=_string_tuple(wire["counterexamples"], "counterexamples"),
            protected_fields=_string_tuple(
                wire["protected_fields"], "protected_fields", identifiers=True
            ),
            activation_kind=_identifier(wire["activation_kind"], "activation_kind"),
            status=_identifier(wire["status"], "status"),
            authority_effect=_text(wire["authority_effect"], "authority_effect"),
            schema_version=_identifier(wire["schema_version"], "schema_version"),
            candidate_id=_digest(wire["candidate_id"], "candidate_id"),
        )


ALLOWED_DETECTORS = frozenset(
    {
        "requires_field",
        "requires_evidence_for_claim_mode",
        "requires_nonclaim",
        "requires_operator_approval",
    }
)
ALLOWED_REPAIRS = frozenset(
    {
        "add_evidence_request",
        "add_nonclaim",
        "populate_typed_field",
        "request_operator_approval",
        "finding_only",
    }
)


@dataclass(frozen=True)
class AntiSkillSpecV1:
    spec_id: str
    version: int
    failure_code: str
    detector_kind: str
    activation_fields: Tuple[str, ...]
    repair_kind: str
    protected_fields: Tuple[str, ...]
    episode_ids: Tuple[str, ...]
    context_keys: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    counterexamples: Tuple[str, ...]
    evaluation_receipt_ref: str
    composition_order: int | None = None
    commutes_with: Tuple[str, ...] = ()
    authority_effect: str = AUTHORITY_EFFECT_NONE
    schema_version: str = "omega.antiskill.spec.v1"
    spec_digest: str = ""

    def __post_init__(self) -> None:
        _identifier(self.spec_id, "spec_id")
        _integer(self.version, "version", minimum=1)
        _identifier(self.failure_code, "failure_code")
        if self.detector_kind not in ALLOWED_DETECTORS:
            raise ValueError("detector_kind is not admitted")
        if self.repair_kind not in ALLOWED_REPAIRS:
            raise ValueError("repair_kind is not admitted")
        object.__setattr__(
            self,
            "activation_fields",
            _string_tuple(self.activation_fields, "activation_fields", identifiers=True),
        )
        object.__setattr__(
            self,
            "protected_fields",
            _string_tuple(self.protected_fields, "protected_fields", identifiers=True),
        )
        object.__setattr__(
            self, "episode_ids", _string_tuple(self.episode_ids, "episode_ids", digests=True)
        )
        object.__setattr__(
            self, "context_keys", _string_tuple(self.context_keys, "context_keys")
        )
        object.__setattr__(
            self, "evidence_refs", _string_tuple(self.evidence_refs, "evidence_refs")
        )
        object.__setattr__(
            self, "counterexamples", _string_tuple(self.counterexamples, "counterexamples")
        )
        _digest(self.evaluation_receipt_ref, "evaluation_receipt_ref")
        if len(set(self.episode_ids)) < 2:
            raise ValueError("admission requires at least two distinct episode ids")
        if len(set(self.context_keys)) < 2:
            raise ValueError("admission requires at least two independent contexts")
        if not self.activation_fields or not self.evidence_refs or not self.counterexamples:
            raise ValueError("admitted spec lacks activation, evidence, or counterexamples")
        if self.composition_order is not None:
            _integer(self.composition_order, "composition_order", minimum=0)
        object.__setattr__(
            self,
            "commutes_with",
            _string_tuple(self.commutes_with, "commutes_with", identifiers=True),
        )
        if self.authority_effect != AUTHORITY_EFFECT_NONE:
            raise ValueError("anti-skill spec authority_effect must be None")
        if self.schema_version != "omega.antiskill.spec.v1":
            raise ValueError("unsupported anti-skill spec schema")
        expected = _canonical_payload_id("omega.antiskill.spec.v1", self._payload())
        if self.spec_digest and self.spec_digest != expected:
            raise ValueError("spec_digest does not match canonical content")
        object.__setattr__(self, "spec_digest", expected)

    def _payload(self) -> dict[str, Any]:
        return {
            "spec_id": self.spec_id,
            "version": self.version,
            "failure_code": self.failure_code,
            "detector_kind": self.detector_kind,
            "activation_fields": list(self.activation_fields),
            "repair_kind": self.repair_kind,
            "protected_fields": list(self.protected_fields),
            "episode_ids": list(self.episode_ids),
            "context_keys": list(self.context_keys),
            "evidence_refs": list(self.evidence_refs),
            "counterexamples": list(self.counterexamples),
            "evaluation_receipt_ref": self.evaluation_receipt_ref,
            "composition_order": self.composition_order,
            "commutes_with": list(self.commutes_with),
            "authority_effect": self.authority_effect,
            "schema_version": self.schema_version,
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "spec_digest": self.spec_digest}

    @classmethod
    def from_dict(cls, value: Any) -> "AntiSkillSpecV1":
        wire = _exact_dict(value, "anti-skill spec")
        required = {
            "spec_id",
            "version",
            "failure_code",
            "detector_kind",
            "activation_fields",
            "repair_kind",
            "protected_fields",
            "episode_ids",
            "context_keys",
            "evidence_refs",
            "counterexamples",
            "evaluation_receipt_ref",
            "composition_order",
            "commutes_with",
            "authority_effect",
            "schema_version",
            "spec_digest",
        }
        _fields(wire, required, "anti-skill spec")
        order = wire["composition_order"]
        if order is not None:
            order = _integer(order, "composition_order", minimum=0)
        return cls(
            spec_id=_identifier(wire["spec_id"], "spec_id"),
            version=_integer(wire["version"], "version", minimum=1),
            failure_code=_identifier(wire["failure_code"], "failure_code"),
            detector_kind=_identifier(wire["detector_kind"], "detector_kind"),
            activation_fields=_string_tuple(
                wire["activation_fields"], "activation_fields", identifiers=True
            ),
            repair_kind=_identifier(wire["repair_kind"], "repair_kind"),
            protected_fields=_string_tuple(
                wire["protected_fields"], "protected_fields", identifiers=True
            ),
            episode_ids=_string_tuple(wire["episode_ids"], "episode_ids", digests=True),
            context_keys=_string_tuple(wire["context_keys"], "context_keys"),
            evidence_refs=_string_tuple(wire["evidence_refs"], "evidence_refs"),
            counterexamples=_string_tuple(wire["counterexamples"], "counterexamples"),
            evaluation_receipt_ref=_digest(
                wire["evaluation_receipt_ref"], "evaluation_receipt_ref"
            ),
            composition_order=order,
            commutes_with=_string_tuple(
                wire["commutes_with"], "commutes_with", identifiers=True
            ),
            authority_effect=_text(wire["authority_effect"], "authority_effect"),
            schema_version=_identifier(wire["schema_version"], "schema_version"),
            spec_digest=_digest(wire["spec_digest"], "spec_digest"),
        )


@dataclass(frozen=True)
class PromptFindingV1:
    code: str
    severity: str
    field: str
    message: str
    repair_hint: str
    detector_ref: str
    authority_effect: str = AUTHORITY_EFFECT_NONE
    schema_version: str = "omega.prompt.finding.v1"
    finding_id: str = ""

    def __post_init__(self) -> None:
        _identifier(self.code, "code")
        if self.severity not in {"ERROR", "WARNING", "INFO"}:
            raise ValueError("invalid finding severity")
        _identifier(self.field, "field")
        _text(self.message, "message")
        _text(self.repair_hint, "repair_hint")
        _identifier(self.detector_ref, "detector_ref")
        if self.authority_effect != AUTHORITY_EFFECT_NONE:
            raise ValueError("finding authority_effect must be None")
        if self.schema_version != "omega.prompt.finding.v1":
            raise ValueError("unsupported prompt finding schema")
        expected = _canonical_payload_id("omega.prompt.finding.v1", self._payload())
        if self.finding_id and self.finding_id != expected:
            raise ValueError("finding_id does not match canonical content")
        object.__setattr__(self, "finding_id", expected)

    def _payload(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "severity": self.severity,
            "field": self.field,
            "message": self.message,
            "repair_hint": self.repair_hint,
            "detector_ref": self.detector_ref,
            "authority_effect": self.authority_effect,
            "schema_version": self.schema_version,
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "finding_id": self.finding_id}

    @classmethod
    def from_dict(cls, value: Any) -> "PromptFindingV1":
        wire = _exact_dict(value, "prompt finding")
        _fields(
            wire,
            {
                "code",
                "severity",
                "field",
                "message",
                "repair_hint",
                "detector_ref",
                "authority_effect",
                "schema_version",
                "finding_id",
            },
            "prompt finding",
        )
        return cls(
            code=_identifier(wire["code"], "code"),
            severity=_identifier(wire["severity"], "severity"),
            field=_identifier(wire["field"], "field"),
            message=_text(wire["message"], "message"),
            repair_hint=_text(wire["repair_hint"], "repair_hint"),
            detector_ref=_identifier(wire["detector_ref"], "detector_ref"),
            authority_effect=_text(wire["authority_effect"], "authority_effect"),
            schema_version=_identifier(wire["schema_version"], "schema_version"),
            finding_id=_digest(wire["finding_id"], "finding_id"),
        )


PROMPT_FIELDS = (
    "in_scope",
    "out_of_scope",
    "inputs",
    "constraints",
    "acceptance_criteria",
    "evidence_requirements",
    "requested_effects",
    "nonclaims",
    "unresolved_questions",
)


@dataclass(frozen=True)
class TypedPromptV1:
    original_text: str
    source_digest: str
    objective: str
    claim_mode: str
    in_scope: Tuple[str, ...]
    out_of_scope: Tuple[str, ...]
    inputs: Tuple[str, ...]
    constraints: Tuple[str, ...]
    acceptance_criteria: Tuple[str, ...]
    evidence_requirements: Tuple[str, ...]
    requested_effects: Tuple[str, ...]
    candidate_budget: int
    operation_budget: int
    nonclaims: Tuple[str, ...]
    unresolved_questions: Tuple[str, ...]
    proposed_prompt: str
    authority_effect: str = AUTHORITY_EFFECT_NONE
    schema_version: str = "omega.prompt.typed.v1"
    prompt_id: str = ""

    def __post_init__(self) -> None:
        _text(self.original_text, "original_text", allow_empty=True)
        if sha256_ref(self.original_text.encode("utf-8")) != self.source_digest:
            raise ValueError("source_digest does not bind original_text bytes")
        _text(self.objective, "objective", allow_empty=True)
        if len(self.objective.encode("utf-8")) > MAX_STRING_LENGTH:
            raise ValueError("objective exceeds the downstream string limit")
        if self.claim_mode not in {"none", "investigate", "verify", "prove"}:
            raise ValueError("claim_mode is unsupported")
        for field in PROMPT_FIELDS:
            object.__setattr__(self, field, _string_tuple(getattr(self, field), field))
        _integer(
            self.candidate_budget,
            "candidate_budget",
            minimum=1,
            maximum=MAX_CANDIDATE_BUDGET,
        )
        _integer(
            self.operation_budget,
            "operation_budget",
            minimum=1,
            maximum=MAX_OPERATION_BUDGET,
        )
        _text(self.proposed_prompt, "proposed_prompt", allow_empty=True)
        if self.authority_effect != AUTHORITY_EFFECT_NONE:
            raise ValueError("typed prompt authority_effect must be None")
        if self.schema_version != "omega.prompt.typed.v1":
            raise ValueError("unsupported typed prompt schema")
        expected = _canonical_payload_id("omega.prompt.typed.v1", self._payload())
        if self.prompt_id and self.prompt_id != expected:
            raise ValueError("prompt_id does not match canonical content")
        object.__setattr__(self, "prompt_id", expected)

    def _payload(self) -> dict[str, Any]:
        payload = {
            "original_text": self.original_text,
            "source_digest": self.source_digest,
            "objective": self.objective,
            "claim_mode": self.claim_mode,
            "candidate_budget": self.candidate_budget,
            "operation_budget": self.operation_budget,
            "proposed_prompt": self.proposed_prompt,
            "authority_effect": self.authority_effect,
            "schema_version": self.schema_version,
        }
        payload.update({field: list(getattr(self, field)) for field in PROMPT_FIELDS})
        return payload

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "prompt_id": self.prompt_id}

    @classmethod
    def from_dict(cls, value: Any) -> "TypedPromptV1":
        wire = _exact_dict(value, "typed prompt")
        required = {
            "original_text",
            "source_digest",
            "objective",
            "claim_mode",
            "candidate_budget",
            "operation_budget",
            "proposed_prompt",
            "authority_effect",
            "schema_version",
            "prompt_id",
            *PROMPT_FIELDS,
        }
        _fields(wire, required, "typed prompt")
        return cls(
            original_text=_text(wire["original_text"], "original_text", allow_empty=True),
            source_digest=_digest(wire["source_digest"], "source_digest"),
            objective=_text(wire["objective"], "objective", allow_empty=True),
            claim_mode=_identifier(wire["claim_mode"], "claim_mode"),
            in_scope=_string_tuple(wire["in_scope"], "in_scope"),
            out_of_scope=_string_tuple(wire["out_of_scope"], "out_of_scope"),
            inputs=_string_tuple(wire["inputs"], "inputs"),
            constraints=_string_tuple(wire["constraints"], "constraints"),
            acceptance_criteria=_string_tuple(
                wire["acceptance_criteria"], "acceptance_criteria"
            ),
            evidence_requirements=_string_tuple(
                wire["evidence_requirements"], "evidence_requirements"
            ),
            requested_effects=_string_tuple(wire["requested_effects"], "requested_effects"),
            candidate_budget=_integer(
                wire["candidate_budget"],
                "candidate_budget",
                minimum=1,
                maximum=MAX_CANDIDATE_BUDGET,
            ),
            operation_budget=_integer(
                wire["operation_budget"],
                "operation_budget",
                minimum=1,
                maximum=MAX_OPERATION_BUDGET,
            ),
            nonclaims=_string_tuple(wire["nonclaims"], "nonclaims"),
            unresolved_questions=_string_tuple(
                wire["unresolved_questions"], "unresolved_questions"
            ),
            proposed_prompt=_text(
                wire["proposed_prompt"], "proposed_prompt", allow_empty=True
            ),
            authority_effect=_text(wire["authority_effect"], "authority_effect"),
            schema_version=_identifier(wire["schema_version"], "schema_version"),
            prompt_id=_digest(wire["prompt_id"], "prompt_id"),
        )


@dataclass(frozen=True)
class PromptReviewReceiptV1:
    source_digest: str
    prompt_id: str
    registry_id: str
    policy_digest: str
    implementation_digest: str
    finding_ids: Tuple[str, ...]
    outcome: str
    protected_fields_ok: bool
    authority_effect: str = AUTHORITY_EFFECT_NONE
    schema_version: str = "omega.prompt.review-receipt.v1"
    receipt_id: str = ""

    def __post_init__(self) -> None:
        for field in (
            "source_digest",
            "prompt_id",
            "registry_id",
            "policy_digest",
            "implementation_digest",
        ):
            _digest(getattr(self, field), field)
        object.__setattr__(
            self,
            "finding_ids",
            _string_tuple(self.finding_ids, "finding_ids", digests=True),
        )
        if self.outcome not in {"READY_FOR_OPERATOR_REVIEW", "NEEDS_CLARIFICATION"}:
            raise ValueError("unsupported review outcome")
        _bool(self.protected_fields_ok, "protected_fields_ok")
        if self.authority_effect != AUTHORITY_EFFECT_NONE:
            raise ValueError("review receipt authority_effect must be None")
        if self.schema_version != "omega.prompt.review-receipt.v1":
            raise ValueError("unsupported prompt review receipt schema")
        expected = _canonical_payload_id("omega.prompt.review-receipt.v1", self._payload())
        if self.receipt_id and self.receipt_id != expected:
            raise ValueError("receipt_id does not match canonical content")
        object.__setattr__(self, "receipt_id", expected)

    def _payload(self) -> dict[str, Any]:
        return {
            "source_digest": self.source_digest,
            "prompt_id": self.prompt_id,
            "registry_id": self.registry_id,
            "policy_digest": self.policy_digest,
            "implementation_digest": self.implementation_digest,
            "finding_ids": list(self.finding_ids),
            "outcome": self.outcome,
            "protected_fields_ok": self.protected_fields_ok,
            "authority_effect": self.authority_effect,
            "schema_version": self.schema_version,
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "receipt_id": self.receipt_id}

    @classmethod
    def from_dict(cls, value: Any) -> "PromptReviewReceiptV1":
        wire = _exact_dict(value, "prompt review receipt")
        _fields(
            wire,
            {
                "source_digest",
                "prompt_id",
                "registry_id",
                "policy_digest",
                "implementation_digest",
                "finding_ids",
                "outcome",
                "protected_fields_ok",
                "authority_effect",
                "schema_version",
                "receipt_id",
            },
            "prompt review receipt",
        )
        return cls(
            source_digest=_digest(wire["source_digest"], "source_digest"),
            prompt_id=_digest(wire["prompt_id"], "prompt_id"),
            registry_id=_digest(wire["registry_id"], "registry_id"),
            policy_digest=_digest(wire["policy_digest"], "policy_digest"),
            implementation_digest=_digest(
                wire["implementation_digest"], "implementation_digest"
            ),
            finding_ids=_string_tuple(wire["finding_ids"], "finding_ids", digests=True),
            outcome=_identifier(wire["outcome"], "outcome"),
            protected_fields_ok=_bool(wire["protected_fields_ok"], "protected_fields_ok"),
            authority_effect=_text(wire["authority_effect"], "authority_effect"),
            schema_version=_identifier(wire["schema_version"], "schema_version"),
            receipt_id=_digest(wire["receipt_id"], "receipt_id"),
        )


@dataclass(frozen=True)
class PromptReviewBundleV1:
    prompt: TypedPromptV1
    findings: Tuple[PromptFindingV1, ...]
    receipt: PromptReviewReceiptV1
    registry: "AntiSkillRegistryV1"
    schema_version: str = "omega.prompt.review-bundle.v1"

    def __post_init__(self) -> None:
        if not isinstance(self.prompt, TypedPromptV1):
            raise TypeError("prompt must be TypedPromptV1")
        findings = tuple(self.findings)
        if any(not isinstance(item, PromptFindingV1) for item in findings):
            raise TypeError("findings must contain PromptFindingV1")
        object.__setattr__(self, "findings", findings)
        if not isinstance(self.receipt, PromptReviewReceiptV1):
            raise TypeError("receipt must be PromptReviewReceiptV1")
        from .registry import AntiSkillRegistryV1

        if not isinstance(self.registry, AntiSkillRegistryV1):
            raise TypeError("registry must be AntiSkillRegistryV1")
        if self.schema_version != "omega.prompt.review-bundle.v1":
            raise ValueError("unsupported prompt review bundle schema")
        if self.receipt.prompt_id != self.prompt.prompt_id:
            raise ValueError("review receipt prompt binding mismatch")
        if self.receipt.registry_id != self.registry.registry_id:
            raise ValueError("review receipt registry binding mismatch")
        if tuple(item.finding_id for item in self.findings) != self.receipt.finding_ids:
            raise ValueError("review receipt finding binding mismatch")

    def to_dict(self) -> dict[str, Any]:
        return {
            "prompt": self.prompt.to_dict(),
            "findings": [item.to_dict() for item in self.findings],
            "receipt": self.receipt.to_dict(),
            "registry": self.registry.to_dict(),
            "schema_version": self.schema_version,
        }

    @classmethod
    def from_dict(cls, value: Any) -> "PromptReviewBundleV1":
        wire = _exact_dict(value, "prompt review bundle")
        _fields(
            wire,
            {"prompt", "findings", "receipt", "registry", "schema_version"},
            "prompt review bundle",
        )
        if type(wire["findings"]) is not list:
            raise ValueError("findings must be an array")
        schema = _identifier(wire["schema_version"], "schema_version")
        if schema != "omega.prompt.review-bundle.v1":
            raise ValueError("unsupported prompt review bundle schema")
        from .registry import AntiSkillRegistryV1

        return cls(
            prompt=TypedPromptV1.from_dict(wire["prompt"]),
            findings=tuple(PromptFindingV1.from_dict(item) for item in wire["findings"]),
            receipt=PromptReviewReceiptV1.from_dict(wire["receipt"]),
            registry=AntiSkillRegistryV1.from_dict(wire["registry"]),
            schema_version=schema,
        )


@dataclass(frozen=True)
class ApprovedPromptV1:
    prompt_id: str
    review_receipt_id: str
    approved_by: str
    objective: str
    claim_mode: str
    rendered_prompt: str
    rendered_digest: str
    candidate_budget: int
    operation_budget: int
    requested_effects: Tuple[str, ...]
    authority_effect: str = AUTHORITY_EFFECT_NONE
    schema_version: str = "omega.prompt.approved.v1"
    approved_prompt_id: str = ""

    def __post_init__(self) -> None:
        _digest(self.prompt_id, "prompt_id")
        _digest(self.review_receipt_id, "review_receipt_id")
        _identifier(self.approved_by, "approved_by")
        _text(self.objective, "objective")
        if len(self.objective.encode("utf-8")) > MAX_STRING_LENGTH:
            raise ValueError("objective exceeds the downstream string limit")
        if self.claim_mode not in {"none", "investigate", "verify", "prove"}:
            raise ValueError("claim_mode is unsupported")
        _text(self.rendered_prompt, "rendered_prompt", allow_empty=True)
        if not self.rendered_prompt:
            raise ValueError("rendered_prompt must not be empty")
        if sha256_ref(self.rendered_prompt.encode("utf-8")) != self.rendered_digest:
            raise ValueError("rendered_digest does not bind rendered_prompt")
        _integer(
            self.candidate_budget,
            "candidate_budget",
            minimum=1,
            maximum=MAX_CANDIDATE_BUDGET,
        )
        _integer(
            self.operation_budget,
            "operation_budget",
            minimum=1,
            maximum=MAX_OPERATION_BUDGET,
        )
        object.__setattr__(
            self,
            "requested_effects",
            _string_tuple(self.requested_effects, "requested_effects"),
        )
        if self.authority_effect != AUTHORITY_EFFECT_NONE:
            raise ValueError("approved prompt authority_effect must be None")
        if self.schema_version != "omega.prompt.approved.v1":
            raise ValueError("unsupported approved prompt schema")
        expected = _canonical_payload_id("omega.prompt.approved.v1", self._payload())
        if self.approved_prompt_id and self.approved_prompt_id != expected:
            raise ValueError("approved_prompt_id does not match canonical content")
        object.__setattr__(self, "approved_prompt_id", expected)

    def _payload(self) -> dict[str, Any]:
        return {
            "prompt_id": self.prompt_id,
            "review_receipt_id": self.review_receipt_id,
            "approved_by": self.approved_by,
            "objective": self.objective,
            "claim_mode": self.claim_mode,
            "rendered_prompt": self.rendered_prompt,
            "rendered_digest": self.rendered_digest,
            "candidate_budget": self.candidate_budget,
            "operation_budget": self.operation_budget,
            "requested_effects": list(self.requested_effects),
            "authority_effect": self.authority_effect,
            "schema_version": self.schema_version,
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "approved_prompt_id": self.approved_prompt_id}

    @classmethod
    def from_dict(cls, value: Any) -> "ApprovedPromptV1":
        wire = _exact_dict(value, "approved prompt")
        _fields(
            wire,
            {
                "prompt_id",
                "review_receipt_id",
                "approved_by",
                "objective",
                "claim_mode",
                "rendered_prompt",
                "rendered_digest",
                "candidate_budget",
                "operation_budget",
                "requested_effects",
                "authority_effect",
                "schema_version",
                "approved_prompt_id",
            },
            "approved prompt",
        )
        return cls(
            prompt_id=_digest(wire["prompt_id"], "prompt_id"),
            review_receipt_id=_digest(wire["review_receipt_id"], "review_receipt_id"),
            approved_by=_identifier(wire["approved_by"], "approved_by"),
            objective=_text(wire["objective"], "objective"),
            claim_mode=_identifier(wire["claim_mode"], "claim_mode"),
            rendered_prompt=_text(
                wire["rendered_prompt"], "rendered_prompt", allow_empty=True
            ),
            rendered_digest=_digest(wire["rendered_digest"], "rendered_digest"),
            candidate_budget=_integer(
                wire["candidate_budget"],
                "candidate_budget",
                minimum=1,
                maximum=MAX_CANDIDATE_BUDGET,
            ),
            operation_budget=_integer(
                wire["operation_budget"],
                "operation_budget",
                minimum=1,
                maximum=MAX_OPERATION_BUDGET,
            ),
            requested_effects=_string_tuple(wire["requested_effects"], "requested_effects"),
            authority_effect=_text(wire["authority_effect"], "authority_effect"),
            schema_version=_identifier(wire["schema_version"], "schema_version"),
            approved_prompt_id=_digest(wire["approved_prompt_id"], "approved_prompt_id"),
        )


__all__ = [
    "ALLOWED_DETECTORS",
    "ALLOWED_REPAIRS",
    "AUTHORITY_EFFECT_NONE",
    "AntiSkillCandidateV1",
    "AntiSkillSpecV1",
    "ApprovedPromptV1",
    "CandidateAnnotationV1",
    "ConversationEpisodeV1",
    "PromptFindingV1",
    "PromptReviewBundleV1",
    "PromptReviewReceiptV1",
    "TypedPromptV1",
    "sha256_ref",
]
