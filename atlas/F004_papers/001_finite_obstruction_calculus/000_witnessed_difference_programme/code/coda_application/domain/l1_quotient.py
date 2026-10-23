"""Exact certificate data and the functional-evaluation interface.

Implementations must delegate Phi_1 and Gamma_2 evaluation to omega_functional.
The domain accepts an explicit evaluator; it performs no functional arithmetic
and supplies no default I/O implementation.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Dict, Protocol, Sequence, Tuple

Row = Dict[int, Fraction]
Tick = Callable[[], None]


def _no_tick() -> None:
    pass


@dataclass(frozen=True)
class QuotientCertificate:
    distance: Fraction
    repair: Tuple[Fraction, ...]
    residual: Tuple[Fraction, ...]
    witness: Tuple[Fraction, ...]
    method: str

    def __post_init__(self) -> None:
        for name in ("repair", "residual", "witness"):
            object.__setattr__(self, name, tuple(getattr(self, name)))

    def verify(self, rows, n_cols, x, *, evaluator: FunctionalEvaluator) -> bool:
        return evaluator.verify(self, rows, n_cols, x)


class FunctionalEvaluator(Protocol):
    """Trusted operator port, never a proposal field.

    The outer application composition root supplies NativeFunctionalEvaluator. Replacing this
    port changes the trusted evaluator and is outside the untrusted-data model.
    """
    def mass(self, values, tick: Tick = _no_tick) -> Fraction: ...
    def solve(self, rows: Sequence[Row], n_cols: int, x: Sequence[Fraction], tick: Tick = _no_tick) -> QuotientCertificate: ...
    def verify(self, certificate: QuotientCertificate, rows, n_cols, x) -> bool: ...
    def verify_repair(self, rows, n_cols, x, repair, witness, value, tick: Tick = _no_tick) -> bool: ...
    def closure(self, d0, n_cols, d1, x, tick: Tick = _no_tick) -> Fraction: ...


def solve_l1_quotient(rows, n_cols, x, tick: Tick = _no_tick, *, evaluator: FunctionalEvaluator) -> QuotientCertificate:
    """Request a checked certificate from the explicitly supplied evaluator."""
    return evaluator.solve(rows, n_cols, x, tick)
