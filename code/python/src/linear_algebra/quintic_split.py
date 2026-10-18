"""Exact finite splitting algebras, not assumed fields.

Origin: code/rust/src/linear_algebra/quintic_split.rs, which states exact
finite splitting algebras whose ranks are not field degrees.
Claim: urn:omega:fqm:linear-algebra:quintic-splitting-degree:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_quintic_split.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 8; AST Sonar cognitive complexity max 8; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 8.
Scope Fence: All divisions are in E. Elements of the splitting algebra may be
zero divisors. This file classifies an irreducible quintic by fixed spaces and
localized separating resolvents. It does not claim carrier transport,
multiplicative dependence, or a float embedding.
"""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import product
import json
import sys
from typing import Any, Mapping, cast

from . import field_factors as factors
from . import field_squares as real


ZERO = factors.ZERO
ONE = factors.ONE
Coordinates = tuple[Q, Q]
Polynomial = list[Coordinates]
Element = dict[int, Coordinates]
Exponent = tuple[int, ...]
Monomial = dict[Exponent, Coordinates]
SCHEMA = "quintic_splitting_degree_v1"
ALGORITHM = "EXACT_LOCALIZED_QUINTIC_FIXED_ALGEBRAS"
SCOPE = "E_QUINTIC_SPLITTING_DEGREE_NO_CARRIER_TRANSPORT_OR_DEPENDENCE"
TRANSLATION = (1, 2, 3, 4, 0)
DILATION = (0, 2, 4, 1, 3)
RESULT_FIELDS = {
    "schema", "authority_effect", "algorithm", "scope", "conductor",
    "real_generator_radicand", "coefficient_field", "algebra_rank", "coefficients",
    "monic_polynomial", "factorization", "discriminant", "discriminant_square",
    "full_fixed_algebra", "localized_fixed_algebra", "galois_group", "degree_over_real_field",
}
FIXED_FIELDS = {
    "generators", "dimension", "basis", "primitive_parameter",
    "primitive_element", "polynomial", "factorization",
}
LOCAL_FIELDS = {"root", "idempotent", "ideal_dimension", "ideal_basis", "cyclic_fixed_algebra"}
REQUEST_FIELDS = {"operation", "conductor", "coefficients"}


class QuinticDegreeError(ValueError):
    """One violated quintic-degree invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> QuinticDegreeError:
    return QuinticDegreeError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _scan_public(value: object, role: str) -> None:
    _refuse_float(value, role)
    if isinstance(value, (list, tuple)):
        for item in value:
            _scan_public(item, role)


def _exact_counter(value: object, role: str) -> int:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where an exact integer was required", role=role)
    if isinstance(value, int):
        return value
    raise _fail("quintic_degree: exact integer required", role=role, received=type(value).__name__)


def _parameter(value: object, invariant: str) -> int:
    number = _exact_counter(value, "primitive_parameter")
    if number < 0:
        raise _fail(invariant)
    return number


def _add(left: Coordinates, right: Coordinates) -> Coordinates:
    return left[0] + right[0], left[1] + right[1]


def _neg(value: Coordinates) -> Coordinates:
    return -value[0], -value[1]


def _mul(left: Coordinates, right: Coordinates, radicand: int) -> Coordinates:
    if not left[1]:
        return left[0] * right[0], left[0] * right[1]
    if not right[1]:
        return left[0] * right[0], left[1] * right[0]
    return left[0] * right[0] + radicand * left[1] * right[1], left[0] * right[1] + left[1] * right[0]


def _div(left: Coordinates, right: Coordinates, radicand: int) -> Coordinates:
    if not right[1]:
        if not right[0]:
            raise _fail("splitting_algebra: division by zero E coefficient")
        return left[0] / right[0], left[1] / right[0]
    return factors._div(left, right, radicand)


def _accumulate(target: dict[Any, Coordinates], key: Any, value: Coordinates) -> None:
    if value == ZERO:
        return
    total = _add(target.get(key, ZERO), value)
    if total == ZERO:
        target.pop(key, None)
    else:
        target[key] = total


def _linear(vectors: list[Element], coefficients: list[Coordinates], radicand: int) -> Element:
    out: Element = {}
    for vector, coefficient in zip(vectors, coefficients, strict=True):
        if coefficient != ZERO:
            for key, value in vector.items():
                _accumulate(out, key, _mul(value, coefficient, radicand))
    return out


class Span:
    """Incremental exact column basis with input-order, unscaled generators."""

    def __init__(self, radicand: int) -> None:
        self.d = radicand
        self.vectors: list[Element] = []
        self.rows: dict[int, tuple[Element, Element]] = {}

    def reduce(self, vector: Element) -> tuple[Element, Element]:
        remainder = dict(vector)
        coordinates: Element = {}
        for pivot in sorted(self.rows):
            _reduce_pivot(self, remainder, coordinates, pivot)
        return remainder, coordinates

    def insert(self, vector: Element) -> bool:
        remainder, coordinates = self.reduce(vector)
        if not remainder:
            return False
        pivot = min(remainder)
        divisor = remainder[pivot]
        row = {key: _div(value, divisor, self.d) for key, value in remainder.items()}
        expression = {key: _neg(_div(value, divisor, self.d)) for key, value in coordinates.items()}
        expression[len(self.vectors)] = _div(ONE, divisor, self.d)
        self.rows[pivot] = row, expression
        self.vectors.append(dict(vector))
        return True

    def coordinates(self, vector: Element) -> list[Coordinates]:
        remainder, coordinates = self.reduce(vector)
        if remainder:
            raise _fail("splitting_algebra: vector outside certified subspace")
        return [coordinates.get(index, ZERO) for index in range(len(self.vectors))]


def _reduce_pivot(span: Span, remainder: Element, coordinates: Element, pivot: int) -> None:
    coefficient = remainder.get(pivot, ZERO)
    if coefficient == ZERO:
        return
    row, expression = span.rows[pivot]
    for key, value in row.items():
        _accumulate(remainder, key, _neg(_mul(coefficient, value, span.d)))
    for key, value in expression.items():
        _accumulate(coordinates, key, _mul(coefficient, value, span.d))


def _clear_pivot(row: Element, pivot_row: Element, column: int, radicand: int) -> None:
    coefficient = row.get(column, ZERO)
    if coefficient == ZERO:
        return
    for key, value in pivot_row.items():
        _accumulate(row, key, _neg(_mul(coefficient, value, radicand)))


def _normalize_pivot(rows: list[Element], index: int, column: int, radicand: int) -> None:
    divisor = rows[index][column]
    rows[index] = {key: _div(value, divisor, radicand) for key, value in rows[index].items()}
    for row_index, row in enumerate(rows):
        if row_index != index:
            _clear_pivot(row, rows[index], column, radicand)


def _select_pivot(rows: list[Element], pivots: list[int], column: int, radicand: int) -> None:
    selected = next(
        (index for index in range(len(pivots), len(rows)) if rows[index].get(column, ZERO) != ZERO),
        None,
    )
    if selected is None:
        return
    index = len(pivots)
    rows[index], rows[selected] = rows[selected], rows[index]
    _normalize_pivot(rows, index, column, radicand)
    pivots.append(column)


def _free_column(rows: list[Element], pivots: list[int], column: int) -> Element:
    vector: Element = {column: ONE}
    for index, pivot in enumerate(pivots):
        value = rows[index].get(column, ZERO)
        if value != ZERO:
            vector[pivot] = _neg(value)
    return vector


def _kernel(rows: list[Element], width: int, radicand: int) -> list[Element]:
    """RREF: columns ascending, first available pivot row, all-row elimination."""
    reduced = [dict(row) for row in rows]
    pivots: list[int] = []
    for column in range(width):
        _select_pivot(reduced, pivots, column, radicand)
    result: list[Element] = []
    for column in range(width):
        if column not in pivots:
            result.append(_free_column(reduced, pivots, column))
    return result


def _push(exponent: Exponent, variable: int) -> Exponent:
    shifted = list(exponent)
    shifted[variable] += 1
    return tuple(shifted)


def _descend_quotient(residual: list[Monomial], bound: int, variable: int) -> list[Monomial]:
    quotient: list[Monomial] = [{} for _ in range(bound)]
    quotient[-1] = dict(residual[-1])
    for index in range(bound - 1, 0, -1):
        quotient[index - 1] = dict(residual[index])
        for exponent, value in quotient[index].items():
            _accumulate(quotient[index - 1], _push(exponent, variable), value)
    return quotient


def _relation_polynomial(
    residual: list[Monomial], quotient: list[Monomial], variable: int, zero_exp: Exponent, bound: int,
) -> Monomial:
    relation = dict(residual[0])
    for exponent, value in quotient[0].items():
        _accumulate(relation, _push(exponent, variable), value)
    leading = list(zero_exp)
    leading[variable] = bound
    if relation.pop(tuple(leading), None) != ONE:
        raise _fail("splitting_algebra: triangular relation is not monic")
    return {exponent: _neg(value) for exponent, value in relation.items()}


class SplittingAlgebra:
    """Successive monic root adjunction for separable degree two through five."""

    def __init__(self, conductor: object, coefficients: object) -> None:
        _scan_public(conductor, "conductor")
        _scan_public(coefficients, "coefficient")
        self.d, self.coefficients = factors._domain(conductor, coefficients)
        self.conductor = factors._require_conductor(conductor)
        self.n = len(self.coefficients) - 1
        if not 2 <= self.n <= 5:
            raise _fail("splitting_algebra: polynomial degree must be two through five", degree=self.n)
        self.monic = [_div(value, self.coefficients[0], self.d) for value in self.coefficients]
        ascending = list(reversed(self.monic))
        if len(factors._gcd(ascending, factors._derivative(ascending), self.d)) != 1:
            raise _fail("splitting_algebra: separable polynomial required")
        self.bounds = tuple(range(self.n, 1, -1))
        self.exponents = sorted(
            product(*(range(bound) for bound in self.bounds)),
            key=lambda exponent: (sum(exponent), exponent),
        )
        self.indices = {exponent: index for index, exponent in enumerate(self.exponents)}
        self.rank = len(self.exponents)
        self.unit: Element = {0: ONE}
        self._normal_cache: dict[Exponent, Element] = {}
        self._actions: dict[tuple[int, ...], list[Element]] = {}
        zero_exp = self._install_relations(ascending)
        self._install_roots(zero_exp)

    def _install_relations(self, ascending: Polynomial) -> Exponent:
        zero_exp = (0,) * (self.n - 1)
        residual: list[Monomial] = [
            {zero_exp: coefficient} if coefficient != ZERO else {} for coefficient in ascending
        ]
        self.relations: list[Monomial] = []
        for variable, bound in enumerate(self.bounds):
            quotient = _descend_quotient(residual, bound, variable)
            self.relations.append(_relation_polynomial(residual, quotient, variable, zero_exp, bound))
            residual = quotient
        return zero_exp

    def _install_roots(self, zero_exp: Exponent) -> None:
        self.roots: list[Element] = []
        for variable in range(self.n - 1):
            exponent = list(zero_exp)
            exponent[variable] = 1
            self.roots.append({self.indices[tuple(exponent)]: ONE})
        last = self.scale(self.unit, _neg(self.monic[1]))
        for root in self.roots:
            last = self.add(last, self.scale(root, (Q(-1), Q(0))))
        self.roots.append(last)

    def normal(self, exponent: Exponent) -> Element:
        cached = self.indices.get(exponent)
        if cached is not None:
            return {cached: ONE}
        stored = self._normal_cache.get(exponent)
        if stored is not None:
            return stored
        variable = max(index for index, bound in enumerate(self.bounds) if exponent[index] >= bound)
        shift = list(exponent)
        shift[variable] -= self.bounds[variable]
        out: Element = {}
        for replacement, coefficient in self.relations[variable].items():
            target = tuple(left + right for left, right in zip(shift, replacement, strict=True))
            for key, value in self.normal(target).items():
                _accumulate(out, key, _mul(coefficient, value, self.d))
        self._normal_cache[exponent] = out
        return out

    def add(self, left: Element, right: Element) -> Element:
        result = dict(left)
        for key, value in right.items():
            _accumulate(result, key, value)
        return result

    def scale(self, element: Element, coefficient: Coordinates) -> Element:
        if coefficient == ZERO:
            return {}
        return {
            key: value
            for key, old in element.items()
            if (value := _mul(old, coefficient, self.d)) != ZERO
        }

    def mul(self, left: Element, right: Element) -> Element:
        # First combine equal exponent sums, then reduce once per monomial.
        raw: Monomial = {}
        for left_index, left_value in left.items():
            for right_index, right_value in right.items():
                exponent = tuple(
                    left + right
                    for left, right in zip(self.exponents[left_index], self.exponents[right_index], strict=True)
                )
                _accumulate(raw, exponent, _mul(left_value, right_value, self.d))
        out: Element = {}
        for exponent, coefficient in raw.items():
            for key, value in self.normal(exponent).items():
                _accumulate(out, key, _mul(coefficient, value, self.d))
        return out

    def evaluate(self, coefficients: Polynomial, element: Element, unit: Element | None = None) -> Element:
        current = self.unit if unit is None else unit
        out: Element = {}
        for coefficient in coefficients:
            out = self.add(self.mul(out, element), self.scale(current, coefficient))
        return out

    def action_columns(self, permutation: object) -> list[Element]:
        checked = self._require_permutation(permutation)
        cached = self._actions.get(checked)
        if cached is not None:
            return cached
        built = self._build_action(checked)
        self._actions[checked] = built
        return built

    def _require_permutation(self, permutation: object) -> tuple[int, ...]:
        if not isinstance(permutation, (list, tuple)):
            raise _fail("splitting_algebra: exact root permutation required")
        checked = tuple(permutation)
        if len(checked) != self.n or any(type(index) is not int for index in checked):
            raise _fail("splitting_algebra: exact root permutation required")
        if sorted(checked) != list(range(self.n)):
            raise _fail("splitting_algebra: exact root permutation required")
        return checked

    def _build_action(self, permutation: tuple[int, ...]) -> list[Element]:
        images: list[Element] = []
        for exponent in self.exponents:
            images.append(self._action_image(images, exponent, permutation))
        return images

    def _action_image(self, images: list[Element], exponent: Exponent, permutation: tuple[int, ...]) -> Element:
        variable = next((index for index, power in enumerate(exponent) if power), None)
        if variable is None:
            return self.unit
        predecessor = list(exponent)
        predecessor[variable] -= 1
        return self.mul(images[self.indices[tuple(predecessor)]], self.roots[permutation[variable]])

    def act(self, element: Element, permutation: object) -> Element:
        columns = self.action_columns(permutation)
        return _linear([columns[index] for index in element], list(element.values()), self.d)

    def fixed_basis(self, permutations: list[tuple[int, ...]], ambient: list[Element] | None = None) -> list[Element]:
        space = [{index: ONE} for index in range(self.rank)] if ambient is None else ambient
        span = Span(self.d)
        for vector in space:
            if not span.insert(vector):
                raise _fail("splitting_algebra: dependent ambient basis")
        rows: list[Element] = []
        for permutation in permutations:
            rows.extend(self._permutation_rows(span, space, permutation))
        return [
            _linear(space, [vector.get(index, ZERO) for index in range(len(space))], self.d)
            for vector in _kernel(rows, len(space), self.d)
        ]

    def _permutation_rows(self, span: Span, ambient: list[Element], permutation: tuple[int, ...]) -> list[Element]:
        matrix_rows: list[Element] = [{} for _ in ambient]
        for column, vector in enumerate(ambient):
            _record_fixed_column(self, span, matrix_rows, column, vector, permutation)
        return matrix_rows

    def primitive(
        self,
        basis: list[Element],
        unit: Element | None = None,
        parameter: object = None,
    ) -> tuple[int, Element, Polynomial]:
        current = self.unit if unit is None else unit
        width = len(basis)
        span = Span(self.d)
        for vector in basis:
            if not span.insert(vector):
                raise _fail("splitting_algebra: dependent fixed basis")
        span.coordinates(current)
        bound = (width - 1) * width * (width - 1) // 2
        candidates: range | list[int]
        if parameter is None:
            candidates = range(bound + 1)
        else:
            candidates = [_parameter(parameter, "splitting_algebra: nonnegative exact primitive parameter required")]
        for candidate in candidates:
            found = self._primitive_at(span, basis, current, candidate, width)
            if found is not None:
                return found
        raise _fail("splitting_algebra: primitive Krylov rank failed for parameter family")

    def _primitive_at(
        self, span: Span, basis: list[Element], unit: Element, candidate: int, width: int,
    ) -> tuple[int, Element, Polynomial] | None:
        theta = _linear(basis, [(Q(candidate ** power), Q(0)) for power in range(width)], self.d)
        closed = self._krylov(span, unit, theta, width)
        if closed is None:
            return None
        krylov, power = closed
        relation = _squarefree_relation(span, krylov, power, self.d)
        return candidate, theta, relation

    def _krylov(self, span: Span, unit: Element, theta: Element, width: int) -> tuple[Span, Element] | None:
        krylov = Span(self.d)
        power = unit
        for _ in range(width):
            span.coordinates(power)
            if not krylov.insert(power):
                break
            power = self.mul(power, theta)
        if len(krylov.vectors) != width:
            return None
        return krylov, power

    def localized_basis(self, idempotent: Element) -> list[Element]:
        if not idempotent or self.mul(idempotent, idempotent) != idempotent:
            raise _fail("splitting_algebra: nonzero idempotent required")
        span = Span(self.d)
        for index in range(self.rank):
            span.insert(self.mul(idempotent, {index: ONE}))
        return span.vectors


def _record_fixed_column(
    algebra: SplittingAlgebra,
    span: Span,
    matrix_rows: list[Element],
    column: int,
    vector: Element,
    permutation: tuple[int, ...],
) -> None:
    coordinates = span.coordinates(algebra.act(vector, permutation))
    for row, value in enumerate(coordinates):
        if row == column:
            value = _add(value, _neg(ONE))
        if value != ZERO:
            matrix_rows[row][column] = value


def _squarefree_relation(span: Span, krylov: Span, power: Element, radicand: int) -> Polynomial:
    span.coordinates(power)
    relation = [ONE] + [_neg(value) for value in reversed(krylov.coordinates(power))]
    ascending = list(reversed(relation))
    if len(factors._gcd(ascending, factors._derivative(ascending), radicand)) != 1:
        raise _fail("splitting_algebra: primitive polynomial is not squarefree")
    return relation


def _fields(value: object, expected: set[str], label: str) -> dict[str, Any]:
    if type(value) is not dict or set(value) != expected:
        raise _fail(f"quintic_degree: exact {label} field census required")
    return cast(dict[str, Any], value)


def _integer(value: object, expected: int, label: str) -> None:
    if type(value) is not int or value != expected:
        raise _fail(f"quintic_degree: exact {label} integer differs")


def _wire_element(element: Element) -> list[list[Any]]:
    return [[index, real._wire(element[index])] for index in sorted(element)]


def _parse_row(algebra: SplittingAlgebra, row: object, previous: int) -> tuple[int, Coordinates]:
    if type(row) is not list or len(row) != 2 or type(row[0]) is not int or not previous < row[0] < algebra.rank:
        raise _fail("quintic_degree: ordered bounded exact element indices required")
    coefficient = real._parse_coordinates(algebra.conductor, row[1])
    if coefficient == ZERO:
        raise _fail("quintic_degree: zero sparse coefficient forbidden")
    return row[0], coefficient


def _parse_element(algebra: SplittingAlgebra, value: object) -> Element:
    if type(value) is not list:
        raise _fail("quintic_degree: sparse element array required")
    result: Element = {}
    previous = -1
    for row in value:
        index, coefficient = _parse_row(algebra, row, previous)
        result[index] = coefficient
        previous = index
    return result


def _sylvester(monic: Polynomial) -> list[list[Coordinates]]:
    derivative = [(value[0] * (5 - index), value[1] * (5 - index)) for index, value in enumerate(monic[:-1])]
    matrix = [[ZERO] * 9 for _ in range(9)]
    for row in range(4):
        matrix[row][row:row + 6] = monic
    for row in range(5):
        matrix[row + 4][row:row + 5] = derivative
    return matrix


def _clear_sylvester_row(
    matrix: list[list[Coordinates]], row: int, column: int, coefficient: Coordinates, radicand: int,
) -> None:
    for index in range(column + 1, 9):
        matrix[row][index] = _add(matrix[row][index], _neg(_mul(coefficient, matrix[column][index], radicand)))


def _clear_sylvester(matrix: list[list[Coordinates]], column: int, divisor: Coordinates, radicand: int) -> None:
    for row in range(column + 1, 9):
        _clear_sylvester_row(matrix, row, column, _div(matrix[row][column], divisor, radicand), radicand)


def _sylvester_pivot(
    matrix: list[list[Coordinates]], column: int, determinant: Coordinates, radicand: int,
) -> Coordinates | None:
    pivot = next((row for row in range(column, 9) if matrix[row][column] != ZERO), None)
    if pivot is None:
        return None
    if pivot != column:
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        determinant = _neg(determinant)
    divisor = matrix[column][column]
    _clear_sylvester(matrix, column, divisor, radicand)
    return _mul(determinant, divisor, radicand)


def _discriminant(monic: Polynomial, radicand: int) -> Coordinates:
    """Sylvester determinant, with exact E pivots; monic quintic sign is +1."""
    matrix = _sylvester(monic)
    determinant = ONE
    for column in range(9):
        updated = _sylvester_pivot(matrix, column, determinant, radicand)
        if updated is None:
            return ZERO
        determinant = updated
    return determinant


def _quintic_input(conductor: object, coefficients: object) -> tuple[int, int, Polynomial, Polynomial]:
    _scan_public(conductor, "conductor")
    _scan_public(coefficients, "coefficient")
    number = factors._require_conductor(conductor)
    radicand, values = factors._domain(number, coefficients)
    if len(values) != 6:
        raise _fail("quintic_degree: degree-five polynomial required", degree=len(values) - 1)
    return number, radicand, values, [_div(value, values[0], radicand) for value in values]


def _irreducible(conductor: int, monic: Polynomial, factorization: Mapping[str, Any]) -> None:
    rows = factorization["factors"]
    if (
        len(rows) != 1
        or type(rows[0]["multiplicity"]) is not int
        or rows[0]["multiplicity"] != 1
        or factors._parse_polynomial(conductor, rows[0]["polynomial"]) != monic
    ):
        raise _fail("quintic_degree: irreducibility over actual E is required")


def _pattern(factorization: Mapping[str, Any]) -> list[int]:
    if any(type(row["multiplicity"]) is not int or row["multiplicity"] != 1 for row in factorization["factors"]):
        raise _fail("quintic_degree: resolvent must have distinct irreducible factors")
    return sorted(len(row["polynomial"]) - 1 for row in factorization["factors"])


def _fixed_record(
    algebra: SplittingAlgebra, generators: list[tuple[int, ...]], basis: list[Element], unit: Element,
) -> dict[str, Any]:
    parameter, theta, polynomial = algebra.primitive(basis, unit)
    return {
        "generators": [list(item) for item in generators],
        "dimension": len(basis),
        "basis": [_wire_element(vector) for vector in basis],
        "primitive_parameter": parameter,
        "primitive_element": _wire_element(theta),
        "polynomial": factors._wire(polynomial),
        "factorization": factors.factor_polynomial(algebra.conductor, polynomial),
    }


def _require_generators(supplied: object, generators: list[tuple[int, ...]]) -> None:
    expected = [list(item) for item in generators]
    if type(supplied) is not list or supplied != expected:
        raise _fail("quintic_degree: root-label generators differ")
    if any(type(row) is not list or any(type(index) is not int for index in row) for row in supplied):
        raise _fail("quintic_degree: root-label generators differ")


def _require_one_fixed(algebra: SplittingAlgebra, span: Span, vector: Element, generators: list[tuple[int, ...]], unit: Element) -> None:
    if not span.insert(vector):
        raise _fail("quintic_degree: fixed basis is linearly dependent")
    if any(algebra.act(vector, permutation) != vector for permutation in generators):
        raise _fail("quintic_degree: basis vector is not subgroup-invariant")
    if algebra.mul(unit, vector) != vector:
        raise _fail("quintic_degree: fixed vector outside unital component")


def _require_fixed_basis(
    algebra: SplittingAlgebra, record: Mapping[str, Any], generators: list[tuple[int, ...]], dimension: int, unit: Element,
) -> tuple[list[Element], Span]:
    if type(record["basis"]) is not list or len(record["basis"]) != dimension:
        raise _fail("quintic_degree: full fixed basis census required")
    basis = [_parse_element(algebra, vector) for vector in record["basis"]]
    span = Span(algebra.d)
    for vector in basis:
        _require_one_fixed(algebra, span, vector, generators, unit)
    return basis, span


def _require_kernel(algebra: SplittingAlgebra, span: Span, generators: list[tuple[int, ...]], dimension: int, ambient: list[Element] | None) -> None:
    # Compare subspaces, not a preferred basis. This independently recounts the kernel.
    actual = algebra.fixed_basis(generators, ambient)
    if len(actual) != dimension:
        raise _fail("quintic_degree: exact invariant kernel dimension differs")
    for vector in actual:
        span.coordinates(vector)


def _require_primitive_binding(
    algebra: SplittingAlgebra, record: Mapping[str, Any], basis: list[Element], unit: Element,
) -> tuple[Element, Polynomial]:
    parameter = _parameter(record["primitive_parameter"], "quintic_degree: exact nonnegative primitive parameter required")
    _, theta, polynomial = algebra.primitive(basis, unit, parameter)
    if _parse_element(algebra, record["primitive_element"]) != theta:
        raise _fail("quintic_degree: primitive element does not bind to parameter and basis")
    if factors._parse_polynomial(algebra.conductor, record["polynomial"]) != polynomial:
        raise _fail("quintic_degree: restricted primitive polynomial differs")
    if algebra.evaluate(polynomial, theta, unit):
        raise _fail("quintic_degree: primitive polynomial does not annihilate element")
    factors.validate_factorization(algebra.conductor, polynomial, record["factorization"])
    return theta, polynomial


def _fixed_validate(
    algebra: SplittingAlgebra,
    record: object,
    generators: list[tuple[int, ...]],
    dimension: int,
    unit: Element,
    ambient: list[Element] | None = None,
) -> tuple[Element, Polynomial]:
    checked = _fields(record, FIXED_FIELDS, "fixed algebra")
    _integer(checked["dimension"], dimension, "fixed dimension")
    _require_generators(checked["generators"], generators)
    basis, span = _require_fixed_basis(algebra, checked, generators, dimension, unit)
    _require_kernel(algebra, span, generators, dimension, ambient)
    return _require_primitive_binding(algebra, checked, basis, unit)


def _root(conductor: int, factorization: Mapping[str, Any]) -> Coordinates:
    linear = [row for row in factorization["factors"] if len(row["polynomial"]) == 2]
    if len(linear) != 1:
        raise _fail("quintic_degree: unique E resolvent root required")
    return _neg(factors._parse_polynomial(conductor, linear[0]["polynomial"])[1])


def _resolvent_quotient(algebra: SplittingAlgebra, polynomial: Polynomial, root: Coordinates) -> Polynomial:
    quotient, remainder = factors._pdivmod(list(reversed(polynomial)), [_neg(root), ONE], algebra.d)
    if remainder:
        raise _fail("quintic_degree: supplied E value is not a resolvent root")
    return list(reversed(quotient))


def _idempotent_scalar(quotient: Polynomial, root: Coordinates, radicand: int) -> Coordinates:
    denominator = ZERO
    for coefficient in quotient:
        denominator = _add(_mul(denominator, root, radicand), coefficient)
    if denominator == ZERO:
        raise _fail("quintic_degree: idempotent scalar denominator is zero")
    return _div(ONE, denominator, radicand)


def _require_idempotent(algebra: SplittingAlgebra, idempotent: Element, theta: Element, root: Coordinates) -> Element:
    if not idempotent or algebra.mul(idempotent, idempotent) != idempotent:
        raise _fail("quintic_degree: fiber element is not a nonzero idempotent")
    if algebra.mul(theta, idempotent) != algebra.scale(idempotent, root):
        raise _fail("quintic_degree: idempotent selects wrong primitive fiber")
    if any(algebra.act(idempotent, permutation) != idempotent for permutation in (TRANSLATION, DILATION)):
        raise _fail("quintic_degree: idempotent is not H-invariant")
    return idempotent


def _idempotent(algebra: SplittingAlgebra, polynomial: Polynomial, theta: Element, root: Coordinates) -> Element:
    quotient = _resolvent_quotient(algebra, polynomial, root)
    scalar = _idempotent_scalar(quotient, root, algebra.d)
    return _require_idempotent(algebra, algebra.scale(algebra.evaluate(quotient, theta), scalar), theta, root)


def _metacyclic(local_pattern: list[int] | None, square: bool) -> tuple[str, int] | None:
    if local_pattern == [1, 1, 1, 1] and square:
        return "C5", 5
    if local_pattern == [2, 2] and square:
        return "D5", 10
    if local_pattern == [4] and not square:
        return "F20", 20
    return None


def _classify(square: object, full_pattern: list[int], local_pattern: list[int] | None) -> tuple[str, int]:
    if type(square) is not bool:
        raise _fail("quintic_degree: exact discriminant Boolean required")
    if full_pattern == [6] and local_pattern is None:
        return ("A5", 60) if square else ("S5", 120)
    if full_pattern == [1, 5]:
        group = _metacyclic(local_pattern, square)
        if group is not None:
            return group
    raise _fail("quintic_degree: inconsistent resolvent pattern or discriminant")


def _require_nonzero(discriminant: Coordinates) -> None:
    if discriminant == ZERO:
        raise _fail("quintic_degree: irreducible polynomial has zero discriminant")


def _localized_record(
    algebra: SplittingAlgebra, conductor: int, full: Mapping[str, Any],
) -> tuple[dict[str, Any], list[int]]:
    root = _root(conductor, full["factorization"])
    theta = _parse_element(algebra, full["primitive_element"])
    polynomial = factors._parse_polynomial(conductor, full["polynomial"])
    idempotent = _idempotent(algebra, polynomial, theta, root)
    ideal_basis = algebra.localized_basis(idempotent)
    if len(ideal_basis) != 20:
        raise _fail("quintic_degree: selected ideal dimension must be twenty")
    cyclic = algebra.fixed_basis([TRANSLATION], ideal_basis)
    if len(cyclic) != 4:
        raise _fail("quintic_degree: localized C-fixed dimension must be four")
    record = _fixed_record(algebra, [TRANSLATION], cyclic, idempotent)
    localized = {
        "root": real._wire(root),
        "idempotent": _wire_element(idempotent),
        "ideal_dimension": 20,
        "ideal_basis": [_wire_element(vector) for vector in ideal_basis],
        "cyclic_fixed_algebra": record,
    }
    return localized, _pattern(record["factorization"])


def quintic_splitting_degree(conductor: object, coefficients: object) -> dict[str, Any]:
    number, radicand, values, monic = _quintic_input(conductor, coefficients)
    factorization = factors.factor_polynomial(number, values)
    _irreducible(number, monic, factorization)
    algebra = SplittingAlgebra(number, values)
    discriminant = _discriminant(monic, radicand)
    _require_nonzero(discriminant)
    square = real.square_certificate(number, discriminant)
    basis = algebra.fixed_basis([TRANSLATION, DILATION])
    if len(basis) != 6:
        raise _fail("quintic_degree: H-fixed dimension must be six")
    full = _fixed_record(algebra, [TRANSLATION, DILATION], basis, algebra.unit)
    full_pattern = _pattern(full["factorization"])
    localized: dict[str, Any] | None = None
    local_pattern: list[int] | None = None
    if full_pattern == [1, 5]:
        localized, local_pattern = _localized_record(algebra, number, full)
    group, degree = _classify(square["is_square"], full_pattern, local_pattern)
    return {
        "schema": SCHEMA,
        "authority_effect": "None",
        "algorithm": ALGORITHM,
        "scope": SCOPE,
        "conductor": number,
        "real_generator_radicand": radicand,
        "coefficient_field": factors._field(radicand),
        "algebra_rank": algebra.rank,
        "coefficients": factors._wire(values),
        "monic_polynomial": factors._wire(monic),
        "factorization": factorization,
        "discriminant": real._wire(discriminant),
        "discriminant_square": square,
        "full_fixed_algebra": full,
        "localized_fixed_algebra": localized,
        "galois_group": group,
        "degree_over_real_field": degree,
    }


def _require_metadata(certificate: Mapping[str, Any], radicand: int) -> None:
    expected = {
        "schema": SCHEMA,
        "authority_effect": "None",
        "algorithm": ALGORITHM,
        "scope": SCOPE,
        "coefficient_field": factors._field(radicand),
    }
    if any(type(certificate[key]) is not str or certificate[key] != value for key, value in expected.items()):
        raise _fail("quintic_degree: metadata binding differs")


def _require_polynomial_bindings(
    conductor: int, certificate: Mapping[str, Any], values: Polynomial, monic: Polynomial,
) -> None:
    if factors._parse_polynomial(conductor, certificate["coefficients"]) != values:
        raise _fail("quintic_degree: original polynomial binding differs")
    if factors._parse_polynomial(conductor, certificate["monic_polynomial"]) != monic:
        raise _fail("quintic_degree: monic polynomial binding differs")


def _require_discriminant(conductor: int, monic: Polynomial, radicand: int, certificate: Mapping[str, Any]) -> Coordinates:
    discriminant = _discriminant(monic, radicand)
    if discriminant == ZERO or real._parse_coordinates(conductor, certificate["discriminant"]) != discriminant:
        raise _fail("quintic_degree: nonzero discriminant binding differs")
    real.validate_square_certificate(conductor, discriminant, certificate["discriminant_square"])
    return discriminant


def _require_ideal_basis(algebra: SplittingAlgebra, localized: Mapping[str, Any], idempotent: Element, radicand: int) -> list[Element]:
    _integer(localized["ideal_dimension"], 20, "ideal dimension")
    if type(localized["ideal_basis"]) is not list or len(localized["ideal_basis"]) != 20:
        raise _fail("quintic_degree: full ideal basis census required")
    ideal_basis = [_parse_element(algebra, vector) for vector in localized["ideal_basis"]]
    span = Span(radicand)
    for vector in ideal_basis:
        if not span.insert(vector) or algebra.mul(idempotent, vector) != vector:
            raise _fail("quintic_degree: independent idempotent-ideal basis required")
    return ideal_basis


def _require_ideal_rank(algebra: SplittingAlgebra, span_vectors: list[Element], idempotent: Element) -> None:
    actual = algebra.localized_basis(idempotent)
    if len(actual) != 20:
        raise _fail("quintic_degree: multiplication-by-idempotent rank differs")
    span = Span(algebra.d)
    for vector in span_vectors:
        if not span.insert(vector):
            raise _fail("quintic_degree: independent idempotent-ideal basis required")
    for vector in actual:
        span.coordinates(vector)


def _validate_localized(
    algebra: SplittingAlgebra,
    conductor: int,
    full: Mapping[str, Any],
    localized: object,
    theta: Element,
    polynomial: Polynomial,
) -> list[int]:
    checked = _fields(localized, LOCAL_FIELDS, "localized algebra")
    root = _root(conductor, full["factorization"])
    if real._parse_coordinates(conductor, checked["root"]) != root:
        raise _fail("quintic_degree: localized E-root binding differs")
    idempotent = _idempotent(algebra, polynomial, theta, root)
    if _parse_element(algebra, checked["idempotent"]) != idempotent:
        raise _fail("quintic_degree: localized idempotent binding differs")
    ideal_basis = _require_ideal_basis(algebra, checked, idempotent, algebra.d)
    _require_ideal_rank(algebra, ideal_basis, idempotent)
    cyclic = checked["cyclic_fixed_algebra"]
    _fixed_validate(algebra, cyclic, [TRANSLATION], 4, idempotent, ideal_basis)
    return _pattern(cyclic["factorization"])


def validate_quintic_degree(conductor: object, coefficients: object, certificate: object) -> None:
    number, radicand, values, monic = _quintic_input(conductor, coefficients)
    checked = _fields(certificate, RESULT_FIELDS, "result")
    _require_metadata(checked, radicand)
    for key, value in (("conductor", number), ("real_generator_radicand", radicand), ("algebra_rank", 120)):
        _integer(checked[key], value, key)
    _require_polynomial_bindings(number, checked, values, monic)
    factors.validate_factorization(number, values, checked["factorization"])
    _irreducible(number, monic, checked["factorization"])
    _require_discriminant(number, monic, radicand, checked)
    algebra = SplittingAlgebra(number, values)
    full = checked["full_fixed_algebra"]
    theta, polynomial = _fixed_validate(algebra, full, [TRANSLATION, DILATION], 6, algebra.unit)
    full_pattern = _pattern(full["factorization"])
    localized = checked["localized_fixed_algebra"]
    local_pattern: list[int] | None = None
    if full_pattern == [1, 5]:
        local_pattern = _validate_localized(algebra, number, full, localized, theta, polynomial)
    elif localized is not None:
        raise _fail("quintic_degree: inapplicable localized algebra must be null")
    group, degree = _classify(checked["discriminant_square"]["is_square"], full_pattern, local_pattern)
    if type(checked["galois_group"]) is not str or checked["galois_group"] != group:
        raise _fail("quintic_degree: Galois group differs from exact arithmetic")
    _integer(checked["degree_over_real_field"], degree, "splitting degree")


def dispatch(request: object) -> dict[str, Any]:
    checked = _fields(request, REQUEST_FIELDS, "request")
    if type(checked["operation"]) is not str or checked["operation"] != "quintic_splitting_degree":
        raise _fail("quintic_degree: quintic_splitting_degree operation required")
    conductor = checked["conductor"]
    return quintic_splitting_degree(conductor, factors._parse_polynomial(factors._require_conductor(conductor), checked["coefficients"]))


def _reject_inexact(token: str) -> None:
    raise _fail("quintic_degree: inexact JSON number forbidden", token=token)


def main() -> int:
    try:
        if len(sys.argv) != 1:
            raise _fail("quintic_degree: stdin request only; no CLI arguments permitted")
        request = json.loads(
            sys.stdin.buffer.read(),
            parse_int=real._integer_from_text,
            parse_float=_reject_inexact,
            parse_constant=_reject_inexact,
        )
        result = dispatch(request)
    except (ValueError, TypeError, ZeroDivisionError) as error:
        print(str(error), file=sys.stderr)
        return 2
    sys.stdout.buffer.write((json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
