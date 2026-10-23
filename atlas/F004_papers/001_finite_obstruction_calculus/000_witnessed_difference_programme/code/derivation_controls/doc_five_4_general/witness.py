"""Scoped finite derivation/assumption control for DOC-FIVE-4-GENERAL (General rejection-rule reuse and O05 institutional grant legitimacy)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_doc_five_4_general(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "DOC-FIVE-4-GENERAL",
            "doc_five_4_general_reuse_o05",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "DOC-FIVE-4-GENERAL",
            "doc_five_4_general_reuse_o05",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (3, 2, 1)
    if candidate != expected:
        return ControlReceipt(
            "DOC-FIVE-4-GENERAL",
            "doc_five_4_general_reuse_o05",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "DOC-FIVE-4-GENERAL",
        "doc_five_4_general_reuse_o05",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_doc_five_4_general() -> dict[str, object]:
    ok = evaluate_doc_five_4_general((3, 2, 1))
    bad_val = evaluate_doc_five_4_general((3 + 1, 2, 1))
    bad_promo = evaluate_doc_five_4_general((3, 2, 1), allow_unrestricted_promotion=True)
    return {
        "control_id": "DOC-FIVE-4-GENERAL",
        "domain": "doc_five_4_general_reuse_o05",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
