"""Scoped finite derivation/assumption control for WDP-APPM-FIELD-THEORY-ROUTE (Completed Meron route to the selected field theory)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_wdp_appm_field_theory_route(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "WDP-APPM-FIELD-THEORY-ROUTE",
            "meron_five_stage_route_composition",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "WDP-APPM-FIELD-THEORY-ROUTE",
            "meron_five_stage_route_composition",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (5, 5, 0)
    if candidate != expected:
        return ControlReceipt(
            "WDP-APPM-FIELD-THEORY-ROUTE",
            "meron_five_stage_route_composition",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "WDP-APPM-FIELD-THEORY-ROUTE",
        "meron_five_stage_route_composition",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_wdp_appm_field_theory_route() -> dict[str, object]:
    ok = evaluate_wdp_appm_field_theory_route((5, 5, 0))
    bad_val = evaluate_wdp_appm_field_theory_route((5 + 1, 5, 0))
    bad_promo = evaluate_wdp_appm_field_theory_route((5, 5, 0), allow_unrestricted_promotion=True)
    return {
        "control_id": "WDP-APPM-FIELD-THEORY-ROUTE",
        "domain": "meron_five_stage_route_composition",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
