"""Exact replay of the selected CH19-O03 phase and readout witness."""

import json
from pathlib import Path

from witnessed_difference.ch19_o03_phase_readout import (
    SCHEMA,
    WITNESS_ID,
    canonical_payload,
    phase_readout_witness,
    problem_sha256,
)

RECEIPT = (
    Path(__file__).resolve().parents[2]
    / "evidence"
    / "ch19_o03_phase_readout_receipt.json"
)


def test_phase_readout_matches_its_receipt() -> None:
    witness = phase_readout_witness()
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert witness["schema"] == SCHEMA
    assert witness["witness_id"] == WITNESS_ID
    assert witness["continuous_character_computed"] is False
    assert witness["anchor_norm"] == "1/1"
    assert witness["anchor_equals_ratio"] is True
    assert witness["no_unit_square_root_in_qi"] is True
    assert witness["anchor_infinite_order"] is True
    assert witness["rational_turn_loop"] == "5/12"
    assert witness["gauge_loop_unchanged"] is True
    assert witness["integer_cycle_not_coboundary"] is True
    assert witness["rational_turn_identifies_integer_cycle"] is True
    assert witness["quadratic_probabilities"] == ["1/5", "4/5"]
    assert witness["quartic_probabilities"] == ["1/17", "16/17"]
    assert witness["readouts_differ"] is True
    assert witness["common_phase_preserves_norms"] is True
    assert witness["common_phase_preserves_cross"] is True
    assert witness["born_matches_quadratic"] is True
    assert witness["born_matches_quartic"] is False
    assert witness["phase_invariance_selects_born"] is False
    assert witness["unnormalized_quadratic"] == "4/1"
    assert witness["unnormalized_quartic"] == "16/1"
    digest = problem_sha256(witness)
    assert receipt["problem_sha256"] == digest
    assert receipt["witness"] == witness
    assert receipt["canonical_payload_sha256"] == digest
    assert canonical_payload(witness) == canonical_payload(receipt["witness"])
