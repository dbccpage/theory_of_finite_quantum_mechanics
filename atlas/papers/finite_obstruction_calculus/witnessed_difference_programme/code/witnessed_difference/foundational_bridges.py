"""Bounded executable witnesses for the 11 WDP foundational bridges and derivations.

Every witness is exact, finite, and replayable.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from types import MappingProxyType
from typing import Callable, Mapping, Sequence

from .exact_linear import ExactField, Matrix, is_zero, matmul
from .outcomes import Accepted, AuthorityEffect, Outcome, RefusalCode, Refused

# ---------------------------------------------------------------------------
# Bridge 1: Inscription <> -> Distinct Admitted Marks
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Inscription:
    """Finite nested constructor for inscription marks arising from empty <>."""

    depth: int = 0

    def nest(self) -> Inscription:
        return Inscription(depth=self.depth + 1)


def empty_inscription() -> Inscription:
    return Inscription(depth=0)


def admit_mark(inscription: Inscription) -> str:
    """Admit a mark from an inscription with explicit depth."""
    return f"mark_{inscription.depth}"


def apartness_witness(m1: Inscription, m2: Inscription) -> Outcome[bool]:
    """Witness that two inscriptions are distinct by comparing their depth."""
    if m1.depth != m2.depth:
        return Accepted(True)
    return Refused(RefusalCode.NOT_DISJOINT, "inscriptions are identical; no distinction witnessed")


# ---------------------------------------------------------------------------
# Bridge 2: Marks -> Algebra, Cochains, and Quotients
# ---------------------------------------------------------------------------
def bool_xor(x: bool, y: bool) -> bool:
    if type(x) is not bool or type(y) is not bool:
        raise TypeError("binary cochains require actual bool values")
    return (x and not y) or (not x and y)


def bool_d0(f: Callable[[str], bool], u: str, v: str) -> bool:
    """0-coboundary operator: d0(f)(u, v) = f(u) XOR f(v)."""
    return bool_xor(f(u), f(v))


def bool_d1(e: Callable[[str, str], bool], a: str, b: str, c: str) -> bool:
    """1-coboundary operator: d1(e)(a, b, c) = e(a, b) XOR e(b, c) XOR e(a, c)."""
    return bool_xor(bool_xor(e(a, b), e(b, c)), e(a, c))


def verify_triangle_coboundary_zero(
    f: Callable[[str], bool],
    a: str,
    b: str,
    c: str,
    *,
    e_override: Callable[[str, str], bool] | None = None,
) -> Outcome[bool]:
    """Verify that d1(d0(f))(a, b, c) == 0 (False) for any 0-cochain f."""
    e = e_override if e_override is not None else (lambda u, v: bool_d0(f, u, v))
    try:
        coboundary = bool_d1(e, a, b, c)
    except TypeError as error:
        return Refused(RefusalCode.INVALID_INPUT, str(error))
    if not coboundary:
        return Accepted(True)
    return Refused(RefusalCode.NOT_A_DIFFERENTIAL, "binary triangle coboundary was non-zero")


# ---------------------------------------------------------------------------
# Bridge 3: Genesis Histories -> Contextual Observers
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class FiniteTransducer:
    num_states: int
    num_inputs: int
    step_table: tuple[tuple[int, ...], ...]  # state x input -> next_state

    def __post_init__(self) -> None:
        if any(type(n) is not int or n < 0 for n in (self.num_states, self.num_inputs)):
            raise ValueError("transducer dimensions must be nonnegative integers")
        table = tuple(tuple(row) for row in self.step_table)
        if (len(table) != self.num_states or any(len(row) != self.num_inputs for row in table)
                or any(type(v) is not int or not 0 <= v < self.num_states for row in table for v in row)):
            raise ValueError("transducer table must be total with targets in its state carrier")
        object.__setattr__(self, "step_table", table)

    def step(self, state: int, inp: int) -> int:
        if type(state) is not int or not (0 <= state < self.num_states):
            raise IndexError(f"state {state} out of range [0, {self.num_states})")
        if type(inp) is not int or not (0 <= inp < self.num_inputs):
            raise IndexError(f"input {inp} out of range [0, {self.num_inputs})")
        return self.step_table[state][inp]


def product_transducer(t1: FiniteTransducer, t2: FiniteTransducer) -> FiniteTransducer:
    """Cartesian product of two finite transducers."""
    prod_states = t1.num_states * t2.num_states
    prod_inputs = t1.num_inputs * t2.num_inputs
    table: list[tuple[int, ...]] = []
    for s in range(prod_states):
        s1 = s // t2.num_states
        s2 = s % t2.num_states
        row: list[int] = []
        for i in range(prod_inputs):
            i1 = i // t2.num_inputs
            i2 = i % t2.num_inputs
            ns1 = t1.step(s1, i1)
            ns2 = t2.step(s2, i2)
            row.append(ns1 * t2.num_states + ns2)
        table.append(tuple(row))
    return FiniteTransducer(prod_states, prod_inputs, tuple(table))


# ---------------------------------------------------------------------------
# Bridge 4: Observers -> Probability and Physical Adapters
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class MultiplicityDistribution:
    """Exact rational probability distribution derived directly from finite counts."""

    counts: Mapping[str, int]
    total: int

    def __post_init__(self) -> None:
        if not isinstance(self.counts, Mapping):
            raise ValueError("counts must be a mapping of non-negative integers")
        counts = dict(self.counts)
        if any(type(count) is not int or count < 0 for count in counts.values()):
            raise ValueError("counts must be non-negative integers")
        if type(self.total) is not int or self.total <= 0 or self.total != sum(counts.values()):
            raise ValueError("total must equal the positive integer sum of counts")
        object.__setattr__(self, "counts", MappingProxyType(counts))

    @classmethod
    def from_counts(cls, counts: Mapping[str, int]) -> Outcome[MultiplicityDistribution]:
        if not isinstance(counts, Mapping) or any(
            type(count) is not int or count < 0 for count in counts.values()
        ):
            return Refused(RefusalCode.INVALID_INPUT, "counts must be non-negative integers")
        total = sum(counts.values())
        if total <= 0:
            return Refused(RefusalCode.EMPTY_SPACE, "total count must be positive")
        return Accepted(cls(dict(counts), total))

    def probability(self, event: str) -> Fraction:
        count = self.counts.get(event, 0)
        return Fraction(count, self.total)

    def disjoint_union_probability(self, events: Sequence[str]) -> Outcome[Fraction]:
        seen: set[str] = set()
        for e in events:
            if e in seen:
                return Refused(RefusalCode.NOT_DISJOINT, f"duplicate event {e}")
            seen.add(e)
        return Accepted(sum((self.probability(e) for e in events), start=Fraction(0)))


# ---------------------------------------------------------------------------
# Bridge 5: Reports -> Evaluation
# ---------------------------------------------------------------------------
class EvaluationStatus(str, Enum):
    ACCEPT = "accept"
    REJECT = "reject"
    REFUSE = "refuse"
    OUTSIDE_PROFILE = "outside_profile"


def evaluate_report_claim(in_profile: bool, evidence_valid: bool) -> EvaluationStatus:
    if type(in_profile) is not bool or type(evidence_valid) is not bool:
        return EvaluationStatus.REFUSE
    if not in_profile:
        return EvaluationStatus.OUTSIDE_PROFILE
    return EvaluationStatus.ACCEPT if evidence_valid else EvaluationStatus.REJECT


# ---------------------------------------------------------------------------
# Bridge 6: Evaluation / Proposals -> Authorization
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class MathematicalReceipt:
    receipt_id: str
    claim_id: str
    verified: bool
    authority_effect: AuthorityEffect | str = AuthorityEffect.NONE


def check_no_authority_effect(receipt: MathematicalReceipt) -> Outcome[bool]:
    if receipt.authority_effect == AuthorityEffect.NONE:
        return Accepted(True)
    return Refused(RefusalCode.CLAIM_STATUS_FIREWALL, "receipt attempted authority leakage")


# ---------------------------------------------------------------------------
# Bridge 7: Binary Carrier vs. General Triangle Parity Law
# ---------------------------------------------------------------------------
def compute_triangle_mark_differences(marks: tuple[str, str, str]) -> tuple[bool, bool, bool, bool]:
    """Computes d(a,b), d(b,c), d(a,c) and their XOR sum.

    Shows that for pairwise distinct marks, XOR sum is True (1), not 0.
    """
    a, b, c = marks
    d_ab = a != b
    d_bc = b != c
    d_ac = a != c
    parity = bool_xor(bool_xor(d_ab, d_bc), d_ac)
    return (d_ab, d_bc, d_ac, parity)


# ---------------------------------------------------------------------------
# Bridge 8: Arbitrary-Norm Rational Attainment
# ---------------------------------------------------------------------------
def rational_l1_norm(point: Sequence[Fraction | int]) -> Fraction:
    """Evaluate only exact integer/Fraction entries; never convert a witness."""
    values = tuple(point)
    if any(type(value) not in (int, Fraction) for value in values):
        raise TypeError("L1 candidates require exact integer or Fraction entries")
    from .native_functionals import representative_mass
    return representative_mass(values)


def find_rational_l1_minimizer(
    points: Sequence[Sequence[Fraction | int]],
) -> Outcome[tuple[Sequence[Fraction | int], Fraction]]:
    """Select an exact L1 minimum from a nonempty finite candidate list."""
    if not points:
        return Refused(RefusalCode.EMPTY_SPACE, "points set cannot be empty")
    try:
        min_pt = points[0]
        min_val = rational_l1_norm(min_pt)
        for pt in points[1:]:
            val = rational_l1_norm(pt)
            if val < min_val:
                min_val = val
                min_pt = pt
    except TypeError as error:
        return Refused(RefusalCode.INVALID_INPUT, str(error))
    return Accepted((min_pt, min_val))


# ---------------------------------------------------------------------------
# Bridge 9: Flat Locus Invariance under Graded Perturbations
# ---------------------------------------------------------------------------
def verify_flat_locus_curvature(d_op: Matrix, field: ExactField = ExactField.RATIONAL) -> Outcome[bool]:
    """Verify that d^2 = 0 implies flat curvature (zero 2-step composition)."""
    dim = len(d_op)
    d2 = matmul(d_op, d_op, dim, field)
    if is_zero(d2, field):
        return Accepted(True)
    return Refused(RefusalCode.NOT_A_DIFFERENTIAL, "d^2 is not zero; non-flat curvature")


# ---------------------------------------------------------------------------
# Bridge 10: Cover Marginals vs. Global Hidden Variables
# ---------------------------------------------------------------------------
def solve_frustrated_spin_cycle(num_nodes: int = 3) -> Outcome[dict[str, bool]]:
    """Attempts to find a global binary spin assignment s_i in {0, 1}
    such that s_i != s_{i+1} for all i in cyclic order.
    The indexed cycle has a positive integer length. For odd cycles (e.g. 3),
    no such global assignment exists (frustrated cycle).
    """
    if type(num_nodes) is not int or num_nodes <= 0:
        return Refused(RefusalCode.INVALID_INPUT, "spin cycle length must be a positive integer")
    if num_nodes % 2 != 0:
        return Refused(
            RefusalCode.INFEASIBLE,
            f"odd cycle of length {num_nodes} is frustrated; no global assignment exists",
        )
    assignment = {f"s_{i}": (i % 2 == 1) for i in range(num_nodes)}
    return Accepted(assignment)


# ---------------------------------------------------------------------------
# Bridge 11: Deterministic Retention vs. Branching Observer Packets
# ---------------------------------------------------------------------------
def verify_deterministic_retention(transitions: Sequence[tuple[str, str, str]]) -> Outcome[bool]:
    """Verify that every (src, input) pair maps to a unique dst (no branching)."""
    table: dict[tuple[str, str], str] = {}
    for src, inp, dst in transitions:
        key = (src, inp)
        if key in table and table[key] != dst:
            return Refused(
                RefusalCode.NOT_CLOSED,
                f"branching detected: input {inp!r} from state {src!r} has multiple destinations: {table[key]!r} and {dst!r}",
            )
        table[key] = dst
    return Accepted(True)
