"""Smith normal form over the integers, cleared from a rational matrix.

Origin: code/python/src/linear_algebra/smith_form.py
Claim: unimodular integer factors satisfy U * A * V = D, and the positive
diagonal entries of an integer matrix divide in order.
AuthorityEffect: None. This is a finite certificate, not a classification theorem.
"""
from fractions import Fraction
from math import gcd
from typing import List, Tuple

from .matrix import ExactMatrix


class SmithFormError(Exception):
    """The Smith factorization could not be built or failed its identity."""


def _lcm(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return abs(a // gcd(a, b) * b)


def _integer_entries(matrix: ExactMatrix) -> Tuple[List[List[int]], int]:
    rows: List[List[Fraction]] = []
    cleared = 1
    for r in range(matrix.rows):
        row: List[Fraction] = []
        for c in range(matrix.cols):
            value = matrix.get(r, c)
            if type(value).__name__ == "GaussianRational":
                raise SmithFormError("Smith form in this module is over Q, not Q(i)")
            try:
                entry = Fraction(value)
            except (TypeError, ValueError) as exc:
                raise SmithFormError(f"entry {value!r} is not rational") from exc
            row.append(entry)
            cleared = _lcm(cleared, entry.denominator)
        rows.append(row)
    scaled = [[int(entry * cleared) for entry in row] for row in rows]
    return scaled, cleared


def smith_normal_form(matrix: ExactMatrix) -> Tuple[ExactMatrix, ExactMatrix, ExactMatrix]:
    """Return D, U, V with U and V unimodular over Z and U * matrix * V = D.

    Rational entries are cleared by the least common denominator c. The integer
    Smith form of c*A is then divided by c. Diagonal entries are nonnegative.
    """
    source, scale = _integer_entries(matrix)
    m = matrix.rows
    n = matrix.cols
    work = [row[:] for row in source]
    left = [[1 if i == j else 0 for j in range(m)] for i in range(m)]
    right = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    def swap_rows(i: int, j: int) -> None:
        if i == j:
            return
        work[i], work[j] = work[j], work[i]
        left[i], left[j] = left[j], left[i]

    def swap_cols(i: int, j: int) -> None:
        if i == j:
            return
        for r in range(m):
            work[r][i], work[r][j] = work[r][j], work[r][i]
        for r in range(n):
            right[r][i], right[r][j] = right[r][j], right[r][i]

    def add_row(dst: int, src: int, coeff: int) -> None:
        if coeff == 0:
            return
        for c in range(n):
            work[dst][c] += coeff * work[src][c]
        for c in range(m):
            left[dst][c] += coeff * left[src][c]

    def add_col(dst: int, src: int, coeff: int) -> None:
        if coeff == 0:
            return
        for r in range(m):
            work[r][dst] += coeff * work[r][src]
        for r in range(n):
            right[r][dst] += coeff * right[r][src]

    def negate_row(i: int) -> None:
        for c in range(n):
            work[i][c] = -work[i][c]
        for c in range(m):
            left[i][c] = -left[i][c]

    steps = 0
    limit = 32 * (m + n + 1) * (m + n + 1) + 8
    for k in range(min(m, n)):
        finished = False
        while True:
            steps += 1
            if steps > limit:
                raise SmithFormError("Smith form exceeded its elimination bound")
            pivot = None
            for i in range(k, m):
                for j in range(k, n):
                    if work[i][j] != 0 and (pivot is None or abs(work[i][j]) < abs(work[pivot[0]][pivot[1]])):
                        pivot = (i, j)
            if pivot is None:
                finished = True
                break
            swap_rows(k, pivot[0])
            swap_cols(k, pivot[1])
            if work[k][k] < 0:
                negate_row(k)
            for i in range(k + 1, m):
                if work[i][k] == 0:
                    continue
                add_row(i, k, -(work[i][k] // work[k][k]))
            for j in range(k + 1, n):
                if work[k][j] == 0:
                    continue
                add_col(j, k, -(work[k][j] // work[k][k]))
            if any(work[i][k] != 0 for i in range(k + 1, m)) or any(work[k][j] != 0 for j in range(k + 1, n)):
                continue
            bad = None
            for i in range(k + 1, m):
                for j in range(k + 1, n):
                    if work[i][j] % work[k][k] != 0:
                        bad = (i, j)
                        break
                if bad is not None:
                    break
            if bad is None:
                break
            add_row(k, bad[0], 1)
        if finished:
            break

    diagonal = []
    for i in range(m):
        row = []
        for j in range(n):
            entry = work[i][j] if i == j and i < min(m, n) else 0
            row.append(Fraction(entry, scale))
        diagonal.append(row)
    d_mat = ExactMatrix.from_rows(diagonal) if m and n else ExactMatrix(m, n, [])
    u_mat = ExactMatrix.from_rows([[Fraction(entry) for entry in row] for row in left]) if m else ExactMatrix(0, 0, [])
    v_mat = ExactMatrix.from_rows([[Fraction(entry) for entry in row] for row in right]) if n else ExactMatrix(0, 0, [])
    if m and n and (u_mat * matrix * v_mat) != d_mat:
        raise SmithFormError("constructed factors do not satisfy U*A*V = D")
    if m == 0 or n == 0:
        if u_mat * matrix * v_mat != d_mat:
            raise SmithFormError("constructed factors do not satisfy U*A*V = D")
    return d_mat, u_mat, v_mat


def invariant_factors(matrix: ExactMatrix) -> Tuple[Fraction, ...]:
    """Diagonal of the Smith form, including exact zeros past the rank."""
    diagonal, _, _ = smith_normal_form(matrix)
    count = min(matrix.rows, matrix.cols)
    return tuple(Fraction(diagonal.get(i, i)) for i in range(count))
