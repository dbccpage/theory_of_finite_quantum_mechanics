from __future__ import annotations
from pydantic import ConfigDict
r"""
Canonical PrimitiveDifference kernel for Python in omega_engine/type.

Formal Lean 4 backing: `omega_engine/lean4/shared_kernel/primitive_difference.lean`.
Matches `OmegaCore.PrimitiveDifference`, `ResidualQuotient`, `DeltaCongruent`, `InvariantCongruent`,
and `PointedPrimitiveDifference`.

AuthorityEffect: None.
"""


from pydantic.dataclasses import dataclass
from typing import Any, Callable, Generic, List, Optional, Tuple, TypeVar

from pydantic import BaseModel, Field

Alpha = TypeVar("Alpha")
Beta = TypeVar("Beta")
Gamma = TypeVar("Gamma")


class PrimitiveDifferenceJudgment(BaseModel):
    left_presentation: str
    right_presentation: str
    zero_difference_relation: str
    licensed_equivalences: List[str] = Field(default_factory=list)
    quotient_residual: str
    residual_class: str
    factors_through_quotient: bool
    authority_effect: str = "None"


@dataclass(config=ConfigDict(arbitrary_types_allowed=True, frozen=True))
class ResidualClass(Generic[Alpha]):
    r"""Represents an equivalence class [x]_\sim in the ResidualQuotient \alpha / \sim."""

    representative: Alpha
    zero_rel: Callable[[Alpha, Alpha], bool]

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ResidualClass):
            return self.zero_rel(self.representative, other.representative)
        return False

    def __hash__(self) -> int:
        return hash(self.representative)


class PrimitiveDifference(Generic[Alpha, Beta]):
    r"""Canonical PrimitiveDifference kernel: \delta: \alpha \to \alpha \to \beta with zero predicate.

    Lean 4 source: `structure PrimitiveDifference (α : Type u) (β : Type v)`.
    """

    def __init__(
        self,
        delta: Callable[[Alpha, Alpha], Beta],
        zero: Callable[[Beta], bool],
    ):
        self._delta = delta
        self._zero = zero

    def delta(self, x: Alpha, y: Alpha) -> Beta:
        r"""Evaluates the difference operator \delta(x, y)."""
        return self._delta(x, y)

    def zero(self, b: Beta) -> bool:
        """Evaluates the zero-difference predicate Zero(b)."""
        return self._zero(b)

    def zero_rel(self, x: Alpha, y: Alpha) -> bool:
        r"""Evaluates ZeroRel(x, y) := Zero(\delta(x, y))."""
        return self._zero(self._delta(x, y))

    def class_of(self, x: Alpha) -> ResidualClass[Alpha]:
        """Maps x to its equivalence class in ResidualQuotient."""
        return ResidualClass(representative=x, zero_rel=self.zero_rel)

    def delta_congruent(self, tuples: List[Tuple[Alpha, Alpha, Alpha, Alpha]]) -> bool:
        r"""Checks DeltaCongruent: x \sim x' \land y \sim y' \implies \delta(x, y) == \delta(x', y')."""
        for x, x_prime, y, y_prime in tuples:
            if self.zero_rel(x, x_prime) and self.zero_rel(y, y_prime):
                if self._delta(x, y) != self._delta(x_prime, y_prime):
                    return False
        return True

    def delta_factor(self, qx: ResidualClass[Alpha], qy: ResidualClass[Alpha]) -> Beta:
        r"""Descends \delta to the ResidualQuotient."""
        return self._delta(qx.representative, qy.representative)

    def invariant_congruent(
        self, phi: Callable[[Alpha], Gamma], pairs: List[Tuple[Alpha, Alpha]]
    ) -> bool:
        r"""Checks InvariantCongruent: x \sim y \implies \phi(x) == \phi(y)."""
        for x, y in pairs:
            if self.zero_rel(x, y) and phi(x) != phi(y):
                return False
        return True

    def invariant_factor(
        self, phi: Callable[[Alpha], Gamma], q: ResidualClass[Alpha]
    ) -> Gamma:
        r"""Descends \phi to the ResidualQuotient."""
        return phi(q.representative)

    def factors_through(
        self, witnesses: List[Tuple[Alpha, Alpha]], phi: Callable[[Alpha], Gamma]
    ) -> bool:
        """Alias for invariant_congruent."""
        return self.invariant_congruent(phi, witnesses)



class PointedPrimitiveDifference(PrimitiveDifference[Alpha, Beta]):
    r"""Pointed Primitive Difference with a distinguished zero element \alpha_0."""

    def __init__(
        self,
        delta: Callable[[Alpha, Alpha], Beta],
        zero_pred: Callable[[Beta], bool],
        zero_element: Alpha,
    ):
        super().__init__(delta, zero_pred)
        self.zero_element = zero_element

    def zero_class(self) -> ResidualClass[Alpha]:
        return self.class_of(self.zero_element)

    def is_zero_class(self, q: ResidualClass[Alpha]) -> bool:
        return q == self.zero_class()


