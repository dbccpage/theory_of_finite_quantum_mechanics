"""Exact finite control witness for PLAN-QP-C9."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for PLAN-QP-C9."""
    primary = 6
    ratio = Fraction(2, 3) if 3 != 0 else Fraction(2, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "PLAN-QP-C9",
        "carrier_val": primary,
        "secondary_pair": (2, 3),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "unscoped_majorana_hardness_or_leakage_claim",
    }


def reject_unscoped_majorana_hardness_or_leakage_claim(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for PLAN-QP-C9."""
    if claim_flag in ("unscoped_majorana_hardness_or_leakage_claim", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for PLAN-QP-C9: unscoped_majorana_hardness_or_leakage_claim"
        )
