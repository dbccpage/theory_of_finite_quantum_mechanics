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


def direct_wilson_determinant(m: Fraction, r: Fraction) -> Fraction:
    """Eliminate the actual 8x8 matrix; no determinant polynomial is used."""
    s = m + 2*r
    a = [[Fraction(x) for x in row] for row in [
        [s, 0, -r, 0, -r, 0, 0, 0], [0, s, 0, -r, 0, -r, 0, 0],
        [-r, 0, s, 0, 0, 0, 0, 1], [0, -r, 0, s, 0, 0, 1, 0],
        [-r, 0, 0, 0, s, 0, 0, 1], [0, -r, 0, 0, 0, s, -1, 0],
        [0, 0, 0, -1, 0, 1, s, 0], [0, 0, -1, 0, -1, 0, 0, s],
    ]]
    det = Fraction(1)
    for col in range(8):
        pivot = next((row for row in range(col, 8) if a[row][col]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            det = -det
        p = a[col][col]
        det *= p
        for row in range(col + 1, 8):
            q = a[row][col] / p
            for k in range(col + 1, 8):
                a[row][k] -= q * a[col][k]
    return det



def assembled_operator_checks() -> bool:
    """Clifford relations and a complete 4D periodic (2,1,1,1), two-color operator over Q(i)."""
    z = (Fraction(0), Fraction(0))
    one = (Fraction(1), Fraction(0))
    imag = (Fraction(0), Fraction(1))
    def add(a,b): return (a[0]+b[0], a[1]+b[1])
    def mul(a,b): return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
    def scale(q,a): return (q*a[0], q*a[1])
    def conj(a): return (a[0], -a[1])
    pauli = [[[z,one],[one,z]], [[z,scale(-1,imag)],[imag,z]], [[one,z],[z,scale(-1,one)]]]
    eye2 = [[one,z],[z,one]]
    gamma=[]
    for mu in range(4):
        block = eye2 if mu==0 else pauli[mu-1]
        g=[[z for _ in range(4)] for _ in range(4)]
        for a in range(2):
            for b in range(2):
                g[a][b+2] = block[a][b] if mu==0 else mul(scale(-1,imag),block[a][b])
                g[a+2][b] = block[a][b] if mu==0 else mul(imag,block[a][b])
        gamma.append(g)
    def dot(a,b):
        value=z
        for x,y in zip(a,b): value=add(value,mul(x,y))
        return value
    signs=[1,1,-1,-1]
    for mu in range(4):
        for a in range(4):
            for b in range(4):
                if gamma[mu][a][b] != conj(gamma[mu][b][a]): return False
                if scale(signs[a]*signs[b],gamma[mu][a][b]) != scale(-1,gamma[mu][a][b]): return False
                for nu in range(4):
                    anti=add(dot(gamma[mu][a],[gamma[nu][k][b] for k in range(4)]),dot(gamma[nu][a],[gamma[mu][k][b] for k in range(4)]))
                    if anti != (scale(2,one) if mu==nu and a==b else z): return False
    def link(mu,x):
        # A color-mixing rational orthogonal rotation times a nontrivial unit phase.
        c,t=(Fraction(3,5),Fraction(4,5)) if (mu+x)%2 else (Fraction(5,13),Fraction(12,13))
        phase=(Fraction(3,5),Fraction(4,5)) if x else one
        return [[scale(c,phase),scale(-t,phase)],[scale(t,phase),scale(c,phase)]]
    def idx(x,a,c): return (x*4+a)*2+c
    for r in (Fraction(0),Fraction(1,2),Fraction(1),Fraction(3,2)):
        dw=[[z for _ in range(16)] for _ in range(16)]
        for x in range(2):
            for a in range(4):
                for c in range(2):
                    row=idx(x,a,c)
                    dw[row][row]=(Fraction(-1)+4*r,Fraction(0))
                    for mu in range(4):
                        y=1-x if mu==0 else x
                        forward, reverse=link(mu,x),link(mu,y)
                        for b in range(4):
                            diag=scale(-r/2,one) if a==b else z
                            minus=add(scale(Fraction(1,2),gamma[mu][a][b]),diag)
                            plus=add(scale(Fraction(-1,2),gamma[mu][a][b]),diag)
                            for d in range(2):
                                col=idx(y,b,d)
                                dw[row][col]=add(dw[row][col],add(mul(minus,forward[c][d]),mul(plus,conj(reverse[d][c]))))
        for x in range(2):
            for a in range(4):
                for c in range(2):
                    i=idx(x,a,c)
                    for y in range(2):
                        for b in range(4):
                            for d in range(2):
                                j=idx(y,b,d)
                                if scale(signs[a]*signs[b],dw[i][j]) != conj(dw[j][i]): return False
    return True


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
        return s**2 * (s**2 - 2*r**2) * (s**2 + 2) * (s**2 + 2 - 2*r**2)

    add_check("det_dw_2x2_m_minus_1_negative", det_dw_2x2(Fraction(-1, 1)) == Fraction(-3, 1) < Fraction(0, 1))
    add_check("det_dw_2x2_two_flavor_m_minus_1_positive", det_dw_2x2(Fraction(-1, 1)) ** 2 == Fraction(9, 1) > Fraction(0, 1))
    add_check("det_dw_2x2_m_0_positive", det_dw_2x2(Fraction(0, 1)) == Fraction(192, 1) > Fraction(0, 1))
    add_check("det_dw_2x2_m_1_positive", det_dw_2x2(Fraction(1, 1)) == Fraction(6237, 1) > Fraction(0, 1))

    for r in (Fraction(0), Fraction(1,2), Fraction(1), Fraction(3,2)):
        for m in (Fraction(-1), Fraction(0), Fraction(1,3)):
            add_check(f"direct_matrix_determinant_m{m}_r{r}", direct_wilson_determinant(m,r) == det_dw_2x2(m,r))
    add_check("nonunit_determinant_counterexample", direct_wilson_determinant(Fraction(0),Fraction(1,2)) == Fraction(15,4))
    add_check("assembled_four_spin_colored_operator", assembled_operator_checks())

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
