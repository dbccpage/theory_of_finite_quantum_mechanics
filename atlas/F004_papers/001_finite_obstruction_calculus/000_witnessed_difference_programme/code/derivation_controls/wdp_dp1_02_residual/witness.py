"""Scoped finite derivation/assumption control for WDP-DP1-02-RESIDUAL (State DP-1 countermodel 2 in Lean)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_wdp_dp1_02_residual(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "WDP-DP1-02-RESIDUAL",
            "dp1_countermodel_no_total_fn",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "WDP-DP1-02-RESIDUAL",
            "dp1_countermodel_no_total_fn",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (3, 2, 0)
    if candidate != expected:
        return ControlReceipt(
            "WDP-DP1-02-RESIDUAL",
            "dp1_countermodel_no_total_fn",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "WDP-DP1-02-RESIDUAL",
        "dp1_countermodel_no_total_fn",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_wdp_dp1_02_residual() -> dict[str, object]:
    ok = evaluate_wdp_dp1_02_residual((3, 2, 0))
    bad_val = evaluate_wdp_dp1_02_residual((3 + 1, 2, 0))
    bad_promo = evaluate_wdp_dp1_02_residual((3, 2, 0), allow_unrestricted_promotion=True)
    return {
        "control_id": "WDP-DP1-02-RESIDUAL",
        "domain": "dp1_countermodel_no_total_fn",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
