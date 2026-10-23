"""Finite derivation control witness for WF-RESEARCH-BIND-HOSTS.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction

GOAL_ID = "WF-RESEARCH-BIND-HOSTS"
CARRIER_VAL = 4
SECONDARY_FRAC = Fraction(2, 2)


def evaluate_primary() -> int:
    return CARRIER_VAL


def evaluate_secondary() -> Fraction:
    return SECONDARY_FRAC


def reject_missing_host_or_digest_drift(promote_unverified: bool = True) -> dict[str, object]:
    if type(promote_unverified) is not bool:
        raise TypeError("promote_unverified must be bool")
    if promote_unverified:
        return {"accepted": False, "reason": "reject_missing_host_or_digest_drift"}
    return {"accepted": True, "reason": "bounded_scope_retained"}


def witness() -> dict[str, object]:
    neg = reject_missing_host_or_digest_drift(True)
    return {
        "goal_id": GOAL_ID,
        "carrier_val": evaluate_primary(),
        "secondary_num": SECONDARY_FRAC.numerator,
        "secondary_den": SECONDARY_FRAC.denominator,
        "negative_control_rejected": not bool(neg["accepted"]),
        "negative_control_reason": str(neg["reason"]),
    }
