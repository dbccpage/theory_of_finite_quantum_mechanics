"""Exact replay of the admitted GEN-WDP-O01 primitive-to-witness floor."""

import json
from pathlib import Path

from witnessed_difference.gen_wdp_o01_admission_floor import (
    SCHEMA,
    WITNESS_ID,
    admission_floor_witness,
    canonical_payload,
    problem_sha256,
)

RECEIPT = (
    Path(__file__).resolve().parents[2]
    / "evidence"
    / "gen_wdp_o01_admission_floor_receipt.json"
)


def test_admission_floor_matches_its_receipt() -> None:
    witness = admission_floor_witness()
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert witness["schema"] == SCHEMA
    assert witness["witness_id"] == WITNESS_ID
    assert witness["admitted_object"] == "primitive-to-witness-admission-floor"
    assert witness["admitted"] == [
        "carrier",
        "signature",
        "irreflexivity-law",
        "no-form-challenge-generation-floor",
    ]
    assert witness["register_row_remains_open"] is True
    assert witness["stronger_floor_proved"] is False
    assert witness["stronger_floor_has_theorem_and_falsifier"] is False
    assert witness["genesis_cost_floor_proved"] is False
    assert witness["declared_responses_exhaust_every_language"] is False
    assert witness["all_regime_challenge_refinement_proved"] is False
    assert witness["irreflexivity_chosen_by_observational_floor"] is False
    assert witness["program_refinement_proved"] is False
    assert witness["generated_token_freshness_proved"] is False
    assert witness["law_selects_one_orientation"] is False
    assert witness["orientations_retained"] == 2
    assert witness["subsingleton_cut_refused"] is True
    assert witness["singleton_instance_without_law"] is True
    assert witness["singleton_law_without_instance"] is True
    assert witness["collapsed_endpoints_force_diagonal"] is True
    assert witness["collapsed_image_obeys_instance_and_law"] is False
    assert witness["identity_transport_preserves_separation"] is True
    assert witness["inscription"]["dedup_datum_count"] == 1
    assert witness["inscription"]["law_present"] is False
    assert witness["raw_item_costs_tie"] is True
    assert witness["declared_arity_selects_unary"] is True
    assert witness["declared_prices_are_not_a_cost_theorem"] is True
    assert witness["datum_without_form_separates"] is False
    assert witness["form_without_instance_separates"] is False
    assert witness["uniform_rule_separates"] is False
    assert witness["pair_cover_size"] == 1
    assert witness["pair_mu1_count"] == 6
    assert witness["pair_mu1_item_cost"] == 2
    assert witness["pair_mu2_count"] == 2
    assert witness["pair_mu2_arity"] == 1
    assert witness["diagonal_instances_retained"] is True
    assert witness["triangle_cover_size"] == 2
    assert witness["triangle_mu2_count"] == 6
    assert witness["triangle_mu2_arity"] == 2
    assert witness["tetrahedron_cover_size"] == 3
    assert witness["tetrahedron_arity_2_count"] == 0
    assert witness["tetrahedron_mu2_count"] == 24
    assert witness["tetrahedron_mu2_arity"] == 3
    digest = problem_sha256(witness)
    assert receipt["problem_sha256"] == digest
    assert receipt["witness"] == witness
    assert receipt["canonical_payload_sha256"] == digest
    assert canonical_payload(witness) == canonical_payload(receipt["witness"])
