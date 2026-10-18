"""Exact density arithmetic in five launch fields.

Origin: code/rust/src/linear_algebra/cyclo_density.rs, which states independent
quotient-field density arithmetic with no floating-point predicate and no
splitting or dependence certificate.
Claim: urn:omega:fqm:linear-algebra:cyclotomic-density:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_cyclo_density.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 8; AST Sonar cognitive complexity max 7; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 8.
Scope Fence: The ordered embedding is frozen, not inferred numerically.
Characteristic polynomials and purity are exact. This file does not claim a
splitting field, multiplicative dependence, or a float embedding.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping, Sequence, cast

from . import entropy_dichotomy as kernel


# Ascending coefficients, including the monic leading coefficient.
MODULI = {1: (-1, 1), 3: (1, 1, 1), 4: (1, 0, 1),
          5: (1, 1, 1, 1, 1), 8: (1, 0, 0, 0, 1)}
ROOT_ISOLATION = "EXACT_CYCLOTOMIC_REAL_STURM_SPECTRAL_CLUSTERS"
_REAL_ENDPOINTS = {0: ["1/1", "1/1"], 2: ["7/5", "3/2"], 5: ["11/5", "12/5"]}


class CyclotomicError(ValueError):
    """One violated cyclotomic invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


class CyclotomicDivisionByZero(CyclotomicError, ZeroDivisionError):
    """Division by a zero cyclotomic element."""


def _fail(invariant: str, **parameters: object) -> CyclotomicError:
    return CyclotomicError(invariant, parameters)


def _division(invariant: str, **parameters: object) -> CyclotomicDivisionByZero:
    return CyclotomicDivisionByZero(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _reject_bool(value: object, role: str, invariant: str) -> None:
    if type(value) is bool:
        raise _fail(invariant, role=role)


def _scan(value: object, role: str) -> None:
    _refuse_float(value, role)
    if isinstance(value, dict):
        for item in value.values():
            _scan(item, role)
        return
    if isinstance(value, (list, tuple)):
        for item in value:
            _scan(item, role)


def _conductor(value: object) -> int:
    _refuse_float(value, "conductor")
    _reject_bool(value, "conductor", "boolean refused where a cyclotomic conductor was required")
    if isinstance(value, int) and value in MODULI:
        return value
    received = type(value).__name__
    raise _fail("unsupported cyclotomic conductor", received=received)


def _exact_rational(value: object, role: str, invariant: str) -> Q:
    _refuse_float(value, role)
    _reject_bool(value, role, "boolean refused where an exact rational was required")
    if isinstance(value, Q):
        return value
    if isinstance(value, int):
        return Q(value)
    raise _fail(invariant, role=role, received=type(value).__name__)


def _coefficients(values: object, count: int) -> tuple[Q, ...]:
    if isinstance(values, tuple) and len(values) == count:
        return tuple(
            _exact_rational(item, "coefficient", "cyclotomic arithmetic requires exact rational coefficients")
            for item in values
        )
    received = len(values) if isinstance(values, tuple) else type(values).__name__
    raise _fail("cyclotomic coefficient arity differs from phi(conductor)", received=received)


def _exponent(value: object) -> int:
    _refuse_float(value, "exponent")
    _reject_bool(value, "exponent", "boolean refused where an exact integer was required")
    if isinstance(value, int):
        return value
    raise _fail("cyclotomic exponent must be an integer", received=type(value).__name__)


def _basis_vector(conductor: int, degree: int, column: int) -> Cyclotomic:
    return Cyclotomic(conductor, tuple(Q(i == column) for i in range(degree)))


def _inverse_rows(value: Cyclotomic) -> list[list[Q]]:
    degree = len(value.coefficients)
    basis = [_basis_vector(value.conductor, degree, column) for column in range(degree)]
    columns = [(value * item).coefficients for item in basis]
    return [[columns[j][i] for j in range(degree)] + [Q(i == 0)] for i in range(degree)]


def _scale_inverse_row(rows: list[list[Q]], column: int) -> None:
    scale = rows[column][column]
    rows[column] = [value / scale for value in rows[column]]


def _cancel_inverse_row(rows: list[list[Q]], row: int, column: int) -> None:
    scale = rows[row][column]
    rows[row] = [left - scale * right for left, right in zip(rows[row], rows[column], strict=True)]


def _clear_inverse_column(rows: list[list[Q]], column: int) -> None:
    for row in range(len(rows)):
        if row != column:
            _cancel_inverse_row(rows, row, column)


def _pivot_inverse(rows: list[list[Q]], column: int) -> None:
    degree = len(rows)
    pivot = next((row for row in range(column, degree) if rows[row][column]), None)
    if pivot is None:
        raise _fail("cyclotomic multiplication map is unexpectedly singular")
    rows[column], rows[pivot] = rows[pivot], rows[column]
    _scale_inverse_row(rows, column)
    _clear_inverse_column(rows, column)


def _eliminate_inverse(rows: list[list[Q]]) -> None:
    for column in range(len(rows)):
        _pivot_inverse(rows, column)


def _require_inverse_product(value: Cyclotomic, result: Cyclotomic) -> None:
    if value * result != 1:
        raise _fail("cyclotomic inverse failed exact product reconstruction")


def _sqrt2_basis(coefficients: tuple[Q, Q, Q, Q]) -> tuple[Q, Q, int]:
    real, radical, next_real, next_radical = coefficients
    if next_real != 0 or next_radical != -radical:
        raise _fail("sqrt(2) real-subfield representation failed")
    return real, radical, 2


def _sqrt5_basis(coefficients: tuple[Q, Q, Q, Q]) -> tuple[Q, Q, int]:
    real, zeta_coeff, pair, pair_image = coefficients
    if zeta_coeff != 0 or pair != pair_image:
        raise _fail("sqrt(5) real-subfield representation failed")
    return real - pair / 2, -pair / 2, 5


def _real_basis(conductor: int, coefficients: tuple[Q, ...]) -> tuple[Q, Q, int]:
    if conductor in {1, 3, 4}:
        if any(coefficients[1:]):
            raise _fail("rational real-subfield representation failed")
        return coefficients[0], Q(0), 0
    if conductor == 8:
        return _sqrt2_basis(cast(tuple[Q, Q, Q, Q], coefficients))
    return _sqrt5_basis(cast(tuple[Q, Q, Q, Q], coefficients))


def _oriented_sign(real: Q, radical: Q, radicand: int) -> int:
    difference = real * real - radicand * radical * radical
    if difference == 0:
        raise _fail("nonzero rational square cannot equal the frozen nonsquare radicand")
    return ((difference > 0) - (difference < 0)) * (1 if real > 0 else -1)


def _require_schur_diagonal(current: list[list[Cyclotomic]]) -> None:
    size = len(current)
    if any(current[index][index] < 0 for index in range(size)):
        raise _fail("negative eigenvalue: cyclotomic Schur complement is not positive semidefinite")
    for index in range(size):
        _require_zero_row(current, index)


def _require_zero_row(current: list[list[Cyclotomic]], index: int) -> None:
    if current[index][index] == 0 and any(current[index]):
        raise _fail("negative eigenvalue: cyclotomic zero diagonal has a nonzero off-diagonal entry")


def _positive_pivot(current: Sequence[Sequence[Cyclotomic]]) -> int | None:
    return next((index for index, row in enumerate(current) if row[index] > 0), None)


def _schur_entry(
    current: list[list[Cyclotomic]], row: int, col: int, pivot: int, pivot_value: Cyclotomic,
) -> Cyclotomic:
    return current[row][col] - current[row][pivot] * current[pivot][col] / pivot_value


def _schur_complement(current: list[list[Cyclotomic]], pivot: int) -> list[list[Cyclotomic]]:
    indices = [index for index in range(len(current)) if index != pivot]
    pivot_value = current[pivot][pivot]
    return [[_schur_entry(current, row, col, pivot, pivot_value) for col in indices] for row in indices]


def _require_matrix_budget(raw: object) -> list[object]:
    if not isinstance(raw, list) or len(raw) > kernel.MAX_D:
        raise kernel.RefusedAtBudget("matrix_dimension_max=5 exhausted")
    return raw


def _require_declared_shape(raw: list[object], dimension: int) -> None:
    if len(raw) != dimension or any(not isinstance(row, list) or len(row) != dimension for row in raw):
        raise _fail("frozen system dimension mismatch")


def _require_hermitian(matrix: list[list[Cyclotomic]]) -> None:
    dimension = len(matrix)
    mismatched = (
        matrix[row][col] != matrix[col][row].conjugate()
        for row in range(dimension)
        for col in range(dimension)
    )
    if any(mismatched):
        raise _fail("input is not Hermitian in its declared cyclotomic field")


def _require_trace_one(matrix: list[list[Cyclotomic]], conductor: int) -> None:
    total = sum((matrix[index][index] for index in range(len(matrix))), Cyclotomic.rational(conductor, 0))
    if total != 1:
        raise _fail("unnormalised spectrum: trace must equal one")


def _require_scope(case: Mapping[str, Any]) -> None:
    if case["system_id"] == "S8":
        if case["scope"] != "S8_DIMENSION_ONLY_PROXY":
            raise _fail("S8 code support unresolved; dimension-only proxy label required")
        return
    if case["scope"] != "DECLARED_SYSTEM_STATE":
        raise _fail("state scope label mismatch")


def _require_diagonal(matrix: list[list[Cyclotomic]]) -> None:
    dimension = len(matrix)
    off_diagonal = (
        matrix[row][col]
        for row in range(dimension)
        for col in range(dimension)
        if row != col
    )
    if any(off_diagonal):
        raise _fail("frozen ladder states must be diagonal")


def _require_geometric(matrix: list[list[Cyclotomic]]) -> None:
    if matrix[0][0] <= 0:
        raise _fail("S6 requires a positive geometric ladder")
    ratio = matrix[1][1] / matrix[0][0]
    degree = len(matrix)
    geometric = (matrix[index][index] != matrix[0][0] * ratio**index for index in range(degree))
    if not 0 < ratio < 1 or any(geometric):
        raise _fail("S6 requires the declared decreasing geometric ladder")


def _require_self_conjugate_coefficients(polynomial: Sequence[Cyclotomic]) -> None:
    if any(value != value.conjugate() for value in polynomial):
        raise _fail("Hermitian characteristic polynomial has a non-self-conjugate coefficient")


def _charpoly(matrix: list[list[Cyclotomic]]) -> list[Any]:
    # The entropy kernel's Faddeev-LeVerrier loop is duck-typed over this ring.
    return kernel.charpoly(cast(list[list[Q]], matrix))


@dataclass(frozen=True, eq=False, slots=True)
class Cyclotomic:
    """Reduced power-basis element of Q[zeta_n], with arbitrary-size rationals."""

    conductor: int
    coefficients: tuple[Q, ...]

    def __post_init__(self) -> None:
        conductor = _conductor(self.conductor)
        coefficients = _coefficients(self.coefficients, kernel.PHI[conductor])
        object.__setattr__(self, "conductor", conductor)
        object.__setattr__(self, "coefficients", coefficients)

    @classmethod
    def rational(cls, conductor: object, value: object) -> Cyclotomic:
        number = _conductor(conductor)
        coefficient = _exact_rational(value, "value", "cyclotomic arithmetic requires an exact rational")
        return cls(number, (coefficient,) + (Q(0),) * (kernel.PHI[number] - 1))

    @classmethod
    def zeta(cls, conductor: object) -> Cyclotomic:
        number = _conductor(conductor)
        if number == 1:
            return cls.rational(1, 1)
        degree = kernel.PHI[number]
        return cls(number, (Q(0), Q(1)) + (Q(0),) * (degree - 2))

    def _coerce(self, other: object) -> Cyclotomic:
        if isinstance(other, Cyclotomic):
            if other.conductor != self.conductor:
                raise _fail("cyclotomic arithmetic cannot mix declared conductors")
            return other
        return self.rational(self.conductor, other)

    def __bool__(self) -> bool:
        return any(self.coefficients)

    def __hash__(self) -> int:
        if not any(self.coefficients[1:]):
            return hash(self.coefficients[0])
        return hash((self.conductor, self.coefficients))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cyclotomic):
            return self.conductor == other.conductor and self.coefficients == other.coefficients
        if type(other) is int or isinstance(other, Q):
            return not any(self.coefficients[1:]) and self.coefficients[0] == other
        return False

    def __add__(self, other: object) -> Cyclotomic:
        partner = self._coerce(other)
        paired = tuple(left + right for left, right in zip(self.coefficients, partner.coefficients, strict=True))
        return Cyclotomic(self.conductor, paired)

    __radd__ = __add__

    def __neg__(self) -> Cyclotomic:
        return Cyclotomic(self.conductor, tuple(-value for value in self.coefficients))

    def __sub__(self, other: object) -> Cyclotomic:
        return self + -self._coerce(other)

    def __rsub__(self, other: object) -> Cyclotomic:
        return self._coerce(other) + -self

    def __mul__(self, other: object) -> Cyclotomic:
        partner = self._coerce(other)
        degree = len(self.coefficients)
        product = [Q(0)] * (2 * degree - 1)
        for i, left in enumerate(self.coefficients):
            for j, right in enumerate(partner.coefficients):
                product[i + j] += left * right
        modulus = MODULI[self.conductor]
        for exponent in range(len(product) - 1, degree - 1, -1):
            leading = product[exponent]
            for i in range(degree):
                product[exponent - degree + i] -= leading * modulus[i]
        return Cyclotomic(self.conductor, tuple(product[:degree]))

    __rmul__ = __mul__

    @lru_cache(maxsize=4096)
    def inverse(self) -> Cyclotomic:
        if not self:
            raise _division("division by zero cyclotomic element")
        rows = _inverse_rows(self)
        _eliminate_inverse(rows)
        result = Cyclotomic(self.conductor, tuple(row[-1] for row in rows))
        _require_inverse_product(self, result)
        return result

    def __truediv__(self, other: object) -> Cyclotomic:
        return self * self._coerce(other).inverse()

    def __rtruediv__(self, other: object) -> Cyclotomic:
        return self._coerce(other) * self.inverse()

    def __pow__(self, exponent: object) -> Cyclotomic:
        power = _exponent(exponent)
        if power < 0:
            return self.inverse() ** -power
        result, base = self.rational(self.conductor, 1), self
        while power:
            if power % 2:
                result *= base
            base *= base
            power //= 2
        return result

    @lru_cache(maxsize=4096)
    def conjugate(self) -> Cyclotomic:
        inverse_zeta = self.zeta(self.conductor) ** (self.conductor - 1)
        result = self.rational(self.conductor, 0)
        for coefficient in reversed(self.coefficients):
            result = result * inverse_zeta + coefficient
        return result

    def real_coordinates(self) -> tuple[Q, Q, int]:
        """a, b, d for a+b*sqrt(d), after exact self-conjugacy."""
        if self != self.conjugate():
            raise _fail("ordering requires an exactly self-conjugate cyclotomic element")
        return _real_basis(self.conductor, self.coefficients)

    def sign(self) -> int:
        real, radical, radicand = self.real_coordinates()
        if not radical:
            return (real > 0) - (real < 0)
        if not real:
            return (radical > 0) - (radical < 0)
        if (real > 0) == (radical > 0):
            return 1 if real > 0 else -1
        return _oriented_sign(real, radical, radicand)

    def __lt__(self, other: object) -> bool:
        return (self - other).sign() < 0

    def __le__(self, other: object) -> bool:
        return (self - other).sign() <= 0

    def __gt__(self, other: object) -> bool:
        return (self - other).sign() > 0

    def __ge__(self, other: object) -> bool:
        return (self - other).sign() >= 0

    def __abs__(self) -> Cyclotomic:
        if self.sign() < 0:
            return -self
        return self

    def wire(self) -> dict[str, list[str]]:
        return {"cyclotomic_coefficients": [kernel.rat(value) for value in self.coefficients]}


def parse_scalar(value: object, conductor: object) -> Cyclotomic:
    number = _conductor(conductor)
    _scan(value, "cyclotomic_scalar")
    if isinstance(value, str):
        return Cyclotomic.rational(number, kernel.parse_rat(value, bounded=True))
    if not isinstance(value, dict) or set(value) != {"cyclotomic_coefficients"}:
        raise _fail("cyclotomic scalar requires exactly cyclotomic_coefficients or a rational string")
    coefficients = value["cyclotomic_coefficients"]
    if not isinstance(coefficients, list) or len(coefficients) != kernel.PHI[number]:
        raise _fail("cyclotomic coefficient arity differs from phi(conductor)")
    return Cyclotomic(number, tuple(kernel.parse_rat(item, bounded=True) for item in coefficients))


def has_cyclotomic_entries(case: object) -> bool:
    raw = case.get("matrix") if isinstance(case, dict) else None
    if not isinstance(raw, list):
        return False
    return any(isinstance(row, list) and any(isinstance(value, dict) for value in row) for row in raw)


def embedding(conductor: object) -> dict[str, Any]:
    number = _conductor(conductor)
    radicand = 2 if number == 8 else 5 if number == 5 else 0
    return {
        "real_generator_radicand": radicand,
        "real_generator_interval": _REAL_ENDPOINTS[radicand],
        "complex_conjugation": "zeta_to_zeta_inverse",
    }


def validate_embedding(value: object) -> None:
    _scan(value, "embedding")
    if not isinstance(value, dict) or type(value.get("real_generator_radicand")) is not int:
        raise _fail("invalid frozen cyclotomic embedding")
    known = {kernel.serialized(embedding(number)) for number in (1, 5, 8)}
    if kernel.serialized(value) not in known:
        raise _fail("invalid frozen cyclotomic embedding")


def validate_psd(matrix: list[list[Cyclotomic]]) -> None:
    """Hermitian scalar-pivot Schur complements at the one frozen embedding."""
    current = [row[:] for row in matrix]
    while current:
        _require_schur_diagonal(current)
        pivot = _positive_pivot(current)
        if pivot is None:
            return
        current = _schur_complement(current, pivot)


def _validate_case_structure(case: dict[str, Any]) -> tuple[int, int]:
    _scan(case, "input")
    if set(case) != kernel.INPUT_KEYS or not isinstance(case["fixture_id"], str):
        raise _fail("typed input requires exactly the five interface fields")
    if not case["fixture_id"]:
        raise _fail("fixture_id: nonempty string required")
    if not isinstance(case["system_id"], str) or case["system_id"] not in kernel.CLASS:
        raise _fail("system missing from frozen class")
    dimension, conductor = kernel.CLASS[case["system_id"]]
    if type(case["conductor"]) is not int or case["conductor"] != conductor:
        raise _fail("frozen conductor mismatch")
    return dimension, conductor


def _parse_and_validate_matrix(case: dict[str, Any], dimension: int, conductor: int) -> list[list[Cyclotomic]]:
    raw = _require_matrix_budget(case["matrix"])
    _require_declared_shape(raw, dimension)
    matrix = [[parse_scalar(value, conductor) for value in cast(list[object], row)] for row in raw]
    _require_hermitian(matrix)
    _require_trace_one(matrix, conductor)
    return matrix


def _validate_case_scope_and_ladder(case: dict[str, Any], matrix: list[list[Cyclotomic]]) -> None:
    _require_scope(case)
    if case["system_id"] in {"S6", "S7"}:
        _require_diagonal(matrix)
    if case["system_id"] == "S6":
        _require_geometric(matrix)


def validated_matrix(case: dict[str, Any]) -> list[list[Cyclotomic]]:
    dimension, conductor = _validate_case_structure(case)
    matrix = _parse_and_validate_matrix(case, dimension, conductor)
    _validate_case_scope_and_ladder(case, matrix)
    validate_psd(matrix)
    return matrix


def trace_square(matrix: list[list[Cyclotomic]]) -> Cyclotomic:
    products = [matrix[row][col] * matrix[col][row] for row in range(len(matrix)) for col in range(len(matrix))]
    conductor = matrix[0][0].conductor
    coefficients = tuple(
        rational_sum([value.coefficients[index] for value in products])
        for index in range(kernel.PHI[conductor])
    )
    return Cyclotomic(conductor, coefficients)


def rational_sum(values: list[Q]) -> Q:
    """Exact stepwise reduced fold used in each trace-square coefficient."""
    result = Q(0)
    for value in values:
        if not isinstance(value, Q):
            raise _fail("rational fold requires exact Fraction terms", received=type(value).__name__)
        result += value
    return result


def characteristic_record(case: dict[str, Any]) -> dict[str, Any]:
    matrix = validated_matrix(case)
    conductor = case["conductor"]
    polynomial = [
        value if isinstance(value, Cyclotomic) else Cyclotomic.rational(conductor, value)
        for value in _charpoly(matrix)
    ]
    _require_self_conjugate_coefficients(polynomial)
    power_sum = trace_square(matrix)
    purity = "PURE" if power_sum == 1 else "MIXED"
    return {
        "characteristic_polynomial": [value.wire() for value in polynomial],
        "renyi2_power_sum": power_sum.wire(),
        "purity": purity,
        "entropy": kernel._verdict_from_validated_purity(purity),
        "embedding": embedding(conductor),
        "spectrum_scope": "CHARACTERISTIC_ONLY_NO_SPLITTING_OR_DEPENDENCE",
    }


def validate_characteristic_record(record: dict[str, Any]) -> None:
    _scan(record, "cyclotomic_record")
    if set(record) != {"input", "output"}:
        raise _fail("cyclotomic record requires input and output")
    expected = characteristic_record(record["input"])
    if not isinstance(record["output"], dict) or set(record["output"]) != set(expected):
        raise _fail("cyclotomic output field census differs")
    for key, value in expected.items():
        if kernel.serialized(record["output"][key]) != kernel.serialized(value):
            raise _fail(f"{record['input']['fixture_id']}: injected or invalid cyclotomic {key}")


def characteristic_report(interface: Path | None = None) -> dict[str, Any]:
    cases = [{"input": case, "output": characteristic_record(case)} for case in kernel.fixtures(interface)]
    return {"authority_effect": "None", "schema": "cyclotomic_density_v1", "cases": cases}


def entropy_verdict(case: dict[str, Any], *, approximation_k: int | None = None) -> dict[str, str]:
    matrix = validated_matrix(case)
    purity = "PURE" if trace_square(matrix) == 1 else "MIXED"
    interval = None if approximation_k is None else entropy_interval(case, approximation_k)
    return kernel._verdict_from_validated_purity(purity, interval)


def entropy_interval(case: dict[str, Any], k: int) -> dict[str, Any]:
    if type(k) is not int or not 0 <= k <= kernel.MAX_K:
        raise kernel.RefusedAtBudget("approximation_k_max=32 exhausted or invalid precision")
    matrix = validated_matrix(case)
    return kernel._entropy_interval_from_characteristic(
        _charpoly(matrix), k, cyclotomic_embedding=embedding(case["conductor"]),
    )
