"""Moore–Penrose pseudoinverse over Q from a full-rank factorization.

Origin: papers/derivations/mub6/artifacts/knowledge/category_moore_penrose_least_squares_annihilation.md
formula R = (J^T J)^{-1} J^T, and papers/derivations/mub6/mub6.md, which
records that a Moore–Penrose preconditioner is not defined for the rank-184
Jacobian.
Claim: urn:omega:fqm:linear-algebra:moore-penrose:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_pseudoinverse.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: moore_penrose checks the four Penrose identities on the rational
matrix it is given. When that matrix has full column rank, the result is also
checked against (A^T A)^{-1} A^T. This file does not build a preconditioner
for the mub6 Jacobian, does not prove the Krawczyk obstruction, and does not
admit floats or Q(i).
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping, Sequence

from .matrix import ExactMatrix, MatrixError
from .scalars import GaussianRational


class PseudoinverseError(MatrixError):
    """One violated pseudoinverse invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> PseudoinverseError:
    return PseudoinverseError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _require_entry(value: object, role: str) -> Fraction:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a rational entry was required", role=role)
    if isinstance(value, GaussianRational):
        raise _fail("Gaussian rational refused; pseudoinverse in this module is over Q", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("matrix entry is not an exact rational", role=role, received=type(value).__name__)


def _require_dimension(value: object, role: str) -> int:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a matrix dimension was required", role=role)
    if type(value) is int:
        if value < 0:
            raise _fail("matrix shape is negative", role=role, received=value)
        return value
    raise _fail("matrix shape is not an integer", role=role, received=type(value).__name__)


def _require_shape(rows: object, cols: object) -> tuple[int, int]:
    return _require_dimension(rows, "rows"), _require_dimension(cols, "cols")


def _require_data_length(matrix: ExactMatrix, rows: int, cols: int) -> None:
    length = len(matrix.data)
    if length != rows * cols:
        raise _fail("matrix data length does not match the shape", length=length, rows=rows, cols=cols)


def _rational_matrix(matrix: object) -> ExactMatrix:
    if not isinstance(matrix, ExactMatrix):
        raise _fail("pseudoinverse input is not an ExactMatrix", received=type(matrix).__name__)
    rows, cols = _require_shape(matrix.rows, matrix.cols)
    _require_data_length(matrix, rows, cols)
    data = [_require_entry(value, f"entry[{index}]") for index, value in enumerate(matrix.data)]
    return ExactMatrix(rows, cols, data)


def _factor_f(source: ExactMatrix, pivots: Sequence[int]) -> ExactMatrix:
    data: list[Fraction] = []
    for row in range(source.rows):
        for pivot in pivots:
            data.append(_require_entry(source.get(row, pivot), "pivot-column"))
    return ExactMatrix(source.rows, len(pivots), data)


def _factor_g(reduced: ExactMatrix, rank: int) -> ExactMatrix:
    data: list[Fraction] = []
    for row in range(rank):
        for col in range(reduced.cols):
            data.append(_require_entry(reduced.get(row, col), "coordinate"))
    return ExactMatrix(rank, reduced.cols, data)


def _require_factorization(source: ExactMatrix, image: ExactMatrix, coordinates: ExactMatrix) -> None:
    if image * coordinates != source:
        raise _fail(
            "pivot columns do not rebuild the matrix",
            rows=source.rows,
            cols=source.cols,
            rank=image.cols,
        )


def _require_inverse(gram: ExactMatrix, role: str) -> ExactMatrix:
    try:
        return gram.inverse()
    except ValueError as exc:
        raise _fail("a full-rank Gram matrix was singular", role=role, rows=gram.rows) from exc


def _pseudo_from_factors(image: ExactMatrix, coordinates: ExactMatrix) -> ExactMatrix:
    inverse_f = _require_inverse(image.transpose() * image, "F^T F")
    inverse_g = _require_inverse(coordinates * coordinates.transpose(), "G G^T")
    return coordinates.transpose() * inverse_g * inverse_f * image.transpose()


def _require_triple(source: ExactMatrix, pseudo: ExactMatrix) -> None:
    if source * pseudo * source != source:
        raise _fail("Penrose identity A A+ A = A failed", rows=source.rows, cols=source.cols)


def _require_reflexive(source: ExactMatrix, pseudo: ExactMatrix) -> None:
    if pseudo * source * pseudo != pseudo:
        raise _fail("Penrose identity A+ A A+ = A+ failed", rows=pseudo.rows, cols=pseudo.cols)


def _require_symmetric(projector: ExactMatrix, role: str) -> None:
    if projector.transpose() != projector:
        raise _fail("a Penrose projector was not symmetric", role=role)


def _left_inverse(source: ExactMatrix) -> ExactMatrix:
    gram = source.transpose() * source
    return _require_inverse(gram, "A^T A") * source.transpose()


def _require_column_formula(source: ExactMatrix, pseudo: ExactMatrix, rank: int) -> None:
    if rank != source.cols:
        return
    cited = _left_inverse(source)
    if pseudo != cited:
        raise _fail("full column rank result is not (A^T A)^{-1} A^T", rows=source.rows, cols=source.cols)


def moore_penrose(matrix: ExactMatrix) -> ExactMatrix:
    """Return A+ in Q^{n×m} for A in Q^{m×n}, after the Penrose checks."""
    source = _rational_matrix(matrix)
    reduced, pivots = source.rref()
    image = _factor_f(source, pivots)
    coordinates = _factor_g(reduced, len(pivots))
    _require_factorization(source, image, coordinates)
    pseudo = _pseudo_from_factors(image, coordinates)
    _require_triple(source, pseudo)
    _require_reflexive(source, pseudo)
    _require_symmetric(source * pseudo, "A A+")
    _require_symmetric(pseudo * source, "A+ A")
    _require_column_formula(source, pseudo, len(pivots))
    return pseudo


__all__ = [
    "ExactMatrix",
    "GaussianRational",
    "MatrixError",
    "PseudoinverseError",
    "moore_penrose",
]
