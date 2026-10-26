"""Exact rational witness for WDP-JOINT-CONTINUUM (`derivation.md`).

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any


def eval_h(x: Fraction) -> Fraction:
    return (x - Fraction(1, 16)) * (x - Fraction(1, 36)) * (x - Fraction(1, 64))


def witness() -> dict[str, Any]:
    lengths = (4, 6, 8)
    nodes = tuple(Fraction(1, length * length) for length in lengths)
    weights = (Fraction(4, 15), Fraction(-81, 35), Fraction(64, 21))

    h_on_nodes = tuple(eval_h(x) for x in nodes)
    h_at_zero = eval_h(Fraction(0))

    moment_0 = sum(weights, Fraction(0))
    moment_1 = sum((w * x for w, x in zip(weights, nodes)), Fraction(0))
    moment_2 = sum((w * x * x for w, x in zip(weights, nodes)), Fraction(0))
    neville_on_h = sum((w * h for w, h in zip(weights, h_on_nodes)), Fraction(0))

    checkerboard_z = (912, 33012, 973824)
    neville_z0 = sum((w * z for w, z in zip(weights, checkerboard_z)), Fraction(0))

    return {
        "lengths": lengths,
        "nodes": nodes,
        "weights": weights,
        "weights_over_105": tuple(int(w * 105) for w in weights),
        "h_on_nodes": h_on_nodes,
        "h_at_zero": h_at_zero,
        "moment_0": moment_0,
        "moment_1": moment_1,
        "moment_2": moment_2,
        "neville_on_h": neville_on_h,
        "checkerboard_z": checkerboard_z,
        "neville_z0": neville_z0,
        "target_3_optimum": Fraction(15, 4),
        "target_4_optimum": 4,
        "target_5_class_count": 29771,
        "authority_effect": "None",
    }


def reject_continuum_or_torus_promotion(claim: str) -> None:
    if (
        "-1/36864 is remainder bound" in claim
        or "Z=912 is 16-site torus" in claim
        or "Q-continuum closed" in claim
    ):
        raise ValueError(
            "three-node polynomial fit and fixed L=4 carrier do not close WDP-JOINT-CONTINUUM or construct a 16-site torus"
        )


if __name__ == "__main__":
    print(witness())
