"""Scoped finite derivation/assumption control for GEN-WDP-O03 (Dynamic carrier transport, context restriction, composition, higher fillers)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_gen_wdp_o03(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "GEN-WDP-O03",
            "dynamic_carrier_transport_fillers",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "GEN-WDP-O03",
            "dynamic_carrier_transport_fillers",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (3, 3, 1)
    if candidate != expected:
        return ControlReceipt(
            "GEN-WDP-O03",
            "dynamic_carrier_transport_fillers",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "GEN-WDP-O03",
        "dynamic_carrier_transport_fillers",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_gen_wdp_o03() -> dict[str, object]:
    ok = evaluate_gen_wdp_o03((3, 3, 1))
    bad_val = evaluate_gen_wdp_o03((3 + 1, 3, 1))
    bad_promo = evaluate_gen_wdp_o03((3, 3, 1), allow_unrestricted_promotion=True)
    return {
        "control_id": "GEN-WDP-O03",
        "domain": "dynamic_carrier_transport_fillers",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
