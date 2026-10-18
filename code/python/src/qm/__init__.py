"""Finite quantum mechanics: states, observables, campaigns, and exact suites."""
from ..linear_algebra import ExactMatrix, GaussianRational, Q, q
from .domain.gaussian_rational import Gaussian as DomainGaussianRational
import hashlib
from typing import Sequence, Tuple, Union

class QmError(Exception):
    pass

class DensityOperator:
    __slots__ = ("dim", "matrix")

    def __init__(self, matrix: ExactMatrix):
        rows, cols = matrix.shape()
        if rows != cols:
            raise QmError(f"Density operator must be square, got {rows}x{cols}")
        if not matrix.is_hermitian():
            raise QmError("Hermiticity violation: operator is not self-adjoint")

        tr_real = q(0)
        tr_imag = q(0)
        for i in range(rows):
            val = matrix.get(i, i)
            if isinstance(val, GaussianRational):
                tr_real += val.real
                tr_imag += val.imag
            else:
                tr_real += q(val)

        if tr_real != q(1) or tr_imag != q(0):
            raise QmError(f"Normalization violation: trace is {tr_real} + {tr_imag}i != 1")

        self.dim = rows
        self.matrix = matrix

    def dimension(self) -> int:
        return self.dim

    def expectation(self, observable: ExactMatrix) -> GaussianRational:
        if observable.shape() != (self.dim, self.dim):
            raise QmError(f"Observable shape {observable.shape()} != ({self.dim}, {self.dim})")
        prod = self.matrix * observable
        tr = GaussianRational.zero()
        for i in range(self.dim):
            val = prod.get(i, i)
            if isinstance(val, GaussianRational):
                tr = tr + val
            else:
                tr = tr + GaussianRational(val, 0)
        return tr

    def purity(self) -> Q:
        sq = self.matrix * self.matrix
        tr = q(0)
        for i in range(self.dim):
            val = sq.get(i, i)
            if isinstance(val, GaussianRational):
                tr += val.real
            else:
                tr += q(val)
        return tr

    def sha256(self) -> str:
        return self.matrix.sha256()

    def __repr__(self) -> str:
        return f"DensityOperator(dim={self.dim}, matrix={self.matrix})"

from . import domain
from . import campaigns
from . import entrypoints

__all__ = [
    "QmError",
    "DensityOperator",
    "domain",
    "campaigns",
    "entrypoints",
]
