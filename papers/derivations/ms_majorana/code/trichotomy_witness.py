"""F2 residual trichotomy. Exact, closed residual, and open obstruction are disjoint.

Origin: papers/derivations/ms_majorana/lean4/MajoranaCore.lean theorem trichotomy_pairwise_disjoint
Claim: urn:omega:fqm:ms-majorana:trichotomy:f2-disjoint-classes:v1
AuthorityEffect: None
Mutation-Kills: 6 non-equivalent source mutants, executed by papers/derivations/ms_majorana/code/tests/unit/test_l5a_exact_slice.py.
Scope Fence: This file does not decide detector adequacy of a hardware readout and does not use floating rank.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


class TrichotomyError(ValueError):
    """One violated trichotomy invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> TrichotomyError:
    return TrichotomyError(invariant, parameters)


def _bit(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if isinstance(value, bool) or type(value) is not int:
        raise _fail("boolean or non-bit refused", role=role, received=type(value).__name__)
    if value not in (0, 1):
        raise _fail("F2 coordinate is not 0 or 1", role=role, received=value)
    return value


def _vector(values: object, role: str, width: int | None) -> tuple[int, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise _fail("F2 vector must be a sequence", role=role, received=type(values).__name__)
    parsed = tuple(_bit(item, f"{role}[{index}]") for index, item in enumerate(values))
    if width is not None and len(parsed) != width:
        raise _fail("F2 vector length does not match the operator", role=role, length=len(parsed), expected=width)
    return parsed


def _matrix(values: object, role: str, width: int | None) -> tuple[tuple[int, ...], ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise _fail("F2 matrix must be a sequence of rows", role=role, received=type(values).__name__)
    rows = tuple(_vector(item, f"{role}[{index}]", width) for index, item in enumerate(values))
    if len(rows) == 0:
        return rows
    expected = len(rows[0])
    for index, row in enumerate(rows):
        if len(row) != expected:
            raise _fail("F2 matrix row lengths differ", role=role, row=index, length=len(row), expected=expected)
    return rows


def _dot(row: Sequence[int], vector: Sequence[int]) -> int:
    total = 0
    for coeff, bit in zip(row, vector):
        total = (total + coeff * bit) % 2
    return total


def _matvec(matrix: Sequence[Sequence[int]], vector: Sequence[int]) -> tuple[int, ...]:
    return tuple(_dot(row, vector) for row in matrix)


def _zero(length: int) -> tuple[int, ...]:
    return tuple(0 for _ in range(length))


def _xor_row(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    return tuple((a + b) % 2 for a, b in zip(left, right))


def _pivot(rows: Sequence[tuple[int, ...]], column: int, start: int) -> int | None:
    for index in range(start, len(rows)):
        if rows[index][column] == 1:
            return index
    return None


def _clear(rows: list[tuple[int, ...]], column: int, pivot: int) -> None:
    for index in range(len(rows)):
        if index != pivot and rows[index][column] == 1:
            rows[index] = _xor_row(rows[index], rows[pivot])


def _rref(matrix: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    working = [tuple(row) for row in matrix]
    if len(working) == 0:
        return ()
    pivot = 0
    width = len(working[0])
    for column in range(width):
        found = _pivot(working, column, pivot)
        if found is None:
            continue
        if found != pivot:
            working[pivot], working[found] = working[found], working[pivot]
        _clear(working, column, pivot)
        pivot += 1
    return tuple(working)


def _nonzero(row: Sequence[int]) -> bool:
    for bit in row:
        if bit == 1:
            return True
    return False


def _rank(matrix: Sequence[Sequence[int]]) -> int:
    total = 0
    for row in _rref(matrix):
        if _nonzero(row):
            total += 1
    return total


def _augment(matrix: Sequence[Sequence[int]], vector: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(row) + (bit,) for row, bit in zip(matrix, vector))


def _in_image(matrix: Sequence[Sequence[int]], vector: Sequence[int]) -> bool:
    if len(matrix) == 0:
        return _rank(()) == 0 and len(vector) == 0
    return _rank(matrix) == _rank(_augment(matrix, vector))


def _column(matrix: Sequence[Sequence[int]], index: int) -> tuple[int, ...]:
    return tuple(row[index] for row in matrix)


def _nilpotent(d0: Sequence[Sequence[int]], d1: Sequence[Sequence[int]]) -> bool:
    if len(d0) == 0:
        return True
    for index in range(len(d0[0])):
        image = _matvec(d1, _column(d0, index))
        if image != _zero(len(d1)):
            return False
    return True


def is_cocycle(d1: object, witness: object) -> bool:
    """Return whether d1(witness) is the zero vector. Nilpotency is not checked here."""
    matrix = _matrix(d1, "d1", None)
    vector = _vector(witness, "witness", len(matrix[0]) if len(matrix) else len(_vector(witness, "witness", None)))
    if len(matrix) != 0 and len(vector) != len(matrix[0]):
        raise _fail("witness length does not match d1", length=len(vector), expected=len(matrix[0]))
    return _matvec(matrix, vector) == _zero(len(matrix))


def is_exact(d0: object, witness: object) -> bool:
    """Return whether the witness lies in the F2 image of d0."""
    matrix = _matrix(d0, "d0", None)
    vector = _vector(witness, "witness", len(matrix))
    if len(vector) != len(matrix):
        raise _fail("witness length does not match d0", length=len(vector), expected=len(matrix))
    return _in_image(matrix, vector)


@dataclass(frozen=True)
class TrichotomyCertificate:
    """Witness of one class together with the three disjoint predicates."""

    kind: str
    exact: bool
    closed_residual: bool
    open_obstruction: bool


def _class_name(exact: bool, closed: bool, opened: bool) -> str:
    if opened:
        return "OpenObstruction"
    if exact:
        return "Exact"
    if closed:
        return "ClosedResidual"
    raise _fail("witness did not meet a trichotomy class")


def _predicates(d0: Sequence[Sequence[int]], d1: Sequence[Sequence[int]], witness: Sequence[int]) -> tuple[bool, bool, bool]:
    opened = _matvec(d1, witness) != _zero(len(d1))
    exact = _in_image(d0, witness)
    closed = (not opened) and (not exact)
    return exact, closed, opened


def _shapes(
    boundary: Sequence[Sequence[int]],
    coboundary: Sequence[Sequence[int]],
    vector: Sequence[int],
) -> None:
    if len(coboundary) != 0 and len(coboundary[0]) != len(boundary):
        raise _fail("d1 input dimension does not match d0", d0_rows=len(boundary), d1_cols=len(coboundary[0]))
    if len(vector) != len(boundary):
        raise _fail("witness length does not match d0", length=len(vector), expected=len(boundary))
    if not _nilpotent(boundary, coboundary):
        raise _fail("complex is not nilpotent", relation="d1 d0 = 0")


def _disjoint(exact: bool, closed: bool, opened: bool) -> None:
    if exact and closed:
        raise _fail("exact and closed residual were both true")
    if exact and opened:
        raise _fail("exact and open obstruction were both true")
    if closed and opened:
        raise _fail("closed residual and open obstruction were both true")


def classify_residual(d0: object, d1: object, witness: object) -> TrichotomyCertificate:
    """Classify one F2 cochain and recheck that the three classes stay disjoint."""
    boundary = _matrix(d0, "d0", None)
    coboundary = _matrix(d1, "d1", None)
    vector = _vector(witness, "witness", len(boundary))
    _shapes(boundary, coboundary, vector)
    exact, closed, opened = _predicates(boundary, coboundary, vector)
    _disjoint(exact, closed, opened)
    return TrichotomyCertificate(_class_name(exact, closed, opened), exact, closed, opened)


def cohomologous(d0: object, left: object, right: object) -> bool:
    """Return whether left - right lies in the image of d0."""
    matrix = _matrix(d0, "d0", None)
    first = _vector(left, "left", len(matrix))
    second = _vector(right, "right", len(matrix))
    difference = tuple((a + b) % 2 for a, b in zip(first, second))
    return _in_image(matrix, difference)


__all__ = [
    "TrichotomyCertificate",
    "TrichotomyError",
    "classify_residual",
    "cohomologous",
    "is_cocycle",
    "is_exact",
]
