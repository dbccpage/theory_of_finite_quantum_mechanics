"""Boundary witness for PLAN-ODM-TORIC.

Theorems A and B and Gates D, F, and G stay open as model proposals.
Gate E remains the single frozen point L=4, M=1, r=1/10 and is not an
all-M theorem. This module reads the historical receipt and does not
rewrite it. AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

SCHEMA = "wdp.plan_odm_toric_boundary.v1"
WITNESS_ID = "plan-odm-toric-boundary"
PROGRAMME = Path(__file__).resolve().parents[2]
RECEIPT_RELATIVE = (
    "docs/meron_field_limit_derivations/code/gate_e_exact_counterexample_receipt.json"
)

SOURCE_ANCHORS = (
    "plans/outstanding_derivations_master.md Theorems A and B and Gates D, F, and G stay open as model",
    "witnessed_difference_programme.md ### W.8 Trotter-response, and the closures that stay open",
    "docs/meron_field_limit_derivations/g3_g4_research_dossier_and_next_targets.md Theorem A / Theorem B / Gate D / Gate E",
    "docs/four_source_inventory.md Gate E at L=4, M=1, r=1/10",
    RECEIPT_RELATIVE,
)

OPEN_MODEL_PROPOSALS = (
    {"id": "theorem-a", "title": "continuous-time Gaussian field", "discharged": False},
    {"id": "theorem-b", "title": "joint discrete volume/time limit", "discharged": False},
    {"id": "gate-d", "title": "complex winding sectors", "discharged": False},
    {"id": "gate-f", "title": "spacetime Ursell bound", "discharged": False},
    {"id": "gate-g", "title": "mode extinction", "discharged": False},
)

NAMED_POINT = {
    "L": 4,
    "M": 1,
    "r": "1/10",
    "q": "11/10",
    "X0": "17661/1100",
    "negative_eigenvalue": "-1/706440",
    "quadratic_form_exact": "-1/88305",
    "test_vector": [-1, -1, -1, -1, 1, 1, 1, 1],
    "is_positive_semidefinite": False,
}
DECLARED_REGION_UPPER = Fraction(1, 192)


def canonical_payload(witness: dict[str, object]) -> str:
    return json.dumps(witness, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def problem_sha256(witness: dict[str, object]) -> str:
    return hashlib.sha256(canonical_payload(witness).encode("utf-8")).hexdigest()


def _fraction(text: str) -> Fraction:
    return Fraction(text)


def toric_boundary_witness() -> dict[str, object]:
    """Record the Gate E point and the proposals that stay open."""
    receipt_path = PROGRAMME / RECEIPT_RELATIVE
    raw = receipt_path.read_bytes()
    receipt = json.loads(raw.decode("utf-8"))
    keys = sorted(receipt.keys())
    eigenvalues = [
        {"eigenvalue": key, "multiplicity": int(value)}
        for key, value in sorted(receipt["eigenvalues_exact"].items(), key=lambda item: Fraction(item[0]))
    ]
    spectrum_dimension = sum(item["multiplicity"] for item in eigenvalues)
    vector = [int(entry) for entry in receipt["test_vector"]]
    squared_norm = sum(entry * entry for entry in vector)
    quadratic = _fraction(receipt["quadratic_form_exact"])
    eigenvalue = _fraction(receipt["negative_eigenvalue"])
    radius = _fraction(receipt["r"])
    matches_named_point = (
        receipt["r"] == NAMED_POINT["r"]
        and receipt["q"] == NAMED_POINT["q"]
        and receipt["X0"] == NAMED_POINT["X0"]
        and receipt["negative_eigenvalue"] == NAMED_POINT["negative_eigenvalue"]
        and receipt["quadratic_form_exact"] == NAMED_POINT["quadratic_form_exact"]
        and vector == NAMED_POINT["test_vector"]
        and receipt["is_positive_semidefinite"] is False
    )
    return {
        "schema": SCHEMA,
        "witness_id": WITNESS_ID,
        "authority_effect": "none",
        "admitted_object": "gate-e-single-point-not-an-all-m-theorem",
        "source_anchors": list(SOURCE_ANCHORS),
        "named_point": {
            "L": NAMED_POINT["L"],
            "M": NAMED_POINT["M"],
            "r": NAMED_POINT["r"],
        },
        "declared_region": "r<=1/192",
        "outside_declared_region": radius > DECLARED_REGION_UPPER,
        "historical_receipt": RECEIPT_RELATIVE,
        "historical_receipt_sha256": hashlib.sha256(raw).hexdigest(),
        "historical_receipt_rewritten": False,
        "writer_invoked": False,
        "receipt_keys": keys,
        "receipt_records_L": "L" in receipt,
        "receipt_records_M": "M" in receipt,
        "receipt_records_scaling": any(
            ("scal" in key) or ("asymp" in key) or ("all" in key) for key in keys
        ),
        "negative_eigenvalue": receipt["negative_eigenvalue"],
        "quadratic_form_exact": receipt["quadratic_form_exact"],
        "test_vector": vector,
        "squared_norm": squared_norm,
        "quadratic_equals_eigenvalue_times_squared_norm": quadratic == eigenvalue * squared_norm,
        "spectrum_dimension": spectrum_dimension,
        "spectrum_dimension_matches_two_layers_of_L": spectrum_dimension == 2 * NAMED_POINT["L"],
        "is_positive_semidefinite": receipt["is_positive_semidefinite"],
        "matches_named_point": matches_named_point,
        "all_m_theorem": False,
        "theorems_a_and_b_proved": False,
        "gates_d_f_g_proved": False,
        "open_model_proposals": [dict(item) for item in OPEN_MODEL_PROPOSALS],
    }


def boundary_receipt() -> dict[str, object]:
    witness = toric_boundary_witness()
    digest = problem_sha256(witness)
    return {
        "schema": SCHEMA,
        "witness_id": WITNESS_ID,
        "problem_sha256": digest,
        "canonical_payload_sha256": digest,
        "scope": (
            "Gate E remains the single point L=4, M=1, r=1/10 and is not an all-M theorem; "
            "Theorems A and B and Gates D, F, and G stay open as model proposals"
        ),
        "witness": witness,
    }
