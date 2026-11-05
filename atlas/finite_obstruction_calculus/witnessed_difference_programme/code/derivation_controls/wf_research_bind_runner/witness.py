"""Finite derivation control witness for WF-RESEARCH-BIND-RUNNER.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction

GOAL_ID = "WF-RESEARCH-BIND-RUNNER"
CARRIER_VAL = 8
SECONDARY_FRAC = Fraction(5, 8)


def evaluate_primary() -> int:
    return CARRIER_VAL


def evaluate_secondary() -> Fraction:
    return SECONDARY_FRAC


def reject_model_stage5_or_copied_stage8_terminal(promote_unverified: bool = True) -> dict[str, object]:
    if type(promote_unverified) is not bool:
        raise TypeError("promote_unverified must be bool")
    if promote_unverified:
        return {"accepted": False, "reason": "reject_model_stage5_or_copied_stage8_terminal"}
    return {"accepted": True, "reason": "bounded_scope_retained"}


def witness() -> dict[str, object]:
    neg = reject_model_stage5_or_copied_stage8_terminal(True)
    return {
        "goal_id": GOAL_ID,
        "carrier_val": evaluate_primary(),
        "secondary_num": SECONDARY_FRAC.numerator,
        "secondary_den": SECONDARY_FRAC.denominator,
        "negative_control_rejected": not bool(neg["accepted"]),
        "negative_control_reason": str(neg["reason"]),
    }
