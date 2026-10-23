"""Exact finite control witness for PLAN-QP-C2."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for PLAN-QP-C2."""
    primary = 9
    ratio = Fraction(9, 9) if 9 != 0 else Fraction(9, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "PLAN-QP-C2",
        "carrier_val": primary,
        "secondary_pair": (9, 9),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "stale_c1000_not_started_status",
    }


def reject_stale_c1000_not_started_status(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for PLAN-QP-C2."""
    if claim_flag in ("stale_c1000_not_started_status", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for PLAN-QP-C2: stale_c1000_not_started_status"
        )
