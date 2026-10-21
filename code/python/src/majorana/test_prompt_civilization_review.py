from __future__ import annotations

import json
import argparse
from pathlib import Path

from omega_engine.crates.prompt_civilization import (
    Err,
    AntiSkillSpecV1,
    PromptReviewBundleV1,
    PromptReviewReceiptV1,
    approve_prompt,
    compile_registry_syntax_only,
    packetize_prompt,
    review_prompt,
)
from omega_engine_pfp.domain import parse_llm_turn_envelope
from omega_engine.crates.prompt_civilization.cli import build_parser


ORIGINAL = b"Repair the module and prove the scoped theorem."
ROOT = Path(__file__).resolve().parents[2]


def _proposal(**changes):
    proposal = {
        "objective": "Repair the module and prove the scoped theorem.",
        "claim_mode": "prove",
        "in_scope": ["Named module"],
        "out_of_scope": ["Shared kernel changes"],
        "inputs": ["module path", "theorem statement"],
        "constraints": ["Preserve AuthorityEffect None"],
        "acceptance_criteria": ["Focused tests pass", "Lean target builds"],
        "evidence_requirements": ["Lean kernel check", "Independent test replay"],
        "requested_effects": ["workspace-write"],
        "candidate_budget": 3,
        "operation_budget": 20,
        "nonclaims": ["Packetization does not prove the theorem"],
        "unresolved_questions": [],
        "proposed_prompt": (
            "Repair only the named module, prove the scoped theorem, "
            "and report replay evidence."
        ),
    }
    proposal.update(changes)
    return proposal


def _registry():
    return compile_registry_syntax_only([]).unwrap()


def test_review_is_deterministic_and_preserves_original_bytes() -> None:
    first = review_prompt(ORIGINAL, _proposal(), _registry()).unwrap()
    second = review_prompt(ORIGINAL, _proposal(), _registry()).unwrap()
    assert first.to_dict() == second.to_dict()
    assert first.prompt.original_text.encode("utf-8") == ORIGINAL
    assert first.receipt.outcome == "READY_FOR_OPERATOR_REVIEW"
    assert [finding.code for finding in first.findings] == [
        "OPERATOR_APPROVAL_REQUIRED"
    ]


def test_unknown_proposal_field_and_original_mutation_refuse() -> None:
    unknown = _proposal(model_certified=True)
    result = review_prompt(ORIGINAL, unknown, _registry())
    assert isinstance(result, Err)
    assert result.error.code == "INVALID_PROMPT_PROPOSAL"

    prompt = review_prompt(ORIGINAL, _proposal(), _registry()).unwrap().prompt
    misbound = review_prompt(b"different", prompt, _registry())
    assert isinstance(misbound, Err)
    assert misbound.error.code == "ORIGINAL_PROMPT_MISBIND"


def test_packet_budgets_refuse_at_review_boundary() -> None:
    for changes in (
        {"candidate_budget": 33},
        {"operation_budget": 4097},
    ):
        result = review_prompt(ORIGINAL, _proposal(**changes), _registry())
        assert isinstance(result, Err)
        assert result.error.code == "INVALID_PROMPT_PROPOSAL"

    bundle = review_prompt(ORIGINAL, _proposal(), _registry()).unwrap()
    approved = approve_prompt(
        bundle,
        {
            "approved": True,
            "operator_id": "jeremy",
            "review_receipt_id": bundle.receipt.receipt_id,
        },
    ).unwrap()
    wire = approved.to_dict()
    wire["candidate_budget"] = 33
    try:
        type(approved).from_dict(wire)
    except ValueError as exc:
        assert "candidate_budget" in str(exc)
    else:
        raise AssertionError("oversized approved prompt budget was accepted")


def test_exact_downstream_packet_limits_are_reviewed_before_ready() -> None:
    bundle = review_prompt(
        ORIGINAL,
        _proposal(
            objective="x" * 8192,
            candidate_budget=32,
            operation_budget=4096,
        ),
        _registry(),
    ).unwrap()
    approved = approve_prompt(
        bundle,
        {
            "approved": True,
            "operator_id": "jeremy",
            "review_receipt_id": bundle.receipt.receipt_id,
        },
    ).unwrap()
    packetize_prompt(approved)

    oversized_objective = review_prompt(
        ORIGINAL, _proposal(objective="x" * 8193), _registry()
    )
    assert isinstance(oversized_objective, Err)
    assert oversized_objective.error.code == "INVALID_PROMPT_PROPOSAL"

    oversized_render = review_prompt(
        ORIGINAL,
        _proposal(proposed_prompt="x" * ((128 * 1024) - 1)),
        _registry(),
    ).unwrap()
    assert oversized_render.receipt.outcome == "NEEDS_CLARIFICATION"
    assert "RENDERED_PROMPT_RESOURCE_LIMIT" in {
        finding.code for finding in oversized_render.findings
    }


def test_consequential_and_proof_gaps_block_approval() -> None:
    bundle = review_prompt(
        ORIGINAL,
        _proposal(acceptance_criteria=[], evidence_requirements=[]),
        _registry(),
    ).unwrap()
    codes = {finding.code for finding in bundle.findings}
    assert "MISSING_ACCEPTANCE_CRITERIA" in codes
    assert "MISSING_EVIDENCE_REQUIREMENTS" in codes
    assert bundle.receipt.outcome == "NEEDS_CLARIFICATION"
    decision = {
        "approved": True,
        "operator_id": "jeremy",
        "review_receipt_id": bundle.receipt.receipt_id,
    }
    result = approve_prompt(bundle, decision)
    assert isinstance(result, Err)
    assert result.error.code == "PROMPT_NOT_READY"


def test_operator_rejection_leaves_bundle_unchanged() -> None:
    bundle = review_prompt(ORIGINAL, _proposal(), _registry()).unwrap()
    before = bundle.to_dict()
    result = approve_prompt(
        bundle,
        {
            "approved": False,
            "operator_id": "jeremy",
            "review_receipt_id": bundle.receipt.receipt_id,
        },
    )
    assert isinstance(result, Err)
    assert result.error.code == "OPERATOR_REJECTED"
    assert bundle.to_dict() == before


def test_forged_direct_receipt_cannot_authorize() -> None:
    real = review_prompt(ORIGINAL, _proposal(), _registry()).unwrap()
    forged_receipt = PromptReviewReceiptV1(
        source_digest=real.receipt.source_digest,
        prompt_id=real.prompt.prompt_id,
        registry_id=real.registry.registry_id,
        policy_digest=real.receipt.policy_digest,
        implementation_digest="sha256:" + "0" * 64,
        finding_ids=(),
        outcome="READY_FOR_OPERATOR_REVIEW",
        protected_fields_ok=True,
    )
    forged = PromptReviewBundleV1(
        prompt=real.prompt,
        findings=(),
        receipt=forged_receipt,
        registry=real.registry,
    )
    result = approve_prompt(
        forged,
        {
            "approved": True,
            "operator_id": "jeremy",
            "review_receipt_id": forged.receipt.receipt_id,
        },
    )
    assert isinstance(result, Err)
    assert result.error.code == "PROMPT_REVIEW_REPLAY_MISMATCH"


def test_schema_version_mutation_is_rejected() -> None:
    bundle = review_prompt(ORIGINAL, _proposal(), _registry()).unwrap()
    receipt = bundle.receipt.to_dict()
    receipt["schema_version"] = "omega.prompt.review-receipt.v999"
    try:
        PromptReviewReceiptV1.from_dict(receipt)
    except ValueError as exc:
        assert "schema" in str(exc)
    else:
        raise AssertionError("mutated receipt schema was accepted")


def test_approved_prompt_packet_round_trip_keeps_model_verdict_untrusted() -> None:
    bundle = review_prompt(ORIGINAL, _proposal(), _registry()).unwrap()
    approved = approve_prompt(
        bundle,
        {
            "approved": True,
            "operator_id": "jeremy",
            "review_receipt_id": bundle.receipt.receipt_id,
        },
    ).unwrap()
    packet = packetize_prompt(approved)
    payload = parse_llm_turn_envelope(packet)
    assert str(payload.turn_kind) == "claimed_result"
    assert "model_verdicts_untrusted" in packet.constraints
    assert packet.authority_effect == "None"
    assert (
        "## Original prompt — immutable provenance\n\n    " + ORIGINAL.decode("utf-8")
    ) in approved.rendered_prompt


def test_packet_kind_tracks_effects_without_creating_authority() -> None:
    for effects, expected in (([], "prose"), (["workspace-write"], "code_change")):
        bundle = review_prompt(
            ORIGINAL,
            _proposal(claim_mode="investigate", requested_effects=effects),
            _registry(),
        ).unwrap()
        approved = approve_prompt(
            bundle,
            {
                "approved": True,
                "operator_id": "jeremy",
                "review_receipt_id": bundle.receipt.receipt_id,
            },
        ).unwrap()
        payload = parse_llm_turn_envelope(packetize_prompt(approved))
        assert str(payload.turn_kind) == expected


def test_syntax_valid_nonempty_registry_is_runtime_inert() -> None:
    specs = [
        AntiSkillSpecV1(
            spec_id="needs-objective",
            version=1,
            failure_code="ANTISKILL_OBJECTIVE_REQUIRED",
            detector_kind="requires_field",
            activation_fields=("objective",),
            repair_kind="populate_typed_field",
            protected_fields=("original_text",),
            episode_ids=("sha256:" + "1" * 64, "sha256:" + "2" * 64),
            context_keys=("task-a", "task-b"),
            evidence_refs=("fixture:objective",),
            counterexamples=("An explicitly optional field.",),
            evaluation_receipt_ref="sha256:" + "3" * 64,
            composition_order=10,
        ),
        AntiSkillSpecV1(
            spec_id="needs-evidence",
            version=1,
            failure_code="ANTISKILL_EVIDENCE_REQUIRED",
            detector_kind="requires_evidence_for_claim_mode",
            activation_fields=("evidence_requirements",),
            repair_kind="add_evidence_request",
            protected_fields=("original_text",),
            episode_ids=("sha256:" + "4" * 64, "sha256:" + "5" * 64),
            context_keys=("task-c", "task-d"),
            evidence_refs=("fixture:evidence",),
            counterexamples=("Investigative prose makes no proof claim.",),
            evaluation_receipt_ref="sha256:" + "6" * 64,
            composition_order=20,
        ),
        AntiSkillSpecV1(
            spec_id="needs-nonclaim",
            version=1,
            failure_code="ANTISKILL_NONCLAIM_REQUIRED",
            detector_kind="requires_nonclaim",
            activation_fields=("nonclaims",),
            repair_kind="add_nonclaim",
            protected_fields=("original_text",),
            episode_ids=("sha256:" + "7" * 64, "sha256:" + "8" * 64),
            context_keys=("task-e", "task-f"),
            evidence_refs=("fixture:nonclaim",),
            counterexamples=("A nonconsequential greeting needs no nonclaim.",),
            evaluation_receipt_ref="sha256:" + "9" * 64,
            composition_order=30,
        ),
        AntiSkillSpecV1(
            spec_id="needs-operator",
            version=1,
            failure_code="ANTISKILL_OPERATOR_REQUIRED",
            detector_kind="requires_operator_approval",
            activation_fields=("authority_effect",),
            repair_kind="request_operator_approval",
            protected_fields=("original_text",),
            episode_ids=("sha256:" + "a" * 64, "sha256:" + "b" * 64),
            context_keys=("task-g", "task-h"),
            evidence_refs=("fixture:operator",),
            counterexamples=("Pure read-only explanation is nonconsequential.",),
            evaluation_receipt_ref="sha256:" + "c" * 64,
            composition_order=40,
        ),
    ]
    registry = compile_registry_syntax_only(specs).unwrap()
    result = review_prompt(
        ORIGINAL,
        _proposal(objective="", evidence_requirements=[], nonclaims=[]),
        registry,
    )
    assert isinstance(result, Err)
    assert result.error.code == "ANTISKILL_ADMISSION_UNVERIFIED"


def test_receipt_copy_to_different_prompt_fails_binding() -> None:
    bundle = review_prompt(ORIGINAL, _proposal(), _registry()).unwrap()
    other = review_prompt(
        b"another", _proposal(objective="Another task"), _registry()
    ).unwrap()
    copied = bundle.to_dict()
    copied["prompt"] = other.prompt.to_dict()
    try:
        PromptReviewBundleV1.from_dict(copied)
    except ValueError as exc:
        assert "prompt binding mismatch" in str(exc)
    else:
        raise AssertionError("copied receipt was accepted for a different prompt")


def test_negative_control_wording_is_not_scanned_as_truth_evidence() -> None:
    fixture = json.loads(
        (ROOT / ".agents" / "anti_skills" / "fixtures" / "eval_cases.json").read_text(
            encoding="utf-8"
        )
    )
    for case in fixture["cases"][:4]:
        original = case["original_prompt"].encode("utf-8")
        bundle = review_prompt(
            original,
            _proposal(
                objective="Review the supplied wording within its declared scope.",
                claim_mode="investigate",
                requested_effects=[],
                proposed_prompt=case["original_prompt"],
            ),
            _registry(),
        ).unwrap()
        assert [finding.code for finding in bundle.findings] == [
            "OPERATOR_APPROVAL_REQUIRED"
        ]


def test_cli_has_no_send_or_admit_command() -> None:
    parser = build_parser()
    subparsers = [
        action
        for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)
    ]
    assert len(subparsers) == 1
    commands = set(subparsers[0].choices)
    assert "send" not in commands
    assert "admit" not in commands
