"""Presentation-axis coordinate transformation."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np


def apply_5axis_presentation_change(
    cochain: Sequence[Any],
    axis: int,
    transform_matrix: Sequence[Sequence[Any]],
) -> tuple[float, ...]:
    """Apply a declared basis, gauge, dual, filtration, or sheaf transform."""

    if axis not in range(1, 6):
        raise ValueError(f"presentation axis must be in range 1..5, got {axis}")
    vector = np.asarray(cochain, dtype=float)
    transform = np.asarray(transform_matrix, dtype=float)
    if vector.ndim != 1 or transform.ndim != 2:
        raise ValueError("cochain must be a vector and transform must be a matrix")
    if transform.shape[1] != vector.shape[0]:
        raise ValueError("transform width must match cochain length")
    if not np.isfinite(vector).all() or not np.isfinite(transform).all():
        raise ValueError("presentation-change inputs must be finite")
    return tuple(float(value) for value in transform @ vector)


__all__ = ["apply_5axis_presentation_change"]
