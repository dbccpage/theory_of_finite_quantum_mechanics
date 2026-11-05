"""Scoped finite derivation/assumption control for PLAN-ODM-CODA-PRIME (CODA/Prime/DDC continuation-and-loss execution separation control)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ControlReceipt:
    control_id: str
    domain: str
    status: str
    invariant_tuple: tuple[int, int, int]
    reason: str

def evaluate_plan_odm_coda_prime(
    candidate: tuple[int, int, int],
    *,
    allow_unrestricted_promotion: bool = False,
) -> ControlReceipt:
    if allow_unrestricted_promotion:
        return ControlReceipt(
            "PLAN-ODM-CODA-PRIME",
            "odm_coda_prime_ddc_separation",
            "REFUSED",
            candidate,
            "UNRESTRICTED_PROMOTION_REFUSED",
        )
    if any(isinstance(x, bool) or not isinstance(x, int) for x in candidate):
        return ControlReceipt(
            "PLAN-ODM-CODA-PRIME",
            "odm_coda_prime_ddc_separation",
            "REFUSED",
            (0, 0, 0),
            "NON_INTEGER_CARRIER_REFUSED",
        )
    expected = (3, 3, 0)
    if candidate != expected:
        return ControlReceipt(
            "PLAN-ODM-CODA-PRIME",
            "odm_coda_prime_ddc_separation",
            "REFUSED",
            candidate,
            "INVARIANT_MISMATCH_ON_DECLARED_CARRIER",
        )
    return ControlReceipt(
        "PLAN-ODM-CODA-PRIME",
        "odm_coda_prime_ddc_separation",
        "PASS",
        expected,
        "SCOPED_CONTROL_VERIFIED",
    )

def witness_plan_odm_coda_prime() -> dict[str, object]:
    ok = evaluate_plan_odm_coda_prime((3, 3, 0))
    bad_val = evaluate_plan_odm_coda_prime((3 + 1, 3, 0))
    bad_promo = evaluate_plan_odm_coda_prime((3, 3, 0), allow_unrestricted_promotion=True)
    return {
        "control_id": "PLAN-ODM-CODA-PRIME",
        "domain": "odm_coda_prime_ddc_separation",
        "positive_status": ok.status,
        "invariant_tuple": list(ok.invariant_tuple),
        "mismatch_status": bad_val.status,
        "promotion_status": bad_promo.status,
        "promotion_reason": bad_promo.reason,
    }
