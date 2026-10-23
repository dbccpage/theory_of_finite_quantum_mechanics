"""Scoped finite derivation/assumption control for GEN-WDP-O02 (Source-to-WDP preservation/reflection refinement maps)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_gen_wdp_o02(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "GEN-WDP-O02",
            "source_to_wdp_refinement_map",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "GEN-WDP-O02",
            "source_to_wdp_refinement_map",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (4, 4, 2)
    if candidate != expected:
        return ControlReceipt(
            "GEN-WDP-O02",
            "source_to_wdp_refinement_map",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "GEN-WDP-O02",
        "source_to_wdp_refinement_map",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_gen_wdp_o02() -> dict[str, object]:
    ok = evaluate_gen_wdp_o02((4, 4, 2))
    bad_val = evaluate_gen_wdp_o02((4 + 1, 4, 2))
    bad_promo = evaluate_gen_wdp_o02((4, 4, 2), allow_unrestricted_promotion=True)
    return {
        "control_id": "GEN-WDP-O02",
        "domain": "source_to_wdp_refinement_map",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
