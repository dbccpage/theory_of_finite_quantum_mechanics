"""Exact finite control witness for PLAN-QP-5."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for PLAN-QP-5."""
    primary = 2
    ratio = Fraction(1, 2) if 2 != 0 else Fraction(1, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "PLAN-QP-5",
        "carrier_val": primary,
        "secondary_pair": (1, 2),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "unassumed_nosignalling_derivation",
    }


def reject_unassumed_nosignalling_derivation(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for PLAN-QP-5."""
    if claim_flag in ("unassumed_nosignalling_derivation", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for PLAN-QP-5: unassumed_nosignalling_derivation"
        )
