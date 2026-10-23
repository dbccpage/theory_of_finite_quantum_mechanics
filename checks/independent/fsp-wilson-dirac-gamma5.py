#!/usr/bin/env python3
"""Independent exact check for FSP-WILSON-DIRAC-GAMMA5.

Origin: checks/independent/fsp-wilson-dirac-gamma5.py
Claim: on the periodic 2x2 lattice in d=2, mass -1, color U(1), and the
link phases in this file, the Wilson-Dirac matrix at r=1 has determinant -3,
matches gamma5 M gamma5 = M adjoint, has characteristic polynomial
[1, -8, 28, -56, 66, -40, 4, 8, -3], and has two-flavor determinant 9.
Clifford relations in d=2 and d=4 are checked on the matrices written here.
AuthorityEffect: None.

Imports no repository module. Scalars are Gaussian integers (sympy Integer and I).
"""

from __future__ import annotations

import sys

import sympy as sp


I = sp.I
z = sp.Integer


def eye(n: int) -> sp.Matrix:
    return sp.eye(n)


def zeros(n: int, m: int) -> sp.Matrix:
    return sp.zeros(n, m)


def mat2(a, b, c, d) -> sp.Matrix:
    return sp.Matrix([[a, b], [c, d]])


def require(cond: bool, message: str) -> None:
    if not cond:
        raise SystemExit(message)


def check_pauli() -> None:
    s1 = mat2(0, 1, 1, 0)
    s2 = mat2(0, -I, I, 0)
    s3 = mat2(1, 0, 0, -1)
    require(s1 * s1 == eye(2), "pauli1 square")
    require(s2 * s2 == eye(2), "pauli2 square")
    require(s3 * s3 == eye(2), "pauli3 square")
    require(s1 * s2 + s2 * s1 == zeros(2, 2), "pauli 12")
    require(s1 * s3 + s3 * s1 == zeros(2, 2), "pauli 13")
    require(s2 * s3 + s3 * s2 == zeros(2, 2), "pauli 23")


def block_off(b: sp.Matrix, c: sp.Matrix) -> sp.Matrix:
    top = b.row_join(zeros(2, 2))
    # fromBlocks 0 B C 0 means rows (0, B) and (C, 0)
    return sp.BlockMatrix([[zeros(2, 2), b], [c, zeros(2, 2)]]).as_explicit()


def check_clifford_d2() -> sp.Matrix:
    g0 = mat2(0, 1, 1, 0)
    g1 = mat2(1, 0, 0, -1)
    g5 = mat2(0, I, -I, 0)
    gammas = [g0, g1]
    for mu, g in enumerate(gammas):
        require(g * g == eye(2), f"d2 square {mu}")
        require(g.H == g, f"d2 herm {mu}")
        require(g5 * g * g5 == -g, f"d2 gamma5 anti {mu}")
    require(g0 * g1 + g1 * g0 == zeros(2, 2), "d2 off anticommutator")
    require(g5.H == g5, "d2 gamma5 herm")
    require(g5 * g5 == eye(2), "d2 gamma5 square")
    return g5


def check_clifford_d4() -> sp.Matrix:
    s1 = mat2(0, 1, 1, 0)
    s2 = mat2(0, -I, I, 0)
    s3 = mat2(1, 0, 0, -1)
    spatial = [block_off((-I) * s, I * s) for s in (s1, s2, s3)]
    temporal = block_off(eye(2), eye(2))
    gammas = spatial + [temporal]
    g5 = sp.BlockMatrix([[eye(2), zeros(2, 2)], [zeros(2, 2), -eye(2)]]).as_explicit()
    for mu, g in enumerate(gammas):
        require(g * g == eye(4), f"d4 square {mu}")
        require(g.H == g, f"d4 herm {mu}")
        require(g5 * g * g5 == -g, f"d4 gamma5 anti {mu}")
    for mu in range(4):
        for nu in range(mu):
            require(gammas[mu] * gammas[nu] + gammas[nu] * gammas[mu] == zeros(4, 4),
                    f"d4 anti {mu}{nu}")
    require(g5.H == g5, "d4 gamma5 herm")
    require(g5 * g5 == eye(4), "d4 gamma5 square")
    return g5


def phase(mu: int, x0: int, x1: int):
    if mu == 0:
        return -z(1) if (x0, x1) == (1, 1) else z(1)
    return I if x0 == 1 else z(1)


def build_witness() -> sp.Matrix:
    """Wilson-Dirac, r = 1, d = 2, extents (2, 2), mass -1, color U(1)."""
    g = [mat2(0, 1, 1, 0), mat2(1, 0, 0, -1)]
    sites = [(0, 0), (0, 1), (1, 0), (1, 1)]
    n = 8
    d = sp.zeros(n)
    mass = -z(1)

    def idx(x0: int, x1: int, s: int) -> int:
        return (x0 * 2 + x1) * 2 + s

    def add_block(x0, x1, y0, y1, block: sp.Matrix) -> None:
        for s in range(2):
            for t in range(2):
                d[idx(x0, x1, s), idx(y0, y1, t)] += block[s, t]

    for x0, x1 in sites:
        add_block(x0, x1, x0, x1, (mass + z(2)) * eye(2))
        for mu in range(2):
            step = (1, 0) if mu == 0 else (0, 1)
            y0 = (x0 + step[0]) % 2
            y1 = (x1 + step[1]) % 2
            z0 = (x0 - step[0]) % 2
            z1 = (x1 - step[1]) % 2
            fwd = sp.Rational(1, 2) * (g[mu] - eye(2)) * phase(mu, x0, x1)
            bwd = sp.Rational(-1, 2) * (g[mu] + eye(2)) * sp.conjugate(phase(mu, z0, z1))
            add_block(x0, x1, y0, y1, fwd)
            add_block(x0, x1, z0, z1, bwd)
    return d


def gamma5_op() -> sp.Matrix:
    g5 = mat2(0, I, -I, 0)
    out = sp.zeros(8)
    for site in range(4):
        for s in range(2):
            for t in range(2):
                out[site * 2 + s, site * 2 + t] = g5[s, t]
    return out


def main() -> int:
    check_pauli()
    check_clifford_d2()
    check_clifford_d4()
    d = build_witness()
    literal = sp.Matrix([
        [1, 0, -1, 0, -1, 0, 0, 0],
        [0, 1, 0, -1, 0, -1, 0, 0],
        [-1, 0, 1, 0, 0, 0, 0, 1],
        [0, -1, 0, 1, 0, 0, 1, 0],
        [-1, 0, 0, 0, 1, 0, I, 0],
        [0, -1, 0, 0, 0, 1, 0, -I],
        [0, 0, 0, -1, I, 0, 1, 0],
        [0, 0, -1, 0, 0, -I, 0, 1],
    ])
    require(d == literal, "witness matrix differs from the recorded literal")
    for i in range(8):
        for j in range(8):
            entry = sp.simplify(d[i, j])
            require(entry in (0, 1, -1, I, -I), f"entry {(i, j)} left the Gaussian integers")
    det = sp.simplify(d.det())
    require(det == -3, f"det = {det}")
    g5 = gamma5_op()
    require(g5 * d * g5 - d.H == zeros(8, 8), "gamma5 hermiticity failed")
    charpoly = d.charpoly(sp.symbols("lam"))
    coeffs = [sp.Integer(c) for c in charpoly.all_coeffs()]
    require(coeffs == [1, -8, 28, -56, 66, -40, 4, 8, -3], f"charpoly {coeffs}")
    two = sp.BlockMatrix([[d, sp.zeros(8)], [sp.zeros(8), d]]).as_explicit().det()
    require(sp.simplify(two) == 9, f"two-flavor det = {two}")
    require(sp.re(det) < 0 and sp.im(det) == 0, "single-flavor det is not a negative real")
    print("independent check ok")
    print("det", det)
    print("two_flavor_det", sp.simplify(two))
    print("charpoly", coeffs)
    return 0


if __name__ == "__main__":
    sys.exit(main())
