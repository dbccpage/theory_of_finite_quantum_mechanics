"""Exact square certificates in the real coefficient fields.

Origin: code/rust/src/linear_algebra/field_squares.rs, which states the exact
square and squareclass certificates in Q, Q(sqrt(2)), and Q(sqrt(5)).
Claim: urn:omega:fqm:linear-algebra:real-square-certificate:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_field_squares.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 7; AST Sonar cognitive complexity max 7; AST nesting depth max 3; lizard 1.24.1 cyclomatic complexity max 7.
Scope Fence: a certificate reports a positive square root or one of the Rust
obstruction names, using math.isqrt for the integer square root. This file does
not run the Rust Newton loop, does not compute a splitting degree or a
logarithm basis, and does not admit floats or Q(i).
"""

from __future__ import annotations

import json
import re
import sys
from fractions import Fraction as Q
from math import isqrt
from typing import Any, Mapping

from .scalars import GaussianRational


RADICANDS = {1: 0, 3: 0, 4: 0, 8: 2, 5: 5}
Coordinates = tuple[Q, Q]
_SQUARE_KEYS = {
    "schema",
    "authority_effect",
    "conductor",
    "real_generator_radicand",
    "coefficients",
    "is_square",
    "root",
    "obstruction",
}
_CLASS_KEYS = {
    "schema",
    "authority_effect",
    "conductor",
    "left",
    "right",
    "quotient",
    "same_squareclass",
    "square_certificate",
}


class FieldSquareError(ValueError):
    """One violated real-square invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> FieldSquareError:
    return FieldSquareError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _require_conductor(value: object) -> int:
    _refuse_float(value, "conductor")
    if type(value) is bool:
        raise _fail("boolean refused where a conductor was required", role="conductor")
    if type(value) is int and value in RADICANDS:
        return value
    raise _fail("real_field: unsupported exact integer conductor", received=type(value).__name__)


def _require_coordinate(value: object, role: str) -> Q:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a rational coordinate was required", role=role)
    if isinstance(value, GaussianRational):
        raise _fail(
            "Gaussian rational refused; square certificates in this module are over a real field",
            role=role,
        )
    if isinstance(value, Q):
        return value
    if type(value) is int:
        return Q(value)
    raise _fail("real_field: exact rational coordinates required", role=role, received=type(value).__name__)


def _require_pair(coefficients: object) -> tuple[object, object]:
    if isinstance(coefficients, (list, tuple)) and len(coefficients) == 2:
        return coefficients[0], coefficients[1]
    raise _fail("real_field: two rational coordinates required", received=type(coefficients).__name__)


def _domain(conductor: object, coefficients: object) -> tuple[int, Coordinates]:
    number = _require_conductor(conductor)
    left, right = _require_pair(coefficients)
    pair = (
        _require_coordinate(left, "coordinate[0]"),
        _require_coordinate(right, "coordinate[1]"),
    )
    radicand = RADICANDS[number]
    if radicand == 0 and pair[1] != 0:
        raise _fail("real_field: rational coefficient field requires zero radical coordinate", conductor=number)
    return radicand, pair


def _rational_root(value: Q) -> Q | None:
    if value < 0:
        return None
    numerator, denominator = isqrt(value.numerator), isqrt(value.denominator)
    if numerator * numerator != value.numerator or denominator * denominator != value.denominator:
        return None
    return Q(numerator, denominator)


def _sign(value: Coordinates, d: int) -> int:
    a, b = value
    if not b:
        return (a > 0) - (a < 0)
    if not a or (a > 0) == (b > 0):
        return (b > 0) - (b < 0)
    comparison = a * a - d * b * b
    if not comparison:
        raise _fail("real_field: impossible rational representation of a nonsquare radical")
    return ((comparison > 0) - (comparison < 0)) * (1 if a > 0 else -1)


def _multiply(left: Coordinates, right: Coordinates, d: int) -> Coordinates:
    a, b = left
    c, e = right
    return a * c + d * b * e, a * e + b * c


def _integer_text(value: int) -> str:
    """Uncapped decimal output without changing interpreter-global limits."""
    if value == 0:
        return "0"
    sign, remaining = ("-" if value < 0 else ""), abs(value)
    chunks: list[int] = []
    while remaining:
        remaining, chunk = divmod(remaining, 10**9)
        chunks.append(chunk)
    return sign + str(chunks[-1]) + "".join(f"{chunk:09d}" for chunk in reversed(chunks[:-1]))


def _integer_from_text(value: str) -> int:
    negative = value.startswith("-")
    digits = value[1:] if negative else value
    result = 0
    for start in range(0, len(digits), 9):
        chunk = digits[start:start + 9]
        result = result * 10 ** len(chunk) + int(chunk)
    return -result if negative else result


def _fraction_text(value: Q) -> str:
    return _integer_text(value.numerator) + "/" + _integer_text(value.denominator)


def _wire(value: Coordinates) -> list[str]:
    return [_fraction_text(coordinate) for coordinate in value]


def _parse_one(coefficient: object) -> Q:
    if not isinstance(coefficient, str) or re.fullmatch(r"-?(0|[1-9][0-9]*)/[1-9][0-9]*", coefficient) is None:
        raise _fail("real_field: canonical rational string required")
    numerator, denominator = coefficient.split("/")
    number = Q(_integer_from_text(numerator), _integer_from_text(denominator))
    if _fraction_text(number) != coefficient:
        raise _fail("real_field: rational string must be reduced")
    return number


def _parse_coordinates(conductor: object, value: object) -> Coordinates:
    if not isinstance(value, list) or len(value) != 2:
        raise _fail("real_field: two canonical rational strings required")
    return _domain(conductor, [_parse_one(coefficient) for coefficient in value])[1]


def _rational_decision(a: Q) -> tuple[Coordinates | None, str]:
    root = _rational_root(a)
    if root is None:
        return None, "RATIONAL_NONSQUARE"
    return (root, Q(0)), "RATIONAL_NONSQUARE"


def _unit_or_radicand(a: Q, d: int) -> tuple[Coordinates | None, str]:
    rational = _rational_root(a)
    if rational is not None:
        return (rational, Q(0)), "RATIONAL_SQUARECLASS_OUTSIDE_1_OR_D"
    radical = _rational_root(a / d)
    if radical is not None:
        return (Q(0), radical), "RATIONAL_SQUARECLASS_OUTSIDE_1_OR_D"
    return None, "RATIONAL_SQUARECLASS_OUTSIDE_1_OR_D"


def _half_trace_hit(b: Q, half_trace: Q) -> Coordinates | None:
    x = _rational_root(half_trace)
    if x is None or x == 0:
        return None
    return x, b / (2 * x)


def _half_trace_scan(a: Q, b: Q, norm_root: Q) -> Coordinates | None:
    for half_trace in ((a + norm_root) / 2, (a - norm_root) / 2):
        found = _half_trace_hit(b, half_trace)
        if found is not None:
            return found
    return None


def _norm_decision(a: Q, b: Q, d: int) -> tuple[Coordinates | None, str]:
    norm_root = _rational_root(a * a - d * b * b)
    if norm_root is None:
        return None, "NORM_NOT_RATIONAL_SQUARE"
    return _half_trace_scan(a, b, norm_root), "NO_RATIONAL_HALF_TRACE_SQUARE"


def _decided_root(d: int, value: Coordinates) -> tuple[Coordinates | None, str]:
    a, b = value
    if d == 0:
        return _rational_decision(a)
    if b == 0:
        return _unit_or_radicand(a, d)
    return _norm_decision(a, b, d)


def _orient_root(root: Coordinates, value: Coordinates, d: int) -> Coordinates:
    if _multiply(root, root, d) != value:
        raise _fail("square_certificate: root reconstruction failed")
    if _sign(root, d) < 0:
        return -root[0], -root[1]
    return root


def square_certificate(conductor: object, coefficients: object) -> dict[str, Any]:
    """Decide squareness in the real subfield, not in the complex carrier."""
    d, value = _domain(conductor, coefficients)
    root, obstruction = _decided_root(d, value)
    published: Coordinates | None = None
    if root is not None:
        published = _orient_root(root, value, d)
    return {
        "schema": "real_field_square_v1",
        "authority_effect": "None",
        "conductor": conductor,
        "real_generator_radicand": d,
        "coefficients": _wire(value),
        "is_square": published is not None,
        "root": None if published is None else _wire(published),
        "obstruction": None if published is not None else obstruction,
    }


def _has_rational_root(candidates: list[Q]) -> bool:
    for candidate in candidates:
        if _rational_root(candidate) is not None:
            return True
    return False


def _negative_obstruction(value: Coordinates, d: int) -> str:
    """Exhaust the necessary and sufficient algebraic cases; no search absence."""
    a, b = value
    if not d:
        candidates, obstruction = [a], "RATIONAL_NONSQUARE"
    elif not b:
        candidates, obstruction = [a, a / d], "RATIONAL_SQUARECLASS_OUTSIDE_1_OR_D"
    else:
        found = _norm_decision(a, b, d)
        if found[0] is not None:
            raise _fail("square_certificate: false nonsquare claim")
        return found[1]
    if _has_rational_root(candidates):
        raise _fail("square_certificate: false nonsquare claim")
    return obstruction


def _require_record(certificate: object, keys: set[str], label: str) -> dict[str, Any]:
    if isinstance(certificate, dict) and set(certificate) == keys:
        return certificate
    raise _fail(f"{label}: exact field census required")


def _same_square_binding(certificate: dict[str, Any], conductor: int, d: int, value: Coordinates) -> bool:
    if certificate["schema"] != "real_field_square_v1" or certificate["authority_effect"] != "None":
        return False
    if type(certificate["conductor"]) is not int or certificate["conductor"] != conductor:
        return False
    if type(certificate["real_generator_radicand"]) is not int or certificate["real_generator_radicand"] != d:
        return False
    return _parse_coordinates(conductor, certificate["coefficients"]) == value


def _require_positive_root(certificate: dict[str, Any], conductor: int, d: int, value: Coordinates) -> None:
    root = _parse_coordinates(conductor, certificate["root"])
    if certificate["obstruction"] is not None:
        raise _fail("square_certificate: a root cannot carry a nonsquare obstruction")
    if _multiply(root, root, d) != value:
        raise _fail("square_certificate: supplied root does not square to the input")
    if _sign(root, d) < 0:
        raise _fail("square_certificate: supplied root has negative embedding sign")


def _require_nonsquare(certificate: dict[str, Any], value: Coordinates, d: int) -> None:
    if certificate["root"] is not None:
        raise _fail("square_certificate: nonsquare certificate has a root")
    if certificate["obstruction"] != _negative_obstruction(value, d):
        raise _fail("square_certificate: nonsquare obstruction differs")


def validate_square_certificate(conductor: object, coefficients: object, certificate: object) -> None:
    """Bind input and verify a witness or the exhaustive nonsquare obstruction."""
    d, value = _domain(conductor, coefficients)
    record = _require_record(certificate, _SQUARE_KEYS, "square_certificate")
    if type(conductor) is not int or not _same_square_binding(record, conductor, d, value):
        raise _fail("square_certificate: original input or field binding differs")
    if type(record["is_square"]) is not bool:
        raise _fail("square_certificate: Boolean square verdict required")
    if record["is_square"]:
        _require_positive_root(record, conductor, d, value)
        return
    _require_nonsquare(record, value, d)


def _nonzero_pair(conductor: object, left: object, right: object) -> tuple[int, Coordinates, Coordinates]:
    d, lhs = _domain(conductor, left)
    _, rhs = _domain(conductor, right)
    if lhs == (Q(0), Q(0)) or rhs == (Q(0), Q(0)):
        raise _fail("squareclass: both arguments must be nonzero")
    return d, lhs, rhs


def _quotient(lhs: Coordinates, rhs: Coordinates, d: int) -> Coordinates:
    norm = rhs[0] * rhs[0] - d * rhs[1] * rhs[1]
    return _multiply(lhs, (rhs[0] / norm, -rhs[1] / norm), d)


def squareclass_certificate(conductor: object, left: object, right: object) -> dict[str, Any]:
    d, lhs, rhs = _nonzero_pair(conductor, left, right)
    quotient = _quotient(lhs, rhs, d)
    square = square_certificate(conductor, quotient)
    return {
        "schema": "real_field_squareclass_v1",
        "authority_effect": "None",
        "conductor": conductor,
        "left": _wire(lhs),
        "right": _wire(rhs),
        "quotient": _wire(quotient),
        "same_squareclass": square["is_square"],
        "square_certificate": square,
    }


def _same_class_binding(
    certificate: dict[str, Any],
    conductor: int,
    lhs: Coordinates,
    rhs: Coordinates,
) -> bool:
    if certificate["schema"] != "real_field_squareclass_v1" or certificate["authority_effect"] != "None":
        return False
    if type(certificate["conductor"]) is not int or certificate["conductor"] != conductor:
        return False
    if _parse_coordinates(conductor, certificate["left"]) != lhs:
        return False
    return _parse_coordinates(conductor, certificate["right"]) == rhs


def validate_squareclass_certificate(
    conductor: object,
    left: object,
    right: object,
    certificate: object,
) -> None:
    d, lhs, rhs = _nonzero_pair(conductor, left, right)
    record = _require_record(certificate, _CLASS_KEYS, "squareclass")
    if type(conductor) is not int or not _same_class_binding(record, conductor, lhs, rhs):
        raise _fail("squareclass: original input or field binding differs")
    quotient = _parse_coordinates(conductor, record["quotient"])
    if _multiply(quotient, rhs, d) != lhs:
        raise _fail("squareclass: quotient does not reconstruct the original arguments")
    validate_square_certificate(conductor, quotient, record["square_certificate"])
    verdict = record["same_squareclass"]
    if type(verdict) is not bool or verdict != record["square_certificate"]["is_square"]:
        raise _fail("squareclass: quotient square verdict differs")


def _square_request(request: dict[str, Any]) -> dict[str, Any] | None:
    if set(request) != {"operation", "conductor", "coefficients"}:
        return None
    conductor = request["conductor"]
    return square_certificate(conductor, _parse_coordinates(conductor, request["coefficients"]))


def _squareclass_request(request: dict[str, Any]) -> dict[str, Any] | None:
    if set(request) != {"operation", "conductor", "left", "right"}:
        return None
    conductor = request["conductor"]
    return squareclass_certificate(
        conductor,
        _parse_coordinates(conductor, request["left"]),
        _parse_coordinates(conductor, request["right"]),
    )


def dispatch(request: object) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise _fail("real_field: request object required", received=type(request).__name__)
    if request.get("operation") == "square":
        square = _square_request(request)
        if square is not None:
            return square
    if request.get("operation") == "squareclass":
        squareclass = _squareclass_request(request)
        if squareclass is not None:
            return squareclass
    raise _fail("real_field: exact request fields and known operation required")


def _reject_inexact(token: str) -> None:
    raise _fail("real_field: inexact JSON number forbidden", token=token)


def _read_request() -> object:
    if len(sys.argv) != 1:
        raise _fail("real_field: stdin request only; no CLI arguments permitted")
    return json.loads(sys.stdin.buffer.read(), parse_float=_reject_inexact, parse_constant=_reject_inexact)


def main() -> int:
    try:
        result = dispatch(_read_request())
    except (ValueError, TypeError, ZeroDivisionError) as error:
        print(str(error), file=sys.stderr)
        return 2
    sys.stdout.buffer.write((json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii"))
    return 0


def witness_positive_root() -> Q:
    """Positive rational square root of 4, the conductor-1 witness."""
    certificate = square_certificate(1, (4, 0))
    root = certificate["root"]
    if not isinstance(root, list) or len(root) != 2:
        raise _fail("square_certificate: supplied root does not square to the input")
    return _parse_one(root[0])


if __name__ == "__main__":
    raise SystemExit(main())
