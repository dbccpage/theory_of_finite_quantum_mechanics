"""Exact polynomial factorization over the declared real coefficient fields.

Origin: code/rust/src/linear_algebra/field_factors.rs, which states
factorization over a declared real field only, with no splitting-degree or
multiplicative-dependence claim, and with coefficients ascending internally.
Claim: urn:omega:fqm:linear-algebra:real-factorization:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_field_factors.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 7; AST Sonar cognitive complexity max 11; AST nesting depth max 3; lizard 1.24.1 cyclomatic complexity max 7.
Scope Fence: Trager reduction calls rational factorization over Q. This file
does not claim a splitting degree, multiplicative dependence, or a complex
carrier, and it does not admit floats or Q(i).
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from typing import Any, Mapping

from . import field_squares as real
from . import rational_factors as rational
from .scalars import GaussianRational


Coordinates = tuple[Q, Q]
Polynomial = list[Coordinates]
ZERO = (Q(0), Q(0))
ONE = (Q(1), Q(0))
SCHEMA = "real_field_polynomial_factorization_v1"
ALGORITHM = "EXACT_TRAGER_RATIONAL_NORM_FACTORIZATION"
_RESULT_FIELDS = {
    "schema", "authority_effect", "conductor", "real_generator_radicand",
    "coefficient_field", "coefficients", "content", "factors", "algorithm",
}
_FACTOR_FIELDS = {"polynomial", "multiplicity"}
_REQUEST_FIELDS = {"operation", "conductor", "coefficients"}


class FieldFactorError(ValueError):
    """One violated factorization invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> FieldFactorError:
    return FieldFactorError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _require_conductor(value: object) -> int:
    _refuse_float(value, "conductor")
    if type(value) is bool:
        raise _fail("boolean refused where a conductor was required", role="conductor")
    if type(value) is int:
        return value
    raise _fail("real_factorization: exact integer conductor required", received=type(value).__name__)


def _refuse_coordinate(value: object, role: str) -> None:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a rational coordinate was required", role=role)
    if isinstance(value, GaussianRational):
        raise _fail(
            "Gaussian rational refused; factorization in this module is over a real field",
            role=role,
        )


def _scan_coefficient(value: object, role: str) -> None:
    _refuse_coordinate(value, role)
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _refuse_coordinate(item, f"{role}[{index}]")


def _scan_coefficients(coefficients: object) -> None:
    _refuse_coordinate(coefficients, "coefficients")
    if isinstance(coefficients, (list, tuple)):
        for index, item in enumerate(coefficients):
            _scan_coefficient(item, f"coefficient[{index}]")


def _add(a: Coordinates, b: Coordinates) -> Coordinates:
    return a[0] + b[0], a[1] + b[1]


def _neg(a: Coordinates) -> Coordinates:
    return -a[0], -a[1]


def _mul(a: Coordinates, b: Coordinates, d: int) -> Coordinates:
    return a[0] * b[0] + d * a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def _div(a: Coordinates, b: Coordinates, d: int) -> Coordinates:
    norm = b[0] * b[0] - d * b[1] * b[1]
    if not norm:
        raise _fail("real_factorization: coefficient division by zero")
    return _mul(a, (b[0] / norm, -b[1] / norm), d)


def _trim(poly: Polynomial) -> Polynomial:
    while poly and poly[-1] == ZERO:
        poly.pop()
    return poly


def _padd(a: Polynomial, b: Polynomial) -> Polynomial:
    out = [ZERO] * max(len(a), len(b))
    for i, coefficient in enumerate(a):
        out[i] = _add(out[i], coefficient)
    for i, coefficient in enumerate(b):
        out[i] = _add(out[i], coefficient)
    return _trim(out)


def _pmul(a: Polynomial, b: Polynomial, d: int) -> Polynomial:
    if not a or not b:
        return []
    out = [ZERO] * (len(a) + len(b) - 1)
    for i, left in enumerate(a):
        for j, right in enumerate(b):
            out[i + j] = _add(out[i + j], _mul(left, right, d))
    return _trim(out)


def _pdivmod(a: Polynomial, b: Polynomial, d: int) -> tuple[Polynomial, Polynomial]:
    if not b:
        raise _fail("real_factorization: polynomial division by zero")
    remainder = a[:]
    quotient = [ZERO] * max(0, len(a) - len(b) + 1)
    while remainder and len(remainder) >= len(b):
        degree = len(remainder) - len(b)
        coefficient = _div(remainder[-1], b[-1], d)
        quotient[degree] = coefficient
        for j, value in enumerate(b):
            remainder[degree + j] = _add(remainder[degree + j], _neg(_mul(coefficient, value, d)))
        _trim(remainder)
    return _trim(quotient), remainder


def _exact_div(a: Polynomial, b: Polynomial, d: int) -> Polynomial:
    quotient, remainder = _pdivmod(a, b, d)
    if remainder:
        raise _fail("real_factorization: nonzero exact-division remainder")
    return quotient


def _gcd(a: Polynomial, b: Polynomial, d: int) -> Polynomial:
    while b:
        a, b = b, _pdivmod(a, b, d)[1]
    return [_div(value, a[-1], d) for value in a] if a else []


def _derivative(a: Polynomial) -> Polynomial:
    return _trim([(i * a[i][0], i * a[i][1]) for i in range(1, len(a))])


def _shift(a: Polynomial, offset: Coordinates, d: int) -> Polynomial:
    """Return a(X+offset) by exact Horner composition."""
    result: Polynomial = []
    for coefficient in reversed(a):
        result = _padd(_pmul(result, [offset, ONE], d), [coefficient])
    return result


def _conjugate(poly: Polynomial) -> Polynomial:
    return [(a, -b) for a, b in poly]


def _squarefree_norm(f: Polynomial, d: int) -> tuple[int, Polynomial, list[Q]]:
    """Find a separating shift using the proven n^2+1 finite parameter family.

    Requires nonconstant monic squarefree f and d in {2,5}. The conjugation
    here is the nontrivial E/Q automorphism, not complex conjugation.
    """
    n = len(f) - 1
    for shift in range(n * n + 1):
        g = _shift(f, (Q(0), Q(-shift)), d)
        norm = _pmul(g, _conjugate(g), d)
        if any(b for _, b in norm) or len(norm) != 2 * n + 1:
            raise _fail("real_factorization: norm failed rationality or degree binding")
        coefficients = [a for a, _ in norm]
        if len(rational._gcd(coefficients, rational._derivative(coefficients))) == 1:
            return shift, g, coefficients
    raise _fail("real_factorization: separating shift theorem invariant failed")


def _embed_rational(part: list[Q]) -> Polynomial:
    return [(coefficient, Q(0)) for coefficient in part]


def _rational_squarefree(f: Polynomial) -> list[Polynomial]:
    parts = rational._factor_squarefree([a for a, _ in f])
    return [_embed_rational(part) for part in parts]


def _norm_divisor(g: Polynomial, part: list[Q], shift: int, d: int) -> Polynomial:
    lifted = _embed_rational(part)
    divisor = _gcd(g, lifted, d)
    if len(divisor) < 2 or len(part) - 1 != 2 * (len(divisor) - 1):
        raise _fail("real_factorization: norm factor and field divisor degrees differ")
    if _pmul(divisor, _conjugate(divisor), d) != lifted:
        raise _fail("real_factorization: field divisor norm does not recover rational factor")
    return _shift(divisor, (Q(0), Q(shift)), d)


def _reconstruct_squarefree(factors: list[Polynomial], f: Polynomial, d: int) -> None:
    product = [ONE]
    for part in factors:
        product = _pmul(product, part, d)
    if product != f:
        raise _fail("real_factorization: Trager factors do not reconstruct squarefree input")


def _factor_squarefree(f: Polynomial, d: int) -> list[Polynomial]:
    if not d:
        return _rational_squarefree(f)
    shift, g, norm = _squarefree_norm(f, d)
    factors = [_norm_divisor(g, part, shift, d) for part in rational._factor_squarefree(norm)]
    _reconstruct_squarefree(factors, f, d)
    return factors


def _domain(conductor: object, coefficients: object) -> tuple[int, Polynomial]:
    number = _require_conductor(conductor)
    _scan_coefficients(coefficients)
    d, _ = real._domain(number, ZERO)
    if not isinstance(coefficients, (list, tuple)) or not coefficients:
        raise _fail("real_factorization: nonempty coefficient sequence required")
    values = [real._domain(number, value)[1] for value in coefficients]
    if values[0] == ZERO:
        raise _fail("real_factorization: nonzero leading coefficient required")
    return d, values


def _parse_polynomial(conductor: int, values: object) -> Polynomial:
    if not isinstance(values, list):
        raise _fail("real_factorization: coefficient array required")
    return _domain(conductor, [real._parse_coordinates(conductor, value) for value in values])[1]


def _wire(poly: Polynomial) -> list[list[str]]:
    return [real._wire(value) for value in poly]


def _field(d: int) -> str:
    return f"Q(sqrt({d}))" if d else "Q"


def _monic_ascending(values: Polynomial, d: int) -> Polynomial:
    return [_div(value, values[0], d) for value in reversed(values)]


def _yun_factors(f: Polynomial, d: int) -> list[tuple[Polynomial, int]]:
    common = _gcd(f, _derivative(f), d)
    remaining = _exact_div(f, common, d)
    multiplicity = 1
    factors: list[tuple[Polynomial, int]] = []
    while len(remaining) > 1:
        overlap = _gcd(remaining, common, d)
        part = _exact_div(remaining, overlap, d)
        if len(part) > 1:
            factors.extend((list(reversed(poly)), multiplicity) for poly in _factor_squarefree(part, d))
        remaining, common = overlap, _exact_div(common, overlap, d)
        multiplicity += 1
    factors.sort(key=lambda item: item[0])
    return factors


def factor_polynomial(conductor: object, coefficients: object) -> dict[str, Any]:
    """Factor a nonzero polynomial over E, retaining leading content and powers."""
    number = _require_conductor(conductor)
    d, values = _domain(number, coefficients)
    factors = _yun_factors(_monic_ascending(values, d), d)
    return {
        "schema": SCHEMA,
        "authority_effect": "None",
        "conductor": number,
        "real_generator_radicand": d,
        "coefficient_field": _field(d),
        "coefficients": _wire(values),
        "content": real._wire(values[0]),
        "factors": [{"polynomial": _wire(poly), "multiplicity": count} for poly, count in factors],
        "algorithm": ALGORITHM,
    }


def _result_record(certificate: object) -> dict[str, Any]:
    if isinstance(certificate, dict) and set(certificate) == _RESULT_FIELDS:
        return certificate
    raise _fail("real_factorization: exact output field census required")


def _require_text(result: dict[str, Any], key: str, expected: str) -> None:
    if result[key] != expected:
        raise _fail("real_factorization: schema or arithmetic-domain binding differs")


def _require_domain_binding(result: dict[str, Any], conductor: int, radicand: int) -> None:
    _require_text(result, "schema", SCHEMA)
    _require_text(result, "authority_effect", "None")
    _require_text(result, "coefficient_field", _field(radicand))
    _require_text(result, "algorithm", ALGORITHM)
    if type(result["conductor"]) is not int or result["conductor"] != conductor:
        raise _fail("real_factorization: schema or arithmetic-domain binding differs")
    if type(result["real_generator_radicand"]) is not int or result["real_generator_radicand"] != radicand:
        raise _fail("real_factorization: schema or arithmetic-domain binding differs")


def _require_input_binding(result: dict[str, Any], conductor: int, values: Polynomial) -> None:
    if _parse_polynomial(conductor, result["coefficients"]) != values:
        raise _fail("real_factorization: original polynomial binding differs")
    if real._parse_coordinates(conductor, result["content"]) != values[0]:
        raise _fail("real_factorization: content differs from original leading coefficient")


def _factor_row(row: object, label: str) -> dict[str, Any]:
    if isinstance(row, dict) and set(row) == _FACTOR_FIELDS:
        return row
    raise _fail(f"{label}: exact factor fields required")


def _monic_factor(conductor: int, row: dict[str, Any], label: str) -> Polynomial:
    poly = _parse_polynomial(conductor, row["polynomial"])
    if len(poly) < 2 or poly[0] != ONE:
        raise _fail(f"{label}: nonconstant monic factor required")
    return poly


def _multiplicity(count: object, limit: int, label: str) -> int:
    if type(count) is not int or not 1 <= count <= limit:
        raise _fail(f"{label}: bounded positive integer multiplicity required")
    return count


def _require_order(previous: Polynomial | None, poly: Polynomial, label: str) -> None:
    if previous is not None and not previous < poly:
        raise _fail(f"{label}: factors must be distinct and numerically ordered")


def _next_degree(degree: int, count: int, poly: Polynomial, limit: int, label: str) -> int:
    updated = degree + count * (len(poly) - 1)
    if updated > limit:
        raise _fail(f"{label}: factor degree census exceeds input degree")
    return updated


def _require_irreducible_factor(poly: Polynomial, radicand: int, label: str) -> Polynomial:
    ascending = list(reversed(poly))
    reducible = len(_gcd(ascending, _derivative(ascending), radicand)) > 1
    split = len(_factor_squarefree(ascending, radicand)) != 1
    if reducible or split:
        raise _fail(f"{label}: supplied factor is reducible over the declared real field")
    return ascending


def _accumulate(product: Polynomial, ascending: Polynomial, count: int, radicand: int) -> Polynomial:
    for _ in range(count):
        product = _pmul(product, ascending, radicand)
    return product


def _consume_factor(
    conductor: int,
    radicand: int,
    values: Polynomial,
    index: int,
    raw: object,
    previous: Polynomial | None,
    degree: int,
    product: Polynomial,
) -> tuple[Polynomial, int, Polynomial]:
    label = f"real_factorization[{index}]"
    row = _factor_row(raw, label)
    poly = _monic_factor(conductor, row, label)
    count = _multiplicity(row["multiplicity"], len(values) - 1, label)
    _require_order(previous, poly, label)
    degree = _next_degree(degree, count, poly, len(values) - 1, label)
    ascending = _require_irreducible_factor(poly, radicand, label)
    return poly, degree, _accumulate(product, ascending, count, radicand)


def _require_product(conductor: int, radicand: int, values: Polynomial, rows: object) -> None:
    if not isinstance(rows, list):
        raise _fail("real_factorization: factor array required")
    product: Polynomial = [values[0]]
    previous: Polynomial | None = None
    degree = 0
    for index, row in enumerate(rows):
        previous, degree, product = _consume_factor(
            conductor, radicand, values, index, row, previous, degree, product
        )
    if product != list(reversed(values)):
        raise _fail("real_factorization: exact factor product does not reconstruct original polynomial")


def validate_factorization(conductor: object, coefficients: object, certificate: object) -> None:
    """Check field binding, exact product, and arithmetic irreducibility.

    Reuses this implementation's Trager/rational irreducibility core, but does
    not compare against producer JSON or infer irreducibility from root absence.
    """
    number = _require_conductor(conductor)
    radicand, values = _domain(number, coefficients)
    result = _result_record(certificate)
    _require_domain_binding(result, number, radicand)
    _require_input_binding(result, number, values)
    _require_product(number, radicand, values, result["factors"])


def dispatch(request: object) -> dict[str, Any]:
    if (
        not isinstance(request, dict)
        or set(request) != _REQUEST_FIELDS
        or request["operation"] != "factor"
    ):
        raise _fail("real_factorization: exact request fields and factor operation required")
    number = _require_conductor(request["conductor"])
    return factor_polynomial(number, _parse_polynomial(number, request["coefficients"]))


def _reject_inexact(token: str) -> None:
    raise _fail("real_factorization: inexact JSON number forbidden", token=token)


def main() -> int:
    try:
        if len(sys.argv) != 1:
            raise _fail("real_factorization: stdin request only; no CLI arguments permitted")
        payload = json.loads(
            sys.stdin.buffer.read(),
            parse_int=real._integer_from_text,
            parse_float=_reject_inexact,
            parse_constant=_reject_inexact,
        )
        result = dispatch(payload)
    except (ValueError, TypeError, ZeroDivisionError) as error:
        print(str(error), file=sys.stderr)
        return 2
    payload_text = json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n"
    sys.stdout.buffer.write(payload_text.encode("ascii"))
    return 0


def witness_split_linear_count() -> int:
    """Number of monic linear factors of x^2 - 4 over Q, which is 2."""
    certificate = factor_polynomial(1, [(Q(1), Q(0)), (Q(0), Q(0)), (Q(-4), Q(0))])
    rows = certificate["factors"]
    if type(rows) is not list:
        raise _fail("real_factorization: factor array required")
    return len(rows)


if __name__ == "__main__":
    raise SystemExit(main())
