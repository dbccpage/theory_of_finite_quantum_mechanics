"""Exact finite control witness for PLAN-QP-C7."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for PLAN-QP-C7."""
    primary = 3
    ratio = Fraction(13, 12) if 12 != 0 else Fraction(13, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "PLAN-QP-C7",
        "carrier_val": primary,
        "secondary_pair": (13, 12),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "rigorous_bound_claim_for_neville_proxy",
    }


def reject_rigorous_bound_claim_for_neville_proxy(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for PLAN-QP-C7."""
    if claim_flag in ("rigorous_bound_claim_for_neville_proxy", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for PLAN-QP-C7: rigorous_bound_claim_for_neville_proxy"
        )
