"""Genesis Primitives Category 12: Observer Inventory, Contexts & Observation Profiles.

Selected educational models related to 19L57G1 (lean4/Derivation/ObserverInventory.lean, ObsDescent.lean, code/derivation/observe.py).
Classification: Genesis Foundation Substrate.
AuthorityEffect: None.

The canonical nine-slot observer inventory, probing contexts with slot holes,
derivable profiles, observational equivalence collapse, and behavioral separation.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import isfinite
from typing import Dict, Iterator, Mapping, Optional, Sequence, Tuple

from .canonical import FrozenMap, validate_typed_fields
from .seed_and_regime import Inst, Pair, Regime

OBSERVER_SLOTS: tuple[str, ...] = (
    "carrier",
    "local_state",
    "support",
    "defect",
    "reversal",
    "closure",
    "residual",
    "maps",
    "terminal",
)

Slot = Optional[int]
Context = tuple[int, tuple[Slot, ...]]


def slot_tuples(arity: int, n_data: int) -> Iterator[tuple[Slot, ...]]:
    """All slot tuples of the given arity over n_data, with at least one hole."""
    options: list[Slot] = [None] + list(range(n_data))
    yield from product(options, repeat=arity)


def contexts(r: Regime) -> tuple[Context, ...]:
    """All probing contexts for regime r, deterministically ordered."""
    out: list[Context] = []
    for f, arity in enumerate(r.forms):
        for slots in slot_tuples(arity, r.n_data()):
            if any(s is None for s in slots):
                out.append((f, slots))
    return tuple(out)


def plug(c: Context, d: int) -> Inst:
    """Plugs datum d into every hole of context c."""
    f, slots = c
    return (f, tuple(d if s is None else s for s in slots))


def derivable(r: Regime, inst: Inst) -> bool:
    """Internal derivability: explicit instance or uniform rule coverage."""
    return inst[0] in r.rules or inst in r.insts


def profile(r: Regime, d: int) -> frozenset[Context]:
    """The observation profile of datum d: set of contexts whose plugging is derivable."""
    return frozenset(c for c in contexts(r) if derivable(r, plug(c, d)))


def profiles(r: Regime) -> tuple[frozenset[Context], ...]:
    """Profiles for all data in regime r."""
    ctxs = contexts(r)
    return tuple(frozenset(c for c in ctxs if derivable(r, plug(c, d))) for d in range(r.n_data()))


def separable(r: Regime, i: int, j: int) -> bool:
    """Two data points are separable if their observation profiles differ."""
    return profile(r, i) != profile(r, j)


def collapsed_pairs(r: Regime) -> tuple[Pair, ...]:
    """All unresolved collapsed pairs (i < j with equal profiles)."""
    profs = profiles(r)
    n = r.n_data()
    return tuple((i, j) for i in range(n) for j in range(i + 1, n) if profs[i] == profs[j])


# ===========================================================================
# Sheaf-Theoretic Contextuality & Čech Gluing Obstruction (Abramsky-Brandenburger)
# ===========================================================================


@dataclass(frozen=True)
class MeasurementContext:
    """A measurement context C representing a set of compatible/jointly observable observables."""

    observables: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.observables) is not tuple:
            raise ValueError("Observable names must form an immutable tuple")
        if any(type(o) is not str or not o for o in self.observables):
            raise ValueError("Observable names must be nonempty strings")
        if len(set(self.observables)) != len(self.observables):
            raise ValueError("A measurement context cannot repeat an observable")
        object.__setattr__(self, "observables", tuple(sorted(self.observables)))
        validate_typed_fields(self)

    def validate(self) -> None:
        """Revalidate canonical names without changing an already-keyed context."""
        if (
            type(self.observables) is not tuple
            or any(type(o) is not str or not o for o in self.observables)
            or len(set(self.observables)) != len(self.observables)
            or tuple(sorted(self.observables)) != self.observables
        ):
            raise ValueError("Context names must be canonical, distinct nonempty strings")

    def contains(self, obs: str) -> bool:
        return obs in self.observables

    def intersection(self, other: MeasurementContext) -> MeasurementContext:
        common = sorted(set(self.observables) & set(other.observables))
        return MeasurementContext(tuple(common))

    def is_subset(self, other: MeasurementContext) -> bool:
        return set(self.observables).issubset(set(other.observables))


@dataclass(frozen=True)
class LocalSection:
    """An empirical distribution / local section s_C over measurement context C.

    Assigns probabilities to joint outcome assignments. Outcomes for each observable
    are in {-1, +1}.
    """

    context: MeasurementContext
    distribution: Mapping[Tuple[int, ...], float | int]

    def validate(self) -> None:
        """Validate a normalized binary distribution, including mutable payloads."""
        if type(self.context) is not MeasurementContext:
            raise ValueError("A section requires a declared measurement context")
        MeasurementContext.validate(self.context)
        total = 0.0
        for outcome, probability in self.distribution.items():
            if (
                type(outcome) is not tuple
                or len(outcome) != len(self.context.observables)
                or any(type(x) is not int or x not in (-1, 1) for x in outcome)
            ):
                raise ValueError("Outcomes must be binary assignments of the declared arity")
            if (
                type(probability) not in (int, float)
                or not isfinite(probability)
                or probability < 0
            ):
                raise ValueError("Probabilities must be finite and nonnegative")
            total += probability
        if abs(total - 1.0) > 1e-7:
            raise ValueError("A probability section must have total mass one")

    def __post_init__(self) -> None:
        self.validate()
        object.__setattr__(self, "distribution", FrozenMap(self.distribution))
        validate_typed_fields(self)

    def marginal(self, target_obs: Sequence[str]) -> LocalSection:
        """Restricts (marginalizes) this section to a subcontext U <= C."""
        self.validate()
        target_set = set(target_obs)
        if not target_set.issubset(set(self.context.observables)):
            raise ValueError(
                f"Target observables {target_obs} not a subset of {self.context.observables}"
            )

        sub_ctx = MeasurementContext(tuple(target_obs))
        if not sub_ctx.observables:
            total_mass = sum(self.distribution.values())
            return LocalSection(sub_ctx, {(): total_mass})

        indices = [self.context.observables.index(o) for o in sub_ctx.observables]

        new_dist: Dict[Tuple[int, ...], float] = {}
        for outcome_tuple, prob in self.distribution.items():
            proj_outcome = tuple(outcome_tuple[i] for i in indices)
            new_dist[proj_outcome] = new_dist.get(proj_outcome, 0.0) + prob

        return LocalSection(sub_ctx, new_dist)

    def correlator(self, obs1: str, obs2: str) -> float:
        """Computes expected correlator <obs1 * obs2> assuming outcomes in {-1, +1}."""
        self.validate()
        if not (self.context.contains(obs1) and self.context.contains(obs2)):
            raise ValueError(
                f"Correlator requires both {obs1} and {obs2} in context {self.context.observables}"
            )
        i1 = self.context.observables.index(obs1)
        i2 = self.context.observables.index(obs2)
        val = 0.0
        for outcome_tuple, prob in self.distribution.items():
            val += outcome_tuple[i1] * outcome_tuple[i2] * prob
        return val


@dataclass
class ObserverPresheaf:
    """Presheaf of empirical observations over an observer context cover.

    Implements restriction morphisms rho^C_U, Čech 0-cycle compatibility (No-Signaling),
    and evaluates the Čech gluing obstruction (contextuality) via Fine's theorem.
    """

    contexts: Sequence[MeasurementContext]
    sections: Mapping[MeasurementContext, LocalSection]

    def _validate_sections(self) -> None:
        if len(set(self.contexts)) != len(self.contexts):
            raise ValueError("The observation cover cannot repeat a context")
        if set(self.sections) != set(self.contexts):
            raise ValueError("The declared contexts and section keys must agree")
        for context in self.contexts:
            if type(context) is not MeasurementContext:
                raise ValueError("A cover requires declared measurement contexts")
            MeasurementContext.validate(context)
            section = self.sections[context]
            if type(section) is not LocalSection or section.context != context:
                raise ValueError("Every section must belong to its declared context")
            LocalSection.validate(section)

    def restriction(
        self, from_context: MeasurementContext, to_subcontext: MeasurementContext
    ) -> LocalSection:
        """Restriction morphism rho^C_U : E(C) -> E(U)."""
        if from_context not in self.sections:
            raise KeyError(f"Context {from_context} not in presheaf")
        return self.sections[from_context].marginal(to_subcontext.observables)

    def check_cech_0_cycle_compatibility(
        self, tol: float = 1e-7
    ) -> tuple[bool, Dict[Tuple[MeasurementContext, MeasurementContext], float]]:
        """Verifies Čech 0-cycle condition: d_0 s = 0.

        For all pairs C, C' in the cover, checks that the restrictions to C cap C' agree:
            rho^C_{C cap C'}(s_C) == rho^{C'}_{C cap C'}(s_{C'})
        In physics, this is exactly the No-Signaling condition.
        Returns (is_compatible, discrepancies_dict).
        """
        self._validate_sections()
        if not isfinite(tol) or tol < 0:
            raise ValueError("Tolerance must be finite and nonnegative")
        discrepancies: Dict[Tuple[MeasurementContext, MeasurementContext], float] = {}
        is_compatible = True

        for i, c1 in enumerate(self.contexts):
            for j in range(i + 1, len(self.contexts)):
                c2 = self.contexts[j]
                inter = c1.intersection(c2)
                if not inter.observables:
                    continue
                s1_m = self.restriction(c1, inter)
                s2_m = self.restriction(c2, inter)
                all_keys = set(s1_m.distribution.keys()) | set(s2_m.distribution.keys())
                tv = 0.5 * sum(
                    abs(s1_m.distribution.get(k, 0.0) - s2_m.distribution.get(k, 0.0))
                    for k in all_keys
                )
                if tv > tol:
                    is_compatible = False
                    discrepancies[(c1, c2)] = tv

        return is_compatible, discrepancies

    def compute_chsh_correlator(
        self, a1: str = "A1", a2: str = "A2", b1: str = "B1", b2: str = "B2"
    ) -> float:
        """Evaluates S = <A1 B1> + <A1 B2> + <A2 B1> - <A2 B2>."""
        c_a1b1 = self._find_context((a1, b1))
        c_a1b2 = self._find_context((a1, b2))
        c_a2b1 = self._find_context((a2, b1))
        c_a2b2 = self._find_context((a2, b2))

        e_a1b1 = self.sections[c_a1b1].correlator(a1, b1)
        e_a1b2 = self.sections[c_a1b2].correlator(a1, b2)
        e_a2b1 = self.sections[c_a2b1].correlator(a2, b1)
        e_a2b2 = self.sections[c_a2b2].correlator(a2, b2)

        return e_a1b1 + e_a1b2 + e_a2b1 - e_a2b2

    def cech_gluing_obstruction(
        self, a1: str = "A1", a2: str = "A2", b1: str = "B1", b2: str = "B2"
    ) -> float:
        """Largest of all eight CHSH violations in the binary 2x2 cover.

        This scalar is a Bell inequality diagnostic, not a computed Čech
        cohomology class. Compatibility is checked separately for gluing.
        The historical method name is retained for callers.
        """
        self._validate_sections()
        if len({a1, a2, b1, b2}) != 4:
            raise ValueError("The binary 2x2 scenario needs four distinct observables")
        expected = set(bell_chsh_contexts(a1, a2, b1, b2))
        if set(self.contexts) != expected:
            raise ValueError("CHSH gluing is implemented only for the complete binary 2x2 cover")
        pairs = ((a1, b1), (a1, b2), (a2, b1), (a2, b2))
        correlations = tuple(
            self.sections[self._find_context(pair)].correlator(*pair) for pair in pairs
        )
        largest = max(
            sum(sign * value for sign, value in zip(signs, correlations))
            for signs in product((-1, 1), repeat=4)
            if signs[0] * signs[1] * signs[2] * signs[3] == -1
        )
        return max(0.0, largest - 2.0)

    def has_global_gluing(
        self, a1: str = "A1", a2: str = "A2", b1: str = "B1", b2: str = "B2", tol: float = 1e-7
    ) -> bool:
        """Tolerance checks for binary 2x2 probability-gluing conditions.

        This uses the finite marginal-polytope characterization; it is not
        a sheaf axiom verifier on an arbitrary observation cover.
        A positive tolerance permits small exact violations; this is not a
        certified exact feasibility decision or a distance-to-polytope bound.
        """
        compatible, _ = self.check_cech_0_cycle_compatibility(tol)
        violation = self.cech_gluing_obstruction(a1, a2, b1, b2)
        return compatible and violation <= tol

    def _find_context(self, pair: Tuple[str, str]) -> MeasurementContext:
        target = tuple(sorted(pair))
        for c in self.contexts:
            if c.observables == target:
                return c
        raise KeyError(f"No context found covering observables {pair}")


def bell_chsh_contexts(
    a1: str = "A1", a2: str = "A2", b1: str = "B1", b2: str = "B2"
) -> tuple[MeasurementContext, ...]:
    """Canonical 4-context cover for the bipartite Bell-CHSH test."""
    return (
        MeasurementContext((a1, b1)),
        MeasurementContext((a1, b2)),
        MeasurementContext((a2, b1)),
        MeasurementContext((a2, b2)),
    )


def make_bipartite_section(c: MeasurementContext, corr: float) -> LocalSection:
    """Creates an unbiased bipartite section over context c with correlation E in [-1, 1].

    P(+, +) = P(-, -) = (1 + E) / 4
    P(+, -) = P(-, +) = (1 - E) / 4
    Marginals are strictly uniform (1/2, 1/2), ensuring exact Čech 0-cycle compatibility (No-Signaling).
    """
    if not isfinite(corr) or not -1.0 <= corr <= 1.0 or len(c.observables) != 2:
        raise ValueError("A bipartite section needs two observables and correlation in [-1, 1]")
    p_eq = (1.0 + corr) / 4.0
    p_neq = (1.0 - corr) / 4.0
    dist = {
        (1, 1): p_eq,
        (1, -1): p_neq,
        (-1, 1): p_neq,
        (-1, -1): p_eq,
    }
    return LocalSection(context=c, distribution=dist)


def classical_local_hidden_variable_fixture() -> ObserverPresheaf:
    """Deterministic local hidden variable model: A1=1, A2=1, B1=1, B2=1.

    All correlators E = +1. S_CHSH = 1 + 1 + 1 - 1 = 2.0.
    Čech 0-cycle: Compatible (No-Signaling holds).
    Čech gluing obstruction gamma = 0.0 (Global gluing exists).
    """
    ctxs = bell_chsh_contexts()
    sections: Dict[MeasurementContext, LocalSection] = {}
    for c in ctxs:
        sections[c] = LocalSection(
            context=c,
            distribution={(1, 1): 1.0, (1, -1): 0.0, (-1, 1): 0.0, (-1, -1): 0.0},
        )
    return ObserverPresheaf(contexts=ctxs, sections=sections)


def rational_pythagorean_bell_fixture() -> ObserverPresheaf:
    """Exact rational Pythagorean Bell model matching paper T059 / p208b / 19L57G1.

    Correlators: E(A1, B1) = 4/5 = 0.8, E(A1, B2) = 4/5 = 0.8, E(A2, B1) = 4/5 = 0.8, E(A2, B2) = -2/5 = -0.4.
    S_CHSH = 0.8 + 0.8 + 0.8 - (-0.4) = 2.8 = 14/5.
    Čech 0-cycle: Strictly compatible (uniform marginals, No-Signaling holds).
    Čech gluing obstruction gamma = 2.8 - 2.0 = 0.8 = 4/5 > 0 (Contextual: global gluing obstructed).
    """
    ctxs = bell_chsh_contexts()
    c_a1b1, c_a1b2, c_a2b1, c_a2b2 = ctxs
    sections = {
        c_a1b1: make_bipartite_section(c_a1b1, 0.8),
        c_a1b2: make_bipartite_section(c_a1b2, 0.8),
        c_a2b1: make_bipartite_section(c_a2b1, 0.8),
        c_a2b2: make_bipartite_section(c_a2b2, -0.4),
    }
    return ObserverPresheaf(contexts=ctxs, sections=sections)


def pr_box_fixture() -> ObserverPresheaf:
    """Popescu-Rohrlich superquantum box fixture.

    Correlators: E(A1, B1) = 1.0, E(A1, B2) = 1.0, E(A2, B1) = 1.0, E(A2, B2) = -1.0.
    S_CHSH = 1.0 + 1.0 + 1.0 - (-1.0) = 4.0.
    Čech 0-cycle: Strictly compatible (uniform marginals).
    Čech gluing obstruction gamma = 4.0 - 2.0 = 2.0 (Maximal algebraic contextuality).
    """
    ctxs = bell_chsh_contexts()
    c_a1b1, c_a1b2, c_a2b1, c_a2b2 = ctxs
    sections = {
        c_a1b1: make_bipartite_section(c_a1b1, 1.0),
        c_a1b2: make_bipartite_section(c_a1b2, 1.0),
        c_a2b1: make_bipartite_section(c_a2b1, 1.0),
        c_a2b2: make_bipartite_section(c_a2b2, -1.0),
    }
    return ObserverPresheaf(contexts=ctxs, sections=sections)
