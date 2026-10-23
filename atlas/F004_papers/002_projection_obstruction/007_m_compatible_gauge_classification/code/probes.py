"""Explicit counterexample search probes for GS-001.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence
import numpy as np

Gauge = Callable[[np.ndarray], float]


@dataclass(frozen=True)
class CounterexampleResult:
    """Typed result of a finite sample-based counterexample search.

    Never pretends to be an unbounded proof or Boolean truth predicate!
    """

    found_counterexample: bool
    witness: np.ndarray | None
    sample_count: int
    seed: int
    description: str

    def __bool__(self) -> bool:
        """Bool conversion returns True if a counterexample was found."""
        return self.found_counterexample


def probe_counterexample_search(
    property_test: Callable[[np.ndarray], bool],
    sample_vectors: Sequence[np.ndarray],
    seed: int = 42,
    description: str = "Counterexample search probe",
) -> CounterexampleResult:
    """Explicit counterexample search over sample vectors.

    Returns CounterexampleResult(found_counterexample=True/False, witness=...).
    """
    for v in sample_vectors:
        if not property_test(v):
            return CounterexampleResult(
                found_counterexample=True,
                witness=v,
                sample_count=len(sample_vectors),
                seed=seed,
                description=description,
            )

    return CounterexampleResult(
        found_counterexample=False,
        witness=None,
        sample_count=len(sample_vectors),
        seed=seed,
        description=description,
    )
