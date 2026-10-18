"""Adversarial and contract tests for PromptArtifactV1 (prompt_artifact_packets.py).

Implements test coverage for the 8 contract laws in Section 6.3:
1. Compile Open residual + dual_witness_ref set -> refuse
2. Compile Exact without dual_witness_ref -> refuse
3. from_dict with forbidden authority fields -> refuse
4. Unsorted arrays on verify -> refuse (REFUSAL_ARRAY_NOT_SORTED)
5. Body bytes mismatch -> refuse (REFUSAL_BODY_DIGEST_MISMATCH)
6. Round-trip: compile -> to_dict -> from_dict -> same prompt_artifact_id
7. Bridge: artifact -> LlmTurnPayloadV1.content_sha256 equals prompt_body_sha256
8. Machine block with RESIDUAL_COLOUR=Exact without dual-witness context -> refuse
"""

from __future__ import annotations

import hashlib
import json
import pytest

from omega_engine_pfp.domain import (
    CanonicalizationError,
    REFUSAL_ARRAY_NOT_SORTED,
    REFUSAL_BODY_DIGEST_MISMATCH,
    REFUSAL_EXACT_WITHOUT_DUAL_WITNESS,
    REFUSAL_FORBIDDEN_AUTHORITY_FIELD,
    REFUSAL_ID_MISMATCH,
    REFUSAL_OPEN_WITH_DUAL_WITNESS,
    normalize_utf8_lf,
    raw_content_sha256,
)
from omega_engine_pfp.domain import (
    DEFAULT_REQUIRED_REPLY_FIELDS,
    PROMPT_ARTIFACT_SCHEMA,
    REFUSAL_AUTHORITY_NON_NONE,
    DemandItemV1,
    EliminationReceiptV1,
    ObjectiveTypedV1,
    ObstructionFamily,
    ObstructionHintV1,
    PromptArtifactV1,
    RegimeKind,
    ResidualColour,
    build_payload_from_prompt_artifact,
    compile_prompt_artifact,
    create_elimination_receipt,
    parse_elimination_receipt_block,
    prompt_artifact_to_content_binding,
    prompt_artifact_to_turn_content_binding,
    render_elimination_receipt_block,
    render_prompt_body,
)
from omega_engine_pfp.use_cases.prompt_artifact import (
    load_regime_id,
    write_elimination_receipt,
    write_prompt_artifact,
    write_prompt_body,
)
from omega_engine_pfp.entrypoints.api import (
    compile_prompt,
    create_turn,
    parse_machine_block,
    validate_reply_residual,
)

SAMPLE_REGIME_BYTES = b"REGIME: fence_only\nAUTHORITY_EFFECT: None\n"
SAMPLE_HEX64_A = "a" * 64
SAMPLE_HEX64_B = "b" * 64


def _sample_objective() -> ObjectiveTypedV1:
    return ObjectiveTypedV1(
        kind="test_turn",
        summary="run contract checks",
        target_obstruction_ids=("OBS-01",),
        target_demand_ids=("DEM-01",),
    )


def _sample_artifact(**overrides: object) -> PromptArtifactV1:
    obj = _sample_objective()
    regime_bytes = SAMPLE_REGIME_BYTES
    body_bytes = render_prompt_body(
        regime_bytes,
        objective_typed=obj,
        admitted_constructors=("ctor_a", "ctor_b"),
        open_obstructions=(
            ObstructionHintV1(
                obstruction_id="OBS-01",
                family="synthetic_curve",
                residual_colour="Open",
            ),
        ),
        demand_set=(DemandItemV1(demand_id="DEM-01", kind="verify_proof"),),
        kill_conditions=("F-01_inherited_meaning", "F-02_syntax_implies_semantic"),
        required_reply_fields=DEFAULT_REQUIRED_REPLY_FIELDS,
    )
    kwargs = {
        "regime_kind": RegimeKind.FENCE_ONLY,
        "regime_definition_bytes": regime_bytes,
        "prompt_body_bytes": body_bytes,
        "objective_typed": obj,
        "admitted_constructors": ("ctor_a", "ctor_b"),
        "open_obstructions": (
            ObstructionHintV1(
                obstruction_id="OBS-01",
                family="synthetic_curve",
                residual_colour="Open",
            ),
        ),
        "demand_set": (DemandItemV1(demand_id="DEM-01", kind="verify_proof"),),
        "kill_conditions": ("F-01_inherited_meaning", "F-02_syntax_implies_semantic"),
        "required_reply_fields": DEFAULT_REQUIRED_REPLY_FIELDS,
        "residual_colour": ResidualColour.OPEN,
    }
    kwargs.update(overrides)
    return compile_prompt_artifact(**kwargs)


# 1. Compile Open residual + dual_witness_ref set -> refuse
def test_1_open_residual_with_dual_witness_ref_is_refused() -> None:
    with pytest.raises(CanonicalizationError, match=REFUSAL_OPEN_WITH_DUAL_WITNESS):
        _sample_artifact(
            residual_colour=ResidualColour.OPEN,
            dual_witness_ref=SAMPLE_HEX64_A,
        )

    with pytest.raises(CanonicalizationError, match=REFUSAL_OPEN_WITH_DUAL_WITNESS):
        _sample_artifact(
            residual_colour=ResidualColour.CLOSED,
            dual_witness_ref=SAMPLE_HEX64_A,
        )


# 2. Compile Exact without dual_witness_ref -> refuse
def test_2_exact_residual_without_dual_witness_is_refused() -> None:
    with pytest.raises(CanonicalizationError, match=REFUSAL_EXACT_WITHOUT_DUAL_WITNESS):
        _sample_artifact(
            residual_colour=ResidualColour.EXACT,
            dual_witness_ref=None,
        )

    # Valid Exact with dual witness passes
    artifact = _sample_artifact(
        residual_colour=ResidualColour.EXACT,
        dual_witness_required=True,
        dual_witness_ref=SAMPLE_HEX64_A,
    )
    assert artifact.residual_colour == "Exact"
    assert artifact.dual_witness_required is True
    assert artifact.dual_witness_ref == SAMPLE_HEX64_A


# 3. from_dict with forbidden authority fields -> refuse
@pytest.mark.parametrize(
    "forbidden_key",
    ["passed", "verified", "promotion_eligible", "trusted"],
)
def test_3_from_dict_with_forbidden_authority_field_is_refused(forbidden_key: str) -> None:
    artifact = _sample_artifact()
    wire = artifact.to_dict()
    wire[forbidden_key] = True
    with pytest.raises(CanonicalizationError, match=REFUSAL_FORBIDDEN_AUTHORITY_FIELD):
        PromptArtifactV1.from_dict(wire)


# 4. Unsorted arrays on verify -> refuse (REFUSAL_ARRAY_NOT_SORTED)
def test_4_unsorted_arrays_on_verify_are_refused() -> None:
    artifact = _sample_artifact()

    # Unsorted kill_conditions
    wire = artifact.to_dict()
    wire["kill_conditions"] = ["F-02_syntax_implies_semantic", "F-01_inherited_meaning"]
    with pytest.raises(CanonicalizationError, match=REFUSAL_ARRAY_NOT_SORTED):
        PromptArtifactV1.from_dict(wire)

    # Unsorted admitted_constructors
    wire = artifact.to_dict()
    wire["admitted_constructors"] = ["ctor_b", "ctor_a"]
    with pytest.raises(CanonicalizationError, match=REFUSAL_ARRAY_NOT_SORTED):
        PromptArtifactV1.from_dict(wire)

    # Unsorted open_obstructions by obstruction_id
    wire = artifact.to_dict()
    obs_b = ObstructionHintV1(
        obstruction_id="OBS-02", family="synthetic_curve", residual_colour="Open"
    ).to_dict()
    obs_a = ObstructionHintV1(
        obstruction_id="OBS-01", family="synthetic_curve", residual_colour="Open"
    ).to_dict()
    wire["open_obstructions"] = [obs_b, obs_a]
    with pytest.raises(CanonicalizationError, match=REFUSAL_ARRAY_NOT_SORTED):
        PromptArtifactV1.from_dict(wire)

    # Unsorted demand_set by demand_id
    wire = artifact.to_dict()
    dem_b = DemandItemV1(demand_id="DEM-02", kind="verify").to_dict()
    dem_a = DemandItemV1(demand_id="DEM-01", kind="verify").to_dict()
    wire["demand_set"] = [dem_b, dem_a]
    with pytest.raises(CanonicalizationError, match=REFUSAL_ARRAY_NOT_SORTED):
        PromptArtifactV1.from_dict(wire)


# 5. Body bytes mismatch -> refuse (REFUSAL_BODY_DIGEST_MISMATCH)
def test_5_body_bytes_mismatch_is_refused() -> None:
    artifact = _sample_artifact()
    artifact.verify_prompt_body(
        render_prompt_body(
            SAMPLE_REGIME_BYTES,
            objective_typed=artifact.objective_typed,
            admitted_constructors=artifact.admitted_constructors,
            open_obstructions=artifact.open_obstructions,
            demand_set=artifact.demand_set,
            kill_conditions=artifact.kill_conditions,
            required_reply_fields=artifact.required_reply_fields,
        )
    )
    with pytest.raises(CanonicalizationError, match=REFUSAL_BODY_DIGEST_MISMATCH):
        artifact.verify_prompt_body(b"tampered prompt body bytes\n")


# 6. Round-trip: compile -> to_dict -> from_dict -> same prompt_artifact_id
def test_6_compile_to_dict_from_dict_round_trip() -> None:
    artifact = _sample_artifact()
    wire = artifact.to_dict()
    reparsed = PromptArtifactV1.from_dict(wire)
    assert reparsed.prompt_artifact_id == artifact.prompt_artifact_id
    assert reparsed.to_dict() == wire

    # Tampering with ID fails verification
    wire["prompt_artifact_id"] = "f" * 64
    with pytest.raises(CanonicalizationError, match=REFUSAL_ID_MISMATCH):
        PromptArtifactV1.from_dict(wire)


# 7. Bridge: artifact -> LlmTurnPayloadV1.content_sha256 equals prompt_body_sha256
def test_7_llm_turn_bridge_content_binding() -> None:
    artifact = _sample_artifact()
    content_sha256, content_byte_count = prompt_artifact_to_turn_content_binding(artifact)
    assert content_sha256 == artifact.prompt_body_sha256
    assert content_byte_count == artifact.prompt_body_byte_count

    payload = build_payload_from_prompt_artifact(artifact)
    assert str(payload.content_sha256) == str(artifact.prompt_body_sha256)
    assert int(payload.content_byte_count) == int(artifact.prompt_body_byte_count)
    assert f"[prompt_artifact:{artifact.prompt_artifact_id}]" in str(payload.objective)
    assert str(payload.authority_effect.value if hasattr(payload.authority_effect, 'value') else payload.authority_effect) == "None"


# 8. Machine block with RESIDUAL_COLOUR=Exact without dual-witness context -> refuse
def test_8_machine_block_exact_residual_without_dual_witness_refused() -> None:
    reply = (
        "Here is my solution.\n"
        "```machine\n"
        "PACKET_ID=abc\n"
        "PARENT=ABSENT\n"
        "CANDIDATE=ABSENT\n"
        "RUN_ROOT=ABSENT\n"
        "OPEN_OBSTRUCTIONS=none\n"
        "RESIDUAL_COLOUR=Exact\n"
        "AUTHORITY_EFFECT=None\n"
        "```\n"
    )
    fields = parse_machine_block(reply)
    assert fields["RESIDUAL_COLOUR"] == "Exact"
    assert fields["AUTHORITY_EFFECT"] == "None"

    # Without dual witness host digest -> refused, falls back to Open
    colour, refusals = validate_reply_residual(fields, dual_witness_digest=None)
    assert REFUSAL_EXACT_WITHOUT_DUAL_WITNESS in refusals
    assert colour == "Open"

    # With dual witness host digest -> accepted as Exact
    colour_ok, refusals_ok = validate_reply_residual(fields, dual_witness_digest=SAMPLE_HEX64_A)
    assert refusals_ok == []
    assert colour_ok == "Exact"


def test_swarm_api_compile_and_create_turn() -> None:
    obj = _sample_objective()
    artifact, body_bytes = compile_prompt(
        RegimeKind.FENCE_ONLY,
        SAMPLE_REGIME_BYTES,
        obj,
        admitted_constructors=("ctor_1",),
        open_obstructions=(
            ObstructionHintV1(
                obstruction_id="OBS-01",
                family="synthetic_curve",
                residual_colour="Open",
            ),
        ),
        kill_conditions=("F-01_inherited_meaning",),
    )
    assert artifact.prompt_body_sha256 == hashlib.sha256(body_bytes).hexdigest()
    turn = create_turn(artifact)
    assert str(turn.content_sha256) == str(artifact.prompt_body_sha256)


def test_cli_compile_verify_and_create_task(tmp_path: pytest.TempPathFactory) -> None:
    from omega_engine_pfp.entrypoints.cli.symbol_game import main

    regime_file = tmp_path / "regime.txt"
    regime_file.write_bytes(SAMPLE_REGIME_BYTES)

    artifact_out = tmp_path / "artifact.json"
    code = main([
        "compile-prompt",
        "--regime-bytes", str(regime_file),
        "--regime-kind", "fence_only",
        "--objective-kind", "test_turn",
        "--objective-summary", "cli test turn",
        "--output", str(artifact_out),
    ])
    assert code == 0
    assert artifact_out.exists()

    # Verify prompt CLI
    code_verify = main([
        "verify-prompt",
        "--artifact", str(artifact_out),
    ])
    assert code_verify == 0

    # Create task from prompt CLI
    task_out = tmp_path / "task.json"
    code_task = main([
        "create-task-from-prompt",
        "--artifact", str(artifact_out),
        "--task-id", "test-prompt-cli-task",
        "--output", str(task_out),
    ])
    assert code_task == 0
    assert task_out.exists()


def test_layer_a_identity_differs_from_layer_b_content() -> None:
    from omega_engine_pfp.domain import (
        prompt_artifact_to_content_binding,
        raw_content_sha256,
        normalize_utf8_lf,
    )

    art = _sample_artifact()
    body_sha, body_len = prompt_artifact_to_content_binding(art)
    assert body_sha == art.prompt_body_sha256
    assert body_len == art.prompt_body_byte_count
    # Layer A (identity) != Layer B (raw content)
    assert art.prompt_artifact_id != art.prompt_body_sha256

    # raw_content_sha256 type checks
    with pytest.raises(TypeError):
        raw_content_sha256("not bytes")  # type: ignore[arg-type]

    # normalize_utf8_lf converts CRLF and CR to LF
    crlf_data = b"Line 1\r\nLine 2\rLine 3\n"
    normalized = normalize_utf8_lf(crlf_data)
    assert normalized == b"Line 1\nLine 2\nLine 3\n"


def test_content_addressed_disk_writing(tmp_path: pytest.TempPathFactory) -> None:
    art = _sample_artifact()
    art_path = write_prompt_artifact(tmp_path, art)
    assert art_path.exists()
    assert art_path.name.startswith("prompt-artifact_")
    assert art_path.name.endswith(".json")

    # Re-writing same artifact succeeds
    art_path_2 = write_prompt_artifact(tmp_path, art)
    assert art_path_2 == art_path

    body = b"hello test body\n"
    body_path = write_prompt_body(tmp_path, body)
    assert body_path.exists()
    assert body_path.name.startswith("prompt-body_")
    assert body_path.name.endswith(".bin")

    # Collision with different bytes fails closed
    fake_body_path = tmp_path / body_path.name
    with pytest.raises(CanonicalizationError, match="different bytes"):
        # Attempt to write different bytes to the same filename
        digest, _ = raw_content_sha256(body)
        clash_path = tmp_path / f"prompt-body_{digest}.bin"
        clash_path.write_bytes(b"corrupted bytes")
        write_prompt_body(tmp_path, body)

    # Regime loading
    regime_file = tmp_path / "test_regime.v1.txt"
    regime_file.write_bytes(b"REGIME: custom_bound\r\nAUTHORITY_EFFECT: None\r\n")
    regime_id, norm_bytes = load_regime_id(regime_file)
    assert norm_bytes == b"REGIME: custom_bound\nAUTHORITY_EFFECT: None\n"
    assert regime_id == hashlib.sha256(norm_bytes).hexdigest()


def test_objective_summary_trimmed_validation() -> None:
    with pytest.raises(CanonicalizationError, match="nonempty and trimmed"):
        ObjectiveTypedV1(kind="turn", summary="")

    with pytest.raises(CanonicalizationError, match="nonempty and trimmed"):
        ObjectiveTypedV1(kind="turn", summary=" leading space")

    with pytest.raises(CanonicalizationError, match="nonempty and trimmed"):
        ObjectiveTypedV1(kind="turn", summary="trailing space ")


def test_elimination_receipt_creation_and_round_trip() -> None:
    from omega_engine_pfp.domain import (
        EliminationReceiptV1,
        create_elimination_receipt,
    )

    receipt = create_elimination_receipt(
        packet_id=SAMPLE_HEX64_A,
        prior_residual_colour="Open",
        new_residual_colour="Closed",
        evidence_root=SAMPLE_HEX64_B,
        eliminated_obstruction_ids=("OBS-02", "OBS-01"),  # should sort to OBS-01, OBS-02
    )
    assert receipt.eliminated_obstruction_ids == ("OBS-01", "OBS-02")
    assert receipt.prior_residual_colour == "Open"
    assert receipt.new_residual_colour == "Closed"
    assert receipt.authority_effect == "None"
    assert receipt.dual_witness_ref is None

    wire = receipt.to_dict()
    assert "elimination_receipt_id" in wire
    reparsed = EliminationReceiptV1.from_dict(wire)
    assert reparsed.elimination_receipt_id == receipt.elimination_receipt_id
    assert reparsed == receipt

    # Tampered id fails closed
    wire["elimination_receipt_id"] = "f" * 64
    with pytest.raises(CanonicalizationError, match=REFUSAL_ID_MISMATCH):
        EliminationReceiptV1.from_dict(wire)


def test_elimination_receipt_residual_honesty() -> None:
    from omega_engine_pfp.domain import (
        create_elimination_receipt,
    )

    # Exact without dual witness -> refuse
    with pytest.raises(CanonicalizationError, match=REFUSAL_EXACT_WITHOUT_DUAL_WITNESS):
        create_elimination_receipt(
            packet_id=SAMPLE_HEX64_A,
            prior_residual_colour="Closed",
            new_residual_colour="Exact",
            evidence_root=SAMPLE_HEX64_B,
            dual_witness_ref=None,
        )

    # Open with dual witness -> refuse
    with pytest.raises(CanonicalizationError, match=REFUSAL_OPEN_WITH_DUAL_WITNESS):
        create_elimination_receipt(
            packet_id=SAMPLE_HEX64_A,
            prior_residual_colour="Open",
            new_residual_colour="Open",
            evidence_root=SAMPLE_HEX64_B,
            dual_witness_ref=SAMPLE_HEX64_A,
        )

    # Valid Exact with dual witness
    exact_receipt = create_elimination_receipt(
        packet_id=SAMPLE_HEX64_A,
        prior_residual_colour="Closed",
        new_residual_colour="Exact",
        evidence_root=SAMPLE_HEX64_B,
        dual_witness_ref=SAMPLE_HEX64_A,
    )
    assert exact_receipt.new_residual_colour == "Exact"
    assert exact_receipt.dual_witness_ref == SAMPLE_HEX64_A


def test_elimination_receipt_render_parse_and_disk_write(tmp_path: pytest.TempPathFactory) -> None:
    from omega_engine_pfp.domain import (
        create_elimination_receipt,
        render_elimination_receipt_block,
        parse_elimination_receipt_block,
    )

    receipt = create_elimination_receipt(
        packet_id=SAMPLE_HEX64_A,
        prior_residual_colour="Open",
        new_residual_colour="Closed",
        evidence_root=SAMPLE_HEX64_B,
        eliminated_obstruction_ids=("OBS-01",),
    )

    block = render_elimination_receipt_block(receipt)
    assert "ELIMINATED: OBS-01" in block
    assert "PRIOR_RESIDUAL_COLOUR: Open" in block
    assert "NEW_RESIDUAL_COLOUR: Closed" in block
    assert f"EVIDENCE_ROOT: {SAMPLE_HEX64_B}" in block
    assert "AUTHORITY_EFFECT: None" in block

    parsed = parse_elimination_receipt_block(block)
    assert parsed is not None
    assert parsed["ELIMINATED"] == "OBS-01"
    assert parsed["PRIOR_RESIDUAL_COLOUR"] == "Open"
    assert parsed["NEW_RESIDUAL_COLOUR"] == "Closed"
    assert parsed["EVIDENCE_ROOT"] == SAMPLE_HEX64_B
    assert parsed["AUTHORITY_EFFECT"] == "None"

    # Disk writing
    receipt_path = write_elimination_receipt(tmp_path, receipt)
    assert receipt_path.exists()
    assert receipt_path.name.startswith("elimination-receipt_")
    assert receipt_path.name.endswith(".json")
