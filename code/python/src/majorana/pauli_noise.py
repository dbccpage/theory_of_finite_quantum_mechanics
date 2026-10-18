"""Exact local Majorana Hamiltonian noise and deterministic rational sampling.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence

from .braid_action import MajoranaBraidAction

MAX_NOISE_MODES: int = 1_024


class NoiseError(Exception):
    pass


@dataclass
class SkewNoiseMatrix:
    dim: int
    data: list[list[Fraction]]

    def __post_init__(self) -> None:
        if self.dim < 2 or self.dim > MAX_NOISE_MODES:
            raise NoiseError(f"dim {self.dim} outside 2..={MAX_NOISE_MODES}")
        if len(self.data) != self.dim or any(len(r) != self.dim for r in self.data):
            raise NoiseError("Invalid shape for noise matrix")
        for i in range(self.dim):
            if self.data[i][i] != 0:
                raise NoiseError(f"Nonzero diagonal at mode {i + 1}")
            for j in range(self.dim):
                if self.data[i][j] != -self.data[j][i]:
                    raise NoiseError(f"Matrix not skew-symmetric at ({i + 1}, {j + 1})")

    @classmethod
    def zeros(cls, dim: int) -> SkewNoiseMatrix:
        return cls(dim, [[Fraction(0) for _ in range(dim)] for _ in range(dim)])

    def conjugate_by_braid(self, action: MajoranaBraidAction) -> SkewNoiseMatrix:
        """K'_{ij} = s_i s_j K_{pi(i), pi(j)}."""
        if action.mode_count() != self.dim:
            raise NoiseError(f"braid has {action.mode_count()} modes, noise has {self.dim}")
        out = [[Fraction(0) for _ in range(self.dim)] for _ in range(self.dim)]
        for i in range(self.dim):
            img_i = action.image(i + 1)
            pi_i = img_i.mode - 1
            s_i = img_i.sign
            for j in range(self.dim):
                img_j = action.image(j + 1)
                pi_j = img_j.mode - 1
                s_j = img_j.sign
                out[i][j] = self.data[pi_i][pi_j] * s_i * s_j
        return SkewNoiseMatrix(self.dim, out)

    def frobenius_norm_sq(self) -> Fraction:
        return sum(x * x for row in self.data for x in row)

    def max_abs_entry(self) -> Fraction:
        return max(abs(x) for row in self.data for x in row)
