"""Scoped finite derivation/assumption control for WDP-CHS-O03 (Native Rust binding and verification of Python source)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_wdp_chs_o03(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "WDP-CHS-O03",
            "appendix_s_game_checker_parity",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "WDP-CHS-O03",
            "appendix_s_game_checker_parity",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (2, 1, 4)
    if candidate != expected:
        return ControlReceipt(
            "WDP-CHS-O03",
            "appendix_s_game_checker_parity",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "WDP-CHS-O03",
        "appendix_s_game_checker_parity",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_wdp_chs_o03() -> dict[str, object]:
    ok = evaluate_wdp_chs_o03((2, 1, 4))
    bad_val = evaluate_wdp_chs_o03((2 + 1, 1, 4))
    bad_promo = evaluate_wdp_chs_o03((2, 1, 4), allow_unrestricted_promotion=True)
    return {
        "control_id": "WDP-CHS-O03",
        "domain": "appendix_s_game_checker_parity",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
