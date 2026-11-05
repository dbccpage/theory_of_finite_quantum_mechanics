"""Chain transport maps, operator norms, and commutation residuals for CODA-FOC.

Bounded Context: CODA.FOC (Finite Obstruction Calculus)
AuthorityEffect: None.
Constraint: Zero floating-point operations in exact algebraic decision paths.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sympy import Abs, Rational, simplify

from .exact_arithmetic import (
    _as_exact_rational,
    _exact_matrix,
    _exact_vector,
)
from .packets import FiniteObstructionPacket


@dataclass(frozen=True, slots=True)
class TransportResiduals:
    """Rich Value Object holding commutation residuals across chain transport squares."""

    r0_max: Rational
    r1_max: Rational
    r2_max: Rational

    def __post_init__(self) -> None:
        object.__setattr__(self, "r0_max", _as_exact_rational(self.r0_max))
        object.__setattr__(self, "r1_max", _as_exact_rational(self.r1_max))
        object.__setattr__(self, "r2_max", _as_exact_rational(self.r2_max))

    @property
    def is_exact_morphism(self) -> bool:
        """Return True when all square commutation residuals vanish identically."""
        return self.r0_max == 0 and self.r1_max == 0 and self.r2_max == 0

    def __iter__(self):
        return iter((self.r0_max, self.r1_max, self.r2_max))

    def __getitem__(self, index: int) -> Rational:
        return (self.r0_max, self.r1_max, self.r2_max)[index]

    def __len__(self) -> int:
        return 3

    def as_tuple(self) -> tuple[Rational, Rational, Rational]:
        return (self.r0_max, self.r1_max, self.r2_max)


def weighted_l1_operator_norm(
    matrix: Any,
    source_weights: Any,
    target_weights: Any,
) -> Rational:
    """Compute the weighted L1 operator norm ||T||_{W_target, W_source}."""
    transform = _exact_matrix(matrix)
    source = _exact_vector(source_weights)
    target = _exact_vector(target_weights)
    if transform.rows != target.rows or transform.cols != source.rows:
        raise ValueError("transport dimensions do not match weights")
    if any(w <= 0 for w in source) or any(w <= 0 for w in target):
        raise ValueError("transport weights must be strictly positive")
    if transform.cols == 0:
        return Rational(0)
    col_norms = [
        sum(target[i, 0] * Abs(transform[i, j]) for i in range(transform.rows)) / source[j, 0]
        for j in range(transform.cols)
    ]
    return simplify(max(col_norms))


def transport_residuals(
    source: FiniteObstructionPacket,
    target: FiniteObstructionPacket,
    t0: Any,
    t1: Any,
    t2: Any,
    s2: Any,
) -> tuple[Rational, Rational, Rational]:
    """Compute exact commutation residuals for chain transport squares."""
    T0 = _exact_matrix(t0)
    T1 = _exact_matrix(t1)
    T2 = _exact_matrix(t2)
    S2 = _exact_matrix(s2)
    R0 = T1 * source.d0 - target.d0 * T0
    R1 = T2 * source.d1 - target.d1 * T1
    R2 = T2 * source.a2 - target.a2 * S2
    r0_max = max([Abs(v) for v in R0], default=Rational(0))
    r1_max = max([Abs(v) for v in R1], default=Rational(0))
    r2_max = max([Abs(v) for v in R2], default=Rational(0))
    return (simplify(r0_max), simplify(r1_max), simplify(r2_max))


__all__ = [
    "TransportResiduals",
    "transport_residuals",
    "weighted_l1_operator_norm",
]
