"""Rational Householder involution and Gaussian conjugation certificate.

Origin: lean4/DerivationDagQMClosure.lean theorem
ds_qm062_u1_selector_layers_and_ring_iso, whose first layer is the
conjugation involution S^2 = I_2.
Claim: urn:omega:fqm:involution:householder-and-conjugation:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_involution.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 5; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: This file does not prove the U(1) selector ring isomorphism,
does not claim that diag(1, -1) is the only rational involution, and does
not order Q(i).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence

from .matrix import ExactMatrix
from .scalars import GaussianRational, Q, q


class InvolutionError(ValueError):
    """One violated involution invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> InvolutionError:
    return InvolutionError(invariant, parameters)


def require_rational(value: object, role: str) -> Fraction:
    """Accept int or Fraction only. Float, bool, and Q(i) are refused."""
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, GaussianRational):
        raise _fail("Q(i) is outside the Householder carrier", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def _require_vector(values: object) -> tuple[Fraction, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence) or len(values) == 0:
        raise _fail(
            "Householder vector must be a nonempty sequence",
            role="vector",
            received=type(values).__name__,
        )
    return tuple(require_rational(item, f"vector[{index}]") for index, item in enumerate(values))


def _norm_sq(coords: Sequence[Fraction]) -> Fraction:
    total = Fraction(0)
    for coord in coords:
        total += coord * coord
    return total


def _require_nonzero(norm_sq: Fraction) -> Fraction:
    if norm_sq == 0:
        raise _fail("Householder vector must be nonzero", norm_sq=str(norm_sq))
    return norm_sq


def _entry(coords: Sequence[Fraction], norm_sq: Fraction, row: int, column: int) -> Fraction:
    diagonal = Fraction(1) if row == column else Fraction(0)
    return diagonal - Fraction(2) * coords[row] * coords[column] / norm_sq


def _reflect(coords: Sequence[Fraction], norm_sq: Fraction) -> ExactMatrix:
    data: list[Fraction] = []
    width = len(coords)
    for row in range(width):
        for column in range(width):
            data.append(_entry(coords, norm_sq, row, column))
    return ExactMatrix(width, width, data)


def require_involution(matrix: ExactMatrix) -> ExactMatrix:
    """Accept the matrix only when it is square and squares to the identity."""
    if matrix.rows != matrix.cols:
        raise _fail("involution matrix must be square", rows=matrix.rows, cols=matrix.cols)
    identity = ExactMatrix.identity(matrix.rows)
    if matrix * matrix != identity:
        raise _fail("matrix is not an involution", rows=matrix.rows)
    return matrix


@dataclass(frozen=True)
class HouseholderCertificate:
    """Witness that I - 2 vv^T / (v·v) squares to the identity."""

    coords: tuple[Fraction, ...]
    norm_sq: Fraction
    matrix: ExactMatrix


def certify_householder(vector: object) -> HouseholderCertificate:
    coords = _require_vector(vector)
    norm_sq = _require_nonzero(_norm_sq(coords))
    matrix = require_involution(_reflect(coords, norm_sq))
    return HouseholderCertificate(coords, norm_sq, matrix)


def householder(vector: object) -> ExactMatrix:
    """Return I - 2 vv^T / (v·v) for a nonzero rational vector."""
    return certify_householder(vector).matrix


@dataclass(frozen=True)
class ConjugationCertificate:
    """Witness that conjugating a Gaussian rational twice restores it."""

    value: GaussianRational
    conjugate: GaussianRational
    twice: GaussianRational


def certify_conjugation(real: object, imag: object) -> ConjugationCertificate:
    value = GaussianRational(require_rational(real, "real"), require_rational(imag, "imag"))
    once = value.conjugate()
    twice = once.conjugate()
    if twice != value:
        raise _fail("conjugation failed to be an involution", real=str(value.real), imag=str(value.imag))
    return ConjugationCertificate(value, once, twice)


def conjugation_square(real: object, imag: object) -> GaussianRational:
    """Conjugate twice and return the original Gaussian rational."""
    return certify_conjugation(real, imag).value


__all__ = [
    "ExactMatrix",
    "GaussianRational",
    "Q",
    "q",
    "InvolutionError",
    "HouseholderCertificate",
    "ConjugationCertificate",
    "require_rational",
    "require_involution",
    "certify_householder",
    "householder",
    "certify_conjugation",
    "conjugation_square",
]
