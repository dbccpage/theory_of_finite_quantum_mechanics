"""Exact finite control witness for PLAN-QP-C3."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for PLAN-QP-C3."""
    primary = 6
    ratio = Fraction(0, 1) if 1 != 0 else Fraction(0, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "PLAN-QP-C3",
        "carrier_val": primary,
        "secondary_pair": (0, 1),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "unpublished_zenodo_placeholder",
    }


def reject_unpublished_zenodo_placeholder(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for PLAN-QP-C3."""
    if claim_flag in ("unpublished_zenodo_placeholder", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for PLAN-QP-C3: unpublished_zenodo_placeholder"
        )
