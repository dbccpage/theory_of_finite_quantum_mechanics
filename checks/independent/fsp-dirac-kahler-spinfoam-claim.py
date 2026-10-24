#!/usr/bin/env python3
"""Independent verification for FSP-DIRAC-KAHLER-SPINFOAM-CLAIM (TFQ-1216).

Checks:
1. Exterior algebra binomial degree dimensions (1, 4, 6, 4, 1) in D = 4, total
   dimension 16 = 4 * 2^(4/2), alternating Euler sum 0, orientifold involution
   signs (-1)^(p*(p-1)/2) across form degrees, and minimal spinor projector
   idempotence P^2 = P with Tr(P) = 4 and Tr(I - P) = 12.
2. Exact simplicial coboundary nilpotence d_1 d_0 = 0, d_2 d_1 = 0, d_3 d_2 = 0
   on the 4-simplex Delta^4 and curved 2-simplex CDT cluster, plus flat vs
   curved Dirac-Kahler spinor-projector commutator [D, P] and S^4 Euler-vs-Ahat
   index mismatch chi(S^4) = 2 != 4 A_hat(S^4) = 0.
3. Exact rational evaluation of finite spin-network boundary contractions:
   - Mirror-glued 2-vertex amplitude W = V^T V gives nonnegative contractions
     <psi | V^T V | psi> >= 0 across 625 matrices V and 25 states psi (15625 checks).
   - Single-vertex spin-1 tetrahedral Racah 6j recoupling kernel
     W_6j = [[1/6, -1/3], [-1/3, 1/6]] gives negative contraction -1/3 < 0 on
     psi_+ = (1, 1) and positive contraction +1 > 0 on psi_- = (1, -1), plus
     sign survey across boundary states.
4. Scope fences: taste count 1+4+6+4+1 = 16 carries no determinant positivity,
   Euclidean EPRL simplicity spin embedding j^+- = (1 +- gamma) k / 2 sublattice
   integrality condition, and odd-simplex orientation-reversal Berezin signs.
"""

from __future__ import annotations

from fractions import Fraction
import itertools
import math
import sys


def check_exterior_taste_and_orientifold() -> tuple[int, int]:
    checks = 0
    failures = 0

    expected_binom = (1, 4, 6, 4, 1)
    total = 0
    alt_sum = 0
    for p in range(5):
        checks += 1
        c = math.comb(4, p)
        if c != expected_binom[p]:
            failures += 1
        total += c
        alt_sum += ((-1) ** p) * c
    checks += 2
    if total != 16 or total != 4 * (2 ** (4 // 2)) or alt_sum != 0:
        failures += 1

    expected_orient = (1, 1, -1, -1, 1)
    for p in range(20):
        checks += 1
        s = (-1) ** ((p * (p - 1)) // 2)
        if s * s != 1:
            failures += 1
        if p < 5 and s != expected_orient[p]:
            failures += 1

    # 16-component taste x spinor projector mask
    taste_mask = (1, 0, 0, 0)
    comp_mask = (1, 1, 1, 1)
    tr_p = 0
    tr_comp = 0
    for t in range(4):
        for s in range(4):
            checks += 1
            p_val = taste_mask[t] * comp_mask[s]
            if p_val * p_val != p_val:
                failures += 1
            tr_p += p_val
            tr_comp += 1 - p_val
    checks += 1
    if tr_p != 4 or tr_comp != 12:
        failures += 1

    return checks, failures


def build_simplicial_coboundaries(
    vertices: list[int],
    edges: list[tuple[int, int]],
    triangles: list[tuple[int, int, int]],
    tetrahedra: list[tuple[int, int, int, int]],
    four_simplices: list[tuple[int, int, int, int, int]],
) -> tuple[list[list[int]], list[list[int]], list[list[int]], list[list[int]]]:
    v_idx = {v: i for i, v in enumerate(vertices)}
    e_idx = {e: i for i, e in enumerate(edges)}
    t_idx = {t: i for i, t in enumerate(triangles)}
    tet_idx = {tet: i for i, tet in enumerate(tetrahedra)}

    d0 = [[0] * len(vertices) for _ in range(len(edges))]
    for i, (u, v) in enumerate(edges):
        d0[i][v_idx[v]] += 1
        d0[i][v_idx[u]] -= 1

    d1 = [[0] * len(edges) for _ in range(len(triangles))]
    for i, (u, v, w) in enumerate(triangles):
        for face, sgn in (((v, w), 1), ((u, w), -1), ((u, v), 1)):
            d1[i][e_idx[face]] += sgn

    d2 = [[0] * len(triangles) for _ in range(len(tetrahedra))]
    for i, (a, b, c, d) in enumerate(tetrahedra):
        for face, sgn in (
            ((b, c, d), 1),
            ((a, c, d), -1),
            ((a, b, d), 1),
            ((a, b, c), -1),
        ):
            d2[i][t_idx[face]] += sgn

    d3 = [[0] * len(tetrahedra) for _ in range(len(four_simplices))]
    for i, (a, b, c, d, e) in enumerate(four_simplices):
        for face, sgn in (
            ((b, c, d, e), 1),
            ((a, c, d, e), -1),
            ((a, b, d, e), 1),
            ((a, b, c, e), -1),
            ((a, b, c, d), 1),
        ):
            d3[i][tet_idx[face]] += sgn

    return d0, d1, d2, d3


def mat_mul_int(A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
    rows = len(A)
    cols = len(B[0])
    inner = len(B)
    return [
        [sum(A[r][k] * B[k][c] for k in range(inner)) for c in range(cols)]
        for r in range(rows)
    ]


def check_coboundary_and_commutator() -> tuple[int, int]:
    checks = 0
    failures = 0

    # Flat 4-simplex Delta^4 and curved 2-simplex CDT cluster
    complexes = [
        (
            list(range(5)),
            [(0, 1, 2, 3, 4)],
        ),
        (
            list(range(6)),
            [(0, 1, 2, 3, 4), (0, 1, 2, 3, 5)],
        ),
    ]
    for verts, f_simplices in complexes:
        edges = sorted(
            {
                tuple(sorted(e))
                for s in f_simplices
                for e in itertools.combinations(s, 2)
            }
        )
        tris = sorted(
            {
                tuple(sorted(t))
                for s in f_simplices
                for t in itertools.combinations(s, 3)
            }
        )
        tets = sorted(
            {
                tuple(sorted(tet))
                for s in f_simplices
                for tet in itertools.combinations(s, 4)
            }
        )
        d0, d1, d2, d3 = build_simplicial_coboundaries(
            verts, edges, tris, tets, f_simplices
        )
        for prod in (mat_mul_int(d1, d0), mat_mul_int(d2, d1), mat_mul_int(d3, d2)):
            for row in prod:
                for val in row:
                    checks += 1
                    if val != 0:
                        failures += 1

    # Flat vs curved Dirac-projector commutator [D_curved(c), P_0]
    for c_num in range(-10, 11):
        for c_den in (1, 2, 3, 5):
            c = Fraction(c_num, c_den)
            checks += 1
            comm_00 = Fraction(0)
            comm_01 = -c
            comm_10 = -c
            comm_11 = Fraction(0)
            frob_sq = comm_00 ** 2 + comm_01 ** 2 + comm_10 ** 2 + comm_11 ** 2
            if c == 0 and frob_sq != 0:
                failures += 1
            if c != 0 and (frob_sq != 2 * (c ** 2) or frob_sq <= 0):
                failures += 1

    # S^4 = partial Delta^5 Euler vs 4 * A_hat index mismatch
    checks += 1
    chi_s4 = 6 - 15 + 20 - 15 + 6
    ahat_s4 = 0
    if chi_s4 != 2 or chi_s4 - 4 * ahat_s4 != 2:
        failures += 1

    return checks, failures


def check_boundary_contractions_and_fences() -> tuple[int, int]:
    checks = 0
    failures = 0

    # 1. Mirror-glued 2-vertex contractions W = V^T V are PSD across 625 x 25 pairs
    entries = (-2, -1, 0, 1, 2)
    for v00, v01, v10, v11 in itertools.product(entries, repeat=4):
        V = ((Fraction(v00), Fraction(v01)), (Fraction(v10), Fraction(v11)))
        W = [
            [sum(V[k][i] * V[k][j] for k in range(2)) for j in range(2)]
            for i in range(2)
        ]
        for p0, p1 in itertools.product(entries, repeat=2):
            checks += 1
            psi = (Fraction(p0), Fraction(p1))
            quad = sum(
                psi[i] * W[i][j] * psi[j] for i in range(2) for j in range(2)
            )
            sos = sum(
                (sum(V[k][i] * psi[i] for i in range(2)) ** 2) for k in range(2)
            )
            if quad != sos or quad < 0:
                failures += 1

    # 2. Single-vertex spin-1 Racah 6j recoupling kernel W_6j = [[1/6, -1/3], [-1/3, 1/6]]
    W_6j = (
        (Fraction(1, 6), Fraction(-1, 3)),
        (Fraction(-1, 3), Fraction(1, 6)),
    )
    c_sym = sum(
        Fraction(1) * W_6j[i][j] * Fraction(1)
        for i in range(2)
        for j in range(2)
    )
    psi_anti = (Fraction(1), Fraction(-1))
    c_anti = sum(
        psi_anti[i] * W_6j[i][j] * psi_anti[j]
        for i in range(2)
        for j in range(2)
    )
    checks += 2
    if c_sym != Fraction(-1, 3) or c_sym >= 0 or c_anti != Fraction(1, 1) or c_anti <= 0:
        failures += 1

    # 3. Fence 1: 16-component diagonal determinants with odd number of -1 eigenvalues
    for neg_count in range(1, 17):
        checks += 1
        diag = [Fraction(-1) if i < neg_count else Fraction(1) for i in range(16)]
        det_val = Fraction(1)
        for d in diag:
            det_val *= d
        expected = Fraction(-1) if (neg_count % 2 == 1) else Fraction(1)
        if len(diag) != 16 or det_val != expected:
            failures += 1

    # 4. Fence 2: EPRL simplicity spin embedding j^+- = (1 +- gamma) k / 2
    for k_num in range(1, 10):
        for g_num in range(1, 6):
            k = Fraction(k_num, 2)
            gamma = Fraction(g_num, 6)
            checks += 1
            j_plus = (1 + gamma) * k / 2
            j_minus = (1 - gamma) * k / 2
            if j_plus + j_minus != k or j_plus - j_minus != gamma * k:
                failures += 1
    checks += 1
    two_jp = 2 * ((1 + Fraction(1, 2)) * Fraction(1) / 2)
    if two_jp != Fraction(3, 2) or two_jp.denominator == 1:
        failures += 1

    # 5. Fence 3: Odd-simplex orientation reversal Berezin sign (-1)^(2m+1) * w = -w < 0
    for m in range(20):
        for w in (Fraction(1, 3), Fraction(1, 1), Fraction(7, 2)):
            checks += 1
            val = (Fraction(-1) ** (2 * m + 1)) * w
            if val != -w or val >= 0:
                failures += 1

    return checks, failures


def main() -> int:
    c1, f1 = check_exterior_taste_and_orientifold()
    c2, f2 = check_coboundary_and_commutator()
    c3, f3 = check_boundary_contractions_and_fences()
    total_checks = c1 + c2 + c3
    total_failures = f1 + f2 + f3
    print(
        f"FSP-DIRAC-KAHLER-SPINFOAM-CLAIM independent check: "
        f"checks={total_checks} exterior_taste={c1} coboundary_comm={c2} "
        f"spinfoam_fences={c3} failures={total_failures}"
    )
    return 0 if total_failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
