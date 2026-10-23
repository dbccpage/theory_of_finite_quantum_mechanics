"""Exact finite control witness for PLAN-QP-C1."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for PLAN-QP-C1."""
    primary = 0
    ratio = Fraction(3, 1) if 1 != 0 else Fraction(3, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "PLAN-QP-C1",
        "carrier_val": primary,
        "secondary_pair": (3, 1),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "i3_zero_implies_unique_born",
    }


def reject_i3_zero_implies_unique_born(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for PLAN-QP-C1."""
    if claim_flag in ("i3_zero_implies_unique_born", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for PLAN-QP-C1: i3_zero_implies_unique_born"
        )
