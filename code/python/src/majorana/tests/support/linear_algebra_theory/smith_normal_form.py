from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Tuple
import numpy as np


class SmithError(Exception):
    """Base class for Smith Normal Form errors."""


class NonIntegerEntry(SmithError):
    """Raised when a non-integer entry is passed to Smith Normal Form."""


class VerificationFailed(SmithError):
    """Raised when terminal certification U * A * V = D or Smith divisibility fails."""


class AlgorithmIncomplete(SmithError):
    """Raised when the reduction step limit is exceeded."""


def _egcd(a: int, b: int) -> Tuple[int, int, int]:
    """Extended Euclidean Algorithm: returns (g, x, y) such that a*x + b*y = g."""
    if b == 0:
        return (abs(a), 1 if a >= 0 else -1, 0)
    g, x1, y1 = _egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)


def _mat_mul_int(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """Exact integer matrix multiplication without overflow."""
    rows_A = len(A)
    cols_A = len(A[0]) if rows_A > 0 else 0
    rows_B = len(B)
    cols_B = len(B[0]) if rows_B > 0 else 0
    if cols_A != rows_B:
        raise ValueError(f"Matrix dimension mismatch in int multiplication: {cols_A} != {rows_B}")
    out = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for k in range(cols_A):
            if A[i][k] != 0:
                for j in range(cols_B):
                    out[i][j] += A[i][k] * B[k][j]
    return out


class SmithDiagonal:
    """Certified diagonal invariants of Smith normal form over Z."""

    def __init__(self, invariants: List[int]):
        self._invariants = tuple(int(x) for x in invariants)

    @classmethod
    def new_checked(cls, invariants: List[int]) -> "SmithDiagonal":
        invs = [int(x) for x in invariants]
        for d in invs:
            if d <= 0:
                raise ValueError("invalid Smith invariant; invariants must be positive")
        for p1, p2 in zip(invs[:-1], invs[1:]):
            if p2 % p1 != 0:
                raise ValueError(f"Smith divisibility violation: {p1} does not divide {p2}")
        return cls(invs)

    def invariants(self) -> List[int]:
        return list(self._invariants)

    def rank(self) -> int:
        return len(self._invariants)


class SmithNormalForm:
    """Result of Smith normal form computation certifying U * A * V = D."""

    def __init__(self, diagonal: SmithDiagonal, diagonal_matrix: np.ndarray, u: np.ndarray, v: np.ndarray):
        self._diagonal = diagonal
        self._diagonal_matrix = np.asarray(diagonal_matrix, dtype=object).copy()
        self._u = np.asarray(u, dtype=object).copy()
        self._v = np.asarray(v, dtype=object).copy()

    def diagonal(self) -> SmithDiagonal:
        return self._diagonal

    def diagonal_matrix(self) -> np.ndarray:
        return self._diagonal_matrix.copy()

    def u(self) -> np.ndarray:
        return self._u.copy()

    def v(self) -> np.ndarray:
        return self._v.copy()


def smith_normal_form_checked(matrix: Any) -> SmithNormalForm:
    """Computes exact integer Smith Normal Form U * A * V = D with terminal certification.

    Rejects non-integer inputs, arbitrary-precision integer safe, bounded elimination loop,
    and independently verifies U * A * V = D in pure integer arithmetic.
    """
    if hasattr(matrix, "tolist"):
        raw_list = matrix.tolist()
    elif isinstance(matrix, (list, tuple)):
        raw_list = [list(row) if isinstance(row, (list, tuple)) else [row] for row in matrix]
    else:
        raise NonIntegerEntry(f"Unsupported matrix container type: {type(matrix)}")

    m = len(raw_list)
    n = len(raw_list[0]) if m > 0 else 0

    if m == 0 or n == 0:
        diag = SmithDiagonal([])
        d_mat = np.zeros((m, n), dtype=object)
        u_mat = np.eye(m, dtype=object)
        v_mat = np.eye(n, dtype=object)
        return SmithNormalForm(diagonal=diag, diagonal_matrix=d_mat, u=u_mat, v=v_mat)

    A_orig: List[List[int]] = []
    for i, row in enumerate(raw_list):
        if len(row) != n:
            raise ValueError(f"Row {i} length {len(row)} != expected {n}")
        row_ints: List[int] = []
        for j, val in enumerate(row):
            if isinstance(val, bool) or not isinstance(val, (int, np.integer)):
                raise NonIntegerEntry(
                    f"Matrix entry {val!r} at ({i}, {j}) is of type {type(val).__name__}, not an exact integer"
                )
            row_ints.append(int(val))
        A_orig.append(row_ints)

    d = [[A_orig[i][j] for j in range(n)] for i in range(m)]
    u = [[1 if i == j else 0 for j in range(m)] for i in range(m)]
    v = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    r = min(m, n)
    max_steps = 2000 * (m + n + 1)
    step_count = 0

    for k in range(r):
        while True:
            step_count += 1
            if step_count > max_steps:
                raise AlgorithmIncomplete(
                    f"Smith normal form reduction exceeded step limit ({max_steps})"
                )

            pivot = None
            min_val = None
            for i in range(k, m):
                for j in range(k, n):
                    if d[i][j] != 0:
                        val = abs(d[i][j])
                        if min_val is None or val < min_val:
                            min_val = val
                            pivot = (i, j)
            if pivot is None:
                break

            pi, pj = pivot
            if pi != k:
                d[pi], d[k] = d[k], d[pi]
                u[pi], u[k] = u[k], u[pi]
            if pj != k:
                for row in d:
                    row[pj], row[k] = row[k], row[pj]
                for row in v:
                    row[pj], row[k] = row[k], row[pj]

            if d[k][k] < 0:
                for j in range(n):
                    d[k][j] = -d[k][j]
                for j in range(m):
                    u[k][j] = -u[k][j]

            cleared = True
            for i in range(k + 1, m):
                if d[i][k] != 0:
                    q = d[i][k] // d[k][k]
                    for j in range(n):
                        d[i][j] -= q * d[k][j]
                    for j in range(m):
                        u[i][j] -= q * u[k][j]
                    if d[i][k] != 0:
                        cleared = False
                        break

            if not cleared:
                continue

            for j in range(k + 1, n):
                if d[k][j] != 0:
                    q = d[k][j] // d[k][k]
                    for i in range(m):
                        d[i][j] -= q * d[i][k]
                    for i in range(n):
                        v[i][j] -= q * v[i][k]
                    if d[k][j] != 0:
                        cleared = False
                        break

            if not cleared:
                continue

            has_row_col = any(d[i][k] != 0 for i in range(k + 1, m)) or any(d[k][j] != 0 for j in range(k + 1, n))
            if has_row_col:
                continue

            divides_all = True
            bad_pos = None
            for i in range(k + 1, m):
                for j in range(k + 1, n):
                    if d[i][j] % d[k][k] != 0:
                        divides_all = False
                        bad_pos = (i, j)
                        break
                if not divides_all:
                    break

            if not divides_all and bad_pos is not None:
                bi, bj = bad_pos
                for j in range(n):
                    d[k][j] += d[bi][j]
                for j in range(m):
                    u[k][j] += u[bi][j]
                continue

            break

    for i in range(r):
        if d[i][i] < 0:
            for j in range(n):
                d[i][j] = -d[i][j]
            for j in range(m):
                u[i][j] = -u[i][j]

    for i in range(m):
        for j in range(n):
            if i != j and d[i][j] != 0:
                raise VerificationFailed(f"Off-diagonal element non-zero: D[{i}, {j}] = {d[i][j]}")

    invs = [d[i][i] for i in range(r) if d[i][i] != 0]
    for p1, p2 in zip(invs[:-1], invs[1:]):
        if p2 % p1 != 0:
            raise VerificationFailed(f"Divisibility violation: {p1} does not divide {p2}")

    UA = _mat_mul_int(u, A_orig)
    UAV = _mat_mul_int(UA, v)
    for i in range(m):
        for j in range(n):
            if UAV[i][j] != d[i][j]:
                raise VerificationFailed(
                    f"Identity violation: (U * A * V)[{i}, {j}] = {UAV[i][j]} != D[{i}, {j}] = {d[i][j]}"
                )

    diag = SmithDiagonal.new_checked(invs)
    d_mat = np.array(d, dtype=object)
    u_mat = np.array(u, dtype=object)
    v_mat = np.array(v, dtype=object)

    return SmithNormalForm(diagonal=diag, diagonal_matrix=d_mat, u=u_mat, v=v_mat)


def from_rational64_integer_matrix(matrix: Any) -> SmithNormalForm:
    return smith_normal_form_checked(matrix)



