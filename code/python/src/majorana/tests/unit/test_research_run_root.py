"""Adversarial tests for the semantic research run-root boundary."""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

from omega_engine_pfp.domain import (
    EVALUATE_FINITE,
    LOCAL_REPLAYABLE_FINITE_EVIDENCE,
    RESEARCH_FAMILY_OWNER_LAWS,
    WITTEN_FINITE_FAMILY,
    ResearchClaimPayloadV1,
    ResearchClaimV1,
    SourceIntakeBundleV1,
    build_research_claim_envelope,
)
from omega_engine_pfp.infrastructure.serialization import (
    write_content_addressed_json,
)
from omega_engine_pfp.use_cases.research import (
    build_source_artifact,
    build_source_intake_bundle,
)
from omega_engine_pfp.domain.aggregates.research_run_root import (
    DDA_TRACE_MEDIA_TYPE,
    RESEARCH_PACKET_MEDIA_TYPE,
    SOURCE_INTAKE_MEDIA_TYPE,
    ArtifactRefV1,
    ResearchRunRootError,
    ResearchRunRootV1,
    SemanticDdaStepV1,
    artifact_ref_from_path,
    build_research_run_root,
    read_research_run_root,
    semantic_dda_from_trace,
    verify_research_run_root,
    write_research_run_root,
)


def _digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _record(
    *,
    run_id: str,
    timestamp: str,
    trace_path: str,
    challenge: str,
    uuid_hex: str,
    letter: str = "E",
    operation: str = "eliminate:finite-obstruction",
    residual_before: float = 1.0,
    residual_after: float = 0.0,
    semantic_value: str = "closed",
) -> dict[str, Any]:
    residual_delta = residual_after - residual_before
    return {
        "schema_version": "omega.dda.trace.v2",
        "dda_dialect": "experimental-z-v1",
        "timestamp_utc": timestamp,
        "runner_id": "semantic-runner",
        "campaign": "bounded-family",
        "run_id": run_id,
        "step_id": "DDA_STEP_001",
        "letter": letter,
        "effect": ("obstruction_eliminated" if letter == "E" else "residual_carried"),
        "action_name": operation,
        "cochain_dim": "C1",
        "coboundary_map": "d1",
        "input_state": "ACTIVE:FINITE_OBSTRUCTION",
        "output_state": "TERMINAL:FINITE_OBSTRUCTION",
        "witness": "FINITE_OBSTRUCTION_WITNESS",
        "obstruction_id": "FINITE_OBSTRUCTION",
        "residual_before": residual_before,
        "residual_after": residual_after,
        "residual_delta": residual_delta,
        "residual_energy": residual_after,
        "structure_delta": {},
        "evidence": {
            "measurement": 0.125,
            "semantic_value": semantic_value,
            "source_path": "research/paper.pdf",
            "occurrence": {
                "path": trace_path,
                "challenge": challenge,
                "uuid": uuid_hex,
                "timestamp": timestamp,
            },
            "packet_artifact": f"{trace_path}/packet.json",
            "source_intake_artifact": f"{trace_path}/intake.json",
            "oesos_trace": f"{trace_path}/oesos.jsonl",
        },
        "refusal_reason": None,
        "authority_effect": "None",
        "prev_step_hash": None,
        "step_hash": _digest(f"native:{run_id}:{timestamp}:{trace_path}"),
        "path": trace_path,
        "challenge_id": challenge,
        "uuid": uuid_hex,
    }


def _native_trace_hash(record: dict[str, Any]) -> str:
    payload = {key: value for key, value in record.items() if key != "step_hash"}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _write_trace(path: Path, record: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    integration = dict(record)
    integration.update(
        {
            "letter": "I",
            "effect": "integration",
            "action_name": "integrate:finite-obstruction",
            "input_state": record["output_state"],
            "output_state": "INTEGRATED:FINITE_OBSTRUCTION",
            "witness": "FINITE_OBSTRUCTION_INTEGRATION",
            "obstruction_id": None,
            "residual_before": record["residual_after"],
            "residual_after": record["residual_after"],
            "residual_delta": (None if record["residual_after"] is None else 0.0),
            "residual_energy": (
                0.0
                if record["residual_after"] is None
                else float(record["residual_after"])
            ),
            "structure_delta": {},
            "evidence": {"semantic_value": "integrated"},
            "refusal_reason": None,
        }
    )
    terminal = dict(integration)
    terminal.update(
        {
            "letter": "T",
            "effect": "terminalization",
            "action_name": "terminalize:finite-obstruction",
            "input_state": integration["output_state"],
            "output_state": "TERMINALIZED:FINITE_OBSTRUCTION",
            "witness": "FINITE_OBSTRUCTION_TERMINAL",
            "evidence": {"semantic_value": "terminalized"},
        }
    )
    records = [record, integration, terminal]
    previous_hash = None
    for index, item in enumerate(records, start=1):
        item["step_id"] = f"DDA_STEP_{index:03d}"
        item["prev_step_hash"] = previous_hash
        item["step_hash"] = _native_trace_hash(item)
        previous_hash = item["step_hash"]
    path.write_text(
        "".join(json.dumps(item, sort_keys=True) + "\n" for item in records),
        encoding="utf-8",
    )
    return path


def _build_root(
    tmp_path: Path,
    trace: Path,
    *,
    status: str = "FINITE_NUMERICAL_SHADOW_CLOSED",
    refusal_codes: tuple[str, ...] = (),
    obligations: tuple[str, ...] = (),
    extra_artifacts: tuple[ArtifactRefV1, ...] = (),
) -> ResearchRunRootV1:
    source_path = tmp_path / "protocol-source.txt"
    source_path.write_text("bounded source\n", encoding="utf-8")
    source = build_source_artifact(
        tmp_path,
        source_id="RUN-ROOT-SOURCE",
        path="protocol-source.txt",
        role="test_fixture",
        normalization="utf8-lf-v1",
        repository_tracked_expected=True,
    )
    initial_state = {"fixture": "bounded"}
    payload = ResearchClaimPayloadV1(
        family=WITTEN_FINITE_FAMILY,
        disposition=EVALUATE_FINITE,
        sources=(source,),
        claims=(
            ResearchClaimV1(
                claim_id="RUN-ROOT-FINITE-CLAIM",
                statement="Close the bounded run-root fixture.",
                disposition=EVALUATE_FINITE,
                source_ids=(source.source_id,),
                assumptions=("fixed fixture",),
                units="dimensionless",
                carrier="one bounded fixture",
                coefficient_semantics="exact strings",
                projection="identity fixture projection",
                retraction="identity fixture retraction",
                obstruction="nonzero fixture residual",
                detector="positive and negative fixture controls",
                comparison_map="identity",
                falsifier="a residual mismatch",
                independent_checker="strict run-root replay",
                unresolved_obligations=(),
                evidence_ceiling=LOCAL_REPLAYABLE_FINITE_EVIDENCE,
            ),
        ),
        initial_state_payload=initial_state,
    )
    envelope = build_research_claim_envelope(
        payload,
        "run-root-fixture",
        RESEARCH_FAMILY_OWNER_LAWS[WITTEN_FINITE_FAMILY][0],
        initial_state,
        RESEARCH_FAMILY_OWNER_LAWS[WITTEN_FINITE_FAMILY][1],
        1,
    )
    intake = build_source_intake_bundle(envelope, tmp_path)
    packet_path = write_content_addressed_json(
        tmp_path,
        "run_root_packet",
        envelope.to_dict(),
    )
    intake_path = write_content_addressed_json(
        tmp_path,
        "run_root_intake",
        intake.to_dict(),
    )
    trace_ref = artifact_ref_from_path(
        trace,
        tmp_path,
        media_type=DDA_TRACE_MEDIA_TYPE,
    )
    protocol_refs = (
        artifact_ref_from_path(
            packet_path,
            tmp_path,
            media_type=RESEARCH_PACKET_MEDIA_TYPE,
        ),
        artifact_ref_from_path(
            intake_path,
            tmp_path,
            media_type=SOURCE_INTAKE_MEDIA_TYPE,
        ),
    )
    return build_research_run_root(
        trace_path=trace,
        claim_packet_id=envelope.packet_id,
        family_id=payload.family,
        source_manifest_root=payload.source_manifest_root,
        claim_manifest_root=payload.claim_manifest_root,
        source_intake_receipt_id=intake.receipt_id,
        terminal_status=status,
        artifact_manifest=(*protocol_refs, *extra_artifacts, trace_ref),
        refusal_codes=refusal_codes,
        unresolved_obligations=obligations,
        evidence_profile=(
            "RefusalOnly" if status == "REFUSED" else "LocalReplayableFiniteEvidence"
        ),
    )


def test_strict_roundtrip_writer_and_artifact_verification(tmp_path: Path) -> None:
    trace = _write_trace(
        tmp_path / "traces" / "finite.jsonl",
        _record(
            run_id="a1b2c3d4e5f6",
            timestamp="2026-08-06T12:00:00+00:00",
            trace_path="C:/tmp/one/finite.jsonl",
            challenge="challenge-one",
            uuid_hex="1234567812344abc8def1234567890ab",
        ),
    )
    claim = tmp_path / "packets" / "claim.json"
    claim.parent.mkdir(parents=True)
    claim.write_text('{"claim":"finite"}\n', encoding="utf-8")
    root = _build_root(
        tmp_path,
        trace,
        extra_artifacts=(
            artifact_ref_from_path(
                claim, tmp_path, media_type="application/json", required=True
            ),
        ),
    )

    assert ResearchRunRootV1.from_dict(root.to_dict()) == root
    assert verify_research_run_root(root, tmp_path)
    output = write_research_run_root(root, tmp_path / "roots")
    assert (
        output.stem.rsplit("_", 1)[-1]
        == hashlib.sha256(output.read_bytes()).hexdigest()
    )
    assert read_research_run_root(output) == root
    assert write_research_run_root(root, tmp_path / "roots") == output


def test_optional_protocol_media_cannot_usurp_required_packet(tmp_path: Path) -> None:
    trace = _write_trace(
        tmp_path / "trace.jsonl",
        _record(
            run_id="a1b2c3d4e5f6",
            timestamp="2026-08-06T12:00:00+00:00",
            trace_path="C:/tmp/trace.jsonl",
            challenge="challenge",
            uuid_hex="1234567812344abc8def1234567890ab",
        ),
    )
    decoy = tmp_path / "000_optional_packet.json"
    decoy.write_text("{}\n", encoding="utf-8")
    root = _build_root(
        tmp_path,
        trace,
        extra_artifacts=(
            artifact_ref_from_path(
                decoy,
                tmp_path,
                media_type=RESEARCH_PACKET_MEDIA_TYPE,
                required=False,
            ),
        ),
    )

    assert verify_research_run_root(root, tmp_path)


def test_terminal_profile_source_and_obligation_laundering_fail_closed(
    tmp_path: Path,
) -> None:
    trace = _write_trace(
        tmp_path / "trace.jsonl",
        _record(
            run_id="a1b2c3d4e5f6",
            timestamp="2026-08-06T12:00:00+00:00",
            trace_path="C:/tmp/trace.jsonl",
            challenge="challenge",
            uuid_hex="1234567812344abc8def1234567890ab",
        ),
    )
    root = _build_root(tmp_path, trace)

    with pytest.raises(ResearchRunRootError, match="terminal_status"):
        replace(root, terminal_status="THEOREM_PROVED")
    forged_refusal = replace(
        root,
        terminal_status="REFUSED",
        evidence_profile="RefusalOnly",
        refusal_codes=("FORGED_REFUSAL",),
    )
    with pytest.raises(ResearchRunRootError, match="typed Z refusal"):
        verify_research_run_root(forged_refusal, tmp_path)
    forged_source_status = replace(
        root,
        terminal_status="FINITE_NUMERICAL_SHADOW_CLOSED_SOURCE_UNVERIFIED",
    )
    with pytest.raises(ResearchRunRootError, match="source verification state"):
        verify_research_run_root(forged_source_status, tmp_path)
    forged_obligation = replace(root, unresolved_obligations=("FORGED_GAP",))
    with pytest.raises(ResearchRunRootError, match="obligations"):
        verify_research_run_root(forged_obligation, tmp_path)


def test_native_trace_hash_chain_is_recomputed(tmp_path: Path) -> None:
    trace = _write_trace(
        tmp_path / "trace.jsonl",
        _record(
            run_id="a1b2c3d4e5f6",
            timestamp="2026-08-06T12:00:00+00:00",
            trace_path="C:/tmp/trace.jsonl",
            challenge="challenge",
            uuid_hex="1234567812344abc8def1234567890ab",
        ),
    )
    records = [json.loads(line) for line in trace.read_text("utf-8").splitlines()]
    records[1]["prev_step_hash"] = "0" * 64
    records[1]["step_hash"] = _native_trace_hash(records[1])
    trace.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )

    with pytest.raises(ResearchRunRootError, match="prev_step_hash chain"):
        semantic_dda_from_trace(trace)


def test_occurrence_uuid_timestamp_and_path_do_not_change_semantic_root(
    tmp_path: Path,
) -> None:
    first = _write_trace(
        tmp_path / "first.jsonl",
        _record(
            run_id="aaaaaaaaaaaa",
            timestamp="2026-08-06T00:00:01+00:00",
            trace_path="C:/tmp/first/trace.jsonl",
            challenge="challenge-alpha",
            uuid_hex="aaaaaaaaaaaa4aaa8aaaaaaaaaaaaaaa",
        ),
    )
    second = _write_trace(
        tmp_path / "nested" / "second.jsonl",
        _record(
            run_id="bbbbbbbbbbbb",
            timestamp="2031-01-02T03:04:05+00:00",
            trace_path="D:/different/location/trace.jsonl",
            challenge="challenge-beta",
            uuid_hex="bbbbbbbbbbbb4bbb8bbbbbbbbbbbbbbb",
        ),
    )

    first_steps, first_root = semantic_dda_from_trace(first)
    second_steps, second_root = semantic_dda_from_trace(second)

    assert first_steps == second_steps
    assert first_root == second_root
    assert first_steps[0].residual_before_hex == float(1.0).hex()
    assert first_steps[0].residual_after_hex == float(0.0).hex()


def test_occurrence_value_cannot_erase_matching_semantic_value(tmp_path: Path) -> None:
    first = _write_trace(
        tmp_path / "semantic-one.jsonl",
        _record(
            run_id="aaaaaaaaaaaa",
            timestamp="2026-08-06T00:00:01+00:00",
            trace_path="semantic-alpha",
            challenge="challenge-alpha",
            uuid_hex="aaaaaaaaaaaa4aaa8aaaaaaaaaaaaaaa",
            semantic_value="semantic-alpha",
        ),
    )
    second = _write_trace(
        tmp_path / "semantic-two.jsonl",
        _record(
            run_id="bbbbbbbbbbbb",
            timestamp="2031-01-02T03:04:05+00:00",
            trace_path="semantic-beta",
            challenge="challenge-beta",
            uuid_hex="bbbbbbbbbbbb4bbb8bbbbbbbbbbbbbbb",
            semantic_value="semantic-beta",
        ),
    )

    assert semantic_dda_from_trace(first)[1] != semantic_dda_from_trace(second)[1]


@pytest.mark.parametrize(
    ("mutation", "value"),
    (
        ("letter", "R"),
        ("operation", "refuse:finite-obstruction"),
        ("residual_after", 0.5),
        ("semantic_value", "still-open"),
    ),
)
def test_each_semantic_mutation_changes_the_chain_root(
    tmp_path: Path,
    mutation: str,
    value: Any,
) -> None:
    base_arguments: dict[str, Any] = {
        "run_id": "a1b2c3d4e5f6",
        "timestamp": "2026-08-06T12:00:00+00:00",
        "trace_path": "C:/tmp/trace.jsonl",
        "challenge": "challenge-one",
        "uuid_hex": "1234567812344abc8def1234567890ab",
    }
    base = _write_trace(tmp_path / "base.jsonl", _record(**base_arguments))
    mutated_arguments = dict(base_arguments)
    mutated_arguments[mutation] = value
    mutated = _write_trace(
        tmp_path / f"mutated-{mutation}.jsonl", _record(**mutated_arguments)
    )

    assert semantic_dda_from_trace(base)[1] != semantic_dda_from_trace(mutated)[1]


@pytest.mark.parametrize("nonfinite", (float("nan"), float("inf"), -float("inf")))
def test_nonfinite_residuals_fail_closed(tmp_path: Path, nonfinite: float) -> None:
    trace = _write_trace(
        tmp_path / "nonfinite.jsonl",
        _record(
            run_id="a1b2c3d4e5f6",
            timestamp="2026-08-06T12:00:00+00:00",
            trace_path="C:/tmp/trace.jsonl",
            challenge="challenge",
            uuid_hex="1234567812344abc8def1234567890ab",
            residual_before=nonfinite,
        ),
    )

    with pytest.raises(ResearchRunRootError, match="non-finite|finite"):
        semantic_dda_from_trace(trace)


def test_missing_changed_and_dangling_artifacts_fail_closed(tmp_path: Path) -> None:
    trace = _write_trace(
        tmp_path / "trace.jsonl",
        _record(
            run_id="a1b2c3d4e5f6",
            timestamp="2026-08-06T12:00:00+00:00",
            trace_path="C:/tmp/trace.jsonl",
            challenge="challenge",
            uuid_hex="1234567812344abc8def1234567890ab",
        ),
    )
    root = _build_root(tmp_path, trace)
    original = trace.read_bytes()

    trace.unlink()
    with pytest.raises(ResearchRunRootError, match="artifact is missing"):
        verify_research_run_root(root, tmp_path)

    trace.write_bytes(original + b" ")
    with pytest.raises(ResearchRunRootError, match="byte count changed"):
        verify_research_run_root(root, tmp_path)

    wire = root.to_dict()
    wire["semantic_trace_label"] = "traces/dangling.jsonl"
    wire["root_id"] = _digest("attacker-cannot-recompute-via-decoder")
    with pytest.raises(ResearchRunRootError, match="semantic_trace_label"):
        ResearchRunRootV1.from_dict(wire)

    with pytest.raises(ResearchRunRootError, match="required artifacts"):
        ArtifactRefV1(
            label="missing.json",
            media_type="application/json",
            content_sha256=_digest("missing"),
            byte_count=0,
            required=True,
            availability="MISSING",
        )


def test_rehashed_trace_substitution_cannot_detach_semantic_root(
    tmp_path: Path,
) -> None:
    trace = _write_trace(
        tmp_path / "trace.jsonl",
        _record(
            run_id="a1b2c3d4e5f6",
            timestamp="2026-08-06T12:00:00+00:00",
            trace_path="C:/tmp/trace.jsonl",
            challenge="challenge",
            uuid_hex="1234567812344abc8def1234567890ab",
        ),
    )
    original_root = _build_root(tmp_path, trace)

    _write_trace(
        trace,
        _record(
            run_id="cccccccccccc",
            timestamp="2027-01-01T00:00:00+00:00",
            trace_path="C:/tmp/substitute.jsonl",
            challenge="new-challenge",
            uuid_hex="cccccccccccc4ccc8ccccccccccccccc",
            semantic_value="unrelated-result",
        ),
    )
    substituted_ref = artifact_ref_from_path(
        trace,
        tmp_path,
        media_type=DDA_TRACE_MEDIA_TYPE,
    )
    detached = replace(
        original_root,
        artifact_manifest=tuple(
            sorted(
                (
                    *(
                        ref
                        for ref in original_root.artifact_manifest
                        if ref.label != original_root.semantic_trace_label
                    ),
                    substituted_ref,
                ),
                key=lambda ref: ref.label,
            )
        ),
    )

    # The attacker can recompute the outer root after rebinding the bytes, but
    # cannot make those unrelated semantic steps agree with the retained root.
    assert detached.root_id != original_root.root_id
    with pytest.raises(ResearchRunRootError, match="semantic trace does not match"):
        verify_research_run_root(detached, tmp_path)


def test_packet_intake_and_run_root_cross_bindings_are_replayed(
    tmp_path: Path,
) -> None:
    trace = _write_trace(
        tmp_path / "cross-binding.jsonl",
        _record(
            run_id="a1b2c3d4e5f6",
            timestamp="2026-08-06T12:00:00+00:00",
            trace_path="C:/tmp/cross-binding.jsonl",
            challenge="challenge",
            uuid_hex="1234567812344abc8def1234567890ab",
        ),
    )
    root = _build_root(tmp_path, trace)

    for field_name in (
        "claim_packet_id",
        "source_manifest_root",
        "claim_manifest_root",
        "source_intake_receipt_id",
    ):
        forged = replace(root, **{field_name: _digest(f"forged:{field_name}")})
        with pytest.raises(ResearchRunRootError, match="do not reconcile"):
            verify_research_run_root(forged, tmp_path)

    wrong_family = replace(root, family_id="gr_stretch_claims_v1")
    with pytest.raises(ResearchRunRootError, match="do not reconcile"):
        verify_research_run_root(wrong_family, tmp_path)


def test_rehashed_intake_receipt_must_match_each_packet_source(tmp_path: Path) -> None:
    trace = _write_trace(
        tmp_path / "receipt-source-binding.jsonl",
        _record(
            run_id="a1b2c3d4e5f6",
            timestamp="2026-08-06T12:00:00+00:00",
            trace_path="C:/tmp/receipt-source-binding.jsonl",
            challenge="challenge",
            uuid_hex="1234567812344abc8def1234567890ab",
        ),
    )
    root = _build_root(tmp_path, trace)
    intake_ref = next(
        ref
        for ref in root.artifact_manifest
        if ref.media_type == SOURCE_INTAKE_MEDIA_TYPE
    )
    intake = SourceIntakeBundleV1.from_dict(
        json.loads((tmp_path / intake_ref.label).read_text("utf-8"))
    )
    forged_receipt = replace(intake.receipts[0], path="forged-source.txt")
    forged_intake = replace(intake, receipts=(forged_receipt,))
    forged_path = write_content_addressed_json(
        tmp_path,
        "forged_intake",
        forged_intake.to_dict(),
    )
    forged_ref = artifact_ref_from_path(
        forged_path,
        tmp_path,
        media_type=SOURCE_INTAKE_MEDIA_TYPE,
    )
    forged_root = replace(
        root,
        source_intake_receipt_id=forged_intake.receipt_id,
        artifact_manifest=tuple(
            sorted(
                (
                    *(
                        ref
                        for ref in root.artifact_manifest
                        if ref.media_type != SOURCE_INTAKE_MEDIA_TYPE
                    ),
                    forged_ref,
                ),
                key=lambda ref: ref.label,
            )
        ),
    )

    with pytest.raises(ResearchRunRootError, match="receipts do not reconcile"):
        verify_research_run_root(forged_root, tmp_path)


def test_order_duplicates_unknown_fields_and_unsorted_refusals_are_rejected(
    tmp_path: Path,
) -> None:
    trace = _write_trace(
        tmp_path / "z-trace.jsonl",
        _record(
            run_id="a1b2c3d4e5f6",
            timestamp="2026-08-06T12:00:00+00:00",
            trace_path="C:/tmp/trace.jsonl",
            challenge="challenge",
            uuid_hex="1234567812344abc8def1234567890ab",
        ),
    )
    auxiliary = tmp_path / "a-packet.json"
    auxiliary.write_text("{}\n", encoding="utf-8")
    aux_ref = artifact_ref_from_path(auxiliary, tmp_path, media_type="application/json")
    root = _build_root(tmp_path, trace, extra_artifacts=(aux_ref,))
    trace_ref = next(
        ref for ref in root.artifact_manifest if ref.label == "z-trace.jsonl"
    )

    with pytest.raises(ResearchRunRootError, match="sorted by label"):
        replace(root, artifact_manifest=(trace_ref, aux_ref))
    with pytest.raises(ResearchRunRootError, match="duplicate labels"):
        replace(root, artifact_manifest=(trace_ref, trace_ref))
    with pytest.raises(ResearchRunRootError, match="refusal_codes must be sorted"):
        replace(root, refusal_codes=("Z_SECOND", "A_FIRST"))
    with pytest.raises(ResearchRunRootError, match="must not contain duplicates"):
        replace(root, refusal_codes=("Z_DUPLICATE", "Z_DUPLICATE"))

    wire = root.to_dict()
    wire["unknown"] = "smuggled"
    with pytest.raises(ResearchRunRootError, match="unknown fields"):
        ResearchRunRootV1.from_dict(wire)
    step_wire = semantic_dda_from_trace(trace)[0][0].to_dict()
    step_wire["unknown"] = "smuggled"
    with pytest.raises(ResearchRunRootError, match="unknown fields"):
        SemanticDdaStepV1.from_dict(step_wire)


def test_builder_sorts_refusal_codes_and_success_refusal_roots_are_distinct(
    tmp_path: Path,
) -> None:
    trace = _write_trace(
        tmp_path / "trace.jsonl",
        _record(
            run_id="a1b2c3d4e5f6",
            timestamp="2026-08-06T12:00:00+00:00",
            trace_path="C:/tmp/trace.jsonl",
            challenge="challenge",
            uuid_hex="1234567812344abc8def1234567890ab",
        ),
    )
    success = _build_root(tmp_path, trace)
    refusal = _build_root(
        tmp_path,
        trace,
        status="REFUSED",
        refusal_codes=("Z_UNSUPPORTED", "A_SOURCE_GAP"),
        obligations=("VERIFY_SOURCE", "BUILD_COMPARISON_MAP"),
    )

    assert refusal.refusal_codes == ("A_SOURCE_GAP", "Z_UNSUPPORTED")
    assert refusal.unresolved_obligations == (
        "BUILD_COMPARISON_MAP",
        "VERIFY_SOURCE",
    )
    assert refusal.root_id != success.root_id


def test_trace_unknown_fields_and_duplicate_json_keys_fail_closed(
    tmp_path: Path,
) -> None:
    record = _record(
        run_id="a1b2c3d4e5f6",
        timestamp="2026-08-06T12:00:00+00:00",
        trace_path="C:/tmp/trace.jsonl",
        challenge="challenge",
        uuid_hex="1234567812344abc8def1234567890ab",
    )
    record["semantic_smuggling"] = "not declared"
    unknown = _write_trace(tmp_path / "unknown.jsonl", record)
    with pytest.raises(ResearchRunRootError, match="unknown fields"):
        semantic_dda_from_trace(unknown)

    duplicate = tmp_path / "duplicate.jsonl"
    duplicate.write_text('{"schema_version":"a","schema_version":"b"}\n', "utf-8")
    with pytest.raises(ResearchRunRootError, match="duplicate JSON key"):
        semantic_dda_from_trace(duplicate)


