"""Scoped finite derivation/assumption control for PLAN-7D-PFP50-CATALOG (PFP50 catalog local check-pass and research-target separation control)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_plan_7d_pfp50_catalog(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "PLAN-7D-PFP50-CATALOG",
            "pfp50_catalog_separation_control",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "PLAN-7D-PFP50-CATALOG",
            "pfp50_catalog_separation_control",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (50, 50, 0)
    if candidate != expected:
        return ControlReceipt(
            "PLAN-7D-PFP50-CATALOG",
            "pfp50_catalog_separation_control",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "PLAN-7D-PFP50-CATALOG",
        "pfp50_catalog_separation_control",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_plan_7d_pfp50_catalog() -> dict[str, object]:
    ok = evaluate_plan_7d_pfp50_catalog((50, 50, 0))
    bad_val = evaluate_plan_7d_pfp50_catalog((50 + 1, 50, 0))
    bad_promo = evaluate_plan_7d_pfp50_catalog((50, 50, 0), allow_unrestricted_promotion=True)
    return {
        "control_id": "PLAN-7D-PFP50-CATALOG",
        "domain": "pfp50_catalog_separation_control",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
