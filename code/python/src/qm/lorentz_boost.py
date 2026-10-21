"""A rational boost preserves the Minkowski form and the hyperbolic identity.

Origin: lean4/LorentzBoost.lean theorem boost_hyperbolic_identity
(5 * 5 - 3 * 3 = 16) and theorem boost_det.
Claim: urn:omega:fqm:qm:minkowski-boost-defect:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: The checked boost is beta = 3/5, gamma = 5/4. The file does not
classify the Lorentz group.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_DEFECT = Fraction(0)
_IDENTITY = 16


class LorentzError(Exception):
    """One violated boost invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> LorentzError:
    return LorentzError(invariant, parameters)


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


def hyperbolic_identity() -> int:
    """Return 5 * 5 - 3 * 3, which theorem boost_hyperbolic_identity sets to 16."""
    value = _require_fraction(5, "five") * _require_fraction(5, "fiveb") - _require_fraction(3, "three") * _require_fraction(3, "threeb")
    if value != _IDENTITY:
        raise _fail("hyperbolic identity is not 16", value=str(value))
    return int(value)


def _entry(left: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]], right: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]], row: int, column: int) -> Fraction:
    return left[row][0] * right[0][column] + left[row][1] * right[1][column]


def _mul(left: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]], right: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    top = (_entry(left, right, 0, 0), _entry(left, right, 0, 1))
    bottom = (_entry(left, right, 1, 0), _entry(left, right, 1, 1))
    return (top, bottom)


def _transpose(matrix: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    return ((matrix[0][0], matrix[1][0]), (matrix[0][1], matrix[1][1]))


def _abs_entry_sum(left: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]], right: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> Fraction:
    return abs(left[0][0] - right[0][0]) + abs(left[0][1] - right[0][1]) + abs(left[1][0] - right[1][0]) + abs(left[1][1] - right[1][1])


def minkowski_defect() -> Fraction:
    """Sum of absolute entries of B^T η B − η for beta = 3/5 and gamma = 5/4."""
    if hyperbolic_identity() != _IDENTITY:
        raise _fail("hyperbolic identity is not 16")
    beta = Fraction(3, 5)
    gamma = Fraction(5, 4)
    if gamma * gamma * (1 - beta * beta) != 1:
        raise _fail("gamma is not the Lorentz factor of beta", beta=str(beta), gamma=str(gamma))
    boost = ((gamma, gamma * beta), (gamma * beta, gamma))
    eta = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(-1)))
    preserved = _mul(_transpose(boost), _mul(eta, boost))
    return _abs_entry_sum(preserved, eta)


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the Minkowski defect 0."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return _locked(minkowski_defect(), _DEFECT, "Minkowski defect drifted")


def main() -> int:
    value = minkowski_defect()
    print(value)
    if value == _DEFECT and hyperbolic_identity() == _IDENTITY:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
