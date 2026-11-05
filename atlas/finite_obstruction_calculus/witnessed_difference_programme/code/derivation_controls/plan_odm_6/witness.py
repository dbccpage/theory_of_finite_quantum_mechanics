"""Scoped finite derivation/assumption control for PLAN-ODM-6 (Compatible carrier refinement, shrinking enclosures, and observable preservation)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_plan_odm_6(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "PLAN-ODM-6",
            "odm_6_carrier_refinement_enclosure",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "PLAN-ODM-6",
            "odm_6_carrier_refinement_enclosure",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (4, 2, 1)
    if candidate != expected:
        return ControlReceipt(
            "PLAN-ODM-6",
            "odm_6_carrier_refinement_enclosure",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "PLAN-ODM-6",
        "odm_6_carrier_refinement_enclosure",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_plan_odm_6() -> dict[str, object]:
    ok = evaluate_plan_odm_6((4, 2, 1))
    bad_val = evaluate_plan_odm_6((4 + 1, 2, 1))
    bad_promo = evaluate_plan_odm_6((4, 2, 1), allow_unrestricted_promotion=True)
    return {
        "control_id": "PLAN-ODM-6",
        "domain": "odm_6_carrier_refinement_enclosure",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
