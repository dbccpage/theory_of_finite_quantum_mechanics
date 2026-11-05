"""Scoped finite derivation/assumption control for WDP-APPW-NATIVE-REPAIR-BINDINGS (Native physical repair bindings for Appendix W)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_wdp_appw_native_repair_bindings(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "WDP-APPW-NATIVE-REPAIR-BINDINGS",
            "repair_holonomy_preservation",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "WDP-APPW-NATIVE-REPAIR-BINDINGS",
            "repair_holonomy_preservation",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (6, 2, 0)
    if candidate != expected:
        return ControlReceipt(
            "WDP-APPW-NATIVE-REPAIR-BINDINGS",
            "repair_holonomy_preservation",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "WDP-APPW-NATIVE-REPAIR-BINDINGS",
        "repair_holonomy_preservation",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_wdp_appw_native_repair_bindings() -> dict[str, object]:
    ok = evaluate_wdp_appw_native_repair_bindings((6, 2, 0))
    bad_val = evaluate_wdp_appw_native_repair_bindings((6 + 1, 2, 0))
    bad_promo = evaluate_wdp_appw_native_repair_bindings((6, 2, 0), allow_unrestricted_promotion=True)
    return {
        "control_id": "WDP-APPW-NATIVE-REPAIR-BINDINGS",
        "domain": "repair_holonomy_preservation",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
