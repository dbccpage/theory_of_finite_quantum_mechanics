"""Finite derivation control witness for WF-RESEARCH-BIND-OEWAS.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction

GOAL_ID = "WF-RESEARCH-BIND-OEWAS"
CARRIER_VAL = 9
SECONDARY_FRAC = Fraction(1, 1)


def evaluate_primary() -> int:
    return CARRIER_VAL


def evaluate_secondary() -> Fraction:
    return SECONDARY_FRAC


def reject_invented_catalog_hash(promote_unverified: bool = True) -> dict[str, object]:
    if type(promote_unverified) is not bool:
        raise TypeError("promote_unverified must be bool")
    if promote_unverified:
        return {"accepted": False, "reason": "reject_invented_catalog_hash"}
    return {"accepted": True, "reason": "bounded_scope_retained"}


def witness() -> dict[str, object]:
    neg = reject_invented_catalog_hash(True)
    return {
        "goal_id": GOAL_ID,
        "carrier_val": evaluate_primary(),
        "secondary_num": SECONDARY_FRAC.numerator,
        "secondary_den": SECONDARY_FRAC.denominator,
        "negative_control_rejected": not bool(neg["accepted"]),
        "negative_control_reason": str(neg["reason"]),
    }
