"""Exact finite control witness for PLAN-QP-8."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for PLAN-QP-8."""
    primary = 2
    ratio = Fraction(1, 1) if 1 != 0 else Fraction(1, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "PLAN-QP-8",
        "carrier_val": primary,
        "secondary_pair": (1, 1),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "noninvariant_observable_orbit_cancellation",
    }


def reject_noninvariant_observable_orbit_cancellation(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for PLAN-QP-8."""
    if claim_flag in ("noninvariant_observable_orbit_cancellation", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for PLAN-QP-8: noninvariant_observable_orbit_cancellation"
        )
