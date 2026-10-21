"""Integer determinant of the boost numerator and the Pauli Z trace.

Origin: lean4/GroupParameter.lean theorem b1_numerator_det
(b1Numerator 0 0 * b1Numerator 1 1 - b1Numerator 0 1 * b1Numerator 1 0 = 16
for b1Numerator = [[5, 3], [3, 5]]) and theorem pauli_z_trace_zero
(pauliZ 0 0 + pauliZ 1 1 = 0 for pauliZ = diag(1, -1)).
Claim: urn:omega:fqm:group:boost-numerator-det:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_group_param.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 4; AST Sonar cognitive complexity max 3; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 4.
Scope Fence: boost_numerator_det returns that integer determinant. On the
default matrix it requires 16. pauli_trace returns the diagonal sum. On the
default Pauli Z it requires 0. shear_parameter returns the (0, 1) entry of
S(2/3) S(4/5), which equals 22/15, and is not either cited theorem. This
file does not prove Lindemann-Weierstrass, the parameter-transcendence
theorems, or pyth_rot_numerator_det.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_BOOST: tuple[tuple[int, int], tuple[int, int]] = ((5, 3), (3, 5))
_PAULI: tuple[tuple[int, int], tuple[int, int]] = ((1, 0), (0, -1))
_DETERMINANT = 16
_TRACE = 0


class GroupParamError(Exception):
    """One violated matrix invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> GroupParamError:
    return GroupParamError(invariant, parameters)


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


def _require_row(row: object, role: str) -> tuple[int, int]:
    if isinstance(row, (str, bytes)) or not isinstance(row, tuple):
        raise _fail("matrix row is not a tuple", role=role, received=type(row).__name__)
    if len(row) != 2:
        raise _fail("matrix row is not a pair", role=role, length=len(row))
    return (_require_int(row[0], role), _require_int(row[1], role))


def _require_matrix(matrix: object) -> tuple[tuple[int, int], tuple[int, int]]:
    if isinstance(matrix, (str, bytes)) or not isinstance(matrix, tuple):
        raise _fail("matrix is not a tuple", received=type(matrix).__name__)
    if len(matrix) != 2:
        raise _fail("matrix is not 2 by 2", length=len(matrix))
    return (_require_row(matrix[0], "row0"), _require_row(matrix[1], "row1"))


def _determinant(rows: tuple[tuple[int, int], tuple[int, int]]) -> int:
    return rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]


def _diagonal_sum(rows: tuple[tuple[int, int], tuple[int, int]]) -> int:
    return rows[0][0] + rows[1][1]


def boost_numerator_det(matrix: object | None = None) -> int:
    """Return det([[5, 3], [3, 5]]) = 16, or the determinant of another integer matrix."""
    rows = _require_matrix(_BOOST if matrix is None else matrix)
    value = _determinant(rows)
    if matrix is None and value != _DETERMINANT:
        raise _fail("boost numerator determinant is not 16", determinant=value)
    return value


def pauli_trace(matrix: object | None = None) -> int:
    """Return the trace of diag(1, -1), which is 0, or the trace of another matrix."""
    rows = _require_matrix(_PAULI if matrix is None else matrix)
    value = _diagonal_sum(rows)
    if matrix is None and value != _TRACE:
        raise _fail("Pauli Z trace is not zero", trace=value)
    return value


def _shear_entry(left: Fraction, right: Fraction) -> Fraction:
    return Fraction(1) * right + left * Fraction(1)


def shear_parameter() -> Fraction:
    """Return the (0, 1) entry of S(2/3) S(4/5), which is 22/15."""
    left = Fraction(2, 3)
    right = Fraction(4, 5)
    entry = _shear_entry(left, right)
    if entry != left + right:
        raise _fail("shear parameter left the sum", entry=str(entry))
    return entry


def main() -> int:
    value = boost_numerator_det()
    trace = pauli_trace()
    print(value)
    if value == _DETERMINANT and trace == _TRACE:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
