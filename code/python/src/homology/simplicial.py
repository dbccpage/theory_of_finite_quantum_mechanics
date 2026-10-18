"""Oriented simplicial boundaries whose consecutive squares are measured over Q.

Origin: lean4/CellGrammar.lean structure ChainGrammar field boundarySquare.
That field requires boundary1 (boundary2 face) = zero0.
Claim: urn:omega:fqm:homology:simplicial-boundary-square:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_simplicial.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 7; AST Sonar cognitive complexity max 5; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 7.
Scope Fence: This file certifies the oriented boundary matrices of the
complexes it is given. It does not prove boundarySquare for an arbitrary
chain grammar, and it does not assign a homology group.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence

from ..linear_algebra import ExactMatrix
from .errors import DimensionMismatchError, HomologyError, NonZeroCompositionError


def _fail(kind: type[HomologyError], invariant: str, **parameters: object) -> HomologyError:
    return kind(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail(DimensionMismatchError, "float refused at the public boundary", role=role, received="float")


def _require_vertex(vertex: object, index: int) -> int:
    _refuse_float(vertex, f"vertex[{index}]")
    if isinstance(vertex, bool):
        raise _fail(DimensionMismatchError, "boolean refused where a vertex was required", index=index)
    if type(vertex) is not int:
        raise _fail(
            DimensionMismatchError,
            "simplex vertices must be ints",
            index=index,
            received=type(vertex).__name__,
        )
    return vertex


def _as_sequence(vertices: object) -> tuple[object, ...]:
    if isinstance(vertices, (str, bytes)) or not isinstance(vertices, Sequence):
        raise _fail(
            DimensionMismatchError,
            "simplex vertices must be a sequence",
            received=type(vertices).__name__,
        )
    return tuple(vertices)


def _require_vertices(vertices: object) -> tuple[int, ...]:
    if isinstance(vertices, (str, bytes)) or not isinstance(vertices, tuple):
        raise _fail(
            DimensionMismatchError,
            "simplex vertices must be a tuple",
            received=type(vertices).__name__,
        )
    if len(vertices) == 0:
        raise _fail(DimensionMismatchError, "simplex needs at least one vertex")
    parsed = tuple(_require_vertex(vertex, index) for index, vertex in enumerate(vertices))
    if len(set(parsed)) != len(parsed):
        raise _fail(DimensionMismatchError, "simplex vertices are not distinct", vertices=str(parsed))
    if parsed != tuple(sorted(parsed)):
        raise _fail(DimensionMismatchError, "simplex vertices are not sorted", vertices=str(parsed))
    return parsed


def _require_dim(dim: object, minimum: int, invariant: str) -> int:
    _refuse_float(dim, "dim")
    if isinstance(dim, bool) or not isinstance(dim, int):
        raise _fail(DimensionMismatchError, "dimension is not an integer", received=type(dim).__name__)
    if dim < minimum:
        raise _fail(DimensionMismatchError, invariant, received=dim)
    return dim


def _orientation(omit: int) -> Fraction:
    if omit % 2 == 0:
        return Fraction(1)
    return Fraction(-1)


def _write_face(column: list[Fraction], index: dict[tuple[int, ...], int], omit: int, face: "Simplex") -> None:
    slot = index.get(face.vertices)
    if slot is None:
        raise _fail(DimensionMismatchError, "face is missing from the complex", face=str(face.vertices))
    column[slot] = _orientation(omit)


def _boundary_columns(domain: Sequence["Simplex"], codomain: Sequence["Simplex"]) -> list[list[Fraction]]:
    index = {simplex.vertices: row for row, simplex in enumerate(codomain)}
    columns: list[list[Fraction]] = []
    for simplex in domain:
        column = [Fraction(0) for _ in codomain]
        for omit, face in enumerate(simplex.faces()):
            _write_face(column, index, omit, face)
        columns.append(column)
    return columns


def _matrix_from_columns(columns: Sequence[Sequence[Fraction]], row_count: int) -> ExactMatrix:
    if row_count == 0:
        return ExactMatrix(0, len(columns), [])
    if len(columns) == 0:
        return ExactMatrix(row_count, 0, [])
    rows = [[column[row] for column in columns] for row in range(row_count)]
    return ExactMatrix.from_rows(rows)


def _rational(value: object, role: str) -> Fraction:
    _refuse_float(value, role)
    if isinstance(value, bool):
        raise _fail(DimensionMismatchError, "boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail(DimensionMismatchError, "value is not an exact rational", role=role, received=type(value).__name__)


@dataclass(frozen=True)
class Simplex:
    """An ordered simplex. Vertices are sorted, distinct, and one longer than dim."""

    dim: int
    vertices: tuple[int, ...]

    def __post_init__(self) -> None:
        checked = _require_vertices(self.vertices)
        if self.dim != len(checked) - 1:
            raise _fail(
                DimensionMismatchError,
                "simplex dimension does not match its vertices",
                dim=self.dim,
                length=len(checked),
            )
        object.__setattr__(self, "vertices", checked)

    @classmethod
    def create(cls, vertices: object) -> "Simplex":
        parsed = tuple(_require_vertex(vertex, index) for index, vertex in enumerate(_as_sequence(vertices)))
        ordered = tuple(sorted(parsed))
        return cls(len(ordered) - 1, ordered)

    def faces(self) -> tuple["Simplex", ...]:
        if self.dim == 0:
            return ()
        return tuple(
            Simplex(self.dim - 1, self.vertices[:omit] + self.vertices[omit + 1 :])
            for omit in range(len(self.vertices))
        )


def _require_simplices(simplices: object) -> tuple[Simplex, ...]:
    if isinstance(simplices, (str, bytes)) or not isinstance(simplices, Sequence):
        raise _fail(
            DimensionMismatchError,
            "simplicial complex requires a sequence of simplices",
            received=type(simplices).__name__,
        )
    checked: list[Simplex] = []
    for index, simplex in enumerate(simplices):
        if not isinstance(simplex, Simplex):
            raise _fail(
                DimensionMismatchError,
                "simplicial complex entries must be simplices",
                index=index,
                received=type(simplex).__name__,
            )
        checked.append(simplex)
    return tuple(checked)


@dataclass(frozen=True)
class SimplicialComplex:
    """A finite set of simplices, stored in the order supplied by the caller."""

    simplices: tuple[Simplex, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "simplices", _require_simplices(self.simplices))

    def dimension(self) -> int:
        return max((simplex.dim for simplex in self.simplices), default=0)

    def of_dimension(self, dim: object) -> tuple[Simplex, ...]:
        checked = _require_dim(dim, 0, "simplex dimension is negative")
        return tuple(simplex for simplex in self.simplices if simplex.dim == checked)

    def boundary_matrix(self, dim: object) -> ExactMatrix:
        """Oriented ∂_dim : C_dim → C_{dim-1}. Columns follow of_dimension order."""
        checked = _require_dim(dim, 1, "the 0-boundary is the zero map out of an empty group")
        domain = self.of_dimension(checked)
        codomain = self.of_dimension(checked - 1)
        columns = _boundary_columns(domain, codomain)
        return _matrix_from_columns(columns, len(codomain))


def filled_triangle() -> SimplicialComplex:
    """Vertices, edges, and the single 2-simplex on {0, 1, 2}."""
    vertices = tuple(Simplex.create([index]) for index in range(3))
    edges = tuple(Simplex.create([left, right]) for left, right in ((0, 1), (0, 2), (1, 2)))
    face = (Simplex.create([0, 1, 2]),)
    return SimplicialComplex(vertices + edges + face)


def boundary_square_defect(complex: object, dim: object) -> Fraction:
    """Sum of absolute entries of ∂_{dim-1} ∂_dim."""
    if not isinstance(complex, SimplicialComplex):
        raise _fail(
            DimensionMismatchError,
            "boundary square expects a simplicial complex",
            received=type(complex).__name__,
        )
    checked = _require_dim(dim, 2, "a boundary square needs dimension at least 2")
    product = complex.boundary_matrix(checked - 1) * complex.boundary_matrix(checked)
    defect = Fraction(0)
    for index, entry in enumerate(product.data):
        defect += abs(_rational(entry, f"product[{index}]"))
    return defect


def triangle_boundary_square() -> Fraction:
    """Defect of ∂1 ∂2 on the filled triangle. The square is the zero chain."""
    defect = boundary_square_defect(filled_triangle(), 2)
    if defect != 0:
        raise _fail(NonZeroCompositionError, "filled triangle boundary square is not zero", defect=str(defect))
    return defect


__all__ = [
    "Simplex",
    "SimplicialComplex",
    "boundary_square_defect",
    "filled_triangle",
    "triangle_boundary_square",
]
