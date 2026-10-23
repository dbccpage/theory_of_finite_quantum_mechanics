"""Finite input contracts for the numerical examples."""

from __future__ import annotations

import math
from numbers import Integral, Real
from typing import Sequence

import numpy as np


def nonnegative(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite nonnegative real")
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise ValueError(f"{name} must be a finite nonnegative real")
    return result


def integer(value: int, name: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, Integral) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return int(value)


def dimensions(dims: Sequence[int]) -> tuple[int, ...]:
    result = tuple(integer(d, "subsystem dimension", 1) for d in dims)
    if not result:
        raise ValueError("dims must be nonempty")
    return result


def indices(keep: Sequence[int], count: int) -> tuple[int, ...]:
    result = tuple(integer(i, "subsystem index") for i in keep)
    if len(set(result)) != len(result) or any(i >= count for i in result):
        raise ValueError("subsystem indices must be unique and in range")
    return result


def matrix(value: np.ndarray, name: str, shape: tuple[int, int] | None = None) -> np.ndarray:
    try:
        result = np.asarray(value, dtype=complex)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{name} must be a finite matrix") from error
    if result.ndim != 2 or min(result.shape) == 0 or not np.isfinite(result).all():
        raise ValueError(f"{name} must be a finite nonempty matrix")
    if shape is not None and result.shape != shape:
        raise ValueError(f"{name} shape {result.shape} != {shape}")
    return result


def density(value: np.ndarray, dim: int, tol: float = 1e-10) -> np.ndarray:
    result = matrix(value, "density matrix", (dim, dim))
    if not np.allclose(result, result.conj().T, atol=tol, rtol=0):
        raise ValueError("density matrix must be Hermitian")
    if abs(np.trace(result) - 1) > tol:
        raise ValueError("density matrix must have unit trace")
    if np.linalg.eigvalsh(result).min() < -tol:
        raise ValueError("density matrix must be positive semidefinite")
    return result


def reference(
    marginals: Sequence[np.ndarray], dims: Sequence[int]
) -> tuple[tuple[int, ...], list[np.ndarray]]:
    ds = dimensions(dims)
    if len(marginals) != len(ds):
        raise ValueError("number of marginals must match dims")
    return ds, [density(rho, d) for rho, d in zip(marginals, ds, strict=True)]
