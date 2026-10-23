"""Scoped finite derivation/assumption control for MS-RELEASE (WDP release gates, residual splits and re-certification)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_ms_release(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "MS-RELEASE",
            "ms_release_milestone_gate",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "MS-RELEASE",
            "ms_release_milestone_gate",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (12, 12, 0)
    if candidate != expected:
        return ControlReceipt(
            "MS-RELEASE",
            "ms_release_milestone_gate",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "MS-RELEASE",
        "ms_release_milestone_gate",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_ms_release() -> dict[str, object]:
    ok = evaluate_ms_release((12, 12, 0))
    bad_val = evaluate_ms_release((12 + 1, 12, 0))
    bad_promo = evaluate_ms_release((12, 12, 0), allow_unrestricted_promotion=True)
    return {
        "control_id": "MS-RELEASE",
        "domain": "ms_release_milestone_gate",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
