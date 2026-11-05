"""Scoped finite derivation/assumption control for MS-PO001-RESIDUAL (PO-001 upgrade residual milestone closure control)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_ms_po001_residual(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "MS-PO001-RESIDUAL",
            "ms_po001_residual_milestone",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "MS-PO001-RESIDUAL",
            "ms_po001_residual_milestone",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (9, 9, 0)
    if candidate != expected:
        return ControlReceipt(
            "MS-PO001-RESIDUAL",
            "ms_po001_residual_milestone",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "MS-PO001-RESIDUAL",
        "ms_po001_residual_milestone",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_ms_po001_residual() -> dict[str, object]:
    ok = evaluate_ms_po001_residual((9, 9, 0))
    bad_val = evaluate_ms_po001_residual((9 + 1, 9, 0))
    bad_promo = evaluate_ms_po001_residual((9, 9, 0), allow_unrestricted_promotion=True)
    return {
        "control_id": "MS-PO001-RESIDUAL",
        "domain": "ms_po001_residual_milestone",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
