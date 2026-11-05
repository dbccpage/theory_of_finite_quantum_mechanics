"""Scoped finite derivation/assumption control for DEC-WDP-REPIN (Owner decides whether to repin the sealed WDP release)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_dec_wdp_repin(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "DEC-WDP-REPIN",
            "wdp_release_repin_decision",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "DEC-WDP-REPIN",
            "wdp_release_repin_decision",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (2183, 2184, 1)
    if candidate != expected:
        return ControlReceipt(
            "DEC-WDP-REPIN",
            "wdp_release_repin_decision",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "DEC-WDP-REPIN",
        "wdp_release_repin_decision",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_dec_wdp_repin() -> dict[str, object]:
    ok = evaluate_dec_wdp_repin((2183, 2184, 1))
    bad_val = evaluate_dec_wdp_repin((2183 + 1, 2184, 1))
    bad_promo = evaluate_dec_wdp_repin((2183, 2184, 1), allow_unrestricted_promotion=True)
    return {
        "control_id": "DEC-WDP-REPIN",
        "domain": "wdp_release_repin_decision",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
