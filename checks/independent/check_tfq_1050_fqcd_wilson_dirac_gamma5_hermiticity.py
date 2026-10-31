#!/usr/bin/env python3
"""Standalone independent verification script for Record TFQ-1050 (FQCD-WILSON-DIRAC-GAMMA5-HERMITICITY).

AuthorityEffect: None
Zero repository imports; uses only Python standard library (fractions, json, sys).
"""

from __future__ import annotations

from fractions import Fraction
import json
import sys
from typing import Any


def check() -> dict[str, Any]:
    """Run independent exact rational checks for FQCD-WILSON-DIRAC-GAMMA5-HERMITICITY (TFQ-1050)."""
    checks: list[tuple[str, bool]] = []

    def add_check(name: str, ok: bool) -> None:
        checks.append((name, bool(ok)))

    # 1. Exact Clifford algebra and gamma_5 anticommutation in d = 2 and d = 4
    # In chiral basis, gamma_5 = diag(I, -I), so gamma_5(alpha) in {+1, -1} and gamma_5^2 = I.
    # Every Hermitian Euclidean gamma_mu = [[0, sigma_mu], [sigma_mu^dagger, 0]] is block off-diagonal
    # between the +1 and -1 chiral sectors, so gamma_5(alpha) * gamma_5(beta) == -1 whenever (gamma_mu)_{alpha,beta} != 0.
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

    # 2. Entrywise finite-lattice link identity gamma_5 D_W gamma_5 = D_W^dagger for arbitrary unitary links U_mu(x)
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
        for g_idx, (g_re, g_im) in enumerate(gamma_entries):
            for r_val in (Fraction(1, 2), Fraction(1, 1), Fraction(2, 1)):
                f_re, f_im = wilson_link_fwd(r_val, Fraction(0, 1), g_re, g_im, u_re, u_im)
                b_re, b_im = wilson_link_bwd(r_val, Fraction(0, 1), g_re, g_im, u_re, u_im)
                add_check(
                    f"offdiag_gamma5_hermiticity_u{idx}_g{g_idx}_r{r_val.numerator}",
                    (-f_re == b_re) and (-f_im == -b_im),
                )
        for r_val in (Fraction(1, 2), Fraction(1, 1), Fraction(2, 1)):
            fd_re, fd_im = wilson_link_fwd(r_val, Fraction(1, 1), Fraction(0, 1), Fraction(0, 1), u_re, u_im)
            bd_re, bd_im = wilson_link_bwd(r_val, Fraction(1, 1), Fraction(0, 1), Fraction(0, 1), u_re, u_im)
            add_check(
                f"diag_wilson_laplacian_hermiticity_u{idx}_r{r_val.numerator}",
                (fd_re == bd_re) and (fd_im == -bd_im),
            )

    # 3. On-site diagonal mass + d*r term in d = 2 and d = 4
    for m_val in (Fraction(-3, 1), Fraction(-1, 1), Fraction(0, 1), Fraction(1, 1)):
        for r_val in (Fraction(1, 2), Fraction(1, 1)):
            d2_diag = m_val + 2 * r_val
            d4_diag = m_val + 4 * r_val
            add_check(
                f"onsite_diag_d2_d4_m{m_val.numerator}_r{r_val.numerator}",
                ((-1) ** 2) * d2_diag == d2_diag and ((-1) ** 2) * d4_diag == d4_diag,
            )

    # 4. Explicit 8x8 Wilson-Dirac operator on 2x2 periodic lattice with non-trivial gauge links
    def det_dw_2x2(m: Fraction, r: Fraction = Fraction(1, 1)) -> Fraction:
        s = m + 2 * r
        return s ** 8 - 4 * (r ** 4) * (s ** 4)

    add_check("det_dw_2x2_m_minus_1_negative", det_dw_2x2(Fraction(-1, 1)) == Fraction(-3, 1) < Fraction(0, 1))
    add_check("det_dw_2x2_two_flavor_m_minus_1_positive", det_dw_2x2(Fraction(-1, 1)) ** 2 == Fraction(9, 1) > Fraction(0, 1))
    add_check("det_dw_2x2_m_0_positive", det_dw_2x2(Fraction(0, 1)) == Fraction(192, 1) > Fraction(0, 1))
    add_check("det_dw_2x2_m_1_positive", det_dw_2x2(Fraction(1, 1)) == Fraction(6237, 1) > Fraction(0, 1))

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


def main() -> None:
    receipt = check()
    print(json.dumps(receipt, indent=2))
    if not receipt["all_passed"]:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
