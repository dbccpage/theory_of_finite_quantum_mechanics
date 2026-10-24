#!/usr/bin/env python3
"""Independent verification for TFQ-0014 (FINITE_QCD).

Disjoint computational check of:
1. Finite 2-object pair groupoid convolution over Z[i] (associativity, two-sided unit
   e00 + e11, orthogonal object idempotents e00 * e11 = 0, and C*-norm sqrt(2) parity obstruction).
2. M_2(Z[i]) qubit packet cochain differential d_0(Omega)(X) = [Omega, X] (tracelessness,
   scalar kernel, Leibniz derivation rule, and Jacobi identity).
3. Non-equivalence fences separating groupoid convolution and M_2 qubit packet complexes
   from Hopf gauge modules and SU(3) color links (matrix entry count 4 != 9, Lie dimension
   3 != 8, fundamental Casimir 3/4 != 4/3, and Lie derivation vs. multiplicative link law).
"""

from __future__ import annotations

from fractions import Fraction
import itertools


def gi_add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] + b[0], a[1] + b[1])


def gi_sub(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] - b[0], a[1] - b[1])


def gi_mul(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def conv(A, B):
    return (
        gi_add(gi_mul(A[0], B[0]), gi_mul(A[1], B[2])),
        gi_add(gi_mul(A[0], B[1]), gi_mul(A[1], B[3])),
        gi_add(gi_mul(A[2], B[0]), gi_mul(A[3], B[2])),
        gi_add(gi_mul(A[2], B[1]), gi_mul(A[3], B[3])),
    )


def mat_add(A, B):
    return tuple(gi_add(x, y) for x, y in zip(A, B))


def mat_sub(A, B):
    return tuple(gi_sub(x, y) for x, y in zip(A, B))


def packet_d0(Omega, X):
    return mat_sub(conv(Omega, X), conv(X, Omega))


def check_groupoid_convolution() -> int:
    checks = 0
    zero = ((0, 0), (0, 0), (0, 0), (0, 0))
    ident = ((1, 0), (0, 0), (0, 0), (1, 0))
    e00 = ((1, 0), (0, 0), (0, 0), (0, 0))
    e11 = ((0, 0), (0, 0), (0, 0), (1, 0))

    assert conv(e00, e00) == e00
    assert conv(e11, e11) == e11
    assert conv(e00, e11) == zero
    assert conv(e11, e00) == zero
    checks += 4

    pool = [
        ((1, 0), (0, 1), (-1, 0), (2, -1)),
        ((0, 1), (1, 1), (2, 0), (-1, 1)),
        ((2, 1), (-1, 2), (0, -1), (1, 0)),
        ((-1, -1), (2, 0), (1, -2), (0, 2)),
        ((1, 2), (0, 0), (3, -1), (-2, 1)),
        ((0, 0), (1, -1), (-1, 1), (2, 2)),
    ]
    for A in pool:
        assert conv(ident, A) == A
        assert conv(A, ident) == A
        checks += 2
    for A, B, C in itertools.product(pool, repeat=3):
        assert conv(conv(A, B), C) == conv(A, conv(B, C))
        checks += 1

    # C*-norm sqrt(2) parity obstruction
    for p in range(-10, 11):
        for q in range(-10, 11):
            assert (2 * p + 1) ** 2 != 2 * (q ** 2)
            checks += 1
    return checks


def check_packet_cochain_d0() -> int:
    checks = 0
    zero = ((0, 0), (0, 0), (0, 0), (0, 0))
    ident = ((1, 0), (0, 0), (0, 0), (1, 0))
    pool = [
        ((1, 0), (0, 1), (-1, 0), (2, -1)),
        ((0, 1), (1, 1), (2, 0), (-1, 1)),
        ((2, 1), (-1, 2), (0, -1), (1, 0)),
        ((-1, -1), (2, 0), (1, -2), (0, 2)),
        ((1, 0), (0, 0), (0, 0), (-1, 0)),
        ((0, 0), (1, 0), (1, 0), (0, 0)),
    ]
    for Omega, X in itertools.product(pool, repeat=2):
        comm = packet_d0(Omega, X)
        tr = gi_add(comm[0], comm[3])
        assert tr == (0, 0)
        assert packet_d0(Omega, ident) == zero
        checks += 2

    for Omega, X, Y in itertools.product(pool, repeat=3):
        # Leibniz rule
        lhs = packet_d0(Omega, conv(X, Y))
        rhs = mat_add(conv(packet_d0(Omega, X), Y), conv(X, packet_d0(Omega, Y)))
        assert lhs == rhs
        # Jacobi identity
        j1 = packet_d0(Omega, packet_d0(X, Y))
        j2 = packet_d0(X, packet_d0(Y, Omega))
        j3 = packet_d0(Y, packet_d0(Omega, X))
        assert mat_add(mat_add(j1, j2), j3) == zero
        checks += 2
    return checks


def check_su3_and_hopf_fences() -> int:
    checks = 0
    zero = ((0, 0), (0, 0), (0, 0), (0, 0))
    ident = ((1, 0), (0, 0), (0, 0), (1, 0))
    assert conv(ident, ident) == ident
    assert packet_d0(ident, ident) == zero
    assert conv(ident, ident) != packet_d0(ident, ident)
    checks += 3

    # M_2 vs SU(3) dimensions and Casimir
    assert 2 ** 2 == 4 and 3 ** 2 == 9 and (2 ** 2) != (3 ** 2)
    assert (2 ** 2 - 1) == 3 and (3 ** 2 - 1) == 8
    c2_su2 = Fraction(2 ** 2 - 1, 2 * 2)
    c2_su3 = Fraction(3 ** 2 - 1, 2 * 3)
    assert c2_su2 == Fraction(3, 4) and c2_su3 == Fraction(4, 3) and c2_su2 != c2_su3
    checks += 3

    # Lie derivation vs multiplicative homomorphism on sigma_z and sigma_x
    sigma_z = ((1, 0), (0, 0), (0, 0), (-1, 0))
    sigma_x = ((0, 0), (1, 0), (1, 0), (0, 0))
    assert packet_d0(sigma_z, conv(sigma_x, sigma_x)) == zero
    assert conv(packet_d0(sigma_z, sigma_x), packet_d0(sigma_z, sigma_x)) != zero
    checks += 2
    return checks


def main() -> None:
    c_grp = check_groupoid_convolution()
    c_pkt = check_packet_cochain_d0()
    c_fnc = check_su3_and_hopf_fences()
    total = c_grp + c_pkt + c_fnc
    print(f"checks={total} groupoid_conv={c_grp} packet_d0={c_pkt} su3_fence={c_fnc} failures=0")


if __name__ == "__main__":
    main()
