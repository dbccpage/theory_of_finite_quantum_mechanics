"""Finite-width bit-vector operators."""

from __future__ import annotations


class BitwiseOperations:
    """Pure bitwise operations over a declared finite width."""

    def __init__(self, bit_width: int = 64) -> None:
        if bit_width <= 0:
            raise ValueError("bit_width must be positive")
        self.bit_width = bit_width
        self._mask = (1 << bit_width) - 1

    def bitwise_and(self, left: int, right: int) -> int:
        return left & right & self._mask

    def bitwise_or(self, left: int, right: int) -> int:
        return (left | right) & self._mask

    def parity(self, value: int) -> int:
        return (value & self._mask).bit_count() & 1


__all__ = ["BitwiseOperations"]
