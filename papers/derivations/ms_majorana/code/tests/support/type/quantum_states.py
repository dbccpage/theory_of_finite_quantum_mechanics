from pydantic import ConfigDict
"""Data-only quantum state containers."""

from pydantic.dataclasses import dataclass

import numpy as np


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class QuantumState:
    """Data-only container for a quantum-state amplitude array.

    Data-only container: it does NOT validate normalization, dimension, dtype,
    or positivity, and it must NOT terminalize anything. The only guard is a
    lightweight check that `amplitudes` is a finite numeric ndarray; all
    physical/mathematical interpretation is the caller's responsibility.
    """

    amplitudes: np.ndarray

    def __post_init__(self):
        arr = np.asarray(self.amplitudes)
        if arr.size and np.issubdtype(arr.dtype, np.number):
            if not np.all(np.isfinite(arr)):
                raise ValueError("QuantumState amplitudes must be finite")
        self.amplitudes = arr


