"""Exact rational witness for WDP-O12-XLM-COMPARISON (`derivation.md`).

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any


def mixed_partial_log_x_at_zero(_j: int, a: int, _k: int, b: int) -> Fraction:
    return Fraction(1, 16) if a == b else Fraction(0)


def rescaled_row_sum(j: int, k: int, m: int = 1) -> Fraction:
    scale = (2 * m) ** 2
    return sum((scale * mixed_partial_log_x_at_zero(j, 0, k, y) for y in range(4)), Fraction(0))


def witness() -> dict[str, Any]:
    r_jk = tuple(
        tuple(rescaled_row_sum(j, k, 1) for k in range(2))
        for j in range(2)
    )
    unrescaled = sum((mixed_partial_log_x_at_zero(0, 0, 0, y) for y in range(4)), Fraction(0))
    time_summed = r_jk[0][0] + r_jk[0][1]
    k0 = Fraction(1, 4)

    return {
        "x_4_1_at_zero": 16,
        "unrescaled_row_sum": unrescaled,
        "rescaled_row_sums_all_jk": r_jk,
        "time_summed_rescaled_row": time_summed,
        "k_4_0": k0,
        "k_0": k0,
        "gap_r_minus_k0": r_jk[0][0] - k0,
        "authority_effect": "None",
    }


def reject_xlm_positive_theta_promotion(claim: str) -> None:
    if (
        "r > 0" in claim
        or "theta > 0" in claim
        or "1/16 == k_0" in claim
        or "1/2 == k_0" in claim
    ):
        raise ValueError(
            "r=0, M=1, L=4 free-cosh Hessian agreement does not prove X_{LM} comparison for r > 0 or theta > 0"
        )


if __name__ == "__main__":
    print(witness())
