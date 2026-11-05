"""Exact finite partial-structure descent; archival identity is outside this theorem."""

from dataclasses import dataclass
from itertools import product
from math import prod


@dataclass(frozen=True)
class Operation:
    inputs: tuple[int, ...]
    output: int
    values: tuple[int | None, ...]


@dataclass(frozen=True)
class Predicate:
    inputs: tuple[int, ...]
    values: tuple[bool, ...]


@dataclass(frozen=True)
class Structure:
    sizes: tuple[int, ...]
    operations: tuple[Operation, ...] = ()
    predicates: tuple[Predicate, ...] = ()


class DescentError(ValueError):
    """Typed conflict with the two concrete source rows proving impossibility."""

    def __init__(self, kind, field=None, left=None, right=None):
        super().__init__(kind, field, left, right)
        self.kind, self.field, self.left, self.right = kind, field, left, right


def descend(source: Structure, target_sizes, maps) -> Structure:
    target_sizes, maps = tuple(target_sizes), tuple(tuple(m) for m in maps)
    if any(type(n) is not int or n < 0 for n in source.sizes + target_sizes):
        raise DescentError("invalid sizes")
    if len(maps) != len(source.sizes) or len(target_sizes) != len(source.sizes):
        raise DescentError("invalid sort map")
    for n, m, q in zip(source.sizes, target_sizes, maps):
        if len(q) != n or any(type(x) is not int for x in q) or set(q) != set(range(m)):
            raise DescentError("invalid sort map")

    def table(inputs, values, output, field):
        if any(type(s) is not int or not 0 <= s < len(source.sizes) for s in inputs):
            raise DescentError("invalid signature")
        if output is not None and (type(output) is not int or not 0 <= output < len(source.sizes)):
            raise DescentError("invalid signature")
        if len(values) != prod(source.sizes[s] for s in inputs):
            raise DescentError("invalid table")
        rows = {}
        for row, (coordinates, value) in enumerate(
            zip(product(*(range(source.sizes[s]) for s in inputs)), values)
        ):
            if output is None:
                if type(value) is not bool:
                    raise DescentError("invalid predicate")
                image = value
            elif value is None:
                image = None
            else:
                if type(value) is not int or not 0 <= value < source.sizes[output]:
                    raise DescentError("invalid operation")
                image = maps[output][value]
            key = tuple(maps[s][x] for s, x in zip(inputs, coordinates))
            if key in rows and rows[key][1] != image:
                raise DescentError(
                    "predicate conflict" if output is None else "operation conflict",
                    field,
                    rows[key][0],
                    row,
                )
            rows.setdefault(key, (row, image))
        return tuple(rows[key][1] for key in product(*(range(target_sizes[s]) for s in inputs)))

    for i, op in enumerate(source.operations):
        if type(op.output) is not int or not 0 <= op.output < len(source.sizes):
            raise DescentError("invalid operation output sort")

    operations = tuple(
        Operation(op.inputs, op.output, table(op.inputs, op.values, op.output, i))
        for i, op in enumerate(source.operations)
    )
    predicates = tuple(
        Predicate(p.inputs, table(p.inputs, p.values, None, i))
        for i, p in enumerate(source.predicates)
    )
    return Structure(target_sizes, operations, predicates)


def verify(source, target_sizes, maps, target):
    if descend(source, target_sizes, maps) != target:
        raise DescentError("receipt mismatch")
