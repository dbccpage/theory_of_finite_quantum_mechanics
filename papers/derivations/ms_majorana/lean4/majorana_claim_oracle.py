"""Exact F2 cycle-space certificate and scalar admission for the Majorana Lean modules.

Origin: papers/derivations/ms_majorana/the_majorana_problem.md
Claim: urn:omega:fqm:majorana:maj-c2-f2-trichotomy:v1
AuthorityEffect: None
Scope Fence: Connected-graph cycle dimensions and the integer shadows of MAJ-C2 are recomputed here. No hardware Majorana, continuum Pfaffian, or Gaussian-elimination runtime is certified. gaussian_elimination_cubic_bound remains a counted product, not a measured clock.
Mutation-Kills: 11 non-equivalent source mutants, executed by papers/derivations/ms_majorana/lean4/test_majorana_boundary.py.
Gate 5 measurement: radon 6.0.1 cyclomatic max 6; lizard 1.24.1 cyclomatic max 6; AST cognitive max 7; nesting max 3.
"""

from __future__ import annotations

from pathlib import Path


class BoundaryRefusal(Exception):
    def __init__(self, invariant: str, parameters: dict[str, str]) -> None:
        self.invariant = invariant
        self.parameters = parameters
        super().__init__(invariant)


def _refuse_binary(value: object, role: str) -> None:
    if isinstance(value, float):
        raise BoundaryRefusal(
            "float refused at the public boundary",
            {"role": role, "received": "float"},
        )
    if isinstance(value, bool):
        raise BoundaryRefusal(
            "boolean refused where an exact integer was required",
            {"role": role, "received": "bool"},
        )


def require_nat(value: object, role: str) -> int:
    _refuse_binary(value, role)
    if not isinstance(value, int):
        raise BoundaryRefusal(
            "natural number is not an integer",
            {"role": role, "received": type(value).__name__},
        )
    if value < 0:
        raise BoundaryRefusal(
            "natural number is negative",
            {"role": role, "received": str(value)},
        )
    return value


def require_int(value: object, role: str) -> int:
    _refuse_binary(value, role)
    if not isinstance(value, int):
        raise BoundaryRefusal(
            "value is not an exact integer",
            {"role": role, "received": type(value).__name__},
        )
    return value


def admit_tag(tag: object) -> str:
    _refuse_binary(tag, "tag")
    if not isinstance(tag, str):
        raise BoundaryRefusal(
            "tag is not an exact scalar name",
            {"role": "tag", "received": type(tag).__name__},
        )
    if tag == "float":
        raise BoundaryRefusal(
            "float refused at the public boundary",
            {"role": "tag", "received": "float"},
        )
    if tag == "bool":
        raise BoundaryRefusal(
            "boolean refused where an exact integer was required",
            {"role": "tag", "received": "bool"},
        )
    if tag == "nat" or tag == "int":
        return tag
    raise BoundaryRefusal(
        "tag is not an admitted exact scalar",
        {"role": "tag", "received": tag},
    )


def _bit(value: object) -> int:
    _refuse_binary(value, "bit")
    if not isinstance(value, int):
        raise BoundaryRefusal(
            "bit is not an exact integer",
            {"role": "bit", "received": type(value).__name__},
        )
    if value != 0 and value != 1:
        raise BoundaryRefusal(
            "bit is outside the field F2",
            {"role": "bit", "received": str(value)},
        )
    return value


def _validated_row(row: object) -> tuple[int, ...]:
    if type(row) is not tuple:
        raise BoundaryRefusal(
            "incidence row is not a tuple",
            {"role": "row", "received": type(row).__name__},
        )
    bits: list[int] = []
    for entry in row:
        bits.append(_bit(entry))
    return tuple(bits)


def _validated_matrix(matrix: object) -> tuple[tuple[int, ...], ...]:
    if type(matrix) is not tuple:
        raise BoundaryRefusal(
            "incidence matrix is not a tuple",
            {"role": "matrix", "received": type(matrix).__name__},
        )
    rows: list[tuple[int, ...]] = []
    width: int | None = None
    for entry in matrix:
        row = _validated_row(entry)
        if width is None:
            width = len(row)
        elif len(row) != width:
            raise BoundaryRefusal(
                "incidence rows do not have equal width",
                {"role": "row", "received": str(len(row))},
            )
        rows.append(row)
    return tuple(rows)


def _xor_rows(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    if len(left) != len(right):
        raise BoundaryRefusal(
            "incidence rows do not have equal width",
            {"role": "row", "received": str(len(left))},
        )
    mixed: list[int] = []
    index = 0
    while index < len(left):
        mixed.append((left[index] + right[index]) & 1)
        index += 1
    return tuple(mixed)


def _swap_rows(rows: list[tuple[int, ...]], left: int, right: int) -> None:
    rows[left], rows[right] = rows[right], rows[left]


def _find_pivot(rows: list[tuple[int, ...]], column: int, start: int) -> int | None:
    index = start
    while index < len(rows):
        if rows[index][column] == 1:
            return index
        index += 1
    return None


def _clear_column(rows: list[tuple[int, ...]], pivot: int, column: int) -> None:
    index = 0
    while index < len(rows):
        if index != pivot and rows[index][column] == 1:
            rows[index] = _xor_rows(rows[index], rows[pivot])
        index += 1


def gf2_rank(matrix: object) -> int:
    rows = list(_validated_matrix(matrix))
    if not rows:
        return 0
    width = len(rows[0])
    if width == 0:
        return 0
    pivot_count = 0
    column = 0
    while column < width and pivot_count < len(rows):
        pivot = _find_pivot(rows, column, pivot_count)
        if pivot is not None:
            _swap_rows(rows, pivot_count, pivot)
            _clear_column(rows, pivot_count, column)
            pivot_count += 1
        column += 1
    return pivot_count


def cycle_dimension(matrix: object) -> int:
    rows = _validated_matrix(matrix)
    if not rows:
        return 0
    return len(rows[0]) - gf2_rank(rows)


def cycle_count(vertices: object, edges: object) -> int:
    vertex_count = require_nat(vertices, "vertices")
    edge_count = require_nat(edges, "edges")
    if vertex_count == 0:
        raise BoundaryRefusal(
            "connected graph has no vertices",
            {"role": "vertices", "received": "0"},
        )
    return edge_count - vertex_count + 1


def disk_incidence() -> tuple[tuple[int, ...], ...]:
    return ((),)


def cylinder_incidence() -> tuple[tuple[int, ...], ...]:
    return (
        (1, 0, 1),
        (1, 1, 0),
        (0, 1, 1),
    )


def torus_incidence() -> tuple[tuple[int, ...], ...]:
    return ((0, 0),)


def cylinder_rank() -> int:
    return gf2_rank(cylinder_incidence())


def crosstalk_channels(terminals: object) -> int:
    count = require_nat(terminals, "terminals")
    if count < 4:
        raise BoundaryRefusal(
            "multi-terminal hypothesis requires at least four terminals",
            {"role": "terminals", "received": str(count)},
        )
    return count * (count - 1) // 2


def signed_mass(weight: object, left: object, right: object) -> int:
    scale = require_nat(weight, "weight")
    first = require_int(left, "left")
    second = require_int(right, "right")
    return scale * first + scale * second


def gin_route(valid: object, mass: object) -> str:
    if type(valid) is not bool:
        raise BoundaryRefusal(
            "validity flag is not a boolean",
            {"role": "valid", "received": type(valid).__name__},
        )
    amount = require_nat(mass, "mass")
    if valid is False:
        return "ClosureFailure"
    if amount == 0:
        return "Repair"
    return "SplitBrainRefusal"


def _count_span(steps: int) -> int:
    count = 0
    cursor = 0
    while cursor < steps:
        count += 1
        cursor += 1
    return count


def _count_square(steps: int) -> int:
    count = 0
    cursor = 0
    while cursor < steps:
        count += _count_span(steps)
        cursor += 1
    return count


def counted_cubic(bound: object) -> int:
    steps = require_nat(bound, "bound")
    count = 0
    cursor = 0
    while cursor < steps:
        count += _count_square(steps)
        cursor += 1
    return count


def polynomial_cubic(bound: object) -> int:
    steps = require_nat(bound, "bound")
    return steps * steps * steps


def _leading_natural(text: str, name: str) -> int:
    digits: list[str] = []
    index = 0
    while index < len(text):
        char = text[index]
        if not char.isdigit():
            break
        digits.append(char)
        index += 1
    if not digits:
        raise BoundaryRefusal(
            "surface arm is not an exact natural",
            {"role": "surface", "received": name},
        )
    return int("".join(digits))


def surface_betti(source: object, name: object) -> int:
    if not isinstance(source, str):
        raise BoundaryRefusal(
            "lean source is not text",
            {"role": "source", "received": type(source).__name__},
        )
    if not isinstance(name, str):
        raise BoundaryRefusal(
            "surface name is not text",
            {"role": "surface", "received": type(name).__name__},
        )
    needle = "SurfaceTopology." + name + " => "
    start = source.find(needle)
    if start < 0:
        raise BoundaryRefusal(
            "surface arm is missing",
            {"role": "surface", "received": name},
        )
    return _leading_natural(source[start + len(needle) :], name)


def _core_source() -> str:
    path = Path(__file__).resolve().parent / "MajoranaCore.lean"
    return path.read_text(encoding="utf-8")


def _route_code(valid: object, mass: object) -> int:
    route = gin_route(valid, mass)
    if route == "Repair":
        return 0
    if route == "SplitBrainRefusal":
        return 1
    if route == "ClosureFailure":
        return 2
    raise BoundaryRefusal("route is not a terminal code", {"role": "route", "received": route})


def claim_snapshot() -> tuple[int, ...]:
    lean = _core_source()
    return (
        cycle_dimension(disk_incidence()),
        cycle_dimension(cylinder_incidence()),
        cycle_dimension(torus_incidence()),
        cycle_count(1, 0),
        cycle_count(3, 3),
        cycle_count(1, 2),
        crosstalk_channels(4),
        counted_cubic(2),
        polynomial_cubic(2),
        signed_mass(2, 1, -1),
        signed_mass(2, 1, 1),
        _route_code(True, 0),
        _route_code(True, 2),
        _route_code(False, 4),
        cylinder_rank(),
        surface_betti(lean, "Disk"),
        surface_betti(lean, "Cylinder"),
        surface_betti(lean, "Torus"),
        gf2_rank(((1, 1), (1, 0))),
    )
