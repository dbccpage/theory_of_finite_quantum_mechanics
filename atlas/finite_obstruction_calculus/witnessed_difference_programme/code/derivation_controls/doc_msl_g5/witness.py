"""Scoped finite derivation/assumption control for DOC-MSL-G5 (Meron spacetime limit Gate G5: joint (L,M) schedule and half-step cumulant error)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_doc_msl_g5(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "DOC-MSL-G5",
            "doc_msl_g5_joint_lm_schedule",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "DOC-MSL-G5",
            "doc_msl_g5_joint_lm_schedule",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (8, 4, 1)
    if candidate != expected:
        return ControlReceipt(
            "DOC-MSL-G5",
            "doc_msl_g5_joint_lm_schedule",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "DOC-MSL-G5",
        "doc_msl_g5_joint_lm_schedule",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_doc_msl_g5() -> dict[str, object]:
    ok = evaluate_doc_msl_g5((8, 4, 1))
    bad_val = evaluate_doc_msl_g5((8 + 1, 4, 1))
    bad_promo = evaluate_doc_msl_g5((8, 4, 1), allow_unrestricted_promotion=True)
    return {
        "control_id": "DOC-MSL-G5",
        "domain": "doc_msl_g5_joint_lm_schedule",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
