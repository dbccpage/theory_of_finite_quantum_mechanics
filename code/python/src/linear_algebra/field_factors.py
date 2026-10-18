"""Exact polynomial factorization over the declared real coefficient fields.

AuthorityEffect: None. Trager reduction uses rational factorization, not a
numerical root search. This is not a splitting-degree or dependence certificate.
Internal polynomial coefficients are ascending pairs of rational coordinates.
"""

from __future__ import annotations

from fractions import Fraction as Q
import json
import sys
from typing import Any

from . import rational_factors as rational
from . import field_squares as real


Coordinates = tuple[Q, Q]
Polynomial = list[Coordinates]
ZERO = (Q(0), Q(0))
ONE = (Q(1), Q(0))
SCHEMA = "real_field_polynomial_factorization_v1"
ALGORITHM = "EXACT_TRAGER_RATIONAL_NORM_FACTORIZATION"


def _add(a: Coordinates, b: Coordinates) -> Coordinates:
    return a[0] + b[0], a[1] + b[1]


def _neg(a: Coordinates) -> Coordinates:
    return -a[0], -a[1]


def _mul(a: Coordinates, b: Coordinates, d: int) -> Coordinates:
    return a[0] * b[0] + d * a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def _div(a: Coordinates, b: Coordinates, d: int) -> Coordinates:
    norm = b[0] * b[0] - d * b[1] * b[1]
    if not norm:
        raise ValueError("real_factorization: coefficient division by zero")
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
        raise ValueError("real_factorization: polynomial division by zero")
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
        raise ValueError("real_factorization: nonzero exact-division remainder")
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


def _squarefree_norm(f: Polynomial, d: int) -> tuple[int, Polynomial, list[Q]]:
    """Find a separating shift using the proven n^2+1 finite parameter family.

    Requires nonconstant monic squarefree f and d in {2,5}. The conjugation
    here is the nontrivial E/Q automorphism, not complex conjugation.
    """
    n = len(f) - 1
    for shift in range(n * n + 1):
        g = _shift(f, (Q(0), Q(-shift)), d)
        norm = _pmul(g, [(a, -b) for a, b in g], d)
        if any(b for _, b in norm) or len(norm) != 2 * n + 1:
            raise ValueError("real_factorization: norm failed rationality or degree binding")
        coefficients = [a for a, _ in norm]
        if len(rational._gcd(coefficients, rational._derivative(coefficients))) == 1:
            return shift, g, coefficients
    raise ValueError("real_factorization: separating shift theorem invariant failed")


def _factor_squarefree(f: Polynomial, d: int) -> list[Polynomial]:
    if not d:
        return [[(a, Q(0)) for a in part] for part in rational._factor_squarefree([a for a, _ in f])]
    shift, g, norm = _squarefree_norm(f, d)
    factors = []
    for part in rational._factor_squarefree(norm):
        lifted = [(a, Q(0)) for a in part]
        divisor = _gcd(g, lifted, d)
        if len(divisor) < 2 or len(part) - 1 != 2 * (len(divisor) - 1):
            raise ValueError("real_factorization: norm factor and field divisor degrees differ")
        if _pmul(divisor, [(a, -b) for a, b in divisor], d) != lifted:
            raise ValueError("real_factorization: field divisor norm does not recover rational factor")
        factors.append(_shift(divisor, (Q(0), Q(shift)), d))
    product = [ONE]
    for part in factors:
        product = _pmul(product, part, d)
    if product != f:
        raise ValueError("real_factorization: Trager factors do not reconstruct squarefree input")
    return factors


def _domain(conductor: Any, coefficients: Any) -> tuple[int, Polynomial]:
    d, _ = real._domain(conductor, ZERO)
    if not isinstance(coefficients, (list, tuple)) or not coefficients:
        raise ValueError("real_factorization: nonempty coefficient sequence required")
    values = [real._domain(conductor, value)[1] for value in coefficients]
    if values[0] == ZERO:
        raise ValueError("real_factorization: nonzero leading coefficient required")
    return d, values


def _parse_polynomial(conductor: int, values: Any) -> Polynomial:
    if not isinstance(values, list):
        raise ValueError("real_factorization: coefficient array required")
    return _domain(conductor, [real._parse_coordinates(conductor, value) for value in values])[1]


def _wire(poly: Polynomial) -> list[list[str]]:
    return [real._wire(value) for value in poly]


def _field(d: int) -> str:
    return f"Q(sqrt({d}))" if d else "Q"


def factor_polynomial(conductor: int, coefficients: Any) -> dict[str, Any]:
    """Factor a nonzero polynomial over E, retaining leading content and powers."""
    d, values = _domain(conductor, coefficients)
    f = [_div(value, values[0], d) for value in reversed(values)]
    common = _gcd(f, _derivative(f), d)
    remaining, multiplicity, factors = _exact_div(f, common, d), 1, []
    while len(remaining) > 1:
        overlap = _gcd(remaining, common, d)
        part = _exact_div(remaining, overlap, d)
        if len(part) > 1:
            factors.extend((list(reversed(poly)), multiplicity) for poly in _factor_squarefree(part, d))
        remaining, common = overlap, _exact_div(common, overlap, d)
        multiplicity += 1
    factors.sort(key=lambda item: item[0])
    return {"schema": SCHEMA, "authority_effect": "None", "conductor": conductor,
            "real_generator_radicand": d, "coefficient_field": _field(d),
            "coefficients": _wire(values), "content": real._wire(values[0]),
            "factors": [{"polynomial": _wire(poly), "multiplicity": count} for poly, count in factors],
            "algorithm": ALGORITHM}


def validate_factorization(conductor: int, coefficients: Any, certificate: Any) -> None:
    """Check field/input binding, exact product and arithmetic irreducibility.

    Reuses this implementation's Trager/rational irreducibility core, but does
    not compare against producer JSON or infer irreducibility from root absence.
    Independent-language and bounded-oracle evidence is recorded separately.
    """
    d, values = _domain(conductor, coefficients)
    keys = {"schema", "authority_effect", "conductor", "real_generator_radicand",
            "coefficient_field", "coefficients", "content", "factors", "algorithm"}
    if not isinstance(certificate, dict) or set(certificate) != keys:
        raise ValueError("real_factorization: exact output field census required")
    expected = {"schema": SCHEMA, "authority_effect": "None", "coefficient_field": _field(d),
                "algorithm": ALGORITHM}
    if (any(certificate[key] != value for key, value in expected.items())
            or type(certificate["conductor"]) is not int or certificate["conductor"] != conductor
            or type(certificate["real_generator_radicand"]) is not int
            or certificate["real_generator_radicand"] != d):
        raise ValueError("real_factorization: schema or arithmetic-domain binding differs")
    if _parse_polynomial(conductor, certificate["coefficients"]) != values:
        raise ValueError("real_factorization: original polynomial binding differs")
    if real._parse_coordinates(conductor, certificate["content"]) != values[0]:
        raise ValueError("real_factorization: content differs from original leading coefficient")
    if not isinstance(certificate["factors"], list):
        raise ValueError("real_factorization: factor array required")
    product, previous, degree = [values[0]], None, 0
    for index, row in enumerate(certificate["factors"]):
        label = f"real_factorization[{index}]"
        if not isinstance(row, dict) or set(row) != {"polynomial", "multiplicity"}:
            raise ValueError(f"{label}: exact factor fields required")
        poly = _parse_polynomial(conductor, row["polynomial"])
        count = row["multiplicity"]
        if len(poly) < 2 or poly[0] != ONE:
            raise ValueError(f"{label}: nonconstant monic factor required")
        if type(count) is not int or not 1 <= count <= len(values) - 1:
            raise ValueError(f"{label}: bounded positive integer multiplicity required")
        if previous is not None and not previous < poly:
            raise ValueError(f"{label}: factors must be distinct and numerically ordered")
        degree += count * (len(poly) - 1)
        if degree > len(values) - 1:
            raise ValueError(f"{label}: factor degree census exceeds input degree")
        ascending = list(reversed(poly))
        if len(_gcd(ascending, _derivative(ascending), d)) > 1 or len(_factor_squarefree(ascending, d)) != 1:
            raise ValueError(f"{label}: supplied factor is reducible over the declared real field")
        for _ in range(count):
            product = _pmul(product, ascending, d)
        previous = poly
    if product != list(reversed(values)):
        raise ValueError("real_factorization: exact factor product does not reconstruct original polynomial")


def dispatch(request: Any) -> dict[str, Any]:
    if (not isinstance(request, dict) or set(request) != {"operation", "conductor", "coefficients"}
            or request["operation"] != "factor"):
        raise ValueError("real_factorization: exact request fields and factor operation required")
    conductor = request["conductor"]
    return factor_polynomial(conductor, _parse_polynomial(conductor, request["coefficients"]))


def _reject_inexact(token: str) -> None:
    raise ValueError(f"real_factorization: inexact JSON number forbidden: {token}")


def main() -> int:
    try:
        if len(sys.argv) != 1:
            raise ValueError("real_factorization: stdin request only; no CLI arguments permitted")
        payload = json.loads(sys.stdin.buffer.read(), parse_int=real._integer_from_text,
                             parse_float=_reject_inexact, parse_constant=_reject_inexact)
        result = dispatch(payload)
    except (ValueError, TypeError, ZeroDivisionError) as error:
        print(str(error), file=sys.stderr)
        return 2
    sys.stdout.buffer.write((json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
