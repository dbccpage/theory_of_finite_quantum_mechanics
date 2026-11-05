"""Exact replay of the selected Q2 reconstruction witness."""

import json
from pathlib import Path

from witnessed_difference.q2_reconstruction_package import (
    SCHEMA,
    WITNESS_ID,
    canonical_payload,
    problem_sha256,
    q2_representation_witness,
)

RECEIPT = (
    Path(__file__).resolve().parents[2]
    / "evidence"
    / "q2_reconstruction_package_receipt.json"
)


def test_q2_representation_matches_its_receipt() -> None:
    witness = q2_representation_witness()
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert witness["schema"] == SCHEMA
    assert witness["witness_id"] == WITNESS_ID
    assert witness["chsh"] == "14/5"
    assert witness["chsh_squared"] == "196/25"
    assert witness["operator_square_slack"] == "4/25"
    assert witness["trace_s_squared"] == "196/25"
    assert witness["deterministic_chsh_values"] == [-2, 2]
    assert witness["classical_joint_excluded"] is True
    assert witness["pr_excluded_by_q2_bound"] is True
    assert witness["correlators"] == {
        "00": "3/5",
        "01": "3/5",
        "10": "4/5",
        "11": "-4/5",
    }
    digest = problem_sha256(witness)
    assert receipt["problem_sha256"] == digest
    assert receipt["witness"] == witness
    assert receipt["canonical_payload_sha256"] == digest
    assert canonical_payload(witness) == canonical_payload(receipt["witness"])
