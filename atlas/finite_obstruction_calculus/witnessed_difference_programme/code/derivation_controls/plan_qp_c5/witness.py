"""Exact finite control witness for PLAN-QP-C5."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for PLAN-QP-C5."""
    primary = 3
    ratio = Fraction(2, 2) if 2 != 0 else Fraction(2, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "PLAN-QP-C5",
        "carrier_val": primary,
        "secondary_pair": (2, 2),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "undeclared_d1_or_phantom_artifacts",
    }


def reject_undeclared_d1_or_phantom_artifacts(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for PLAN-QP-C5."""
    if claim_flag in ("undeclared_d1_or_phantom_artifacts", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for PLAN-QP-C5: undeclared_d1_or_phantom_artifacts"
        )
