"""Exact weighted L1 quotient seminorm certificate on Q^n / im(B).

Origin: dag/derivation_dag.json node L1-WDP-WINDOW-PHI1-GAMMA2, and
lean/DerivationDagQMClosure.lean theorem
l1_gs001_replica_and_phi1_quotient_invariance.
Claim: urn:omega:fqm:phi1:weighted-l1-quotient-certificate:v1
AuthorityEffect: None
Mutation-Kills: 9 non-equivalent source mutants, executed by code/python/tests/test_l1_seminorm.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 7; AST Sonar cognitive complexity max 6; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 7.
Scope Fence: This file does not claim that the weighted l1 form is derived
from MSS-0, does not compute Gamma2 or R_cl, does not select L1 over rival
seminorms, and does not inherit an authority grant from a passing certificate.

Phi1([omega]) is certified exactly when a primal residual
r = omega - B alpha and a dual witness z satisfy B^T z = 0, |z_i| <= w_i,
and sum_i w_i |r_i| = z · omega = the reported value. The scalar field is Q.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence


class L1SeminormError(ValueError):
    """One violated certificate invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object]) -> None:
        self.invariant = invariant
        self.parameters = dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _refuse(invariant: str, **parameters: object) -> L1SeminormError:
    return L1SeminormError(invariant, parameters)


def _require_sequence(values: object, role: str) -> Sequence[object]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise _refuse(
            "expected a finite sequence of exact rationals",
            role=role,
            received=type(values).__name__,
        )
    return values


def _pair_to_fraction(value: tuple[object, ...], role: str) -> Fraction:
    if len(value) != 2:
        raise _refuse("rational pair must have length 2", role=role, length=len(value))
    numer, denom = value
    if isinstance(numer, bool) or isinstance(denom, bool):
        raise _refuse("boolean refused inside a rational pair", role=role)
    if type(numer) is not int or type(denom) is not int:
        raise _refuse(
            "rational pair entries must be exact integers",
            role=role,
            numerator_type=type(numer).__name__,
            denominator_type=type(denom).__name__,
        )
    if denom == 0:
        raise _refuse("rational denominator is zero", role=role, numerator=numer)
    return Fraction(numer, denom)


def require_rational(value: object, role: str) -> Fraction:
    """Accept int or Fraction only. Float, bool, and other types are refused."""
    if isinstance(value, float):
        raise _refuse(
            "float refused at the public boundary",
            role=role,
            received=type(value).__name__,
        )
    if isinstance(value, bool):
        raise _refuse("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    if isinstance(value, tuple):
        return _pair_to_fraction(value, role)
    raise _refuse(
        "value is not an exact rational",
        role=role,
        received=type(value).__name__,
    )


def require_vector(values: object, role: str, length: int | None = None) -> tuple[Fraction, ...]:
    sequence = _require_sequence(values, role)
    parsed = tuple(require_rational(item, f"{role}[{index}]") for index, item in enumerate(sequence))
    if length is not None and len(parsed) != length:
        raise _refuse(
            "vector length does not match the declared coordinate count",
            role=role,
            expected=length,
            actual=len(parsed),
        )
    return parsed


def require_positive_weights(weights: object) -> tuple[Fraction, ...]:
    parsed = require_vector(weights, "weight")
    for index, weight in enumerate(parsed):
        if weight <= 0:
            raise _refuse(
                "Weight at index must be strictly positive",
                index=index,
                weight=str(weight),
            )
    return parsed


def _width(rows: Sequence[Sequence[Fraction]]) -> int:
    if not rows:
        return 0
    return len(rows[0])


def _coerce_matrix(rows: object, role: str) -> tuple[tuple[Fraction, ...], ...]:
    sequence = _require_sequence(rows, role)
    parsed: list[tuple[Fraction, ...]] = []
    for index, row in enumerate(sequence):
        if isinstance(row, (str, bytes)) or not isinstance(row, Sequence):
            raise _refuse("boundary row is not a vector", role=role, row=index)
        parsed.append(require_vector(row, f"{role}[{index}]"))
    return tuple(parsed)


def _require_matrix_shape(rows: Sequence[Sequence[Fraction]], height: int) -> None:
    if len(rows) != height:
        raise _refuse(
            "Boundary rows must match weights length",
            rows=len(rows),
            weights=height,
        )
    width = _width(rows)
    for index, row in enumerate(rows):
        if len(row) != width:
            raise _refuse(
                "Boundary matrix must be rectangular",
                row=index,
                expected_columns=width,
                actual_columns=len(row),
            )


def _row_equal(left: Sequence[Fraction], right: Sequence[Fraction]) -> bool:
    if len(left) != len(right):
        return False
    for item, other in zip(left, right):
        if item != other:
            return False
    return True


def _rows_equal(
    left: Sequence[Sequence[Fraction]],
    right: Sequence[Sequence[Fraction]],
) -> bool:
    if len(left) != len(right):
        return False
    for row, other in zip(left, right):
        if not _row_equal(row, other):
            return False
    return True


def _dot(left: Sequence[Fraction], right: Sequence[Fraction]) -> Fraction:
    total = Fraction(0)
    for item, other in zip(left, right):
        total += item * other
    return total


def _weighted_l1(weights: Sequence[Fraction], residual: Sequence[Fraction]) -> Fraction:
    total = Fraction(0)
    for weight, value in zip(weights, residual):
        total += weight * abs(value)
    return total


def _column_pairing(
    boundary: Sequence[Sequence[Fraction]],
    dual: Sequence[Fraction],
    column: int,
) -> Fraction:
    total = Fraction(0)
    for row_index, row in enumerate(boundary):
        total += row[column] * dual[row_index]
    return total


def _require_binding(
    rows: Sequence[Sequence[Fraction]],
    weights: Sequence[Fraction],
    presentation_rows: Sequence[Sequence[Fraction]],
    presentation_weights: Sequence[Fraction],
) -> None:
    if not _rows_equal(rows, presentation_rows):
        raise _refuse("Boundary binding mismatch", rows=len(rows), expected_rows=len(presentation_rows))
    if tuple(weights) != tuple(presentation_weights):
        raise _refuse("Weight binding mismatch", coordinates=len(weights))


def _require_alpha(alpha: Sequence[Fraction], width: int) -> None:
    if len(alpha) != width:
        raise _refuse("Alpha length does not match boundary columns", expected=width, actual=len(alpha))


def _require_primal(
    boundary: Sequence[Sequence[Fraction]],
    alpha: Sequence[Fraction],
    omega: Sequence[Fraction],
    residual: Sequence[Fraction],
) -> None:
    for index, row in enumerate(boundary):
        repair = _dot(row, alpha)
        expected = omega[index] - repair
        if residual[index] != expected:
            raise _refuse(
                "Primal residual mismatch",
                index=index,
                expected=str(expected),
                actual=str(residual[index]),
            )


def _require_dual_orthogonal(
    boundary: Sequence[Sequence[Fraction]],
    dual: Sequence[Fraction],
) -> None:
    for column in range(_width(boundary)):
        pairing = _column_pairing(boundary, dual, column)
        if pairing != 0:
            raise _refuse(
                "Dual witness not orthogonal to column",
                column=column,
                pairing=str(pairing),
            )


def _require_dual_box(dual: Sequence[Fraction], weights: Sequence[Fraction]) -> None:
    for index, witness in enumerate(dual):
        if abs(witness) > weights[index]:
            raise _refuse(
                "dual witness bound violated",
                index=index,
                abs_witness=str(abs(witness)),
                weight=str(weights[index]),
            )


def _require_optimality(primal: Fraction, dual: Fraction, reported: Fraction) -> None:
    if primal != dual or reported != primal:
        raise _refuse(
            "Duality gap not closed",
            primal=str(primal),
            dual=str(dual),
            reported=str(reported),
        )


@dataclass(frozen=True)
class ExactPhi1Certificate:
    """Submitted primal-dual witness. Fields stay public so a caller can build a refusal case."""

    omega: list[Fraction]
    d0: list[list[Fraction]]
    weights: list[Fraction]
    alpha: list[Fraction]
    primal_residual: list[Fraction]
    dual_witness: list[Fraction]
    reported_value: Fraction


@dataclass(frozen=True)
class VerifiedExactPhi1:
    certificate: ExactPhi1Certificate

    @property
    def value(self) -> Fraction:
        return self.certificate.reported_value

    @property
    def d0(self) -> list[list[Fraction]]:
        return self.certificate.d0

    @property
    def weights(self) -> list[Fraction]:
        return self.certificate.weights


class L1Seminorm:
    """Immutable presentation of positive weights and a rational boundary matrix."""

    def __init__(
        self,
        boundary: Sequence[Sequence[object]],
        weights: Sequence[object],
    ) -> None:
        parsed_weights = require_positive_weights(weights)
        parsed_boundary = _coerce_matrix(boundary, "boundary")
        _require_matrix_shape(parsed_boundary, len(parsed_weights))
        self._boundary = parsed_boundary
        self._weights = parsed_weights

    @property
    def boundary(self) -> list[list[Fraction]]:
        return [list(row) for row in self._boundary]

    @property
    def weights(self) -> list[Fraction]:
        return list(self._weights)

    def verify_certificate(self, cert: ExactPhi1Certificate) -> VerifiedExactPhi1:
        count = len(self._weights)
        omega = require_vector(cert.omega, "omega", count)
        residual = require_vector(cert.primal_residual, "primal_residual", count)
        dual = require_vector(cert.dual_witness, "dual_witness", count)
        weights = require_positive_weights(cert.weights)
        rows = _coerce_matrix(cert.d0, "d0")
        _require_matrix_shape(rows, count)
        alpha = require_vector(cert.alpha, "alpha")
        _require_alpha(alpha, _width(self._boundary))
        reported = require_rational(cert.reported_value, "reported_value")
        _require_binding(rows, weights, self._boundary, self._weights)
        _require_primal(self._boundary, alpha, omega, residual)
        _require_dual_orthogonal(self._boundary, dual)
        _require_dual_box(dual, self._weights)
        primal = _weighted_l1(self._weights, residual)
        paired = _dot(dual, omega)
        _require_optimality(primal, paired, reported)
        return VerifiedExactPhi1(cert)


def evaluate_weighted_l1_quotient(
    boundary: Sequence[Sequence[object]],
    weights: Sequence[object],
    omega: Sequence[object],
    alpha: Sequence[object],
    primal_residual: Sequence[object],
    dual_witness: Sequence[object],
    reported_value: object,
) -> Fraction:
    """Outermost public contract: exact Phi1, or a typed L1SeminormError."""
    presentation = L1Seminorm(boundary, weights)
    certificate = ExactPhi1Certificate(
        omega=list(require_vector(omega, "omega")),
        d0=[list(row) for row in _coerce_matrix(boundary, "boundary")],
        weights=list(require_positive_weights(weights)),
        alpha=list(require_vector(alpha, "alpha")),
        primal_residual=list(require_vector(primal_residual, "primal_residual")),
        dual_witness=list(require_vector(dual_witness, "dual_witness")),
        reported_value=require_rational(reported_value, "reported_value"),
    )
    return presentation.verify_certificate(certificate).value


__all__ = [
    "ExactPhi1Certificate",
    "L1Seminorm",
    "L1SeminormError",
    "VerifiedExactPhi1",
    "evaluate_weighted_l1_quotient",
    "require_positive_weights",
    "require_rational",
    "require_vector",
]
