"""Exact witness for the finite carrier in derivation.md.

Sites are (Z/4Z)^2. Configurations are the two orientations of each
4-cycle on the periodic nearest-neighbour grid: 16 faces and 8 generator
cycles. The selected hypotheses are A=1, s=+1, and m=(W_x+W_y) mod 2.
The returned partition is not the 1D trace 912.
"""

from __future__ import annotations

from fractions import Fraction


def _edge(a: tuple[int, int], b: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    return (a, b) if a <= b else (b, a)


def faces() -> list[frozenset]:
    found = []
    for x in range(4):
        for y in range(4):
            found.append(
                frozenset(
                    (
                        _edge((x, y), ((x + 1) % 4, y)),
                        _edge(((x + 1) % 4, y), ((x + 1) % 4, (y + 1) % 4)),
                        _edge(((x + 1) % 4, (y + 1) % 4), (x, (y + 1) % 4)),
                        _edge((x, (y + 1) % 4), (x, y)),
                    )
                )
            )
    return found


def rows() -> list[frozenset]:
    return [
        frozenset(_edge((x, y), ((x + 1) % 4, y)) for x in range(4))
        for y in range(4)
    ]


def cols() -> list[frozenset]:
    return [
        frozenset(_edge((x, y), (x, (y + 1) % 4)) for y in range(4))
        for x in range(4)
    ]


def _orbit_sums(meron_bit: int) -> tuple[int, int]:
    partition = 0
    numerator = 0
    for orientation in (0, 1):
        weight = 1 if (meron_bit * orientation) % 2 == 0 else -1
        observable = 1 if orientation == 0 else -1
        partition += weight
        numerator += weight * observable
    return partition, numerator


def witness() -> dict[str, int | Fraction]:
    found_faces = faces()
    found_rows = rows()
    found_cols = cols()
    cycles = found_faces + found_rows + found_cols
    if len(set(cycles)) != len(cycles):
        raise RuntimeError("4-cycle edge sets are not distinct")
    if any(len(cycle) != 4 for cycle in cycles):
        raise RuntimeError("a listed cycle does not have four edges")
    face_partition, face_numerator = _orbit_sums(0)
    generator_partition, generator_numerator = _orbit_sums(1)
    z = len(found_faces) * face_partition + (len(found_rows) + len(found_cols)) * generator_partition
    n = len(found_faces) * face_numerator + (len(found_rows) + len(found_cols)) * generator_numerator
    orientations = 2 * len(cycles)
    return {
        "sites": 16,
        "cycles": len(cycles),
        "faces": len(found_faces),
        "generators": len(found_rows) + len(found_cols),
        "orientations": orientations,
        "Z": z,
        "N": n,
        "average_sign": Fraction(z, orientations),
        "expectation": Fraction(n, z),
    }


def reject_pinned_scalar(value: int) -> None:
    if value == 912:
        raise ValueError("the 1D trace 912 is not the partition of this carrier")
