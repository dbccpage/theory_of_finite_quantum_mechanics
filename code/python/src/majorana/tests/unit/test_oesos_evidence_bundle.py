"""Replay and tamper tests for strict OESOS evidence bundles."""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import replace

import pytest
from omega_engine.crates.engine.eng_symbol_game import OesosLab

from omega_engine_pfp.domain.entities.oesos_evidence_bundle import (
    OESOS_EVIDENCE_BUNDLE_SCHEMA,
    OesosEvidenceBundleError,
    OesosEvidenceBundleV1,
    RuntimeProblemIdentityV1,
    build_oesos_evidence_bundle,
    read_oesos_evidence_bundle,
    verify_oesos_evidence_bundle,
    write_oesos_evidence_bundle,
)
from omega_engine_pfp.infrastructure.adapters.research_solvers import (
    AiryNewtonProposalSolver,
    build_airy_problem,
)

PARENT_PACKET_ID = "1" * 64
SOURCE_DIGEST = "2" * 64


@pytest.fixture(scope="module")
def evidence():
    problem = build_airy_problem(
        research_parent_event_id=PARENT_PACKET_ID,
        source_digest=SOURCE_DIGEST,
    )
    run = OesosLab((AiryNewtonProposalSolver(),)).solve(problem)
    bundle = build_oesos_evidence_bundle(
        problem,
        run,
        research_parent_packet_id=PARENT_PACKET_ID,
    )
    return problem, run, bundle


def test_build_reconciles_every_requested_oesos_identity(evidence) -> None:
    problem, run, bundle = evidence
    receipt = run.to_wire_receipt()

    assert bundle.schema_version == OESOS_EVIDENCE_BUNDLE_SCHEMA
    assert bundle.authority_effect == "None"
    assert bundle.research_parent_packet_id == PARENT_PACKET_ID
    assert bundle.packet_envelope.packet_id == run.packet_id
    assert bundle.runtime_problem.runtime_id == problem.runtime_id == run.runtime_id
    assert bundle.evaluation_receipt.event_root == run.event_root
    assert bundle.wire_receipt_id == receipt.receipt_id
    assert tuple(candidate.candidate_id for candidate in bundle.candidates) == tuple(
        receipt.candidate_ids
    )
    assert bundle.process_events[-1].event_hash == receipt.event_root
    assert verify_oesos_evidence_bundle(
        bundle,
        expected_research_parent_packet_id=PARENT_PACKET_ID,
    )


def test_runtime_identity_is_exactly_recomputable_without_solver_code(evidence) -> None:
    problem, _, bundle = evidence

    reparsed = RuntimeProblemIdentityV1.from_dict(bundle.runtime_problem.to_dict())

    assert reparsed.runtime_id == problem.runtime_id
    assert reparsed.to_dict() == bundle.runtime_problem.to_dict()


def test_bundle_json_roundtrip_is_stable_and_content_addressed(evidence) -> None:
    _, _, bundle = evidence
    wire = json.loads(json.dumps(bundle.to_dict()))

    reparsed = OesosEvidenceBundleV1.from_dict(wire)

    assert reparsed.bundle_id == bundle.bundle_id
    assert reparsed.to_dict() == bundle.to_dict()


@pytest.mark.parametrize(
    ("layer", "mutate", "message"),
    (
        (
            "outer",
            lambda wire: wire.__setitem__("undeclared", True),
            "unknown fields",
        ),
        (
            "runtime",
            lambda wire: wire["runtime_problem"].__setitem__(
                "observer_id", "forged-observer"
            ),
            "runtime_id does not match",
        ),
        (
            "event-chain",
            lambda wire: wire["process_events"][0].__setitem__("event_hash", "f" * 64),
            "event chain failed replay",
        ),
        (
            "candidate",
            lambda wire: wire["candidates"][0].__setitem__(
                "producer_id", "forged-producer"
            ),
            "nested OESOS evidence transport failed",
        ),
        (
            "authority",
            lambda wire: wire["process_events"][0].__setitem__(
                "authority_effect", "Expanded"
            ),
            "authority_effect must be None",
        ),
    ),
)
def test_strict_parser_refuses_unknown_or_tampered_evidence(
    evidence,
    layer: str,
    mutate,
    message: str,
) -> None:
    del layer
    wire = copy.deepcopy(evidence[2].to_dict())
    mutate(wire)

    with pytest.raises(OesosEvidenceBundleError, match=message):
        OesosEvidenceBundleV1.from_dict(wire)


def test_parent_packet_is_not_a_free_floating_label(evidence) -> None:
    wire = copy.deepcopy(evidence[2].to_dict())
    wire["research_parent_packet_id"] = "3" * 64

    with pytest.raises(OesosEvidenceBundleError, match="research parent packet"):
        OesosEvidenceBundleV1.from_dict(wire)
    with pytest.raises(OesosEvidenceBundleError, match="different research parent"):
        verify_oesos_evidence_bundle(
            evidence[2],
            expected_research_parent_packet_id="3" * 64,
        )


def test_builder_refuses_an_internally_invalid_run(evidence) -> None:
    problem, run, _ = evidence
    forged = replace(run, event_root="f" * 64)

    with pytest.raises(
        OesosEvidenceBundleError, match="run receipt evidence is invalid"
    ):
        build_oesos_evidence_bundle(
            problem,
            forged,
            research_parent_packet_id=PARENT_PACKET_ID,
        )


def test_writer_uses_exact_content_sha_and_reuses_identical_bytes(
    evidence,
    tmp_path,
) -> None:
    bundle = evidence[2]

    first = write_oesos_evidence_bundle(bundle, tmp_path)
    second = write_oesos_evidence_bundle(bundle, tmp_path)
    content_digest = hashlib.sha256(first.read_bytes()).hexdigest()

    assert first == second
    assert first.name == f"oesos_evidence_bundle_v1_{content_digest}.json"
    assert read_oesos_evidence_bundle(first).bundle_id == bundle.bundle_id


def test_reader_refuses_duplicate_json_keys(tmp_path) -> None:
    path = tmp_path / "duplicate.json"
    path.write_text('{"schema_version":"one","schema_version":"two"}\n')

    with pytest.raises(OesosEvidenceBundleError, match="duplicate JSON key"):
        read_oesos_evidence_bundle(path)


