"""Integer 3 by 3 check of one forced block identity.

No repository imports. AuthorityEffect: None.
"""

from __future__ import annotations


def mul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)
    ]


def transpose(a):
    return [[a[j][i] for j in range(3)] for i in range(3)]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(3)] for i in range(3)]


def neg(a):
    return [[-a[i][j] for j in range(3)] for i in range(3)]


def check() -> int:
    b_mat = [[1, 1, 0], [0, 1, 1], [0, 0, 1]]
    b_inv = [[1, -1, 1], [0, 1, -1], [0, 0, 1]]
    e_mat = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    c_mat = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]
    d_mat = [[1, -1, 0], [-1, 1, -1], [-1, 0, 0]]
    eye = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    zero = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    failures = 0
    if mul(b_mat, b_inv) != eye or mul(b_inv, b_mat) != eye:
        failures += 1
    formula = neg(mul(mul(c_mat, transpose(e_mat)), transpose(b_inv)))
    if formula != d_mat:
        failures += 1
    cross = add(mul(c_mat, transpose(e_mat)), mul(d_mat, transpose(b_mat)))
    if cross != zero:
        failures += 1
    zero_cross = add(mul(c_mat, transpose(e_mat)), mul(zero, transpose(b_mat)))
    nonzero = sum(cell != 0 for row in zero_cross for cell in row)
    if zero_cross == zero or nonzero != 3:
        failures += 1
    print(
        "mub6-finite-corner-reduction"
        f" failures={failures}"
        " rows=3"
        " inverse_sides=2"
        f" cross_nonzero_entries={nonzero}"
    )
    return failures


if __name__ == "__main__":
    raise SystemExit(check())
