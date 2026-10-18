"""Recover a rational matrix from its action on the coordinate basis.

Origin: code/python/src/linear_algebra/elimination.py function
witness_upper_entry, which states the witness [[1, 2], [3, 4]].
Claim: urn:omega:fqm:qm:matrix-column-recovery:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_matrix_recovery.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 3; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: The defect is the entrywise absolute difference between the
witness and the matrix rebuilt from its columns. This file does not factor
the witness and does not claim a pseudoinverse.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping, Sequence


class RecoveryError(ValueError):
    """One violated recovery invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> RecoveryError:
    return RecoveryError(invariant, parameters)


_WITNESS: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]] = (
    (Fraction(1), Fraction(2)),
    (Fraction(3), Fraction(4)),
)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _exact(value: object, role: str) -> Fraction:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where an exact rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is not int:
        raise _fail("matrix entry is not an exact rational", role=role, received=type(value).__name__)
    return Fraction(value)


def _column(value: object, role: str, height: int) -> tuple[Fraction, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, tuple):
        raise _fail("basis image is not a column", role=role, received=type(value).__name__)
    if len(value) != height:
        raise _fail("basis images do not match the dimension", role=role, height=height, received=len(value))
    return tuple(_exact(entry, role + "_" + str(index)) for index, entry in enumerate(value))


def _columns(value: object) -> tuple[tuple[Fraction, ...], ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, tuple) or len(value) == 0:
        raise _fail("columns are not a nonempty tuple", received=type(value).__name__)
    height = len(value)
    return tuple(_column(column, "column" + str(index), height) for index, column in enumerate(value))


def _witness_columns() -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    return (
        (_WITNESS[0][0], _WITNESS[1][0]),
        (_WITNESS[0][1], _WITNESS[1][1]),
    )


def recover(columns: object) -> tuple[tuple[Fraction, ...], ...]:
    """Rebuild the matrix whose columns are the images of the coordinate basis."""
    parsed = _columns(columns)
    width = len(parsed)
    return tuple(tuple(parsed[column][row] for column in range(width)) for row in range(width))


def _entry_defect(rebuilt: Sequence[Sequence[Fraction]]) -> Fraction:
    defect = Fraction(0)
    for row in range(2):
        for column in range(2):
            defect += abs(rebuilt[row][column] - _WITNESS[row][column])
    return defect


def recovery_defect(columns: object = None) -> Fraction:
    """Entrywise absolute defect of the rebuilt witness. The frozen defect is 0."""
    source = _witness_columns() if columns is None else columns
    rebuilt = recover(source)
    if len(rebuilt) != 2:
        raise _fail("recovery witness is 2 by 2", rows=len(rebuilt))
    defect = _entry_defect(rebuilt)
    if defect != 0:
        raise _fail("recovery defect is not zero", defect=str(defect))
    return defect


__all__ = ["RecoveryError", "recover", "recovery_defect"]
