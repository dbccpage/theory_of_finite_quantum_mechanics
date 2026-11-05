"""Exact finite control witness for PLAN-QP-9."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for PLAN-QP-9."""
    primary = 13
    ratio = Fraction(13, 12) if 12 != 0 else Fraction(13, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "PLAN-QP-9",
        "carrier_val": primary,
        "secondary_pair": (13, 12),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "uncertified_neville_continuum_bound",
    }


def reject_uncertified_neville_continuum_bound(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for PLAN-QP-9."""
    if claim_flag in ("uncertified_neville_continuum_bound", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for PLAN-QP-9: uncertified_neville_continuum_bound"
        )
