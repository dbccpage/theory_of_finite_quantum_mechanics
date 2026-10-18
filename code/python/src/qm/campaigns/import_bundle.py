"""Determinant, trace, and purity of one rational matrix, multiplied.

Origin: code/python/src/qm/campaigns/import_bundle.py
Claim: urn:omega:fqm:qm:rational-bundle-product:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: The bundle is computed from [[1, 1], [0, 2]] only.
Trace 3, determinant 2, and purity 5 multiply to 30.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_PRODUCT = Fraction(30)


class BundleError(Exception):
    """One violated bundle invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> BundleError:
    return BundleError(invariant, parameters)


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


def _trace(matrix: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> Fraction:
    return matrix[0][0] + matrix[1][1]


def _determinant(matrix: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> Fraction:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def _purity(matrix: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> Fraction:
    square_00 = matrix[0][0] * matrix[0][0] + matrix[0][1] * matrix[1][0]
    square_11 = matrix[1][0] * matrix[0][1] + matrix[1][1] * matrix[1][1]
    return square_00 + square_11


def bundle_product() -> Fraction:
    """Return trace * determinant * purity of [[1, 1], [0, 2]]."""
    matrix = (
        (_require_fraction(1, "a"), _require_fraction(1, "b")),
        (_require_fraction(0, "c"), _require_fraction(2, "d")),
    )
    trace = _trace(matrix)
    determinant = _determinant(matrix)
    purity = _purity(matrix)
    if trace != 3 or determinant != 2 or purity != 5:
        raise _fail("bundle components drifted", trace=str(trace), determinant=str(determinant), purity=str(purity))
    return trace * determinant * purity


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the bundle product 30."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return _locked(bundle_product(), _PRODUCT, "bundle product drifted")


def main() -> int:
    value = bundle_product()
    print(value)
    if value == _PRODUCT:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
