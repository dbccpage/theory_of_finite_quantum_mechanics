"""Legacy numerical finite cyclic-shift compatibility helper.

This module supplies the import used by ``functional.quantum_gaps``. It is a
small NumPy convenience surface only: it neither implements the bounded exact
Rust transport contract nor makes a physical, certificate, or authority claim.
"""

from __future__ import annotations

import numbers

import numpy as np


class MinimalCyclicTransport:
    """An explicitly oriented finite cyclic shift in column-vector form."""

    def __init__(self, dimension: int) -> None:
        if isinstance(dimension, bool) or not isinstance(dimension, numbers.Integral):
            raise ValueError("dimension must be a positive integer")
        if dimension < 1:
            raise ValueError("dimension must be a positive integer")
        self._dimension = int(dimension)

    @property
    def dimension(self) -> int:
        return self._dimension

    def shift_operator(self) -> np.ndarray:
        """Return the cyclic shift where column ``i`` maps to row ``i + 1``."""
        shift = np.zeros((self._dimension, self._dimension), dtype=float)
        for source in range(self._dimension):
            shift[(source + 1) % self._dimension, source] = 1.0
        return shift
