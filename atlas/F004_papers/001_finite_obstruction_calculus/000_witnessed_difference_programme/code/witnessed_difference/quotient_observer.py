"""Repair-compatible linear quotient observers and their finite resolution bounds.

A report map R: C1 -> Q^k with R o d0 = 0 descends to the quotient Q1.  It
enters the layered observer only as a presentation report map and an evaluator
cost, the induced norm on realized reports Phi_O(y) = min{||h||_{1,w} : R h = y}.  It supplies no
memory, policy, or authority layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Hashable, Mapping, Sequence

from .cochains import Edge, FiniteComplex
from .obstruction import (
    DEFAULT_PIVOT_BUDGET,
    MatrixQuotientCertificate,
    QuotientCertificate,
    _exact_matrix,
    d0_matrix,
    edge_weights,
    exact_quotient_l1,
    matrix_product,
    matrix_quotient_l1,
)
from .outcomes import Accepted, Outcome, RefusalCode, Refused
from .simplicial import rank_rational
from observer_completion.observer_completion import M, null, solve

ExactScalar = int | str | Fraction
ADMITTED_LAYERS = frozenset({"presentation", "evaluator"})
MISSING_LAYERS = frozenset({"memory", "policy"})


@dataclass(frozen=True)
class QuotientEvaluatorReceipt:
    """The declared class relation and the independently checked evaluator witness."""

    class_repairs: tuple[tuple[Fraction, ...], ...]
    certificate: MatrixQuotientCertificate


def evaluate_quotient_profile(
    class_repairs: Sequence[Sequence[ExactScalar]],
    evaluator_repairs: Sequence[Sequence[ExactScalar]],
    representative: Sequence[ExactScalar],
    weights: Sequence[ExactScalar] | None = None,
    *,
    max_pivots: int = DEFAULT_PIVOT_BUDGET,
) -> Outcome[QuotientEvaluatorReceipt]:
    """Descend an l1 evaluator only if its repair image contains the class repairs.

    Both matrices map into the same cochain space. Equality of images preserves
    exactly the same zero classes; strict inclusion intentionally forgets more.
    The supplied representative is passed intact to the existing exact solver.
    """

    core = _exact_matrix(class_repairs, None)
    repairs = _exact_matrix(evaluator_repairs, None)
    if core is None or repairs is None or len(core) != len(repairs):
        return Refused(RefusalCode.INVALID_INPUT, "repair matrices must be exact with a shared carrier")
    joined = tuple(left + right for left, right in zip(repairs, core))
    if rank_rational(joined) != rank_rational(repairs):
        return Refused(
            RefusalCode.NOT_REPAIR_COMPATIBLE,
            "the evaluator repair image does not contain the declared class repairs",
        )
    solved = matrix_quotient_l1(repairs, representative, weights, max_pivots=max_pivots)
    if isinstance(solved, Refused):
        return solved
    return Accepted(QuotientEvaluatorReceipt(core, solved.value))


@dataclass(frozen=True)
class LinearQuotientObserver:
    complex_: FiniteComplex
    report_rows: tuple[tuple[Fraction, ...], ...]


def make_linear_quotient_observer(
    complex_: FiniteComplex,
    report_rows: Sequence[Sequence[ExactScalar]],
) -> Outcome[LinearQuotientObserver]:
    """Admit R only when every row is exact, edge-aligned, and R o d0 = 0 exactly."""

    if not isinstance(complex_, FiniteComplex):
        return Refused(RefusalCode.INVALID_INPUT, "an observer needs a finite complex")
    rows = _exact_matrix(report_rows, len(complex_.edges))
    if rows is None:
        return Refused(RefusalCode.INVALID_INPUT, "report rows must be exact and aligned with the edges")
    composite = matrix_product(rows, d0_matrix(complex_), len(complex_.vertices))
    if any(entry != 0 for row in composite for entry in row):
        return Refused(RefusalCode.NOT_REPAIR_COMPATIBLE, "R o d0 is not zero; the report sees repairs")
    return Accepted(LinearQuotientObserver(complex_, rows))


def _readmitted(observer: object) -> Outcome[LinearQuotientObserver]:
    """Re-run admission on a stored observer; a hand-built record is not trusted."""

    if not isinstance(observer, LinearQuotientObserver):
        return Refused(RefusalCode.INVALID_INPUT, "a linear quotient observer is required")
    admitted = make_linear_quotient_observer(observer.complex_, observer.report_rows)
    if isinstance(admitted, Accepted) and admitted.value != observer:
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "the stored observer differs from its re-admitted form")
    return admitted


def observer_report(observer: LinearQuotientObserver, values: Sequence[Fraction]) -> tuple[Fraction, ...]:
    return tuple(sum((a * b for a, b in zip(row, values)), start=Fraction(0)) for row in observer.report_rows)


def induced_observer_norm(
    observer: LinearQuotientObserver,
    report_value: Sequence[ExactScalar],
    weights: Mapping[Edge, ExactScalar] | None = None,
    *,
    max_pivots: int = DEFAULT_PIVOT_BUDGET,
) -> Outcome[Fraction]:
    """Phi_O(y) = min{||h||_{1,w} : R h = y}; values outside im R are refused.

    Exact elimination proposes h0 with R h0 = y and a basis N of ker R.
    The feasible fiber is h0 + im N. Its minimum weighted mass is the quotient
    distance of h0 modulo im N, evaluated and checked by omega_functional.
    """

    admitted = _readmitted(observer)
    if isinstance(admitted, Refused):
        return admitted
    target = _exact_matrix((report_value,), None)
    if target is None or len(target[0]) != len(observer.report_rows):
        return Refused(RefusalCode.INVALID_INPUT, "the report value must be exact with one entry per row")
    w = edge_weights(observer.complex_, weights)
    if isinstance(w, Refused):
        return w
    report = M(observer.report_rows, len(observer.complex_.edges))
    try:
        preimage = solve(report, M([[entry] for entry in target[0]], 1))
    except ValueError:
        return Refused(RefusalCode.INFEASIBLE, "the requested report has no preimage")
    kernel = null(report)
    solved = matrix_quotient_l1(kernel.a, tuple(row[0] for row in preimage.a), w.value,
                               columns=kernel.c, max_pivots=max_pivots)
    if isinstance(solved, Refused):
        return solved
    return Accepted(solved.value.value)


@dataclass(frozen=True)
class PassivityReceipt:
    phi1: Fraction
    observer_norm: Fraction
    report: tuple[Fraction, ...]
    exact_stays_exact: bool
    certificate: QuotientCertificate


def check_passivity(
    observer: LinearQuotientObserver,
    cochain: Mapping[Edge, ExactScalar],
    weights: Mapping[Edge, ExactScalar] | None = None,
) -> Outcome[PassivityReceipt]:
    """Phi_O(R delta) <= Phi_1([delta]); an observer never creates obstruction."""

    admitted = _readmitted(observer)
    if isinstance(admitted, Refused):
        return admitted
    certified = exact_quotient_l1(observer.complex_, cochain, weights)
    if isinstance(certified, Refused):
        return certified
    certificate = certified.value
    report = observer_report(observer, certificate.cochain)
    observed = induced_observer_norm(observer, report, weights)
    if isinstance(observed, Refused):
        return observed
    if observed.value > certificate.value:
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "the observer norm exceeds the core quotient norm")
    exact_stays_exact = certificate.value != 0 or observed.value == 0
    return Accepted(PassivityReceipt(certificate.value, observed.value, report, exact_stays_exact, certificate))


@dataclass(frozen=True)
class ObserverLayers:
    presentation: tuple[tuple[Fraction, ...], ...]
    evaluator: str
    layers: tuple[str, ...]


def quotient_observer_layers(
    observer: LinearQuotientObserver,
    requested: tuple[str, ...],
) -> Outcome[ObserverLayers]:
    """Only presentation and evaluator layers exist; memory, policy, authority do not."""

    if not isinstance(observer, LinearQuotientObserver) or type(requested) is not tuple:
        return Refused(RefusalCode.INVALID_INPUT, "an observer and a tuple of layer names are required")
    admitted = _readmitted(observer)
    if isinstance(admitted, Refused):
        return admitted
    for layer in requested:
        if layer == "authority":
            return Refused(RefusalCode.SCOPE_VIOLATION, "a quotient observer supplies no authority layer")
        if layer in MISSING_LAYERS:
            return Refused(RefusalCode.MISSING_ADAPTER, f"a quotient observer supplies no {layer} layer")
        if layer not in ADMITTED_LAYERS:
            return Refused(RefusalCode.INVALID_INPUT, f"undeclared observer layer {layer!r}")
    return Accepted(ObserverLayers(observer.report_rows, "induced_l1_quotient_norm", requested))


def _report_matrix(value: object) -> M:
    if isinstance(value, LinearQuotientObserver):
        admitted = _readmitted(value)
        if isinstance(admitted, Refused):
            raise ValueError(f"the observer is not admissible: {admitted.detail}")
        return M(admitted.value.report_rows, len(admitted.value.complex_.edges))
    rows = _exact_matrix(value, None)
    if rows is None or not rows:
        raise ValueError("a raw report matrix must be nonempty; use a declared observer for zero rows")
    return M(rows)


def kernel_le(a: object, b: object) -> bool:
    """ker a is contained in ker b iff rank([a; b]) == rank(a), computed exactly."""

    first, second = _report_matrix(a), _report_matrix(b)
    if first.c != second.c:
        raise ValueError("report maps must share one source space")
    return rank_rational(first.a + second.a) == rank_rational(first.a)


@dataclass(frozen=True)
class ObserverOrder:
    names: tuple[str, ...]
    relation: frozenset[tuple[str, str]]
    kernel_classes: tuple[frozenset[str], ...]
    class_order: frozenset[tuple[int, int]]


def observer_family_order(family: Mapping[str, object]) -> Outcome[ObserverOrder]:
    """Kernel inclusion as a preorder; equal-kernel classes as a partial order."""

    if not isinstance(family, Mapping) or not family or any(not isinstance(n, str) or not n for n in family):
        return Refused(RefusalCode.INVALID_INPUT, "the observer family must be a nonempty named mapping")
    names = tuple(family)
    try:
        relation = frozenset((a, b) for a in names for b in names if kernel_le(family[a], family[b]))
    except (TypeError, ValueError) as error:
        return Refused(RefusalCode.INVALID_INPUT, f"invalid observer family: {error}")
    classes: list[frozenset[str]] = []
    for name in names:
        if not any(name in block for block in classes):
            classes.append(frozenset(other for other in names if {(name, other), (other, name)} <= relation))
    representatives = [min(block, key=names.index) for block in classes]
    order = frozenset(
        (i, j)
        for i, left in enumerate(representatives)
        for j, right in enumerate(representatives)
        if (left, right) in relation
    )
    return Accepted(ObserverOrder(names, relation, tuple(classes), order))


@dataclass(frozen=True)
class GrammarReceipt:
    core_classes: int
    capacity: int
    visible_classes: int
    collision: tuple[Hashable, Hashable] | None
    pigeonhole_forced: bool


def grammar_resolution(
    classes: tuple[Hashable, ...],
    report: Mapping[Hashable, Hashable],
    grammar: frozenset[Hashable] | tuple[Hashable, ...],
) -> Outcome[GrammarReceipt]:
    """A report into a finite grammar G exposes at most |G| classes."""

    if type(classes) is not tuple or len(set(classes)) != len(classes):
        return Refused(RefusalCode.INVALID_INPUT, "core classes must be a unique tuple")
    if not isinstance(report, Mapping) or set(report) != set(classes):
        return Refused(RefusalCode.INVALID_INPUT, "the report map must be defined on every core class")
    words = frozenset(grammar)
    outside = [label for label in classes if report[label] not in words]
    if outside:
        return Refused(RefusalCode.GRAMMAR_VIOLATION, f"reports for {outside!r} are not grammar words")
    seen: dict[Hashable, Hashable] = {}
    collision = None
    for label in classes:
        word = report[label]
        if word in seen and collision is None:
            collision = (seen[word], label)
        seen.setdefault(word, label)
    return Accepted(GrammarReceipt(len(classes), len(words), len(seen), collision, len(classes) > len(words)))


def bounded_string_capacity(alphabet_size: int, max_length: int) -> int:
    """Number of strings of length at most L over an alphabet: sum of |Sigma|^l."""

    if any(type(value) is not int or value < 0 for value in (alphabet_size, max_length)):
        raise ValueError("alphabet size and maximum length must be non-negative integers")
    return sum(alphabet_size**length for length in range(max_length + 1))


# Executable finite evidence; AuthorityEffect: None.
