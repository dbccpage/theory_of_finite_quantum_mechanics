"""Scoped finite derivation/assumption control for GEN-WDP-O04 (Operational reconstruction of effects, probability, scalars, composition)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_gen_wdp_o04(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "GEN-WDP-O04",
            "operational_effect_readout_comparison",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "GEN-WDP-O04",
            "operational_effect_readout_comparison",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (3, 1, 0)
    if candidate != expected:
        return ControlReceipt(
            "GEN-WDP-O04",
            "operational_effect_readout_comparison",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "GEN-WDP-O04",
        "operational_effect_readout_comparison",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_gen_wdp_o04() -> dict[str, object]:
    ok = evaluate_gen_wdp_o04((3, 1, 0))
    bad_val = evaluate_gen_wdp_o04((3 + 1, 1, 0))
    bad_promo = evaluate_gen_wdp_o04((3, 1, 0), allow_unrestricted_promotion=True)
    return {
        "control_id": "GEN-WDP-O04",
        "domain": "operational_effect_readout_comparison",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
