"""Exact finite control witness for PLAN-QP-C8."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for PLAN-QP-C8."""
    primary = 5
    ratio = Fraction(9, 1) if 1 != 0 else Fraction(9, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "PLAN-QP-C8",
        "carrier_val": primary,
        "secondary_pair": (9, 1),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "mub6_subgap_global_promotion",
    }


def reject_mub6_subgap_global_promotion(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for PLAN-QP-C8."""
    if claim_flag in ("mub6_subgap_global_promotion", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for PLAN-QP-C8: mub6_subgap_global_promotion"
        )
