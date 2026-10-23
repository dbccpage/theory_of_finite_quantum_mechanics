"""Primitive same/different calculus and its finite parity consequences."""

from __future__ import annotations

from enum import IntEnum
from typing import Hashable, Iterable


class Difference(IntEnum):
    SAME = 0
    DIFFERENT = 1


def primitive_difference(left: Hashable, right: Hashable) -> Difference:
    return Difference.SAME if left == right else Difference.DIFFERENT


def parity(bits: Iterable[int | Difference]) -> Difference:
    value = 0
    for bit in bits:
        if type(bit) not in (int, Difference) or bit not in (0, 1):
            raise ValueError("parity accepts only zero/one distinctions")
        value ^= int(bit)
    return Difference(value)


def triangle_boundary(a: Hashable, b: Hashable, c: Hashable) -> tuple[Difference, Difference, Difference]:
    return primitive_difference(a, b), primitive_difference(b, c), primitive_difference(a, c)


def triangle_identity(a: Hashable, b: Hashable, c: Hashable) -> bool:
    """The boundary identity d(a,b) xor d(b,c) xor d(a,c)=0 for binary-labelled carriers."""

    if len({a, b, c}) > 2:
        raise ValueError("triangle_identity requires a binary-labelled carrier (at most two distinct marks)")
    return parity(triangle_boundary(a, b, c)) is Difference.SAME


def odd_cycle_frustrated(edge_bits: Iterable[int | Difference]) -> bool:
    return parity(edge_bits) is Difference.DIFFERENT
# Executable finite evidence; AuthorityEffect: None.
