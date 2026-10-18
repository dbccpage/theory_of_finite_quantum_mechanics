"""Exact finite splitting algebras, not assumed fields. AuthorityEffect: None.

All divisions are in E. Elements of the splitting algebra may be zero divisors.
The quintic classifier uses fixed spaces and localized, separating resolvents.
"""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import product
import json
import sys
from typing import Any

from . import field_factors as factors
from . import field_squares as real


ZERO = factors.ZERO
ONE = factors.ONE
Coordinates = tuple[Q, Q]
Element = dict[int, Coordinates]
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
FIXED_FIELDS = {"generators", "dimension", "basis", "primitive_parameter",
                "primitive_element", "polynomial", "factorization"}


def _add(a, b):
    return a[0] + b[0], a[1] + b[1]


def _neg(a):
    return -a[0], -a[1]


def _mul(a, b, d):
    if not a[1]:
        return a[0] * b[0], a[0] * b[1]
    if not b[1]:
        return a[0] * b[0], a[1] * b[0]
    return a[0] * b[0] + d * a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def _div(a, b, d):
    if not b[1]:
        if not b[0]:
            raise ValueError("splitting_algebra: division by zero E coefficient")
        return a[0] / b[0], a[1] / b[0]
    return factors._div(a, b, d)


def _accumulate(target, key, value):
    if value == ZERO:
        return
    total = _add(target.get(key, ZERO), value)
    if total == ZERO:
        target.pop(key, None)
    else:
        target[key] = total


def _linear(vectors, coefficients, d):
    out = {}
    for vector, coefficient in zip(vectors, coefficients, strict=True):
        if coefficient != ZERO:
            for key, value in vector.items():
                _accumulate(out, key, _mul(value, coefficient, d))
    return out


class Span:
    """Incremental exact column basis with input-order, unscaled generators."""

    def __init__(self, d):
        self.d = d
        self.vectors = []
        self.rows = {}  # pivot -> (reduced vector, coordinates in original basis)

    def reduce(self, vector):
        remainder = dict(vector)
        coordinates = {}
        for pivot in sorted(self.rows):
            coefficient = remainder.get(pivot, ZERO)
            if coefficient == ZERO:
                continue
            row, expression = self.rows[pivot]
            for key, value in row.items():
                _accumulate(remainder, key, _neg(_mul(coefficient, value, self.d)))
            for key, value in expression.items():
                _accumulate(coordinates, key, _mul(coefficient, value, self.d))
        return remainder, coordinates

    def insert(self, vector):
        remainder, coordinates = self.reduce(vector)
        if not remainder:
            return False
        pivot = min(remainder)
        divisor = remainder[pivot]
        row = {key: _div(value, divisor, self.d) for key, value in remainder.items()}
        expression = {key: _neg(_div(value, divisor, self.d))
                      for key, value in coordinates.items()}
        expression[len(self.vectors)] = _div(ONE, divisor, self.d)
        self.rows[pivot] = row, expression
        self.vectors.append(dict(vector))
        return True

    def coordinates(self, vector):
        remainder, coordinates = self.reduce(vector)
        if remainder:
            raise ValueError("splitting_algebra: vector outside certified subspace")
        return [coordinates.get(i, ZERO) for i in range(len(self.vectors))]


def _kernel(rows, width, d):
    """RREF: columns ascending, first available pivot row, all-row elimination."""
    rows = [dict(row) for row in rows]
    pivots = []
    for column in range(width):
        selected = next((i for i in range(len(pivots), len(rows))
                         if rows[i].get(column, ZERO) != ZERO), None)
        if selected is None:
            continue
        index = len(pivots)
        rows[index], rows[selected] = rows[selected], rows[index]
        divisor = rows[index][column]
        rows[index] = {key: _div(value, divisor, d) for key, value in rows[index].items()}
        for i, row in enumerate(rows):
            coefficient = row.get(column, ZERO)
            if i != index and coefficient != ZERO:
                for key, value in rows[index].items():
                    _accumulate(row, key, _neg(_mul(coefficient, value, d)))
        pivots.append(column)
    result = []
    for column in range(width):
        if column in pivots:
            continue
        vector = {column: ONE}
        for i, pivot in enumerate(pivots):
            value = rows[i].get(column, ZERO)
            if value != ZERO:
                vector[pivot] = _neg(value)
        result.append(vector)
    return result


class SplittingAlgebra:
    """Successive monic root adjunction for separable degree two through five."""

    def __init__(self, conductor: int, coefficients: Any):
        self.d, self.coefficients = factors._domain(conductor, coefficients)
        self.conductor = conductor
        self.n = len(self.coefficients) - 1
        if not 2 <= self.n <= 5:
            raise ValueError("splitting_algebra: polynomial degree must be two through five")
        self.monic = [_div(value, self.coefficients[0], self.d) for value in self.coefficients]
        ascending = list(reversed(self.monic))
        if len(factors._gcd(ascending, factors._derivative(ascending), self.d)) != 1:
            raise ValueError("splitting_algebra: separable polynomial required")
        self.bounds = tuple(range(self.n, 1, -1))
        self.exponents = sorted(product(*(range(bound) for bound in self.bounds)),
                                key=lambda exponent: (sum(exponent), exponent))
        self.indices = {exponent: i for i, exponent in enumerate(self.exponents)}
        self.rank = len(self.exponents)
        self.unit = {0: ONE}
        self._normal_cache = {}
        self._actions = {}
        zero_exp = (0,) * (self.n - 1)
        residual = [{zero_exp: coefficient} if coefficient != ZERO else {}
                    for coefficient in ascending]
        self.relations = []
        for variable, bound in enumerate(self.bounds):
            quotient = [{} for _ in range(bound)]
            quotient[-1] = dict(residual[-1])
            for k in range(bound - 1, 0, -1):
                quotient[k - 1] = dict(residual[k])
                for exponent, value in quotient[k].items():
                    shifted = list(exponent)
                    shifted[variable] += 1
                    _accumulate(quotient[k - 1], tuple(shifted), value)
            relation = dict(residual[0])
            for exponent, value in quotient[0].items():
                shifted = list(exponent)
                shifted[variable] += 1
                _accumulate(relation, tuple(shifted), value)
            leading = list(zero_exp)
            leading[variable] = bound
            if relation.pop(tuple(leading), None) != ONE:
                raise ValueError("splitting_algebra: triangular relation is not monic")
            self.relations.append({exponent: _neg(value) for exponent, value in relation.items()})
            residual = quotient
        self.roots = []
        for variable in range(self.n - 1):
            exponent = list(zero_exp)
            exponent[variable] = 1
            self.roots.append({self.indices[tuple(exponent)]: ONE})
        last = self.scale(self.unit, _neg(self.monic[1]))
        for root in self.roots:
            last = self.add(last, self.scale(root, (Q(-1), Q(0))))
        self.roots.append(last)

    def normal(self, exponent):
        if exponent in self.indices:
            return {self.indices[exponent]: ONE}
        if exponent in self._normal_cache:
            return self._normal_cache[exponent]
        variable = max(i for i, bound in enumerate(self.bounds) if exponent[i] >= bound)
        shift = list(exponent)
        shift[variable] -= self.bounds[variable]
        out = {}
        for replacement, coefficient in self.relations[variable].items():
            target = tuple(a + b for a, b in zip(shift, replacement, strict=True))
            for key, value in self.normal(target).items():
                _accumulate(out, key, _mul(coefficient, value, self.d))
        self._normal_cache[exponent] = out
        return out

    def add(self, left, right):
        result = dict(left)
        for key, value in right.items():
            _accumulate(result, key, value)
        return result

    def scale(self, element, coefficient):
        if coefficient == ZERO:
            return {}
        return {key: value for key, old in element.items()
                if (value := _mul(old, coefficient, self.d)) != ZERO}

    def mul(self, left, right):
        # First combine equal exponent sums, then reduce once per monomial.
        raw = {}
        for i, a in left.items():
            for j, b in right.items():
                exponent = tuple(x + y for x, y in zip(self.exponents[i], self.exponents[j], strict=True))
                _accumulate(raw, exponent, _mul(a, b, self.d))
        out = {}
        for exponent, coefficient in raw.items():
            for key, value in self.normal(exponent).items():
                _accumulate(out, key, _mul(coefficient, value, self.d))
        return out

    def evaluate(self, coefficients, element, unit=None):
        unit = self.unit if unit is None else unit
        out = {}
        for coefficient in coefficients:
            out = self.add(self.mul(out, element), self.scale(unit, coefficient))
        return out

    def action_columns(self, permutation):
        permutation = tuple(permutation)
        if (len(permutation) != self.n or any(type(i) is not int for i in permutation)
                or sorted(permutation) != list(range(self.n))):
            raise ValueError("splitting_algebra: exact root permutation required")
        if permutation not in self._actions:
            images = []
            for exponent in self.exponents:
                variable = next((i for i, power in enumerate(exponent) if power), None)
                if variable is None:
                    images.append(self.unit)
                else:
                    predecessor = list(exponent)
                    predecessor[variable] -= 1
                    images.append(self.mul(images[self.indices[tuple(predecessor)]],
                                           self.roots[permutation[variable]]))
            self._actions[permutation] = images
        return self._actions[permutation]

    def act(self, element, permutation):
        columns = self.action_columns(permutation)
        return _linear([columns[i] for i in element], list(element.values()), self.d)

    def fixed_basis(self, permutations, ambient=None):
        ambient = [{i: ONE} for i in range(self.rank)] if ambient is None else ambient
        span = Span(self.d)
        for vector in ambient:
            if not span.insert(vector):
                raise ValueError("splitting_algebra: dependent ambient basis")
        rows = []
        for permutation in permutations:
            matrix_rows = [{} for _ in ambient]
            for column, vector in enumerate(ambient):
                coordinates = span.coordinates(self.act(vector, permutation))
                for row, value in enumerate(coordinates):
                    if row == column:
                        value = _add(value, _neg(ONE))
                    if value != ZERO:
                        matrix_rows[row][column] = value
            rows.extend(matrix_rows)
        return [_linear(ambient, [vector.get(i, ZERO) for i in range(len(ambient))], self.d)
                for vector in _kernel(rows, len(ambient), self.d)]

    def primitive(self, basis, unit=None, parameter=None):
        unit = self.unit if unit is None else unit
        m = len(basis)
        span = Span(self.d)
        for vector in basis:
            if not span.insert(vector):
                raise ValueError("splitting_algebra: dependent fixed basis")
        span.coordinates(unit)
        bound = (m - 1) * m * (m - 1) // 2
        if parameter is not None and (type(parameter) is not int or parameter < 0):
            raise ValueError("splitting_algebra: nonnegative exact primitive parameter required")
        candidates = range(bound + 1) if parameter is None else [parameter]
        for candidate in candidates:
            theta = _linear(basis, [(Q(candidate ** j), Q(0)) for j in range(m)], self.d)
            krylov = Span(self.d)
            power = unit
            for _ in range(m):
                span.coordinates(power)
                if not krylov.insert(power):
                    break
                power = self.mul(power, theta)
            if len(krylov.vectors) != m:
                continue
            span.coordinates(power)
            relation = [ONE] + [_neg(value) for value in reversed(krylov.coordinates(power))]
            ascending = list(reversed(relation))
            if len(factors._gcd(ascending, factors._derivative(ascending), self.d)) != 1:
                raise ValueError("splitting_algebra: primitive polynomial is not squarefree")
            return candidate, theta, relation
        raise ValueError("splitting_algebra: primitive Krylov rank failed for parameter family")

    def localized_basis(self, idempotent):
        if not idempotent or self.mul(idempotent, idempotent) != idempotent:
            raise ValueError("splitting_algebra: nonzero idempotent required")
        span = Span(self.d)
        for i in range(self.rank):
            span.insert(self.mul(idempotent, {i: ONE}))
        return span.vectors


def _fields(value, expected, label):
    if type(value) is not dict or set(value) != expected:
        raise ValueError(f"quintic_degree: exact {label} field census required")


def _integer(value, expected, label):
    if type(value) is not int or value != expected:
        raise ValueError(f"quintic_degree: exact {label} integer differs")


def _wire_element(element):
    return [[index, real._wire(element[index])] for index in sorted(element)]


def _parse_element(algebra, value):
    if type(value) is not list:
        raise ValueError("quintic_degree: sparse element array required")
    result, previous = {}, -1
    for row in value:
        if (type(row) is not list or len(row) != 2 or type(row[0]) is not int
                or not previous < row[0] < algebra.rank):
            raise ValueError("quintic_degree: ordered bounded exact element indices required")
        coefficient = real._parse_coordinates(algebra.conductor, row[1])
        if coefficient == ZERO:
            raise ValueError("quintic_degree: zero sparse coefficient forbidden")
        result[row[0]] = coefficient
        previous = row[0]
    return result


def _discriminant(monic, d):
    """Sylvester determinant, with exact E pivots; monic quintic sign is +1."""
    derivative = [(value[0] * (5 - i), value[1] * (5 - i))
                  for i, value in enumerate(monic[:-1])]
    matrix = [[ZERO] * 9 for _ in range(9)]
    for row in range(4):
        matrix[row][row:row + 6] = monic
    for row in range(5):
        matrix[row + 4][row:row + 5] = derivative
    determinant = ONE
    for column in range(9):
        pivot = next((row for row in range(column, 9) if matrix[row][column] != ZERO), None)
        if pivot is None:
            return ZERO
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            determinant = _neg(determinant)
        divisor = matrix[column][column]
        determinant = _mul(determinant, divisor, d)
        for row in range(column + 1, 9):
            coefficient = _div(matrix[row][column], divisor, d)
            for j in range(column + 1, 9):
                matrix[row][j] = _add(matrix[row][j], _neg(_mul(coefficient, matrix[column][j], d)))
    return determinant


def _input(conductor, coefficients):
    d, values = factors._domain(conductor, coefficients)
    if len(values) != 6:
        raise ValueError("quintic_degree: degree-five polynomial required")
    return d, values, [_div(value, values[0], d) for value in values]


def _irreducible(conductor, monic, factorization):
    rows = factorization["factors"]
    if (len(rows) != 1 or type(rows[0]["multiplicity"]) is not int
            or rows[0]["multiplicity"] != 1
            or factors._parse_polynomial(conductor, rows[0]["polynomial"]) != monic):
        raise ValueError("quintic_degree: irreducibility over actual E is required")


def _pattern(factorization):
    if any(type(row["multiplicity"]) is not int or row["multiplicity"] != 1
           for row in factorization["factors"]):
        raise ValueError("quintic_degree: resolvent must have distinct irreducible factors")
    return sorted(len(row["polynomial"]) - 1 for row in factorization["factors"])


def _fixed_record(algebra, generators, basis, unit):
    parameter, theta, polynomial = algebra.primitive(basis, unit)
    return {"generators": [list(p) for p in generators], "dimension": len(basis),
            "basis": [_wire_element(vector) for vector in basis],
            "primitive_parameter": parameter, "primitive_element": _wire_element(theta),
            "polynomial": factors._wire(polynomial),
            "factorization": factors.factor_polynomial(algebra.conductor, polynomial)}


def _fixed_validate(algebra, record, generators, dimension, unit, ambient=None):
    _fields(record, FIXED_FIELDS, "fixed algebra")
    _integer(record["dimension"], dimension, "fixed dimension")
    supplied = record["generators"]
    if (type(supplied) is not list or any(type(p) is not list for p in supplied)
            or any(type(i) is not int for p in supplied for i in p)
            or supplied != [list(p) for p in generators]):
        raise ValueError("quintic_degree: root-label generators differ")
    if type(record["basis"]) is not list or len(record["basis"]) != dimension:
        raise ValueError("quintic_degree: full fixed basis census required")
    basis = [_parse_element(algebra, vector) for vector in record["basis"]]
    span = Span(algebra.d)
    for vector in basis:
        if not span.insert(vector):
            raise ValueError("quintic_degree: fixed basis is linearly dependent")
        if any(algebra.act(vector, p) != vector for p in generators):
            raise ValueError("quintic_degree: basis vector is not subgroup-invariant")
        if algebra.mul(unit, vector) != vector:
            raise ValueError("quintic_degree: fixed vector outside unital component")
    # Compare subspaces, not a preferred basis. This independently recounts the kernel.
    actual = algebra.fixed_basis(generators, ambient)
    if len(actual) != dimension:
        raise ValueError("quintic_degree: exact invariant kernel dimension differs")
    for vector in actual:
        span.coordinates(vector)
    if type(record["primitive_parameter"]) is not int or record["primitive_parameter"] < 0:
        raise ValueError("quintic_degree: exact nonnegative primitive parameter required")
    parameter, theta, polynomial = algebra.primitive(basis, unit, record["primitive_parameter"])
    if _parse_element(algebra, record["primitive_element"]) != theta:
        raise ValueError("quintic_degree: primitive element does not bind to parameter and basis")
    if factors._parse_polynomial(algebra.conductor, record["polynomial"]) != polynomial:
        raise ValueError("quintic_degree: restricted primitive polynomial differs")
    if algebra.evaluate(polynomial, theta, unit):
        raise ValueError("quintic_degree: primitive polynomial does not annihilate element")
    factors.validate_factorization(algebra.conductor, polynomial, record["factorization"])
    return theta, polynomial


def _root(conductor, factorization):
    linear = [row for row in factorization["factors"] if len(row["polynomial"]) == 2]
    if len(linear) != 1:
        raise ValueError("quintic_degree: unique E resolvent root required")
    return _neg(factors._parse_polynomial(conductor, linear[0]["polynomial"])[1])


def _idempotent(algebra, polynomial, theta, root):
    quotient, remainder = factors._pdivmod(list(reversed(polynomial)), [_neg(root), ONE], algebra.d)
    if remainder:
        raise ValueError("quintic_degree: supplied E value is not a resolvent root")
    denominator = ZERO
    for coefficient in reversed(quotient):
        denominator = _add(_mul(denominator, root, algebra.d), coefficient)
    if denominator == ZERO:
        raise ValueError("quintic_degree: idempotent scalar denominator is zero")
    e = algebra.scale(algebra.evaluate(list(reversed(quotient)), theta), _div(ONE, denominator, algebra.d))
    if not e or algebra.mul(e, e) != e:
        raise ValueError("quintic_degree: fiber element is not a nonzero idempotent")
    if algebra.mul(theta, e) != algebra.scale(e, root):
        raise ValueError("quintic_degree: idempotent selects wrong primitive fiber")
    if any(algebra.act(e, p) != e for p in (TRANSLATION, DILATION)):
        raise ValueError("quintic_degree: idempotent is not H-invariant")
    return e


def _classify(square, full_pattern, local_pattern):
    if type(square) is not bool:
        raise ValueError("quintic_degree: exact discriminant Boolean required")
    if full_pattern == [6] and local_pattern is None:
        return ("A5", 60) if square else ("S5", 120)
    if full_pattern == [1, 5]:
        if local_pattern == [1, 1, 1, 1] and square:
            return "C5", 5
        if local_pattern == [2, 2] and square:
            return "D5", 10
        if local_pattern == [4] and not square:
            return "F20", 20
    raise ValueError("quintic_degree: inconsistent resolvent pattern or discriminant")


def quintic_splitting_degree(conductor: int, coefficients: Any) -> dict[str, Any]:
    d, values, monic = _input(conductor, coefficients)
    factorization = factors.factor_polynomial(conductor, values)
    _irreducible(conductor, monic, factorization)
    algebra = SplittingAlgebra(conductor, values)
    discriminant = _discriminant(monic, d)
    if discriminant == ZERO:
        raise ValueError("quintic_degree: irreducible polynomial has zero discriminant")
    square = real.square_certificate(conductor, discriminant)
    basis = algebra.fixed_basis([TRANSLATION, DILATION])
    if len(basis) != 6:
        raise ValueError("quintic_degree: H-fixed dimension must be six")
    full = _fixed_record(algebra, [TRANSLATION, DILATION], basis, algebra.unit)
    full_pattern = _pattern(full["factorization"])
    localized, local_pattern = None, None
    if full_pattern == [1, 5]:
        root = _root(conductor, full["factorization"])
        theta = _parse_element(algebra, full["primitive_element"])
        polynomial = factors._parse_polynomial(conductor, full["polynomial"])
        e = _idempotent(algebra, polynomial, theta, root)
        ideal_basis = algebra.localized_basis(e)
        if len(ideal_basis) != 20:
            raise ValueError("quintic_degree: selected ideal dimension must be twenty")
        cyclic = algebra.fixed_basis([TRANSLATION], ideal_basis)
        if len(cyclic) != 4:
            raise ValueError("quintic_degree: localized C-fixed dimension must be four")
        record = _fixed_record(algebra, [TRANSLATION], cyclic, e)
        local_pattern = _pattern(record["factorization"])
        localized = {"root": real._wire(root), "idempotent": _wire_element(e),
                     "ideal_dimension": 20, "ideal_basis": [_wire_element(v) for v in ideal_basis],
                     "cyclic_fixed_algebra": record}
    group, degree = _classify(square["is_square"], full_pattern, local_pattern)
    return {"schema": SCHEMA, "authority_effect": "None", "algorithm": ALGORITHM, "scope": SCOPE,
            "conductor": conductor, "real_generator_radicand": d, "coefficient_field": factors._field(d),
            "algebra_rank": algebra.rank, "coefficients": factors._wire(values),
            "monic_polynomial": factors._wire(monic), "factorization": factorization,
            "discriminant": real._wire(discriminant), "discriminant_square": square,
            "full_fixed_algebra": full, "localized_fixed_algebra": localized,
            "galois_group": group, "degree_over_real_field": degree}


def validate_quintic_degree(conductor: int, coefficients: Any, certificate: Any) -> None:
    d, values, monic = _input(conductor, coefficients)
    _fields(certificate, RESULT_FIELDS, "result")
    expected = {"schema": SCHEMA, "authority_effect": "None", "algorithm": ALGORITHM,
                "scope": SCOPE, "coefficient_field": factors._field(d)}
    if any(type(certificate[key]) is not str or certificate[key] != value for key, value in expected.items()):
        raise ValueError("quintic_degree: metadata binding differs")
    for key, value in (("conductor", conductor), ("real_generator_radicand", d), ("algebra_rank", 120)):
        _integer(certificate[key], value, key)
    if factors._parse_polynomial(conductor, certificate["coefficients"]) != values:
        raise ValueError("quintic_degree: original polynomial binding differs")
    if factors._parse_polynomial(conductor, certificate["monic_polynomial"]) != monic:
        raise ValueError("quintic_degree: monic polynomial binding differs")
    factors.validate_factorization(conductor, values, certificate["factorization"])
    _irreducible(conductor, monic, certificate["factorization"])
    discriminant = _discriminant(monic, d)
    if discriminant == ZERO or real._parse_coordinates(conductor, certificate["discriminant"]) != discriminant:
        raise ValueError("quintic_degree: nonzero discriminant binding differs")
    real.validate_square_certificate(conductor, discriminant, certificate["discriminant_square"])
    algebra = SplittingAlgebra(conductor, values)
    full = certificate["full_fixed_algebra"]
    theta, polynomial = _fixed_validate(algebra, full, [TRANSLATION, DILATION], 6, algebra.unit)
    full_pattern, local_pattern = _pattern(full["factorization"]), None
    localized = certificate["localized_fixed_algebra"]
    if full_pattern == [1, 5]:
        _fields(localized, {"root", "idempotent", "ideal_dimension", "ideal_basis", "cyclic_fixed_algebra"},
                "localized algebra")
        root = _root(conductor, full["factorization"])
        if real._parse_coordinates(conductor, localized["root"]) != root:
            raise ValueError("quintic_degree: localized E-root binding differs")
        e = _idempotent(algebra, polynomial, theta, root)
        if _parse_element(algebra, localized["idempotent"]) != e:
            raise ValueError("quintic_degree: localized idempotent binding differs")
        _integer(localized["ideal_dimension"], 20, "ideal dimension")
        if type(localized["ideal_basis"]) is not list or len(localized["ideal_basis"]) != 20:
            raise ValueError("quintic_degree: full ideal basis census required")
        ideal_basis = [_parse_element(algebra, vector) for vector in localized["ideal_basis"]]
        span = Span(d)
        for vector in ideal_basis:
            if not span.insert(vector) or algebra.mul(e, vector) != vector:
                raise ValueError("quintic_degree: independent idempotent-ideal basis required")
        actual = algebra.localized_basis(e)
        if len(actual) != 20:
            raise ValueError("quintic_degree: multiplication-by-idempotent rank differs")
        for vector in actual:
            span.coordinates(vector)
        cyclic = localized["cyclic_fixed_algebra"]
        _fixed_validate(algebra, cyclic, [TRANSLATION], 4, e, ideal_basis)
        local_pattern = _pattern(cyclic["factorization"])
    elif localized is not None:
        raise ValueError("quintic_degree: inapplicable localized algebra must be null")
    group, degree = _classify(certificate["discriminant_square"]["is_square"], full_pattern, local_pattern)
    if type(certificate["galois_group"]) is not str or certificate["galois_group"] != group:
        raise ValueError("quintic_degree: Galois group differs from exact arithmetic")
    _integer(certificate["degree_over_real_field"], degree, "splitting degree")


def dispatch(request: Any) -> dict[str, Any]:
    _fields(request, {"operation", "conductor", "coefficients"}, "request")
    if type(request["operation"]) is not str or request["operation"] != "quintic_splitting_degree":
        raise ValueError("quintic_degree: quintic_splitting_degree operation required")
    conductor = request["conductor"]
    return quintic_splitting_degree(conductor, factors._parse_polynomial(conductor, request["coefficients"]))


def _reject_inexact(token):
    raise ValueError(f"quintic_degree: inexact JSON number forbidden: {token}")


def main() -> int:
    try:
        if len(sys.argv) != 1:
            raise ValueError("quintic_degree: stdin request only; no CLI arguments permitted")
        request = json.loads(sys.stdin.buffer.read(), parse_int=real._integer_from_text,
                             parse_float=_reject_inexact, parse_constant=_reject_inexact)
        result = dispatch(request)
    except (ValueError, TypeError, ZeroDivisionError) as error:
        print(str(error), file=sys.stderr)
        return 2
    sys.stdout.buffer.write((json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
