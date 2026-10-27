"""2 by 2 toric-code dimension from even star-plaquette overlaps.

Origin: lean4/SurfaceCodeToricTopology.lean theorem homology_dimension_k2
((8 : Int) - (4 - 1) - (4 - 1) = 2).
Claim: urn:omega:fqm:qm:toric-dimension:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/qm/tests/test_isolated_certificates.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 10; AST Sonar cognitive complexity max 9; AST nesting depth max 3; lizard 1.24.1 cyclomatic complexity max 10.
Scope Fence: The supports are the four stars and four plaquettes on eight
edges. The file checks even overlap and the rank formula. It does not claim
a distance or a threshold.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping

_DIMENSION = 2


class ToricError(Exception):
    """One violated toric invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> ToricError:
    return ToricError(invariant, parameters)


def _require_fraction(value: object, role: str) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def _vertex(row: int, col: int) -> frozenset[int]:
    return frozenset({
        row * 2 + col,
        row * 2 + ((col - 1) % 2),
        4 + row * 2 + col,
        4 + ((row - 1) % 2) * 2 + col,
    })


def _plaquette(row: int, col: int) -> frozenset[int]:
    return frozenset({
        row * 2 + col,
        4 + row * 2 + ((col + 1) % 2),
        ((row + 1) % 2) * 2 + col,
        4 + row * 2 + col,
    })


def _bits(support: frozenset[int]) -> list[int]:
    return [1 if index in support else 0 for index in range(8)]


def _pivot(matrix: list[list[int]], column: int, start: int) -> int | None:
    row = start
    while row < len(matrix):
        if matrix[row][column] == 1:
            return row
        row += 1
    return None


def _clear(matrix: list[list[int]], column: int, pivot: int) -> None:
    other = 0
    while other < len(matrix):
        if other != pivot and matrix[other][column] == 1:
            matrix[other] = [left ^ right for left, right in zip(matrix[other], matrix[pivot])]
        other += 1


def _rank(rows: list[list[int]]) -> int:
    matrix = [row[:] for row in rows]
    pivot_row = 0
    column = 0
    while column < 8:
        host = _pivot(matrix, column, pivot_row)
        if host is not None:
            matrix[pivot_row], matrix[host] = matrix[host], matrix[pivot_row]
            _clear(matrix, column, pivot_row)
            pivot_row += 1
        column += 1
    return pivot_row


def _even(vertices: tuple[frozenset[int], ...], plaquettes: tuple[frozenset[int], ...]) -> bool:
    for vertex in vertices:
        for plaquette in plaquettes:
            if len(vertex & plaquette) % 2 != 0:
                return False
    return True


def _formula() -> int:
    value = _require_fraction(8, "edges") - (_require_fraction(4, "stars") - _require_fraction(1, "one"))
    value = value - (_require_fraction(4, "plaquettes") - _require_fraction(1, "oneb"))
    return int(value)


def toric_dimension() -> int:
    """Return n - rank(Hx) - rank(Hz) after the even-overlap check."""
    vertices = tuple(_vertex(row, col) for row in range(2) for col in range(2))
    plaquettes = tuple(_plaquette(row, col) for row in range(2) for col in range(2))
    if not _even(vertices, plaquettes):
        raise _fail("a vertex check anticommutes with a plaquette check")
    rank_z = _rank([_bits(support) for support in vertices])
    rank_x = _rank([_bits(support) for support in plaquettes])
    dimension = 8 - rank_x - rank_z
    if dimension != _formula():
        raise _fail("toric dimension disagrees with the homology formula", dimension=dimension, formula=_formula())
    if dimension != _DIMENSION:
        raise _fail("toric dimension is not 2", dimension=dimension)
    return dimension


def _locked(value: Fraction, expected: Fraction, invariant: str) -> Fraction:
    if value != expected:
        raise _fail(invariant, value=str(value), expected=str(expected))
    return value


_MARK = 7


def _mark() -> int:
    return _MARK


def certify(probe: object | None = None) -> Fraction:
    """Refuse a non-rational probe, then return the toric dimension 2."""
    if probe is not None:
        _require_fraction(probe, "probe")
    if _mark() != 7:
        raise _fail("certificate mark drifted", mark=_mark())
    return _locked(Fraction(toric_dimension()), Fraction(_DIMENSION), "toric dimension drifted")


def main() -> int:
    value = toric_dimension()
    print(value)
    if value == _DIMENSION:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
