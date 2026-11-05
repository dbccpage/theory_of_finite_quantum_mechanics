"""Exact finite control witness for BRIDGE-CLOSURE-RATIO-LOWER."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for BRIDGE-CLOSURE-RATIO-LOWER."""
    primary = 1
    ratio = Fraction(1, 2) if 2 != 0 else Fraction(1, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "BRIDGE-CLOSURE-RATIO-LOWER",
        "carrier_val": primary,
        "secondary_pair": (1, 2),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "expansion_implies_unconditional_termination",
    }


def reject_expansion_implies_unconditional_termination(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for BRIDGE-CLOSURE-RATIO-LOWER."""
    if claim_flag in ("expansion_implies_unconditional_termination", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for BRIDGE-CLOSURE-RATIO-LOWER: expansion_implies_unconditional_termination"
        )
