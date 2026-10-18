from __future__ import annotations

from collections import OrderedDict
from copy import deepcopy
from dataclasses import dataclass, replace
from enum import Enum, IntEnum
import json
from pathlib import Path

import pytest

from omega_engine_pfp.domain.shared_kernel import canonical as canonical_module
from omega_engine_pfp.domain.shared_kernel.canonical import (
    CanonicalizationError,
    canonical_unwire,
    canonical_wire,
    domain_digest,
    freeze,
)
from omega_engine_pfp.fixtures import (
    ExhaustiveCspSolver,
    NoOpClaimingSolver,
    build_demo_problem,
)
from omega_engine_pfp.domain.entities.obstruction import verify_event_chain
from omega_engine.crates.engine.eng_symbol_game import OesosLab
from omega_engine_pfp.domain.entities.candidate_artifact import (
    CANDIDATE_SCHEMA,
    CandidateArtifactV1,
)
from omega_engine_pfp.domain.entities.packet_envelope import (
    PACKET_SCHEMA,
    EvaluationReceiptV1,
    PacketEnvelopeV2,
)


class ExampleEnum(Enum):
    ONE = 1


class ExampleStrEnum(str, Enum):
    VALUE = "same"


class ExampleIntEnum(IntEnum):
    ONE = 1


@dataclass(frozen=True)
class ExampleDataclass:
    x: int


@dataclass(frozen=True)
class PrivateAuthorityDataclass:
    x: int
    _authority: str


def test_packet_identity_binds_schema_kind_and_payload() -> None:
    envelope = build_demo_problem().envelope

    assert envelope.schema_version == PACKET_SCHEMA
    assert (
        replace(
            envelope, schema_version="omega.symbol-game.packet-envelope.v3"
        ).packet_id
        != envelope.packet_id
    )
    assert replace(envelope, packet_kind="candidate").packet_id != envelope.packet_id
    assert replace(envelope, payload={"tampered": True}).packet_id != envelope.packet_id


def test_non_finite_packet_payload_fails_closed() -> None:
    envelope = build_demo_problem().envelope

    with pytest.raises(CanonicalizationError):
        replace(envelope, payload={"mass": float("nan")})


def test_wire_receipt_binds_candidate_metadata_and_event_root() -> None:
    problem = build_demo_problem()
    run = OesosLab((NoOpClaimingSolver(), ExhaustiveCspSolver())).solve(problem)
    wire = run.to_wire_receipt()

    assert run.locally_resolved
    assert wire.replay_required
    assert wire.packet_id == problem.envelope.packet_id
    assert wire.event_root == run.event_root
    assert len(wire.candidate_ids) == 2
    assert len(wire.attempts) == 2
    assert wire.attempts[0].solver_id == "candidate-claim-only"
    assert not wire.attempts[0].accepted
    assert wire.attempts[1].accepted
    assert wire.transport_valid()
    assert type(wire).from_dict(wire.to_dict()).receipt_id == wire.receipt_id
    assert len(wire.receipt_id) == 64


@pytest.mark.parametrize(
    "change",
    (
        {"event_root": "0" * 64},
        {"event_root": "not-a-digest"},
        {"packet_id": "not-a-digest"},
        {"input_state_hash": "not-a-digest"},
        {"output_state_hash": "not-a-digest"},
        {"attempts": ()},
        {"solver_registry_hash": "1" * 64},
        {"authority_effect": "Promote"},
    ),
)
def test_run_receipt_admission_reconciles_evidence_root(
    change: dict[str, object],
) -> None:
    run = OesosLab((NoOpClaimingSolver(), ExhaustiveCspSolver())).solve(
        build_demo_problem()
    )
    forged = replace(run, **change)

    assert not forged.locally_resolved
    assert not forged.evidence_valid()
    with pytest.raises(ValueError, match="committed evidence"):
        forged.to_wire_receipt()


def test_canonical_tags_cannot_be_forged_by_user_sequences_or_mappings() -> None:
    tagged_sequence = ["__map__", ["x", 1]]
    mapping = {"x": 1}
    float_mimic = {"$float_hex": (1.0).hex()}

    assert domain_digest("collision-test", tagged_sequence) != domain_digest(
        "collision-test", mapping
    )
    assert domain_digest("collision-test", 1.0) != domain_digest(
        "collision-test", float_mimic
    )
    assert domain_digest("collision-test", {1}) != domain_digest("collision-test", [1])
    assert domain_digest("collision-test", [1]) != domain_digest("collision-test", (1,))
    assert domain_digest("collision-test", ExampleEnum.ONE) != domain_digest(
        "collision-test", 1
    )
    assert domain_digest("collision-test", ExampleStrEnum.VALUE) != domain_digest(
        "collision-test", "same"
    )
    assert domain_digest("collision-test", ExampleIntEnum.ONE) != domain_digest(
        "collision-test", 1
    )
    assert domain_digest("collision-test", ExampleDataclass(1)) != domain_digest(
        "collision-test", {"x": 1}
    )
    with pytest.raises(CanonicalizationError):
        domain_digest("collision-test", OrderedDict((("x", 1),)))
    assert freeze(freeze(mapping)) == freeze(mapping)


def test_builtin_subclasses_and_subclassed_mapping_keys_are_refused() -> None:
    class MutableList(list):
        pass

    class MutableTuple(tuple):
        pass

    class MutableString(str):
        pass

    class MutableInt(int):
        pass

    values = (
        MutableList((1, 2)),
        MutableTuple((1, 2)),
        MutableString("same"),
        MutableInt(1),
    )
    for value in values:
        value.hidden_authority = "Promote"
        with pytest.raises(CanonicalizationError, match="subclasses"):
            canonical_wire(value)

    key = MutableString("x")
    key.hidden_authority = "Promote"
    with pytest.raises(CanonicalizationError, match="exact strings"):
        canonical_wire({key: 1})


def test_dataclass_and_enum_undeclared_instance_state_is_refused() -> None:
    @dataclass
    class MutableDataclass:
        x: int

    class MutableEnum(Enum):
        ONE = 1

    dataclass_value = MutableDataclass(1)
    dataclass_value.hidden_authority = "Promote"
    MutableEnum.ONE.hidden_authority = "Promote"

    with pytest.raises(CanonicalizationError, match="undeclared instance"):
        canonical_wire(dataclass_value)
    with pytest.raises(CanonicalizationError, match="undeclared instance"):
        canonical_wire(MutableEnum.ONE)


def test_private_dataclass_fields_are_identity_bearing() -> None:
    baseline = PrivateAuthorityDataclass(1, "None")
    elevated = PrivateAuthorityDataclass(1, "Promote")

    assert domain_digest("private-field", baseline) != domain_digest(
        "private-field", elevated
    )
    assert canonical_unwire(canonical_wire(baseline)) == freeze(baseline)


@pytest.mark.parametrize(
    "frozen",
    (
        canonical_module._FrozenValue("undeclared", ()),
        canonical_module._FrozenValue("fraction", (2, 4)),
        canonical_module._FrozenValue("field", ()),
    ),
)
def test_canonical_wire_refuses_caller_forged_frozen_nodes(
    frozen: object,
) -> None:
    with pytest.raises(CanonicalizationError):
        canonical_wire(frozen)


def test_packet_and_candidate_canonical_wire_round_trip_identity() -> None:
    packet = build_demo_problem().envelope
    candidate = CandidateArtifactV1(
        packet_id=packet.packet_id,
        producer_id="roundtrip-control",
        payload={"float": 1.0, "tuple": (1, 2)},
        witness="canonical-wire-roundtrip",
        metadata={"bytes": b"omega"},
    )

    assert PacketEnvelopeV2.from_dict(packet.to_dict()).packet_id == packet.packet_id
    assert (
        CandidateArtifactV1.from_dict(candidate.to_dict()).candidate_id
        == candidate.candidate_id
    )
    assert candidate.to_dict()["payload"] != {"$float_hex": (1.0).hex()}


@pytest.mark.parametrize(
    "wire",
    (
        ["omega-canonical-v1", "undeclared", []],
        [
            "omega-canonical-v1",
            "float",
            [canonical_wire("0x1p+0")],
        ],
        [
            "omega-canonical-v1",
            "fraction",
            [canonical_wire(2), canonical_wire(4)],
        ],
        [
            "omega-canonical-v1",
            "bytes",
            [canonical_wire("FF")],
        ],
    ),
)
def test_canonical_unwire_refuses_unknown_or_non_normalized_tags(
    wire: object,
) -> None:
    with pytest.raises(CanonicalizationError):
        canonical_unwire(wire)


def test_canonical_unwire_refuses_unordered_mapping_entries() -> None:
    wire = canonical_wire({"a": 1, "b": 2})
    wire[2][2], wire[2][3] = wire[2][3], wire[2][2]

    with pytest.raises(CanonicalizationError, match="unique and ordered"):
        canonical_unwire(wire)


def test_packet_parser_refuses_coercion_and_unknown_fields() -> None:
    envelope = build_demo_problem().envelope
    string_task = replace(envelope, task_id="17").to_dict()
    string_task["task_id"] = 17
    string_constraint = replace(envelope, constraints=("1",)).to_dict()
    string_constraint["constraints"] = [1]
    string_budget = envelope.to_dict()
    string_budget["step_budget"] = str(envelope.step_budget)
    boolean_budget = replace(envelope, step_budget=1).to_dict()
    boolean_budget["step_budget"] = True
    unknown_field = envelope.to_dict()
    unknown_field["uncommitted_hint"] = "ignore me"

    for wire in (
        string_task,
        string_constraint,
        string_budget,
        boolean_budget,
        unknown_field,
    ):
        with pytest.raises(CanonicalizationError):
            PacketEnvelopeV2.from_dict(wire)


def test_candidate_parser_refuses_coercion_invalid_claim_types_and_extras() -> None:
    packet_id = build_demo_problem().envelope.packet_id
    candidate = CandidateArtifactV1(
        packet_id=packet_id,
        producer_id="17",
        payload={"candidate": 1},
        witness="strict-candidate-parser",
    )
    numeric_producer = candidate.to_dict()
    numeric_producer["producer_id"] = 17
    invalid_claim = CandidateArtifactV1(
        packet_id=packet_id,
        producer_id="strict-candidate-parser",
        payload={"candidate": 1},
        witness="invalid-claim-type",
        claimed_valid="false",  # type: ignore[arg-type]
    ).to_dict()
    unknown_field = candidate.to_dict()
    unknown_field["uncommitted_hint"] = "ignore me"

    for wire in (numeric_producer, invalid_claim, unknown_field):
        with pytest.raises(CanonicalizationError):
            CandidateArtifactV1.from_dict(wire)


def test_evaluation_parser_refuses_truthiness_coercion_and_extras() -> None:
    run = OesosLab((NoOpClaimingSolver(), ExhaustiveCspSolver())).solve(
        build_demo_problem()
    )
    valid = run.to_wire_receipt().to_dict()
    replay_string = deepcopy(valid)
    replay_string["replay_required"] = "false"
    accepted_string = deepcopy(valid)
    accepted_string["attempts"][0]["accepted"] = "false"
    numeric_obstruction = deepcopy(valid)
    numeric_obstruction["active_obstructions"] = [7]
    tuple_attempts = deepcopy(valid)
    tuple_attempts["attempts"] = tuple(tuple_attempts["attempts"])
    unknown_field = deepcopy(valid)
    unknown_field["uncommitted_hint"] = "ignore me"
    unknown_attempt_field = deepcopy(valid)
    unknown_attempt_field["attempts"][0]["uncommitted_hint"] = "ignore me"

    for wire in (
        replay_string,
        accepted_string,
        numeric_obstruction,
        tuple_attempts,
        unknown_field,
        unknown_attempt_field,
    ):
        with pytest.raises(CanonicalizationError):
            EvaluationReceiptV1.from_dict(wire)


def test_process_event_chain_detects_tampering() -> None:
    run = OesosLab((NoOpClaimingSolver(), ExhaustiveCspSolver())).solve(
        build_demo_problem()
    )
    events = run.process_events

    assert verify_event_chain(events)
    tampered = list(events)
    tampered[1] = replace(tampered[1], output_state_hash=domain_digest("tamper", 1))
    assert not verify_event_chain(tuple(tampered))


def test_parent_event_is_bound_into_the_cross_run_chain() -> None:
    problem = build_demo_problem()
    parent = "f" * 64
    linked = replace(
        problem, envelope=replace(problem.envelope, parent_event_id=parent)
    )
    run = OesosLab((ExhaustiveCspSolver(),)).solve(linked)

    assert run.locally_resolved
    assert run.process_events[0].parent_hash == parent
    assert verify_event_chain(run.process_events, parent)
    assert not verify_event_chain(run.process_events)
    assert run.to_wire_receipt().parent_event_id == parent


def _find_schema_dir() -> Path:
    cur = Path(__file__).resolve().parent
    for _ in range(10):
        t0 = cur / "crates" / "symbol_game" / "schemas"
        if t0.exists():
            return t0
        t1 = cur / "omega_engine" / "crates" / "symbol_game" / "schemas"
        if t1.exists():
            return t1
        t2 = cur / "schemas"
        if t2.exists():
            return t2
        if cur.parent == cur:
            break
        cur = cur.parent
    return (
        Path(__file__).resolve().parent.parent
        / "crates"
        / "symbol_game"
        / "schemas"
    )


def test_published_lab_schemas_match_runtime_versions() -> None:
    schema_dir = _find_schema_dir()
    packet_schema = json.loads(
        (schema_dir / "schema_packet_envelope_v2.schema.json").read_text(encoding="utf-8")
    )
    receipt_schema = json.loads(
        (schema_dir / "schema_evaluation_receipt_v1.schema.json").read_text(encoding="utf-8")
    )
    candidate_schema = json.loads(
        (schema_dir / "schema_candidate_artifact_v1.schema.json").read_text(encoding="utf-8")
    )

    assert packet_schema["$id"] == PACKET_SCHEMA
    assert packet_schema["properties"]["authority_effect"]["const"] == "None"
    assert "initial_state_hash" in packet_schema["required"]
    assert receipt_schema["$id"] == "omega.oesos.evaluation-receipt.v1"
    assert receipt_schema["properties"]["replay_required"]["const"] is True
    assert "attempts" in receipt_schema["required"]
    assert candidate_schema["$id"] == CANDIDATE_SCHEMA


def test_runtime_transport_dicts_validate_against_published_schemas() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema_dir = _find_schema_dir()
    problem = build_demo_problem()
    run = OesosLab((NoOpClaimingSolver(), ExhaustiveCspSolver())).solve(problem)
    candidate = CandidateArtifactV1(
        packet_id=problem.envelope.packet_id,
        producer_id="schema-control",
        payload=(("x", 1), ("y", 1)),
        witness="schema-validation-control",
    )

    jsonschema.validate(
        problem.envelope.to_dict(),
        json.loads(
            (schema_dir / "schema_packet_envelope_v2.schema.json").read_text(encoding="utf-8")
        ),
    )
    jsonschema.validate(
        candidate.to_dict(),
        json.loads(
            (schema_dir / "schema_candidate_artifact_v1.schema.json").read_text(
                encoding="utf-8"
            )
        ),
    )
    jsonschema.validate(
        run.to_wire_receipt().to_dict(),
        json.loads(
            (schema_dir / "schema_evaluation_receipt_v1.schema.json").read_text(
                encoding="utf-8"
            )
        ),
    )


def _canonical_node_schemas() -> tuple[dict[str, object], ...]:
    schema_dir = _find_schema_dir()
    schemas = tuple(
        json.loads((schema_dir / name).read_text(encoding="utf-8"))
        for name in (
            "schema_packet_envelope_v2.schema.json",
            "schema_candidate_artifact_v1.schema.json",
        )
    )
    return tuple(
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$ref": "#/$defs/canonicalNode",
            "$defs": schema["$defs"],
        }
        for schema in schemas
    )


@pytest.mark.parametrize(
    "value",
    (
        0.0,
        -0.0,
        float.fromhex("0x0.0000000000001p-1022"),
        float.fromhex("0x1.0000000000000p-1022"),
        float.fromhex("0x1.fffffffffffffp+1023"),
    ),
)
def test_float_schema_accepts_exact_python_hex_normal_forms(value: float) -> None:
    jsonschema = pytest.importorskip("jsonschema")
    wire = canonical_wire(value)

    assert canonical_unwire(wire) == freeze(value)
    for schema in _canonical_node_schemas():
        jsonschema.validate(wire, schema)


@pytest.mark.parametrize(
    "hex_value",
    (
        "0x0.0000000000000p+0",
        "0x0.0000000000000p-1022",
        "0x0.0000000000001p-1021",
        "0x1.0000000000000p-1023",
        "0x1.0000000000000p+1024",
    ),
)
def test_float_schema_and_parser_reject_non_normal_hex_forms(
    hex_value: str,
) -> None:
    jsonschema = pytest.importorskip("jsonschema")
    wire = [
        "omega-canonical-v1",
        "float",
        [canonical_wire(hex_value)],
    ]

    with pytest.raises(CanonicalizationError):
        canonical_unwire(wire)
    for schema in _canonical_node_schemas():
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(wire, schema)


def test_mapping_schema_and_parser_require_exact_builtin_dict_tag() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    wire = canonical_wire({"x": 1})
    wire[2][0] = canonical_wire("collections")
    wire[2][1] = canonical_wire("OrderedDict")

    with pytest.raises(CanonicalizationError, match="built-in dict"):
        canonical_unwire(wire)
    for schema in _canonical_node_schemas():
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(wire, schema)


def test_published_schemas_reject_runtime_invalid_json_transports() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema_dir = _find_schema_dir()
    packet_schema = json.loads(
        (schema_dir / "schema_packet_envelope_v2.schema.json").read_text(encoding="utf-8")
    )
    candidate_schema = json.loads(
        (schema_dir / "schema_candidate_artifact_v1.schema.json").read_text(encoding="utf-8")
    )
    receipt_schema = json.loads(
        (schema_dir / "schema_evaluation_receipt_v1.schema.json").read_text(encoding="utf-8")
    )
    problem = build_demo_problem()
    run = OesosLab((NoOpClaimingSolver(), ExhaustiveCspSolver())).solve(problem)
    candidate = CandidateArtifactV1(
        packet_id=problem.envelope.packet_id,
        producer_id="schema-negative-control",
        payload={"candidate": 1},
        witness="schema-negative-control",
    )

    ordinary_packet_payload = problem.envelope.to_dict()
    ordinary_packet_payload["payload"] = {"not": "canonical-wire"}
    invalid_parent_digest = problem.envelope.to_dict()
    invalid_parent_digest["parent_event_id"] = "not-a-digest"
    ordinary_candidate_metadata = candidate.to_dict()
    ordinary_candidate_metadata["metadata"] = {"not": "canonical-wire"}
    unknown_candidate_tag = candidate.to_dict()
    unknown_candidate_tag["payload"] = [
        "omega-canonical-v1",
        "undeclared",
        [],
    ]
    duplicate_obstructions = run.to_wire_receipt().to_dict()
    duplicate_obstructions["active_obstructions"] = ["same", "same"]
    truthy_replay_flag = run.to_wire_receipt().to_dict()
    truthy_replay_flag["replay_required"] = "true"

    cases = (
        (packet_schema, PacketEnvelopeV2.from_dict, ordinary_packet_payload),
        (packet_schema, PacketEnvelopeV2.from_dict, invalid_parent_digest),
        (
            candidate_schema,
            CandidateArtifactV1.from_dict,
            ordinary_candidate_metadata,
        ),
        (candidate_schema, CandidateArtifactV1.from_dict, unknown_candidate_tag),
        (
            receipt_schema,
            EvaluationReceiptV1.from_dict,
            duplicate_obstructions,
        ),
        (receipt_schema, EvaluationReceiptV1.from_dict, truthy_replay_flag),
    )
    for schema, parser, wire in cases:
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(wire, schema)
        with pytest.raises((CanonicalizationError, ValueError)):
            parser(wire)


