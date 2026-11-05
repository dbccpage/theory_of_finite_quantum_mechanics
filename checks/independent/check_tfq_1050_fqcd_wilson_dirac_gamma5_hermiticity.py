#!/usr/bin/env python3
"""Standalone independent verification script for Record TFQ-1050 (FQCD-WILSON-DIRAC-GAMMA5-HERMITICITY).

AuthorityEffect: None
Imports checker infrastructure only; no production implementation.
"""

from __future__ import annotations

from fractions import Fraction
import json
from collections.abc import Callable
from itertools import product

# Shared checker infrastructure only; no production implementation is imported.
from pathlib import Path as _Path
import sys as _sys
_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from checker_support.boundary import cli
from checker_support.cases import Cases
from checker_support.wilson_operator import assembled_operator_checks, direct_wilson_determinant


CheckRecorder = Callable[[str, bool], None]


def check_chiral_links(add_check: CheckRecorder) -> None:
    for d in (2, 4):
        spin_dim = 2 ** (d // 2)
        half = spin_dim // 2
        g5_diag = [1 if i < half else -1 for i in range(spin_dim)]
        add_check(f"d{d}_gamma5_involution_sq_is_1", all(s * s == 1 for s in g5_diag))
        add_check(f"d{d}_gamma5_traceless", sum(g5_diag) == 0)
        add_check(
            f"d{d}_chiral_offdiag_product_is_minus_1",
            all(g5_diag[a] * g5_diag[b] == -1 for a in range(half) for b in range(half, spin_dim)),
        )

    # 2. Entrywise identity on the supplied finite grid of exact unitary links.
    def wilson_link_fwd(
        r: Fraction, d_spin: Fraction, g_re: Fraction, g_im: Fraction, u_re: Fraction, u_im: Fraction
    ) -> tuple[Fraction, Fraction]:
        a_re = Fraction(1, 2) * g_re - Fraction(1, 2) * r * d_spin
        a_im = Fraction(1, 2) * g_im
        return (a_re * u_re - a_im * u_im, a_re * u_im + a_im * u_re)

    def wilson_link_bwd(
        r: Fraction, d_spin: Fraction, g_re: Fraction, g_im: Fraction, u_re: Fraction, u_im: Fraction
    ) -> tuple[Fraction, Fraction]:
        b_re = -Fraction(1, 2) * g_re - Fraction(1, 2) * r * d_spin
        b_im = Fraction(1, 2) * g_im
        return (b_re * u_re - b_im * (-u_im), b_re * (-u_im) + b_im * u_re)

    pythagorean_links = [
        (Fraction(1, 1), Fraction(0, 1)),
        (Fraction(0, 1), Fraction(1, 1)),
        (Fraction(3, 5), Fraction(4, 5)),
        (Fraction(5, 13), Fraction(-12, 13)),
        (Fraction(-8, 17), Fraction(15, 17)),
        (Fraction(7, 25), Fraction(-24, 25)),
    ]
    gamma_entries = [
        (Fraction(1, 1), Fraction(0, 1)),
        (Fraction(0, 1), Fraction(-1, 1)),
        (Fraction(3, 5), Fraction(-4, 5)),
    ]
    for idx, (u_re, u_im) in enumerate(pythagorean_links):
        add_check(f"unitary_link_norm_{idx}", u_re * u_re + u_im * u_im == Fraction(1, 1))
        for (g_idx, (g_re, g_im)), r_val in product(enumerate(gamma_entries), (Fraction(1, 2), Fraction(1, 1), Fraction(2, 1))):
            f_re, f_im = wilson_link_fwd(r_val, Fraction(0, 1), g_re, g_im, u_re, u_im)
            b_re, b_im = wilson_link_bwd(r_val, Fraction(0, 1), g_re, g_im, u_re, u_im)
            add_check(
                f"offdiag_gamma5_hermiticity_u{idx}_g{g_idx}_r{r_val.numerator}_over_{r_val.denominator}",
                (-f_re == b_re) and (-f_im == -b_im),
            )
        for r_val in (Fraction(1, 2), Fraction(1, 1), Fraction(2, 1)):
            fd_re, fd_im = wilson_link_fwd(r_val, Fraction(1, 1), Fraction(0, 1), Fraction(0, 1), u_re, u_im)
            bd_re, bd_im = wilson_link_bwd(r_val, Fraction(1, 1), Fraction(0, 1), Fraction(0, 1), u_re, u_im)
            add_check(
                f"diag_wilson_laplacian_hermiticity_u{idx}_r{r_val.numerator}_over_{r_val.denominator}",
                (fd_re == bd_re) and (fd_im == -bd_im),
            )

    # Fixed independent values also detect a wrong coefficient of r. The old
    # sign-square identity alone held for every value, including a wrong one.
    expected_diagonals = {
        (-3, Fraction(1, 2)): (-2, -1), (-3, Fraction(1)): (-1, 1),
        (-1, Fraction(1, 2)): (0, 1), (-1, Fraction(1)): (1, 3),
        (0, Fraction(1, 2)): (1, 2), (0, Fraction(1)): (2, 4),
        (1, Fraction(1, 2)): (2, 3), (1, Fraction(1)): (3, 5),
    }
    for (mass, r_val), expected in expected_diagonals.items():
        m_val = Fraction(mass)
        d2_diag = m_val + 2 * r_val
        d4_diag = m_val + 4 * r_val
        add_check(
            f"onsite_diag_d2_d4_m{m_val.numerator}_r{r_val.numerator}_over_{r_val.denominator}",
            d2_diag == Fraction(expected[0]) and d4_diag == Fraction(expected[1]),
        )


def check_determinant_examples(add_check: CheckRecorder) -> None:
    def det_dw_2x2(m: Fraction, r: Fraction = Fraction(1, 1)) -> Fraction:
        s = m + 2 * r
        return s**2 * (s**2 - 2*r**2) * (s**2 + 2) * (s**2 + 2 - 2*r**2)

    add_check("det_dw_2x2_m_minus_1_negative", det_dw_2x2(Fraction(-1, 1)) == Fraction(-3, 1) < Fraction(0, 1))
    add_check("det_dw_2x2_two_flavor_m_minus_1_positive", det_dw_2x2(Fraction(-1, 1)) ** 2 == Fraction(9, 1) > Fraction(0, 1))
    add_check("det_dw_2x2_m_0_positive", det_dw_2x2(Fraction(0, 1)) == Fraction(192, 1) > Fraction(0, 1))
    add_check("det_dw_2x2_m_1_positive", det_dw_2x2(Fraction(1, 1)) == Fraction(6237, 1) > Fraction(0, 1))

    for r, m in product((Fraction(0), Fraction(1, 2), Fraction(1), Fraction(3, 2)), (Fraction(-1), Fraction(0), Fraction(1, 3))):
        add_check(f"direct_matrix_determinant_m{m}_r{r}", direct_wilson_determinant(m,r) == det_dw_2x2(m,r))
    add_check("nonunit_determinant_counterexample", direct_wilson_determinant(Fraction(0),Fraction(1,2)) == Fraction(15,4))
    add_check("assembled_four_spin_colored_operator", assembled_operator_checks())


def check() -> dict[str, object]:
    """Run independent exact rational checks for FQCD-WILSON-DIRAC-GAMMA5-HERMITICITY (TFQ-1050)."""
    checks = Cases()

    def add_check(name: str, ok: bool) -> None:
        checks.append((name, ok))

    # 1. Chiral-sign identities in d = 2 and d = 4 (not a 2D Clifford construction).
    # In chiral basis, gamma_5 = diag(I, -I), so gamma_5(alpha) in {+1, -1} and gamma_5^2 = I.
    # Every Hermitian Euclidean gamma_mu = [[0, sigma_mu], [sigma_mu^dagger, 0]] is block off-diagonal
    # between the +1 and -1 chiral sectors, so gamma_5(alpha) * gamma_5(beta) == -1 whenever (gamma_mu)_{alpha,beta} != 0.
    check_chiral_links(add_check)

    # 4. Explicit 8x8 Wilson-Dirac operator on 2x2 periodic lattice with non-trivial gauge links
    check_determinant_examples(add_check)

    failures = [name for name, ok in checks if not ok]
    return {
        "record_id": "TFQ-1050",
        "dag_node": "FQCD-WILSON-DIRAC-GAMMA5-HERMITICITY",
        "authority_effect": "None",
        "total_checks": len(checks),
        "failed_checks": len(failures),
        "failures": failures,
        "all_passed": len(failures) == 0,
    }


def main() -> int:
    receipt = check()
    print(json.dumps(receipt, indent=2))
    if not receipt["all_passed"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(cli(main))
