"""Scoped finite derivation/assumption control for WDP-CH23-NEXT-TEST (Calibrated instance study for observer completion)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_wdp_ch23_next_test(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "WDP-CH23-NEXT-TEST",
            "calibrated_observer_completion",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "WDP-CH23-NEXT-TEST",
            "calibrated_observer_completion",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (4, 4, 1)
    if candidate != expected:
        return ControlReceipt(
            "WDP-CH23-NEXT-TEST",
            "calibrated_observer_completion",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "WDP-CH23-NEXT-TEST",
        "calibrated_observer_completion",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_wdp_ch23_next_test() -> dict[str, object]:
    ok = evaluate_wdp_ch23_next_test((4, 4, 1))
    bad_val = evaluate_wdp_ch23_next_test((4 + 1, 4, 1))
    bad_promo = evaluate_wdp_ch23_next_test((4, 4, 1), allow_unrestricted_promotion=True)
    return {
        "control_id": "WDP-CH23-NEXT-TEST",
        "domain": "calibrated_observer_completion",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
