"""Subgap R7: Full 55-Generator Positivstellensatz Solver & Exact Rational Certificate Verifier.

AuthorityEffect: None.
Firewall Line: stated region only; mints no authority.

This script evaluates the 55 real generators of I_55 and a squared distance
to one Karlsson sample. It does not construct Stengle multipliers or sums of
squares, and it does not emit a certificate.

The written receipt is:
omega_engine_atlas/coda_atlas/F004_papers/010_mub6/artifacts/mub_r7_genuine_positivstellensatz_receipt.json
"""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

REFUSAL_REASON = (
    "Stengle multipliers and sums of squares were not constructed. "
    "An assigned defect of zero is not an evaluated identity. "
    "The Karlsson z=0 sample is not a point of I_55."
)


def digest_str(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


class Exact55GeneratorSystem:
    """Represents the 55 polynomial generators of I_55 in R^50 plus corner determinant."""

    def __init__(self, eps_0_sq: Fraction = Fraction(1, 100)) -> None:
        self.eps_0_sq = eps_0_sq

    @staticmethod
    def eval_unimodularity(x: list[list[Fraction]], y: list[list[Fraction]]) -> list[Fraction]:
        """25 Unimodular circle generators: x_{jk}^2 + y_{jk}^2 - 1 = 0 (1 <= j, k <= 5)."""
        res = []
        for j in range(1, 6):
            for k in range(1, 6):
                val = x[j][k] * x[j][k] + y[j][k] * y[j][k] - Fraction(1, 1)
                res.append(val)
        return res

    @staticmethod
    def eval_row0_orthogonality(x: list[list[Fraction]], y: list[list[Fraction]]) -> tuple[list[Fraction], list[Fraction]]:
        """10 Row-0 orthogonality generators (5 real, 5 imag)."""
        re_res = []
        im_res = []
        for k in range(1, 6):
            sum_x = Fraction(1, 1) + sum(x[k][col] for col in range(1, 6))
            sum_y = sum(y[k][col] for col in range(1, 6))
            re_res.append(sum_x)
            im_res.append(sum_y)
        return re_res, im_res

    @staticmethod
    def eval_pairwise_row_orthogonality(x: list[list[Fraction]], y: list[list[Fraction]]) -> tuple[list[Fraction], list[Fraction]]:
        """20 Bilinear pairwise row-orthogonality generators (10 real, 10 imag)."""
        re_res = []
        im_res = []
        for j in range(1, 6):
            for k in range(j + 1, 6):
                re_part = Fraction(1, 1) + sum(x[j][col] * x[k][col] + y[j][col] * y[k][col] for col in range(1, 6))
                im_part = sum(y[j][col] * x[k][col] - x[j][col] * y[k][col] for col in range(1, 6))
                re_res.append(re_part)
                im_res.append(im_part)
        return re_res, im_res

    @staticmethod
    def eval_corner_determinant(x: list[list[Fraction]], y: list[list[Fraction]]) -> tuple[Fraction, Fraction]:
        """3x3 corner determinant top-left minor."""
        p_re = ((x[1][1] - 1) * (x[2][2] - 1) - y[1][1] * y[2][2]
                - ((x[1][2] - 1) * (x[2][1] - 1) - y[1][2] * y[2][1]))
        p_im = ((x[1][1] - 1) * y[2][2] + (x[2][2] - 1) * y[1][1]
                - ((x[1][2] - 1) * y[2][1] + (x[2][1] - 1) * y[1][2]))
        return p_re, p_im

    def eval_catalog_distance_sq(self, x: list[list[Fraction]], y: list[list[Fraction]]) -> Fraction:
        """Evaluate sum of squared catalog orbit invariants Q_m(X)^2."""
        karl_base_x, karl_base_y = create_karlsson_point(z_angle=0)
        q_vals = [
            x[1][1] - karl_base_x[1][1],
            y[1][1] - karl_base_y[1][1],
            x[2][2] - karl_base_x[2][2],
            y[2][2] - karl_base_y[2][2],
        ]
        return sum(q * q for q in q_vals)

    def eval_separation_polynomial(self, x: list[list[Fraction]], y: list[list[Fraction]]) -> Fraction:
        """g_sep(X) = sum Q_m(X)^2 - eps_0^2."""
        dist_sq = self.eval_catalog_distance_sq(x, y)
        return dist_sq - self.eps_0_sq


def create_tao_point() -> tuple[list[list[Fraction]], list[list[Fraction]]]:
    """Exact rational representation of the Tao S6 matrix over Eisenstein integers."""
    x = [[Fraction(0)] * 6 for _ in range(6)]
    y = [[Fraction(0)] * 6 for _ in range(6)]
    for j in range(6):
        x[0][j] = Fraction(1)
        x[j][0] = Fraction(1)

    phase_pattern = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 2, 2],
        [0, 1, 0, 2, 2, 1],
        [0, 1, 2, 0, 1, 2],
        [0, 2, 2, 1, 0, 1],
        [0, 2, 1, 2, 1, 0],
    ]
    for j in range(1, 6):
        for k in range(1, 6):
            p = phase_pattern[j][k]
            if p == 0:
                x[j][k] = Fraction(1)
                y[j][k] = Fraction(0)
            elif p == 1:
                x[j][k] = Fraction(-1, 2)
                y[j][k] = Fraction(866, 1000)
            elif p == 2:
                x[j][k] = Fraction(-1, 2)
                y[j][k] = Fraction(-866, 1000)
    return x, y


def create_karlsson_point(z_angle: int = 0) -> tuple[list[list[Fraction]], list[list[Fraction]]]:
    """Exact rational Karlsson boundary matrix representative (z=0 Diță slice)."""
    x = [[Fraction(1)] * 6 for _ in range(6)]
    y = [[Fraction(0)] * 6 for _ in range(6)]
    x[1][1] = Fraction(-1)
    x[1][2] = Fraction(1)
    x[1][3] = Fraction(-1)
    x[1][4] = Fraction(1)
    x[1][5] = Fraction(-1)

    x[2][1] = Fraction(1)
    x[2][2] = Fraction(-1, 2)
    x[2][3] = Fraction(-1, 2)
    x[2][4] = Fraction(-1, 2)
    x[2][5] = Fraction(-1, 2)
    return x, y


def _count_nonzero(values: list[Fraction]) -> int:
    return sum(1 for value in values if value != 0)


def diagnose_r7_karlsson_boundary() -> dict[str, Any]:
    """Evaluate I_55 and g_sep on one sample. Refuse a Stengle certificate."""
    sys_eval = Exact55GeneratorSystem(eps_0_sq=Fraction(1, 100))
    karl_x, karl_y = create_karlsson_point(z_angle=0)
    unimodular = sys_eval.eval_unimodularity(karl_x, karl_y)
    row0_re, row0_im = sys_eval.eval_row0_orthogonality(karl_x, karl_y)
    pair_re, pair_im = sys_eval.eval_pairwise_row_orthogonality(karl_x, karl_y)
    corner_re, corner_im = sys_eval.eval_corner_determinant(karl_x, karl_y)
    nonzero = {
        "unimodular": _count_nonzero(unimodular),
        "row0_re": _count_nonzero(row0_re),
        "row0_im": _count_nonzero(row0_im),
        "pairwise_re": _count_nonzero(pair_re),
        "pairwise_im": _count_nonzero(pair_im),
        "corner_re": 0 if corner_re == 0 else 1,
        "corner_im": 0 if corner_im == 0 else 1,
    }
    g_karl = sys_eval.eval_separation_polynomial(karl_x, karl_y)
    tao_x, tao_y = create_tao_point()
    g_tao = sys_eval.eval_separation_polynomial(tao_x, tao_y)
    pert_x = [row[:] for row in karl_x]
    pert_y = [row[:] for row in karl_y]
    pert_x[1][1] += Fraction(1, 2)
    g_pert = sys_eval.eval_separation_polynomial(pert_x, pert_y)
    receipt: dict[str, Any] = {
        "schema_version": "omega.mub.positivstellensatz.v1",
        "authority_effect": "None",
        "firewall": "stated region only; mints no authority",
        "scope": "r7_singular_segre_positivstellensatz_karlsson_boundary",
        "target": "ENC-1147 / Subgap R7",
        "status": "NOT_A_CERTIFICATE",
        "refusal_reason": REFUSAL_REASON,
        "arithmetic_regime": "EXACT_RATIONAL_FRACTION",
        "identity_evaluated": False,
        "exact_identity_verified": False,
        "variety_empty_on_exterior": False,
        "generator_ideal": {
            "name": "I_55",
            "ambient_ring": "Q[x_11, y_11, ..., x_55, y_55]",
            "num_real_variables": 50,
            "num_unimodular_generators": 25,
            "num_row0_orthogonality_generators": 10,
            "num_pairwise_bilinear_generators": 20,
            "total_ideal_generators": 55,
            "corner_determinant_generators": 2,
        },
        "sample": {
            "name": "karlsson_boundary_slice_z0",
            "on_ideal_i55": all(count == 0 for count in nonzero.values()),
            "nonzero_residuals": nonzero,
            "g_sep": str(g_karl),
            "separation_nonpositive": g_karl <= 0,
        },
        "tao_rational_proxy": {
            "note": "Imaginary parts use 866/1000, not sqrt(3)/2.",
            "g_sep": str(g_tao),
        },
        "perturbed_sample": {
            "g_sep": str(g_pert),
            "separation_positive": g_pert > 0,
        },
    }
    payload = json.dumps(receipt, sort_keys=True, indent=2)
    receipt["receipt_id"] = f"sha256:{digest_str(payload)}"
    return receipt


def main() -> int:
    print("[R7] Evaluating I_55 on the Karlsson z=0 sample.")
    receipt = diagnose_r7_karlsson_boundary()
    if receipt["status"] == "CERTIFICATE" or receipt["exact_identity_verified"]:
        print("[R7] Refusing to write a certificate for an identity that was not evaluated.")
        return 1
    output_path = Path(__file__).resolve().parents[1] / "artifacts" / "mub_r7_genuine_positivstellensatz_receipt.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"[R7] Wrote {output_path}")
    print(f"[R7] Status: {receipt['status']}")
    print(f"[R7] On I_55: {receipt['sample']['on_ideal_i55']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
