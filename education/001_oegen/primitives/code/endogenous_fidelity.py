"""Genesis Primitives Category 19: Endogenous Fidelity, No-Outside Invariants & Gauge Breaking.

Selected educational models related to 19L57G1 (lean4/Derivation/NoOutside.lean, FidelityClosure.lean, Breaking.lean).
Classification: Genesis Foundation Substrate.
AuthorityEffect: None.

The No-Outside Contract, the Effectual-Outside Dichotomy (Rule 1 & Rule 3),
fidelity closure, and explicit symmetry-breaking witnesses.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .canonical import validate_typed_fields
from .represented_progress import World


@dataclass(frozen=True)
class RepresentedSupport:
    """The operational support of a World state excluding inert notes."""

    data: tuple[int, ...]
    views: tuple[tuple[int, ...], ...]
    reqs: tuple[tuple[int, int], ...]
    refusals: tuple[tuple[int, int], ...]
    budget: int
    aug_licensed: bool

    def __post_init__(self) -> None:
        validate_typed_fields(self)


def extract_support(w: World) -> RepresentedSupport:
    """Extracts the represented support tuple."""
    return RepresentedSupport(
        data=w.data,
        views=w.views,
        reqs=w.reqs,
        refusals=w.refusals,
        budget=w.budget,
        aug_licensed=w.aug_licensed,
    )


def effectual_outside_dichotomy_check(
    w1: World,
    w2: World,
    evaluator: Callable[[World], Any],
) -> bool:
    """Verifies the Effectual-Outside Dichotomy:
    If two configurations agree on represented support, every internal operational
    evaluation must agree identically.
    Contrapositively: any difference that alters an operational verdict MUST already
    appear inside the represented support.
    """
    if extract_support(w1) == extract_support(w2):
        return evaluator(w1) == evaluator(w2)
    return True


@dataclass(frozen=True)
class SymmetryBreakingWitness:
    """Witness certifying the breaking of a relational symmetry."""

    symmetry_name: str
    broken_pair: tuple[int, int]
    distinguishing_relation: str

    def __post_init__(self) -> None:
        validate_typed_fields(self)
