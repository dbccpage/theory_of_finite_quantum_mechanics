"""Exact finite Paper031 (C,D,G,R,T) policy observers, without authority.

G is a declared finite transformation group, R is a separate linear repair
operator, and the weighted-l1 norm is an additional declared bridge. Defects
are computed from actual carrier payloads and comparisons before certificates
are checked. SourceCustody is metadata; it does not authenticate source bytes.
"""
import json
from dataclasses import dataclass, fields, is_dataclass, replace
from fractions import Fraction
from hashlib import sha256

from .obstruction import MatrixQuotientCertificate, verify_matrix_certificate
from .outcomes import Accepted
from .semantic_legacy_observers import SourceCustody


@dataclass(frozen=True)
class PolicyCarrier:
    names: tuple
    coordinates: tuple
    values: tuple


@dataclass(frozen=True)
class PolicyComparisonDomain:
    names: tuple
    pairs: tuple
    restrictions: tuple


@dataclass(frozen=True)
class SignedPermutation:
    image: tuple
    signs: tuple

    @classmethod
    def identity(cls, size):
        return cls(tuple(range(size)), (1,) * size)

    def valid(self, size):
        return (_permutation(self.image, size) and type(self.signs) is tuple
                and len(self.signs) == size
                and all(type(s) is int and s in (-1, 1) for s in self.signs))

    def apply(self, vector):
        result = [Fraction(0)] * len(vector)
        for i, value in enumerate(vector):
            result[self.image[i]] = self.signs[i] * value
        return tuple(result)

    def then(self, next_):
        return SignedPermutation(tuple(next_.image[j] for j in self.image),
                                 tuple(self.signs[i] * next_.signs[j]
                                       for i, j in enumerate(self.image)))


@dataclass(frozen=True)
class PolicyGaugeAction:
    states: tuple
    comparisons: tuple
    defects: SignedPermutation
    repairs: SignedPermutation

    @classmethod
    def identity(cls, states, comparisons, defects, repairs):
        return cls(tuple(range(states)), tuple(range(comparisons)),
                   SignedPermutation.identity(defects), SignedPermutation.identity(repairs))

    def then(self, next_):
        return PolicyGaugeAction(tuple(next_.states[j] for j in self.states),
                                 tuple(next_.comparisons[j] for j in self.comparisons),
                                 self.defects.then(next_.defects), self.repairs.then(next_.repairs))


@dataclass(frozen=True)
class PolicyRepairOperator:
    coordinates: tuple
    map: tuple


@dataclass(frozen=True)
class PolicyTerminalRules:
    permitted_statuses: frozenset
    tolerance: Fraction
    within_tolerance: str
    above_tolerance: str


@dataclass(frozen=True)
class PolicyObserverProblem:
    carrier: PolicyCarrier
    comparison_domain: PolicyComparisonDomain
    gauge_group: tuple
    repair: PolicyRepairOperator
    terminal_rules: PolicyTerminalRules
    norm_weights: tuple
    source: SourceCustody


def _names(names, allow_empty=False):
    return (type(names) is tuple and (allow_empty or bool(names))
            and all(isinstance(n, str) and n for n in names)
            and len(set(names)) == len(names))


def _permutation(values, size):
    return (type(values) is tuple and len(values) == size
            and all(type(i) is int for i in values) and set(values) == set(range(size)))


def _matrix(matrix, rows, columns):
    return (type(matrix) is tuple and len(matrix) == rows
            and all(type(row) is tuple and len(row) == columns
                    and all(type(q) is Fraction for q in row) for row in matrix))


def _apply(matrix, vector):
    return tuple(sum((a*b for a, b in zip(row, vector)), Fraction(0)) for row in matrix)


def _wire(value):
    if type(value) is Fraction:
        return [value.numerator, value.denominator]
    if is_dataclass(value):
        return {field.name: _wire(getattr(value, field.name)) for field in fields(value)}
    if type(value) is tuple:
        return [_wire(item) for item in value]
    if type(value) is frozenset:
        return sorted(value)
    if type(value) in (str, int, bool):
        return value
    raise ValueError("noncanonical policy payload")


def _digest(kind, value):
    return sha256(json.dumps({"kind": kind, "payload": _wire(value)}, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def _validate(problem):
    if not isinstance(problem, PolicyObserverProblem) or not isinstance(problem.source, SourceCustody):
        raise ValueError("actual policy problem and declared source binding required")
    c, d, r, t = problem.carrier, problem.comparison_domain, problem.repair, problem.terminal_rules
    if not all(isinstance(value, expected) for value, expected in (
            (c, PolicyCarrier), (d, PolicyComparisonDomain), (r, PolicyRepairOperator),
            (t, PolicyTerminalRules))):
        raise ValueError("all five typed source fields required")
    n, m, queries, repairs = len(c.names), len(c.coordinates), len(d.names), len(r.coordinates)
    if not _names(c.names) or not _names(c.coordinates) or not _matrix(c.values, n, m):
        raise ValueError("typed nonempty actual carrier required")
    if (not _names(d.names) or type(d.pairs) is not tuple or len(d.pairs) != queries
            or any(type(pair) is not tuple or len(pair) != 2
                   or any(type(i) is not int or not 0 <= i < n for i in pair) for pair in d.pairs)
            or type(d.restrictions) is not tuple or len(d.restrictions) != queries
            or any(not _matrix(matrix, m, m) for matrix in d.restrictions)):
        raise ValueError("complete typed comparison domain required")
    if not _names(r.coordinates, allow_empty=True) or not _matrix(r.map, m, repairs):
        raise ValueError("explicit linear admissible repair operator required")
    if (type(problem.norm_weights) is not tuple or len(problem.norm_weights) != m
            or any(type(w) is not Fraction or w <= 0 for w in problem.norm_weights)):
        raise ValueError("independent positive weighted-l1 norm bridge required")
    if (type(t.permitted_statuses) is not frozenset or not t.permitted_statuses
            or any(not isinstance(s, str) or not s for s in t.permitted_statuses)
            or t.within_tolerance not in t.permitted_statuses
            or t.above_tolerance not in t.permitted_statuses
            or type(t.tolerance) is not Fraction or t.tolerance < 0):
        raise ValueError("complete permitted mathematical terminal rule required")
    defects = tuple(tuple(a-b for a, b in zip(_apply(matrix, c.values[right]), c.values[left]))
                    for (left, right), matrix in zip(d.pairs, d.restrictions))
    if type(problem.gauge_group) is not tuple:
        raise ValueError("declared finite gauge group required")
    for g in problem.gauge_group:
        if (not isinstance(g, PolicyGaugeAction) or not _permutation(g.states, n)
                or not _permutation(g.comparisons, queries)
                or not isinstance(g.defects, SignedPermutation) or not g.defects.valid(m)
                or not isinstance(g.repairs, SignedPermutation) or not g.repairs.valid(repairs)):
            raise ValueError("gauge actions must be typed simultaneous signed permutations")
        for i, (left, right) in enumerate(d.pairs):
            j = g.comparisons[i]
            if d.pairs[j] != (g.states[left], g.states[right]) or g.defects.apply(defects[i]) != defects[j]:
                raise ValueError("gauge must preserve actual compared states and defects")
        for i in range(m):
            if problem.norm_weights[i] != problem.norm_weights[g.defects.image[i]]:
                raise ValueError("gauge must preserve the independently supplied norm")
            for j in range(repairs):
                if (g.defects.signs[i] * r.map[i][j]
                        != r.map[g.defects.image[i]][g.repairs.image[j]] * g.repairs.signs[j]):
                    raise ValueError("gauge/repair intertwiner P d0 = d0 A failed")
    identity = PolicyGaugeAction.identity(n, queries, m, repairs)
    if (identity not in problem.gauge_group or len(set(problem.gauge_group)) != len(problem.gauge_group)
            or any(g.then(h) not in problem.gauge_group for g in problem.gauge_group for h in problem.gauge_group)):
        raise ValueError("gauge group requires identity, unique actions and composition closure")
    return defects


@dataclass(frozen=True)
class PolicyEvaluationReceipt:
    problem_digest: str
    comparison: int
    comparison_name: str
    defect: tuple
    certificate: MatrixQuotientCertificate
    value: Fraction
    status: str
    digest: str = ""

    def refresh_digest(self):
        """Hash candidate bytes; this method does not check their truth."""
        return replace(self, digest=_digest("wdp-policy-observer-evaluation-v1", replace(self, digest="")))


@dataclass(frozen=True)
class AdaptedPolicyObserver:
    problem: PolicyObserverProblem

    @property
    def defects(self):
        return _validate(self.problem)

    def evaluate(self, comparison, certificate):
        actual = self.defects  # Even hand-built reference views are re-admitted.
        if type(comparison) is not int or not 0 <= comparison < len(actual):
            raise ValueError("comparison outside actual declared domain")
        p, c = self.problem, certificate
        if (not isinstance(c, MatrixQuotientCertificate)
                or (c.delta, c.matrix, c.columns, c.weights)
                != (actual[comparison], p.repair.map, len(p.repair.coordinates), p.norm_weights)):
            raise ValueError("certificate belongs to another actual comparison/repair/norm problem")
        if not isinstance(verify_matrix_certificate(c), Accepted):
            raise ValueError("independent primal/dual replay failed")
        t = p.terminal_rules
        status = t.within_tolerance if c.value <= t.tolerance else t.above_tolerance
        return PolicyEvaluationReceipt(_digest("wdp-policy-observer-problem-v1", p), comparison,
                                       p.comparison_domain.names[comparison], actual[comparison],
                                       c, c.value, status).refresh_digest()


def adapt_policy_observer(problem):
    _validate(problem)
    return AdaptedPolicyObserver(problem)


def verify_policy_evaluation(actual, candidate):
    """Recompute from actual input; freshly rehashed false records are refused."""
    if (type(candidate) is not PolicyEvaluationReceipt
            or type(candidate.value) is not Fraction
            or type(candidate.defect) is not tuple
            or any(type(x) is not Fraction for x in candidate.defect)
            or any(type(text) is not str for text in (candidate.problem_digest,
                                                     candidate.comparison_name, candidate.status,
                                                     candidate.digest))):
        return False
    try:
        if candidate.refresh_digest().digest != candidate.digest:
            return False
        return adapt_policy_observer(actual).evaluate(candidate.comparison, candidate.certificate) == candidate
    except (ValueError, TypeError, AttributeError):
        return False
