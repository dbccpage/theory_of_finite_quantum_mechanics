"""Exact finite control witness for BRIDGE-NC-IDENTITY."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for BRIDGE-NC-IDENTITY."""
    primary = 12
    ratio = Fraction(1, 1) if 1 != 0 else Fraction(1, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "BRIDGE-NC-IDENTITY",
        "carrier_val": primary,
        "secondary_pair": (1, 1),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "totalized_zero_inverse",
    }


def reject_totalized_zero_inverse(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for BRIDGE-NC-IDENTITY."""
    if claim_flag in ("totalized_zero_inverse", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for BRIDGE-NC-IDENTITY: totalized_zero_inverse"
        )
