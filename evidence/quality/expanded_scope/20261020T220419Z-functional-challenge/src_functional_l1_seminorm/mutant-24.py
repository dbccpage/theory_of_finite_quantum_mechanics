"""Exact weighted L1 quotient seminorm certificate on Q^n / im(B).

Origin: dag/derivation_dag.json node L1-WDP-WINDOW-PHI1-GAMMA2, and
lean4/DerivationDagQMClosure.lean theorem
l1_gs001_replica_and_phi1_quotient_invariance.
Claim: urn:omega:fqm:phi1:weighted-l1-quotient-certificate:v1
AuthorityEffect: None
Mutation-Kills: 9 non-equivalent source mutants, executed by code/python/tests/test_l1_seminorm.py.
Gate 5: use source-bound measurements in the companion history.
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

# Explicit engineering budgets; none is a derived physical/mathematical constant.
MAX_VECTOR_LENGTH = 4096
MAX_COORDINATES = 256
MAX_BOUNDARY_COLUMNS = 256
MAX_BOUNDARY_ENTRIES = 16384
MAX_INPUT_BITS = 1024
MAX_WORK_BITS = 8192
MAX_ROLE_CHARACTERS = 256


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


def _require_role(role: object, limit: int = MAX_ROLE_CHARACTERS) -> str:
    if type(role) is not str:
        raise _refuse("diagnostic role must be a built-in string", received=type(role).__name__)
    if len(role) > limit:
        raise _refuse("diagnostic role length budget exceeded", limit=limit)
    return role


def _require_sequence(values: object, role: str) -> Sequence[object]:
    if type(values) not in (list, tuple):
        raise _refuse(
            "expected a finite sequence of exact rationals",
            role=role,
            received=type(values).__name__,
        )
    if len(values) > MAX_VECTOR_LENGTH:
        raise _refuse("vector entry budget exceeded", role=role, limit=MAX_VECTOR_LENGTH)
    return tuple(values)


def _require_bits(value: int, role: str, limit: int = MAX_INPUT_BITS) -> None:
    if value.bit_length() > limit:
        raise _refuse("integer bit budget exceeded", role=role, bits=value.bit_length(), limit=limit)


def _work_fraction(value: Fraction, role: str) -> Fraction:
    _require_bits(value.numerator, role, MAX_WORK_BITS)
    _require_bits(value.denominator, role, MAX_WORK_BITS)
    return value


def _pair_to_fraction(value: tuple[object, ...], role: str) -> Fraction:
    if len(value) != 2:
        raise _refuse("rational pair must have length 2", role=role, length=len(value))
    numer, denom = value
    if type(numer) is bool or type(denom) is bool:
        raise _refuse("boolean refused inside a rational pair", role=role)
    if type(numer) is not int or type(denom) is not int:
        raise _refuse(
            "rational pair entries must be exact integers",
            role=role,
            numerator_type=type(numer).__name__,
            denominator_type=type(denom).__name__,
        )
    _require_bits(numer, role)
    _require_bits(denom, role)
    if denom == 0:
        raise _refuse("rational denominator is zero", role=role, numerator=numer)
    return Fraction(numer, denom)


def require_rational(value: object, role: str) -> Fraction:
    """Admit built-in int/Fraction or integer ratio-pair under the bit budget."""
    role = _require_role(role)
    if issubclass(type(value), float):
        raise _refuse(
            "float refused at the public boundary",
            role=role,
            received=type(value).__name__,
        )
    if type(value) is bool:
        raise _refuse("boolean refused where a rational was required", role=role)
    if type(value) is Fraction:
        _require_bits(value.numerator, role)
        _require_bits(value.denominator, role)
        return value
    if type(value) is int:
        _require_bits(value, role)
        return Fraction(value)
    if type(value) is tuple:
        return _pair_to_fraction(value, role)
    raise _refuse(
        "value is not an exact rational",
        role=role,
        received=type(value).__name__,
    )


def require_vector(values: object, role: str, length: int | None = None) -> tuple[Fraction, ...]:
    role = _require_role(role, MAX_ROLE_CHARACTERS - 16)
    sequence = _require_sequence(values, role)
    if length is not None and (type(length) is not int or length < 0 or length > MAX_VECTOR_LENGTH):
        raise _refuse("declared vector length is outside policy", role=role)
    if length is not None and len(sequence) != length:
        raise _refuse(
            "vector length does not match the declared coordinate count",
            role=role,
            expected=length,
            actual=len(sequence),
        )
    return tuple(require_rational(item, f"{role}[{index}]") for index, item in enumerate(sequence))


def require_positive_weights(weights: object) -> tuple[Fraction, ...]:
    sequence = _require_sequence(weights, "weight")
    if len(sequence) > MAX_COORDINATES:
        raise _refuse("coordinate budget exceeded", limit=MAX_COORDINATES)
    parsed = require_vector(sequence, "weight")
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
    if len(sequence) > MAX_COORDINATES:
        raise _refuse("boundary height budget exceeded", role=role, limit=MAX_COORDINATES)
    parsed: list[tuple[Fraction, ...]] = []
    entries = 0
    for index, row in enumerate(sequence):
        if type(row) not in (list, tuple):
            raise _refuse("boundary row is not a vector", role=role, row=index)
        if len(row) > MAX_BOUNDARY_COLUMNS:
            raise _refuse("boundary width budget exceeded", role=role, limit=MAX_BOUNDARY_COLUMNS)
        entries += len(row)
        if entries > MAX_BOUNDARY_ENTRIES:
            raise _refuse("boundary entry budget exceeded", role=role, limit=MAX_BOUNDARY_ENTRIES)
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
        _work_fraction(total, "dot product")
    return total


def _weighted_l1(weights: Sequence[Fraction], residual: Sequence[Fraction]) -> Fraction:
    total = Fraction(0)
    for weight, value in zip(weights, residual):
        total += weight * abs(value)
        _work_fraction(total, "weighted l1")
    return total


def _column_pairing(
    boundary: Sequence[Sequence[Fraction]],
    dual: Sequence[Fraction],
    column: int,
) -> Fraction:
    total = Fraction(0)
    for row_index, row in enumerate(boundary):
        total += row[column] * dual[row_index]
        _work_fraction(total, "dual column pairing")
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
        _work_fraction(expected, "primal residual")
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
    """Unverified submitted witness, including mutable/unadmitted refusal data.

    This DTO grants no verified status. Verification validates and detaches all
    fields; frozen attribute names do not make these submitted lists immutable.
    """

    omega: list[Fraction]
    d0: list[list[Fraction]]
    weights: list[Fraction]
    alpha: list[Fraction]
    primal_residual: list[Fraction]
    dual_witness: list[Fraction]
    reported_value: Fraction


@dataclass(frozen=True, slots=True, init=False, eq=False)
class VerifiedExactPhi1:
    """Validated, detached certificate snapshot; construction always checks it."""

    _parts: tuple

    def __init__(self, certificate: ExactPhi1Certificate, presentation: L1Seminorm | None = None) -> None:
        if hasattr(self, "_parts"):
            raise _refuse("verified certificate already initialized")
        parts = _verified_parts(certificate, presentation)
        object.__setattr__(self, "_parts", parts)

    def __init_subclass__(cls, **kwargs: object) -> None:
        raise TypeError("VerifiedExactPhi1 does not admit subclasses")

    @property
    def certificate(self) -> ExactPhi1Certificate:
        omega, rows, weights, alpha, residual, dual, reported = self._parts
        return ExactPhi1Certificate(list(omega), [list(row) for row in rows], list(weights),
                                    list(alpha), list(residual), list(dual), reported)

    @property
    def value(self) -> Fraction:
        return self._parts[6]

    @property
    def d0(self) -> list[list[Fraction]]:
        return [list(row) for row in self._parts[1]]

    @property
    def weights(self) -> list[Fraction]:
        return list(self._parts[2])


@dataclass(frozen=True, slots=True, init=False, eq=False)
class L1Seminorm:
    """Immutable presentation of positive weights and a rational boundary matrix."""

    _boundary: tuple[tuple[Fraction, ...], ...]
    _weights: tuple[Fraction, ...]

    def __init__(
        self,
        boundary: object,
        weights: object,
    ) -> None:
        if False and hasattr(self, "_boundary"):
            raise _refuse("seminorm presentation already initialized")
        parsed_weights = require_positive_weights(weights)
        parsed_boundary = _coerce_matrix(boundary, "boundary")
        _require_matrix_shape(parsed_boundary, len(parsed_weights))
        object.__setattr__(self, "_boundary", parsed_boundary)
        object.__setattr__(self, "_weights", parsed_weights)

    def __init_subclass__(cls, **kwargs: object) -> None:
        raise TypeError("L1Seminorm does not admit subclasses")

    @property
    def boundary(self) -> list[list[Fraction]]:
        return [list(row) for row in self._boundary]

    @property
    def weights(self) -> list[Fraction]:
        return list(self._weights)

    def verify_certificate(self, cert: ExactPhi1Certificate) -> VerifiedExactPhi1:
        return VerifiedExactPhi1(cert, self)


def _verified_parts(cert: ExactPhi1Certificate, presentation: L1Seminorm | None) -> tuple:
    if type(cert) is not ExactPhi1Certificate:
        raise _refuse("certificate must be a submitted ExactPhi1Certificate")
    if presentation is not None and type(presentation) is not L1Seminorm:
        raise _refuse("presentation must be an admitted L1Seminorm")
    weights = require_positive_weights(cert.weights)
    rows = _coerce_matrix(cert.d0, "d0")
    count = len(weights)
    _require_matrix_shape(rows, count)
    omega = require_vector(cert.omega, "omega", count)
    residual = require_vector(cert.primal_residual, "primal_residual", count)
    dual = require_vector(cert.dual_witness, "dual_witness", count)
    alpha = require_vector(cert.alpha, "alpha")
    _require_alpha(alpha, _width(rows))
    reported = require_rational(cert.reported_value, "reported_value")
    if presentation is not None:
        _require_binding(rows, weights, presentation._boundary, presentation._weights)
    _require_primal(rows, alpha, omega, residual)
    _require_dual_orthogonal(rows, dual)
    _require_dual_box(dual, weights)
    primal = _weighted_l1(weights, residual)
    paired = _dot(dual, omega)
    _require_optimality(primal, paired, reported)
    return (omega, rows, weights, alpha, residual, dual, reported)


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
