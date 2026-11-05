"""Immutable 2x2 matrix of Gaussian-rational values; no physical SU(2) claim by construction."""
from __future__ import annotations
from dataclasses import dataclass
from .gaussian_rational import GaussianRational as G
from .boundary import Violation


@dataclass(frozen=True, slots=True)
class GaussianMatrix2:
    a11: G
    a12: G
    a21: G
    a22: G

    def __post_init__(self) -> None:
        if any(type(x) is not G for x in (self.a11,self.a12,self.a21,self.a22)):
            raise Violation("input", "matrix entries must be GaussianRational values")

    @staticmethod
    def eye() -> GaussianMatrix2:
        return GaussianMatrix2(G(1),G(0),G(0),G(1))

    @staticmethod
    def pauli_z() -> GaussianMatrix2:
        return GaussianMatrix2(G(1),G(0),G(0),G(-1))

    @staticmethod
    def pauli_x() -> GaussianMatrix2:
        return GaussianMatrix2(G(0),G(1),G(1),G(0))

    def mul(self, other: GaussianMatrix2) -> GaussianMatrix2:
        if type(other) is not GaussianMatrix2:
            raise Violation("input", "matrix multiplication requires a GaussianMatrix2 operand")
        return GaussianMatrix2(self.a11*other.a11+self.a12*other.a21,
                               self.a11*other.a12+self.a12*other.a22,
                               self.a21*other.a11+self.a22*other.a21,
                               self.a21*other.a12+self.a22*other.a22)

    def trace(self) -> G:
        return self.a11+self.a22

    def det(self) -> G:
        return self.a11*self.a22-self.a12*self.a21

    def inv(self) -> GaussianMatrix2:
        inv_det=self.det().inv()
        return GaussianMatrix2(self.a22*inv_det,G(-1)*self.a12*inv_det,
                               G(-1)*self.a21*inv_det,self.a11*inv_det)

    def adjoint(self) -> GaussianMatrix2:
        return GaussianMatrix2(self.a11.conj(), self.a21.conj(),
                               self.a12.conj(), self.a22.conj())

    def is_unitary(self) -> bool:
        return self.adjoint().mul(self) == self.eye()
