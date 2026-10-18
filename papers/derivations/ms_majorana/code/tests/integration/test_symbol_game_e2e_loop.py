"""End-to-end integration test driving an active ObstructionLedger through iterative model proposal turns.

Exercises the complete lab protocol:
1. Host initializes ObstructionLedger with active open obstructions (OBS-01, OBS-02, OBS-03).
2. Host compiles PromptArtifactV1 (Layer A ID + Layer B body bytes).
3. Candidate proposals are scored via coboundary_scoring and residual_drop metrics.
4. Winning candidate repairs OBS-01 and OBS-02; ledger is reconciled; host emits EliminationReceiptV1 (Open -> Open).
5. Turn 2 compiles PromptArtifactV1 with surviving OBS-03.
6. Candidate repair eliminates OBS-03 with verified dual-witness ref; ledger is reconciled to empty; host emits EliminationReceiptV1 (Open -> Exact).
7. All artifacts, prompt bodies, and elimination receipts are content-addressed and verified on disk.
8. AuthorityEffect: None is preserved across all transitions.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
import pytest

from omega_engine_pfp.domain import (
    CanonicalizationError,
    raw_content_sha256,
)
from omega_engine_pfp.domain.entities.obstruction import ObstructionLedger
from omega_engine_pfp.domain import (
    AUTHORITY_EFFECT,
    CandidateProposal,
    DemandItemV1,
    EliminationReceiptV1,
    ObjectiveTypedV1,
    ObstructionHintV1,
    PromptArtifactV1,
    ResidualDropV1,
    compile_prompt_artifact,
    create_elimination_receipt,
    parse_elimination_receipt_block,
    prompt_artifact_to_content_binding,
    render_elimination_receipt_block,
    render_prompt_body,
)
from omega_engine_pfp.use_cases.prompt_artifact import (
    write_elimination_receipt,
    write_prompt_artifact,
    write_prompt_body,
)
from omega_engine_pfp.use_cases import (
    magnitudes_from_ledger_active,
    rank_by_efficiency,
    rank_candidate_proposals,
    residual_drop_from_ids,
    residual_drop_from_ledger_maps,
    score_discrete_proposal,
)
from omega_engine.crates.type.symgame import Obstruction, ProjectionReceipt

SAMPLE_HEX64_EV_1 = "1" * 64
SAMPLE_HEX64_EV_2 = "2" * 64
SAMPLE_HEX64_WITNESS = "e" * 64
REGIME_BYTES = b"REGIME: branch_o_observational\nAUTHORITY_EFFECT: None\n"


def _make_projection(
    obstruction_map: dict[str, float],
    step: int = 1,
) -> ProjectionReceipt:
    obs_list = tuple(
        Obstruction(obstruction_id=oid, magnitude=mag, witness=f"witness_{oid}")
        for oid, mag in sorted(obstruction_map.items())
    )
    return ProjectionReceipt(
        projector_id="proj_discrete_obstruction_gate",
        state_hash=f"state_{step:04d}",
        obstructions=obs_list,
        witness=f"receipt_witness_{step:04d}",
    )


def test_symbol_game_e2e_iterative_loop(tmp_path: Path) -> None:
    # -----------------------------------------------------------------------
    # Step 1: Initialize Host ObstructionLedger with 3 active obstructions
    # -----------------------------------------------------------------------
    ledger = ObstructionLedger()
    proj_0 = _make_projection({"OBS-01": 1.0, "OBS-02": 2.0, "OBS-03": 1.5}, step=0)
    ledger.reconcile(proj_0, step=0, witness="initial_projection")

    assert ledger.active_ids == ("OBS-01", "OBS-02", "OBS-03")
    assert len(ledger.events) == 3

    # -----------------------------------------------------------------------
    # Step 2: Compile Turn 1 PromptArtifact presenting open obstructions
    # -----------------------------------------------------------------------
    obj_turn1 = ObjectiveTypedV1(
        kind="obstruction_refine",
        summary="eliminate open cochain obstructions",
        target_obstruction_ids=ledger.active_ids,
    )
    demands_turn1 = (
        DemandItemV1(
            demand_id="DEM-01",
            kind="repair_obstruction",
            note="repair OBS-01 and OBS-02",
        ),
    )
    hints_turn1 = tuple(
        ObstructionHintV1(
            obstruction_id=oid,
            family="undecidable_treated_as_equal",
            residual_colour="Open",
        )
        for oid in ledger.active_ids
    )

    body_bytes_1 = render_prompt_body(
        REGIME_BYTES,
        objective_typed=obj_turn1,
        open_obstructions=hints_turn1,
        demand_set=demands_turn1,
        kill_conditions=("SYNTAX_VALID_IMPLIES_SEMANTIC_TRUE", "MODEL_OUTPUT_IMPLIES_EXECUTION"),
    )

    artifact_turn1 = compile_prompt_artifact(
        regime_definition_bytes=REGIME_BYTES,
        regime_kind="branch_o_observational",
        objective_typed=obj_turn1,
        demand_set=demands_turn1,
        open_obstructions=hints_turn1,
        kill_conditions=("MODEL_OUTPUT_IMPLIES_EXECUTION", "SYNTAX_VALID_IMPLIES_SEMANTIC_TRUE"),
        prompt_body_bytes=body_bytes_1,
        residual_colour="Open",
    )

    assert artifact_turn1.authority_effect == "None"
    assert artifact_turn1.residual_colour == "Open"

    # Persist prompt artifact & body to content-addressed storage
    art_path_1 = write_prompt_artifact(tmp_path, artifact_turn1)
    body_path_1 = write_prompt_body(tmp_path, body_bytes_1)
    assert art_path_1.exists()
    assert body_path_1.exists()

    # -----------------------------------------------------------------------
    # Step 3: Model emits Candidate Proposals; Host scores & ranks them
    # -----------------------------------------------------------------------
    # alpha_1: eliminates OBS-01 and OBS-02 with structural cost 0.5
    prop_1 = CandidateProposal(
        proposal_id="proposal-turn1-alpha1",
        repaired_obstruction_ids=("OBS-01", "OBS-02"),
        structural_cost=0.5,
    )
    # alpha_2: eliminates OBS-01 with cost 0.0
    prop_2 = CandidateProposal(
        proposal_id="proposal-turn1-alpha2",
        repaired_obstruction_ids=("OBS-01",),
        structural_cost=0.0,
    )
    # alpha_3: illegal proposal triggering kill condition
    prop_3 = CandidateProposal(
        proposal_id="proposal-turn1-alpha3",
        kill_triggers=("MODEL_OUTPUT_IMPLIES_EXECUTION",),
    )

    ranked_props = rank_candidate_proposals(
        ledger.active_ids,
        [prop_2, prop_3, prop_1],
    )
    assert len(ranked_props) == 3
    # prop_1: delta = 2.0, efficiency = 2.0 / 1.5 = 1.333
    # prop_2: delta = 1.0, efficiency = 1.0 / 1.0 = 1.0
    # prop_3: illegal (-inf)
    assert ranked_props[0].proposal_id == "proposal-turn1-alpha1"
    assert ranked_props[1].proposal_id == "proposal-turn1-alpha2"
    assert not ranked_props[2].is_legal

    winning_prop = ranked_props[0]

    # -----------------------------------------------------------------------
    # Step 4: Host adopts winning proposal, reconciles ledger, emits EliminationReceipt
    # -----------------------------------------------------------------------
    before_ledger_active = dict(ledger._active)

    # Reconcile ledger: only OBS-03 remains
    proj_1 = _make_projection({"OBS-03": 1.5}, step=1)
    ledger.reconcile(proj_1, step=1, witness="host_accepted_alpha1")

    assert ledger.active_ids == ("OBS-03",)

    # Compute residual drop metrics from ledger maps
    drop_turn1 = residual_drop_from_ledger_maps(
        before_ledger_active,
        ledger._active,
        cost=prop_1.structural_cost,
    )
    assert drop_turn1.omega_mass == 4.5
    assert drop_turn1.residual_mass == 1.5
    assert drop_turn1.delta == 3.0
    assert drop_turn1.eliminated_ids == ("OBS-01", "OBS-02")
    assert drop_turn1.residual_colour == "Open"

    # Host emits EliminationReceiptV1
    receipt_turn1 = create_elimination_receipt(
        packet_id=artifact_turn1.prompt_artifact_id,
        prior_residual_colour="Open",
        new_residual_colour="Open",
        evidence_root=SAMPLE_HEX64_EV_1,
        eliminated_obstruction_ids=drop_turn1.eliminated_ids,
    )
    assert receipt_turn1.authority_effect == "None"
    assert receipt_turn1.new_residual_colour == "Open"
    assert receipt_turn1.dual_witness_ref is None

    # Persist receipt
    receipt_path_1 = write_elimination_receipt(tmp_path, receipt_turn1)
    assert receipt_path_1.exists()

    # -----------------------------------------------------------------------
    # Step 5: Turn 2 — Compile PromptArtifact for surviving OBS-03
    # -----------------------------------------------------------------------
    obj_turn2 = ObjectiveTypedV1(
        kind="terminal_closure",
        summary="discharge final obstruction with dual witness",
        target_obstruction_ids=ledger.active_ids,
    )
    hints_turn2 = (
        ObstructionHintV1(
            obstruction_id="OBS-03",
            family="undecidable_treated_as_equal",
            residual_colour="Open",
        ),
    )
    body_bytes_2 = render_prompt_body(
        REGIME_BYTES,
        objective_typed=obj_turn2,
        open_obstructions=hints_turn2,
        demand_set=(),
        kill_conditions=("EXACT_WITHOUT_DUAL_WITNESS", "MODEL_OUTPUT_IMPLIES_EXECUTION"),
    )
    artifact_turn2 = compile_prompt_artifact(
        regime_definition_bytes=REGIME_BYTES,
        regime_kind="branch_o_observational",
        objective_typed=obj_turn2,
        demand_set=(),
        open_obstructions=hints_turn2,
        kill_conditions=("EXACT_WITHOUT_DUAL_WITNESS", "MODEL_OUTPUT_IMPLIES_EXECUTION"),
        prompt_body_bytes=body_bytes_2,
        parent_packet_id=artifact_turn1.prompt_artifact_id,
        residual_colour="Open",
    )

    art_path_2 = write_prompt_artifact(tmp_path, artifact_turn2)
    body_path_2 = write_prompt_body(tmp_path, body_bytes_2)
    assert art_path_2.exists()
    assert body_path_2.exists()

    # -----------------------------------------------------------------------
    # Step 6: Model emits Candidate Proposal with Dual-Witness certificate
    # -----------------------------------------------------------------------
    prop_turn2 = CandidateProposal(
        proposal_id="proposal-turn2-final-exact",
        repaired_obstruction_ids=("OBS-03",),
        dual_witness_ref=SAMPLE_HEX64_WITNESS,
        structural_cost=0.0,
    )

    res_turn2 = score_discrete_proposal(ledger.active_ids, prop_turn2)
    assert res_turn2.is_legal
    assert res_turn2.post_residual_norm == 0.0
    assert res_turn2.is_exact_candidate
    assert res_turn2.dual_witness_ref == SAMPLE_HEX64_WITNESS

    # -----------------------------------------------------------------------
    # Step 7: Host verifies, reconciles ledger to empty, and emits Exact receipt
    # -----------------------------------------------------------------------
    proj_2 = _make_projection({}, step=2)  # empty obstructions
    ledger.reconcile(proj_2, step=2, witness="dual_witness_verified")
    assert ledger.active_ids == ()

    receipt_turn2 = create_elimination_receipt(
        packet_id=artifact_turn2.prompt_artifact_id,
        prior_residual_colour="Open",
        new_residual_colour="Exact",
        evidence_root=SAMPLE_HEX64_EV_2,
        eliminated_obstruction_ids=("OBS-03",),
        dual_witness_ref=SAMPLE_HEX64_WITNESS,
    )

    assert receipt_turn2.new_residual_colour == "Exact"
    assert receipt_turn2.dual_witness_ref == SAMPLE_HEX64_WITNESS
    assert receipt_turn2.authority_effect == "None"

    # Persist receipt
    receipt_path_2 = write_elimination_receipt(tmp_path, receipt_turn2)
    assert receipt_path_2.exists()

    # Render machine block + host elimination block and parse
    rendered_block = render_elimination_receipt_block(receipt_turn2)
    parsed_block = parse_elimination_receipt_block(rendered_block)
    assert parsed_block is not None
    assert parsed_block["ELIMINATED"] == "OBS-03"
    assert parsed_block["NEW_RESIDUAL_COLOUR"] == "Exact"
    assert parsed_block["DUAL_WITNESS_REF"] == SAMPLE_HEX64_WITNESS
    assert parsed_block["AUTHORITY_EFFECT"] == "None"

    # -----------------------------------------------------------------------
    # Step 8: Verify wire round-trip of all saved artifacts on disk
    # -----------------------------------------------------------------------
    # Check that reading back saved JSON matches Layer A identity digests
    import json
    loaded_art1 = PromptArtifactV1.from_dict(json.loads(art_path_1.read_text("utf-8")))
    assert loaded_art1.prompt_artifact_id == artifact_turn1.prompt_artifact_id

    loaded_rec1 = EliminationReceiptV1.from_dict(json.loads(receipt_path_1.read_text("utf-8")))
    assert loaded_rec1.elimination_receipt_id == receipt_turn1.elimination_receipt_id

    loaded_rec2 = EliminationReceiptV1.from_dict(json.loads(receipt_path_2.read_text("utf-8")))
    assert loaded_rec2.elimination_receipt_id == receipt_turn2.elimination_receipt_id
