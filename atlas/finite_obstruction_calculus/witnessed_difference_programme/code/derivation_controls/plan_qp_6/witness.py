"""Exact finite control witness for PLAN-QP-6."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for PLAN-QP-6."""
    primary = 6
    ratio = Fraction(9, 2) if 2 != 0 else Fraction(9, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "PLAN-QP-6",
        "carrier_val": primary,
        "secondary_pair": (9, 2),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "refuted_k23_dual_equality",
    }


def reject_refuted_k23_dual_equality(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for PLAN-QP-6."""
    if claim_flag in ("refuted_k23_dual_equality", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for PLAN-QP-6: refuted_k23_dual_equality"
        )
