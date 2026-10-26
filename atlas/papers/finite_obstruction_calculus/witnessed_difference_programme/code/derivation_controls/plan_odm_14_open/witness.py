"""Scoped finite derivation/assumption control for PLAN-ODM-14-OPEN (Coupling/temperature scaling and common-mesh smeared observable control)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_plan_odm_14_open(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "PLAN-ODM-14-OPEN",
            "odm_14_smeared_observable_mesh",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "PLAN-ODM-14-OPEN",
            "odm_14_smeared_observable_mesh",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (3, 3, 1)
    if candidate != expected:
        return ControlReceipt(
            "PLAN-ODM-14-OPEN",
            "odm_14_smeared_observable_mesh",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "PLAN-ODM-14-OPEN",
        "odm_14_smeared_observable_mesh",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_plan_odm_14_open() -> dict[str, object]:
    ok = evaluate_plan_odm_14_open((3, 3, 1))
    bad_val = evaluate_plan_odm_14_open((3 + 1, 3, 1))
    bad_promo = evaluate_plan_odm_14_open((3, 3, 1), allow_unrestricted_promotion=True)
    return {
        "control_id": "PLAN-ODM-14-OPEN",
        "domain": "odm_14_smeared_observable_mesh",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
