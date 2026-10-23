"""Scoped finite derivation/assumption control for WDP-APPM-T5 (Appendix M T5: Field-theoretic topological sector)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_wdp_appm_t5(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "WDP-APPM-T5",
            "topological_charge_involution",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "WDP-APPM-T5",
            "topological_charge_involution",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (1, -1, 4)
    if candidate != expected:
        return ControlReceipt(
            "WDP-APPM-T5",
            "topological_charge_involution",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "WDP-APPM-T5",
        "topological_charge_involution",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_wdp_appm_t5() -> dict[str, object]:
    ok = evaluate_wdp_appm_t5((1, -1, 4))
    bad_val = evaluate_wdp_appm_t5((1 + 1, -1, 4))
    bad_promo = evaluate_wdp_appm_t5((1, -1, 4), allow_unrestricted_promotion=True)
    return {
        "control_id": "WDP-APPM-T5",
        "domain": "topological_charge_involution",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
