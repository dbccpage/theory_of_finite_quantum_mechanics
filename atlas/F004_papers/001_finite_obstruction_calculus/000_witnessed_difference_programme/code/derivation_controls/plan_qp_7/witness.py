"""Exact finite control witness for PLAN-QP-7."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for PLAN-QP-7."""
    primary = 3
    ratio = Fraction(0, 1) if 1 != 0 else Fraction(0, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "PLAN-QP-7",
        "carrier_val": primary,
        "secondary_pair": (0, 1),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "trivial_group_dephasing_at_n2",
    }


def reject_trivial_group_dephasing_at_n2(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for PLAN-QP-7."""
    if claim_flag in ("trivial_group_dephasing_at_n2", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for PLAN-QP-7: trivial_group_dephasing_at_n2"
        )
