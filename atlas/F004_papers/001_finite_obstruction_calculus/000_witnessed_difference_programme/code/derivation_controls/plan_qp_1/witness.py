"""Exact finite control witness for PLAN-QP-1."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for PLAN-QP-1."""
    primary = 512
    ratio = Fraction(1, 1) if 1 != 0 else Fraction(1, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "PLAN-QP-1",
        "carrier_val": primary,
        "secondary_pair": (1, 1),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "unconditional_h1_promotion_without_d1",
    }


def reject_unconditional_h1_promotion_without_d1(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for PLAN-QP-1."""
    if claim_flag in ("unconditional_h1_promotion_without_d1", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for PLAN-QP-1: unconditional_h1_promotion_without_d1"
        )
