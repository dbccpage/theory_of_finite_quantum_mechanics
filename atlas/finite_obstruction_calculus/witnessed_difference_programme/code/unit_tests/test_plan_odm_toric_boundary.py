"""Exact replay of the PLAN-ODM-TORIC Gate E boundary."""

import hashlib
import json
from pathlib import Path

from witnessed_difference.plan_odm_toric_boundary import (
    SCHEMA,
    WITNESS_ID,
    boundary_receipt,
    canonical_payload,
    problem_sha256,
    toric_boundary_witness,
)

RECEIPT = (
    Path(__file__).resolve().parents[2]
    / "evidence"
    / "plan_odm_toric_boundary_receipt.json"
)
HISTORICAL = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "meron_field_limit_derivations"
    / "code"
    / "gate_e_exact_counterexample_receipt.json"
)


def test_toric_boundary_matches_its_receipt() -> None:
    witness = toric_boundary_witness()
    stored = json.loads(RECEIPT.read_text(encoding="utf-8"))
    digest = problem_sha256(witness)
    assert witness["schema"] == SCHEMA
    assert witness["witness_id"] == WITNESS_ID
    assert witness["admitted_object"] == "gate-e-single-point-not-an-all-m-theorem"
    assert witness["named_point"] == {"L": 4, "M": 1, "r": "1/10"}
    assert witness["outside_declared_region"] is True
    assert witness["matches_named_point"] is True
    assert witness["negative_eigenvalue"] == "-1/706440"
    assert witness["quadratic_form_exact"] == "-1/88305"
    assert witness["test_vector"] == [-1, -1, -1, -1, 1, 1, 1, 1]
    assert witness["quadratic_equals_eigenvalue_times_squared_norm"] is True
    assert witness["spectrum_dimension"] == 8
    assert witness["spectrum_dimension_matches_two_layers_of_L"] is True
    assert witness["is_positive_semidefinite"] is False
    assert witness["all_m_theorem"] is False
    assert witness["theorems_a_and_b_proved"] is False
    assert witness["gates_d_f_g_proved"] is False
    assert witness["historical_receipt_rewritten"] is False
    assert witness["writer_invoked"] is False
    assert witness["receipt_records_L"] is False
    assert witness["receipt_records_M"] is False
    assert witness["receipt_records_scaling"] is False
    assert [item["id"] for item in witness["open_model_proposals"]] == [
        "theorem-a",
        "theorem-b",
        "gate-d",
        "gate-f",
        "gate-g",
    ]
    assert all(item["discharged"] is False for item in witness["open_model_proposals"])
    assert witness["historical_receipt_sha256"] == stored["witness"]["historical_receipt_sha256"]
    historical_bytes = HISTORICAL.read_bytes()
    assert hashlib.sha256(historical_bytes).hexdigest() == witness["historical_receipt_sha256"]
    assert stored["problem_sha256"] == digest
    assert stored["witness"] == witness
    assert stored["canonical_payload_sha256"] == digest
    assert stored == boundary_receipt()
    assert canonical_payload(witness) == canonical_payload(stored["witness"])
