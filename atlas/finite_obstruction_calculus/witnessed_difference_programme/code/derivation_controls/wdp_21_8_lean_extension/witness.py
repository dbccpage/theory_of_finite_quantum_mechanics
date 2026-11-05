"""Scoped finite derivation/assumption control for WDP-21-8-LEAN-EXTENSION (Extend partial Lean bindings to the complete prose results)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_wdp_21_8_lean_extension(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "WDP-21-8-LEAN-EXTENSION",
            "ch21_8_lean_scope_accounting",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "WDP-21-8-LEAN-EXTENSION",
            "ch21_8_lean_scope_accounting",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (154, 124, 30)
    if candidate != expected:
        return ControlReceipt(
            "WDP-21-8-LEAN-EXTENSION",
            "ch21_8_lean_scope_accounting",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "WDP-21-8-LEAN-EXTENSION",
        "ch21_8_lean_scope_accounting",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_wdp_21_8_lean_extension() -> dict[str, object]:
    ok = evaluate_wdp_21_8_lean_extension((154, 124, 30))
    bad_val = evaluate_wdp_21_8_lean_extension((154 + 1, 124, 30))
    bad_promo = evaluate_wdp_21_8_lean_extension((154, 124, 30), allow_unrestricted_promotion=True)
    return {
        "control_id": "WDP-21-8-LEAN-EXTENSION",
        "domain": "ch21_8_lean_scope_accounting",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
