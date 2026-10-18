"""Deterministic review, operator approval, and Symbol Game packetization use cases.

AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Mapping, Sequence

from omega_engine.kernel.higher_operad.canonical import canonical_id
from omega_engine_operations.domain.rop.result import Err, Ok, Refusal, Result
from omega_engine_pfp.domain import (
    build_llm_turn_envelope,
    build_payload_from_content,
)
from omega_engine_pfp.domain.entities.packet_envelope import PacketEnvelopeV2


from ..domain.constants import AUTHORITY_EFFECT_NONE, MAX_TEXT_BYTES
from ..domain.models import (
    AntiSkillRegistryV1,
    ApprovedPromptV1,
    PromptFindingV1,
    PromptReviewBundleV1,
    PromptReviewReceiptV1,
    TypedPromptV1,
    sha256_ref,
)


PROMPT_PROPOSAL_FIELDS = frozenset(
    {
        "objective",
        "claim_mode",
        "in_scope",
        "out_of_scope",
        "inputs",
        "constraints",
        "acceptance_criteria",
        "evidence_requirements",
        "requested_effects",
        "candidate_budget",
        "operation_budget",
        "nonclaims",
        "unresolved_questions",
        "proposed_prompt",
    }
)

CORE_POLICY = {
    "version": "omega.prompt-review.policy.v1",
    "authority_effect": AUTHORITY_EFFECT_NONE,
    "rules": (
        "objective_required",
        "acceptance_required_for_effects",
        "evidence_required_for_verify_or_prove",
        "external_effects_require_resolved_questions",
        "operator_approval_always_required",
        "original_bytes_immutable",
        "model_verdicts_untrusted",
    ),
}
POLICY_DIGEST = canonical_id("omega.prompt-review.policy.v1", CORE_POLICY)


def review_implementation_digest() -> str:
    digest = hashlib.sha256()
    root = Path(__file__).resolve().parents[1]
    repo_root = root
    for p in [root] + list(root.parents):
        if (p / "omega_engine_pfp").exists():
            repo_root = p
            break

    symbol_game = repo_root / "omega_engine_pfp"
    canonical_path = symbol_game / "domain" / "shared_kernel" / "canonical.py"
    llm_turn_path = symbol_game / "use_cases" / "llm_turn.py"
    packets_path = symbol_game / "domain" / "entities" / "packet_envelope.py"

    paths = (
        root / "infrastructure" / "json_wire.py",
        root / "domain" / "models.py",
        root / "infrastructure" / "registry.py",
        root / "use_cases" / "review.py",
        canonical_path,
        llm_turn_path,
        packets_path,
    )
    for path in paths:
        relative = path.relative_to(repo_root).as_posix()
        raw = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(raw).digest())
    return "sha256:" + digest.hexdigest()


def _exact_proposal(value: Any) -> dict[str, Any]:
    if type(value) is not dict:
        raise ValueError("prompt proposal must be an exact object")
    missing = PROMPT_PROPOSAL_FIELDS - set(value)
    unknown = set(value) - PROMPT_PROPOSAL_FIELDS
    if missing:
        raise ValueError("prompt proposal missing fields: " + ", ".join(sorted(missing)))
    if unknown:
        raise ValueError("prompt proposal unknown fields: " + ", ".join(sorted(unknown)))
    return value


def _array(value: Any, label: str) -> tuple[str, ...]:
    if type(value) is not list or any(type(item) is not str for item in value):
        raise ValueError(f"{label} must be an array of exact strings")
    if any(not item or item.strip() != item for item in value):
        raise ValueError(f"{label} items must be nonempty normalized strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{label} must not contain duplicates")
    return tuple(value)


def build_typed_prompt(
    original: bytes,
    proposal: Mapping[str, Any],
) -> Result[TypedPromptV1, Refusal]:
    """Bind an untrusted structural proposal to immutable original bytes."""

    try:
        if type(original) is not bytes:
            raise TypeError("original must be exact bytes")
        original_text = original.decode("utf-8", errors="strict")
        wire = _exact_proposal(proposal)
        candidate_budget = wire["candidate_budget"]
        operation_budget = wire["operation_budget"]
        if type(candidate_budget) is not int or candidate_budget < 1:
            raise ValueError("candidate_budget must be a positive integer")
        if type(operation_budget) is not int or operation_budget < 1:
            raise ValueError("operation_budget must be a positive integer")
        for field in ("objective", "claim_mode", "proposed_prompt"):
            if type(wire[field]) is not str:
                raise ValueError(f"{field} must be an exact string")
        prompt = TypedPromptV1(
            original_text=original_text,
            source_digest=sha256_ref(original),
            objective=wire["objective"],
            claim_mode=wire["claim_mode"],
            in_scope=_array(wire["in_scope"], "in_scope"),
            out_of_scope=_array(wire["out_of_scope"], "out_of_scope"),
            inputs=_array(wire["inputs"], "inputs"),
            constraints=_array(wire["constraints"], "constraints"),
            acceptance_criteria=_array(
                wire["acceptance_criteria"], "acceptance_criteria"
            ),
            evidence_requirements=_array(
                wire["evidence_requirements"], "evidence_requirements"
            ),
            requested_effects=_array(wire["requested_effects"], "requested_effects"),
            candidate_budget=candidate_budget,
            operation_budget=operation_budget,
            nonclaims=_array(wire["nonclaims"], "nonclaims"),
            unresolved_questions=_array(
                wire["unresolved_questions"], "unresolved_questions"
            ),
            proposed_prompt=wire["proposed_prompt"],
        )
        return Ok(prompt)
    except (TypeError, UnicodeDecodeError, ValueError) as exc:
        return Err(
            Refusal(
                code="INVALID_PROMPT_PROPOSAL",
                message=str(exc),
                locus="prompt-proposal",
            )
        )


def _finding(
    code: str,
    severity: str,
    field: str,
    message: str,
    repair_hint: str,
    detector_ref: str = "omega-prompt-core-v1",
) -> PromptFindingV1:
    return PromptFindingV1(
        code=code,
        severity=severity,
        field=field,
        message=message,
        repair_hint=repair_hint,
        detector_ref=detector_ref,
    )


def _core_findings(prompt: TypedPromptV1) -> list[PromptFindingV1]:
    findings: list[PromptFindingV1] = []
    if not prompt.objective.strip():
        findings.append(
            _finding(
                "MISSING_OBJECTIVE",
                "ERROR",
                "objective",
                "The typed interpretation has no declared objective.",
                "Declare one bounded outcome without changing the original prompt.",
            )
        )
    if prompt.requested_effects and not prompt.acceptance_criteria:
        findings.append(
            _finding(
                "MISSING_ACCEPTANCE_CRITERIA",
                "ERROR",
                "acceptance_criteria",
                "A consequential prompt has no explicit acceptance criteria.",
                "Add replayable criteria for every requested effect.",
            )
        )
    if prompt.claim_mode in {"verify", "prove"} and not prompt.evidence_requirements:
        findings.append(
            _finding(
                "MISSING_EVIDENCE_REQUIREMENTS",
                "ERROR",
                "evidence_requirements",
                "Verify/prove mode has no declared evidence boundary.",
                "Name the checker, source, replay, or theorem evidence required.",
            )
        )
    if prompt.requested_effects and prompt.unresolved_questions:
        findings.append(
            _finding(
                "UNRESOLVED_CONSEQUENTIAL_AMBIGUITY",
                "ERROR",
                "unresolved_questions",
                "Consequential effects remain requested while material questions are open.",
                "Resolve the questions or remove the effects from this prompt.",
            )
        )
    if not prompt.proposed_prompt.strip():
        findings.append(
            _finding(
                "MISSING_TYPED_REWRITE",
                "ERROR",
                "proposed_prompt",
                "No candidate prompt was supplied for operator review.",
                "Propose a rewrite while preserving all structured fields.",
            )
        )
    try:
        render_typed_prompt(prompt)
    except ValueError as exc:
        findings.append(
            _finding(
                "RENDERED_PROMPT_RESOURCE_LIMIT",
                "ERROR",
                "proposed_prompt",
                str(exc),
                f"Reduce the rendered prompt to at most {MAX_TEXT_BYTES} UTF-8 bytes.",
            )
        )
    findings.append(
        _finding(
            "OPERATOR_APPROVAL_REQUIRED",
            "INFO",
            "authority_effect",
            "The deterministic review cannot authorize or send this prompt.",
            "Present the review bundle to an operator for an explicit decision.",
        )
    )
    return findings


def _field_value(prompt: TypedPromptV1, field: str) -> Any:
    if not hasattr(prompt, field):
        raise ValueError(f"anti-skill references unknown prompt field: {field}")
    return getattr(prompt, field)


def _registry_findings(
    prompt: TypedPromptV1,
    registry: AntiSkillRegistryV1,
) -> list[PromptFindingV1]:
    findings: list[PromptFindingV1] = []
    for spec in registry.specs:
        triggered_fields: list[str] = []
        if spec.detector_kind == "requires_field":
            triggered_fields = [
                field for field in spec.activation_fields if not _field_value(prompt, field)
            ]
        elif spec.detector_kind == "requires_evidence_for_claim_mode":
            if prompt.claim_mode in {"verify", "prove"} and not prompt.evidence_requirements:
                triggered_fields = ["evidence_requirements"]
        elif spec.detector_kind == "requires_nonclaim":
            if not prompt.nonclaims:
                triggered_fields = ["nonclaims"]
        elif spec.detector_kind == "requires_operator_approval":
            triggered_fields = ["authority_effect"]
        for field in triggered_fields:
            findings.append(
                _finding(
                    spec.failure_code,
                    "WARNING" if spec.repair_kind == "finding_only" else "ERROR",
                    field,
                    f"Admitted anti-skill {spec.spec_id} detected a structural omission.",
                    f"Apply declared repair kind {spec.repair_kind} and re-review.",
                    detector_ref=spec.spec_id,
                )
            )
    return findings


def review_prompt(
    original: bytes,
    proposed_structure: TypedPromptV1 | Mapping[str, Any],
    registry: AntiSkillRegistryV1,
) -> Result[PromptReviewBundleV1, Refusal]:
    """Review structure and evidence boundaries without deciding truth."""

    try:
        if type(original) is not bytes:
            raise TypeError("original must be exact bytes")
        validated_registry = AntiSkillRegistryV1.from_dict(registry.to_dict())
        if validated_registry.specs:
            return Err(
                Refusal(
                    code="ANTISKILL_ADMISSION_UNVERIFIED",
                    message=(
                        "v0 refuses nonempty anti-skill registries until an "
                        "external admission validator is available"
                    ),
                    locus="registry",
                )
            )
        if isinstance(proposed_structure, TypedPromptV1):
            prompt = TypedPromptV1.from_dict(proposed_structure.to_dict())
        elif type(proposed_structure) is dict:
            built = build_typed_prompt(original, proposed_structure)
            if isinstance(built, Err):
                return built
            prompt = built.value
        else:
            raise TypeError("proposed_structure must be TypedPromptV1 or exact mapping")
        if sha256_ref(original) != prompt.source_digest:
            return Err(
                Refusal(
                    code="ORIGINAL_PROMPT_MISBIND",
                    message="typed prompt does not bind the supplied original bytes",
                    locus="source_digest",
                )
            )
        protected_ok = original == prompt.original_text.encode("utf-8")
        if not protected_ok:
            return Err(
                Refusal(
                    code="ORIGINAL_PROMPT_MUTATED",
                    message="original prompt bytes changed during structural proposal",
                    locus="original_text",
                )
            )
        findings = _core_findings(prompt) + _registry_findings(prompt, validated_registry)
        findings.sort(key=lambda item: (item.severity, item.code, item.field, item.finding_id))
        outcome = (
            "NEEDS_CLARIFICATION"
            if any(item.severity == "ERROR" for item in findings)
            else "READY_FOR_OPERATOR_REVIEW"
        )
        receipt = PromptReviewReceiptV1(
            source_digest=prompt.source_digest,
            prompt_id=prompt.prompt_id,
            registry_id=validated_registry.registry_id,
            policy_digest=POLICY_DIGEST,
            implementation_digest=review_implementation_digest(),
            finding_ids=tuple(item.finding_id for item in findings),
            outcome=outcome,
            protected_fields_ok=protected_ok,
        )
        return Ok(
            PromptReviewBundleV1(
                prompt,
                tuple(findings),
                receipt,
                validated_registry,
            )
        )
    except (OSError, TypeError, ValueError) as exc:
        return Err(
            Refusal(
                code="PROMPT_REVIEW_REFUSED",
                message=str(exc),
                locus="review_prompt",
            )
        )


def _render_list(title: str, values: Sequence[str]) -> list[str]:
    lines = [f"## {title}", ""]
    if not values:
        lines.extend(("- None declared.", ""))
    else:
        lines.extend(f"- {value}" for value in values)
        lines.append("")
    return lines


def render_typed_prompt(prompt: TypedPromptV1) -> str:
    """Render every typed field; free prose cannot erase protected structure."""

    lines = [
        "# Typed Prompt",
        "",
        f"Objective: {prompt.objective}",
        f"Claim mode: {prompt.claim_mode}",
        "AuthorityEffect: None",
        "Model-authored verdicts are untrusted.",
        "",
        "## Proposed instruction",
        "",
        prompt.proposed_prompt,
        "",
    ]
    for title, values in (
        ("In scope", prompt.in_scope),
        ("Out of scope", prompt.out_of_scope),
        ("Inputs", prompt.inputs),
        ("Constraints", prompt.constraints),
        ("Acceptance criteria", prompt.acceptance_criteria),
        ("Evidence requirements", prompt.evidence_requirements),
        ("Requested effects", prompt.requested_effects),
        ("Nonclaims", prompt.nonclaims),
        ("Unresolved questions", prompt.unresolved_questions),
    ):
        lines.extend(_render_list(title, values))
    lines.extend(
        (
            "## Budgets",
            "",
            f"- Candidate budget: {prompt.candidate_budget}",
            f"- Operation budget: {prompt.operation_budget}",
            "",
            "## Original prompt — immutable provenance",
            "",
        )
    )
    original_lines = prompt.original_text.splitlines() or [""]
    lines.extend("    " + line for line in original_lines)
    rendered = "\n".join(lines).rstrip() + "\n"
    if len(rendered.encode("utf-8")) > MAX_TEXT_BYTES:
        raise ValueError("rendered prompt exceeds the approved-prompt text limit")
    return rendered


def approve_prompt(
    bundle: PromptReviewBundleV1,
    operator_decision: Mapping[str, Any],
) -> Result[ApprovedPromptV1, Refusal]:
    """Record an explicit decision after replay; v0 does not authenticate identity."""

    try:
        validated = PromptReviewBundleV1.from_dict(bundle.to_dict())
        replayed = review_prompt(
            validated.prompt.original_text.encode("utf-8"),
            validated.prompt,
            validated.registry,
        )
        if isinstance(replayed, Err) or replayed.value.to_dict() != validated.to_dict():
            return Err(
                Refusal(
                    code="PROMPT_REVIEW_REPLAY_MISMATCH",
                    message="review bundle does not match independent deterministic replay",
                    locus="review_bundle",
                )
            )
        if type(operator_decision) is not dict:
            raise ValueError("operator decision must be an exact object")
        required = {"approved", "operator_id", "review_receipt_id"}
        if set(operator_decision) != required:
            raise ValueError("operator decision fields are not exact")
        approved = operator_decision["approved"]
        operator_id = operator_decision["operator_id"]
        receipt_id = operator_decision["review_receipt_id"]
        if type(approved) is not bool:
            raise ValueError("approved must be an exact boolean")
        if type(operator_id) is not str or not operator_id.strip():
            raise ValueError("operator_id must be a nonempty string")
        if receipt_id != validated.receipt.receipt_id:
            raise ValueError("operator decision is bound to another review receipt")
        if not approved:
            return Err(
                Refusal(
                    code="OPERATOR_REJECTED",
                    message="operator declined the prompt candidate",
                    locus="operator_decision",
                )
            )
        if validated.receipt.outcome != "READY_FOR_OPERATOR_REVIEW":
            return Err(
                Refusal(
                    code="PROMPT_NOT_READY",
                    message="error findings must be repaired before approval",
                    locus="review_receipt",
                )
            )
        rendered = render_typed_prompt(validated.prompt)
        return Ok(
            ApprovedPromptV1(
                prompt_id=validated.prompt.prompt_id,
                review_receipt_id=validated.receipt.receipt_id,
                approved_by=operator_id.strip(),
                objective=validated.prompt.objective,
                claim_mode=validated.prompt.claim_mode,
                rendered_prompt=rendered,
                rendered_digest=sha256_ref(rendered.encode("utf-8")),
                candidate_budget=validated.prompt.candidate_budget,
                operation_budget=validated.prompt.operation_budget,
                requested_effects=validated.prompt.requested_effects,
            )
        )
    except (TypeError, ValueError) as exc:
        return Err(
            Refusal(
                code="PROMPT_APPROVAL_REFUSED",
                message=str(exc),
                locus="operator_decision",
            )
        )


def packetize_prompt(approved: ApprovedPromptV1) -> PacketEnvelopeV2:
    """Package approved bytes; packetization still grants no execution authority."""

    validated = ApprovedPromptV1.from_dict(approved.to_dict())
    if validated.claim_mode in {"verify", "prove"}:
        turn_kind = "claimed_result"
    elif validated.requested_effects:
        turn_kind = "code_change"
    else:
        turn_kind = "prose"
    content = validated.rendered_prompt.encode("utf-8")
    payload = build_payload_from_content(
        objective=validated.objective,
        role="user",
        turn_kind=turn_kind,
        content_bytes=content,
        candidate_budget=validated.candidate_budget,
        operation_budget=validated.operation_budget,
    )
    task_id = "omega-prompt-" + validated.approved_prompt_id.removeprefix("sha256:")[:24]
    return build_llm_turn_envelope(payload, task_id=task_id)


__all__ = [
    "CORE_POLICY",
    "POLICY_DIGEST",
    "PROMPT_PROPOSAL_FIELDS",
    "approve_prompt",
    "build_typed_prompt",
    "packetize_prompt",
    "render_typed_prompt",
    "review_implementation_digest",
    "review_prompt",
]
