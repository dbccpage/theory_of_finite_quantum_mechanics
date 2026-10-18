"""Attack matrix and contract tests for llm_turn_v1 (post-review repair)."""

from __future__ import annotations

from copy import deepcopy
import hashlib

import pytest

from omega_engine_pfp.domain.shared_kernel.canonical import (
    CanonicalizationError,
)
from omega_engine_pfp.domain import (
    DEFAULT_REQUIRED_REPLY_FIELDS,
    LLM_TURN_PACKET_FAMILY,
    LLM_TURN_SCHEMA,
    OBSTRUCTION_CLAIM_EVALUATOR_REQUIRED,
    REFUSAL_CANDIDATE_BUDGET_EXCEEDED,
    REFUSAL_CONSEQUENTIAL_WITHOUT_PACKET,
    REFUSAL_CONTENT_DIGEST_MISMATCH,
    REFUSAL_MARKDOWN_CLAIM_INJECTION,
    REFUSAL_PACKET_ID_ABSENT,
    REFUSAL_PARENT_ABSENT,
    REFUSAL_PROSE_PROMPT_REFUSED,
    REFUSAL_REFUSAL_ERASURE,
    REFUSAL_REPLY_NOT_BOUND,
    LlmTurnPayloadV1,
    LlmTurnRunRootV1,
    attach_llm_turn_candidate,
    bind_content_bytes,
    build_llm_turn_envelope,
    build_payload_from_content,
    evaluate_llm_turn_candidate,
    loads_strict_json,
    parse_llm_turn_envelope,
    parse_machine_reply_block,
    render_llm_turn_run_root_markdown,
    validate_machine_reply_fields,
    verify_content_bytes,
    verify_llm_turn_run_root,
    verify_markdown_does_not_mutate_claims,
)

BOOTSTRAP_PARENT = "3b84624481a397d4ba07a8e49a5e609392ea432ff96daf45345b03a19111edfd"
TURN_BODY = b"objective: ship llm_turn_v1 packet family\n"


def _payload(**overrides: object) -> LlmTurnPayloadV1:
    fields = {
        "objective": "package llm chat turn as PacketEnvelopeV2",
        "role": "user",
        "turn_kind": "prose",
        "content_sha256": hashlib.sha256(TURN_BODY).hexdigest(),
        "content_byte_count": len(TURN_BODY),
        "candidate_budget": 3,
        "operation_budget": 20,
        "required_reply_fields": DEFAULT_REQUIRED_REPLY_FIELDS,
        "parent_packet_id": BOOTSTRAP_PARENT,
        "conversation_root_id": None,
    }
    fields.update(overrides)
    return LlmTurnPayloadV1(**fields)  # type: ignore[arg-type]


def _envelope(payload: LlmTurnPayloadV1 | None = None):
    payload = payload or _payload()
    return build_llm_turn_envelope(
        payload,
        task_id="llm-turn-v1-smoke",
    )


def _content(envelope, *, body: bytes = TURN_BODY):
    return bind_content_bytes(
        packet_id=envelope.packet_id,
        producer_id="model-worker",
        content_bytes=body,
        claimed_summary="untrusted summary",
    )


def _machine_block(
    *,
    packet_id: str,
    parent: str = BOOTSTRAP_PARENT,
    candidate: str = "ABSENT",
    run_root: str = "ABSENT",
    open_obstructions: str = "none",
    authority: str = "None",
    residual_colour: str = "Open",
) -> str:
    return (
        f"PACKET_ID={packet_id}\n"
        f"PARENT={parent}\n"
        f"CANDIDATE={candidate}\n"
        f"RUN_ROOT={run_root}\n"
        f"OPEN_OBSTRUCTIONS={open_obstructions}\n"
        f"RESIDUAL_COLOUR={residual_colour}\n"
        f"AUTHORITY_EFFECT={authority}\n"
        "\n"
        f"{TURN_BODY.decode('utf-8')}"
    )


def test_payload_and_envelope_round_trip_canonical_wire() -> None:
    payload = _payload()
    envelope = _envelope(payload)
    parsed_object = parse_llm_turn_envelope(envelope)
    parsed_wire = parse_llm_turn_envelope(envelope.to_dict())

    assert envelope.packet_family == LLM_TURN_PACKET_FAMILY
    assert envelope.authority_effect == "None"
    assert envelope.source_digest == payload.turn_manifest_root
    assert envelope.initial_state_hash == payload.turn_manifest_root
    assert envelope.parent_event_id == BOOTSTRAP_PARENT
    assert str(payload.schema_version) == LLM_TURN_SCHEMA
    assert parsed_object == payload
    assert parsed_wire == payload
    assert parsed_wire.payload_id == payload.payload_id
    assert _envelope(parsed_wire).packet_id == envelope.packet_id


def test_kill_conditions_are_round_tripped_and_bound_into_payload_identity() -> None:
    payload = _payload(kill_conditions=("F-01_inherited_meaning", "F-02_syntax"))
    wire = payload.to_dict()

    assert wire["kill_conditions"] == ["F-01_inherited_meaning", "F-02_syntax"]
    assert LlmTurnPayloadV1.from_dict(wire) == payload

    mutated = deepcopy(wire)
    mutated["kill_conditions"] = ["F-01_inherited_meaning"]
    assert LlmTurnPayloadV1.from_dict(mutated).payload_id != payload.payload_id


def test_strict_payload_parser_refuses_unknown_and_missing_fields() -> None:
    wire = _payload().to_dict()
    unknown = deepcopy(wire)
    unknown["promotion_eligible"] = True
    missing = deepcopy(wire)
    del missing["content_sha256"]
    extra = deepcopy(wire)
    extra["verified"] = True

    for attack in (unknown, missing, extra):
        with pytest.raises(CanonicalizationError):
            LlmTurnPayloadV1.from_dict(attack)

    arbitrary_unknown = deepcopy(wire)
    arbitrary_unknown["unbound_metadata"] = "ignored-before-repair"
    with pytest.raises(CanonicalizationError, match="unknown fields"):
        LlmTurnPayloadV1.from_dict(arbitrary_unknown)


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("candidate_budget", True),
        ("candidate_budget", "3"),
        ("operation_budget", 4.5),
        ("content_byte_count", "12"),
    ),
)
def test_payload_wire_refuses_coerced_numeric_types(field: str, value: object) -> None:
    wire = _payload().to_dict()
    wire[field] = value
    with pytest.raises(CanonicalizationError, match="exact integer"):
        LlmTurnPayloadV1.from_dict(wire)


def test_payload_wire_refuses_schema_family_and_alias_misbinding() -> None:
    wire = _payload().to_dict()
    for field, value in (
        ("schema_version", "omega.symbol-game.llm-turn.v999"),
        ("family", "research_claim"),
    ):
        attack = deepcopy(wire)
        attack[field] = value
        with pytest.raises(CanonicalizationError, match="unsupported"):
            LlmTurnPayloadV1.from_dict(attack)

    aliases = deepcopy(wire)
    aliases["prompt_body_sha256"] = "f" * 64
    with pytest.raises(CanonicalizationError, match="aliases disagree"):
        LlmTurnPayloadV1.from_dict(aliases)


def test_duplicate_json_keys_are_refused() -> None:
    text = '{"objective":"a","objective":"b"}'
    with pytest.raises(CanonicalizationError, match="duplicate JSON key"):
        loads_strict_json(text)


def test_authority_effect_must_be_none_on_payload_and_envelope() -> None:
    wire = _payload().to_dict()
    wire["authority_effect"] = "Promote"
    with pytest.raises(CanonicalizationError, match="AuthorityEffect None"):
        LlmTurnPayloadV1.from_dict(wire)

    envelope_wire = _envelope().to_dict()
    envelope_wire["authority_effect"] = "Promote"
    with pytest.raises(CanonicalizationError, match="authority"):
        parse_llm_turn_envelope(envelope_wire)


def test_content_bytes_are_content_addressed_and_verified() -> None:
    body = b"hello turn body\n"
    payload = build_payload_from_content(
        objective="bind content",
        role="user",
        turn_kind="prose",
        content_bytes=body,
        parent_packet_id=BOOTSTRAP_PARENT,
    )
    envelope = _envelope(payload)
    content = _content(envelope, body=body)
    assert content.content_sha256 == hashlib.sha256(body).hexdigest()
    assert content.content_byte_count == len(body)
    verify_content_bytes(content, body)
    with pytest.raises(CanonicalizationError, match="CONTENT_DIGEST_MISMATCH"):
        verify_content_bytes(content, body + b"tamper")


def test_attach_and_evaluate_happy_path_transport_validated() -> None:
    envelope = _envelope()
    content = _content(envelope)
    reply = _machine_block(packet_id=envelope.packet_id)
    candidate = attach_llm_turn_candidate(
        envelope,
        content,
        claimed_valid=True,
        claimed_terminal="LabExactCandidate",
        reply_text=reply,
    )
    root = evaluate_llm_turn_candidate(
        envelope,
        candidate,
        content,
        content_bytes=TURN_BODY,
        reply_text=reply,
        machine_phase="proposal",
    )
    verified = verify_llm_turn_run_root(
        root,
        packet=envelope,
        candidate=candidate,
        content=content,
        content_bytes=TURN_BODY,
        reply_text=reply,
        machine_phase="proposal",
    )

    assert verified.terminal_status == "TransportValidated"
    assert verified.turn_kind == "prose"
    assert verified.refusals == ()
    assert verified.authority_effect == "None"
    assert verified.task_packet_id == envelope.packet_id
    assert candidate.claimed_valid is True


def test_consequential_attach_without_reply_text_is_refused() -> None:
    payload = _payload(turn_kind="code_change")
    envelope = _envelope(payload)
    content = _content(envelope)
    with pytest.raises(CanonicalizationError, match="reply_text"):
        attach_llm_turn_candidate(envelope, content)


def test_consequential_turn_without_machine_block_is_prose_prompt_refused() -> None:
    payload = _payload(turn_kind="code_change")
    envelope = _envelope(payload)
    content = _content(envelope)
    # Bound reply without a machine field block.
    candidate = attach_llm_turn_candidate(
        envelope, content, reply_text="no machine header\n"
    )
    root = evaluate_llm_turn_candidate(
        envelope,
        candidate,
        content,
        content_bytes=TURN_BODY,
        reply_text="no machine header\n",
    )
    assert root.terminal_status == "ProsePromptRefused"
    assert REFUSAL_PROSE_PROMPT_REFUSED in root.refusals
    assert "MISSING:PACKET_ID" in root.refusals


def test_consequential_payload_cannot_weaken_required_reply_fields() -> None:
    with pytest.raises(CanonicalizationError, match="exact canonical"):
        _payload(
            turn_kind="code_change",
            required_reply_fields=("AUTHORITY_EFFECT",),
        )
    with pytest.raises(CanonicalizationError, match="exact canonical"):
        _payload(
            turn_kind="claimed_result",
            required_reply_fields=(
                "AUTHORITY_EFFECT",
                "CANDIDATE",
                "OPEN_OBSTRUCTIONS",
                "PACKET_ID",
                "PARENT",
            ),  # missing RUN_ROOT
        )
    # Full canonical set accepted for consequential.
    payload = _payload(
        turn_kind="code_change",
        required_reply_fields=DEFAULT_REQUIRED_REPLY_FIELDS,
    )
    assert payload.required_reply_fields.fields == DEFAULT_REQUIRED_REPLY_FIELDS
    # Non-consequential prose may relax the set intentionally.
    relaxed = _payload(
        turn_kind="prose",
        required_reply_fields=("AUTHORITY_EFFECT", "PACKET_ID"),
    )
    assert relaxed.required_reply_fields.fields == ("AUTHORITY_EFFECT", "PACKET_ID")


def test_claimed_result_is_packetized_not_claim_verified() -> None:
    payload = _payload(turn_kind="claimed_result")
    envelope = _envelope(payload)
    content = _content(envelope)
    reply = _machine_block(packet_id=envelope.packet_id)
    candidate = attach_llm_turn_candidate(envelope, content, reply_text=reply)
    root = evaluate_llm_turn_candidate(
        envelope,
        candidate,
        content,
        content_bytes=TURN_BODY,
        reply_text=reply,
        machine_phase="proposal",
    )
    assert root.terminal_status == "PacketizedTurn"
    assert OBSTRUCTION_CLAIM_EVALUATOR_REQUIRED in root.open_obstruction_ids
    assert root.refusals == ()


def test_packet_id_absent_with_known_packet_is_refused() -> None:
    fields = parse_machine_reply_block(_machine_block(packet_id="ABSENT"))
    refusals = validate_machine_reply_fields(
        fields,
        required=DEFAULT_REQUIRED_REPLY_FIELDS,
        expected_packet_id="a" * 64,
        expected_parent=BOOTSTRAP_PARENT,
        phase="proposal",
    )
    assert REFUSAL_PACKET_ID_ABSENT in refusals


def test_parent_absent_with_known_parent_is_refused() -> None:
    fields = parse_machine_reply_block(
        _machine_block(packet_id="a" * 64, parent="ABSENT")
    )
    refusals = validate_machine_reply_fields(
        fields,
        required=DEFAULT_REQUIRED_REPLY_FIELDS,
        expected_packet_id="a" * 64,
        expected_parent=BOOTSTRAP_PARENT,
        phase="proposal",
    )
    assert REFUSAL_PARENT_ABSENT in refusals


def test_proposal_phase_rejects_dummy_candidate_run_root_ids() -> None:
    fields = parse_machine_reply_block(
        _machine_block(
            packet_id="a" * 64,
            candidate="c" * 64,
            run_root="d" * 64,
        )
    )
    refusals = validate_machine_reply_fields(
        fields,
        required=DEFAULT_REQUIRED_REPLY_FIELDS,
        expected_packet_id="a" * 64,
        expected_parent=BOOTSTRAP_PARENT,
        phase="proposal",
    )
    assert any("CANDIDATE_MUST_BE_ABSENT" in code for code in refusals)


def test_changed_reply_text_after_attach_is_refused() -> None:
    envelope = _envelope()
    content = _content(envelope)
    reply = _machine_block(packet_id=envelope.packet_id)
    candidate = attach_llm_turn_candidate(envelope, content, reply_text=reply)
    other = _machine_block(packet_id=envelope.packet_id, open_obstructions="FORGED")
    root = evaluate_llm_turn_candidate(
        envelope,
        candidate,
        content,
        content_bytes=TURN_BODY,
        reply_text=other,
        machine_phase="proposal",
    )
    assert root.terminal_status == "TypedRefusal"
    assert REFUSAL_REPLY_NOT_BOUND in root.refusals


def test_parse_machine_reply_block_reads_leading_fields_only() -> None:
    text = _machine_block(packet_id="a" * 64) + "PACKET_ID=should-not-override\n"
    fields = parse_machine_reply_block(text)
    assert fields["PACKET_ID"] == "a" * 64
    assert fields["AUTHORITY_EFFECT"] == "None"
    assert "should-not-override" not in fields["PACKET_ID"]


def test_content_digest_mismatch_is_typed_refusal() -> None:
    envelope = _envelope()
    content = _content(envelope)
    candidate = attach_llm_turn_candidate(envelope, content)
    with pytest.raises(CanonicalizationError, match=REFUSAL_CONTENT_DIGEST_MISMATCH):
        evaluate_llm_turn_candidate(
            envelope,
            candidate,
            content,
            content_bytes=b"different body\n",
        )
    with pytest.raises(CanonicalizationError, match=REFUSAL_CONTENT_DIGEST_MISMATCH):
        verify_content_bytes(content, b"different body\n")


def test_candidate_budget_exhaustion_is_typed() -> None:
    envelope = _envelope(_payload(candidate_budget=1))
    content = _content(envelope)
    candidate = attach_llm_turn_candidate(envelope, content)
    root = evaluate_llm_turn_candidate(
        envelope, candidate, content, prior_candidate_count=1
    )
    assert root.terminal_status == "BudgetExhausted"
    assert REFUSAL_CANDIDATE_BUDGET_EXCEEDED in root.refusals


def test_markdown_cannot_erase_refusals_or_add_claims() -> None:
    payload = _payload(turn_kind="code_change")
    envelope = _envelope(payload)
    content = _content(envelope)
    bare = "no machine header\n"
    candidate = attach_llm_turn_candidate(envelope, content, reply_text=bare)
    root = evaluate_llm_turn_candidate(
        envelope,
        candidate,
        content,
        content_bytes=TURN_BODY,
        reply_text=bare,
    )
    markdown = render_llm_turn_run_root_markdown(root)
    verify_markdown_does_not_mutate_claims(root, markdown)
    assert REFUSAL_PROSE_PROMPT_REFUSED in root.refusals
    assert f"`{REFUSAL_PROSE_PROMPT_REFUSED}`" in markdown

    erased = markdown.replace(f"`{REFUSAL_PROSE_PROMPT_REFUSED}`", "`HIDDEN`")
    with pytest.raises(CanonicalizationError, match=REFUSAL_REFUSAL_ERASURE):
        verify_markdown_does_not_mutate_claims(root, erased)

    injected = markdown + "\npromotion_eligible: true\n"
    with pytest.raises(CanonicalizationError, match=REFUSAL_MARKDOWN_CLAIM_INJECTION):
        verify_markdown_does_not_mutate_claims(root, injected)


def test_run_root_refuses_verified_proposal_terminal() -> None:
    with pytest.raises(CanonicalizationError):
        LlmTurnRunRootV1(
            task_packet_id="a" * 64,
            task_packet_sha256="b" * 64,
            turn_kind="prose",
            candidate_ids=("c" * 64,),
            content_ids=("d" * 64,),
            attempts=(),
            refusals=(),
            terminal_status="VerifiedProposal",
            open_obstruction_ids=(),
        )


def test_forged_transport_validated_without_evidence_is_refused() -> None:
    with pytest.raises(CanonicalizationError):
        LlmTurnRunRootV1(
            task_packet_id="a" * 64,
            task_packet_sha256="b" * 64,
            turn_kind="prose",
            candidate_ids=(),
            content_ids=(),
            attempts=(),
            refusals=(),
            terminal_status="TransportValidated",
            open_obstruction_ids=(),
        )


def test_candidate_content_substitution_is_refused() -> None:
    envelope = _envelope()
    content_a = _content(envelope, body=TURN_BODY)
    content_b = bind_content_bytes(
        packet_id=envelope.packet_id,
        producer_id="model-worker",
        content_bytes=b"other body\n",
    )
    candidate = attach_llm_turn_candidate(envelope, content_a)
    with pytest.raises(CanonicalizationError, match="CANDIDATE_CONTENT_MISBIND"):
        evaluate_llm_turn_candidate(
            envelope, candidate, content_b, content_bytes=b"other body\n"
        )


def test_positive_llm_verify_without_evidence_is_refused() -> None:
    envelope = _envelope()
    content = _content(envelope)
    reply = _machine_block(packet_id=envelope.packet_id)
    candidate = attach_llm_turn_candidate(envelope, content, reply_text=reply)
    root = evaluate_llm_turn_candidate(
        envelope,
        candidate,
        content,
        content_bytes=TURN_BODY,
        reply_text=reply,
        machine_phase="proposal",
    )
    with pytest.raises(
        CanonicalizationError, match="POSITIVE_TERMINAL_NEEDS_EVIDENCE_REPLAY"
    ):
        verify_llm_turn_run_root(root)


def test_family_identity_is_not_research_or_code_change() -> None:
    envelope = _envelope()
    assert envelope.packet_family == "llm_turn_v1"
    assert envelope.packet_family != "code_change_proposal_v1"
    assert envelope.packet_family != "research_claim_v1"
