"""Exact rational witness for WDP-APPW-UNIFORM-VOLUME (`derivation.md`).

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any


def lambda_1(r: Fraction) -> Fraction:
    return -(r**4) / (4 * (r + 2) * (r**2 + 4 * r + 8))


def witness() -> dict[str, Any]:
    r = Fraction(1, 192)
    factored_den = 4 * (r + 2) * (r**2 + 4 * r + 8)
    expanded_den = 64 + 64 * r + 24 * (r**2) + 4 * (r**3)
    s1 = Fraction(3, 43)
    m1 = 2 * s1 * (64**2)

    return {
        "r": r,
        "r_plus_2": r + 2,
        "r2_plus_4r_plus_8": r**2 + 4 * r + 8,
        "factored_den": factored_den,
        "expanded_den": expanded_den,
        "denominators_equal": factored_den == expanded_den,
        "lambda_1_at_1_192": lambda_1(r),
        "s1_constant": s1,
        "m1_constant": m1,
        "gate_e_eigenvalue": Fraction(-1, 706440),
        "gate_e_quadratic": Fraction(-1, 88305),
        "authority_effect": "None",
    }


def reject_uniform_volume_promotion(claim: str) -> None:
    if (
        "uniform in L for G_M" in claim
        or "O.12 discharges Appendix W" in claim
        or "-1/87426958080 bounds all volumes" in claim
    ):
        raise ValueError(
            "fixed L=4 one-period eigenvalue and O.12 Euclidean row-sum do not supply a uniform-in-L Trotter bound on G_M"
        )


if __name__ == "__main__":
    print(witness())
