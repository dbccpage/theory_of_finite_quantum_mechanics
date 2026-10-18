"""Paper Alpha primitive difference operator and discrete carrier separation floor.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Dict, List, Tuple


class PrimitiveDifference:
    """Primitive scalar difference and raw L1 inconsistency."""

    @staticmethod
    def validate(section: Dict[str, float]) -> None:
        for k, v in section.items():
            assert math.isfinite(v), f"Invalid scalar at {k}: {v}"

    @staticmethod
    def phi_raw(section: Dict[str, float], edges: List[Tuple[str, str]]) -> float:
        """Phi_raw = sum_e |x_b - x_a|."""
        PrimitiveDifference.validate(section)
        return sum(abs(section[b] - section[a]) for a, b in edges)

    @staticmethod
    def support(
        section: Dict[str, float],
        edges: List[Tuple[str, str]],
        tol: float = 1e-10,
    ) -> int:
        """Number of edges with nonzero defect."""
        return sum(1 for a, b in edges if abs(section[b] - section[a]) > tol)

    @staticmethod
    def delta_phi(
        old: Dict[str, float],
        new: Dict[str, float],
        edges: List[Tuple[str, str]],
        changed: List[str],
    ) -> float:
        """Incremental Phi change over edges incident to changed nodes."""
        PrimitiveDifference.validate(old)
        PrimitiveDifference.validate(new)
        changed_set = set(changed)
        total = 0.0
        for a, b in edges:
            if a in changed_set or b in changed_set:
                total += abs(new[b] - new[a]) - abs(old[b] - old[a])
        return total


@dataclass(frozen=True, order=True)
class SeparationCost:
    """Lexicographic cost vector (mu_1, mu_2) for carrier distinction.

    AuthorityEffect: None.

    Attributes:
        mu_1: Primary cost measuring total response items in declare-then-assert grammar.
        mu_2: Secondary refinement cost measuring total arity sum of newly declared forms.
    """
    mu_1: int
    mu_2: int

    @property
    def as_tuple(self) -> Tuple[int, int]:
        return (self.mu_1, self.mu_2)


@dataclass(frozen=True)
class SeparationFloorCertificate:
    """Machine-checkable dual witness certificate for the cost-two separation floor.

    AuthorityEffect: None.
    References:
        - WDP-CH03-P03: Separation price and the surviving tie.
        - SN-C05: Cost-2 floor theorem (1 form + 1 instance).
        - Genesis 19L57G1: Reading L (3 classes) vs Reading F (5 classes).

    Attributes:
        carrier_size: Number of points on the carrier set (|X| >= 2).
        mu_1: Minimum item count floor (strictly 2).
        mu_2: Minimal arity sum under refinement (strictly 1).
        lexicographic_cost: Tuple (mu_1, mu_2) = (2, 1).
        is_tied_under_mu_1: True, reflecting infinite arity family and bounded minima.
        mu_1_classes_bounded_arity_2: Number of non-isomorphic classes with arity <= 2 (3 for n=2, 5 for n>=3).
        resolved_under_mu_2: True, as arity sum minimisation isolates the unary form.
        surviving_isomorphism_classes: Number of isomorphism classes surviving mu_2 (strictly 1).
        surviving_instances: The concrete instances in the surviving class ('mark_a', 'mark_b').
        equivariant_selection_possible: False, as base automorphism (a b) exchanges them.
        authority_effect: Declared authority ceiling ("None").
    """
    carrier_size: int
    mu_1: int
    mu_2: int
    lexicographic_cost: Tuple[int, int]
    is_tied_under_mu_1: bool
    mu_1_classes_bounded_arity_2: int
    resolved_under_mu_2: bool
    surviving_isomorphism_classes: int
    surviving_instances: Tuple[str, ...]
    equivariant_selection_possible: bool
    authority_effect: str = "None"


def _require_carrier(carrier_size: object) -> int:
    """Reject a non-int, a bool, or a carrier too small for pair separation."""
    if isinstance(carrier_size, bool) or not isinstance(carrier_size, int):
        raise TypeError(
            f"carrier_size must be int, got {type(carrier_size).__name__}"
        )
    if carrier_size < 2:
        raise ValueError(f"carrier_size must be at least 2, got {carrier_size}")
    return carrier_size


def evaluate_cost_two_separation_floor(carrier_size: int) -> int:
    """Return the stated separation cost floor mu_1 = 2.

    AuthorityEffect: None.
    Reference: WDP-CH03-P03, SN-C05.

    The floor is the constant 2 for every carrier of size at least 2. This
    function checks the carrier and returns that constant. It does not search
    a grammar.

    Raises:
        TypeError: If carrier_size is not an int. Bool is rejected.
        ValueError: If carrier_size < 2.
    """
    _require_carrier(carrier_size)
    return 2


def evaluate_separation_cost(carrier_size: int, arity: int = 1) -> SeparationCost:
    """Compute the lexicographic separation cost (mu_1, mu_2) for a given form arity.

    AuthorityEffect: None.

    Args:
        carrier_size: Carrier cardinality (must be >= 2).
        arity: Arity of the distinguishing form (must be >= 1).

    Returns:
        SeparationCost(mu_1=2, mu_2=arity).

    Raises:
        ValueError: If carrier_size < 2 or arity < 1.
    """
    _require_carrier(carrier_size)
    if arity < 1:
        raise ValueError(f"arity must be at least 1, got {arity}")
    return SeparationCost(mu_1=2, mu_2=arity)


def evaluate_mu1_tied_classes(carrier_size: int, max_arity: int = 2) -> int:
    """Return the stated class counts for max_arity 1 and 2.

    AuthorityEffect: None.
    Reference: WDP-CH03-P03 worked count for arity at most 2.

    The counts this function returns are:
    - max_arity == 1: 1
    - max_arity == 2 and carrier_size == 2: 3
    - max_arity == 2 and carrier_size >= 3: 5

    Arity above 2 is not enumerated. A linear extrapolation is not a class count.

    Raises:
        TypeError: If carrier_size is not an int.
        ValueError: If carrier_size < 2, max_arity < 1, or max_arity > 2.
    """
    _require_carrier(carrier_size)
    if max_arity < 1:
        raise ValueError(f"max_arity must be at least 1, got {max_arity}")
    if max_arity == 1:
        return 1
    if max_arity == 2:
        return 3 if carrier_size == 2 else 5
    raise ValueError(
        f"max_arity {max_arity} is not enumerated; only 1 and 2 have a class count"
    )


def evaluate_mu2_refined_classes(carrier_size: int) -> int:
    """Count non-isomorphic classes under lexicographic refinement mu_2.

    AuthorityEffect: None.
    Reference: WDP-CH03-P03 clause 3, SN-C05.

    Refining mu_1 by form arity sum mu_2 forces arity k = 1. All binary and
    higher-arity responses are eliminated. Exactly 1 isomorphism class survives:
    the unary mark class.

    Args:
        carrier_size: Carrier cardinality (must be >= 2).

    Returns:
        Always returns 1, as the tie is uniquely resolved to the unary class.

    Raises:
        ValueError: If carrier_size < 2.
    """
    _require_carrier(carrier_size)
    return 1


def certify_cost_two_separation(carrier_size: int) -> SeparationFloorCertificate:
    """Return the stated cost-two record for a carrier of size at least 2.

    The numeric fields come from the floor and the arity-at-most-2 counts.
    The boolean fields restate that reading. They are not the result of a search.

    AuthorityEffect: None.
    Reference: WDP-CH03-P03, SN-C05.

    Args:
        carrier_size: Carrier cardinality (must be >= 2).

    Returns:
        SeparationFloorCertificate certifying exact floor and refinement invariants.

    Raises:
        ValueError: If carrier_size < 2.
    """
    _require_carrier(carrier_size)
    mu1 = evaluate_cost_two_separation_floor(carrier_size)
    cost = evaluate_separation_cost(carrier_size, arity=1)
    tied_classes = evaluate_mu1_tied_classes(carrier_size, max_arity=2)
    refined_classes = evaluate_mu2_refined_classes(carrier_size)
    return SeparationFloorCertificate(
        carrier_size=carrier_size,
        mu_1=mu1,
        mu_2=cost.mu_2,
        lexicographic_cost=(cost.mu_1, cost.mu_2),
        is_tied_under_mu_1=True,
        mu_1_classes_bounded_arity_2=tied_classes,
        resolved_under_mu_2=True,
        surviving_isomorphism_classes=refined_classes,
        surviving_instances=("mark_a", "mark_b"),
        equivariant_selection_possible=False,
        authority_effect="None",
    )


__all__ = [
    "PrimitiveDifference",
    "SeparationCost",
    "SeparationFloorCertificate",
    "evaluate_cost_two_separation_floor",
    "evaluate_separation_cost",
    "evaluate_mu1_tied_classes",
    "evaluate_mu2_refined_classes",
    "certify_cost_two_separation",
]
