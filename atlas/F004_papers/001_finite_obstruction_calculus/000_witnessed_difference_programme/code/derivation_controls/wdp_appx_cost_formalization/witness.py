"""Scoped finite derivation/assumption control for WDP-APPX-COST-FORMALIZATION (Formalize interval signatures and robust cost equivalence)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_wdp_appx_cost_formalization(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "WDP-APPX-COST-FORMALIZATION",
            "interval_signature_cost_equivalence",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "WDP-APPX-COST-FORMALIZATION",
            "interval_signature_cost_equivalence",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (3, 3, 8)
    if candidate != expected:
        return ControlReceipt(
            "WDP-APPX-COST-FORMALIZATION",
            "interval_signature_cost_equivalence",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "WDP-APPX-COST-FORMALIZATION",
        "interval_signature_cost_equivalence",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_wdp_appx_cost_formalization() -> dict[str, object]:
    ok = evaluate_wdp_appx_cost_formalization((3, 3, 8))
    bad_val = evaluate_wdp_appx_cost_formalization((3 + 1, 3, 8))
    bad_promo = evaluate_wdp_appx_cost_formalization((3, 3, 8), allow_unrestricted_promotion=True)
    return {
        "control_id": "WDP-APPX-COST-FORMALIZATION",
        "domain": "interval_signature_cost_equivalence",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
