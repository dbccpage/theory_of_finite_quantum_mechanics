"""Exact solver for finite-cochain obstruction classification."""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from hashlib import sha256
import json
from typing import Iterable, Sequence, Tuple


try:
    from .finite_cochain_complex import (
        COEFFICIENT_DOMAIN,
        FiniteCochainComplex,
        Matrix,
        Scalar,
        Vector,
    )
except ImportError:
    from finite_cochain_complex import (
        COEFFICIENT_DOMAIN,
        FiniteCochainComplex,
        Matrix,
        Scalar,
        Vector,
    )

class Verdict(str, Enum):
    """Exhaustive outcomes for a supplied finite C1 cochain."""

    INVALID_COMPLEX = "invalid_complex"
    CURVATURE = "curvature"
    EXACT_REPAIR = "exact_repair"
    CLOSED_RESIDUAL = "closed_residual"


def _scalar(value: int | str | Fraction) -> Scalar:
    if isinstance(value, bool) or isinstance(value, float):
        raise TypeError(
            "use integers, strings, or Fraction; floating point is forbidden"
        )
    if not isinstance(value, (int, str, Fraction)):
        raise TypeError(f"unsupported exact scalar: {type(value).__name__}")
    return Fraction(value)


def _vector(
    values: Iterable[int | str | Fraction], expected: int, label: str
) -> Vector:
    result = tuple(_scalar(value) for value in values)
    if len(result) != expected:
        raise ValueError(f"{label} has length {len(result)}; expected {expected}")
    return result


def _matrix(
    rows: Iterable[Iterable[int | str | Fraction]],
    row_count: int,
    column_count: int,
    label: str,
) -> Matrix:
    result = tuple(
        _vector(row, column_count, f"{label}[{index}]")
        for index, row in enumerate(rows)
    )
    if len(result) != row_count:
        raise ValueError(f"{label} has {len(result)} rows; expected {row_count}")
    return result


def _matvec(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(
        sum(
            (coefficient * value for coefficient, value in zip(row, vector)),
            Fraction(0),
        )
        for row in matrix
    )


def _matmul(left: Matrix, right: Matrix, inner_dimension: int) -> Matrix:
    if not left:
        return ()
    right_columns = len(right[0]) if right else 0
    return tuple(
        tuple(
            sum(
                (left[row][k] * right[k][column] for k in range(inner_dimension)),
                Fraction(0),
            )
            for column in range(right_columns)
        )
        for row in range(len(left))
    )


def _transpose(matrix: Matrix, row_count: int, column_count: int) -> Matrix:
    """Transpose a matrix while retaining empty-dimension shape information."""

    return tuple(
        tuple(matrix[row][column] for row in range(row_count))
        for column in range(column_count)
    )


def _dot(left: Vector, right: Vector) -> Scalar:
    return sum(
        (left_value * right_value for left_value, right_value in zip(left, right)),
        Fraction(0),
    )


def _is_zero(values: Iterable[Scalar]) -> bool:
    return all(value == 0 for value in values)


def _solve_exact(matrix: Matrix, rhs: Vector, variable_count: int) -> Vector | None:
    """Solve matrix @ x = rhs over Q, choosing all free variables as zero."""

    equation_count = len(rhs)
    if equation_count == 0:
        return tuple(Fraction(0) for _ in range(variable_count))

    augmented = [list(matrix[row]) + [rhs[row]] for row in range(equation_count)]
    pivot_columns: list[int] = []
    pivot_row = 0

    for column in range(variable_count):
        candidate = next(
            (
                row
                for row in range(pivot_row, equation_count)
                if augmented[row][column] != 0
            ),
            None,
        )
        if candidate is None:
            continue

        augmented[pivot_row], augmented[candidate] = (
            augmented[candidate],
            augmented[pivot_row],
        )
        pivot = augmented[pivot_row][column]
        augmented[pivot_row] = [value / pivot for value in augmented[pivot_row]]

        for row in range(equation_count):
            if row == pivot_row:
                continue
            factor = augmented[row][column]
            if factor != 0:
                augmented[row] = [
                    value - factor * pivot_value
                    for value, pivot_value in zip(augmented[row], augmented[pivot_row])
                ]

        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == equation_count:
            break

    for row in augmented:
        if _is_zero(row[:variable_count]) and row[variable_count] != 0:
            return None

    solution = [Fraction(0) for _ in range(variable_count)]
    for row, column in enumerate(pivot_columns):
        solution[column] = augmented[row][variable_count]
    return tuple(solution)


def _fraction_text(value: Scalar) -> str:
    return f"{value.numerator}/{value.denominator}"


def _encoded_vector(vector: Vector | None) -> list[str] | None:
    if vector is None:
        return None
    return [_fraction_text(value) for value in vector]


def _encoded_matrix(matrix: Matrix) -> list[list[str]]:
    return [[_fraction_text(value) for value in row] for row in matrix]


@dataclass(frozen=True)
class CochainAnalysis:
    """A deterministic, evidence-only result; never an authority certificate."""

    verdict: Verdict
    beta: Vector
    complex_defect: Matrix
    closure_defect: Vector
    primitive_witness: Vector | None
    residual_representative: Vector | None
    period_witness: Vector | None
    period_boundary_defect: Vector | None
    period_pairing: Scalar | None
    period_is_boundary: bool | None
    coefficient_domain: str
    evidence_sha256: str
    authority_effect: str = "None"


def analyze_finite_cochain(
    complex_: FiniteCochainComplex,
    beta: Sequence[int | str | Fraction],
) -> CochainAnalysis:
    """Classify beta and bind the complete exact computation to SHA-256."""

    checked_beta = _vector(beta, complex_.c1_dimension, "beta")
    complex_defect = complex_.complex_defect()
    closure_defect = _matvec(complex_.d1, checked_beta)
    primitive_witness = _solve_exact(complex_.d0, checked_beta, complex_.c0_dimension)
    residual_representative: Vector | None = None
    period_witness: Vector | None = None
    period_boundary_defect: Vector | None = None
    period_pairing: Scalar | None = None
    period_is_boundary: bool | None = None

    if any(not _is_zero(row) for row in complex_defect):
        verdict = Verdict.INVALID_COMPLEX
    elif not _is_zero(closure_defect):
        if primitive_witness is not None:
            raise AssertionError("valid complex produced a nonclosed exact cochain")
        verdict = Verdict.CURVATURE
    else:
        if primitive_witness is not None:
            if _matvec(complex_.d0, primitive_witness) != checked_beta:
                raise AssertionError(
                    "internal exact solver produced an invalid witness"
                )
            verdict = Verdict.EXACT_REPAIR
        else:
            verdict = Verdict.CLOSED_RESIDUAL
            residual_representative = checked_beta
            boundary1 = _transpose(
                complex_.d0, complex_.c1_dimension, complex_.c0_dimension
            )
            period_constraints = boundary1 + (checked_beta,)
            period_rhs = tuple(Fraction(0) for _ in range(complex_.c0_dimension)) + (
                Fraction(1),
            )
            period_witness = _solve_exact(
                period_constraints, period_rhs, complex_.c1_dimension
            )
            if period_witness is None:
                raise AssertionError(
                    "closed nonexact cochain has no dual period witness"
                )
            period_boundary_defect = _matvec(boundary1, period_witness)
            period_pairing = _dot(checked_beta, period_witness)
            boundary2 = _transpose(
                complex_.d1, complex_.c2_dimension, complex_.c1_dimension
            )
            period_is_boundary = (
                _solve_exact(boundary2, period_witness, complex_.c2_dimension)
                is not None
            )
            if not _is_zero(period_boundary_defect):
                raise AssertionError("period witness is not a 1-cycle")
            if period_pairing == 0:
                raise AssertionError("period witness has zero pairing")
            if period_is_boundary:
                raise AssertionError("period witness is a 2-boundary")

    payload = {
        "authority_effect": "None",
        "beta": _encoded_vector(checked_beta),
        "coefficient_domain": COEFFICIENT_DOMAIN,
        "closure_defect": _encoded_vector(closure_defect),
        "complex_defect": _encoded_matrix(complex_defect),
        "d0": _encoded_matrix(complex_.d0),
        "d1": _encoded_matrix(complex_.d1),
        "dimensions": [
            complex_.c0_dimension,
            complex_.c1_dimension,
            complex_.c2_dimension,
        ],
        "primitive_witness": _encoded_vector(primitive_witness),
        "residual_representative": _encoded_vector(residual_representative),
        "period_witness": _encoded_vector(period_witness),
        "period_boundary_defect": _encoded_vector(period_boundary_defect),
        "period_pairing": None
        if period_pairing is None
        else _fraction_text(period_pairing),
        "period_is_boundary": period_is_boundary,
        "verdict": verdict.value,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    evidence_sha256 = sha256(canonical).hexdigest()

    return CochainAnalysis(
        verdict=verdict,
        beta=checked_beta,
        complex_defect=complex_defect,
        closure_defect=closure_defect,
        primitive_witness=primitive_witness,
        residual_representative=residual_representative,
        period_witness=period_witness,
        period_boundary_defect=period_boundary_defect,
        period_pairing=period_pairing,
        period_is_boundary=period_is_boundary,
        coefficient_domain=COEFFICIENT_DOMAIN,
        evidence_sha256=evidence_sha256,
    )


solve_finite_cochain_obstruction = analyze_finite_cochain


def self_check() -> None:
    filled = FiniteCochainComplex.from_rows(
        (3, 3, 1),
        ((-1, 1, 0), (0, -1, 1), (-1, 0, 1)),
        ((1, 1, -1),),
    )
    assert analyze_finite_cochain(filled, (1, 2, 3)).verdict is Verdict.EXACT_REPAIR
    assert analyze_finite_cochain(filled, (1, 2, 4)).verdict is Verdict.CURVATURE


__all__ = [
    "CochainAnalysis",
    "Verdict",
    "analyze_finite_cochain",
    "self_check",
    "solve_finite_cochain_obstruction",
]
