"""Triangle coboundary holonomy of a rational 0-cochain.

Origin: lean4/CoboundaryHolonomy.lean theorem coboundary_triangle_holonomy_zero
(path_holonomy (coboundary φ) (triangle_cycle a b c) = 0) and def coboundary
((δφ)(u, v) = φ v - φ u).
Claim: urn:omega:fqm:obstruction:triangle-coboundary:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_obstruction_calc.py.
Gate 5: earlier measurements are retained in contract history; the changed source requires a fresh structural assessment.
Scope Fence: face_obstruction returns the sum of successive differences around
a length-3 rational triple after that cycle sum agrees with the reading
(v1 - v0) - (v2 - v0) + (v2 - v1). certified_obstruction checks (0, 1/2, 3/5)
and requires 0. The cited theorem is integer holonomy of a coboundary on
triangle_cycle. This file uses Python Fraction, does not prove that theorem,
and does not claim square holonomy or that a nonzero cochain is not a
coboundary.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_FIXTURE: tuple[object, ...] = (Fraction(0), Fraction(1, 2), Fraction(3, 5))
_ZERO = Fraction(0)


class ObstructionError(Exception):
    """One violated triangle-coboundary invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> ObstructionError:
    return ObstructionError(invariant, parameters)


def _default(vertices: object | None) -> object:
    if vertices is None:
        return _FIXTURE
    return vertices


def _require_tuple(vertices: object) -> tuple[object, ...]:
    if isinstance(vertices, (str, bytes)) or not isinstance(vertices, tuple):
        raise _fail("triangle vertices are not a tuple", received=type(vertices).__name__)
    return tuple(vertices)


def _require_three(vertices: tuple[object, ...]) -> tuple[object, ...]:
    if len(vertices) != 3:
        raise _fail("triangle vertices are not three", length=len(vertices))
    return vertices


def _require_value(value: object, index: int) -> Fraction:
    if issubclass(type(value), float):
        raise _fail("float refused at the vertex boundary", index=index, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational vertex was required", index=index)
    if type(value) in (int, Fraction):
        numerator = value if type(value) is int else value.numerator
        denominator = 1 if type(value) is int else value.denominator
        if max(numerator.bit_length(), denominator.bit_length()) > 1024:
            raise _fail("exact scalar exceeds the 1024-bit limit", index=index)
    if type(value) is Fraction:
        vertex = value
    elif type(value) is int:
        vertex = Fraction(value)
    else:
        raise _fail(
            "triangle vertex is not an exact rational",
            index=index,
            received=type(value).__name__,
        )
    return vertex


def _collect(vertices: tuple[object, ...]) -> tuple[Fraction, ...]:
    collected: list[Fraction] = []
    for index, value in enumerate(vertices):
        collected.append(_require_value(value, index))
    return tuple(collected)


def _edge(start: Fraction, end: Fraction) -> Fraction:
    return end - start


def _cycle(vertices: tuple[Fraction, ...]) -> Fraction:
    first = _edge(vertices[0], vertices[1])
    second = _edge(vertices[1], vertices[2])
    third = _edge(vertices[2], vertices[0])
    return first + second + third


def _signed(vertices: tuple[Fraction, ...]) -> Fraction:
    left = vertices[1] - vertices[0]
    middle = vertices[2] - vertices[0]
    right = vertices[2] - vertices[1]
    return left - middle + right


def face_obstruction(vertices: object | None = None) -> Fraction:
    """Return the triangle coboundary holonomy of a rational triple."""
    checked = _collect(_require_three(_require_tuple(_default(vertices))))
    cycle = _cycle(checked)
    signed = _signed(checked)
    if cycle != signed:
        raise _fail(
            "edge reading differs from the signed face",
            cycle=str(cycle),
            signed=str(signed),
        )
    return cycle


def certified_obstruction() -> Fraction:
    """Holonomy of (0, 1/2, 3/5). It must be 0."""
    value = face_obstruction()
    if value != _ZERO:
        raise _fail("certified triangle holonomy is not zero", holonomy=str(value))
    return value


def main() -> int:
    value = certified_obstruction()
    print(value)
    if value == _ZERO:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
