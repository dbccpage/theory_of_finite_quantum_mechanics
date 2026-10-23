"""Scoped finite derivation/assumption control for PO001-NATIVE-TRANSPORT (Finite restriction-system to DDC/MSSN history-carrier transport and path-error control)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_po001_native_transport(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "PO001-NATIVE-TRANSPORT",
            "po001_ddc_mssn_native_transport",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "PO001-NATIVE-TRANSPORT",
            "po001_ddc_mssn_native_transport",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (4, 3, 1)
    if candidate != expected:
        return ControlReceipt(
            "PO001-NATIVE-TRANSPORT",
            "po001_ddc_mssn_native_transport",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "PO001-NATIVE-TRANSPORT",
        "po001_ddc_mssn_native_transport",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_po001_native_transport() -> dict[str, object]:
    ok = evaluate_po001_native_transport((4, 3, 1))
    bad_val = evaluate_po001_native_transport((4 + 1, 3, 1))
    bad_promo = evaluate_po001_native_transport((4, 3, 1), allow_unrestricted_promotion=True)
    return {
        "control_id": "PO001-NATIVE-TRANSPORT",
        "domain": "po001_ddc_mssn_native_transport",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
