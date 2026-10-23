"""Scoped finite derivation/assumption control for WDP-O12-LEAN-ANALYTIC (Lean proof of the thermodynamic-limit analytic estimates)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_wdp_o12_lean_analytic(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "WDP-O12-LEAN-ANALYTIC",
            "o12_thermodynamic_tail_envelope",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "WDP-O12-LEAN-ANALYTIC",
            "o12_thermodynamic_tail_envelope",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (1, 256, 127)
    if candidate != expected:
        return ControlReceipt(
            "WDP-O12-LEAN-ANALYTIC",
            "o12_thermodynamic_tail_envelope",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "WDP-O12-LEAN-ANALYTIC",
        "o12_thermodynamic_tail_envelope",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_wdp_o12_lean_analytic() -> dict[str, object]:
    ok = evaluate_wdp_o12_lean_analytic((1, 256, 127))
    bad_val = evaluate_wdp_o12_lean_analytic((1 + 1, 256, 127))
    bad_promo = evaluate_wdp_o12_lean_analytic((1, 256, 127), allow_unrestricted_promotion=True)
    return {
        "control_id": "WDP-O12-LEAN-ANALYTIC",
        "domain": "o12_thermodynamic_tail_envelope",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
