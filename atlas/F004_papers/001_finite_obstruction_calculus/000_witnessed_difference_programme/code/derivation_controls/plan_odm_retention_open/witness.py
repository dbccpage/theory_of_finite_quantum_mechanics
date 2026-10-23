"""Scoped finite derivation/assumption control for PLAN-ODM-RETENTION-OPEN (Multi-step future retention and transported action-label control (GEN-WDP-73))."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_plan_odm_retention_open(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "PLAN-ODM-RETENTION-OPEN",
            "odm_multi_step_future_retention",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "PLAN-ODM-RETENTION-OPEN",
            "odm_multi_step_future_retention",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (5, 5, 0)
    if candidate != expected:
        return ControlReceipt(
            "PLAN-ODM-RETENTION-OPEN",
            "odm_multi_step_future_retention",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "PLAN-ODM-RETENTION-OPEN",
        "odm_multi_step_future_retention",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_plan_odm_retention_open() -> dict[str, object]:
    ok = evaluate_plan_odm_retention_open((5, 5, 0))
    bad_val = evaluate_plan_odm_retention_open((5 + 1, 5, 0))
    bad_promo = evaluate_plan_odm_retention_open((5, 5, 0), allow_unrestricted_promotion=True)
    return {
        "control_id": "PLAN-ODM-RETENTION-OPEN",
        "domain": "odm_multi_step_future_retention",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
