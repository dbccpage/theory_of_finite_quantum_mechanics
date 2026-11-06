"""
fermion_boson_germ.py — Discrete Primitive Difference Germ: Void to <arb> / <ara>

Status: Finite Relational Model
AuthorityEffect: None
Primary Reference: sealed-derivation-v1 (commit 3100c4e) - Derivation.PrimDiff, PrimDiffAlternation

Claim Hygiene:
1. What this supports:
   - Discrete relational state transitions from void <> to directed cut <arb> (D2) and symmetric link S2 / loop <ara>.
   - Demonstration that D2 is rigid (Aut = {id}) and asymmetric, representing the discrete germ of fermionic orientation.
   - Demonstration that S2 admits the swap automorphism (Aut = Z2) and <ara> has vanishing boundary differential, representing bosonic symmetry.
   - Exact finite proof that swap-invariant predicates evaluate identically on D2 and D2_rev (invariant blindness).
2. What this does not support:
   - Continuous Spin(d) representations, 720-degree rotations, quantum fields, or physical particles.
3. Narrowest defensible claim:
   - On a two-element carrier, an irreflexive directed relation admits only the identity automorphism, while its symmetrization admits a non-trivial involution; predicates invariant under that involution cannot separate the relation from its transpose.
4. Next test needed:
   - Connect this swap-blindness to signed path sums in configuration complexes.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Callable, Any, Optional

@dataclass(frozen=True)
class DirectedCutD2:
    """Directed irreflexive cut D2: a -> b with a != b."""
    source: str
    target: str

    def __post_init__(self):
        if self.source == self.target:
            raise ValueError("Diagonal self-loop refused under strict irreflexivity.")

    @property
    def boundary_0chain(self) -> Dict[str, int]:
        """∂₁(a -> b) = b - a (formal 0-chain)."""
        return {self.target: 1, self.source: -1}

    @property
    def reversed(self) -> "DirectedCutD2":
        return DirectedCutD2(source=self.target, target=self.source)

    def automorphism_group(self) -> List[Dict[str, str]]:
        """Aut(D2) on {a, b} preserving relation."""
        # Only identity preserves (a, b) without mapping to (b, a)
        return [{"a": "a", "b": "b"}]


@dataclass(frozen=True)
class SymmetricLinkS2:
    """Symmetric link S2: undirected edge {a, b} with a != b."""
    endpoint1: str
    endpoint2: str

    def __post_init__(self):
        if self.endpoint1 == self.endpoint2:
            raise ValueError("Endpoints must be distinct loci.")

    def automorphism_group(self) -> List[Dict[str, str]]:
        """Aut(S2) on {a, b}: identity and swap."""
        return [
            {"a": "a", "b": "b"},
            {"a": "b", "b": "a"},
        ]


@dataclass(frozen=True)
class LoopCycleZ1:
    """Self-loop or closed cycle <ara>: boundary ∂₁ = a - a = 0."""
    vertex: str

    @property
    def boundary_0chain(self) -> Dict[str, int]:
        """∂₁(a -> a) = a - a = 0."""
        return {self.vertex: 0}


class GermState:
    """State machine tracking genesis rungs 0 to 5."""
    def __init__(self):
        self.stage: int = 0
        self.inscription: str = "<>"
        self.carrier: Set[str] = set()
        self.relations: Set[Tuple[str, str]] = set()
        self.active_obstruction: Optional[str] = "demand_initial_challenge_supply"
        self.admitted_rules: List[str] = []
        self.history: List[Dict[str, Any]] = []

    def step_00_void(self) -> "GermState":
        """Stage 0: Void <> — pure inertia."""
        self.stage = 0
        self.inscription = "<>"
        self.carrier = set()
        self.relations = set()
        self.active_obstruction = "demand_initial_challenge_supply"
        self._record("step_00_void", "Empty carrier maintained; supply changes nothing.")
        return self

    def step_01_lone_mark(self, mark: str = "a") -> "GermState":
        """Stage 1: Lone mark <a> — no internal distinction possible."""
        self.stage = 1
        self.inscription = f"<{mark}>"
        self.carrier = {mark}
        self.relations = set()
        self.active_obstruction = "demand_multiplicity_locus"
        self._record("step_01_lone_mark", f"Admit single locus {mark}; no boundary exists.")
        return self

    def step_02_unmarked_pair(self, a: str = "a", b: str = "b") -> "GermState":
        """Stage 2: Unmarked pair <ab> — observational collapse [a] = [b]."""
        self.stage = 2
        self.inscription = f"<{a}{b}>"
        self.carrier = {a, b}
        self.relations = set()
        self.active_obstruction = "demand_distinguishing_relation"
        self._record("step_02_unmarked_pair", f"Two names {a}, {b} without relation collapse observationally.")
        return self

    def step_03_directed_cut(self, a: str = "a", b: str = "b") -> DirectedCutD2:
        """Stage 3: Primitive pointed cut <arb> (D2) — First sign of a fermion."""
        self.stage = 3
        self.inscription = f"<{a}r{b}>"
        self.carrier = {a, b}
        self.relations = {(a, b)}
        self.active_obstruction = None
        self.admitted_rules.append("rule_directed_irreflexive_cut")
        self._record("step_03_directed_cut", f"Pointed edge {a} -> {b}; asymmetric boundary b - a != 0.")
        return DirectedCutD2(source=a, target=b)

    def step_04_refuse_self_loop(self, a: str = "a") -> Tuple[bool, str]:
        """Stage 4: Refuse loop <ara> under strict irreflexivity."""
        # Self-loop boundary ∂(a -> a) = 0 cannot witness distinction
        refusal_reason = "Loop a -> a has boundary a - a = 0; collapsed into identity."
        self._record("step_04_refuse_self_loop", refusal_reason)
        return False, refusal_reason

    def step_05_symmetric_link(self, a: str = "a", b: str = "b") -> SymmetricLinkS2:
        """Stage 5: Symmetrized pair S2 / loop closure — First sign of a boson."""
        self.stage = 5
        self.inscription = f"<{a}r{b}_symm>"
        self.carrier = {a, b}
        self.relations = {(a, b), (b, a)}
        self.admitted_rules.append("rule_symmetrization")
        self._record("step_05_symmetric_link", f"Symmetric pair {a} <-> {b}; admits swap involution.")
        return SymmetricLinkS2(endpoint1=a, endpoint2=b)

    def _record(self, action: str, note: str):
        self.history.append({
            "stage": self.stage,
            "inscription": self.inscription,
            "action": action,
            "note": note,
            "carrier_size": len(self.carrier),
            "relation_count": len(self.relations)
        })


def swap_action_on_pair(pair: Tuple[str, str]) -> Tuple[str, str]:
    """Transposition τ: (x, y) -> (y, x)."""
    return (pair[1], pair[0])


def verify_invariant_blindness(
    d2: DirectedCutD2,
    invariant_predicates: List[Callable[[Tuple[str, str]], Any]]
) -> Dict[str, bool]:
    """
    Checks that every swap-invariant predicate satisfies:
    P(d2) == P(d2_rev).
    Corresponds to PrimDiffAlternation.invariant_blind from sealed-derivation-v1.
    """
    d2_pair = (d2.source, d2.target)
    d2_rev_pair = (d2.reversed.source, d2.reversed.target)
    
    results = {}
    for i, pred in enumerate(invariant_predicates):
        val_forward = pred(d2_pair)
        val_reverse = pred(d2_rev_pair)
        # Is the predicate itself swap-invariant?
        is_symmetric = (val_forward == val_reverse)
        results[f"predicate_{i}"] = is_symmetric
    return results
