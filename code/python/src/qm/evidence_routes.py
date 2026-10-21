"""Determinant of the Pythagorean rotation numerator.

Origin: lean4/GroupParameter.lean theorem pyth_rot_numerator_det
(the determinant of [[3, -4, 0], [4, 3, 0], [0, 0, 5]] is 125).
Claim: urn:omega:fqm:route:pythagorean-rotation-det:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_evidence_routes.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 4; AST Sonar cognitive complexity max 3; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 4.
Scope Fence: rotation_numerator_det returns that integer determinant.
On the default matrix it requires 125. route_digest_length returns the
SHA-256 byte length of a rebuilt parent digest of Fraction(2, 3) and
Fraction(4, 5), which is 32. That length is not the cited theorem.
This file does not prove the boost-numerator determinant or the Pauli
trace.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction
from typing import Mapping

_ROTATION: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]] = (
    (3, -4, 0),
    (4, 3, 0),
    (0, 0, 5),
)
_DETERMINANT = 125


class EvidenceRouteError(Exception):
    """One violated route invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> EvidenceRouteError:
    return EvidenceRouteError(invariant, parameters)


def _require_int(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the matrix boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where an integer entry was required", role=role)
    if type(value) is int:
        if value.bit_length() > 1024:
            raise _fail("integer exceeds 1024 bits", role=role)
        return value
    raise _fail("matrix entry is not an integer", role=role, received=type(value).__name__)


def _require_row(row: object, role: str) -> tuple[int, int, int]:
    if isinstance(row, (str, bytes)) or not isinstance(row, tuple):
        raise _fail("matrix row is not a tuple", role=role, received=type(row).__name__)
    if len(row) != 3:
        raise _fail("matrix row is not a triple", role=role, length=len(row))
    return (_require_int(row[0], role), _require_int(row[1], role), _require_int(row[2], role))


def _require_matrix(
    matrix: object,
) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]:
    if isinstance(matrix, (str, bytes)) or not isinstance(matrix, tuple):
        raise _fail("matrix is not a tuple", received=type(matrix).__name__)
    if len(matrix) != 3:
        raise _fail("matrix is not 3 by 3", length=len(matrix))
    return (
        _require_row(matrix[0], "row0"),
        _require_row(matrix[1], "row1"),
        _require_row(matrix[2], "row2"),
    )


def _determinant(
    rows: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]],
) -> int:
    first = rows[0][0] * (rows[1][1] * rows[2][2] - rows[1][2] * rows[2][1])
    second = rows[0][1] * (rows[1][0] * rows[2][2] - rows[1][2] * rows[2][0])
    third = rows[0][2] * (rows[1][0] * rows[2][1] - rows[1][1] * rows[2][0])
    return first - second + third


def rotation_numerator_det(matrix: object | None = None) -> int:
    """Return det of the Pythagorean numerator, or of another integer 3 by 3 matrix."""
    rows = _require_matrix(_ROTATION if matrix is None else matrix)
    value = _determinant(rows)
    if matrix is None and value != _DETERMINANT:
        raise _fail("rotation numerator determinant is not 125", determinant=value)
    return value


def route_digest_length() -> int:
    """Return the byte length of a parent digest that matches its rebuild."""
    left = hashlib.sha256(f"{Fraction(2, 3)}".encode("ascii")).digest()
    right = hashlib.sha256(f"{Fraction(4, 5)}".encode("ascii")).digest()
    parent = hashlib.sha256(left + right).digest()
    rebuilt = hashlib.sha256(bytes(left) + bytes(right)).digest()
    if parent != rebuilt:
        raise _fail("parent digest did not rebuild")
    if len(parent) != 32:
        raise _fail("digest length is not 32", length=len(parent))
    return len(parent)


def main() -> int:
    value = rotation_numerator_det()
    print(value)
    if value == _DETERMINANT and route_digest_length() == 32:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
