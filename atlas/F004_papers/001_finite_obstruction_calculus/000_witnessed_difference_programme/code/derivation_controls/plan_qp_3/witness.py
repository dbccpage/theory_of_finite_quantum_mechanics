"""Exact finite control witness for PLAN-QP-3."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for PLAN-QP-3."""
    primary = 8
    ratio = Fraction(196, 25) if 25 != 0 else Fraction(196, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "PLAN-QP-3",
        "carrier_val": primary,
        "secondary_pair": (196, 25),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "gaussian_rational_tsirelson_attainment",
    }


def reject_gaussian_rational_tsirelson_attainment(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for PLAN-QP-3."""
    if claim_flag in ("gaussian_rational_tsirelson_attainment", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for PLAN-QP-3: gaussian_rational_tsirelson_attainment"
        )
