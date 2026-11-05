"""Exact finite control witness for PLAN-QP-2."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for PLAN-QP-2."""
    primary = 14
    ratio = Fraction(14, 5) if 5 != 0 else Fraction(14, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "PLAN-QP-2",
        "carrier_val": primary,
        "secondary_pair": (14, 5),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "mixture_table_as_quantum",
    }


def reject_mixture_table_as_quantum(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for PLAN-QP-2."""
    if claim_flag in ("mixture_table_as_quantum", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for PLAN-QP-2: mixture_table_as_quantum"
        )
