"""Exact real coefficient-field square certificates. AuthorityEffect: None.

This supplies a field-arithmetic prerequisite, not a general splitting degree
or logarithm basis. No approximation or state-admission bound is involved.
"""

from __future__ import annotations

from fractions import Fraction as Q
from math import isqrt
import json
import re
import sys
from typing import Any


RADICANDS = {1: 0, 3: 0, 4: 0, 8: 2, 5: 5}
Coordinates = tuple[Q, Q]


def _domain(conductor: int, coefficients: Any) -> tuple[int, Coordinates]:
    if type(conductor) is not int or conductor not in RADICANDS:
        raise ValueError("real_field: unsupported exact integer conductor")
    if not isinstance(coefficients, (list, tuple)) or len(coefficients) != 2:
        raise ValueError("real_field: two rational coordinates required")
    if any(type(c) is not int and not isinstance(c, Q) for c in coefficients):
        raise ValueError("real_field: exact rational coordinates required")
    a, b = map(Q, coefficients)
    d = RADICANDS[conductor]
    if d == 0 and b != 0:
        raise ValueError("real_field: rational coefficient field requires zero radical coordinate")
    return d, (a, b)


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
        raise ValueError("real_field: impossible rational representation of a nonsquare radical")
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
    chunks = []
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
        result = result * 10**len(chunk) + int(chunk)
    return -result if negative else result


def _fraction_text(value: Q) -> str:
    return _integer_text(value.numerator) + "/" + _integer_text(value.denominator)


def _wire(value: Coordinates) -> list[str]:
    return [_fraction_text(c) for c in value]


def _parse_coordinates(conductor: int, value: Any) -> Coordinates:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError("real_field: two canonical rational strings required")
    parsed = []
    for coefficient in value:
        if (not isinstance(coefficient, str)
                or re.fullmatch(r"-?(0|[1-9][0-9]*)/[1-9][0-9]*", coefficient) is None):
            raise ValueError("real_field: canonical rational string required")
        numerator, denominator = coefficient.split("/")
        number = Q(_integer_from_text(numerator), _integer_from_text(denominator))
        if _fraction_text(number) != coefficient:
            raise ValueError("real_field: rational string must be reduced")
        parsed.append(number)
    return _domain(conductor, parsed)[1]


def square_certificate(conductor: int, coefficients: Any) -> dict[str, Any]:
    """Decide squareness in the real subfield, not in the complex carrier."""
    d, value = _domain(conductor, coefficients)
    a, b = value
    root: Coordinates | None = None
    if d == 0:
        x = _rational_root(a)
        if x is not None:
            root = x, Q(0)
        obstruction = "RATIONAL_NONSQUARE"
    elif b == 0:
        x, y = _rational_root(a), _rational_root(a / d)
        if x is not None:
            root = x, Q(0)
        elif y is not None:
            root = Q(0), y
        obstruction = "RATIONAL_SQUARECLASS_OUTSIDE_1_OR_D"
    else:
        norm_root = _rational_root(a * a - d * b * b)
        obstruction = "NORM_NOT_RATIONAL_SQUARE"
        if norm_root is not None:
            obstruction = "NO_RATIONAL_HALF_TRACE_SQUARE"
            for half_trace in ((a + norm_root) / 2, (a - norm_root) / 2):
                x = _rational_root(half_trace)
                if x is not None and x != 0:
                    root = x, b / (2 * x)
                    break
    if root is not None:
        if _multiply(root, root, d) != value:
            raise ValueError("square_certificate: root reconstruction failed")
        if _sign(root, d) < 0:
            root = -root[0], -root[1]
    return {"schema": "real_field_square_v1", "authority_effect": "None",
            "conductor": conductor, "real_generator_radicand": d,
            "coefficients": _wire(value), "is_square": root is not None,
            "root": None if root is None else _wire(root),
            "obstruction": obstruction if root is None else None}


def _negative_obstruction(value: Coordinates, d: int) -> str:
    """Exhaust the necessary and sufficient algebraic cases; no search absence."""
    a, b = value
    if not d:
        candidates, obstruction = [a], "RATIONAL_NONSQUARE"
    elif not b:
        candidates, obstruction = [a, a / d], "RATIONAL_SQUARECLASS_OUTSIDE_1_OR_D"
    else:
        norm_root = _rational_root(a * a - d * b * b)
        if norm_root is None:
            return "NORM_NOT_RATIONAL_SQUARE"
        candidates = [(a + norm_root) / 2, (a - norm_root) / 2]
        obstruction = "NO_RATIONAL_HALF_TRACE_SQUARE"
    if any(_rational_root(candidate) is not None for candidate in candidates):
        raise ValueError("square_certificate: false nonsquare claim")
    return obstruction


def validate_square_certificate(conductor: int, coefficients: Any, certificate: Any) -> None:
    """Bind input and verify a witness or the exhaustive nonsquare obstruction."""
    d, value = _domain(conductor, coefficients)
    keys = {"schema", "authority_effect", "conductor", "real_generator_radicand",
            "coefficients", "is_square", "root", "obstruction"}
    if not isinstance(certificate, dict) or set(certificate) != keys:
        raise ValueError("square_certificate: exact field census required")
    if (certificate["schema"] != "real_field_square_v1" or certificate["authority_effect"] != "None"
            or type(certificate["conductor"]) is not int or certificate["conductor"] != conductor
            or type(certificate["real_generator_radicand"]) is not int
            or certificate["real_generator_radicand"] != d
            or _parse_coordinates(conductor, certificate["coefficients"]) != value):
        raise ValueError("square_certificate: original input or field binding differs")
    if type(certificate["is_square"]) is not bool:
        raise ValueError("square_certificate: Boolean square verdict required")
    if certificate["is_square"]:
        root = _parse_coordinates(conductor, certificate["root"])
        if certificate["obstruction"] is not None:
            raise ValueError("square_certificate: a root cannot carry a nonsquare obstruction")
        if _multiply(root, root, d) != value:
            raise ValueError("square_certificate: supplied root does not square to the input")
        if _sign(root, d) < 0:
            raise ValueError("square_certificate: supplied root has negative embedding sign")
    else:
        if certificate["root"] is not None:
            raise ValueError("square_certificate: nonsquare certificate has a root")
        if certificate["obstruction"] != _negative_obstruction(value, d):
            raise ValueError("square_certificate: nonsquare obstruction differs")


def _nonzero_pair(conductor: int, left: Any, right: Any) -> tuple[int, Coordinates, Coordinates]:
    d, lhs = _domain(conductor, left)
    _, rhs = _domain(conductor, right)
    if lhs == (0, 0) or rhs == (0, 0):
        raise ValueError("squareclass: both arguments must be nonzero")
    return d, lhs, rhs


def squareclass_certificate(conductor: int, left: Any, right: Any) -> dict[str, Any]:
    d, lhs, rhs = _nonzero_pair(conductor, left, right)
    norm = rhs[0] * rhs[0] - d * rhs[1] * rhs[1]
    quotient = _multiply(lhs, (rhs[0] / norm, -rhs[1] / norm), d)
    square = square_certificate(conductor, quotient)
    return {"schema": "real_field_squareclass_v1", "authority_effect": "None",
            "conductor": conductor, "left": _wire(lhs), "right": _wire(rhs),
            "quotient": _wire(quotient), "same_squareclass": square["is_square"],
            "square_certificate": square}


def validate_squareclass_certificate(conductor: int, left: Any, right: Any, certificate: Any) -> None:
    d, lhs, rhs = _nonzero_pair(conductor, left, right)
    keys = {"schema", "authority_effect", "conductor", "left", "right", "quotient",
            "same_squareclass", "square_certificate"}
    if not isinstance(certificate, dict) or set(certificate) != keys:
        raise ValueError("squareclass: exact field census required")
    if (certificate["schema"] != "real_field_squareclass_v1" or certificate["authority_effect"] != "None"
            or type(certificate["conductor"]) is not int or certificate["conductor"] != conductor
            or _parse_coordinates(conductor, certificate["left"]) != lhs
            or _parse_coordinates(conductor, certificate["right"]) != rhs):
        raise ValueError("squareclass: original input or field binding differs")
    quotient = _parse_coordinates(conductor, certificate["quotient"])
    if _multiply(quotient, rhs, d) != lhs:
        raise ValueError("squareclass: quotient does not reconstruct the original arguments")
    validate_square_certificate(conductor, quotient, certificate["square_certificate"])
    if (type(certificate["same_squareclass"]) is not bool
            or certificate["same_squareclass"] != certificate["square_certificate"]["is_square"]):
        raise ValueError("squareclass: quotient square verdict differs")


def dispatch(request: Any) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("real_field: request object required")
    operation = request.get("operation")
    if operation == "square" and set(request) == {"operation", "conductor", "coefficients"}:
        n = request["conductor"]
        return square_certificate(n, _parse_coordinates(n, request["coefficients"]))
    if operation == "squareclass" and set(request) == {"operation", "conductor", "left", "right"}:
        n = request["conductor"]
        return squareclass_certificate(n, _parse_coordinates(n, request["left"]),
                                       _parse_coordinates(n, request["right"]))
    raise ValueError("real_field: exact request fields and known operation required")


def _reject_inexact(token: str) -> None:
    raise ValueError(f"real_field: inexact JSON number forbidden: {token}")


def main() -> int:
    try:
        if len(sys.argv) != 1:
            raise ValueError("real_field: stdin request only; no CLI arguments permitted")
        request = json.loads(sys.stdin.buffer.read(), parse_float=_reject_inexact, parse_constant=_reject_inexact)
        result = dispatch(request)
    except (ValueError, TypeError, ZeroDivisionError) as error:
        print(str(error), file=sys.stderr)
        return 2
    sys.stdout.buffer.write((json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
