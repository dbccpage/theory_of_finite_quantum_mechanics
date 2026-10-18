"""Exact irreducible cubic/quartic splitting degrees over the real field E.

AuthorityEffect: None. This does not compute degrees over the complex carrier,
quintic or compositum degrees, eigenvalue assignments, or logarithm dependence.
All polynomial lists in this module use descending exact coordinate pairs.
"""

from __future__ import annotations

from fractions import Fraction as Q
import json
import sys
from typing import Any, Iterable

from . import field_factors as factors
from . import field_squares as real


Coordinates = tuple[Q, Q]
Polynomial = list[Coordinates]
ZERO = (Q(0), Q(0))
ONE = (Q(1), Q(0))
SCHEMA = "real_field_splitting_degree_v1"
ALGORITHM = "EXACT_CUBIC_QUARTIC_RESOLVENT_CLASSIFICATION"
RESULT_FIELDS = {
    "schema", "authority_effect", "algorithm", "conductor", "real_generator_radicand",
    "coefficient_field", "degree_over_real_field", "galois_group", "coefficients",
    "monic_polynomial", "factorization", "discriminant", "discriminant_square", "resolvent",
}


def _sum(values: Iterable[Coordinates]) -> Coordinates:
    """Fold coordinate sums stepwise in reduced, arbitrary-precision rationals."""
    total = ZERO
    for value in values:
        total = factors._add(total, value)
    return total


def _scale(value: Coordinates, integer: int) -> Coordinates:
    return integer * value[0], integer * value[1]


def _square(value: Coordinates, radicand: int) -> Coordinates:
    return factors._mul(value, value, radicand)


def _cubic_discriminant(a: Coordinates, b: Coordinates, c: Coordinates,
                        radicand: int) -> Coordinates:
    a2, b2 = _square(a, radicand), _square(b, radicand)
    return _sum((
        factors._mul(a2, b2, radicand),
        _scale(factors._mul(b2, b, radicand), -4),
        _scale(factors._mul(factors._mul(a2, a, radicand), c, radicand), -4),
        _scale(_square(c, radicand), -27),
        _scale(factors._mul(factors._mul(a, b, radicand), c, radicand), 18),
    ))


def _quartic_resolvent(monic: Polynomial, radicand: int) -> Polynomial:
    _, a, b, c, constant = monic
    return [
        ONE,
        factors._neg(b),
        _sum((factors._mul(a, c, radicand), _scale(constant, -4))),
        _sum((
            factors._neg(factors._mul(_square(a, radicand), constant, radicand)),
            factors._neg(_square(c, radicand)),
            _scale(factors._mul(b, constant, radicand), 4),
        )),
    ]


def _cyclic_values(monic: Polynomial, root: Coordinates, discriminant: Coordinates,
                   radicand: int) -> tuple[Coordinates, Coordinates]:
    _, a, b, _, constant = monic
    first = _sum((_square(a, radicand), _scale(_sum((b, factors._neg(root))), -4)))
    second = _sum((_square(root, radicand), _scale(constant, -4)))
    return (factors._mul(discriminant, first, radicand),
            factors._mul(discriminant, second, radicand))


def _fields(value: Any, expected: set[str], label: str) -> None:
    if type(value) is not dict or set(value) != expected:
        raise ValueError(f"splitting_degree: exact {label} field census required")


def _input(conductor: int, coefficients: Any) -> tuple[int, Polynomial, Polynomial]:
    radicand, values = factors._domain(conductor, coefficients)
    if len(values) not in (4, 5):
        raise ValueError("splitting_degree: polynomial degree must be three or four")
    monic = [factors._div(value, values[0], radicand) for value in values]
    return radicand, values, monic


def _require_irreducible(conductor: int, monic: Polynomial, certificate: dict) -> None:
    # Called only after producing or arithmetically validating this certificate.
    rows = certificate["factors"]
    if (len(rows) != 1 or type(rows[0]["multiplicity"]) is not int
            or rows[0]["multiplicity"] != 1
            or factors._parse_polynomial(conductor, rows[0]["polynomial"]) != monic):
        raise ValueError("splitting_degree: input must be irreducible over the declared real field")


def _resolvent_pattern(certificate: dict) -> list[int]:
    if any(type(row["multiplicity"]) is not int or row["multiplicity"] != 1
           for row in certificate["factors"]):
        raise ValueError("splitting_degree: resolvent factors must have unit multiplicity")
    return sorted(len(row["polynomial"]) - 1 for row in certificate["factors"])


def _resolvent_root(conductor: int, certificate: dict) -> Coordinates:
    linear = [row for row in certificate["factors"] if len(row["polynomial"]) == 2]
    if len(linear) != 1:
        raise ValueError("splitting_degree: unique real-field resolvent root required")
    polynomial = factors._parse_polynomial(conductor, linear[0]["polynomial"])
    return factors._neg(polynomial[1])


def _classification(degree: int, square: bool, pattern: list[int] | None,
                    first_square: bool | None = None,
                    second_square: bool | None = None) -> tuple[str, int]:
    if degree == 3:
        return ("C3", 3) if square else ("S3", 6)
    if pattern == [3]:
        return ("A4", 12) if square else ("S4", 24)
    if pattern == [1, 1, 1] and square:
        return "V4", 4
    if pattern == [1, 2] and not square:
        if type(first_square) is not bool or type(second_square) is not bool:
            raise ValueError("splitting_degree: both cyclic square tests required")
        return ("C4", 4) if first_square and second_square else ("D4", 8)
    raise ValueError("splitting_degree: inconsistent resolvent pattern and discriminant")


def irreducible_splitting_degree(conductor: int, coefficients: Any) -> dict[str, Any]:
    """Compute [Spl_E(f):E], never silently the degree over the complex carrier."""
    radicand, values, monic = _input(conductor, coefficients)
    factorization = factors.factor_polynomial(conductor, values)
    _require_irreducible(conductor, monic, factorization)
    degree = len(monic) - 1
    resolvent_polynomial = _quartic_resolvent(monic, radicand) if degree == 4 else None
    cubic = resolvent_polynomial if resolvent_polynomial is not None else monic
    discriminant = _cubic_discriminant(*cubic[1:], radicand)
    if discriminant == ZERO:
        raise ValueError("splitting_degree: irreducible characteristic-zero input has zero discriminant")
    square = real.square_certificate(conductor, discriminant)
    resolvent, pattern, first_square, second_square = None, None, None, None
    if resolvent_polynomial is not None:
        decomposition = factors.factor_polynomial(conductor, resolvent_polynomial)
        pattern = _resolvent_pattern(decomposition)
        resolvent = {"coefficients": factors._wire(resolvent_polynomial),
                     "factorization": decomposition, "factor_degrees": pattern,
                     "root": None, "cyclic_tests": None}
        if pattern == [1, 2]:
            root = _resolvent_root(conductor, decomposition)
            first, second = _cyclic_values(monic, root, discriminant, radicand)
            first_certificate = real.square_certificate(conductor, first)
            second_certificate = real.square_certificate(conductor, second)
            first_square, second_square = first_certificate["is_square"], second_certificate["is_square"]
            resolvent["root"] = real._wire(root)
            resolvent["cyclic_tests"] = {
                "first_value": real._wire(first), "first_square": first_certificate,
                "second_value": real._wire(second), "second_square": second_certificate,
            }
    group, extension_degree = _classification(degree, square["is_square"], pattern,
                                               first_square, second_square)
    return {"schema": SCHEMA, "authority_effect": "None", "algorithm": ALGORITHM,
            "conductor": conductor, "real_generator_radicand": radicand,
            "coefficient_field": factors._field(radicand),
            "degree_over_real_field": extension_degree, "galois_group": group,
            "coefficients": factors._wire(values), "monic_polynomial": factors._wire(monic),
            "factorization": factorization, "discriminant": real._wire(discriminant),
            "discriminant_square": square, "resolvent": resolvent}


def validate_splitting_degree(conductor: int, coefficients: Any, result: Any) -> None:
    """Recompute branch invariants and validate supplied nested arithmetic proofs."""
    radicand, values, monic = _input(conductor, coefficients)
    _fields(result, RESULT_FIELDS, "result")
    for key in ("schema", "authority_effect", "algorithm", "coefficient_field", "galois_group"):
        if type(result[key]) is not str:
            raise ValueError(f"splitting_degree: string metadata required: {key}")
    for key in ("conductor", "real_generator_radicand", "degree_over_real_field"):
        if type(result[key]) is not int:
            raise ValueError(f"splitting_degree: exact integer metadata required: {key}")
    expected = {"schema": SCHEMA, "authority_effect": "None", "algorithm": ALGORITHM,
                "conductor": conductor, "real_generator_radicand": radicand,
                "coefficient_field": factors._field(radicand)}
    if any(result[key] != value for key, value in expected.items()):
        raise ValueError("splitting_degree: metadata or coefficient-field binding differs")
    if factors._parse_polynomial(conductor, result["coefficients"]) != values:
        raise ValueError("splitting_degree: original polynomial binding differs")
    if factors._parse_polynomial(conductor, result["monic_polynomial"]) != monic:
        raise ValueError("splitting_degree: normalized monic polynomial binding differs")
    factors.validate_factorization(conductor, values, result["factorization"])
    _require_irreducible(conductor, monic, result["factorization"])
    degree = len(monic) - 1
    resolvent_polynomial = _quartic_resolvent(monic, radicand) if degree == 4 else None
    cubic = resolvent_polynomial if resolvent_polynomial is not None else monic
    discriminant = _cubic_discriminant(*cubic[1:], radicand)
    if discriminant == ZERO or real._parse_coordinates(conductor, result["discriminant"]) != discriminant:
        raise ValueError("splitting_degree: nonzero discriminant binding differs")
    real.validate_square_certificate(conductor, discriminant, result["discriminant_square"])
    pattern, first_square, second_square = None, None, None
    resolvent = result["resolvent"]
    if resolvent_polynomial is None:
        if resolvent is not None:
            raise ValueError("splitting_degree: cubic resolvent field must be null")
    else:
        _fields(resolvent, {"coefficients", "factorization", "factor_degrees", "root", "cyclic_tests"},
                "resolvent")
        supplied_pattern = resolvent["factor_degrees"]
        if (type(supplied_pattern) is not list
                or any(type(value) is not int for value in supplied_pattern)):
            raise ValueError("splitting_degree: exact integer resolvent factor degrees required")
        if factors._parse_polynomial(conductor, resolvent["coefficients"]) != resolvent_polynomial:
            raise ValueError("splitting_degree: resolvent coefficient binding differs")
        factors.validate_factorization(conductor, resolvent_polynomial, resolvent["factorization"])
        pattern = _resolvent_pattern(resolvent["factorization"])
        if supplied_pattern != pattern:
            raise ValueError("splitting_degree: resolvent factor-degree census differs")
        if pattern == [1, 2]:
            root = _resolvent_root(conductor, resolvent["factorization"])
            if real._parse_coordinates(conductor, resolvent["root"]) != root:
                raise ValueError("splitting_degree: unique resolvent root binding differs")
            first, second = _cyclic_values(monic, root, discriminant, radicand)
            tests = resolvent["cyclic_tests"]
            _fields(tests, {"first_value", "first_square", "second_value", "second_square"}, "cyclic tests")
            for label, value in (("first", first), ("second", second)):
                if real._parse_coordinates(conductor, tests[f"{label}_value"]) != value:
                    raise ValueError(f"splitting_degree: {label} cyclic value binding differs")
                real.validate_square_certificate(conductor, value, tests[f"{label}_square"])
            first_square = tests["first_square"]["is_square"]
            second_square = tests["second_square"]["is_square"]
        elif resolvent["root"] is not None or resolvent["cyclic_tests"] is not None:
            raise ValueError("splitting_degree: inapplicable resolvent root and cyclic tests must be null")
    group, extension_degree = _classification(degree, result["discriminant_square"]["is_square"], pattern,
                                               first_square, second_square)
    if result["galois_group"] != group or result["degree_over_real_field"] != extension_degree:
        raise ValueError("splitting_degree: Galois group or real-field degree differs from arithmetic branch")


def dispatch(request: Any) -> dict[str, Any]:
    _fields(request, {"operation", "conductor", "coefficients"}, "request")
    if type(request["operation"]) is not str or request["operation"] != "irreducible_splitting_degree":
        raise ValueError("splitting_degree: irreducible_splitting_degree operation required")
    conductor = request["conductor"]
    coefficients = factors._parse_polynomial(conductor, request["coefficients"])
    return irreducible_splitting_degree(conductor, coefficients)


def _reject_inexact(token: str) -> None:
    raise ValueError(f"splitting_degree: inexact JSON number forbidden: {token}")


def main() -> int:
    try:
        if len(sys.argv) != 1:
            raise ValueError("splitting_degree: stdin request only; no CLI arguments permitted")
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
