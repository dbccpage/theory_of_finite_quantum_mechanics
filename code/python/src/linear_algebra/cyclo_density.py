"""Exact density arithmetic in five launch fields. AuthorityEffect: None.

The ordered embedding is frozen, not inferred numerically. Characteristic
polynomials and purity are exact; entropy uses the cited Baker reduction.
No splitting-field or multiplicative-dependence implementation is claimed here.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from typing import Any

from . import entropy_dichotomy as kernel


# Ascending coefficients, including the monic leading coefficient.
MODULI = {1: (-1, 1), 3: (1, 1, 1), 4: (1, 0, 1),
          5: (1, 1, 1, 1, 1), 8: (1, 0, 0, 0, 1)}
ROOT_ISOLATION = "EXACT_CYCLOTOMIC_REAL_STURM_SPECTRAL_CLUSTERS"


@dataclass(frozen=True, eq=False, slots=True)
class Cyclotomic:
    """Reduced power-basis element of Q[zeta_n], with arbitrary-size rationals."""

    conductor: int
    coefficients: tuple[Q, ...]

    def __post_init__(self) -> None:
        if type(self.conductor) is not int or self.conductor not in MODULI:
            raise ValueError("unsupported cyclotomic conductor")
        if len(self.coefficients) != kernel.PHI[self.conductor]:
            raise ValueError("cyclotomic coefficient arity differs from phi(conductor)")
        if any(type(value) is not int and not isinstance(value, Q) for value in self.coefficients):
            raise ValueError("cyclotomic arithmetic requires exact rational coefficients")
        object.__setattr__(self, "coefficients", tuple(Q(value) for value in self.coefficients))

    @classmethod
    def rational(cls, conductor: int, value: Q | int) -> Cyclotomic:
        if type(conductor) is not int or conductor not in MODULI:
            raise ValueError("unsupported cyclotomic conductor")
        if type(value) is not int and not isinstance(value, Q):
            raise ValueError("cyclotomic arithmetic requires an exact rational")
        return cls(conductor, (Q(value),) + (Q(0),) * (kernel.PHI[conductor] - 1))

    @classmethod
    def zeta(cls, conductor: int) -> Cyclotomic:
        if type(conductor) is not int or conductor not in MODULI:
            raise ValueError("unsupported cyclotomic conductor")
        if conductor == 1:
            return cls.rational(1, 1)
        return cls(conductor, (Q(0), Q(1)) + (Q(0),) * (kernel.PHI[conductor] - 2))

    def _coerce(self, other: Any) -> Cyclotomic:
        if isinstance(other, Cyclotomic):
            if other.conductor != self.conductor:
                raise ValueError("cyclotomic arithmetic cannot mix declared conductors")
            return other
        return self.rational(self.conductor, other)

    def __bool__(self) -> bool:
        return any(self.coefficients)

    def __hash__(self) -> int:
        if not any(self.coefficients[1:]):
            return hash(self.coefficients[0])
        return hash((self.conductor, self.coefficients))

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Cyclotomic):
            return self.conductor == other.conductor and self.coefficients == other.coefficients
        if type(other) is int or isinstance(other, Q):
            return not any(self.coefficients[1:]) and self.coefficients[0] == other
        return False

    def __add__(self, other: Any) -> Cyclotomic:
        other = self._coerce(other)
        return Cyclotomic(self.conductor, tuple(a + b for a, b in zip(self.coefficients, other.coefficients)))

    __radd__ = __add__

    def __neg__(self) -> Cyclotomic:
        return Cyclotomic(self.conductor, tuple(-value for value in self.coefficients))

    def __sub__(self, other: Any) -> Cyclotomic:
        return self + -self._coerce(other)

    def __rsub__(self, other: Any) -> Cyclotomic:
        return self._coerce(other) + -self

    def __mul__(self, other: Any) -> Cyclotomic:
        other = self._coerce(other)
        degree = len(self.coefficients)
        product = [Q(0)] * (2 * degree - 1)
        for i, a in enumerate(self.coefficients):
            for j, b in enumerate(other.coefficients):
                product[i + j] += a * b
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
            raise ZeroDivisionError("division by zero cyclotomic element")
        degree = len(self.coefficients)
        # Invert the Q-linear multiplication map in at most phi(n) pivots.
        basis = [Cyclotomic(self.conductor, tuple(Q(i == j) for i in range(degree)))
                 for j in range(degree)]
        columns = [(self * value).coefficients for value in basis]
        rows = [[columns[j][i] for j in range(degree)] + [Q(i == 0)] for i in range(degree)]
        for column in range(degree):
            pivot = next((row for row in range(column, degree) if rows[row][column]), None)
            if pivot is None:
                raise ValueError("cyclotomic multiplication map is unexpectedly singular")
            rows[column], rows[pivot] = rows[pivot], rows[column]
            scale = rows[column][column]
            rows[column] = [value / scale for value in rows[column]]
            for row in range(degree):
                if row != column:
                    scale = rows[row][column]
                    rows[row] = [a - scale * b for a, b in zip(rows[row], rows[column])]
        result = Cyclotomic(self.conductor, tuple(row[-1] for row in rows))
        if self * result != 1:
            raise ValueError("cyclotomic inverse failed exact product reconstruction")
        return result

    def __truediv__(self, other: Any) -> Cyclotomic:
        return self * self._coerce(other).inverse()

    def __rtruediv__(self, other: Any) -> Cyclotomic:
        return self._coerce(other) * self.inverse()

    def __pow__(self, exponent: int) -> Cyclotomic:
        if type(exponent) is not int:
            raise ValueError("cyclotomic exponent must be an integer")
        if exponent < 0:
            return self.inverse() ** -exponent
        result, base = self.rational(self.conductor, 1), self
        while exponent:
            if exponent % 2:
                result *= base
            base *= base
            exponent //= 2
        return result

    @lru_cache(maxsize=4096)
    def conjugate(self) -> Cyclotomic:
        inverse_zeta = self.zeta(self.conductor) ** (self.conductor - 1)
        result = self.rational(self.conductor, 0)
        for coefficient in reversed(self.coefficients):
            result = result * inverse_zeta + coefficient
        return result

    def real_coordinates(self) -> tuple[Q, Q, int]:
        """a,b,d for a+b*sqrt(d), but only after exact self-conjugacy."""
        if self != self.conjugate():
            raise ValueError("ordering requires an exactly self-conjugate cyclotomic element")
        if self.conductor in {1, 3, 4}:
            if any(self.coefficients[1:]):
                raise ValueError("rational real-subfield representation failed")
            return self.coefficients[0], Q(0), 0
        if self.conductor == 8:
            a, b, c, d = self.coefficients
            if c != 0 or d != -b:
                raise ValueError("sqrt(2) real-subfield representation failed")
            return a, b, 2
        a, b, c, d = self.coefficients
        if b != 0 or c != d:
            raise ValueError("sqrt(5) real-subfield representation failed")
        return a - c / 2, -c / 2, 5

    def sign(self) -> int:
        a, b, d = self.real_coordinates()
        if not b:
            return (a > 0) - (a < 0)
        if not a:
            return (b > 0) - (b < 0)
        if (a > 0) == (b > 0):
            return 1 if a > 0 else -1
        difference = a * a - d * b * b
        if difference == 0:
            raise ValueError("nonzero rational square cannot equal the frozen nonsquare radicand")
        return ((difference > 0) - (difference < 0)) * (1 if a > 0 else -1)

    def __lt__(self, other: Any) -> bool:
        return (self - other).sign() < 0

    def __le__(self, other: Any) -> bool:
        return (self - other).sign() <= 0

    def __gt__(self, other: Any) -> bool:
        return (self - other).sign() > 0

    def __ge__(self, other: Any) -> bool:
        return (self - other).sign() >= 0

    def __abs__(self) -> Cyclotomic:
        return -self if self.sign() < 0 else self

    def wire(self) -> dict[str, list[str]]:
        return {"cyclotomic_coefficients": [kernel.rat(value) for value in self.coefficients]}


def parse_scalar(value: Any, conductor: int) -> Cyclotomic:
    kernel.reject_floats(value, "cyclotomic_scalar")
    if isinstance(value, str):
        return Cyclotomic.rational(conductor, kernel.parse_rat(value, bounded=True))
    if not isinstance(value, dict) or set(value) != {"cyclotomic_coefficients"}:
        raise ValueError("cyclotomic scalar requires exactly cyclotomic_coefficients or a rational string")
    coefficients = value["cyclotomic_coefficients"]
    if not isinstance(coefficients, list) or len(coefficients) != kernel.PHI.get(conductor):
        raise ValueError("cyclotomic coefficient arity differs from phi(conductor)")
    return Cyclotomic(conductor, tuple(kernel.parse_rat(item, bounded=True) for item in coefficients))


def has_cyclotomic_entries(case: Any) -> bool:
    raw = case.get("matrix") if isinstance(case, dict) else None
    return isinstance(raw, list) and any(isinstance(row, list) and any(isinstance(value, dict) for value in row)
                                         for row in raw)


def embedding(conductor: int) -> dict[str, Any]:
    if type(conductor) is not int or conductor not in MODULI:
        raise ValueError("unsupported cyclotomic conductor")
    radicand = 2 if conductor == 8 else 5 if conductor == 5 else 0
    endpoints = {0: ["1/1", "1/1"], 2: ["7/5", "3/2"], 5: ["11/5", "12/5"]}[radicand]
    return {"real_generator_radicand": radicand, "real_generator_interval": endpoints,
            "complex_conjugation": "zeta_to_zeta_inverse"}


def validate_embedding(value: Any) -> None:
    if not isinstance(value, dict) or type(value.get("real_generator_radicand")) is not int:
        raise ValueError("invalid frozen cyclotomic embedding")
    if kernel.serialized(value) not in {kernel.serialized(embedding(n)) for n in (1, 5, 8)}:
        raise ValueError("invalid frozen cyclotomic embedding")


def validate_psd(matrix: list[list[Cyclotomic]]) -> None:
    """Hermitian scalar-pivot Schur complements at the one frozen embedding."""
    current = [row[:] for row in matrix]
    while current:
        if any(current[i][i] < 0 for i in range(len(current))):
            raise ValueError("negative eigenvalue: cyclotomic Schur complement is not positive semidefinite")
        for i in range(len(current)):
            if current[i][i] == 0 and any(current[i][j] for j in range(len(current))):
                raise ValueError("negative eigenvalue: cyclotomic zero diagonal has a nonzero off-diagonal entry")
        pivot = next((i for i in range(len(current)) if current[i][i] > 0), None)
        if pivot is None:
            return
        indices = [i for i in range(len(current)) if i != pivot]
        current = [[current[i][j] - current[i][pivot] * current[pivot][j] / current[pivot][pivot]
                    for j in indices] for i in indices]


def _validate_case_structure(case: dict[str, Any]) -> tuple[int, int]:
    kernel.reject_floats(case, "input")
    if not isinstance(case, dict) or set(case) != kernel.INPUT_KEYS or not isinstance(case["fixture_id"], str):
        raise ValueError("typed input requires exactly the five interface fields")
    if not case["fixture_id"]:
        raise ValueError("fixture_id: nonempty string required")
    if not isinstance(case["system_id"], str) or case["system_id"] not in kernel.CLASS:
        raise ValueError("system missing from frozen class")
    dimension, conductor = kernel.CLASS[case["system_id"]]
    if type(case["conductor"]) is not int or case["conductor"] != conductor:
        raise ValueError("frozen conductor mismatch")
    return dimension, conductor


def _parse_and_validate_matrix(case: dict[str, Any], dimension: int, conductor: int) -> list[list[Cyclotomic]]:
    raw = case["matrix"]
    if not isinstance(raw, list) or len(raw) > kernel.MAX_D:
        raise kernel.RefusedAtBudget("matrix_dimension_max=5 exhausted")
    if len(raw) != dimension or any(not isinstance(row, list) or len(row) != dimension for row in raw):
        raise ValueError("frozen system dimension mismatch")
    matrix = [[parse_scalar(value, conductor) for value in row] for row in raw]
    if any(matrix[i][j] != matrix[j][i].conjugate() for i in range(dimension) for j in range(dimension)):
        raise ValueError("input is not Hermitian in its declared cyclotomic field")
    if sum((matrix[i][i] for i in range(dimension)), Cyclotomic.rational(conductor, 0)) != 1:
        raise ValueError("unnormalised spectrum: trace must equal one")
    return matrix


def _validate_case_scope_and_ladder(case: dict[str, Any], matrix: list[list[Cyclotomic]], dimension: int) -> None:
    if case["system_id"] == "S8":
        if case["scope"] != "S8_DIMENSION_ONLY_PROXY":
            raise ValueError("S8 code support unresolved; dimension-only proxy label required")
    elif case["scope"] != "DECLARED_SYSTEM_STATE":
        raise ValueError("state scope label mismatch")

    if case["system_id"] in {"S6", "S7"}:
        if any(matrix[i][j] for i in range(dimension) for j in range(dimension) if i != j):
            raise ValueError("frozen ladder states must be diagonal")

    if case["system_id"] == "S6":
        if matrix[0][0] <= 0:
            raise ValueError("S6 requires a positive geometric ladder")
        ratio = matrix[1][1] / matrix[0][0]
        if not 0 < ratio < 1 or any(matrix[i][i] != matrix[0][0] * ratio**i for i in range(dimension)):
            raise ValueError("S6 requires the declared decreasing geometric ladder")


def validated_matrix(case: dict[str, Any]) -> list[list[Cyclotomic]]:
    dimension, conductor = _validate_case_structure(case)
    matrix = _parse_and_validate_matrix(case, dimension, conductor)
    _validate_case_scope_and_ladder(case, matrix, dimension)
    validate_psd(matrix)
    return matrix


def trace_square(matrix: list[list[Cyclotomic]]) -> Cyclotomic:
    products = [matrix[i][j] * matrix[j][i] for i in range(len(matrix)) for j in range(len(matrix))]
    conductor = matrix[0][0].conductor
    return Cyclotomic(conductor, tuple(rational_sum([value.coefficients[index] for value in products])
                                      for index in range(kernel.PHI[conductor])))


def rational_sum(values: list[Q]) -> Q:
    """Exact stepwise reduced fold used in each trace-square coefficient."""
    result = Q(0)
    for value in values:
        if not isinstance(value, Q):
            raise ValueError("rational fold requires exact Fraction terms")
        result += value
    return result


def characteristic_record(case: dict[str, Any]) -> dict[str, Any]:
    matrix = validated_matrix(case)
    conductor = case["conductor"]
    polynomial = [Cyclotomic.rational(conductor, value) if not isinstance(value, Cyclotomic) else value
                  for value in kernel.charpoly(matrix)]
    if any(value != value.conjugate() for value in polynomial):
        raise ValueError("Hermitian characteristic polynomial has a non-self-conjugate coefficient")
    power_sum = trace_square(matrix)
    purity = "PURE" if power_sum == 1 else "MIXED"
    return {"characteristic_polynomial": [value.wire() for value in polynomial],
            "renyi2_power_sum": power_sum.wire(), "purity": purity,
            "entropy": kernel._verdict_from_validated_purity(purity),
            "embedding": embedding(conductor),
            "spectrum_scope": "CHARACTERISTIC_ONLY_NO_SPLITTING_OR_DEPENDENCE"}


def validate_characteristic_record(record: dict[str, Any]) -> None:
    kernel.reject_floats(record, "cyclotomic_record")
    if not isinstance(record, dict) or set(record) != {"input", "output"}:
        raise ValueError("cyclotomic record requires input and output")
    expected = characteristic_record(record["input"])
    if not isinstance(record["output"], dict) or set(record["output"]) != set(expected):
        raise ValueError("cyclotomic output field census differs")
    for key, value in expected.items():
        if kernel.serialized(record["output"][key]) != kernel.serialized(value):
            raise ValueError(f"{record['input']['fixture_id']}: injected or invalid cyclotomic {key}")


def characteristic_report(interface: Path | None = None) -> dict[str, Any]:
    return {"authority_effect": "None", "schema": "cyclotomic_density_v1", "cases": [
        {"input": case, "output": characteristic_record(case)} for case in kernel.fixtures(interface)]}


def entropy_verdict(case: dict[str, Any], *, approximation_k: int | None = None) -> dict[str, str]:
    matrix = validated_matrix(case)
    purity = "PURE" if trace_square(matrix) == 1 else "MIXED"
    interval = None if approximation_k is None else entropy_interval(case, approximation_k)
    return kernel._verdict_from_validated_purity(purity, interval)


def entropy_interval(case: dict[str, Any], k: int) -> dict[str, Any]:
    if type(k) is not int or not 0 <= k <= kernel.MAX_K:
        raise kernel.RefusedAtBudget("approximation_k_max=32 exhausted or invalid precision")
    matrix = validated_matrix(case)
    return kernel._entropy_interval_from_characteristic(kernel.charpoly(matrix), k,
                                                        cyclotomic_embedding=embedding(case["conductor"]))
