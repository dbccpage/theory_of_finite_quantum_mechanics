from __future__ import annotations

import json
from pathlib import Path
import tempfile

from omega_engine.crates.prompt_civilization import (
    AntiSkillCandidateV1,
    AntiSkillSpecV1,
    Err,
    compile_registry_syntax_only,
    load_admitted_registry,
    loads_strict_json,
    segment_dialogue,
)


ROOT = Path(__file__).resolve().parents[2]


def _digest(character: str) -> str:
    return "sha256:" + character * 64


def _spec(
    spec_id: str,
    *,
    order: int | None = None,
    field: str = "objective",
    evidence: str = "receipt:a",
) -> AntiSkillSpecV1:
    return AntiSkillSpecV1(
        spec_id=spec_id,
        version=1,
        failure_code="MISSING_TYPED_FIELD",
        detector_kind="requires_field",
        activation_fields=(field,),
        repair_kind="populate_typed_field",
        protected_fields=("original_text",),
        episode_ids=(_digest("1"), _digest("2")),
        context_keys=("session-a", "session-b"),
        evidence_refs=(evidence,),
        counterexamples=("An exploratory prompt may declare the field optional.",),
        evaluation_receipt_ref=_digest("3"),
        composition_order=order,
    )


def test_empty_admitted_registry_replays_exactly() -> None:
    path = ROOT / ".agents" / "anti_skills" / "admitted" / "registry.json"
    loaded = load_admitted_registry(path).unwrap()
    assert loaded.specs == ()
    assert loaded.registry_id == (
        "sha256:90730de946f568fba0807ffbf8bb9fdf14c4ecf5d4c3c85cc8c7d9599639789d"
    )


def test_nonempty_registry_refuses_without_admission_validator() -> None:
    registry = compile_registry_syntax_only([_spec("shape-only")]).unwrap()
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "registry.json"
        path.write_text(json.dumps(registry.to_dict()), encoding="utf-8")
        result = load_admitted_registry(path)
    assert isinstance(result, Err)
    assert result.error.code == "ADMISSION_VALIDATOR_UNAVAILABLE"


def test_public_schema_is_strict_json_and_covers_evaluation_receipts() -> None:
    path = ROOT / ".agents" / "anti_skills" / "schema.json"
    wire = json.loads(path.read_text(encoding="utf-8"))
    assert wire["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert wire["$defs"]["candidate"]["additionalProperties"] is False
    assert wire["$defs"]["spec"]["additionalProperties"] is False
    assert wire["$defs"]["typedPrompt"]["additionalProperties"] is False
    assert wire["$defs"]["evaluationReceipt"]["additionalProperties"] is False
    for name in (
        "conversationEpisode",
        "promptFinding",
        "promptReviewReceipt",
        "promptReviewBundle",
        "approvedPrompt",
        "registry",
    ):
        assert wire["$defs"][name]["additionalProperties"] is False


def test_duplicate_keys_and_nonfinite_numbers_refuse() -> None:
    for attack in ('{"outcome":"a","outcome":"b"}', '{"score":NaN}'):
        try:
            loads_strict_json(attack)
        except ValueError:
            pass
        else:
            raise AssertionError("noncanonical JSON was accepted")


def test_seed_candidates_are_strict_candidates_not_specs() -> None:
    path = ROOT / ".agents" / "anti_skills" / "ooutwire" / "seed_candidates.json"
    wire = json.loads(path.read_text(encoding="utf-8"))
    candidates = [AntiSkillCandidateV1.from_dict(item) for item in wire["candidates"]]
    assert len(candidates) == 6
    assert all(len(item.context_keys) == 1 for item in candidates)
    result = compile_registry_syntax_only([candidates[0].to_dict()])
    assert isinstance(result, Err)
    assert result.error.items[0].code == "INVALID_SPEC_SHAPE"


def test_seed_candidate_episode_refs_replay_from_canonical_source() -> None:
    source = (
        ROOT
        / "_ooutwire"
        / "2026-08-13-132939-local-command-caveatcaveat-the-messages-below.txt"
    )
    episodes = segment_dialogue(
        source,
        start_line=12693,
        end_line=13354,
        session_id="fable-2026-08-13",
        task_id="primitive-difference-audit",
        model_id="claude-opus-5",
    ).unwrap()
    replayed_episode_ids = {episode.episode_id for episode in episodes}

    candidate_path = (
        ROOT / ".agents" / "anti_skills" / "ooutwire" / "seed_candidates.json"
    )
    candidate_wire = json.loads(candidate_path.read_text(encoding="utf-8"))
    candidates = [
        AntiSkillCandidateV1.from_dict(item) for item in candidate_wire["candidates"]
    ]
    assert candidates
    assert all(set(candidate.episode_ids) <= replayed_episode_ids for candidate in candidates)


def test_admission_requires_independent_contexts() -> None:
    try:
        AntiSkillSpecV1(
            spec_id="bad-contexts",
            version=1,
            failure_code="MISSING_TYPED_FIELD",
            detector_kind="requires_field",
            activation_fields=("objective",),
            repair_kind="populate_typed_field",
            protected_fields=("original_text",),
            episode_ids=(_digest("1"), _digest("2")),
            context_keys=("same-session",),
            evidence_refs=("receipt:a",),
            counterexamples=("A clean negative control.",),
            evaluation_receipt_ref=_digest("3"),
        )
    except ValueError as exc:
        assert "independent contexts" in str(exc)
    else:
        raise AssertionError("single-context candidate was admitted")


def test_overlapping_repairs_require_order_or_tested_commutation() -> None:
    unordered = compile_registry_syntax_only([_spec("first"), _spec("second")])
    assert isinstance(unordered, Err)
    assert unordered.error.items[0].code == "OVERLAPPING_REPAIRS_UNORDERED"

    ordered = compile_registry_syntax_only(
        [_spec("first", order=10), _spec("second", order=20)]
    )
    assert ordered.unwrap().specs[0].spec_id == "first"


def test_spec_evidence_mutation_changes_digest() -> None:
    first = _spec("stable", evidence="receipt:a")
    second = _spec("stable", evidence="receipt:b")
    assert first.spec_digest != second.spec_digest


def test_dynamic_executor_fields_fail_closed() -> None:
    wire = _spec("stable").to_dict()
    wire["callable"] = "evil.module:function"
    result = compile_registry_syntax_only([wire])
    assert isinstance(result, Err)
    assert "unknown fields" in result.error.items[0].message


def test_candidate_and_registry_id_mutations_fail_closed() -> None:
    candidate_path = (
        ROOT / ".agents" / "anti_skills" / "ooutwire" / "seed_candidates.json"
    )
    candidate_wire = json.loads(candidate_path.read_text(encoding="utf-8"))["candidates"][0]
    candidate_wire["candidate_id"] = _digest("f")
    try:
        AntiSkillCandidateV1.from_dict(candidate_wire)
    except ValueError as exc:
        assert "candidate_id" in str(exc)
    else:
        raise AssertionError("mutated candidate id was accepted")

    registry_path = ROOT / ".agents" / "anti_skills" / "admitted" / "registry.json"
    registry_wire = json.loads(registry_path.read_text(encoding="utf-8"))
    registry_wire["registry_id"] = _digest("e")
    with tempfile.TemporaryDirectory() as folder:
        mutated = Path(folder) / "registry.json"
        mutated.write_text(json.dumps(registry_wire), encoding="utf-8")
        result = load_admitted_registry(mutated)
    assert isinstance(result, Err)
    assert result.error.code == "REGISTRY_LOAD_REFUSED"


def test_direct_constructor_owns_repeated_fields() -> None:
    episode_ids = [_digest("1")]
    context_keys = ["session-a"]
    evidence_refs = ["receipt:a"]
    counterexamples = ["A clean counterexample."]
    protected_fields = ["original_text"]
    candidate = AntiSkillCandidateV1(
        name="owned-fields",
        failure_code="MUTABLE_INPUT",
        proposed_invariant="Repeated fields become immutable owned tuples.",
        episode_ids=episode_ids,  # type: ignore[arg-type]
        context_keys=context_keys,  # type: ignore[arg-type]
        evidence_refs=evidence_refs,  # type: ignore[arg-type]
        counterexamples=counterexamples,  # type: ignore[arg-type]
        protected_fields=protected_fields,  # type: ignore[arg-type]
    )
    before = candidate.to_dict()
    episode_ids.append(_digest("2"))
    context_keys.append("session-b")
    evidence_refs.append("receipt:b")
    counterexamples.append("Mutation after construction.")
    protected_fields.append("objective")
    assert candidate.to_dict() == before
    assert type(candidate.episode_ids) is tuple
