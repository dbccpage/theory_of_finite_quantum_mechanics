"""Exact rational factorization by Berlekamp–Hensel recombination.

Origin: code/rust/src/linear_algebra/rational_factors.rs, which states exact
rational factorization, not a splitting-field or dependence certificate, with
internal coefficients ascending and the external protocol descending.
Claim: urn:omega:fqm:linear-algebra:rational-polynomial-factorization:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_rational_factors.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 9; AST Sonar cognitive complexity max 9; AST nesting depth max 3; lizard 1.24.1 cyclomatic complexity max 9.
Scope Fence: This file factors polynomials over Q. It does not claim a
splitting-field degree, multiplicative dependence, or a real-quadratic
extension, and it does not admit floats.
"""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations
from math import gcd, lcm
import json
import re
import sys
from typing import Any, Mapping, cast

from .field_squares import _fraction_text, _integer_from_text


ALGORITHM = "EXACT_BERLEKAMP_HENSEL_RECOMBINATION"
SCHEMA = "rational_polynomial_factorization_v1"
_RESULT_FIELDS = {
    "schema", "authority_effect", "coefficient_field", "coefficients", "content", "factors", "algorithm",
}
_FACTOR_FIELDS = {"polynomial", "multiplicity"}
_REQUEST_FIELDS = {"operation", "coefficients"}


class RationalFactorError(ValueError):
    """One violated rational-factorization invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> RationalFactorError:
    return RationalFactorError(invariant, parameters)


def _ztrim(poly: list[int]) -> list[int]:
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def _qtrim(poly: list[Q]) -> list[Q]:
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def _zadd(left: list[int], right: list[int]) -> list[int]:
    out = [0] * max(len(left), len(right))
    for index, coefficient in enumerate(left):
        out[index] += coefficient
    for index, coefficient in enumerate(right):
        out[index] += coefficient
    return _ztrim(out)


def _qadd(left: list[Q], right: list[Q]) -> list[Q]:
    out = [Q(0)] * max(len(left), len(right))
    for index, coefficient in enumerate(left):
        out[index] += coefficient
    for index, coefficient in enumerate(right):
        out[index] += coefficient
    return _qtrim(out)


def _zmul(left: list[int], right: list[int]) -> list[int]:
    if not left or not right:
        return []
    out = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] += x * y
    return _ztrim(out)


def _qmul(left: list[Q], right: list[Q]) -> list[Q]:
    if not left or not right:
        return []
    out = [Q(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] += x * y
    return _qtrim(out)


def _qdivmod(dividend: list[Q], divisor: list[Q]) -> tuple[list[Q], list[Q]]:
    if not divisor:
        raise _fail("factorization: polynomial division by zero", role="divisor")
    remainder = dividend[:]
    quotient = [Q(0)] * max(0, len(dividend) - len(divisor) + 1)
    while remainder and len(remainder) >= len(divisor):
        place = len(remainder) - len(divisor)
        scale = Q(remainder[-1]) / Q(divisor[-1])
        quotient[place] = scale
        _subtract_scaled(remainder, divisor, place, scale)
        _qtrim(remainder)
    return _qtrim(quotient), remainder


def _subtract_scaled(remainder: list[Q], divisor: list[Q], place: int, scale: Q) -> None:
    for index, coefficient in enumerate(divisor):
        remainder[place + index] -= scale * coefficient


def _exact_div(dividend: list[Q], divisor: list[Q]) -> list[Q]:
    quotient, remainder = _qdivmod(dividend, divisor)
    if remainder:
        raise _fail("factorization: nonzero exact-division remainder", degree=len(remainder) - 1)
    return quotient


def _gcd(left: list[Q], right: list[Q]) -> list[Q]:
    while right:
        left, right = right, _qdivmod(left, right)[1]
    return [Q(coefficient) / Q(left[-1]) for coefficient in left] if left else []


def _derivative(poly: list[Q]) -> list[Q]:
    return _qtrim([index * poly[index] for index in range(1, len(poly))])


def _zderivative(poly: list[int]) -> list[int]:
    return _ztrim([index * poly[index] for index in range(1, len(poly))])


def _mod(poly: list[int], prime: int) -> list[int]:
    return _ztrim([coefficient % prime for coefficient in poly])


def _mod_divmod(dividend: list[int], divisor: list[int], prime: int) -> tuple[list[int], list[int]]:
    remainder, reduced = _mod(dividend, prime), _mod(divisor, prime)
    if not reduced:
        raise _fail("factorization: modular polynomial division by zero", role="divisor")
    quotient = [0] * max(0, len(remainder) - len(reduced) + 1)
    inverse = pow(reduced[-1], -1, prime)
    while remainder and len(remainder) >= len(reduced):
        place = len(remainder) - len(reduced)
        scale = remainder[-1] * inverse % prime
        quotient[place] = scale
        _subtract_mod(remainder, reduced, place, scale, prime)
        _ztrim(remainder)
    return _ztrim(quotient), remainder


def _subtract_mod(remainder: list[int], divisor: list[int], place: int, scale: int, prime: int) -> None:
    for index, coefficient in enumerate(divisor):
        remainder[place + index] = (remainder[place + index] - scale * coefficient) % prime


def _mod_gcd(left: list[int], right: list[int], prime: int) -> list[int]:
    while right:
        left, right = right, _mod_divmod(left, right, prime)[1]
    if not left:
        return []
    inverse = pow(left[-1], -1, prime)
    return _mod([coefficient * inverse for coefficient in left], prime)


def _mod_power(base: list[int], exponent: int, modulus: list[int], prime: int) -> list[int]:
    result = [1]
    while exponent:
        if exponent % 2:
            result = _mod_divmod(_zmul(result, base), modulus, prime)[1]
        base = _mod_divmod(_zmul(base, base), modulus, prime)[1]
        exponent //= 2
    return result


def _mod_inverse(poly: list[int], modulus: list[int], prime: int) -> list[int]:
    old_r, current = poly, modulus
    old_s: list[int] = [1]
    current_s: list[int] = []
    while current:
        quotient, remainder = _mod_divmod(old_r, current, prime)
        old_r, current = current, remainder
        old_s, current_s = current_s, _bezout_step(old_s, quotient, current_s, prime)
    if len(old_r) != 1:
        raise _fail("factorization: Hensel factors are not coprime", degree=len(old_r) - 1)
    inverse = pow(old_r[0], -1, prime)
    return _mod_divmod([coefficient * inverse for coefficient in old_s], modulus, prime)[1]


def _bezout_step(old_s: list[int], quotient: list[int], current_s: list[int], prime: int) -> list[int]:
    product = _zmul(quotient, current_s)
    return _mod(_zadd(old_s, [-coefficient for coefficient in product]), prime)


def _scale_pivot(matrix: list[list[int]], index: int, column: int, prime: int) -> None:
    inverse = pow(matrix[index][column], -1, prime)
    matrix[index] = [entry * inverse % prime for entry in matrix[index]]


def _clear_column(matrix: list[list[int]], index: int, column: int, prime: int) -> None:
    for row in range(len(matrix)):
        if row != index:
            scale = matrix[row][column]
            matrix[row] = [(entry - scale * pivot) % prime for entry, pivot in zip(matrix[row], matrix[index])]


def _eliminate(matrix: list[list[int]], column: int, pivot_columns: list[int], prime: int) -> None:
    start = len(pivot_columns)
    pivot = next((row for row in range(start, len(matrix)) if matrix[row][column] % prime), None)
    if pivot is None:
        return
    matrix[start], matrix[pivot] = matrix[pivot], matrix[start]
    _scale_pivot(matrix, start, column, prime)
    _clear_column(matrix, start, column, prime)
    pivot_columns.append(column)


def _kernel_vector(
    matrix: list[list[int]], pivot_columns: list[int], column: int, width: int, prime: int,
) -> list[int]:
    vector = [0] * width
    vector[column] = 1
    for row, pivot in enumerate(pivot_columns):
        vector[pivot] = -matrix[row][column] % prime
    return _ztrim(vector)


def _nullspace(rows: list[list[int]], prime: int) -> list[list[int]]:
    matrix = [row[:] for row in rows]
    width = len(matrix[0])
    pivot_columns: list[int] = []
    for column in range(width):
        _eliminate(matrix, column, pivot_columns, prime)
    basis: list[list[int]] = []
    for column in range(width):
        if column not in pivot_columns:
            basis.append(_kernel_vector(matrix, pivot_columns, column, width, prime))
    return basis


def _berlekamp_matrix(polynomial: list[int], prime: int) -> list[list[int]]:
    degree = len(polynomial) - 1
    columns = [_mod_power([0, 1], prime * column, polynomial, prime) for column in range(degree)]
    matrix: list[list[int]] = []
    for row in range(degree):
        matrix.append(_berlekamp_row(columns, row, degree, prime))
    return matrix


def _berlekamp_row(columns: list[list[int]], row: int, degree: int, prime: int) -> list[int]:
    entries: list[int] = []
    for column in range(degree):
        coefficient = columns[column][row] if row < len(columns[column]) else 0
        entries.append((coefficient - int(row == column)) % prime)
    return entries


def _require_exact_split(remainder: list[int]) -> None:
    if remainder:
        raise _fail("factorization: Berlekamp split has a remainder", degree=len(remainder) - 1)


def _split_piece(piece: list[int], vector: list[int], constant: int, prime: int) -> list[list[int]]:
    divisor = _mod_gcd(piece, _mod(_zadd(vector, [-constant]), prime), prime)
    if not 1 < len(divisor) < len(piece):
        return [piece]
    quotient, remainder = _mod_divmod(piece, divisor, prime)
    _require_exact_split(remainder)
    return [divisor, quotient]


def _refine(pieces: list[list[int]], vector: list[int], constant: int, prime: int) -> list[list[int]]:
    refined: list[list[int]] = []
    for piece in pieces:
        refined.extend(_split_piece(piece, vector, constant, prime))
    return refined


def _split_by_vector(
    pieces: list[list[int]], vector: list[int], target: int, prime: int,
) -> tuple[list[list[int]], bool]:
    for constant in range(prime):
        pieces = _refine(pieces, vector, constant, prime)
        if len(pieces) == target:
            return sorted(pieces), True
    return pieces, False


def _census_failure(found: int, nullity: int) -> None:
    raise _fail("factorization: Berlekamp factor census differs from nullity", found=found, nullity=nullity)


def _berlekamp(polynomial: list[int], prime: int) -> list[list[int]]:
    """Monic squarefree input over the prime field; deterministic splitting."""
    reduced = _mod(polynomial, prime)
    basis = _nullspace(_berlekamp_matrix(reduced, prime), prime)
    pieces = [reduced]
    for vector in basis:
        pieces, done = _split_by_vector(pieces, vector, len(basis), prime)
        if done:
            return pieces
    _census_failure(len(pieces), len(basis))
    return pieces


def _good_prime(polynomial: list[int]) -> int:
    candidate = 2
    while True:
        prime = True
        divisor = 2
        while divisor * divisor <= candidate:
            if candidate % divisor == 0:
                prime = False
                break
            divisor += 1
        if prime and _mod_gcd(_mod(polynomial, candidate), _mod(_zderivative(polynomial), candidate), candidate) == [1]:
            return candidate
        candidate += 1


def _other_product(factors: list[list[int]], index: int, prime: int) -> list[int]:
    other = [1]
    for place, part in enumerate(factors):
        if place != index:
            other = _mod(_zmul(other, part), prime)
    return other


def _cofactor_inverses(factors: list[list[int]], prime: int) -> list[list[int]]:
    inverses: list[list[int]] = []
    for index, factor in enumerate(factors):
        inverses.append(_mod_inverse(_other_product(factors, index, prime), factor, prime))
    return inverses


def _product_mod(parts: list[list[int]], modulus: int) -> list[int]:
    product = [1]
    for part in parts:
        product = _mod(_zmul(product, part), modulus)
    return product


def _lifting_digit(error: list[int], modulus: int) -> list[int]:
    if any(coefficient % modulus for coefficient in error):
        raise _fail("factorization: Hensel product does not match input modulo current modulus", modulus=modulus)
    return [coefficient // modulus for coefficient in error]


def _apply_digit(
    part: list[int],
    correction: list[int],
    inverse: list[int],
    factor: list[int],
    modulus: int,
    prime: int,
) -> list[int]:
    delta = _mod_divmod(_zmul(correction, inverse), factor, prime)[1]
    return _zadd(part, [modulus * entry for entry in delta])


def _lift_all(
    polynomial: list[int],
    factors: list[list[int]],
    lifted: list[list[int]],
    inverses: list[list[int]],
    modulus: int,
    prime: int,
) -> list[list[int]]:
    # Reduction modulo m*p preserves (f-product)/m modulo p.
    # Reducing modulo m alone would lose the next lifting digit.
    product = _product_mod(lifted, modulus * prime)
    error = _zadd(polynomial, [-coefficient for coefficient in product])
    correction = _mod(_lifting_digit(error, modulus), prime)
    updated: list[list[int]] = []
    for index, part in enumerate(lifted):
        updated.append(_apply_digit(part, correction, inverses[index], factors[index], modulus, prime))
    return updated


def _require_lifted_product(product: list[int], target: list[int]) -> None:
    if product != target:
        raise _fail("factorization: lifted product does not match input", length=len(product))


def _hensel(
    polynomial: list[int], factors: list[list[int]], prime: int, bound: int,
) -> tuple[int, list[list[int]]]:
    """Lift all monic factors; product agrees with f modulo the returned modulus."""
    inverses = _cofactor_inverses(factors, prime)
    modulus, lifted = prime, [part[:] for part in factors]
    while modulus <= 2 * bound:
        lifted = _lift_all(polynomial, factors, lifted, inverses, modulus, prime)
        modulus *= prime
    _require_lifted_product(_product_mod(lifted, modulus), _mod(polynomial, modulus))
    return modulus, lifted


def _balanced_residue(coefficient: int, modulus: int) -> int:
    residue = coefficient % modulus
    if 2 * residue <= modulus:
        return residue
    return residue - modulus


def _center(poly: list[int], modulus: int) -> list[int]:
    return _ztrim([_balanced_residue(coefficient, modulus) for coefficient in poly])


def _integer_root_ceiling(value: int, exponent: int) -> int:
    """Least nonnegative r with r**exponent >= value, using integers only."""
    if type(value) is not int or value < 0 or type(exponent) is not int or exponent < 1:
        raise _fail("factor_bound: nonnegative integer and positive integer exponent required")
    if value < 2 or exponent == 1:
        return value
    lower, upper = 0, 1 << ((value.bit_length() + exponent - 1) // exponent)
    while lower + 1 < upper:
        middle = (lower + upper) // 2
        if middle ** exponent < value:
            lower = middle
        else:
            upper = middle
    return upper


def _root_radius(polynomial: list[int]) -> int:
    """Proved complex-root radius for a nonconstant monic integer polynomial."""
    if len(polynomial) < 2 or any(type(coefficient) is not int for coefficient in polynomial) or polynomial[-1] != 1:
        raise _fail("factor_bound: nonconstant monic integer polynomial required")
    degree = len(polynomial) - 1
    magnitude = max(_integer_root_ceiling(abs(coefficient), degree - index) for index, coefficient in enumerate(polynomial[:-1]))
    # If M>0, at |z|>=2M the sum |a_(n-k)|/|z|^k is <=1-2^-n<1.
    # M=0 means f=X^n and radius zero is valid. Retain the old Cauchy
    # bound when smaller, so the required reconstruction modulus never grows.
    return min(1 + max(abs(coefficient) for coefficient in polynomial[:-1]), 2 * magnitude)


def _integer_quotient(quotient: list[Q]) -> list[int]:
    if any(coefficient.denominator != 1 for coefficient in quotient):
        raise _fail("factorization: monic integer divisor gave noninteger quotient")
    return [int(coefficient) for coefficient in quotient]


def _trial_product(lifted: list[list[int]], indices: tuple[int, ...], modulus: int) -> list[int]:
    product = [1]
    for index in indices:
        product = _mod(_zmul(product, lifted[index]), modulus)
    return _center(product, modulus)


def _exact_integer_split(polynomial: list[int], candidate: list[int]) -> list[int] | None:
    quotient, remainder = _qdivmod([Q(coefficient) for coefficient in polynomial], [Q(coefficient) for coefficient in candidate])
    if remainder:
        return None
    return _integer_quotient(quotient)


def _search_count(
    polynomial: list[int],
    lifted: list[list[int]],
    modulus: int,
    count: int,
    n: int,
) -> tuple[list[int], list[int]] | None:
    for indices in combinations(range(len(lifted)), count):
        degree = sum(len(lifted[index]) - 1 for index in indices)
        if degree > n // 2:
            continue
        candidate = _trial_product(lifted, indices, modulus)
        quotient = _exact_integer_split(polynomial, candidate)
        if quotient is not None:
            return candidate, quotient
    return None


def _search_split(
    polynomial: list[int], lifted: list[list[int]], modulus: int,
) -> tuple[list[int], list[int]] | None:
    degree = len(polynomial) - 1
    for count in range(1, len(lifted)):
        found = _search_count(polynomial, lifted, modulus, count, degree)
        if found is not None:
            return found
    return None


def _factor_monic_integer(polynomial: list[int]) -> list[list[int]]:
    degree = len(polynomial) - 1
    if degree <= 1:
        return [polynomial]
    prime = _good_prime(polynomial)
    modular = _berlekamp(polynomial, prime)
    if len(modular) == 1:
        return [polynomial]
    # Both exact radii bound every complex root. A monic divisor of degree
    # k has coefficients bounded by (1+R)^k; only k<=floor(n/2) is needed.
    radius = _root_radius(polynomial)
    bound = (1 + radius) ** (degree // 2)
    modulus, lifted = _hensel(polynomial, modular, prime, bound)
    found = _search_split(polynomial, lifted, modulus)
    if found is None:
        return [polynomial]
    candidate, quotient = found
    return _factor_monic_integer(candidate) + _factor_monic_integer(quotient)


def _factor_squarefree(polynomial: list[Q]) -> list[list[Q]]:
    denominator = lcm(*(coefficient.denominator for coefficient in polynomial))
    integer = [int(coefficient * denominator) for coefficient in polynomial]
    common = 0
    for coefficient in integer:
        common = gcd(common, coefficient)
    integer = [coefficient // common for coefficient in integer]
    leading, degree = integer[-1], len(integer) - 1
    # Scaling y=a*x avoids nonmonic Hensel lifting without losing any factor.
    transformed = [integer[index] * leading ** (degree - 1 - index) for index in range(degree)] + [1]
    result: list[list[Q]] = []
    for factor in _factor_monic_integer(transformed):
        factor_degree = len(factor) - 1
        result.append([Q(coefficient, leading ** (factor_degree - index)) for index, coefficient in enumerate(factor)])
    return result


def _as_rational(value: object, role: str) -> Q:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where an exact rational was required", role=role)
    if isinstance(value, int) or isinstance(value, Q):
        return Q(value)
    raise _fail(
        "factorization: exact rational coefficients required",
        role=role,
        received=type(value).__name__,
    )


def _domain(coefficients: object) -> list[Q]:
    if isinstance(coefficients, (list, tuple)) and coefficients:
        values = [_as_rational(item, "coefficient") for item in coefficients]
        if not values[0]:
            raise _fail("factorization: nonzero leading coefficient required", role="leading")
        return values
    received = "empty" if isinstance(coefficients, (list, tuple)) else type(coefficients).__name__
    raise _fail("factorization: nonempty coefficient sequence required", received=received)


def _parse(value: object) -> Q:
    if isinstance(value, float):
        return _as_rational(value, "coefficient")
    if not isinstance(value, str) or re.fullmatch(r"-?(0|[1-9][0-9]*)/[1-9][0-9]*", value) is None:
        raise _fail("factorization: canonical rational string required", received=type(value).__name__)
    numerator, denominator = value.split("/")
    result = Q(_integer_from_text(numerator), _integer_from_text(denominator))
    if _fraction_text(result) != value:
        raise _fail("factorization: rational string must be reduced", received="unreduced")
    return result


def _parse_polynomial(values: object) -> list[Q]:
    if not isinstance(values, list):
        raise _fail("factorization: coefficient array required", received=type(values).__name__)
    return _domain([_parse(item) for item in values])


def _wire(values: list[Q]) -> list[str]:
    return [_fraction_text(coefficient) for coefficient in values]


def _squarefree_parts(part: list[Q], multiplicity: int) -> list[tuple[list[Q], int]]:
    if len(part) <= 1:
        return []
    return [(list(reversed(factor)), multiplicity) for factor in _factor_squarefree(part)]


def factor_polynomial(coefficients: object) -> dict[str, Any]:
    """Factor a nonzero rational polynomial, with independently testable product."""
    values = _domain(coefficients)
    polynomial = [coefficient / values[0] for coefficient in reversed(values)]
    common = _gcd(polynomial, _derivative(polynomial))
    remaining, multiplicity = _exact_div(polynomial, common), 1
    factors: list[tuple[list[Q], int]] = []
    while len(remaining) > 1:
        overlap = _gcd(remaining, common)
        factors.extend(_squarefree_parts(_exact_div(remaining, overlap), multiplicity))
        remaining, common = overlap, _exact_div(common, overlap)
        multiplicity += 1
    factors.sort(key=lambda item: item[0])
    return {
        "schema": SCHEMA,
        "authority_effect": "None",
        "coefficient_field": "Q",
        "coefficients": _wire(values),
        "content": _fraction_text(values[0]),
        "factors": [{"polynomial": _wire(poly), "multiplicity": count} for poly, count in factors],
        "algorithm": ALGORITHM,
    }


def _require_certificate(certificate: object) -> dict[str, Any]:
    if isinstance(certificate, dict) and set(certificate) == _RESULT_FIELDS:
        return cast(dict[str, Any], certificate)
    raise _fail("factorization: exact output field census required")


def _require_metadata(certificate: Mapping[str, object]) -> None:
    if certificate.get("schema") != SCHEMA or certificate.get("authority_effect") != "None":
        raise _fail("factorization: schema or arithmetic-domain binding differs")
    if certificate.get("coefficient_field") != "Q" or certificate.get("algorithm") != ALGORITHM:
        raise _fail("factorization: schema or arithmetic-domain binding differs")


def _require_input_binding(certificate: Mapping[str, object], values: list[Q]) -> None:
    if _parse_polynomial(certificate.get("coefficients")) != values:
        raise _fail("factorization: original polynomial binding differs")
    if _parse(certificate.get("content")) != values[0]:
        raise _fail("factorization: content differs from original leading coefficient")


def _factor_rows(certificate: Mapping[str, object]) -> list[object]:
    rows = certificate.get("factors")
    if isinstance(rows, list):
        return rows
    raise _fail("factorization: factor array required", received=type(rows).__name__)


def _factor_record(row: object, index: int) -> dict[str, Any]:
    if isinstance(row, dict) and set(row) == _FACTOR_FIELDS:
        return cast(dict[str, Any], row)
    raise _fail("factorization: exact factor fields required", index=index)


def _monic_nonconstant(poly: list[Q], index: int) -> list[Q]:
    if len(poly) < 2 or poly[0] != 1:
        raise _fail("factorization: nonconstant monic factor required", index=index)
    return poly


def _bounded_multiplicity(count: object, limit: int, index: int) -> int:
    if isinstance(count, float):
        raise _fail("float refused at the public boundary", role="multiplicity", received="float")
    if type(count) is bool:
        raise _fail("boolean refused where an exact integer was required", role="multiplicity")
    if isinstance(count, int) and 1 <= count <= limit:
        return count
    raise _fail("factorization: bounded positive integer multiplicity required", index=index)


def _require_increasing(previous: list[Q] | None, poly: list[Q], index: int) -> None:
    if previous is not None and not previous < poly:
        raise _fail("factorization: factors must be distinct and numerically ordered", index=index)


def _require_degree(total: int, limit: int, index: int) -> None:
    if total > limit:
        raise _fail("factorization: factor degree census exceeds input degree", index=index, degree=total)


def _require_irreducible(ascending: list[Q], index: int) -> None:
    reducible = len(_gcd(ascending, _derivative(ascending))) > 1
    if reducible or len(_factor_squarefree(ascending)) != 1:
        raise _fail("factorization: supplied factor is reducible over Q", index=index)


def _repeat_product(product: list[Q], factor: list[Q], count: int) -> list[Q]:
    for _ in range(count):
        product = _qmul(product, factor)
    return product


def _accept_factor(
    row: object,
    index: int,
    degree: int,
    limit: int,
    previous: list[Q] | None,
    product: list[Q],
) -> tuple[list[Q], list[Q], int]:
    record = _factor_record(row, index)
    poly = _monic_nonconstant(_parse_polynomial(record["polynomial"]), index)
    count = _bounded_multiplicity(record["multiplicity"], limit, index)
    _require_increasing(previous, poly, index)
    total = degree + count * (len(poly) - 1)
    _require_degree(total, limit, index)
    ascending = list(reversed(poly))
    _require_irreducible(ascending, index)
    return poly, _repeat_product(product, ascending, count), total


def validate_factorization(coefficients: object, certificate: object) -> None:
    """Verify input, exact product, multiplicities and irreducibility over Q.

    Irreducibility is checked by exact modular reconstruction, not inferred
    from product equality, absence of rational roots, or supplied labels.
    """
    values = _domain(coefficients)
    checked = _require_certificate(certificate)
    _require_metadata(checked)
    _require_input_binding(checked, values)
    product: list[Q] = [values[0]]
    previous: list[Q] | None = None
    degree = 0
    limit = len(values) - 1
    for index, row in enumerate(_factor_rows(checked)):
        previous, product, degree = _accept_factor(row, index, degree, limit, previous, product)
    if product != list(reversed(values)):
        raise _fail("factorization: exact factor product does not reconstruct original polynomial")


def dispatch(request: object) -> dict[str, Any]:
    if isinstance(request, dict) and set(request) == _REQUEST_FIELDS and request["operation"] == "factor":
        return factor_polynomial(_parse_polynomial(request["coefficients"]))
    raise _fail("factorization: exact request fields and factor operation required")


def _reject_inexact(token: str) -> None:
    raise _fail("factorization: inexact JSON number forbidden", token=token)


def main() -> int:
    try:
        if len(sys.argv) != 1:
            raise _fail("factorization: stdin request only; no CLI arguments permitted")
        payload = json.loads(
            sys.stdin.buffer.read(),
            parse_float=_reject_inexact,
            parse_constant=_reject_inexact,
        )
        result = dispatch(payload)
    except (ValueError, TypeError, ZeroDivisionError) as error:
        print(str(error), file=sys.stderr)
        return 2
    sys.stdout.buffer.write((json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
