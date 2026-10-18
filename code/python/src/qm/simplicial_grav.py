"""Even boundary area of a glued simplicial 3-complex.

Origin: lean4/H022SimplicialAreaLawPageCurve.lean theorem boundary_area_even
((boundary_area N M_int) % 2 = 0) and theorem gluing_reduces_boundary
(M_int > 0 implies boundary_area N M_int < 4 * N), where
boundary_area N M_int = 4 * N - 2 * M_int.
Claim: urn:omega:fqm:grav:boundary-area-even:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_simplicial_grav.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: boundary_face_area computes 4 * N - 2 * M for nonnegative
integers, requires the value to be even, and requires a positive interior
count to land strictly below 4 * N. polygon_area returns the shoelace area
of the rectangle (0, 0), (4, 0), (4, 3), (0, 3), which is 12. That shoelace
reading is not boundary_area. The numeral 12 also occurs as
boundary_face_area(3, 0). This file does not prove the Page curve, the
holographic microstate bounds, or a continuous area law.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping


class SimplicialGravityError(Exception):
    """One violated area invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> SimplicialGravityError:
    return SimplicialGravityError(invariant, parameters)


def _require_nat(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the count boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a natural count was required", role=role)
    if type(value) is not int:
        raise _fail("count is not an integer", role=role, received=type(value).__name__)
    if value < 0:
        raise _fail("count is negative", role=role, value=value)
    return value


def _area(simplex_count: int, interior_faces: int) -> int:
    return 4 * simplex_count - 2 * interior_faces


def _require_even(area: int) -> int:
    if area % 2 != 0:
        raise _fail("boundary area is odd", area=area)
    return area


def _require_gluing(area: int, simplex_count: int, interior_faces: int) -> None:
    if interior_faces > 0 and area >= 4 * simplex_count:
        raise _fail("gluing did not reduce the boundary", area=area, simplices=simplex_count)


def boundary_face_area(simplex_count: object = 3, interior_faces: object = 0) -> int:
    """Return 4 * N - 2 * M and require that value to be even."""
    simplices = _require_nat(simplex_count, "simplices")
    interior = _require_nat(interior_faces, "interior")
    area = _require_even(_area(simplices, interior))
    _require_gluing(area, simplices, interior)
    return area


def _shoelace(vertices: tuple[tuple[int, int], ...]) -> Fraction:
    total = Fraction(0)
    for index, (x_pos, y_pos) in enumerate(vertices):
        nxt = vertices[(index + 1) % len(vertices)]
        total += Fraction(x_pos) * Fraction(nxt[1]) - Fraction(nxt[0]) * Fraction(y_pos)
    return abs(total) / 2


def polygon_area() -> Fraction:
    """Return the shoelace area of the 4 by 3 rectangle, which is 12."""
    rectangle = ((0, 0), (4, 0), (4, 3), (0, 3))
    whole = _shoelace(rectangle)
    if whole != Fraction(12):
        raise _fail("shoelace rectangle is not 12", area=str(whole))
    return whole


def main() -> int:
    value = boundary_face_area()
    shoelace = polygon_area()
    print(value)
    if value == 12 and shoelace == Fraction(12):
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
