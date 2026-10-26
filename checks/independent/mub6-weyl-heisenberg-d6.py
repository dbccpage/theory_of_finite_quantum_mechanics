"""Integer-pair clock and shift at dimension 6, with polynomial scalar sanity checks.

The matrix equality checks share the integer-pair computation; applying the
polynomial map to equal results is not an independent polynomial-matrix oracle.
"""

from __future__ import annotations

import sympy as sp


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def mul(x, y):
    a, b = x
    c, d = y
    return (a * c - b * d, a * d + b * c + b * d)


def conj(x):
    a, b = x
    return (a + b, -b)


ZERO = (0, 0)
ONE = (1, 0)
W = (0, 1)


def wpow(n):
    value = ONE
    for _ in range(n):
        value = mul(W, value)
    return value


def mmul(left, right):
    out = [[ZERO for _ in range(6)] for _ in range(6)]
    for i in range(6):
        for j in range(6):
            acc = ZERO
            for k in range(6):
                acc = add(acc, mul(left[i][k], right[k][j]))
            out[i][j] = acc
    return out


def mscale(factor, matrix):
    return [[mul(factor, matrix[i][j]) for j in range(6)] for i in range(6)]


def madj(matrix):
    return [[conj(matrix[j][i]) for j in range(6)] for i in range(6)]


def trace(matrix):
    acc = ZERO
    for i in range(6):
        acc = add(acc, matrix[i][i])
    return acc


def mpow(matrix, n):
    out = [[ONE if i == j else ZERO for j in range(6)] for i in range(6)]
    for _ in range(n):
        out = mmul(matrix, out)
    return out


def disp_entry(p, q, i, j):
    if i == (j + p) % 6:
        return wpow(q * j)
    return ZERO


SYMBOL = sp.symbols("w")
MODULUS = sp.Poly(SYMBOL**2 - SYMBOL + 1, SYMBOL)


def reduce_expr(expr):
    polynomial = sp.Poly(sp.expand(expr), SYMBOL)
    return polynomial.rem(MODULUS).as_expr()


def sym_of(pair):
    return reduce_expr(pair[0] + pair[1] * SYMBOL)


def check() -> int:
    failures = 0
    if wpow(2) != (-1, 1) or wpow(2) != add(W, (-1, 0)):
        failures += 1
    if wpow(3) != (-1, 0) or wpow(6) != ONE:
        failures += 1
    if mul(conj(W), W) != ONE:
        failures += 1
    if reduce_expr(SYMBOL**2 - (SYMBOL - 1)) != 0:
        failures += 1
    if reduce_expr(SYMBOL**3 - (-1)) != 0 or reduce_expr(SYMBOL**6 - 1) != 0:
        failures += 1

    shift = [[ONE if i == (j + 1) % 6 else ZERO for j in range(6)] for i in range(6)]
    clock = [[wpow(i) if i == j else ZERO for j in range(6)] for i in range(6)]
    zx = mmul(clock, shift)
    wxz = mscale(W, mmul(shift, clock))
    comm_mismatch = sum(zx[i][j] != wxz[i][j] for i in range(6) for j in range(6))
    if comm_mismatch != 0:
        failures += 1
    xz = mmul(shift, clock)
    wzx = mscale(W, zx)
    opposite_mismatch = sum(xz[i][j] != wzx[i][j] for i in range(6) for j in range(6))
    if opposite_mismatch == 0:
        failures += 1

    powers_x = [mpow(shift, p) for p in range(6)]
    powers_z = [mpow(clock, q) for q in range(6)]
    ops = [[mmul(powers_x[p], powers_z[q]) for q in range(6)] for p in range(6)]
    entry_fail = 0
    for p in range(6):
        for q in range(6):
            for i in range(6):
                for j in range(6):
                    got = ops[p][q][i][j]
                    expect = disp_entry(p, q, i, j)
                    if got != expect or sym_of(got) != sym_of(expect):
                        entry_fail += 1
    if entry_fail != 0:
        failures += 1

    orth_fail = 0
    pairs = 0
    for p in range(6):
        for q in range(6):
            for r in range(6):
                for s in range(6):
                    pairs += 1
                    value = trace(mmul(madj(ops[p][q]), ops[r][s]))
                    expect = (6, 0) if (p, q) == (r, s) else ZERO
                    if value != expect or sym_of(value) != sym_of(expect):
                        orth_fail += 1
    operators = sum(1 for p in range(6) for q in range(6))
    if orth_fail != 0 or pairs != 1296 or operators != 36:
        failures += 1

    print(
        "mub6-weyl-heisenberg-d6"
        f" failures={failures}"
        f" operators={operators}"
        f" pairs={pairs}"
        f" comm_mismatch={comm_mismatch}"
        f" opposite_mismatch={opposite_mismatch}"
        f" entry_fail={entry_fail}"
        f" orth_fail={orth_fail}"
    )
    return failures


if __name__ == "__main__":
    raise SystemExit(check())
