"""Tests for packet-bound universal obstruction receipts and DDA emission."""

from copy import deepcopy
from pathlib import Path
import runpy

import pytest

from omega_engine.crates.pipeline.omega_engine_prompt_intake_pipeline import (
    DDAEmissionCollision,
    emit_dda_module,
)

from omega_engine.crates.pipeline.research_pipeline import OmegaResearchPipeline
from omega_engine.crates.runtime.rt_universal_obstruction import (
    UniversalSolverRefusal,
    build_universal_obstruction_receipt,
    parse_research_proposal,
    replay_dda_payload,
)

from omega_engine_pfp.domain.entities.research_packets import ClaimKind, ResearchClaim, ResearchMode, ResearchProposal

EXACT_TRIANGLE = {
    "dimensions": (3, 3, 1),
    "d0": ((-1, 1, 0), (0, -1, 1), (-1, 0, 1)),
    "d1": ((1, 1, -1),),
    "beta": (1, 2, 3),
}


def _packet_and_proposal(tmp_path: Path):
    paper = tmp_path / "paper.md"
    paper.write_text("# Paper\n\nPL-TEST remains provisional.\n", encoding="utf-8")
    engine = OmegaResearchPipeline()
    packet = engine.start(

        paper,
        "Test a finite obstruction without promoting the paper claim",
        "test-provider:model",
        mode=ResearchMode.FAST,
    )
    proposal = ResearchProposal(
        proposal_id="prop-test-universal",
        seed_sha256=packet.packet_sha256,
        model_id=packet.proposer_id,
        target_path="paper.md",
        summary="Check one exact finite cochain representative.",
        proposed_change="Keep PL-TEST provisional and attach the local receipt.",
        claims=(
            ResearchClaim(
                claim_id="claim-local-exactness",
                text="The supplied beta is exact in the displayed rational complex.",
                kind=ClaimKind.CONDITIONAL,
                hypotheses=("The displayed matrices are the complete finite carrier.",),
                evidence_refs=("paper.md#PL-TEST",),
                falsifier="Exact elimination finds no primitive witness.",
            ),
        ),
        proof_obligations=("PL-TEST",),
        cochain_problem=EXACT_TRIANGLE,
        declared_cochain_verdict="exact_repair",
    )
    return packet, proposal


def test_strict_provider_payload_parser_binds_seed_and_model(tmp_path: Path):
    packet, proposal = _packet_and_proposal(tmp_path)
    parsed = parse_research_proposal(packet, proposal.canonical_payload())
    assert parsed.proposal_sha256 == proposal.proposal_sha256

    wrong_model = proposal.canonical_payload()
    wrong_model["model_id"] = "counterfeit:model"
    with pytest.raises(UniversalSolverRefusal, match="identity"):
        parse_research_proposal(packet, wrong_model)


def test_universal_receipt_runs_all_finite_rails_without_promotion(tmp_path: Path):
    packet, proposal = _packet_and_proposal(tmp_path)
    receipt = build_universal_obstruction_receipt(packet, proposal)
    payload = receipt.canonical_payload()

    assert payload["authority_effect"] == "none"
    assert payload["mechanical_evidence"]["exact_cochain"]["verdict"] == "exact_repair"
    assert payload["mechanical_evidence"]["parity_shadow"]["delta1_delta0_zero"] is True
    assert payload["mechanical_evidence"]["q_degree0"]["converged"] is True
    assert payload["mechanical_evidence"]["q_degree1"]["converged"] is True
    assert payload["paper_update_disposition"] == "REFUSE_PROMOTION"
    assert payload["unsupported_paper_obligations"][0]["proof_obligation"] == "PL-TEST"
    assert len(payload["loss_ledger"]) == 3
    assert replay_dda_payload(payload) == receipt.receipt_sha256


def test_content_addressed_dda_module_is_idempotent_and_replays(tmp_path: Path):
    packet, proposal = _packet_and_proposal(tmp_path)
    output = tmp_path / "dda"
    first = emit_dda_module(packet, proposal, output)
    second = emit_dda_module(packet, proposal, output)
    assert first == second
    assert first.name.startswith("dda_prop_test_universal_")
    namespace = runpy.run_path(str(first))
    assert namespace["PAYLOAD"]["authority_effect"] == "none"
    assert namespace["replay"]() == namespace["PAYLOAD"]["receipt_sha256"]
    source = first.read_text(encoding="utf-8")
    assert proposal.proposed_change not in source
    assert "exec(" not in source


def test_dda_replay_refuses_mechanical_tampering(tmp_path: Path):
    packet, proposal = _packet_and_proposal(tmp_path)
    payload = build_universal_obstruction_receipt(packet, proposal).canonical_payload()
    tampered = deepcopy(payload)
    tampered["cochain_problem"]["beta"] = (999, 2, 3)
    with pytest.raises(UniversalSolverRefusal, match="mechanical replay mismatch"):
        replay_dda_payload(tampered)


def test_dda_emitter_refuses_content_collision(tmp_path: Path):
    packet, proposal = _packet_and_proposal(tmp_path)
    path = emit_dda_module(packet, proposal, tmp_path / "dda")
    path.write_text("tampered\n", encoding="utf-8")
    with pytest.raises(DDAEmissionCollision):
        emit_dda_module(packet, proposal, tmp_path / "dda")


