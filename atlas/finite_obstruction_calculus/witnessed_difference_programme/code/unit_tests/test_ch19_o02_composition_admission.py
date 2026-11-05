"""Exact replay of the selected CH19-O02 composition-admission witness."""

import json
from pathlib import Path

from witnessed_difference.ch19_o02_composition_admission import (
    SCHEMA,
    WITNESS_ID,
    canonical_payload,
    composition_admission_witness,
    problem_sha256,
)

RECEIPT = (
    Path(__file__).resolve().parents[2]
    / "evidence"
    / "ch19_o02_composition_admission_receipt.json"
)


def test_composition_admission_matches_its_receipt() -> None:
    witness = composition_admission_witness()
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert witness["schema"] == SCHEMA
    assert witness["witness_id"] == WITNESS_ID
    assert witness["derived_from_cp"] is False
    assert witness["dump_right_injective"] is False
    assert witness["identity_tagging_injective"] is True
    assert witness["classical_bilinear_recovers_joint"] is True
    assert witness["deterministic_chsh_values"] == [-2, 2]
    assert witness["pr_no_signalling"] is True
    assert witness["pr_chsh"] == "4/1"
    assert witness["pr_squared_exceeds_8"] is True
    assert witness["density_is_rational_gram"] is True
    assert witness["local_hermitian_involutions"] is True
    assert witness["square_identity"] is True
    assert witness["operator_gap_principal_minors_nonnegative"] is True
    assert witness["quantum_chsh"] == "14/5"
    assert witness["quantum_chsh_squared"] == "196/25"
    assert witness["operator_bound_slack"] == "4/25"
    assert witness["scalar_variance_slack"] == "0/1"
    assert witness["above_classical_joint_bound"] is True
    assert witness["multiplicity_named_by_cp"] is False
    digest = problem_sha256(witness)
    assert receipt["problem_sha256"] == digest
    assert receipt["witness"] == witness
    assert receipt["canonical_payload_sha256"] == digest
    assert canonical_payload(witness) == canonical_payload(receipt["witness"])
