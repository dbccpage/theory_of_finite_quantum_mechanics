"""Scoped finite derivation/assumption control for PLAN-ODM-GUARDED-OPEN (General guard classification and higher guarded-history coherence)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_plan_odm_guarded_open(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "PLAN-ODM-GUARDED-OPEN",
            "guarded_history_higher_cell_control",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "PLAN-ODM-GUARDED-OPEN",
            "guarded_history_higher_cell_control",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (8, 12, 6)
    if candidate != expected:
        return ControlReceipt(
            "PLAN-ODM-GUARDED-OPEN",
            "guarded_history_higher_cell_control",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "PLAN-ODM-GUARDED-OPEN",
        "guarded_history_higher_cell_control",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_plan_odm_guarded_open() -> dict[str, object]:
    ok = evaluate_plan_odm_guarded_open((8, 12, 6))
    bad_val = evaluate_plan_odm_guarded_open((8 + 1, 12, 6))
    bad_promo = evaluate_plan_odm_guarded_open((8, 12, 6), allow_unrestricted_promotion=True)
    return {
        "control_id": "PLAN-ODM-GUARDED-OPEN",
        "domain": "guarded_history_higher_cell_control",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
