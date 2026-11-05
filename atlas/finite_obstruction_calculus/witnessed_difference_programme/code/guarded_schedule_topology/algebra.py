"""Integral boundary matrices and replayable unimodular unit reductions.

The proposer searches for unit entries. The checker only replays the supplied
pivots against the original matrix. A zero residual certifies that every
nonzero Smith invariant is one; a nonzero residual is explicitly unclassified.
No floating rank, homotopy inference, or torsion guess is made.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from .model import Levels, TopologyRefusal, boundary, dimension

SparseColumn = dict[int, int]


@dataclass(frozen=True)
class Matrix:
    rows: int
    columns: tuple[tuple[tuple[int, int], ...], ...]

    def __post_init__(self) -> None:
        if type(self.rows) is not int or self.rows < 0 or type(self.columns) is not tuple:
            raise TopologyRefusal("invalid integral matrix shape")
        for column in self.columns:
            if type(column) is not tuple:
                raise TopologyRefusal("matrix columns must be immutable tuples")
            indices = []
            for entry in column:
                if type(entry) is not tuple or len(entry) != 2:
                    raise TopologyRefusal("invalid matrix incidence")
                row, value = entry
                if (type(row) is not int or not 0 <= row < self.rows
                        or type(value) is not int or value == 0):
                    raise TopologyRefusal("invalid nonzero integral matrix entry")
                indices.append(row)
            if indices != sorted(set(indices)):
                raise TopologyRefusal("matrix row indices must be sorted and distinct")


def matrices(levels: Levels) -> tuple[Matrix, ...]:
    """d_0 is the zero map to 0; d_k occupies index k."""
    out: list[Matrix] = []
    for k, cells in enumerate(levels):
        if len(set(cells)) != len(cells) or any(dimension(cell) != k for cell in cells):
            raise TopologyRefusal("cell levels contain duplicates or wrong dimensions")
        index = {cell: i for i, cell in enumerate(levels[k - 1])} if k else {}
        columns = []
        for cell in cells:
            incidences = boundary(cell)
            if any(face not in index for face in incidences):
                raise TopologyRefusal("cell family is not closed under its full boundary")
            columns.append(tuple(sorted((index[face], sign) for face, sign in incidences.items())))
        out.append(Matrix(len(index), tuple(columns)))
    return tuple(out)


def verify_chain(chain: tuple[Matrix, ...]) -> None:
    for k, matrix in enumerate(chain):
        if k == 0:
            if matrix.rows != 0 or any(matrix.columns):
                raise TopologyRefusal("d_0 must vanish")
            continue
        previous = chain[k - 1]
        if matrix.rows != len(previous.columns):
            raise TopologyRefusal("consecutive boundary dimensions disagree")
        for column in matrix.columns:
            composite: dict[int, int] = {}
            for middle, value in column:
                for row, lower in previous.columns[middle]:
                    composite[row] = composite.get(row, 0) + value * lower
            if any(composite.values()):
                raise TopologyRefusal("boundary squared is nonzero")


def _tables(matrix: Matrix) -> tuple[dict[int, SparseColumn], dict[int, SparseColumn]]:
    columns = {j: dict(column) for j, column in enumerate(matrix.columns) if column}
    rows: dict[int, SparseColumn] = {}
    for column, values in columns.items():
        for row, value in values.items():
            rows.setdefault(row, {})[column] = value
    return columns, rows


def _cancel(columns: dict[int, SparseColumn], rows: dict[int, SparseColumn],
            row: int, column: int) -> int:
    """Elementary integral column operations isolate a unit, then delete it.

    The remaining pivot column can be cleared by integral row operations
    without altering the residual, because its pivot row is already zero
    elsewhere. Thus the removed summand has Smith invariant exactly one.
    """
    pivot = columns.get(column, {}).get(row)
    if pivot not in (-1, 1):
        raise TopologyRefusal("submitted pivot is absent or is not an integral unit")
    pivot_column = tuple(columns[column].items())
    affected = tuple(rows[row].items())
    for other, coefficient in affected:
        if other == column:
            continue
        factor = coefficient * pivot
        vector = columns[other]
        for target, value in pivot_column:
            updated = vector.get(target, 0) - factor * value
            if updated:
                vector[target] = updated
                rows.setdefault(target, {})[other] = updated
            else:
                vector.pop(target, None)
                rows[target].pop(other, None)
                if not rows[target]:
                    del rows[target]
        if not vector:
            del columns[other]
    for target, _ in pivot_column:
        rows[target].pop(column)
        if not rows[target]:
            del rows[target]
    del columns[column]
    return pivot


def _residual(columns: dict[int, SparseColumn]) -> list:
    return [[column, [[row, value] for row, value in sorted(values.items())]]
            for column, values in sorted(columns.items())]


def reduce_integer_boundary(matrix: Matrix) -> dict:
    """Propose unit pivots, preferring sparse columns to reduce fill-in."""
    columns, rows = _tables(matrix)
    pivots = []
    while columns:
        selected = None
        # Avoid a dense rank computation and keep all choices deterministic.
        for column in sorted(columns, key=lambda j: (len(columns[j]), j)):
            units = [row for row, value in columns[column].items() if abs(value) == 1]
            if units:
                row = min(units, key=lambda i: (len(rows[i]), i))
                selected = row, column
                break
        if selected is None:
            break
        row, column = selected
        pivots.append([row, column, _cancel(columns, rows, row, column)])
    return {"pivots": pivots, "residual": _residual(columns)}


def replay_reduction(matrix: Matrix, certificate: object) -> dict:
    """Check proposed operations without invoking the pivot search."""
    if type(certificate) is not dict or set(certificate) != {"pivots", "residual"}:
        raise TopologyRefusal("invalid matrix-reduction certificate fields")
    pivots = certificate["pivots"]
    if type(pivots) is not list or len(pivots) > min(matrix.rows, len(matrix.columns)):
        raise TopologyRefusal("invalid or excessive pivot sequence")
    columns, rows = _tables(matrix)
    for pivot in pivots:
        if (type(pivot) is not list or len(pivot) != 3
                or any(type(value) is not int for value in pivot)):
            raise TopologyRefusal("a pivot must contain three exact integers")
        row, column, claimed = pivot
        actual = _cancel(columns, rows, row, column)
        if claimed != actual:
            raise TopologyRefusal("submitted unit-pivot sign is incorrect")
    residual = _residual(columns)
    # Equality alone would admit bool as int; canonical encoding is checked by
    # the public certificate parser before any retained artifact is trusted.
    if json.dumps(certificate["residual"], sort_keys=True) != json.dumps(residual, sort_keys=True):
        raise TopologyRefusal("submitted residual differs from replay")
    return {"unit_rank": len(pivots), "residual_zero": not residual,
            "smith_invariants": "all_nonzero_are_one" if not residual else "unclassified"}


def certify_homology(chain: tuple[Matrix, ...]) -> tuple[dict, dict]:
    """Propose and separately replay the reductions; report only proved ranks."""
    verify_chain(chain)
    certificate = {"reductions": [reduce_integer_boundary(matrix) for matrix in chain]}
    result = check_homology(chain, certificate)
    return certificate, result


def check_homology(chain: tuple[Matrix, ...], certificate: object) -> dict:
    verify_chain(chain)
    if (type(certificate) is not dict or set(certificate) != {"reductions"}
            or type(certificate["reductions"]) is not list
            or len(certificate["reductions"]) != len(chain)):
        raise TopologyRefusal("homology certificate must contain every boundary reduction")
    reductions = [replay_reduction(matrix, proof)
                  for matrix, proof in zip(chain, certificate["reductions"])]
    complete = all(row["residual_zero"] for row in reductions)
    ranks = [row["unit_rank"] for row in reductions]
    betti = [len(matrix.columns) - ranks[k] - (ranks[k + 1] if k + 1 < len(ranks) else 0)
             for k, matrix in enumerate(chain)] if complete else None
    if betti is not None and any(value < 0 for value in betti):
        raise TopologyRefusal("certified boundary ranks contradict the chain dimensions")
    return {"status": "CERTIFIED" if complete else "UNCLASSIFIED_NONUNIT_RESIDUAL",
            "f_vector": [len(matrix.columns) for matrix in chain],
            "boundary_ranks": ranks if complete else None,
            "integral_betti": betti, "torsion_free": True if complete else None,
            "boundary_squared_zero": True, "reductions": reductions}


def check_top_cycle_pairing(chain: tuple[Matrix, ...], certificate: object) -> dict:
    """Check a top cycle and a closed cochain with nonzero integral pairing.

    The declared chain has no group above this positive top degree. A
    nonzero pairing with a cycle also precludes the cochain from being a
    coboundary, because every coboundary pairs to zero with every cycle.
    """
    verify_chain(chain)
    if (type(certificate) is not dict
            or set(certificate) != {"degree", "cycle", "cochain", "pairing"}):
        raise TopologyRefusal("invalid cycle/cocycle certificate fields")
    degree = certificate["degree"]
    if type(degree) is not int or degree < 1 or degree != len(chain) - 1:
        raise TopologyRefusal("certificate must address the positive top degree")
    size = len(chain[degree].columns)

    def vector(value: object) -> dict[int, int]:
        if type(value) is not list:
            raise TopologyRefusal("cycle/cochain must be a sparse integer array")
        result = {}
        for pair in value:
            if (type(pair) is not list or len(pair) != 2
                    or any(type(x) is not int for x in pair)
                    or not 0 <= pair[0] < size or pair[1] == 0 or pair[0] in result):
                raise TopologyRefusal("invalid cycle/cochain coordinate")
            result[pair[0]] = pair[1]
        if list(result) != sorted(result):
            raise TopologyRefusal("cycle/cochain coordinates are not sorted")
        return result

    cycle, cochain = vector(certificate["cycle"]), vector(certificate["cochain"])
    lower = {}
    for column, value in cycle.items():
        for row, incidence in chain[degree].columns[column]:
            lower[row] = lower.get(row, 0) + value * incidence
    if any(lower.values()):
        raise TopologyRefusal("submitted cycle has a nonzero boundary")
    pairing = sum(value * cochain.get(column, 0) for column, value in cycle.items())
    if (type(certificate["pairing"]) is not int or not pairing
            or certificate["pairing"] != pairing):
        raise TopologyRefusal("cycle/cocycle pairing is zero or incorrectly reported")
    return {"degree": degree, "cycle_closed": True, "cochain_closed": True,
            "cochain_not_exact": True, "cycle_not_boundary": True,
            "pairing": pairing, "higher_chain_group_zero": True}
