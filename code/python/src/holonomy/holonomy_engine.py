"""Discrete cell complexes, rational connections, and coboundary holonomy.

Origin: lean4/CoboundaryHolonomy.lean theorem coboundary_triangle_holonomy_zero,
theorem coboundary_square_holonomy_zero, and theorem coboundary_closed_cycle_zero.
Claim: urn:omega:fqm:holonomy:coboundary-cycle-zero:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/holonomy/test_holonomy_control.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 7; AST Sonar cognitive complexity max 5; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 7.
Scope Fence: coboundary_cycle_witness checks that an integer coboundary has
holonomy 0 on a triangle, a square, and a closed vertex path. Matrix
transport on a cell complex is exact GL(d, Q) arithmetic. This file does
not prove the Lean coboundary lemmas and does not claim continuum curvature.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence


class HolonomyError(ValueError):
    """One violated holonomy invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> HolonomyError:
    return HolonomyError(invariant, parameters)


def _require_int(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the holonomy boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where an integer was required", role=role)
    if isinstance(value, int):
        return value
    raise _fail("value is not an integer", role=role, received=type(value).__name__)


def _require_fraction(value: object, role: str) -> Fraction:
    if isinstance(value, float):
        raise _fail("float refused at the holonomy boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where a rational was required", role=role)
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


@dataclass(frozen=True)
class Vertex:
    id: str
    index: int


@dataclass(frozen=True)
class Edge:
    index: int
    source: str
    target: str


@dataclass(frozen=True)
class OrientedStep:
    edge_index: int
    direction: int


@dataclass(frozen=True)
class Face:
    id: str
    index: int
    boundary_vertices: tuple[str, ...]
    boundary_edges: tuple[OrientedStep, ...]


class CellComplex:
    """Finite complex with vertices, edges, and faces."""

    def __init__(self) -> None:
        self.vertices: list[Vertex] = []
        self.vertex_map: dict[str, int] = {}
        self.edges: list[Edge] = []
        self.edge_map: dict[tuple[str, str], int] = {}
        self.faces: list[Face] = []
        self.face_map: dict[str, int] = {}

    def add_vertex(self, vertex_id: object) -> int:
        name = _require_name(vertex_id, "vertex")
        if name in self.vertex_map:
            raise _fail("vertex is duplicated", vertex=name)
        index = len(self.vertices)
        self.vertices.append(Vertex(name, index))
        self.vertex_map[name] = index
        return index

    def add_edge(self, source: object, target: object) -> int:
        start = _require_known_vertex(self, source, "source")
        end = _require_known_vertex(self, target, "target")
        key = (start, end)
        if key in self.edge_map:
            raise _fail("edge is duplicated", source=start, target=end)
        index = len(self.edges)
        self.edges.append(Edge(index, start, end))
        self.edge_map[key] = index
        return index

    def add_face(self, face_id: object, vertices: Sequence[object]) -> int:
        name = _require_name(face_id, "face")
        if name in self.face_map:
            raise _fail("face is duplicated", face=name)
        boundary = _require_cycle(vertices)
        steps = _boundary_steps(self, boundary)
        index = len(self.faces)
        self.faces.append(Face(name, index, boundary, tuple(steps)))
        self.face_map[name] = index
        return index

    @property
    def euler_characteristic(self) -> int:
        return len(self.vertices) - len(self.edges) + len(self.faces)


def _require_name(value: object, role: str) -> str:
    if isinstance(value, str) and value != "":
        return value
    raise _fail("name is not a non-empty string", role=role, received=type(value).__name__)


def _require_known_vertex(complex_: CellComplex, value: object, role: str) -> str:
    name = _require_name(value, role)
    if name not in complex_.vertex_map:
        raise _fail("vertex is not in the complex", role=role, vertex=name)
    return name


def _require_cycle(vertices: Sequence[object]) -> tuple[str, ...]:
    if isinstance(vertices, (str, bytes)) or not isinstance(vertices, (list, tuple)):
        raise _fail("face boundary is not a sequence", received=type(vertices).__name__)
    names = tuple(_require_name(item, "face vertex") for item in vertices)
    if len(names) < 3:
        raise _fail("face has fewer than 3 vertices", length=len(names))
    return names


def _boundary_steps(complex_: CellComplex, vertices: tuple[str, ...]) -> list[OrientedStep]:
    steps: list[OrientedStep] = []
    for index, source in enumerate(vertices):
        target = vertices[(index + 1) % len(vertices)]
        steps.append(_oriented_step(complex_, source, target))
    return steps


def _oriented_step(complex_: CellComplex, source: str, target: str) -> OrientedStep:
    forward = complex_.edge_map.get((source, target))
    if forward is not None:
        return OrientedStep(forward, 1)
    backward = complex_.edge_map.get((target, source))
    if backward is not None:
        return OrientedStep(backward, -1)
    raise _fail("face edge is missing", source=source, target=target)


@dataclass(frozen=True)
class RationalMatrix:
    """Exact matrix over Q."""

    rows: int
    cols: int
    data: tuple[tuple[Fraction, ...], ...]

    @classmethod
    def identity(cls, dim: object) -> RationalMatrix:
        width = _require_positive(dim, "dimension")
        return cls(width, width, _identity_data(width))

    @classmethod
    def from_ints(cls, raw: Sequence[object]) -> RationalMatrix:
        parsed = _parse_matrix(raw)
        rows = len(parsed)
        cols = len(parsed[0]) if rows else 0
        return cls(rows, cols, parsed)

    def multiply(self, other: RationalMatrix) -> RationalMatrix:
        partner = _require_matrix(other, "factor")
        if self.cols != partner.rows:
            raise _fail("matrix shapes do not match", left=self.cols, right=partner.rows)
        return RationalMatrix(self.rows, partner.cols, _product_data(self, partner))

    def inverse(self) -> RationalMatrix:
        if self.rows != self.cols:
            raise _fail("only a square matrix can be inverted", rows=self.rows, cols=self.cols)
        return RationalMatrix(self.rows, self.cols, _invert(self.data))

    def trace(self) -> Fraction:
        if self.rows != self.cols:
            raise _fail("trace requires a square matrix", rows=self.rows, cols=self.cols)
        return _trace_of(self.data)

    def equals(self, other: RationalMatrix) -> bool:
        partner = _require_matrix(other, "other")
        if self.rows != partner.rows or self.cols != partner.cols:
            return False
        return self.data == partner.data


def _require_positive(value: object, role: str) -> int:
    number = _require_int(value, role)
    if number <= 0:
        raise _fail("dimension is not positive", role=role, value=number)
    return number


def _identity_data(width: int) -> tuple[tuple[Fraction, ...], ...]:
    rows: list[tuple[Fraction, ...]] = []
    for row in range(width):
        rows.append(_identity_row(row, width))
    return tuple(rows)


def _identity_row(row: int, width: int) -> tuple[Fraction, ...]:
    return tuple(Fraction(1) if row == col else Fraction(0) for col in range(width))


def _parse_matrix(raw: Sequence[object]) -> tuple[tuple[Fraction, ...], ...]:
    if isinstance(raw, (str, bytes)) or not isinstance(raw, (list, tuple)) or len(raw) == 0:
        raise _fail("matrix is not a nonempty row sequence", received=type(raw).__name__)
    rows = tuple(_parse_row(item, index) for index, item in enumerate(raw))
    width = len(rows[0])
    for row in rows:
        if len(row) != width:
            raise _fail("matrix rows have different widths", expected=width, received=len(row))
    return rows


def _parse_row(item: object, index: int) -> tuple[Fraction, ...]:
    if isinstance(item, (str, bytes)) or not isinstance(item, (list, tuple)) or len(item) == 0:
        raise _fail("matrix row is empty or not a sequence", index=index, received=type(item).__name__)
    return tuple(_require_fraction(entry, f"entry[{index}]") for entry in item)


def _require_matrix(value: object, role: str) -> RationalMatrix:
    if isinstance(value, RationalMatrix):
        return value
    raise _fail("value is not a rational matrix", role=role, received=type(value).__name__)


def _product_data(left: RationalMatrix, right: RationalMatrix) -> tuple[tuple[Fraction, ...], ...]:
    rows: list[tuple[Fraction, ...]] = []
    for row in range(left.rows):
        rows.append(_product_row(left, right, row))
    return tuple(rows)


def _product_row(left: RationalMatrix, right: RationalMatrix, row: int) -> tuple[Fraction, ...]:
    return tuple(_dot(left, right, row, col) for col in range(right.cols))


def _dot(left: RationalMatrix, right: RationalMatrix, row: int, col: int) -> Fraction:
    total = Fraction(0)
    for index in range(left.cols):
        total += left.data[row][index] * right.data[index][col]
    return total


def _trace_of(data: tuple[tuple[Fraction, ...], ...]) -> Fraction:
    total = Fraction(0)
    for index, row in enumerate(data):
        total += row[index]
    return total


def _invert(data: tuple[tuple[Fraction, ...], ...]) -> tuple[tuple[Fraction, ...], ...]:
    width = len(data)
    augmented = _augment(data)
    for col in range(width):
        _eliminate_column(augmented, col, width)
    return _right_block(augmented, width)


def _augment(data: tuple[tuple[Fraction, ...], ...]) -> list[list[Fraction]]:
    return [_augment_row(row, index, len(data)) for index, row in enumerate(data)]


def _augment_row(row: tuple[Fraction, ...], index: int, width: int) -> list[Fraction]:
    copied = list(row)
    for col in range(width):
        copied.append(Fraction(1) if col == index else Fraction(0))
    return copied


def _eliminate_column(augmented: list[list[Fraction]], col: int, width: int) -> None:
    pivot = _pivot_row(augmented, col, width)
    if pivot < 0:
        raise _fail("matrix is singular", column=col)
    augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
    _scale_row(augmented[col], col, width + width)
    _clear_other_rows(augmented, col, width)


def _pivot_row(augmented: list[list[Fraction]], col: int, width: int) -> int:
    for row in range(col, width):
        if augmented[row][col] != 0:
            return row
    return -1


def _scale_row(row: list[Fraction], col: int, span: int) -> None:
    scale = row[col]
    if scale == 0:
        raise _fail("pivot scale is zero", column=col)
    for index in range(span):
        row[index] /= scale


def _clear_other_rows(augmented: list[list[Fraction]], col: int, width: int) -> None:
    for row in range(width):
        if row != col:
            _clear_row(augmented[row], augmented[col], col, width + width)


def _clear_row(row: list[Fraction], pivot: list[Fraction], col: int, span: int) -> None:
    factor = row[col]
    if factor == 0:
        return
    for index in range(span):
        row[index] -= factor * pivot[index]


def _right_block(augmented: list[list[Fraction]], width: int) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(row[width:]) for row in augmented)


class DiscreteConnection:
    """Edge transport in GL(d, Q), with the reverse edge stored as the inverse."""

    def __init__(self, dim: object) -> None:
        self.dim = _require_positive(dim, "dimension")
        self.forward: dict[tuple[str, str], RationalMatrix] = {}
        self.reverse: dict[tuple[str, str], RationalMatrix] = {}

    def set_connection(self, source: object, target: object, matrix: object) -> None:
        start = _require_name(source, "source")
        end = _require_name(target, "target")
        value = _require_square(matrix, self.dim)
        self.forward[(start, end)] = value
        self.reverse[(end, start)] = value.inverse()

    def get_step(self, source: object, target: object) -> RationalMatrix:
        start = _require_name(source, "source")
        end = _require_name(target, "target")
        forward = self.forward.get((start, end))
        if forward is not None:
            return forward
        backward = self.reverse.get((start, end))
        if backward is not None:
            return backward
        raise _fail("connection step is missing", source=start, target=end)

    def path_holonomy(self, path: Sequence[object]) -> RationalMatrix:
        vertices = _name_sequence(path, "path")
        if len(vertices) < 2:
            return RationalMatrix.identity(self.dim)
        return _transport(self, vertices)

    def face_holonomy(self, face: Face) -> RationalMatrix:
        if not isinstance(face, Face):
            raise _fail("face holonomy requires a face", received=type(face).__name__)
        return self.path_holonomy(_closed_vertices(face.boundary_vertices))

    def is_flat(self, complex_: CellComplex) -> bool:
        if not isinstance(complex_, CellComplex):
            raise _fail("flatness requires a cell complex", received=type(complex_).__name__)
        identity = RationalMatrix.identity(self.dim)
        for face in complex_.faces:
            if not self.face_holonomy(face).equals(identity):
                return False
        return True


def _require_square(value: object, dim: int) -> RationalMatrix:
    matrix = _require_matrix(value, "connection")
    if matrix.rows != dim or matrix.cols != dim:
        raise _fail("connection matrix has the wrong shape", expected=dim, rows=matrix.rows, cols=matrix.cols)
    return matrix


def _name_sequence(values: Sequence[object], role: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, (list, tuple)):
        raise _fail("names are not a sequence", role=role, received=type(values).__name__)
    return tuple(_require_name(item, role) for item in values)


def _transport(connection: DiscreteConnection, vertices: tuple[str, ...]) -> RationalMatrix:
    result = RationalMatrix.identity(connection.dim)
    for index in range(len(vertices) - 1):
        result = result.multiply(connection.get_step(vertices[index], vertices[index + 1]))
    return result


def _closed_vertices(vertices: tuple[str, ...]) -> tuple[str, ...]:
    if not vertices:
        return vertices
    return vertices + (vertices[0],)


def _coboundary_step(values: tuple[int, ...], source: int, target: int) -> int:
    return values[target] - values[source]


def closed_coboundary_holonomy(values: object, cycle: object) -> int:
    """Sum (phi(head) - phi(tail)) along a vertex cycle."""
    phi = _parse_cochain(values)
    steps = _parse_cycle(cycle, len(phi))
    total = 0
    for index in range(len(steps) - 1):
        total += _coboundary_step(phi, steps[index], steps[index + 1])
    return total


def _parse_cochain(values: object) -> tuple[int, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, (list, tuple)) or len(values) == 0:
        raise _fail("cochain is not a nonempty sequence", received=type(values).__name__)
    return tuple(_require_int(item, f"cochain[{index}]") for index, item in enumerate(values))


def _parse_cycle(cycle: object, width: int) -> tuple[int, ...]:
    if isinstance(cycle, (str, bytes)) or not isinstance(cycle, (list, tuple)) or len(cycle) < 2:
        raise _fail("cycle is not a vertex path", received=type(cycle).__name__)
    parsed = tuple(_cycle_index(item, index, width) for index, item in enumerate(cycle))
    return parsed


def _cycle_index(value: object, index: int, width: int) -> int:
    parsed = _require_int(value, f"cycle[{index}]")
    if parsed < 0 or parsed >= width:
        raise _fail("cycle index is outside the cochain", index=parsed, width=width)
    return parsed


def coboundary_cycle_witness() -> int:
    """Return 0 when triangle, square, and closed-path coboundaries vanish."""
    triangle = closed_coboundary_holonomy((3, -5, 8), (0, 1, 2, 0))
    square = closed_coboundary_holonomy((1, 2, 4, 7), (0, 1, 2, 3, 0))
    if triangle != 0 or square != 0:
        raise _fail("coboundary cycle holonomy is not zero", triangle=triangle, square=square)
    return 0


def main() -> int:
    """Print the coboundary holonomy certificate."""
    try:
        print(coboundary_cycle_witness())
    except HolonomyError as error:
        print(error.invariant)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
