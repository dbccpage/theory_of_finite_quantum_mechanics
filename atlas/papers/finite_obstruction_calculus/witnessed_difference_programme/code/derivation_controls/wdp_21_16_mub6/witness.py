"""Exact witness for the four finite carriers in derivation.md for WDP-21-16-MUB6."""

from __future__ import annotations

from fractions import Fraction

TAO_PHASE_TABLE: tuple[tuple[int, ...], ...] = (
    (0, 0, 0, 0, 0, 0),
    (0, 0, 1, 1, 2, 2),
    (0, 1, 0, 2, 2, 1),
    (0, 1, 2, 0, 1, 2),
    (0, 2, 2, 1, 0, 1),
    (0, 2, 1, 2, 1, 0),
)

GAMMA_1: tuple[int, ...] = (1, 1, 1, -1, -1, -1)

LOOKUP_ROW_COUNTS: dict[str, int] = {
    "FourierDita": 3,
    "Szollosi": 3,
    "TaoS6": 0,
    "Haagerup": 1,
    "KarlssonGeneric": 2,
}


def witness() -> dict[str, object]:
    col_sums = [
        sum(GAMMA_1[r] * TAO_PHASE_TABLE[r][c] for r in range(6))
        for c in range(6)
    ]
    residues = [s % 3 for s in col_sums]
    counts = (residues.count(0), residues.count(1), residues.count(2))
    x = counts[0] - counts[2]
    y = counts[1] - counts[2]
    eisenstein_norm_sq = x * x - x * y + y * y
    alpha_2 = [6 * m - 9 for m in range(4)]
    parity_sums = [1 + (-1 if a % 2 == 1 else 1) for a in alpha_2]
    alpha_pot = (7, -3, 11)
    coboundary_cycle_sum = (
        (alpha_pot[1] - alpha_pot[0])
        + (alpha_pot[2] - alpha_pot[1])
        + (alpha_pot[0] - alpha_pot[2])
    )
    spectral_floor = (1 - Fraction(1907, 2000)) / Fraction(6, 5)
    return {
        "tao_column_sums": tuple(col_sums),
        "tao_column_residues_mod3": tuple(residues),
        "tao_residue_counts": counts,
        "tao_eisenstein_norm_sq": eisenstein_norm_sq,
        "alpha_2_values": tuple(alpha_2),
        "parity_pair_sums": tuple(parity_sums),
        "synthetic_nerve_sum_012": 4045 + 4044 + 4044,
        "synthetic_coboundary_cycle_sum": coboundary_cycle_sum,
        "spectral_floor_frac": spectral_floor,
        "lookup_row_counts": dict(LOOKUP_ROW_COUNTS),
        "external_haagerup_minus_one_rows": 5,
    }


def reject_moduli_phi1_coverage_claim(value: int | Fraction) -> None:
    if value in (0, 9, 12133, Fraction(12133, 5000), Fraction(12133, 30000)):
        raise ValueError(
            "labelled finite carrier values 9, 0, and 12133 do not certify WDP Phi_1 coverage on CHM(6)"
        )
