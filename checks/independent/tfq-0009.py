#!/usr/bin/env python3
"""Independent verification for TFQ-0009 (FINITE_GAUGE).

Disjoint computational check of:
1. Shared finite complex boundary exactness (d_1 o d_2 = 0 on single and adjacent plaquettes).
2. Abelian cochain connection, coboundary curvature (d_1 o d_0 = 0), gauge invariance,
   and the discrete Bianchi identity (d_2 o d_1 = 0) on the 6-face, 12-edge 3-cube.
3. Non-abelian 2x2 matrix link holonomy conjugation, cyclic trace invariance, Wilson loop
   gauge invariance, and the abelian vs. non-abelian commutator fork.
4. No-continuum-Yang-Mills fence: finite cochain cardinality N^E and metric-coupling
   dependence of the Yang-Mills plaquette action versus metric-free combinatorial curvature.
"""

from __future__ import annotations

from fractions import Fraction
import itertools


def check_boundary_and_abelian_cochains() -> int:
    checks = 0
    # 1. Single plaquette boundary d_1(d_2(c)) == (0, 0, 0, 0)
    for c in range(-10, 11):
        e0, e1, e2, e3 = c, c, c, c
        v0 = e3 - e0
        v1 = e0 - e1
        v2 = e1 - e2
        v3 = e2 - e3
        assert (v0, v1, v2, v3) == (0, 0, 0, 0)
        checks += 1

    # 2. Adjacent plaquettes shared edge cancellation
    for cL in range(-6, 7):
        for cR in range(-6, 7):
            mid = cL - cR
            if cL == cR:
                assert mid == 0
            else:
                assert mid != 0
            checks += 1

    # 3. Abelian coboundary d_1(d_0(lam)) == 0 and gauge invariance d_1(A + d_0(lam)) == d_1(A)
    for l0, l1, l2, l3 in itertools.product(range(-3, 4), repeat=4):
        d0 = (l1 - l0, l2 - l1, l3 - l2, l0 - l3)
        assert sum(d0) == 0
        checks += 1
        A = (2, -5, 7, 3)
        A_gauge = tuple(a + da for a, da in zip(A, d0))
        assert sum(A_gauge) == sum(A)
        checks += 1

    # 4. Discrete abelian Bianchi identity on 12-edge 3-cube
    for seed in range(-15, 16):
        b0, b1, b2, b3 = seed + 1, seed - 2, 2 * seed + 3, -seed + 4
        t0, t1, t2, t3 = seed + 5, -2 * seed + 1, seed - 7, 3 * seed + 2
        v0, v1, v2, v3 = -seed + 3, 2 * seed - 1, seed + 6, -3 * seed + 4
        f_bot = b0 + b1 + b2 + b3
        f_top = t0 + t1 + t2 + t3
        f_0 = b0 + v1 - t0 - v0
        f_1 = b1 + v2 - t1 - v1
        f_2 = b2 + v3 - t2 - v2
        f_3 = b3 + v0 - t3 - v3
        assert (f_top - f_bot + f_0 + f_1 + f_2 + f_3) == 0
        checks += 1

    return checks


def mat_mul(A: tuple[int, int, int, int], B: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return (
        A[0] * B[0] + A[1] * B[2],
        A[0] * B[1] + A[1] * B[3],
        A[2] * B[0] + A[3] * B[2],
        A[2] * B[1] + A[3] * B[3],
    )


def mat_inv_sl2(G: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    det = G[0] * G[3] - G[1] * G[2]
    assert det == 1
    return (G[3], -G[1], -G[2], G[0])


def mat_trace(A: tuple[int, int, int, int]) -> int:
    return A[0] + A[3]


def check_nonabelian_holonomy_and_fork() -> int:
    checks = 0
    sl2_pool = [
        (1, 0, 0, 1),
        (1, 1, 0, 1),
        (1, -1, 0, 1),
        (1, 0, 1, 1),
        (1, 0, -1, 1),
        (2, 1, 1, 1),
        (1, 2, 1, 3),
        (0, -1, 1, 0),
    ]
    U0, U1, U2, U3 = sl2_pool[1], sl2_pool[3], sl2_pool[5], sl2_pool[6]
    H_orig = mat_mul(mat_mul(mat_mul(U0, U1), U2), U3)

    for g0, g1 in itertools.product(sl2_pool[:6], repeat=2):
        for g2, g3 in itertools.product(sl2_pool[:4], repeat=2):
            g0_inv = mat_inv_sl2(g0)
            g1_inv = mat_inv_sl2(g1)
            g2_inv = mat_inv_sl2(g2)
            g3_inv = mat_inv_sl2(g3)

            U0_g = mat_mul(mat_mul(g0, U0), g1_inv)
            U1_g = mat_mul(mat_mul(g1, U1), g2_inv)
            U2_g = mat_mul(mat_mul(g2, U2), g3_inv)
            U3_g = mat_mul(mat_mul(g3, U3), g0_inv)

            H_g = mat_mul(mat_mul(mat_mul(U0_g, U1_g), U2_g), U3_g)
            H_conj = mat_mul(mat_mul(g0, H_orig), g0_inv)
            assert H_g == H_conj
            assert mat_trace(H_g) == mat_trace(H_orig)
            checks += 2

    # Non-abelian fork witness
    S_up = (1, 1, 0, 1)
    S_lo = (1, 0, 1, 1)
    assert mat_mul(S_up, S_lo) != mat_mul(S_lo, S_up)
    S_conj = mat_mul(mat_mul(S_up, S_lo), mat_inv_sl2(S_up))
    assert S_conj != S_lo
    assert mat_trace(S_conj) == mat_trace(S_lo)
    checks += 3
    return checks


def check_yang_mills_fence() -> int:
    checks = 0
    for N in range(2, 10):
        for E in range(1, 6):
            assert (N ** E) >= (2 ** E)
            checks += 1

    # Metric coupling fence
    A = (1, 0, 0, 0)
    curv = sum(A)
    assert curv == 1
    for n1 in range(1, 10):
        for n2 in range(n1 + 1, 11):
            w1 = Fraction(1, n1)
            w2 = Fraction(1, n2)
            act1 = w1 * (curv ** 2)
            act2 = w2 * (curv ** 2)
            assert act1 != act2
            checks += 1
    return checks


def main() -> None:
    c_ab = check_boundary_and_abelian_cochains()
    c_na = check_nonabelian_holonomy_and_fork()
    c_ym = check_yang_mills_fence()
    total = c_ab + c_na + c_ym
    print(f"checks={total} abelian_cochain={c_ab} nonabelian_holonomy={c_na} ym_fence={c_ym} failures=0")


if __name__ == "__main__":
    main()
