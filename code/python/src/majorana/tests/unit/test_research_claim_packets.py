from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import hashlib

import pytest

from omega_engine_pfp.domain.shared_kernel.canonical import (
    CanonicalizationError,
)
from omega_engine_pfp.domain import (
    EVALUATE_FINITE,
    GR_FINITE_FAMILY,
    GR_STRETCH_FAMILY,
    LOCAL_REPLAYABLE_FINITE_EVIDENCE,
    MAX_ARRAY_LENGTH,
    MAX_CLAIMS,
    MAX_SOURCES,
    MAX_STRING_LENGTH,
    REFUSAL_ONLY,
    REFUSE_UNSUPPORTED,
    RESEARCH_FAMILY_OWNER_LAWS,
    RESEARCH_PACKET_FAMILY,
    WITTEN_FINITE_FAMILY,
    WITTEN_FULL_FAMILY,
    ResearchClaimPayloadV1,
    ResearchClaimV1,
    SourceArtifactV1,
    SourceIntakeBundleV1,
    build_research_claim_envelope,
    normalize_source_bytes,
    normalized_source_digest,
    parse_research_claim_envelope,
)
from omega_engine_pfp.infrastructure.serialization import (
    write_content_addressed_json,
)
from omega_engine_pfp.use_cases.research import (
    build_source_artifact,
    build_source_intake_bundle,
    verify_source_artifact,
)


def _source(
    source_id: str = "paper",
    *,
    content: bytes = b"finite source\n",
) -> SourceArtifactV1:
    digest, byte_count = normalized_source_digest(content, "utf8-lf-v1")
    return SourceArtifactV1(
        source_id=source_id,
        path=f"research/{source_id}.txt",
        role="primary_source",
        normalization="utf8-lf-v1",
        sha256=digest,
        byte_count=byte_count,
        repository_tracked_expected=True,
    )


def _finite_claim(
    claim_id: str = "airy-critical-points", source_id: str = "paper"
) -> ResearchClaimV1:
    return ResearchClaimV1(
        claim_id=claim_id,
        statement="The declared finite carrier has the two Airy critical points.",
        disposition=EVALUATE_FINITE,
        source_ids=(source_id,),
        assumptions=("lambda-is-nonzero",),
        units="dimensionless",
        carrier="five-labelled-complex-seed-slots",
        coefficient_semantics="ieee754-finite-real-imaginary-pairs",
        projection="evaluate z squared minus one at every labelled slot",
        retraction="Newton update on each labelled slot",
        obstruction="maximum finite gradient residual",
        detector="independent gradient evaluation",
        comparison_map="slotwise identity on the fixed carrier",
        falsifier="any accepted slot has gradient residual above tolerance",
        independent_checker="direct polynomial substitution",
        unresolved_obligations=(),
        evidence_ceiling=LOCAL_REPLAYABLE_FINITE_EVIDENCE,
    )


def _refusal_claim(
    claim_id: str = "full-chern-simons", source_id: str = "paper"
) -> ResearchClaimV1:
    return ResearchClaimV1(
        claim_id=claim_id,
        statement="The full analytic-continuation theorem is requested.",
        disposition=REFUSE_UNSUPPORTED,
        source_ids=(source_id,),
        assumptions=(),
        units="",
        carrier="",
        coefficient_semantics="",
        projection="",
        retraction="",
        obstruction="",
        detector="",
        comparison_map="",
        falsifier="",
        independent_checker="",
        unresolved_obligations=(
            "external peer verification",
            "full infinite-dimensional comparison theorem",
        ),
        evidence_ceiling=REFUSAL_ONLY,
    )


def _finite_payload() -> ResearchClaimPayloadV1:
    return ResearchClaimPayloadV1(
        family=WITTEN_FINITE_FAMILY,
        disposition=EVALUATE_FINITE,
        sources=(_source(),),
        claims=(_finite_claim(),),
        initial_state_payload={
            "lambda": 1,
            "seeds": [-2.0, -0.25, 0.25, 2.0],
        },
    )


def _refusal_payload() -> ResearchClaimPayloadV1:
    return ResearchClaimPayloadV1(
        family=WITTEN_FULL_FAMILY,
        disposition=REFUSE_UNSUPPORTED,
        sources=(_source(),),
        claims=(_refusal_claim(),),
        initial_state_payload={"request": "full-theory"},
    )


def _envelope(payload: ResearchClaimPayloadV1 | None = None):
    payload = payload or _finite_payload()
    initial = (
        {"lambda": 1, "seeds": [-2.0, -0.25, 0.25, 2.0]}
        if payload.family == WITTEN_FINITE_FAMILY
        else {"request": "full-theory"}
    )
    carrier_id, protected_boundaries = RESEARCH_FAMILY_OWNER_LAWS[payload.family]
    return build_research_claim_envelope(
        payload,
        task_id="witten-finite",
        carrier_id=carrier_id,
        initial_state_payload=initial,
        protected_boundaries=protected_boundaries,
        step_budget=5,
    )


def test_payload_and_core_envelope_round_trip_canonical_wire() -> None:
    payload = _finite_payload()
    envelope = _envelope(payload)

    parsed_object = parse_research_claim_envelope(envelope)
    parsed_wire = parse_research_claim_envelope(envelope.to_dict())

    assert envelope.packet_family == RESEARCH_PACKET_FAMILY
    assert envelope.authority_effect == "None"
    assert envelope.source_digest == payload.source_manifest_root
    assert envelope.initial_state_hash == payload.initial_state_hash
    assert parsed_object == payload
    assert parsed_wire == payload
    assert parsed_wire.payload_id == payload.payload_id
    assert _envelope(parsed_wire).packet_id == envelope.packet_id


def test_lf_normalization_is_cross_platform_and_source_receipt_is_typed(
    tmp_path,
) -> None:
    lf = b"alpha\nbeta\n"
    crlf = b"alpha\r\nbeta\r\n"
    old_mac = b"alpha\rbeta\r"

    assert normalize_source_bytes(crlf, "utf8-lf-v1") == lf
    assert normalize_source_bytes(old_mac, "utf8-lf-v1") == lf
    assert normalized_source_digest(lf, "utf8-lf-v1") == (
        hashlib.sha256(lf).hexdigest(),
        len(lf),
    )
    assert normalized_source_digest(crlf, "utf8-lf-v1") == (
        hashlib.sha256(lf).hexdigest(),
        len(lf),
    )

    source_dir = tmp_path / "research"
    source_dir.mkdir()
    source_path = source_dir / "paper.txt"
    source_path.write_bytes(lf)
    source = build_source_artifact(
        tmp_path,
        source_id="paper",
        path="research/paper.txt",
        role="primary_source",
        normalization="utf8-lf-v1",
        repository_tracked_expected=False,
    )
    source_path.write_bytes(crlf)
    receipt = verify_source_artifact(source, tmp_path)

    assert receipt.available
    assert receipt.hash_matches
    assert receipt.size_matches
    assert receipt.verified
    assert receipt.repository_tracked_expected is False
    assert receipt.authority_effect == "None"


@pytest.mark.parametrize(
    "path",
    (
        "../paper.txt",
        "research/../paper.txt",
        "/research/paper.txt",
        "C:/research/paper.txt",
        r"research\paper.txt",
        "./research/paper.txt",
        "research//paper.txt",
        "research/paper.txt:shadow",
        "research/paper.",
        "research/CON",
    ),
)
def test_source_paths_refuse_traversal_absolute_and_noncanonical_forms(
    path: str,
) -> None:
    with pytest.raises(CanonicalizationError, match="POSIX path"):
        replace(_source(), path=path)


def test_source_paths_refuse_windows_trailing_space_alias() -> None:
    with pytest.raises(CanonicalizationError, match="normalized string|POSIX path"):
        replace(_source(), path="research/paper.txt ")


def test_strict_payload_parser_refuses_unknown_and_missing_fields() -> None:
    payload_wire = _finite_payload().to_dict()
    unknown = deepcopy(payload_wire)
    unknown["uncommitted_hint"] = "ignore"
    missing = deepcopy(payload_wire)
    del missing["claim_manifest_root"]
    unknown_claim = deepcopy(payload_wire)
    unknown_claim["claims"][0]["promotion_status"] = "certified"
    missing_source = deepcopy(payload_wire)
    del missing_source["sources"][0]["normalization"]

    for wire in (unknown, missing, unknown_claim, missing_source):
        with pytest.raises(CanonicalizationError):
            ResearchClaimPayloadV1.from_dict(wire)


def test_payload_refuses_duplicate_or_unordered_stable_ids() -> None:
    source_a = _source("a")
    source_b = _source("b")
    claim_a = _finite_claim("a-claim", "a")
    claim_b = _finite_claim("b-claim", "b")

    with pytest.raises(CanonicalizationError, match="unique source IDs"):
        ResearchClaimPayloadV1(
            family=GR_FINITE_FAMILY,
            disposition=EVALUATE_FINITE,
            sources=(source_a, source_a),
            claims=(claim_a,),
            initial_state_payload={},
        )
    with pytest.raises(CanonicalizationError, match="unique claim IDs"):
        ResearchClaimPayloadV1(
            family=GR_FINITE_FAMILY,
            disposition=EVALUATE_FINITE,
            sources=(source_a,),
            claims=(claim_a, claim_a),
            initial_state_payload={},
        )
    with pytest.raises(CanonicalizationError, match="sorted order"):
        ResearchClaimPayloadV1(
            family=GR_FINITE_FAMILY,
            disposition=EVALUATE_FINITE,
            sources=(source_b, source_a),
            claims=(claim_a,),
            initial_state_payload={},
        )
    with pytest.raises(CanonicalizationError, match="sorted order"):
        ResearchClaimPayloadV1(
            family=GR_FINITE_FAMILY,
            disposition=EVALUATE_FINITE,
            sources=(source_a, source_b),
            claims=(claim_b, claim_a),
            initial_state_payload={},
        )


def test_mutation_with_recomputed_packet_id_fails_source_root_binding() -> None:
    envelope = _envelope()
    tampered_payload = _finite_payload().to_dict()
    tampered_payload["sources"][0]["sha256"] = "f" * 64
    rehashed_envelope = replace(envelope, payload=tampered_payload)

    assert rehashed_envelope.packet_id != envelope.packet_id
    with pytest.raises(CanonicalizationError, match="source_manifest_root"):
        parse_research_claim_envelope(rehashed_envelope.to_dict())


def test_mutation_with_recomputed_packet_id_fails_initial_state_binding() -> None:
    envelope = _envelope()
    tampered_payload = _finite_payload().to_dict()
    alternate = ResearchClaimPayloadV1(
        family=WITTEN_FINITE_FAMILY,
        disposition=EVALUATE_FINITE,
        sources=(_source(),),
        claims=(_finite_claim(),),
        initial_state_payload={"lambda": 9, "seeds": [0.0]},
    )
    tampered_payload["initial_state_payload"] = alternate.to_dict()[
        "initial_state_payload"
    ]
    rehashed_envelope = replace(envelope, payload=tampered_payload)

    assert rehashed_envelope.packet_id != envelope.packet_id
    with pytest.raises(CanonicalizationError, match="initial_state_hash"):
        parse_research_claim_envelope(rehashed_envelope.to_dict())


@pytest.mark.parametrize(
    ("family", "disposition"),
    (
        (WITTEN_FINITE_FAMILY, REFUSE_UNSUPPORTED),
        (GR_FINITE_FAMILY, REFUSE_UNSUPPORTED),
        (WITTEN_FULL_FAMILY, EVALUATE_FINITE),
        (GR_STRETCH_FAMILY, EVALUATE_FINITE),
    ),
)
def test_family_disposition_swap_is_refused(family: str, disposition: str) -> None:
    claim = _finite_claim() if disposition == EVALUATE_FINITE else _refusal_claim()
    with pytest.raises(CanonicalizationError, match="family and disposition"):
        ResearchClaimPayloadV1(
            family=family,
            disposition=disposition,
            sources=(_source(),),
            claims=(claim,),
            initial_state_payload={},
        )


def test_finite_claim_requires_complete_mechanics_and_no_open_obligations() -> None:
    claim = _finite_claim()
    for field_name in (
        "units",
        "carrier",
        "coefficient_semantics",
        "projection",
        "retraction",
        "obstruction",
        "detector",
        "comparison_map",
        "falsifier",
        "independent_checker",
    ):
        with pytest.raises(CanonicalizationError):
            replace(claim, **{field_name: ""})
    with pytest.raises(CanonicalizationError, match="unresolved obligations"):
        replace(claim, unresolved_obligations=("open",))
    with pytest.raises(CanonicalizationError, match="evidence ceiling"):
        replace(claim, evidence_ceiling=REFUSAL_ONLY)


def test_refusal_requires_open_obligations_and_has_no_success_surface() -> None:
    refusal = _refusal_claim()

    with pytest.raises(CanonicalizationError, match="unresolved obligations"):
        replace(refusal, unresolved_obligations=())
    with pytest.raises(CanonicalizationError, match="refusal-only"):
        replace(refusal, evidence_ceiling=LOCAL_REPLAYABLE_FINITE_EVIDENCE)
    forged = refusal.to_dict()
    forged["success_criteria"] = "declare theorem"
    with pytest.raises(CanonicalizationError, match="unknown fields"):
        ResearchClaimV1.from_dict(forged)


@pytest.mark.parametrize("level", ("source", "claim", "payload", "envelope"))
def test_authority_effect_is_none_at_every_layer(level: str) -> None:
    payload = _finite_payload()
    if level == "source":
        wire = payload.to_dict()
        wire["sources"][0]["authority_effect"] = "Promote"
        parser = ResearchClaimPayloadV1.from_dict
    elif level == "claim":
        wire = payload.to_dict()
        wire["claims"][0]["authority_effect"] = "Promote"
        parser = ResearchClaimPayloadV1.from_dict
    elif level == "payload":
        wire = payload.to_dict()
        wire["authority_effect"] = "Promote"
        parser = ResearchClaimPayloadV1.from_dict
    else:
        wire = _envelope(payload).to_dict()
        wire["authority_effect"] = "Promote"
        parser = parse_research_claim_envelope

    with pytest.raises(CanonicalizationError, match="authority|Authority"):
        parser(wire)


def test_content_addressed_json_helper_reuses_exact_bytes(tmp_path) -> None:
    payload = _finite_payload()
    first = write_content_addressed_json(
        tmp_path, "research-payload", payload.to_dict()
    )
    second = write_content_addressed_json(
        tmp_path, "research-payload", payload.to_dict()
    )

    assert first == second
    assert first.name.startswith("research-payload_")

    with pytest.raises(CanonicalizationError, match="portable filename stem"):
        write_content_addressed_json(tmp_path, "research:payload", payload.to_dict())
    assert (
        first.name.removesuffix(".json").rsplit("_", 1)[1]
        == hashlib.sha256(first.read_bytes()).hexdigest()
    )
    assert first.read_bytes().endswith(b"\n")


def test_research_family_owner_laws_bind_carrier_and_boundaries() -> None:
    envelope = _envelope()

    with pytest.raises(CanonicalizationError, match="carrier_id"):
        parse_research_claim_envelope(
            replace(envelope, carrier_id="finite-cochain-2-v1")
        )
    with pytest.raises(CanonicalizationError, match="protected_boundaries"):
        parse_research_claim_envelope(replace(envelope, protected_boundaries=()))


def test_source_and_claim_references_are_resolved_within_payload() -> None:
    with pytest.raises(CanonicalizationError, match="resolve"):
        ResearchClaimPayloadV1(
            family=WITTEN_FINITE_FAMILY,
            disposition=EVALUATE_FINITE,
            sources=(_source("different"),),
            claims=(_finite_claim(),),
            initial_state_payload={},
        )


def test_build_envelope_refuses_initial_state_or_boundary_mismatch() -> None:
    payload = _finite_payload()

    with pytest.raises(CanonicalizationError, match="initial_state_payload"):
        build_research_claim_envelope(
            payload,
            task_id="witten-finite",
            carrier_id=RESEARCH_FAMILY_OWNER_LAWS[WITTEN_FINITE_FAMILY][0],
            initial_state_payload={"lambda": 2},
            protected_boundaries=RESEARCH_FAMILY_OWNER_LAWS[WITTEN_FINITE_FAMILY][1],
            step_budget=5,
        )
    with pytest.raises(CanonicalizationError, match="sorted"):
        build_research_claim_envelope(
            payload,
            task_id="witten-finite",
            carrier_id=RESEARCH_FAMILY_OWNER_LAWS[WITTEN_FINITE_FAMILY][0],
            initial_state_payload={
                "lambda": 1,
                "seeds": [-2.0, -0.25, 0.25, 2.0],
            },
            protected_boundaries=("z", "a"),
            step_budget=5,
        )


@pytest.mark.parametrize(
    "reserved_key",
    (
        "passed",
        "proved",
        "valid",
        "verified",
        "trusted",
        "promotion_eligible",
        "authorized",
        "authority-effect",
        "success",
    ),
)
def test_initial_state_recursively_refuses_authority_and_success_keys(
    reserved_key: str,
) -> None:
    with pytest.raises(CanonicalizationError, match="authority-bearing"):
        ResearchClaimPayloadV1(
            family=WITTEN_FINITE_FAMILY,
            disposition=EVALUATE_FINITE,
            sources=(_source(),),
            claims=(_finite_claim(),),
            initial_state_payload={
                "ordinary": [
                    {"nested": {reserved_key: True}},
                ]
            },
        )


def test_payload_resource_caps_apply_to_construction_and_parse() -> None:
    too_many_sources = tuple(
        _source(f"source-{index:02d}") for index in range(MAX_SOURCES + 1)
    )
    with pytest.raises(CanonicalizationError, match="source resource limit"):
        ResearchClaimPayloadV1(
            family=GR_FINITE_FAMILY,
            disposition=EVALUATE_FINITE,
            sources=too_many_sources,
            claims=(_finite_claim(source_id="source-00"),),
            initial_state_payload={},
        )

    too_many_claims = tuple(
        _finite_claim(f"claim-{index:02d}") for index in range(MAX_CLAIMS + 1)
    )
    with pytest.raises(CanonicalizationError, match="claim resource limit"):
        ResearchClaimPayloadV1(
            family=GR_FINITE_FAMILY,
            disposition=EVALUATE_FINITE,
            sources=(_source(),),
            claims=too_many_claims,
            initial_state_payload={},
        )

    oversized_wire = _finite_payload().to_dict()
    oversized_wire["sources"] = [
        _source(f"wire-{index:02d}").to_dict() for index in range(MAX_SOURCES + 1)
    ]
    with pytest.raises(CanonicalizationError, match="source resource limit"):
        ResearchClaimPayloadV1.from_dict(oversized_wire)


def test_string_array_and_initial_state_wire_caps_fail_closed() -> None:
    with pytest.raises(CanonicalizationError, match="string resource limit"):
        replace(_finite_claim(), statement="x" * (MAX_STRING_LENGTH + 1))
    with pytest.raises(CanonicalizationError, match="array resource limit"):
        replace(
            _finite_claim(),
            assumptions=tuple(
                f"assumption-{index:03d}" for index in range(MAX_ARRAY_LENGTH + 1)
            ),
        )
    with pytest.raises(CanonicalizationError, match="canonical resource limit"):
        ResearchClaimPayloadV1(
            family=WITTEN_FINITE_FAMILY,
            disposition=EVALUATE_FINITE,
            sources=(_source(),),
            claims=(_finite_claim(),),
            initial_state_payload={
                "samples": ["x" * 100 for _ in range(4096)],
            },
        )


def test_source_intake_bundle_is_sorted_packet_bound_and_strict(tmp_path) -> None:
    source_dir = tmp_path / "research"
    source_dir.mkdir()
    (source_dir / "paper.txt").write_bytes(b"finite source\n")
    payload = _finite_payload()
    envelope = _envelope(payload)

    bundle = build_source_intake_bundle(envelope, tmp_path)
    round_trip = SourceIntakeBundleV1.from_dict(bundle.to_dict())

    assert bundle.packet_id == envelope.packet_id
    assert bundle.source_manifest_root == payload.source_manifest_root
    assert bundle.all_verified
    assert round_trip == bundle
    assert round_trip.receipt_id == bundle.receipt_id
    assert bundle.authority_effect == "None"

    forged = deepcopy(bundle.to_dict())
    forged["packet_id"] = "f" * 64
    with pytest.raises(CanonicalizationError, match="receipt_id"):
        SourceIntakeBundleV1.from_dict(forged)
    unknown = deepcopy(bundle.to_dict())
    unknown["trusted"] = True
    with pytest.raises(CanonicalizationError, match="unknown fields"):
        SourceIntakeBundleV1.from_dict(unknown)


