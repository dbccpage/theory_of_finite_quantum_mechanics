"""CH19 conditional iid tolerance and exact arbitrary-cover minimax L1 repair.

Uses the existing generic rational LP owner; replay does not call its solver.
Compatibility means equal overlap marginals, not a global hidden-variable model.
"""

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations, product

from .obstruction import LinearProgramSolution, solve_standard_lp, verify_standard_lp
from .outcomes import Accepted, AuthorityEffect, Refused
from .native_functionals import representative_mass


@dataclass(frozen=True)
class Scenario:
    measurements: int
    outcomes: int
    contexts: tuple[tuple[int, ...], ...]
    max_sections: int = 10000
    max_cells: int = 100000

    def __post_init__(self):
        if (type(self.measurements) is not int or self.measurements <= 0
                or type(self.outcomes) is not int or self.outcomes <= 0
                or type(self.max_sections) is not int or self.max_sections < 0
                or type(self.max_cells) is not int or self.max_cells < 0
                or type(self.contexts) is not tuple or not self.contexts):
            raise ValueError("invalid finite scenario")
        for c in self.contexts:
            if (type(c) is not tuple or not c or any(type(x) is not int for x in c)
                    or any(x < 0 or x >= self.measurements for x in c)
                    or tuple(sorted(set(c))) != c):
                raise ValueError("contexts must be increasing nonempty measurement lists")
        total = 0
        for c in self.contexts:
            count = 1
            for _ in c:
                count *= self.outcomes
                if count > self.max_sections:
                    raise ValueError("declared section budget exhausted")
            total += count
            if total > self.max_sections:
                raise ValueError("declared section budget exhausted")

    def sections(self):
        return tuple(tuple(product(range(self.outcomes), repeat=len(c))) for c in self.contexts)

    def validate(self, distributions):
        if (type(distributions) is not tuple or len(distributions) != len(self.contexts)
                or any(type(p) is not tuple or len(p) != len(s)
                       or any(type(v) is not Q or v < 0 for v in p) or sum(p) != 1
                       for p, s in zip(distributions, self.sections()))):
            raise ValueError("exact normalized probabilities required on every context")

    def compatible(self, distributions):
        self.validate(distributions)
        sections = self.sections()
        for i, j in combinations(range(len(self.contexts)), 2):
            overlap = tuple(x for x in self.contexts[i] if x in self.contexts[j])
            for shared in product(range(self.outcomes), repeat=len(overlap)):
                def marginal(k):
                    indices = tuple(self.contexts[k].index(x) for x in overlap)
                    return sum((p for s, p in zip(sections[k], distributions[k])
                                if tuple(s[at] for at in indices) == shared), Q(0))
                if marginal(i) != marginal(j):
                    return False
        return True

    def repair_program(self, source):
        self.validate(source)
        sections = self.sections()
        n, k = sum(map(len, sections)), len(sections)
        width = 4 * n + 1 + k
        overlap_rows = sum(
            self.outcomes ** len(tuple(x for x in self.contexts[i] if x in self.contexts[j]))
            for i, j in combinations(range(k), 2)
        )
        total_rows = 2 * k + 2 * n + overlap_rows
        if total_rows * width > self.max_cells:
            raise ValueError("declared dense matrix cell budget exhausted")
        costs, matrix, rhs, offsets = [Q(0)] * width, [], [], []
        costs[2 * n] = Q(1)
        offset = 0
        for i, local in enumerate(source):
            offsets.append(offset)
            row = [Q(0)] * width
            row[offset:offset + len(local)] = [Q(1)] * len(local)
            matrix.append(row)
            rhs.append(Q(1))
            for j, value in enumerate(local):
                at = offset + j
                positive, negative = [Q(0)] * width, [Q(0)] * width
                positive[at], positive[n + at], positive[2 * n + 1 + at] = Q(1), Q(-1), Q(1)
                negative[at], negative[n + at], negative[3 * n + 1 + at] = Q(-1), Q(-1), Q(1)
                matrix.extend((positive, negative))
                rhs.extend((value, -value))
            row = [Q(0)] * width
            row[n + offset:n + offset + len(local)] = [Q(1)] * len(local)
            row[2 * n], row[4 * n + 1 + i] = Q(-1), Q(1)
            matrix.append(row)
            rhs.append(Q(0))
            offset += len(local)
        for i, j in combinations(range(k), 2):
            overlap = tuple(x for x in self.contexts[i] if x in self.contexts[j])
            for shared in product(range(self.outcomes), repeat=len(overlap)):
                row = [Q(0)] * width
                for context, sign in ((i, Q(1)), (j, Q(-1))):
                    indices = tuple(self.contexts[context].index(x) for x in overlap)
                    for at, section in enumerate(sections[context]):
                        if tuple(section[p] for p in indices) == shared:
                            row[offsets[context] + at] += sign
                matrix.append(row)
                rhs.append(Q(0))
        return tuple(costs), tuple(map(tuple, matrix)), tuple(rhs)

    def unpack(self, primal):
        result, offset = [], 0
        for local in self.sections():
            result.append(tuple(primal[offset:offset + len(local)]))
            offset += len(local)
        result = tuple(result)
        self.validate(result)
        return result


@dataclass(frozen=True)
class RepairReceipt:
    scenario: Scenario
    source: tuple[tuple[Q, ...], ...]
    repaired: tuple[tuple[Q, ...], ...]
    radius: Q
    optimum: LinearProgramSolution
    authority_effect: AuthorityEffect = AuthorityEffect.NONE


def verify_repair(scenario, source, receipt):
    try:
        if (not isinstance(receipt, RepairReceipt) or receipt.scenario != scenario
                or receipt.source != source or receipt.authority_effect is not AuthorityEffect.NONE):
            return False
        scenario.validate(receipt.source)
        scenario.validate(receipt.repaired)
        if not verify_standard_lp(*scenario.repair_program(source), receipt.optimum):
            return False
        repaired = scenario.unpack(receipt.optimum.primal)
        distance = max(representative_mass(a - b for a, b in zip(x, y))
                       for x, y in zip(source, repaired))
        return (receipt.repaired == repaired and scenario.compatible(repaired)
                and type(receipt.radius) is Q and receipt.radius == receipt.optimum.value == distance)
    except (ValueError, TypeError, AttributeError):
        return False


def repair(scenario: Scenario, source, max_pivots=10000):
    result = solve_standard_lp(*scenario.repair_program(source), max_pivots=max_pivots)
    if isinstance(result, Refused):
        return result
    solution = result.value
    receipt = RepairReceipt(scenario, source, scenario.unpack(solution.primal), solution.value, solution)
    if not verify_repair(scenario, source, receipt):
        raise ArithmeticError("independent repair replay failed")
    return Accepted(receipt)


def iid_l1_failure(trials: int, outcomes: int, radius: Q) -> Q:
    """Under iid categorical trials, P(||f-p||1 > r) <= (m-1)/(n r²)."""
    if (type(trials) is not int or trials <= 0 or type(outcomes) is not int or outcomes <= 0
            or type(radius) is not Q or radius <= 0):
        raise ValueError("positive exact radius, trials and outcomes required")
    if radius >= 2:
        return Q(0)
    return min(Q(1), Q(outcomes - 1, trials) / radius ** 2)


def sampling_tolerance(scenario, runs, radii):
    """Protocol counts plus DECLARED within-context iid compatible-population model."""
    if len(runs) != len(scenario.contexts) or len(radii) != len(runs):
        raise ValueError("one actual nonempty run list and radius per context required")
    for c, local in zip(scenario.contexts, runs):
        if not local or any(len(s) != len(c) or any(type(v) is not int or v < 0 or v >= scenario.outcomes
                                                  for v in s) for s in local):
            raise ValueError("invalid trial outcomes")
    failures = tuple(iid_l1_failure(len(local), len(sections), r)
                     for local, sections, r in zip(runs, scenario.sections(), radii))
    pairs = tuple((i, j, radii[i] + radii[j]) for i, j in combinations(range(len(runs)), 2))
    return pairs, min(Q(1), sum(failures, Q(0)))
