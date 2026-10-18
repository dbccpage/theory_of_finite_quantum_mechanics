"""Smith normal form over Z, cleared from a rational matrix.

Origin: code/rust/src/linear_algebra/smith_form.rs, which certifies
U * A * V = D, where U and V are unimodular products of elementary
row and column operations, by pivot-selection elimination over Z.
Claim: urn:omega:fqm:linear-algebra:smith-normal-form:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_smith_form.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 7; AST Sonar cognitive complexity max 10; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 7.
Scope Fence: the factors are checked on the rational matrix after clearing
denominators, and a later negative diagonal entry is negated. This file uses
remainder elimination plus a one-row repair, one shared step budget, and the
empty matrix. It does not run the Rust extended-gcd replacement, the per-pivot
iteration counter, the overflow error, or the empty-matrix refusal, and it
does not admit floats or Q(i).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import Mapping

from .matrix import ExactMatrix, MatrixError
from .scalars import GaussianRational


class SmithFormError(MatrixError):
    """One violated Smith invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> SmithFormError:
    return SmithFormError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _require_entry(value: object, role: str) -> Fraction:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a rational entry was required", role=role)
    if isinstance(value, GaussianRational):
        raise _fail("Gaussian rational refused; Smith form in this module is over Q", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("matrix entry is not an exact rational", role=role, received=type(value).__name__)


def _require_dimension(value: object, role: str) -> int:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a matrix dimension was required", role=role)
    if type(value) is int:
        if value < 0:
            raise _fail("matrix shape is negative", role=role, received=value)
        return value
    raise _fail("matrix shape is not an integer", role=role, received=type(value).__name__)


def _require_data_length(matrix: ExactMatrix, rows: int, cols: int) -> None:
    length = len(matrix.data)
    if length != rows * cols:
        raise _fail("matrix data length does not match the shape", length=length, rows=rows, cols=cols)


def _require_matrix(matrix: object) -> ExactMatrix:
    if not isinstance(matrix, ExactMatrix):
        raise _fail("Smith form expects an exact matrix", received=type(matrix).__name__)
    rows = _require_dimension(matrix.rows, "rows")
    cols = _require_dimension(matrix.cols, "cols")
    _require_data_length(matrix, rows, cols)
    return matrix


def _lcm(left: int, right: int) -> int:
    if left == 0 or right == 0:
        return 0
    return abs(left // gcd(left, right) * right)


def _parse_row(matrix: ExactMatrix, row: int) -> list[Fraction]:
    return [_require_entry(matrix.get(row, col), f"entry[{row},{col}]") for col in range(matrix.cols)]


def _row_scale(row: list[Fraction], scale: int) -> int:
    for entry in row:
        scale = _lcm(scale, entry.denominator)
    return scale


def _rational_rows(matrix: ExactMatrix) -> tuple[list[list[Fraction]], int]:
    rows: list[list[Fraction]] = []
    scale = 1
    for row in range(matrix.rows):
        parsed = _parse_row(matrix, row)
        scale = _row_scale(parsed, scale)
        rows.append(parsed)
    return rows, scale


def _integer_rows(rows: list[list[Fraction]], scale: int) -> list[list[int]]:
    return [[int(entry * scale) for entry in row] for row in rows]


def _identity(size: int) -> list[list[int]]:
    return [[1 if col == row else 0 for col in range(size)] for row in range(size)]


def _elimination_limit(rows: int, cols: int) -> int:
    span = rows + cols + 1
    return 32 * span * span + 8


@dataclass
class _Board:
    work: list[list[int]]
    left: list[list[int]]
    right: list[list[int]]
    rows: int
    cols: int
    steps: int
    limit: int


def _make_board(work: list[list[int]], rows: int, cols: int) -> _Board:
    return _Board(work, _identity(rows), _identity(cols), rows, cols, 0, _elimination_limit(rows, cols))


def _swap_rows(board: _Board, left: int, right: int) -> None:
    if left == right:
        return
    board.work[left], board.work[right] = board.work[right], board.work[left]
    board.left[left], board.left[right] = board.left[right], board.left[left]


def _swap_cols(board: _Board, left: int, right: int) -> None:
    if left == right:
        return
    for row in board.work:
        row[left], row[right] = row[right], row[left]
    for row in board.right:
        row[left], row[right] = row[right], row[left]


def _axpy(destination: list[int], source: list[int], coeff: int) -> None:
    for index in range(len(destination)):
        destination[index] += coeff * source[index]


def _add_row(board: _Board, destination: int, source: int, coeff: int) -> None:
    if coeff == 0:
        return
    _axpy(board.work[destination], board.work[source], coeff)
    _axpy(board.left[destination], board.left[source], coeff)


def _add_col(board: _Board, destination: int, source: int, coeff: int) -> None:
    if coeff == 0:
        return
    for row in board.work:
        row[destination] += coeff * row[source]
    for row in board.right:
        row[destination] += coeff * row[source]


def _negate(row: list[int]) -> None:
    for index in range(len(row)):
        row[index] = -row[index]


def _negate_row(board: _Board, index: int) -> None:
    _negate(board.work[index])
    _negate(board.left[index])


def _charge_step(board: _Board) -> None:
    board.steps += 1
    if board.steps > board.limit:
        raise _fail("Smith form exceeded its elimination bound", steps=board.steps, limit=board.limit)


def _smaller(
    work: list[list[int]],
    row: int,
    col: int,
    current: tuple[int, int] | None,
) -> bool:
    if current is None:
        return True
    pivot_row, pivot_col = current
    return abs(work[row][col]) < abs(work[pivot_row][pivot_col])


def _pivot_in_row(
    work: list[list[int]],
    row: int,
    start: int,
    cols: int,
    current: tuple[int, int] | None,
) -> tuple[int, int] | None:
    chosen = current
    for col in range(start, cols):
        if work[row][col] == 0:
            continue
        if _smaller(work, row, col, chosen):
            chosen = (row, col)
    return chosen


def _smallest_pivot(work: list[list[int]], start: int, cols: int) -> tuple[int, int] | None:
    chosen: tuple[int, int] | None = None
    for row in range(start, len(work)):
        chosen = _pivot_in_row(work, row, start, cols, chosen)
    return chosen


def _prepare_pivot(board: _Board, pivot: int, chosen: tuple[int, int]) -> None:
    _swap_rows(board, pivot, chosen[0])
    _swap_cols(board, pivot, chosen[1])
    if board.work[pivot][pivot] < 0:
        _negate_row(board, pivot)


def _quotient(entry: int, pivot: int) -> int:
    if pivot == 0:
        raise _fail("Smith pivot is zero", entry=entry)
    return -(entry // pivot)


def _clear_one_below(board: _Board, row: int, pivot: int) -> None:
    entry = board.work[row][pivot]
    if entry == 0:
        return
    _add_row(board, row, pivot, _quotient(entry, board.work[pivot][pivot]))


def _clear_below(board: _Board, pivot: int) -> None:
    for row in range(pivot + 1, board.rows):
        _clear_one_below(board, row, pivot)


def _clear_one_right(board: _Board, pivot: int, col: int) -> None:
    entry = board.work[pivot][col]
    if entry == 0:
        return
    _add_col(board, col, pivot, _quotient(entry, board.work[pivot][pivot]))


def _clear_right(board: _Board, pivot: int) -> None:
    for col in range(pivot + 1, board.cols):
        _clear_one_right(board, pivot, col)


def _column_dirty(work: list[list[int]], pivot: int) -> bool:
    for row in range(pivot + 1, len(work)):
        if work[row][pivot] != 0:
            return True
    return False


def _row_dirty(work: list[list[int]], pivot: int, cols: int) -> bool:
    for col in range(pivot + 1, cols):
        if work[pivot][col] != 0:
            return True
    return False


def _still_dirty(board: _Board, pivot: int) -> bool:
    if _column_dirty(board.work, pivot):
        return True
    return _row_dirty(board.work, pivot, board.cols)


def _nondivisor_in_row(work: list[list[int]], row: int, start: int, cols: int, modulus: int) -> int | None:
    for col in range(start + 1, cols):
        if work[row][col] % modulus != 0:
            return col
    return None


def _first_nondivisor(work: list[list[int]], pivot: int, cols: int) -> tuple[int, int] | None:
    modulus = work[pivot][pivot]
    if modulus == 0:
        raise _fail("Smith pivot is zero", entry=0)
    for row in range(pivot + 1, len(work)):
        col = _nondivisor_in_row(work, row, pivot, cols, modulus)
        if col is not None:
            return (row, col)
    return None


def _repair_or_accept(board: _Board, pivot: int) -> str:
    found = _first_nondivisor(board.work, pivot, board.cols)
    if found is None:
        return "next"
    _add_row(board, pivot, found[0], 1)
    return "retry"


def _one_attempt(board: _Board, pivot: int) -> str:
    _charge_step(board)
    chosen = _smallest_pivot(board.work, pivot, board.cols)
    if chosen is None:
        return "done"
    _prepare_pivot(board, pivot, chosen)
    _clear_below(board, pivot)
    _clear_right(board, pivot)
    if _still_dirty(board, pivot):
        return "retry"
    return _repair_or_accept(board, pivot)


def _reduce_column(board: _Board, pivot: int) -> bool:
    while True:
        status = _one_attempt(board, pivot)
        if status == "done":
            return True
        if status == "next":
            return False


def _normalize_signs(board: _Board) -> None:
    for index in range(min(board.rows, board.cols)):
        if board.work[index][index] < 0:
            _negate_row(board, index)


def _eliminate(board: _Board) -> None:
    for pivot in range(min(board.rows, board.cols)):
        if _reduce_column(board, pivot):
            break
    _normalize_signs(board)


def _cleared_diagonal(board: _Board) -> list[int]:
    return [board.work[index][index] for index in range(min(board.rows, board.cols))]


def _require_divisibility(diagonal: list[int]) -> None:
    previous = 0
    seen_zero = False
    for entry in diagonal:
        if entry < 0:
            raise _fail("Smith diagonal entry is negative", entry=entry)
        if entry == 0:
            seen_zero = True
            continue
        if seen_zero:
            raise _fail("nonzero Smith entry follows a zero", entry=entry)
        if previous != 0 and entry % previous != 0:
            raise _fail("Smith divisibility failed", left=previous, right=entry)
        previous = entry


def _diagonal_entry(board: _Board, scale: int, row: int, col: int) -> Fraction:
    rank = min(board.rows, board.cols)
    if row == col and row < rank:
        return Fraction(board.work[row][col], scale)
    return Fraction(0)


def _diagonal_matrix(board: _Board, scale: int) -> ExactMatrix:
    if board.rows == 0 or board.cols == 0:
        return ExactMatrix(board.rows, board.cols, [])
    rows = [
        [_diagonal_entry(board, scale, row, col) for col in range(board.cols)]
        for row in range(board.rows)
    ]
    return ExactMatrix.from_rows(rows)


def _integer_matrix(grid: list[list[int]]) -> ExactMatrix:
    if not grid:
        return ExactMatrix(0, 0, [])
    return ExactMatrix.from_rows([[Fraction(entry) for entry in row] for row in grid])


def _require_product(
    original: ExactMatrix,
    left: ExactMatrix,
    right: ExactMatrix,
    diagonal: ExactMatrix,
) -> None:
    if left * original * right != diagonal:
        raise _fail("constructed factors do not satisfy U*A*V = D")


def _require_unimodular(transform: ExactMatrix, role: str) -> None:
    det = transform.determinant()
    if type(det) is not Fraction or abs(det) != 1:
        raise _fail("transform determinant is not ±1", role=role, determinant=str(det))


def smith_normal_form(matrix: object) -> tuple[ExactMatrix, ExactMatrix, ExactMatrix]:
    """Return D, U, V with U and V unimodular over Z and U * matrix * V = D."""
    source = _require_matrix(matrix)
    rational_rows, scale = _rational_rows(source)
    board = _make_board(_integer_rows(rational_rows, scale), source.rows, source.cols)
    _eliminate(board)
    _require_divisibility(_cleared_diagonal(board))
    diagonal = _diagonal_matrix(board, scale)
    left = _integer_matrix(board.left)
    right = _integer_matrix(board.right)
    _require_product(source, left, right, diagonal)
    _require_unimodular(left, "U")
    _require_unimodular(right, "V")
    return diagonal, left, right


def invariant_factors(matrix: object) -> tuple[Fraction, ...]:
    """Diagonal of the Smith form, including exact zeros past the rank."""
    source = _require_matrix(matrix)
    diagonal, _, _ = smith_normal_form(source)
    count = min(source.rows, source.cols)
    return tuple(_require_entry(diagonal.get(index, index), f"invariant[{index}]") for index in range(count))


def witness_diagonal_sum() -> Fraction:
    """Sum of the Smith diagonal of [[2, 4], [2, 6]], which is 4."""
    witness = ExactMatrix.from_rows(
        [
            [Fraction(2), Fraction(4)],
            [Fraction(2), Fraction(6)],
        ]
    )
    diagonal, _, _ = smith_normal_form(witness)
    first = _require_entry(diagonal.get(0, 0), "witness[0]")
    second = _require_entry(diagonal.get(1, 1), "witness[1]")
    return first + second
