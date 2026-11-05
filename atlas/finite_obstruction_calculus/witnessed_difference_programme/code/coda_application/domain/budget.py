# -*- coding: utf-8 -*-
"""
Non-Terminal Computation Budget Guard (Paper 028).

Enforces:
1. Reasoning Authority Non-Generation Invariant:
   Computation, heuristic search, or deductive steps cannot synthesize authority tokens:
   forall n in N, step^n(E) subseteq E.
2. Finite Non-Terminal Budget:
   Execution time T and step count N must stay strictly within declared bounds.
   If exhausted without terminal certificate generation, execution halts closed
   into BudgetUnknown / Refusal rather than permissive fallthrough.

The domain reads no clock of its own: a time limit is enforced only through a clock
the caller injects (the use cases pass ``time.perf_counter``). Without a clock the
guard enforces the step limit alone. The exact solver calls ``tick`` inside its loops,
so exhaustion interrupts a layer instead of being noticed after it.

AuthorityEffect: None.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Callable, Optional

from coda_application.domain.value_objects import ExactRational

Clock = Callable[[], float]


class BudgetExhaustedError(RuntimeError):
    """Raised when computational budget (time or steps) is exceeded."""


def _finite_positive(value, name: str):
    if isinstance(value, bool) or not isinstance(value, (int, float, Fraction)):
        raise ValueError(f"{name} must be a positive finite number, got {value!r}")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{name} must be finite, got {value!r}")
    if value <= 0:
        raise ValueError(f"{name} must be strictly positive")
    return value


class NonTerminalBudgetGuard:
    """
    Guards computation loops against non-terminal divergence and unbounded execution.
    Defaults to 3.0 seconds (when a clock is supplied) and 5,000,000 steps.
    """

    DEFAULT_MAX_SECONDS = 3.0
    DEFAULT_MAX_STEPS = 5_000_000

    def __init__(
        self,
        max_seconds: float = DEFAULT_MAX_SECONDS,
        max_steps: int = DEFAULT_MAX_STEPS,
        clock: Optional[Clock] = None,
    ):
        self.max_seconds = _finite_positive(max_seconds, "max_seconds")
        if isinstance(max_steps, bool) or not isinstance(max_steps, int) or max_steps <= 0:
            raise ValueError("max_steps must be a strictly positive int")
        self.max_steps = max_steps
        self.clock = clock
        self.step_count = 0
        self._start_time: Optional[float] = None
        self._elapsed: float = 0.0

    def __enter__(self) -> NonTerminalBudgetGuard:
        self.step_count = 0
        self._start_time = self.clock() if self.clock is not None else None
        self._elapsed = 0.0
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._update_elapsed()
        return False

    def _update_elapsed(self) -> None:
        if self._start_time is not None and self.clock is not None:
            self._elapsed = self.clock() - self._start_time

    def tick(self, steps: int = 1) -> None:
        """Increment step count and raise BudgetExhaustedError once a bound is exceeded."""
        if type(steps) is not int or steps < 0:
            raise ValueError("steps must be a nonnegative integer; zero checks the clock")
        self.step_count += steps
        if self.step_count > self.max_steps:
            raise BudgetExhaustedError(
                f"BUDGET EXHAUSTION: Step limit {self.max_steps} exceeded (reached {self.step_count})"
            )
        if self._start_time is not None:
            self._update_elapsed()
            if self._elapsed > self.max_seconds:
                raise BudgetExhaustedError(
                    f"BUDGET EXHAUSTION: Time limit {float(self.max_seconds):.3g}s exceeded "
                    f"(elapsed {self._elapsed:.3f}s)"
                )

    def check(self) -> None:
        """One solver step; the callback the exact solver receives."""
        self.tick(1)

    @property
    def elapsed_seconds(self) -> float:
        return self._elapsed

    @property
    def exact_elapsed_rational(self) -> ExactRational:
        """Elapsed time as exact milliseconds (the clock's float is truncated, not trusted)."""
        return ExactRational(int(self._elapsed * 1000), 1000)
