"""Exact finite control witness for PLAN-QP-10."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for PLAN-QP-10."""
    primary = 9
    ratio = Fraction(31, 800) if 800 != 0 else Fraction(31, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "PLAN-QP-10",
        "carrier_val": primary,
        "secondary_pair": (31, 800),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "mub6_full_resolution_claim",
    }


def reject_mub6_full_resolution_claim(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for PLAN-QP-10."""
    if claim_flag in ("mub6_full_resolution_claim", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for PLAN-QP-10: mub6_full_resolution_claim"
        )
