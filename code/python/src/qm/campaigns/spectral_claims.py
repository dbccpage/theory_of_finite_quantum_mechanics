"""Characteristic values of a rational 2 by 2 matrix.

Origin: code/python/src/qm/campaigns/spectral_claims.py
Claim: urn:omega:fqm:qm:rational-eigenvalue-defect:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 8; AST Sonar cognitive complexity max 7; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 8.
Scope Fence: det(λI − A) is checked at λ = 1 and λ = 2 for A = [[1, 1], [0, 2]].
The constant term equals det(A) = 2. No general spectral theorem is claimed.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_DEFECT = Fraction(0)


class SpectralError(Exception):
    """One violated spectral invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> SpectralError:
    return SpectralError(invariant, parameters)


def _require_fraction(value: object, role: str) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def characteristic_value(matrix: object, point: object) -> Fraction:
    """det(point * I − matrix) for a 2 by 2 matrix."""
    if isinstance(matrix, (str, bytes)) or not isinstance(matrix, tuple) or len(matrix) != 2:
        raise _fail("spectral matrix is not 2 by 2", received=type(matrix).__name__)
    top = matrix[0]
    bottom = matrix[1]
    if not isinstance(top, tuple) or not isinstance(bottom, tuple) or len(top) != 2 or len(bottom) != 2:
        raise _fail("spectral row is not a pair")
    left = _require_fraction(point, "point")
    a = _require_fraction(top[0], "a")
    b = _require_fraction(top[1], "b")
    c = _require_fraction(bottom[0], "c")
    d = _require_fraction(bottom[1], "d")
    return (left - a) * (left - d) - b * c


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


def eigenvalue_defect() -> Fraction:
    """Absolute characteristic values at the eigenvalues 1 and 2, added."""
    matrix = ((1, 1), (0, 2))
    at_one = characteristic_value(matrix, 1)
    at_two = characteristic_value(matrix, 2)
    constant = characteristic_value(matrix, 0)
    if constant != 2:
        raise _fail("constant term is not det(A)", constant=str(constant))
    return _locked(abs(at_one) + abs(at_two), _DEFECT, "eigenvalue defect drifted")


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the eigenvalue defect 0."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return eigenvalue_defect()


def main() -> int:
    value = eigenvalue_defect()
    print(value)
    if value == _DEFECT:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
