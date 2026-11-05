"""Exact rational witness for WDP-O12-THETA-ABOVE-1-128 (`derivation.md`).

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any

M1 = Fraction(24576, 43)


def lift_error_bound(length: int, theta: Fraction) -> Fraction:
    if length < 4 or length % 2 != 0:
        raise ValueError("L must be even and >= 4")
    if abs(theta) >= Fraction(1, 128):
        raise ValueError("lift_error_bound is undefined for |theta| >= 1/128")
    return 4 * M1 * length * ((128 * abs(theta)) ** length)


def witness() -> dict[str, Any]:
    img_ratio = Fraction(96, 128)
    wrap_tail = Fraction(2, 1) / (1 - img_ratio**4)
    wrap_total = 1 + wrap_tail
    wrap_margin = 4 - wrap_total
    four_m1 = 4 * M1

    return {
        "ratio_128_over_192": Fraction(128, 192),
        "gap_128_minus_192": Fraction(1, 128) - Fraction(1, 192),
        "polymer_bond_label_norm": Fraction(3, 4) * Fraction(1, 96),
        "polymer_source_label_norm": Fraction(1, 64) * Fraction(1, 2),
        "image_ratio_at_128": img_ratio,
        "geometric_wrap_tail": wrap_tail,
        "wrap_factor_total": wrap_total,
        "wrap_margin_below_4": wrap_margin,
        "formal_endpoint_prefactor": four_m1,
        "formal_endpoint_l4": 4 * four_m1,
        "bound_at_l4_theta_1_192": lift_error_bound(4, Fraction(1, 192)),
        "authority_effect": "None",
    }


if __name__ == "__main__":
    print(witness())
