from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from omega_engine.crates.prompt_civilization import (
    AntiSkillActivationProfileV1,
    AntiSkillEvaluationReceiptV2,
    AntiSkillFixtureBankV1,
    AntiSkillSubjectV1,
    Err,
    HumanAntiSkillAdmissionDecisionV1,
    PredicateAtomV1,
    canonical_json_bytes,
    evaluate_antiskill_fixture_bank,
    load_antiskill_activation_profile,
    loads_strict_json,
    parse_antiskill_spec_v2,
    truth_boundary_fixture_bank,
    truth_boundary_specs,
)
from omega_engine_workflows_agents_skills.application.anti_skill_admission import (
    verify_anti_skill_admission,
    verify_verified_anti_skill_registry,
)
from omega_engine_workflows_agents_skills.application.anti_skill_admission.load_truth_boundary_activation import (
    load_truth_boundary_activation,
)

ROOT = Path(__file__).resolve().parents[2]
CANARY = ROOT / ".agents" / "anti_skills" / "ooutwire" / "truth_boundary_v2"
ADMITTED = ROOT / ".agents" / "anti_skills" / "admitted" / "truth_boundary_v2"
APPROVAL_REFERENCE = (
    "sha256:2687f86ed6784b8a5fca36e6c468e12aa44dc3c7e8137e3160d1a95079bdcd02"
)


def _digest(character: str) -> str:
    return "sha256:" + character * 64


def _canonical_documents(values: tuple[object, ...]) -> tuple[bytes, ...]:
    return tuple(canonical_json_bytes(value.to_dict()) for value in values)


def _approved_registry():
    specs = truth_boundary_specs()
    bank = truth_boundary_fixture_bank()
    receipts = evaluate_antiskill_fixture_bank(specs, bank).unwrap()
    decisions = tuple(
        HumanAntiSkillAdmissionDecisionV1(
            reviewer_identity="human-test-reviewer",
            spec_digest=spec.spec_digest,
            evaluation_receipt_id=next(
                receipt.receipt_id
                for receipt in receipts
                if receipt.spec_digest == spec.spec_digest
            ),
            decision="APPROVE",
            approval_reference=_digest(str(index + 1)),
        )
        for index, spec in enumerate(specs)
    )
    verified = verify_anti_skill_admission(
        spec_documents=_canonical_documents(specs),
        fixture_bank_document=canonical_json_bytes(bank.to_dict()),
        evaluation_receipt_documents=_canonical_documents(receipts),
        human_decision_documents=_canonical_documents(decisions),
    ).unwrap()
    return specs, bank, receipts, decisions, verified


def test_truth_boundary_canary_has_complete_independent_controls() -> None:
    specs = truth_boundary_specs()
    bank = truth_boundary_fixture_bank()
    result = evaluate_antiskill_fixture_bank(specs, bank).unwrap()
    assert len(specs) == len(result) == 3
    assert all(receipt.outcome == "COMPUTED_PASS" for receipt in result)
    for spec in specs:
        cases = [case for case in bank.cases if case.spec_id == spec.spec_id]
        assert sum(case.expected_hit for case in cases) == 1
        assert sum(case.negative_control for case in cases) == 1
        assert len({case.context_key for case in cases}) == 2


def test_committed_canary_bytes_replay_and_profile_admission_is_bound() -> None:
    specs = truth_boundary_specs()
    bank = truth_boundary_fixture_bank()
    receipts = evaluate_antiskill_fixture_bank(specs, bank).unwrap()
    for spec in specs:
        assert (
            CANARY / f"{spec.spec_id}.spec.json"
        ).read_bytes() == canonical_json_bytes(spec.to_dict())
    assert (
        CANARY / "truth-boundary.fixture-bank.json"
    ).read_bytes() == canonical_json_bytes(bank.to_dict())
    for spec, receipt in zip(specs, receipts, strict=True):
        assert (
            CANARY / f"{spec.spec_id}.evaluation-receipt.json"
        ).read_bytes() == canonical_json_bytes(receipt.to_dict())
    request = loads_strict_json((CANARY / "admission-request.json").read_text("utf-8"))
    assert request["human_decision_status"] == "APPROVED"
    assert request["verified_registry_status"] == "VERIFIED_PROFILE_SCOPED"
    live = loads_strict_json(
        (ROOT / ".agents" / "anti_skills" / "admitted" / "registry.json").read_text(
            "utf-8"
        )
    )
    assert live["specs"] == []

    decisions = tuple(
        HumanAntiSkillAdmissionDecisionV1.from_dict(
            loads_strict_json(
                (ADMITTED / f"{spec.spec_id}.human-decision.json").read_text("utf-8")
            )
        )
        for spec in specs
    )
    assert {decision.approval_reference for decision in decisions} == {
        APPROVAL_REFERENCE
    }
    registry_document = (ADMITTED / "verified-registry.json").read_bytes()
    verified = verify_verified_anti_skill_registry(
        registry_document=registry_document,
        spec_documents=_canonical_documents(specs),
        fixture_bank_document=canonical_json_bytes(bank.to_dict()),
        evaluation_receipt_documents=_canonical_documents(receipts),
        human_decision_documents=_canonical_documents(decisions),
    ).unwrap()
    profile = AntiSkillActivationProfileV1.from_dict(
        loads_strict_json(
            (ADMITTED / "woland-engineering-v1.activation-profile.json").read_text(
                "utf-8"
            )
        )
    )
    runtime = load_antiskill_activation_profile(verified, profile).unwrap()
    assert profile.profile_id == "woland-engineering-v1"
    assert set(profile.active_spec_ids) == {spec.spec_id for spec in specs}
    assert runtime.registry.registry_id == verified.registry_id
    loaded = load_truth_boundary_activation(
        canary_directory=CANARY,
        admitted_directory=ADMITTED,
    ).unwrap()
    assert loaded.registry.registry_id == verified.registry_id
    assert loaded.profile.profile_digest == profile.profile_digest


def test_strict_canonical_wire_rejects_unknown_duplicate_bool_and_subclass() -> None:
    spec = truth_boundary_specs()[0]
    wire = spec.to_dict()
    wire["dynamic_callable"] = "evil.module:run"
    assert isinstance(parse_antiskill_spec_v2(canonical_json_bytes(wire)), Err)

    duplicate = (
        canonical_json_bytes(spec.to_dict())
        .decode("utf-8")
        .replace('"version":1', '"version":1,"version":1')
    )
    assert isinstance(parse_antiskill_spec_v2(duplicate.encode("utf-8")), Err)

    bool_version = spec.to_dict()
    bool_version["version"] = True
    assert isinstance(parse_antiskill_spec_v2(canonical_json_bytes(bool_version)), Err)

    class SubjectSubclass(AntiSkillSubjectV1):
        pass

    subject = truth_boundary_fixture_bank().cases[0].subject
    spoof = SubjectSubclass(
        claim_scope=subject.claim_scope,
        evidence_scope=subject.evidence_scope,
        producer_identity=subject.producer_identity,
        verifier_identity=subject.verifier_identity,
        claim_mode=subject.claim_mode,
        requested_effect=subject.requested_effect,
        nonclaims=subject.nonclaims,
    )
    atom = PredicateAtomV1(
        operator="VALUE_IN", fields=("claim_mode",), values=("BOUNDED",)
    )
    try:
        atom.matches(spoof)
    except TypeError:
        pass
    else:
        raise AssertionError("subject subclass spoof was accepted")


def test_copied_fixture_and_stale_implementation_refuse() -> None:
    specs = truth_boundary_specs()
    bank = truth_boundary_fixture_bank()
    copied = replace(
        bank.cases[1],
        case_id="copied-subject",
        case_digest="",
        subject=bank.cases[0].subject,
    )
    try:
        AntiSkillFixtureBankV1(
            cases=tuple(sorted((*bank.cases, copied), key=lambda x: x.case_id))
        )
    except ValueError as exc:
        assert "copied fixture" in str(exc)
    else:
        raise AssertionError("copied fixture was accepted")

    stale = replace(specs[0], implementation_digest=_digest("f"), spec_digest="")
    assert isinstance(evaluate_antiskill_fixture_bank((stale, *specs[1:]), bank), Err)


def test_caller_authored_pass_is_refused() -> None:
    specs = truth_boundary_specs()
    bank = truth_boundary_fixture_bank()
    receipt = evaluate_antiskill_fixture_bank(specs, bank).unwrap()[0]
    wire = receipt.to_dict()
    first = wire["case_results"][0]
    first["observed_hit"] = not first["expected_hit"]
    first["passed"] = False
    first["result_id"] = ""
    wire["receipt_id"] = ""
    wire["outcome"] = "COMPUTED_PASS"
    try:
        AntiSkillEvaluationReceiptV2.from_dict(wire)
    except ValueError as exc:
        assert "outcome" in str(exc) or "digest" in str(exc) or "result_id" in str(exc)
    else:
        raise AssertionError("caller-authored pass was accepted")


def test_external_verifier_requires_exact_human_decisions_and_replays_registry() -> (
    None
):
    specs = truth_boundary_specs()
    bank = truth_boundary_fixture_bank()
    receipts = evaluate_antiskill_fixture_bank(specs, bank).unwrap()
    missing = verify_anti_skill_admission(
        spec_documents=_canonical_documents(specs),
        fixture_bank_document=canonical_json_bytes(bank.to_dict()),
        evaluation_receipt_documents=_canonical_documents(receipts),
        human_decision_documents=(),
    )
    assert isinstance(missing, Err)
    assert "human admission decision" in missing.error.message

    _, _, receipts, decisions, verified = _approved_registry()
    replayed = verify_verified_anti_skill_registry(
        registry_document=canonical_json_bytes(verified.to_dict()),
        spec_documents=_canonical_documents(specs),
        fixture_bank_document=canonical_json_bytes(bank.to_dict()),
        evaluation_receipt_documents=_canonical_documents(receipts),
        human_decision_documents=_canonical_documents(decisions),
    ).unwrap()
    assert replayed == verified
    assert replayed.authority_effect == "None"


def test_activation_is_profile_scoped_and_detects_without_repair() -> None:
    specs, _, _, _, registry = _approved_registry()
    profile = AntiSkillActivationProfileV1(
        profile_id="woland-truth-boundary-test",
        registry_id=registry.registry_id,
        active_spec_ids=tuple(spec.spec_id for spec in specs),
        subject_scopes=("candidate_result",),
    )
    runtime = load_antiskill_activation_profile(registry, profile).unwrap()
    subject = AntiSkillSubjectV1(
        claim_scope=("candidate_result",),
        evidence_scope=("model_verdict",),
        producer_identity="same-model",
        verifier_identity="same-model",
        claim_mode="SELF_CERTIFIED",
        requested_effect="FINDING",
        nonclaims=("No authority is granted.",),
    )
    hits = runtime.evaluate(subject)
    assert [hit.failure_code for hit in hits] == ["MODEL_SELF_CERTIFICATION"]
    assert all(hit.authority_effect == "None" for hit in hits)
    assert not hasattr(runtime, "repair")


def test_ag_arena_adapter_requires_complete_nonrecurrence_evidence() -> None:
    trap = TrapSignature(
        failure_class="arena_failure",
        times_seen=3,
        distinct_runs=2,
        severity_max=4,
        severity_avg=3.0,
        evidence_samples=("finding-a", "finding-b"),
    )
    anti = AntiMorphism.from_trap(trap, domain="woland")
    incomplete = anti_morphism_to_inert_candidate(
        anti,
        subject_schema="omega.antiskill.subject.v1",
        proposed_invariant="Do not collapse this arena finding.",
        episode_ids=(_digest("1"), _digest("2")),
        context_keys=("run-a", "run-b"),
        evidence_refs=("finding-a",),
        counterexamples=("A negative control.",),
        protected_fields=("claim_scope",),
    )
    assert isinstance(incomplete, Err)

    complete = anti_morphism_to_inert_candidate(
        anti,
        subject_schema="omega.antiskill.subject.v1",
        proposed_invariant="Do not collapse this arena finding.",
        episode_ids=(_digest("1"), _digest("2")),
        context_keys=("run-a", "run-b"),
        evidence_refs=("finding-a", "finding-b"),
        counterexamples=("A negative control.",),
        protected_fields=("claim_scope",),
    ).unwrap()
    assert complete.status == "PROPOSED"
    assert complete.authority_effect == "None"
