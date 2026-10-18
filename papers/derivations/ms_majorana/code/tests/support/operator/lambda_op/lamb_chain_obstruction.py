"""Projection-obstruction operator for finite matrix presentations."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np


def compute_po_015_projection_obstruction(
    differential: Sequence[Sequence[Any]],
    projection: Sequence[Sequence[Any]],
    *,
    tolerance: float = 1e-12,
) -> tuple[bool, float]:
    """Evaluate P d (1-P) + (1-P) d P in an explicit float profile."""

    differential_array = np.asarray(differential, dtype=float)
    projection_array = np.asarray(projection, dtype=float)
    if differential_array.ndim != 2 or projection_array.ndim != 2:
        raise ValueError("differential and projection must be matrices")
    if projection_array.shape[0] != projection_array.shape[1]:
        raise ValueError("projection must be square")
    if differential_array.shape != projection_array.shape:
        raise ValueError("differential and projection shapes must match")
    if not np.isfinite(differential_array).all() or not np.isfinite(
        projection_array
    ).all():
        raise ValueError("projection-obstruction inputs must be finite")

    identity = np.eye(projection_array.shape[0])
    obstruction = (
        projection_array @ differential_array @ (identity - projection_array)
        + (identity - projection_array)
        @ differential_array
        @ projection_array
    )
    norm = float(np.linalg.norm(obstruction))
    return norm <= tolerance, norm


__all__ = ["compute_po_015_projection_obstruction"]
