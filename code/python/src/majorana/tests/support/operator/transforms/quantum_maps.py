"""Quantum map transforms."""

from __future__ import annotations
import numpy as np


def squared_modulus_map(arr: Any) -> np.ndarray:
    """Calculates squared modulus |arr|^2 elementwise."""
    return np.abs(np.asarray(arr)) ** 2
