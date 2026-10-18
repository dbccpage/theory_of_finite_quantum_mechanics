"""Packed upper-triangular Hermitian storage.

Faithful port of ``crates/omega_engine.crates.engine/src/quantum/packed_hermitian.rs``.
Round-trips through :class:`omega_linear_algebra.density.NumericalDensityMatrix`.
"""

from __future__ import annotations
from typing import List

import numpy as np

from omega_engine.crates.linear_algebra_theory.density import (
    DensityMatrixConfig,
    DensityMatrixCandidate,
    NumericalDensityMatrix,
)


class PackedHermitianError(Exception):
    pass


class ZeroDimension(PackedHermitianError):
    pass


class DataLengthMismatch(PackedHermitianError):
    pass


def _packed_index(dim: int, i: int, j: int) -> int:
    return i * (2 * dim - i - 1) // 2 + j


class PackedHermitian:
    def __init__(self, dim: int, data: List[complex]):
        self.dim = dim
        self.data = data

    @staticmethod
    def packed_len(dim: int) -> int:
        return dim * (dim + 1) // 2

    @classmethod
    def new(cls, dim: int, data: List[complex]) -> "PackedHermitian":
        if dim == 0:
            raise ZeroDimension("packed Hermitian dimension must be positive")
        expected = cls.packed_len(dim)
        if len(data) != expected:
            raise DataLengthMismatch(
                f"packed Hermitian data length mismatch: expected {expected}, got {len(data)}"
            )
        return cls(dim, list(data))

    @classmethod
    def from_density_matrix(cls, dm: NumericalDensityMatrix) -> "PackedHermitian":
        dim = dm.dim()
        rho = dm.rho()
        data = []
        for i in range(dim):
            for j in range(i, dim):
                data.append(complex(rho[i, j]))
        return cls.new(dim, data)

    def to_density_matrix(self) -> NumericalDensityMatrix:
        dim = self.dim
        m = np.zeros((dim, dim), dtype=complex)
        for i in range(dim):
            for j in range(i, dim):
                val = self.data[_packed_index(dim, i, j)]
                m[i, j] = val
                if i != j:
                    m[j, i] = np.conj(val)
        cfg = DensityMatrixConfig.default()
        return DensityMatrixCandidate.from_rho(m).validate(cfg)

    def get(self, i: int, j: int) -> complex:
        if i <= j:
            return self.data[_packed_index(self.dim, i, j)]
        return np.conj(self.data[_packed_index(self.dim, j, i)])

    def diagonal(self) -> List[float]:
        return [self.data[_packed_index(self.dim, i, i)].real for i in range(self.dim)]



