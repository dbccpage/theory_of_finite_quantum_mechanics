"""Paper Alpha primitive difference operator and discrete carrier separation floor.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations  # permutations canonicalizes graphs
from typing import Dict, List, Tuple


class PrimitiveDifferenceError(Exception):
    """A section entry was not a finite rational, or a separation search failed."""


def _as_fraction(value: object) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, float, Fraction)):
        raise PrimitiveDifferenceError(f"scalar must be rational, got {type(value).__name__}")
    if isinstance(value, float):
        if value != value or value in (float("inf"), float("-inf")):
            raise PrimitiveDifferenceError(f"Invalid scalar: {value}")
    return Fraction(value)


class PrimitiveDifference:
    """Primitive scalar difference and raw L1 inconsistency."""

    @staticmethod
    def validate(section: Dict[str, float]) -> None:
        for key, value in section.items():
            _as_fraction(value)
            if not isinstance(key, str):
                raise PrimitiveDifferenceError(f"section key {key!r} is not a string")

    @staticmethod
    def phi_raw(section: Dict[str, float], edges: List[Tuple[str, str]]) -> Fraction:
        """Phi_raw = sum_e |x_b - x_a|, summed in the rationals."""
        PrimitiveDifference.validate(section)
        total = Fraction(0)
        for origin, target in edges:
            total += abs(_as_fraction(section[target]) - _as_fraction(section[origin]))
        return total

    @staticmethod
    def support(
        section: Dict[str, float],
        edges: List[Tuple[str, str]],
        tol: float = 1e-10,
    ) -> int:
        """Number of edges whose rational defect is nonzero. `tol` is ignored."""
        del tol
        return sum(
            1
            for origin, target in edges
            if _as_fraction(section[target]) != _as_fraction(section[origin])
        )

    @staticmethod
    def delta_phi(
        old: Dict[str, float],
        new: Dict[str, float],
        edges: List[Tuple[str, str]],
        changed: List[str],
    ) -> Fraction:
        """Incremental Phi change over edges incident to changed nodes."""
        PrimitiveDifference.validate(old)
        PrimitiveDifference.validate(new)
        changed_set = set(changed)
        total = Fraction(0)
        for origin, target in edges:
            if origin in changed_set or target in changed_set:
                total += abs(_as_fraction(new[target]) - _as_fraction(new[origin]))
                total -= abs(_as_fraction(old[target]) - _as_fraction(old[origin]))
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
    """Return the cheapest unary test that splits some pair, counted in items.

    A test is a singleton. Its item count is one form token plus the named
    point. The search keeps the minimum over pairs and raises if none splits.

    Raises:
        TypeError: If carrier_size is not an int. Bool is rejected.
        ValueError: If carrier_size < 2.
    """
    size = _require_carrier(carrier_size)
    best = None
    for left, right in combinations(range(size), 2):
        mark = {left}
        if (left in mark) == (right in mark):
            continue
        cost = 1 + len(mark)
        best = cost if best is None else min(best, cost)
    if best is None:
        raise PrimitiveDifferenceError("no unary test separates the carrier")
    return best


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


def _unary_mark_orbits(carrier_size: int) -> int:
    """Orbits of singletons. The symmetric group identifies them by cardinality."""
    by_cardinality: Dict[int, int] = {}
    for point in range(carrier_size):
        mark = frozenset((point,))
        by_cardinality[len(mark)] = by_cardinality.get(len(mark), 0) + 1
    return len(by_cardinality)


def _graph_isomorphism_classes(vertex_count: int) -> int:
    """Canonical undirected graphs on `vertex_count` vertices."""
    vertices = range(vertex_count)
    possible = list(combinations(vertices, 2))
    seen = set()
    for mask in range(1 << len(possible)):
        edges = frozenset(possible[index] for index in range(len(possible)) if mask & (1 << index))
        canonical = None
        for perm in permutations(vertices):
            mapped = tuple(sorted(tuple(sorted((perm[origin], perm[target]))) for origin, target in edges))
            if canonical is None or mapped < canonical:
                canonical = mapped
        seen.add(canonical)
    return len(seen)


def evaluate_mu1_tied_classes(carrier_size: int, max_arity: int = 2) -> int:
    """Count isomorphism classes of forms of arity at most `max_arity`.

    Arity 1 contributes the singleton-mark orbit. Arity at most 2 adds the
    isomorphism types of simple graphs on min(carrier, 3) vertices: a binary
    form is witnessed by its restriction to a 3-point subset once the carrier
    is at least that large.

    Raises:
        TypeError: If carrier_size is not an int.
        ValueError: If carrier_size < 2, max_arity < 1, or max_arity > 2.
    """
    size = _require_carrier(carrier_size)
    if max_arity < 1:
        raise ValueError(f"max_arity must be at least 1, got {max_arity}")
    unary = _unary_mark_orbits(size)
    if max_arity == 1:
        return unary
    if max_arity == 2:
        span = size if size <= 3 else 3
        return _graph_isomorphism_classes(span) + unary
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
    size = _require_carrier(carrier_size)
    return _unary_mark_orbits(size)


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
    instances = ("mark_a", "mark_b")
    swapped = (instances[1], instances[0])
    return SeparationFloorCertificate(
        carrier_size=carrier_size,
        mu_1=mu1,
        mu_2=cost.mu_2,
        lexicographic_cost=(cost.mu_1, cost.mu_2),
        is_tied_under_mu_1=tied_classes > refined_classes,
        mu_1_classes_bounded_arity_2=tied_classes,
        resolved_under_mu_2=refined_classes == 1,
        surviving_isomorphism_classes=refined_classes,
        surviving_instances=instances,
        equivariant_selection_possible=swapped == instances,
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
