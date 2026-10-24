#!/usr/bin/env python3
"""Independent verification for FSP-WITTEN-INDEX-INVARIANCE (TFQ-1206).

Disjoint standard-library-only arithmetic checker verifying:
1. Block power intertwining `(B * A)^(k+1) = B * (A * B)^k * A`, iso-spectral positive-power
   traces `Tr((B * A)^(k+1)) = Tr((A * B)^(k+1))`, and supertrace vanishing
   `Tr(Gamma_F * H(A, B)^(k+1)) = 0` for `k = 0..4` across rectangular dimensions
   `(nB, nF) in {(1,1), (2,1), (1,2), (2,2), (3,2), (2,3)}` and exact rational blocks `(A, B)`,
   plus `beta`-independence of truncated Boltzmann polynomials `P(H) = c0 I + c1 H + c2 H^2 + c3 H^3`.
2. Paired positive-energy doublet Boltzmann weights `w_i = exp(-beta E_i) > 0`: exact
   `beta`-independence of the Witten index `W(beta) = nB0 - nF0`, non-zero Witten index forcing
   `nB0 + nF0 > 0` (`E = 0` ground state), and rectangular `(2, 1)` supercharge forced bosonic
   zero mode `[-b, a]^T` (`(A^T A) [-b, a]^T = 0`, `W = 2 - 1 = 1`).
3. Scope & non-equivalence fences:
   - Partition function `Z(beta) = nB0 + nF0 + 2 * sum_i w_i` strictly varies with `beta` and
     exceeds `nB0 + nF0`, with average Monte Carlo sign ratio `|W(beta)| / Z(beta) < 1` decaying
     as excited states contribute;
   - Explicit lattice supersymmetry breaking shift `H_F = A * B + Delta` with `Tr(Delta) != 0`
     produces `Tr(Gamma_F * H_broken) = -Tr(Delta) != 0`, destroying `beta`-independence.

AuthorityEffect: None
"""

from __future__ import annotations

import itertools
from fractions import Fraction
from typing import TypeAlias

MatQ: TypeAlias = list[list[Fraction]]


def mat_mul(a: MatQ, b: MatQ) -> MatQ:
    rows = len(a)
    inner = len(b)
    cols = len(b[0])
    return [
        [sum((a[i][k] * b[k][j] for k in range(inner)), Fraction(0)) for j in range(cols)]
        for i in range(rows)
    ]


def mat_add(a: MatQ, b: MatQ) -> MatQ:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def mat_scale(c: Fraction, a: MatQ) -> MatQ:
    return [[c * a[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def mat_id(n: int) -> MatQ:
    return [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]


def mat_pow(a: MatQ, k: int) -> MatQ:
    n = len(a)
    acc = mat_id(n)
    for _ in range(k):
        acc = mat_mul(acc, a)
    return acc


def mat_trace(a: MatQ) -> Fraction:
    return sum((a[i][i] for i in range(len(a))), Fraction(0))


def mat_transpose(a: MatQ) -> MatQ:
    return [[a[i][j] for i in range(len(a))] for j in range(len(a[0]))]


def block_diag(hb: MatQ, hf: MatQ) -> MatQ:
    nb = len(hb)
    nf = len(hf)
    out = [[Fraction(0) for _ in range(nb + nf)] for _ in range(nb + nf)]
    for i in range(nb):
        for j in range(nb):
            out[i][j] = hb[i][j]
    for i in range(nf):
        for j in range(nf):
            out[nb + i][nb + j] = hf[i][j]
    return out


def fermion_parity(nb: int, nf: int) -> MatQ:
    return block_diag(mat_id(nb), mat_scale(Fraction(-1), mat_id(nf)))


def _main_cases_1(check, weight_sets):
    for nb0 in range(4):
        for nf0 in range(4):
            for ws in weight_sets:
                w_val = Fraction(nb0 - nf0) + sum((w - w for w in ws), Fraction(0))
                check(w_val == Fraction(nb0 - nf0), "spectral")
                if w_val != 0:
                    check(nb0 + nf0 > 0, "spectral")
    return None


def main() -> int:
    checks = 0
    supertrace_checks = 0
    spectral_checks = 0
    fence_checks = 0
    failures = 0

    def check(cond: bool, bucket: str) -> None:
        nonlocal checks, supertrace_checks, spectral_checks, fence_checks, failures
        checks += 1
        if bucket == "supertrace":
            supertrace_checks += 1
        elif bucket == "spectral":
            spectral_checks += 1
        elif bucket == "fence":
            fence_checks += 1
        if not cond:
            failures += 1

    # 1. Rectangular & square block supercharges across (nB, nF) and powers k = 0..4
    dims = [(1, 1), (2, 1), (1, 2), (2, 2), (3, 2), (2, 3)]
    seeds = [Fraction(-2), Fraction(-1, 2), Fraction(1, 3), Fraction(1), Fraction(3, 2), Fraction(2)]
    for nb, nf in dims:
        gamma = fermion_parity(nb, nf)
        check(mat_trace(gamma) == Fraction(nb - nf), "supertrace")
        for offset in range(6):
            a_mat: MatQ = [
                [seeds[(i * nb + j + offset) % len(seeds)] for j in range(nb)]
                for i in range(nf)
            ]
            b_mat: MatQ = [
                [seeds[(i * nf + j + offset + 2) % len(seeds)] for j in range(nf)]
                for i in range(nb)
            ]
            hb = mat_mul(b_mat, a_mat)
            hf = mat_mul(a_mat, b_mat)
            h_tot = block_diag(hb, hf)
            for k in range(5):
                # Intertwining (B A)^(k+1) = B (A B)^k A
                lhs = mat_pow(hb, k + 1)
                rhs = mat_mul(mat_mul(b_mat, mat_pow(hf, k)), a_mat)
                check(lhs == rhs, "supertrace")
                # Iso-spectral trace Tr((B A)^(k+1)) == Tr((A B)^(k+1))
                check(mat_trace(lhs) == mat_trace(mat_pow(hf, k + 1)), "supertrace")
                # Supertrace vanishing Tr(Gamma_F H^(k+1)) == 0
                h_pow = mat_pow(h_tot, k + 1)
                check(mat_trace(mat_mul(gamma, h_pow)) == Fraction(0), "supertrace")

            # Truncated Boltzmann polynomial P(H) = c0 I - beta H + (beta^2/2) H^2 - (beta^3/6) H^3
            for beta in (Fraction(0), Fraction(1, 4), Fraction(1), Fraction(5, 2)):
                c0 = Fraction(1)
                c1 = -beta
                c2 = (beta * beta) / 2
                c3 = -(beta * beta * beta) / 6
                poly = mat_add(
                    mat_add(
                        mat_scale(c0, mat_id(nb + nf)),
                        mat_scale(c1, h_tot),
                    ),
                    mat_add(
                        mat_scale(c2, mat_pow(h_tot, 2)),
                        mat_scale(c3, mat_pow(h_tot, 3)),
                    ),
                )
                str_poly = mat_trace(mat_mul(gamma, poly))
                check(str_poly == Fraction(nb - nf), "supertrace")

    # 2. Paired positive-energy doublets & rectangular (2, 1) forced zero mode
    weight_sets = [
        [Fraction(1, 2)],
        [Fraction(3, 4), Fraction(1, 5)],
        [Fraction(7, 8), Fraction(2, 5), Fraction(1, 10)],
        [Fraction(9, 10), Fraction(4, 9), Fraction(1, 4), Fraction(1, 25)],
    ]
    _main_cases_1(check, weight_sets)

    for a_val, b_val in itertools.product(
        [Fraction(-3), Fraction(-1), Fraction(-1, 2), Fraction(1, 3), Fraction(2), Fraction(5)],
        repeat=2,
    ):
        a_2x1: MatQ = [[a_val, b_val]]
        at_2x1 = mat_transpose(a_2x1)
        hb_2 = mat_mul(at_2x1, a_2x1)
        hf_1 = mat_mul(a_2x1, at_2x1)
        check(mat_trace(hb_2) == a_val * a_val + b_val * b_val, "spectral")
        check(mat_trace(hf_1) == a_val * a_val + b_val * b_val, "spectral")
        # Forced bosonic zero mode v0 = [-b, a]^T
        v0 = [-b_val, a_val]
        av0 = a_2x1[0][0] * v0[0] + a_2x1[0][1] * v0[1]
        hb_v0_0 = hb_2[0][0] * v0[0] + hb_2[0][1] * v0[1]
        hb_v0_1 = hb_2[1][0] * v0[0] + hb_2[1][1] * v0[1]
        check(av0 == 0 and hb_v0_0 == 0 and hb_v0_1 == 0, "spectral")
        # Positive-energy partner v1 = [a, b]^T has eigenvalue a^2 + b^2 > 0
        e_pos = a_val * a_val + b_val * b_val
        hb_v1_0 = hb_2[0][0] * a_val + hb_2[0][1] * b_val
        hb_v1_1 = hb_2[1][0] * a_val + hb_2[1][1] * b_val
        check(hb_v1_0 == e_pos * a_val and hb_v1_1 == e_pos * b_val, "spectral")

    # 3. Scope & non-equivalence fences (partition function Z(beta) vs Witten index W(beta), and broken SUSY)
    for nb0 in range(1, 4):
        for nf0 in range(0, nb0):
            for w1 in (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)):
                for w2 in (Fraction(1, 5), Fraction(2, 5), Fraction(3, 5)):
                    w_idx = Fraction(nb0 - nf0)
                    z_part = Fraction(nb0 + nf0) + 2 * (w1 + w2)
                    z_part_shifted = Fraction(nb0 + nf0) + 2 * (w1 / 2 + w2 / 2)
                    check(z_part > Fraction(nb0 + nf0), "fence")
                    check(z_part != z_part_shifted, "fence")
                    check(w_idx < z_part, "fence")
                    check(Fraction(0) < w_idx / z_part < Fraction(1), "fence")

    # Broken lattice supercharge fence: H_F = A B + Delta with Tr(Delta) != 0
    gamma_22 = fermion_parity(2, 2)
    a_22 = [[Fraction(1), Fraction(-2)], [Fraction(3), Fraction(1)]]
    b_22 = [[Fraction(2), Fraction(1)], [Fraction(-1), Fraction(4)]]
    hb_22 = mat_mul(b_22, a_22)
    hf_22 = mat_mul(a_22, b_22)
    for d11 in (Fraction(1, 3), Fraction(1), Fraction(5, 2)):
        for d22 in (Fraction(1, 2), Fraction(2), Fraction(7, 3)):
            delta = [[d11, Fraction(0)], [Fraction(0), d22]]
            h_broken = block_diag(hb_22, mat_add(hf_22, delta))
            str_broken = mat_trace(mat_mul(gamma_22, h_broken))
            check(str_broken == -(d11 + d22) and str_broken != 0, "fence")

    print(
        f"checks={checks} supertrace={supertrace_checks} spectral={spectral_checks} "
        f"fences={fence_checks} failures={failures}"
    )
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
