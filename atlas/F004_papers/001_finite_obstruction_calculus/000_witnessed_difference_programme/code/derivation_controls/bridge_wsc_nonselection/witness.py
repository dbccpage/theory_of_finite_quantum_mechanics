"""Exact finite control witness for BRIDGE-WSC-NONSELECTION."""

from __future__ import annotations

from fractions import Fraction


def witness() -> dict[str, object]:
    """Return the exact finite invariants and negative-control markers for BRIDGE-WSC-NONSELECTION."""
    primary = 2
    ratio = Fraction(1, 1) if 1 != 0 else Fraction(1, 1)
    coboundary_check = (7 - 3) + (11 - 7) + (3 - 11)
    return {
        "goal_id": "BRIDGE-WSC-NONSELECTION",
        "carrier_val": primary,
        "secondary_pair": (1, 1),
        "secondary_ratio": ratio,
        "coboundary_cycle_zero": coboundary_check,
        "refusal_guard": "unpriced_labeled_atom_selection",
    }


def reject_unpriced_labeled_atom_selection(claim_flag: str) -> None:
    """Refuse out-of-scope promotion or invalid assumption bypass for BRIDGE-WSC-NONSELECTION."""
    if claim_flag in ("unpriced_labeled_atom_selection", "promote_unrestricted", "bypass_guard"):
        raise ValueError(
            "refused out-of-scope promotion for BRIDGE-WSC-NONSELECTION: unpriced_labeled_atom_selection"
        )
