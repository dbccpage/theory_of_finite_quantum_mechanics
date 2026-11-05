"""Conditional finite clock and Boolean-valuation representation theorems.

These exact witnesses concern declared finite chains and full Boolean event
algebras. They make no stochastic, continuum, or physical-clock inference.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .exact import as_fraction


@dataclass(frozen=True)
class ChainClock:
    """A clock coupled to every edge of a finite occurrence chain.

    Calibration is a positive scale; error budgets are nonnegative edgewise
    bounds. The unit and recurrence/coupling interpretation are external data.
    """

    durations: tuple[Fraction, ...]
    readings: tuple[Fraction, ...]
    calibration: Fraction
    error_budgets: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        durations = tuple(as_fraction(x) for x in self.durations)
        readings = tuple(as_fraction(x) for x in self.readings)
        budgets = tuple(as_fraction(x) for x in self.error_budgets)
        calibration = as_fraction(self.calibration)
        if len(readings) != len(durations) + 1 or len(budgets) != len(durations):
            raise ValueError("a clock needs one reading per vertex and one budget per edge")
        if calibration <= 0 or any(x <= 0 for x in durations) or any(x < 0 for x in budgets):
            raise ValueError("positive durations/calibration and nonnegative budgets required")
        if any(
            abs(calibration * (readings[i + 1] - readings[i]) - duration) > budgets[i]
            for i, duration in enumerate(durations)
        ):
            raise ValueError("edge coupling exceeds its declared error budget")
        object.__setattr__(self, "durations", durations)
        object.__setattr__(self, "readings", readings)
        object.__setattr__(self, "calibration", calibration)
        object.__setattr__(self, "error_budgets", budgets)

    def interval_bound(self, start: int, stop: int) -> tuple[Fraction, Fraction]:
        """Return actual endpoint-duration discrepancy and its additive bound.

        Proof: sum the edge residuals, telescope readings, then use the triangle
        inequality. For start=stop the empty sum and discrepancy are both zero.
        """
        if type(start) is not int or type(stop) is not int or not 0 <= start <= stop <= len(self.durations):
            raise ValueError("interval endpoints must be ordered chain vertex indices")
        duration = sum(self.durations[start:stop], Fraction(0))
        discrepancy = abs(self.calibration * (self.readings[stop] - self.readings[start]) - duration)
        return discrepancy, sum(self.error_budgets[start:stop], Fraction(0))

    def coarsen(self, cuts: tuple[int, ...]) -> ChainClock:
        """Restrict a refined clock to partition endpoints, preserving adequacy.

        Each coarse duration/budget is the sum within its block. Thus every
        coarse edge satisfies interval_bound; coarse and fine interval budgets
        and endpoint discrepancies coincide. This proves stability for every
        refinement with preserved block durations, calibration, endpoint
        readings, and a fine-budget sum no larger than the coarse budget.
        """
        if (
            not cuts
            or any(type(cut) is not int for cut in cuts)
            or cuts[0] != 0
            or cuts[-1] != len(self.durations)
            or any(a >= b for a, b in zip(cuts, cuts[1:]))
        ):
            raise ValueError("cuts must be a strict endpoint-covering partition")
        return ChainClock(
            tuple(sum(self.durations[a:b], Fraction(0)) for a, b in zip(cuts, cuts[1:])),
            tuple(self.readings[cut] for cut in cuts),
            self.calibration,
            tuple(sum(self.error_budgets[a:b], Fraction(0)) for a, b in zip(cuts, cuts[1:])),
        )


@dataclass(frozen=True)
class AtomicValuation:
    """A nonnegative rational measure on the full powerset of numbered atoms."""

    masses: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        masses = tuple(as_fraction(x) for x in self.masses)
        if any(x < 0 for x in masses):
            raise ValueError("atomic masses must be nonnegative")
        object.__setattr__(self, "masses", masses)

    def event_mass(self, mask: int) -> Fraction:
        if type(mask) is not int or not 0 <= mask < 1 << len(self.masses):
            raise ValueError("event mask is outside the full Boolean algebra")
        return sum((mass for i, mass in enumerate(self.masses) if mask & (1 << i)), Fraction(0))

    @classmethod
    def from_event_table(cls, values: tuple[Fraction, ...]) -> AtomicValuation:
        """Check and reconstruct a full Boolean valuation, uniquely.

        Hypotheses: v(empty)=0, nonnegativity, finite disjoint additivity on
        every event. Equivalent check: v(A)=sum(i in A)v({i}) for every A.
        Necessity follows by induction on |A|; sufficiency follows because
        disjoint events contain disjoint atoms; uniqueness follows on singletons.
        No powerset completion of a partial event family is asserted.
        """
        size = len(values)
        if size == 0 or size & (size - 1):
            raise ValueError("a full event table has power-of-two length")
        exact = tuple(as_fraction(x) for x in values)
        valuation = cls(tuple(exact[1 << i] for i in range(size.bit_length() - 1)))
        if any(value != valuation.event_mass(mask) for mask, value in enumerate(exact)):
            raise ValueError("event table is not a normalized disjoint-additive valuation")
        return valuation

    def pushforward(self, atom_map: tuple[int, ...], target_size: int) -> AtomicValuation:
        """Coarsen atoms by a total map; preserve every pullback event mass.

        Target mass j is the sum over its fiber. Disjoint fibers partition each
        pullback event, proving v'(B)=v(f^-1(B)). Empty fibers have zero mass.
        """
        if (
            type(target_size) is not int
            or target_size < 0
            or len(atom_map) != len(self.masses)
            or any(type(j) is not int or not 0 <= j < target_size for j in atom_map)
        ):
            raise ValueError("atom map must be total and inside the target carrier")
        masses = [Fraction(0) for _ in range(target_size)]
        for mass, target in zip(self.masses, atom_map):
            masses[target] += mass
        return AtomicValuation(tuple(masses))

    def event_distance(self, other: AtomicValuation) -> Fraction:
        """Exact sup_A |v(A)-w(A)|; stable under every common pushforward.

        Write delta_i=v_i-w_i. Maximal positive event sum selects all positive
        delta_i, and minimal event sum selects all negative delta_i. Hence the
        supremum is max(sum(delta_i>0), sum(-delta_i<0)). Grouping into fibers
        cannot increase either sum (triangle inequality). With equal total
        masses the two sums agree, giving half the l1 distance.
        """
        if len(self.masses) != len(other.masses):
            raise ValueError("valuation carriers must coincide")
        deltas = tuple(a - b for a, b in zip(self.masses, other.masses))
        return max(
            sum((delta for delta in deltas if delta > 0), Fraction(0)),
            sum((-delta for delta in deltas if delta < 0), Fraction(0)),
        )


@dataclass(frozen=True)
class BooleanEventValuation:
    """A checked nonnegative additive valuation on a finite Boolean subalgebra.

    Events are bit masks on a declared carrier. The algebra's atoms, rather
    than individual carrier points, have uniquely determined masses. Each
    atom is the equivalence class of points with the same event-membership
    signature; finite complement/intersection closure makes that class an
    event. Every event is its disjoint union of atoms, which proves the unique
    atomic representation without assuming that singletons are measurable.
    """

    size: int
    events: tuple[int, ...]
    values: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        if type(self.size) is not int or self.size < 0:
            raise ValueError("carrier size must be a nonnegative integer")
        events = tuple(self.events)
        values = tuple(as_fraction(x) for x in self.values)
        full = (1 << self.size) - 1
        if len(events) != len(values) or len(set(events)) != len(events):
            raise ValueError("exactly one value is required for every declared event")
        if any(type(e) is not int or not 0 <= e <= full for e in events):
            raise ValueError("event masks must belong to the declared carrier")
        table = dict(zip(events, values))
        if 0 not in table or full not in table:
            raise ValueError("Boolean algebra must contain empty and full events")
        if any((full ^ a) not in table or (a | b) not in table for a in events for b in events):
            raise ValueError("events must be closed under complement and union")
        if table[0] != 0 or any(value < 0 for value in values):
            raise ValueError("valuation must vanish on empty and be nonnegative")
        if any(table[a | b] != table[a] + table[b] for a in events for b in events if a & b == 0):
            raise ValueError("valuation must be additive on disjoint events")
        object.__setattr__(self, "events", events)
        object.__setattr__(self, "values", values)

    def atoms(self) -> tuple[int, ...]:
        groups: dict[tuple[bool, ...], int] = {}
        for i in range(self.size):
            signature = tuple(bool(event & (1 << i)) for event in self.events)
            groups[signature] = groups.get(signature, 0) | (1 << i)
        return tuple(sorted(groups.values()))

    def atomic_representation(self) -> AtomicValuation:
        table = dict(zip(self.events, self.values))
        return AtomicValuation(tuple(table[atom] for atom in self.atoms()))

    def atom_event(self, event: int) -> int:
        if type(event) is not int or event not in self.events:
            raise ValueError("event is not measurable in the declared algebra")
        return sum(1 << i for i, atom in enumerate(self.atoms()) if atom & event)

    def singleton_extension(self, choose_last: bool = False) -> AtomicValuation:
        """Exhibit full-powerset extensions, without claiming they are unique.

        Put each atom's mass on its first or last point. Their restrictions
        agree with the original valuation because each measurable event is a
        union of whole atoms. A positive nonsingleton atom gives two distinct
        extensions, witnessing necessity in singleton_extension_is_unique.
        """
        if type(choose_last) is not bool:
            raise TypeError("extension choice must be a Boolean")
        table = dict(zip(self.events, self.values))
        masses = [Fraction(0) for _ in range(self.size)]
        for atom in self.atoms():
            point = atom.bit_length() - 1 if choose_last else (atom & -atom).bit_length() - 1
            masses[point] = table[atom]
        return AtomicValuation(tuple(masses))

    def singleton_extension_is_unique(self) -> bool:
        """Uniqueness iff every nonsingleton algebra atom has mass zero.

        Sufficiency: nonnegative masses summing to zero all vanish; singleton
        masses are fixed. Necessity: first/last concentration gives distinct
        extensions on any positive nonsingleton atom.
        """
        table = dict(zip(self.events, self.values))
        return all(atom.bit_count() == 1 or table[atom] == 0 for atom in self.atoms())
