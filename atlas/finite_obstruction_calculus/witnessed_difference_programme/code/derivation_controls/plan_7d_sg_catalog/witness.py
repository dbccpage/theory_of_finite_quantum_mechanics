"""Scoped finite derivation/assumption control for PLAN-7D-SG-CATALOG (Fifty staged Symbol Game episodes Stage 0 and Stages 1-8 reporting control)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_plan_7d_sg_catalog(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "PLAN-7D-SG-CATALOG",
            "sg50_stage_reporting_control",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "PLAN-7D-SG-CATALOG",
            "sg50_stage_reporting_control",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (50, 9, 0)
    if candidate != expected:
        return ControlReceipt(
            "PLAN-7D-SG-CATALOG",
            "sg50_stage_reporting_control",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "PLAN-7D-SG-CATALOG",
        "sg50_stage_reporting_control",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_plan_7d_sg_catalog() -> dict[str, object]:
    ok = evaluate_plan_7d_sg_catalog((50, 9, 0))
    bad_val = evaluate_plan_7d_sg_catalog((50 + 1, 9, 0))
    bad_promo = evaluate_plan_7d_sg_catalog((50, 9, 0), allow_unrestricted_promotion=True)
    return {
        "control_id": "PLAN-7D-SG-CATALOG",
        "domain": "sg50_stage_reporting_control",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
