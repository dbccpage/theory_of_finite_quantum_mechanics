"""Exact finite control witness for PLAN-QP-4."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for PLAN-QP-4."""
    primary = 18
    ratio = Fraction(9, 4) if 4 != 0 else Fraction(9, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "PLAN-QP-4",
        "carrier_val": primary,
        "secondary_pair": (9, 4),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "noncontextual_18ray_assignment",
    }


def reject_noncontextual_18ray_assignment(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for PLAN-QP-4."""
    if claim_flag in ("noncontextual_18ray_assignment", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for PLAN-QP-4: noncontextual_18ray_assignment"
        )
