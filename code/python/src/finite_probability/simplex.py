"""Probability simplices and stochastic maps with exact rational arithmetic.
Under the Zero-Float Law, every mass is a fractions.Fraction and sums to exactly 1.
"""

from __future__ import annotations
from fractions import Fraction
from dataclasses import dataclass
from typing import List, Sequence, Tuple, Optional


class ProbabilitySimplex:
    """Exact rational probability distribution on Fin n."""

    def __init__(self, probs: Sequence[Fraction | int | Tuple[int, int]], label: str = "") -> None:
        raw = []
        for x in probs:
            if isinstance(x, tuple):
                raw.append(Fraction(x[0], x[1]))
            else:
                raw.append(Fraction(x))

        if not raw:
            raise ValueError("Probability simplex cannot be empty")
        for i, p in enumerate(raw):
            if p < 0:
                raise ValueError(f"Negative mass at index {i}: {p}")
        total = sum(raw)
        if total != Fraction(1):
            raise ValueError(f"Probabilities must sum to 1, got {total}")

        self._probs = raw
        self.label = label

    @classmethod
    def uniform(cls, n: int, label: str = "uniform") -> ProbabilitySimplex:
        if n <= 0:
            raise ValueError("Dimension must be positive")
        p = Fraction(1, n)
        return cls([p] * n, label)

    @classmethod
    def dirac(cls, n: int, index: int, label: str = "dirac") -> ProbabilitySimplex:
        if n <= 0:
            raise ValueError("Dimension must be positive")
        if not (0 <= index < n):
            raise IndexError(f"Index {index} out of range for dimension {n}")
        probs = [Fraction(1) if i == index else Fraction(0) for i in range(n)]
        return cls(probs, label)

    @property
    def dim(self) -> int:
        return len(self._probs)

    @property
    def probs(self) -> List[Fraction]:
        return list(self._probs)

    def __getitem__(self, index: int) -> Fraction:
        return self._probs[index]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ProbabilitySimplex):
            return False
        return self._probs == other._probs

    def total_variation_distance(self, other: ProbabilitySimplex) -> Fraction:
        """1/2 sum_i |p_i - q_i|."""
        if self.dim != other.dim:
            raise ValueError(f"Dimension mismatch: {self.dim} vs {other.dim}")
        return Fraction(1, 2) * sum(abs(p - q) for p, q in zip(self._probs, other._probs))

    def mixture(self, other: ProbabilitySimplex, weight: Fraction | Tuple[int, int]) -> ProbabilitySimplex:
        """w * self + (1 - w) * other."""
        if isinstance(weight, tuple):
            w = Fraction(weight[0], weight[1])
        else:
            w = Fraction(weight)
        if not (Fraction(0) <= w <= Fraction(1)):
            raise ValueError(f"Mixture weight must be in [0, 1], got {w}")
        if self.dim != other.dim:
            raise ValueError(f"Dimension mismatch: {self.dim} vs {other.dim}")
        mixed = [w * p + (Fraction(1) - w) * q for p, q in zip(self._probs, other._probs)]
        return ProbabilitySimplex(mixed, f"mix({self.label}, {other.label})")

    def expectation(self, values: Sequence[Fraction | int]) -> Fraction:
        if len(values) != self.dim:
            raise ValueError("Values length mismatch")
        return sum(p * Fraction(v) for p, v in zip(self._probs, values))


class StochasticMap:
    """Row-stochastic transition matrix M with entries in Fraction."""

    def __init__(self, matrix: Sequence[Sequence[Fraction | int | Tuple[int, int]]]) -> None:
        rows = len(matrix)
        if rows == 0:
            raise ValueError("Matrix cannot be empty")
        cols = len(matrix[0])
        if cols == 0:
            raise ValueError("Matrix columns cannot be empty")

        parsed: List[List[Fraction]] = []
        for r_idx, row in enumerate(matrix):
            if len(row) != cols:
                raise ValueError(f"Inconsistent column count at row {r_idx}")
            p_row: List[Fraction] = []
            for c_idx, val in enumerate(row):
                if isinstance(val, tuple):
                    f_val = Fraction(val[0], val[1])
                else:
                    f_val = Fraction(val)
                if f_val < 0:
                    raise ValueError(f"Negative transition probability at ({r_idx}, {c_idx}): {f_val}")
                p_row.append(f_val)
            row_sum = sum(p_row)
            if row_sum != Fraction(1):
                raise ValueError(f"Row {r_idx} must sum to 1, got {row_sum}")
            parsed.append(p_row)

        self.rows = rows
        self.cols = cols
        self._data = parsed

    def apply(self, dist: ProbabilitySimplex) -> ProbabilitySimplex:
        """Pushes forward distribution p: q_j = sum_i p_i M_{ij}."""
        if dist.dim != self.rows:
            raise ValueError(f"Dimension mismatch: dist {dist.dim} vs matrix rows {self.rows}")
        out = [sum(dist[i] * self._data[i][j] for i in range(self.rows)) for j in range(self.cols)]
        return ProbabilitySimplex(out)
