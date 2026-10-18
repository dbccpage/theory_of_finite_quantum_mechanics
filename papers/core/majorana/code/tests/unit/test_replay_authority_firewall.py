from __future__ import annotations
"""Negative tests for replay, evaluation, residual, and authority firewalls."""


import pytest

from omega_engine.crates.type.domain_packet import CheckedPacket, FOCRealCert
from omega_engine_governance.contracts import AuthorityEffect
from omega_engine.crates.replay import DescentWitness, ReplayTracePacket
from omega_engine.crates.residuals import (
    ResidualFamily,
    ResidualFamilyId,
    ResidualRegistry,
)
from omega_engine_pfp.domain.entities.research_packets import (
    ResearchStepPacket,
    StepRealization,
)
from omega_engine.crates.type.paper_hygiene import (
    GateCheck,
    GateName,
    GateVerdict,
    PaperPipeline,
    SixGateReceipt,
)
from omega_engine.crates.type.outcome import CertifiedAuthority
from omega_engine.crates.type.terminal import AuthorityDescentState, AuthorityTerminal


def _trace(status: str = "BLOCKED@adversary") -> ReplayTracePacket:
    return ReplayTracePacket(
        paper_sha256="0" * 64,
        proposal_sha256="1" * 64,
        gate_receipt_sha256="2" * 64,
        loop_pass=1,
        step_index=1,
        status=status,
    )


def _witness(packet: ReplayTracePacket) -> DescentWitness:
    return DescentWitness.from_verified_replay(packet, packet.replay_hash)


def _pass_checks(failing_gate: GateName | None = None) -> tuple[GateCheck, ...]:
    checks = []
    for gate in GateName:
        if gate is failing_gate:
            checks.append(
                GateCheck(
                    gate,
                    GateVerdict.FAIL,
                    "ADVERSARIAL_COUNTEREXAMPLE",
                    "3" * 64,
                )
            )
        else:
            checks.append(GateCheck(gate, GateVerdict.PASS, "CHECKED", "3" * 64))
    return tuple(checks)


def test_replay_rejects_arbitrary_objects_and_hash_tampering() -> None:
    packet = _trace()

    with pytest.raises(TypeError, match="requires a ReplayTracePacket"):
        DescentWitness.from_verified_replay("not-a-packet", "0" * 64)
    with pytest.raises(ValueError, match="mismatch"):
        DescentWitness.from_verified_replay(packet, "f" * 64)


def test_evidence_certificate_is_hash_bound_and_non_authoritative() -> None:
    packet = _trace()
    checked = CheckedPacket(FOCRealCert(packet, _witness(packet)))

    assert checked.packet is packet
    assert checked.replay_hash == packet.replay_hash
    assert checked.authority_effect is AuthorityEffect.None_

    tampered = _trace("SWEEP_COMPLETE")
    with pytest.raises(ValueError, match="not bound"):
        FOCRealCert(tampered, _witness(packet))


def test_local_authority_minting_fails_even_with_all_boolean_guards_true() -> None:
    packet = _trace()
    witness = _witness(packet)
    terminal = AuthorityTerminal("proposal-only", "evidence")
    state = AuthorityDescentState(
        replay_hash=witness.replay_hash,
        deterministic=True,
        phi1=0,
        exhaustive=True,
        skeleton_aligned=True,
        lift_required=False,
        has_refusal=False,
        human_promoted=True,
    )

    with pytest.raises(PermissionError, match="human promotion"):
        CertifiedAuthority.certify(terminal, witness, state)
    with pytest.raises(TypeError, match="requires a DescentWitness"):
        CertifiedAuthority.certify(terminal, "arbitrary", state)


def test_mechanical_research_packet_requires_verifier_and_evidence() -> None:
    with pytest.raises(ValueError, match="mechanical realization"):
        ResearchStepPacket(
            carrier_sha256="0" * 64,
            proposal_sha256="1" * 64,
            round_index=1,
            step_index=1,
            realization=StepRealization.MECHANICAL,
        )


@pytest.mark.parametrize("failing_gate", list(GateName))
def test_each_adversarial_gate_can_block_acceptance(failing_gate: GateName) -> None:
    receipt = SixGateReceipt(
        carrier_sha256="0" * 64,
        proposal_sha256="1" * 64,
        producer_id="model-producer",
        evaluator_id="independent-model-evaluator",
        checks=_pass_checks(failing_gate),
    )
    assert receipt.passed is False
    assert receipt.authority_effect is AuthorityEffect.None_


def test_six_gate_receipt_requires_independent_identities_and_exact_gate_set() -> None:
    with pytest.raises(ValueError, match="separate"):
        SixGateReceipt(
            carrier_sha256="0" * 64,
            proposal_sha256="1" * 64,
            producer_id="same-model",
            evaluator_id="same-model",
            checks=_pass_checks(),
        )
    with pytest.raises(ValueError, match="exactly once"):
        SixGateReceipt(
            carrier_sha256="0" * 64,
            proposal_sha256="1" * 64,
            producer_id="producer",
            evaluator_id="evaluator",
            checks=_pass_checks()[:-1],
        )


def test_passing_gate_requires_evidence_hash() -> None:
    with pytest.raises(ValueError, match="evidence hash"):
        GateCheck(GateName.STEP_TRUTH, GateVerdict.PASS, "CHECKED")


def test_residual_registry_rejects_rebinding() -> None:
    registry = ResidualRegistry()
    family = ResidualFamily(
        ResidualFamilyId.GTTA_GROUND_STATE_UNLIFTED,
        "CODA-A ground-state unlifted",
    )
    registry.register(family)
    with pytest.raises(ValueError, match="already registered"):
        registry.register(family)


def test_pipeline_stages_require_external_roles() -> None:
    pipeline = PaperPipeline("paper.md")
    results = (
        pipeline.run_improver(),
        pipeline.run_adversary(),
        pipeline.run_proof_signoff(),
        pipeline.run_release_preflight(),
    )
    assert {result["status"] for result in results} == {"EXTERNAL_ROLE_REQUIRED"}
    assert {result["authority_effect"] for result in results} == {"none"}


