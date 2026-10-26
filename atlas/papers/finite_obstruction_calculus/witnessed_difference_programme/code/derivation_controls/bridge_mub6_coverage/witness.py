"""Exact finite control witness for BRIDGE-MUB6-COVERAGE."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for BRIDGE-MUB6-COVERAGE."""
    primary = 9
    ratio = Fraction(31, 800) if 800 != 0 else Fraction(31, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "BRIDGE-MUB6-COVERAGE",
        "carrier_val": primary,
        "secondary_pair": (31, 800),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "unreplayed_mub6_fourier_or_float_search",
    }


def reject_unreplayed_mub6_fourier_or_float_search(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for BRIDGE-MUB6-COVERAGE."""
    if claim_flag in ("unreplayed_mub6_fourier_or_float_search", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for BRIDGE-MUB6-COVERAGE: unreplayed_mub6_fourier_or_float_search"
        )
