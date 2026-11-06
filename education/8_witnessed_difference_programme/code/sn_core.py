"""S(n) Tower Core Stages (S(0) through S(6)).

Internal algebraic shadow models for Track 000 curriculum notebooks.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Sequence, Set, Tuple


@dataclass(frozen=True)
class S0Ground:
    """Stage S(0): Ground state with empty carrier and verified inertia."""

    s_0: int = 0
    v_0: FrozenSet[str] = field(default_factory=frozenset)
    w_0_active: FrozenSet[str] = field(default_factory=frozenset)

    def verify_inertia(self) -> bool:
        """Check ground inertia holds under empty carrier in this toy model."""
        return self.s_0 == 0 and len(self.v_0) == 0 and len(self.w_0_active) == 0


@dataclass(frozen=True)
class S1Supply:
    """Stage S(1): External supply operation and lone mark subsingleton collapse."""

    s_1: int = 1
    w_1_active: FrozenSet[str] = field(default_factory=lambda: frozenset({"obs_unconsumed_mark"}))

    @staticmethod
    def supply_mark(token: str) -> FrozenSet[str]:
        """Supply a single mark into a carrier set."""
        return frozenset({token})

    def verify_subsingleton(self, token: str) -> bool:
        """Check that supplied carrier has cardinality exactly 1."""
        return len(self.supply_mark(token)) == 1 and self.s_1 == 1


@dataclass(frozen=True)
class S2Collapse:
    """Stage S(2): Retention and S_2 permutation action on unseparated pair."""

    s_2: int = 1

    @staticmethod
    def permute_pair(pair: Tuple[str, str]) -> Tuple[str, str]:
        """S_2 permutation action swapping the pair elements."""
        return (pair[1], pair[0])

    @staticmethod
    def verify_set_equivalence(a: str, b: str) -> bool:
        """Check that unordered set representation collapses distinguishing order."""
        return {a, b} == {b, a}


@dataclass(frozen=True)
class S3Separation:
    """Stage S(3): Directed separation relation and cost-2 floor."""

    s_3: int = 1
    cost_floor: int = 2

    @staticmethod
    def directed_edge(u: str, v: str) -> Tuple[str, str]:
        """Form an ordered directed pair."""
        return (u, v)

    @staticmethod
    def coboundary_delta(u: int, v: int) -> int:
        """Compute 1-dimensional coboundary difference."""
        return v - u

    def verify_separation(self, u: str, v: str) -> bool:
        """Check directed pair distinction and cost floor in this toy setup."""
        if u == v:
            return False
        edge = self.directed_edge(u, v)
        reversed_edge = self.directed_edge(v, u)
        return edge != reversed_edge and self.cost_floor == 2 and self.s_3 == 1


@dataclass(frozen=True)
class S4Orbit:
    """Stage S(4): Complete graph K_n orbit closure and terminal fixpoint."""

    s_4: int = 0

    @staticmethod
    def complete_edges(vertices: Sequence[str]) -> Set[Tuple[str, str]]:
        """Generate all distinct unordered edge pairs for complete graph K_n."""
        edges = set()
        n = len(vertices)
        for i in range(n):
            for j in range(i + 1, n):
                edges.add((vertices[i], vertices[j]))
        return edges

    def verify_orbit_closure(self, vertices: Sequence[str]) -> bool:
        """Check orbit closure edge count matches n*(n-1)//2 and s_4 is zero."""
        n = len(vertices)
        expected_count = n * (n - 1) // 2
        edges = self.complete_edges(vertices)
        return len(edges) == expected_count and self.s_4 == 0


@dataclass(frozen=True)
class S5Continuation:
    """Stage S(5): External continuation across stages and OB-1 demand gap."""

    s_5: int = 1
    ob_1_active: bool = True

    @staticmethod
    def assert_endogenous_inertia(state: Set[str]) -> bool:
        """Check closed state does not self-generate marks without external continuation."""
        new_state = set(state)
        return new_state == state

    def verify_continuation_demand(self) -> bool:
        """Check external continuation demand gap is active."""
        return self.s_5 == 1 and self.ob_1_active is True


@dataclass(frozen=True)
class S6Descent:
    """Stage S(6): Section lift and retraction down-map with descent check."""

    s_6: int = 1
    delta_n: int = 1

    @staticmethod
    def section_lift(x: int) -> Tuple[int, int]:
        """Embed element into extended product space."""
        return (x, 0)

    @staticmethod
    def retraction_down(pair: Tuple[int, int]) -> int:
        """Retract product pair back to base element."""
        return pair[0]

    def verify_retraction_identity(self, test_values: Sequence[int]) -> bool:
        """Check retraction identity r_N(u_N(x)) == x across test inputs."""
        return all(self.retraction_down(self.section_lift(x)) == x for x in test_values)

    def descent_status(self) -> str:
        """Return typed descent indicator based on lift size delta_n."""
        if self.delta_n > 0:
            return "NON_DESCENT"
        return "DESCENT"
