"""Port of ``omega_solvers/src/fixpoint.rs``.

Fixpoint convergence protocol and bounded recursion runner.
"""

from __future__ import annotations
from typing import Protocol, TypeVar

S = TypeVar("S")


class FixpointConverge(Protocol[S]):
    """Trait ``FixpointConverge<S>``: a step map and a convergence predicate."""

    def step(self, state: S) -> S:
        ...

    def has_converged(self, old: S, new: S) -> bool:
        ...


def _fixpoint_recursive_runner(solver, state, remaining_steps: int):
    """Tail-recursive-style fixpoint runner (loop-free in Rust).

    Implemented iteratively here to avoid Python recursion-depth limits while
    preserving identical semantics.
    """
    while True:
        if remaining_steps == 0:
            return state
        nxt = solver.step(state)
        if solver.has_converged(state, nxt):
            return nxt
        state = nxt
        remaining_steps -= 1


def fixpoint_bounded_recursion(solver, initial, max_steps: int):
    """Bounded fixpoint runner. Raises ``ValueError`` if the budget is not positive.

    A negative budget never reaches ``remaining_steps == 0`` and would loop
    indefinitely when the solver does not converge.
    """
    if max_steps <= 0:
        raise ValueError("Iteration budget must be positive")
    return _fixpoint_recursive_runner(solver, initial, max_steps)
