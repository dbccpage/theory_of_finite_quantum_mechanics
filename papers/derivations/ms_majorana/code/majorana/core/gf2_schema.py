from __future__ import annotations

from typing import Literal

GF2Bit = Literal[0, 1]
TerminalStatus = Literal[
    "Exact",
    "ClosedResidual",
    "OpenObstruction",
    "RepresentationInvalid",
]


def mod2(value: int) -> int:
    """Reduce an exact signed integer; reject boolean and numeric aliases."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("GF(2) entries must be integers, not bool or approximate numbers")
    return value & 1


def normalize_vector(vector: list[int]) -> list[int]:
    return [mod2(x) for x in vector]


def normalize_matrix(matrix: list[list[int]]) -> list[list[int]]:
    return [[mod2(x) for x in row] for row in matrix]
