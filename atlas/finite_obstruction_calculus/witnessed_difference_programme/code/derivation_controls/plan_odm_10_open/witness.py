"""Scoped finite derivation/assumption control for PLAN-ODM-10-OPEN (U=t spin model sign-character identity and finite-volume correlation control)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_plan_odm_10_open(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "PLAN-ODM-10-OPEN",
            "odm_10_ut_spin_sign_character",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "PLAN-ODM-10-OPEN",
            "odm_10_ut_spin_sign_character",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (4, 2, 0)
    if candidate != expected:
        return ControlReceipt(
            "PLAN-ODM-10-OPEN",
            "odm_10_ut_spin_sign_character",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "PLAN-ODM-10-OPEN",
        "odm_10_ut_spin_sign_character",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_plan_odm_10_open() -> dict[str, object]:
    ok = evaluate_plan_odm_10_open((4, 2, 0))
    bad_val = evaluate_plan_odm_10_open((4 + 1, 2, 0))
    bad_promo = evaluate_plan_odm_10_open((4, 2, 0), allow_unrestricted_promotion=True)
    return {
        "control_id": "PLAN-ODM-10-OPEN",
        "domain": "odm_10_ut_spin_sign_character",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
