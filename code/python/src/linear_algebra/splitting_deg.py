"""Exact irreducible cubic and quartic splitting degrees over the real field E.

Origin: code/rust/src/linear_algebra/splitting_deg.rs, which states the exact
cubic/quartic splitting degree over E, not over a complex carrier K, and names
the groups C3, S3, A4, S4, V4, C4, and D4.
Claim: urn:omega:fqm:linear-algebra:splitting-degree:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_splitting_deg.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 5; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: the degree is the resolvent classification of one irreducible
cubic or quartic. This file does not claim a quintic, a compositum, a
root assignment, multiplicative dependence, or a degree over the complex
carrier, and it does not admit floats or Q(i).
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from typing import Any, Iterable, Mapping

from . import field_factors as factors
from . import field_squares as real
from .scalars import GaussianRational


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
_REQUEST_FIELDS = {"operation", "conductor", "coefficients"}
_RESOLVENT_FIELDS = {"coefficients", "factorization", "factor_degrees", "root", "cyclic_tests"}
_CYCLIC_FIELDS = {"first_value", "first_square", "second_value", "second_square"}


class SplittingDegreeError(ValueError):
    """One violated splitting-degree invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> SplittingDegreeError:
    return SplittingDegreeError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _require_conductor(value: object) -> int:
    _refuse_float(value, "conductor")
    if type(value) is bool:
        raise _fail("boolean refused where a conductor was required", role="conductor")
    if type(value) is int:
        return value
    raise _fail("splitting_degree: exact integer conductor required", received=type(value).__name__)


def _refuse_coordinate(value: object, role: str) -> None:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a rational coordinate was required", role=role)
    if isinstance(value, GaussianRational):
        raise _fail(
            "Gaussian rational refused; splitting degrees in this module are over a real field",
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


def _cubic_discriminant(
    linear: Coordinates,
    quadratic: Coordinates,
    constant: Coordinates,
    radicand: int,
) -> Coordinates:
    linear_square = _square(linear, radicand)
    quadratic_square = _square(quadratic, radicand)
    return _sum((
        factors._mul(linear_square, quadratic_square, radicand),
        _scale(factors._mul(quadratic_square, quadratic, radicand), -4),
        _scale(factors._mul(factors._mul(linear_square, linear, radicand), constant, radicand), -4),
        _scale(_square(constant, radicand), -27),
        _scale(factors._mul(factors._mul(linear, quadratic, radicand), constant, radicand), 18),
    ))


def _cubic_from(monic: Polynomial, radicand: int) -> Coordinates:
    return _cubic_discriminant(monic[1], monic[2], monic[3], radicand)


def _quartic_resolvent(monic: Polynomial, radicand: int) -> Polynomial:
    linear, quadratic, cubic, constant = monic[1], monic[2], monic[3], monic[4]
    return [
        ONE,
        factors._neg(quadratic),
        _sum((factors._mul(linear, cubic, radicand), _scale(constant, -4))),
        _sum((
            factors._neg(factors._mul(_square(linear, radicand), constant, radicand)),
            factors._neg(_square(cubic, radicand)),
            _scale(factors._mul(quadratic, constant, radicand), 4),
        )),
    ]


def _prepared(monic: Polynomial, radicand: int) -> tuple[Polynomial | None, Coordinates]:
    if len(monic) == 5:
        resolvent = _quartic_resolvent(monic, radicand)
        return resolvent, _cubic_from(resolvent, radicand)
    return None, _cubic_from(monic, radicand)


def _cyclic_values(
    monic: Polynomial,
    root: Coordinates,
    discriminant: Coordinates,
    radicand: int,
) -> tuple[Coordinates, Coordinates]:
    linear, quadratic, constant = monic[1], monic[2], monic[4]
    first = _sum((_square(linear, radicand), _scale(_sum((quadratic, factors._neg(root))), -4)))
    second = _sum((_square(root, radicand), _scale(constant, -4)))
    return (
        factors._mul(discriminant, first, radicand),
        factors._mul(discriminant, second, radicand),
    )


def _fields(value: object, expected: set[str], label: str) -> dict[str, Any]:
    if type(value) is dict and set(value) == expected:
        return value
    raise _fail(f"splitting_degree: exact {label} field census required")


def _input(conductor: int, coefficients: object) -> tuple[int, Polynomial, Polynomial]:
    radicand, values = factors._domain(conductor, coefficients)
    if len(values) not in (4, 5):
        raise _fail("splitting_degree: polynomial degree must be three or four")
    monic = [factors._div(value, values[0], radicand) for value in values]
    return radicand, values, monic


def _require_irreducible(conductor: int, monic: Polynomial, certificate: dict[str, Any]) -> None:
    rows = certificate["factors"]
    if len(rows) != 1 or type(rows[0]["multiplicity"]) is not int or rows[0]["multiplicity"] != 1:
        raise _fail("splitting_degree: input must be irreducible over the declared real field")
    if factors._parse_polynomial(conductor, rows[0]["polynomial"]) != monic:
        raise _fail("splitting_degree: input must be irreducible over the declared real field")


def _resolvent_pattern(certificate: dict[str, Any]) -> list[int]:
    rows = certificate["factors"]
    for row in rows:
        if type(row["multiplicity"]) is not int or row["multiplicity"] != 1:
            raise _fail("splitting_degree: resolvent factors must have unit multiplicity")
    return sorted(len(row["polynomial"]) - 1 for row in rows)


def _resolvent_root(conductor: int, certificate: dict[str, Any]) -> Coordinates:
    linear = [row for row in certificate["factors"] if len(row["polynomial"]) == 2]
    if len(linear) != 1:
        raise _fail("splitting_degree: unique real-field resolvent root required")
    polynomial = factors._parse_polynomial(conductor, linear[0]["polynomial"])
    return factors._neg(polynomial[1])


def _cubic_group(square: bool) -> tuple[str, int]:
    return ("C3", 3) if square else ("S3", 6)


def _quartic_resolvent_group(square: bool) -> tuple[str, int]:
    return ("A4", 12) if square else ("S4", 24)


def _cyclic_or_dihedral(first_square: bool | None, second_square: bool | None) -> tuple[str, int]:
    if type(first_square) is not bool or type(second_square) is not bool:
        raise _fail("splitting_degree: both cyclic square tests required")
    return ("C4", 4) if first_square and second_square else ("D4", 8)


def _quartic_group(
    square: bool,
    pattern: list[int] | None,
    first_square: bool | None,
    second_square: bool | None,
) -> tuple[str, int]:
    if pattern == [3]:
        return _quartic_resolvent_group(square)
    if pattern == [1, 1, 1] and square:
        return "V4", 4
    if pattern == [1, 2] and not square:
        return _cyclic_or_dihedral(first_square, second_square)
    raise _fail("splitting_degree: inconsistent resolvent pattern and discriminant")


def _classification(
    degree: int,
    square: bool,
    pattern: list[int] | None,
    first_square: bool | None = None,
    second_square: bool | None = None,
) -> tuple[str, int]:
    if degree == 3:
        return _cubic_group(square)
    return _quartic_group(square, pattern, first_square, second_square)


def _square_flag(certificate: object) -> bool:
    record = certificate if isinstance(certificate, dict) else None
    flag = None if record is None else record.get("is_square")
    if type(flag) is bool:
        return flag
    raise _fail("splitting_degree: Boolean discriminant square verdict required")


def _square_tests(
    conductor: int,
    first: Coordinates,
    second: Coordinates,
) -> tuple[dict[str, Any], dict[str, Any], bool, bool]:
    first_certificate = real.square_certificate(conductor, first)
    second_certificate = real.square_certificate(conductor, second)
    return (
        first_certificate,
        second_certificate,
        _square_flag(first_certificate),
        _square_flag(second_certificate),
    )


def _cyclic_resolvent(
    conductor: int,
    monic: Polynomial,
    decomposition: dict[str, Any],
    discriminant: Coordinates,
    radicand: int,
) -> tuple[list[str], dict[str, Any], bool, bool]:
    root = _resolvent_root(conductor, decomposition)
    first, second = _cyclic_values(monic, root, discriminant, radicand)
    first_certificate, second_certificate, first_square, second_square = _square_tests(conductor, first, second)
    tests = {
        "first_value": real._wire(first),
        "first_square": first_certificate,
        "second_value": real._wire(second),
        "second_square": second_certificate,
    }
    return real._wire(root), tests, first_square, second_square


def _make_resolvent(
    conductor: int,
    monic: Polynomial,
    resolvent_polynomial: Polynomial,
    discriminant: Coordinates,
    radicand: int,
) -> tuple[dict[str, Any], list[int], bool | None, bool | None]:
    decomposition = factors.factor_polynomial(conductor, resolvent_polynomial)
    pattern = _resolvent_pattern(decomposition)
    root: list[str] | None = None
    tests: dict[str, Any] | None = None
    first_square: bool | None = None
    second_square: bool | None = None
    if pattern == [1, 2]:
        root, tests, first_square, second_square = _cyclic_resolvent(
            conductor, monic, decomposition, discriminant, radicand
        )
    resolvent = {
        "coefficients": factors._wire(resolvent_polynomial),
        "factorization": decomposition,
        "factor_degrees": pattern,
        "root": root,
        "cyclic_tests": tests,
    }
    return resolvent, pattern, first_square, second_square


def irreducible_splitting_degree(conductor: object, coefficients: object) -> dict[str, Any]:
    """Compute the splitting degree over E for one irreducible cubic or quartic."""
    number = _require_conductor(conductor)
    _scan_coefficients(coefficients)
    radicand, values, monic = _input(number, coefficients)
    factorization = factors.factor_polynomial(number, values)
    _require_irreducible(number, monic, factorization)
    resolvent_polynomial, discriminant = _prepared(monic, radicand)
    if discriminant == ZERO:
        raise _fail("splitting_degree: irreducible characteristic-zero input has zero discriminant")
    square = real.square_certificate(number, discriminant)
    resolvent: dict[str, Any] | None = None
    pattern: list[int] | None = None
    first_square: bool | None = None
    second_square: bool | None = None
    if resolvent_polynomial is not None:
        resolvent, pattern, first_square, second_square = _make_resolvent(
            number, monic, resolvent_polynomial, discriminant, radicand
        )
    group, extension_degree = _classification(
        len(monic) - 1, _square_flag(square), pattern, first_square, second_square
    )
    return {
        "schema": SCHEMA,
        "authority_effect": "None",
        "algorithm": ALGORITHM,
        "conductor": number,
        "real_generator_radicand": radicand,
        "coefficient_field": factors._field(radicand),
        "degree_over_real_field": extension_degree,
        "galois_group": group,
        "coefficients": factors._wire(values),
        "monic_polynomial": factors._wire(monic),
        "factorization": factorization,
        "discriminant": real._wire(discriminant),
        "discriminant_square": square,
        "resolvent": resolvent,
    }


def _require_text(result: dict[str, Any], key: str) -> None:
    if type(result[key]) is not str:
        raise _fail(f"splitting_degree: string metadata required: {key}")


def _require_int_meta(result: dict[str, Any], key: str) -> None:
    if type(result[key]) is not int:
        raise _fail(f"splitting_degree: exact integer metadata required: {key}")


def _require_metadata(result: dict[str, Any]) -> None:
    for key in ("schema", "authority_effect", "algorithm", "coefficient_field", "galois_group"):
        _require_text(result, key)
    for key in ("conductor", "real_generator_radicand", "degree_over_real_field"):
        _require_int_meta(result, key)


def _binding(conductor: int, radicand: int) -> dict[str, object]:
    return {
        "schema": SCHEMA,
        "authority_effect": "None",
        "algorithm": ALGORITHM,
        "conductor": conductor,
        "real_generator_radicand": radicand,
        "coefficient_field": factors._field(radicand),
    }


def _require_binding(
    result: dict[str, Any],
    conductor: int,
    radicand: int,
    values: Polynomial,
    monic: Polynomial,
) -> None:
    expected = _binding(conductor, radicand)
    if any(result[key] != value for key, value in expected.items()):
        raise _fail("splitting_degree: metadata or coefficient-field binding differs")
    if factors._parse_polynomial(conductor, result["coefficients"]) != values:
        raise _fail("splitting_degree: original polynomial binding differs")
    if factors._parse_polynomial(conductor, result["monic_polynomial"]) != monic:
        raise _fail("splitting_degree: normalized monic polynomial binding differs")


def _require_discriminant(conductor: int, result: dict[str, Any], discriminant: Coordinates) -> bool:
    if discriminant == ZERO or real._parse_coordinates(conductor, result["discriminant"]) != discriminant:
        raise _fail("splitting_degree: nonzero discriminant binding differs")
    real.validate_square_certificate(conductor, discriminant, result["discriminant_square"])
    return _square_flag(result["discriminant_square"])


def _require_degree_list(value: object) -> list[int]:
    if type(value) is not list:
        raise _fail("splitting_degree: exact integer resolvent factor degrees required")
    degrees: list[int] = []
    for item in value:
        if type(item) is not int:
            raise _fail("splitting_degree: exact integer resolvent factor degrees required")
        degrees.append(item)
    return degrees


def _require_cyclic_value(
    conductor: int,
    tests: dict[str, Any],
    label: str,
    value: Coordinates,
) -> None:
    if real._parse_coordinates(conductor, tests[f"{label}_value"]) != value:
        raise _fail(f"splitting_degree: {label} cyclic value binding differs")
    real.validate_square_certificate(conductor, value, tests[f"{label}_square"])


def _require_cyclic(
    conductor: int,
    resolvent: dict[str, Any],
    monic: Polynomial,
    discriminant: Coordinates,
    radicand: int,
) -> tuple[bool, bool]:
    root = _resolvent_root(conductor, resolvent["factorization"])
    if real._parse_coordinates(conductor, resolvent["root"]) != root:
        raise _fail("splitting_degree: unique resolvent root binding differs")
    first, second = _cyclic_values(monic, root, discriminant, radicand)
    tests = _fields(resolvent["cyclic_tests"], _CYCLIC_FIELDS, "cyclic tests")
    _require_cyclic_value(conductor, tests, "first", first)
    _require_cyclic_value(conductor, tests, "second", second)
    return _square_flag(tests["first_square"]), _square_flag(tests["second_square"])


def _require_resolvent_body(
    conductor: int,
    resolvent: dict[str, Any],
    resolvent_polynomial: Polynomial,
    monic: Polynomial,
    discriminant: Coordinates,
    radicand: int,
) -> tuple[list[int], bool | None, bool | None]:
    supplied = _require_degree_list(resolvent["factor_degrees"])
    if factors._parse_polynomial(conductor, resolvent["coefficients"]) != resolvent_polynomial:
        raise _fail("splitting_degree: resolvent coefficient binding differs")
    factors.validate_factorization(conductor, resolvent_polynomial, resolvent["factorization"])
    pattern = _resolvent_pattern(resolvent["factorization"])
    if supplied != pattern:
        raise _fail("splitting_degree: resolvent factor-degree census differs")
    if pattern == [1, 2]:
        first_square, second_square = _require_cyclic(conductor, resolvent, monic, discriminant, radicand)
        return pattern, first_square, second_square
    if resolvent["root"] is not None or resolvent["cyclic_tests"] is not None:
        raise _fail("splitting_degree: inapplicable resolvent root and cyclic tests must be null")
    return pattern, None, None


def _optional_resolvent(
    conductor: int,
    result: dict[str, Any],
    monic: Polynomial,
    discriminant: Coordinates,
    radicand: int,
    resolvent_polynomial: Polynomial | None,
) -> tuple[list[int] | None, bool | None, bool | None]:
    resolvent = result["resolvent"]
    if resolvent_polynomial is None:
        if resolvent is not None:
            raise _fail("splitting_degree: cubic resolvent field must be null")
        return None, None, None
    record = _fields(resolvent, _RESOLVENT_FIELDS, "resolvent")
    return _require_resolvent_body(conductor, record, resolvent_polynomial, monic, discriminant, radicand)


def _checked_branch(
    conductor: int,
    result: dict[str, Any],
    monic: Polynomial,
    radicand: int,
) -> tuple[str, int]:
    resolvent_polynomial, discriminant = _prepared(monic, radicand)
    square = _require_discriminant(conductor, result, discriminant)
    pattern, first_square, second_square = _optional_resolvent(
        conductor, result, monic, discriminant, radicand, resolvent_polynomial
    )
    return _classification(len(monic) - 1, square, pattern, first_square, second_square)


def _validate_splitting_degree(conductor: int, coefficients: object, result: object) -> None:
    radicand, values, monic = _input(conductor, coefficients)
    record = _fields(result, RESULT_FIELDS, "result")
    _require_metadata(record)
    _require_binding(record, conductor, radicand, values, monic)
    factors.validate_factorization(conductor, values, record["factorization"])
    _require_irreducible(conductor, monic, record["factorization"])
    group, extension_degree = _checked_branch(conductor, record, monic, radicand)
    if record["galois_group"] != group or record["degree_over_real_field"] != extension_degree:
        raise _fail("splitting_degree: Galois group or real-field degree differs from arithmetic branch")


def validate_splitting_degree(conductor: object, coefficients: object, certificate: object) -> None:
    """Recompute the resolvent branch and validate the supplied arithmetic proofs."""
    number = _require_conductor(conductor)
    _scan_coefficients(coefficients)
    try:
        _validate_splitting_degree(number, coefficients, certificate)
    except (KeyError, IndexError, TypeError, AttributeError, ZeroDivisionError) as error:
        raise _fail("splitting_degree: malformed nested certificate or input") from error


def dispatch(request: object) -> dict[str, Any]:
    record = _fields(request, _REQUEST_FIELDS, "request")
    if type(record["operation"]) is not str or record["operation"] != "irreducible_splitting_degree":
        raise _fail("splitting_degree: irreducible_splitting_degree operation required")
    number = _require_conductor(record["conductor"])
    coefficients = factors._parse_polynomial(number, record["coefficients"])
    return irreducible_splitting_degree(number, coefficients)


def _reject_inexact(token: str) -> None:
    raise _fail("splitting_degree: inexact JSON number forbidden", token=token)


def main() -> int:
    try:
        if len(sys.argv) != 1:
            raise _fail("splitting_degree: stdin request only; no CLI arguments permitted")
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


def witness_s3_degree() -> int:
    """Splitting degree of x^3 - 2 over Q, which is 6."""
    coefficients = [(Q(1), Q(0)), (Q(0), Q(0)), (Q(0), Q(0)), (Q(-2), Q(0))]
    degree = irreducible_splitting_degree(1, coefficients)["degree_over_real_field"]
    if type(degree) is not int:
        raise _fail("splitting_degree: exact integer metadata required: degree_over_real_field")
    return degree


if __name__ == "__main__":
    raise SystemExit(main())
