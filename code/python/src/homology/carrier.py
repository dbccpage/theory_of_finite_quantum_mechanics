"""Carrier complexes for finite quantum mechanics gauge and homology structures."""
import hashlib
from typing import Sequence, Tuple
from ..linear_algebra import ExactMatrix
from .errors import NonZeroCompositionError

class Carrier:
    __slots__ = ("dim0", "dim1", "dim2", "d0", "d1", "weights")

    def __init__(
        self,
        dim0: int,
        dim1: int,
        dim2: int,
        d0: ExactMatrix,
        d1: ExactMatrix,
        weights: Sequence[object] | None = None,
    ):
        if d0.shape() != (dim1, dim0):
            raise ValueError(f"d0 shape {d0.shape()} does not match dims ({dim1}, {dim0})")
        if d1.shape() != (dim2, dim1):
            raise ValueError(f"d1 shape {d1.shape()} does not match dims ({dim2}, {dim1})")

        comp = d1 * d0
        zeros = ExactMatrix.zeros(dim2, dim0)
        if comp != zeros:
            raise NonZeroCompositionError("d1 . d0 != 0 in Carrier complex")

        self.dim0 = dim0
        self.dim1 = dim1
        self.dim2 = dim2
        self.d0 = d0
        self.d1 = d1
        self.weights = list(weights) if weights is not None else None

    def dimensions(self) -> Tuple[int, int, int]:
        return (self.dim0, self.dim1, self.dim2)

    def rank_d0(self) -> int:
        return self.d0.rank()

    def rank_d1(self) -> int:
        return self.d1.rank()

    def dim_q1(self) -> int:
        return self.dim1 - self.rank_d0()

    def dim_h1(self) -> int:
        ker_d1 = self.dim1 - self.rank_d1()
        im_d0 = self.rank_d0()
        return ker_d1 - im_d0

    def sha256(self) -> str:
        h = hashlib.sha256()
        h.update(f"{self.dim0},{self.dim1},{self.dim2}:".encode("utf-8"))
        h.update(self.d0.sha256().encode("utf-8"))
        h.update(self.d1.sha256().encode("utf-8"))
        return h.hexdigest()
