"""Exact finite control witness for PLAN-QP-C4."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for PLAN-QP-C4."""
    primary = 8
    ratio = Fraction(1, 0) if 0 != 0 else Fraction(1, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "PLAN-QP-C4",
        "carrier_val": primary,
        "secondary_pair": (1, 0),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "proved_theorem_on_cited_input",
    }


def reject_proved_theorem_on_cited_input(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for PLAN-QP-C4."""
    if claim_flag in ("proved_theorem_on_cited_input", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for PLAN-QP-C4: proved_theorem_on_cited_input"
        )
