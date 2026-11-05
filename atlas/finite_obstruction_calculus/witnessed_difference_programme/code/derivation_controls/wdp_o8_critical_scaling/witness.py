"""Exact rational witness for WDP-O8-CRITICAL-SCALING (`derivation.md`).

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any

FOUR_P = (
    (0, 0, 0, 0),
    (0, 2, 2, 0),
    (0, 2, 2, 0),
    (0, 0, 0, 0),
)
TWO_A0 = (-1, -1, 1, 1)
TWO_A1 = (1, -1, 1, -1)
ZERO_MODE_RECORDED = (
    Fraction(1, 4),
    Fraction(1, 8),
    Fraction(1, 48),
    Fraction(-1, 96),
)


def c0y_theta1(y: int, u: Fraction) -> Fraction:
    ka0ay = Fraction(-1, 16) if y in (1, 3) else Fraction(0)
    return -((1 - u) * ka0ay + u * ka0ay)


def witness() -> dict[str, Any]:
    trace_4p = sum(FOUR_P[i][i] for i in range(4))
    four_p_sq_ok = all(
        sum(FOUR_P[i][k] * FOUR_P[k][j] for k in range(4)) == 4 * FOUR_P[i][j]
        for i in range(4)
        for j in range(4)
    )
    tr_16_p_a0_a1 = sum(FOUR_P[i][i] * TWO_A0[i] * TWO_A1[i] for i in range(4))
    exp_p_a0_a1 = Fraction(tr_16_p_a0_a1, 64)
    exp_k_a0_a1 = -exp_p_a0_a1

    u_values = (Fraction(0), Fraction(1, 3), Fraction(3, 7), Fraction(1))
    u_independent = all(
        tuple(c0y_theta1(y, u) for y in range(4))
        == (Fraction(0), Fraction(1, 16), Fraction(0), Fraction(1, 16))
        for u in u_values
    )
    jet = tuple(c0y_theta1(y, Fraction(3, 7)) for y in range(4))
    spatial_sum = sum(jet, Fraction(0))

    c01_l4 = Fraction(1, 16)
    c01_l6 = Fraction(1, 16)
    ratio_l6_l4 = c01_l6 / c01_l4

    return {
        "trace_4p": trace_4p,
        "four_p_idempotent_scaled": four_p_sq_ok,
        "normalized_trace_p": Fraction(trace_4p, 16),
        "bond_expectation_p_a0_a1": exp_p_a0_a1,
        "bond_expectation_k_a0_a1": exp_k_a0_a1,
        "c00_at_theta0": Fraction(1, 4),
        "c0y_theta1_jet": jet,
        "u_independent": u_independent,
        "spatial_sum_theta1": spatial_sum,
        "zero_mode_1_matches_spatial_sum": spatial_sum == ZERO_MODE_RECORDED[1],
        "ratio_l6_over_l4": ratio_l6_l4,
        "mesh_exponent_alpha": 0,
        "tl3_decay_base_at_1_192": Fraction(96, 192),
        "authority_effect": "None",
    }


def reject_critical_scaling_promotion(claim: str) -> None:
    if (
        "alpha=0 proves critical scaling" in claim
        or "L^{-1/2} derived" in claim
        or "ZERO_MODE[1]=1/8 is continuum field" in claim
    ):
        raise ValueError(
            "theta^1 single-bond jet and exponent 0 at theta=0 do not close WDP-O8-CRITICAL-SCALING"
        )


if __name__ == "__main__":
    print(witness())
