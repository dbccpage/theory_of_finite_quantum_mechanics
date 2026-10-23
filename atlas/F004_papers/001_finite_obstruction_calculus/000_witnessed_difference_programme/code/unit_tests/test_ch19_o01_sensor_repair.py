"""Exact replay of the selected CH19-O01 sensor-repair witness."""

import json
from pathlib import Path

from witnessed_difference.ch19_o01_sensor_repair import (
    SCHEMA,
    WITNESS_ID,
    canonical_payload,
    problem_sha256,
    sensor_repair_witness,
)

RECEIPT = (
    Path(__file__).resolve().parents[2]
    / "evidence"
    / "ch19_o01_sensor_repair_receipt.json"
)


def test_sensor_repair_matches_its_receipt() -> None:
    witness = sensor_repair_witness()
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert witness["schema"] == SCHEMA
    assert witness["witness_id"] == WITNESS_ID
    assert witness["premises_from_table"] is False
    assert witness["repair_radius"] == "1/2"
    assert witness["lp_value"] == "1/2"
    assert witness["repaired"] == ["3/4", "1/4", "1/2", "1/4", "1/4", "0/1"]
    assert witness["uniform_population_radius"] == "0/1"
    assert witness["incompatible_preparation_radius"] == "1/1"
    assert witness["iid_formula_at_recorded_joint"] == "5/96"
    assert witness["fixed_multiset_squared_error"] == "0/1"
    assert witness["union_bound"] == "7/12"
    assert witness["pair_tolerance"] == "3/2"
    digest = problem_sha256(witness)
    assert receipt["problem_sha256"] == digest
    assert receipt["witness"] == witness
    assert receipt["canonical_payload_sha256"] == digest
    assert canonical_payload(witness) == canonical_payload(receipt["witness"])
