"""Scoped finite derivation/assumption control for CH19-O04 (Physical calibration authentication and operational model selection)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_ch19_o04(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "CH19-O04",
            "ch19_calibration_authentication",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "CH19-O04",
            "ch19_calibration_authentication",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (3, 15, 20)
    if candidate != expected:
        return ControlReceipt(
            "CH19-O04",
            "ch19_calibration_authentication",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "CH19-O04",
        "ch19_calibration_authentication",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_ch19_o04() -> dict[str, object]:
    ok = evaluate_ch19_o04((3, 15, 20))
    bad_val = evaluate_ch19_o04((3 + 1, 15, 20))
    bad_promo = evaluate_ch19_o04((3, 15, 20), allow_unrestricted_promotion=True)
    return {
        "control_id": "CH19-O04",
        "domain": "ch19_calibration_authentication",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
