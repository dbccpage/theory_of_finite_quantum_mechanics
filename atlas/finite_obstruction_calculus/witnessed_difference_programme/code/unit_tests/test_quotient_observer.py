from fractions import Fraction
from itertools import product

import pytest
import witnessed_difference.quotient_observer as quotient_observer
from witnessed_difference.cochains import FiniteComplex, d0
from witnessed_difference.obstruction import LinearProgramSolution, exact_quotient_l1
from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused
from witnessed_difference.quotient_observer import (
    LinearQuotientObserver,
    bounded_string_capacity,
    check_passivity,
    grammar_resolution,
    induced_observer_norm,
    kernel_le,
    make_linear_quotient_observer,
    observer_family_order,
    observer_report,
    quotient_observer_layers,
)

SQUARE = FiniteComplex((0, 1, 2, 3), ((0, 1), (1, 2), (2, 3), (0, 3), (0, 2)))
C1 = (1, 1, 0, 0, -1)
C2 = (0, 0, 1, -1, 1)


def accepted(outcome):
    assert isinstance(outcome, Accepted), outcome
    assert outcome.authority_effect is AuthorityEffect.NONE
    return outcome.value


def refused(outcome, code: RefusalCode, fragment: str = "") -> Refused:
    assert isinstance(outcome, Refused), outcome
    assert outcome.code is code, outcome
    assert fragment in outcome.detail, outcome.detail
    return outcome


def observer(*rows) -> LinearQuotientObserver:
    return accepted(make_linear_quotient_observer(SQUARE, rows))


def test_only_repair_compatible_report_maps_are_admitted() -> None:
    admitted = observer(C1, C2)
    assert admitted.report_rows == ((1, 1, 0, 0, -1), (0, 0, 1, -1, 1))
    assert all(type(entry) is Fraction for row in admitted.report_rows for entry in row)
    assert observer().report_rows == ()
    refused(make_linear_quotient_observer(SQUARE, ((1, 0, 0, 0, 0),)), RefusalCode.NOT_REPAIR_COMPATIBLE)
    refused(make_linear_quotient_observer(SQUARE, (C1, (1, 1, 1, 1, 1))), RefusalCode.NOT_REPAIR_COMPATIBLE)
    for rows in (((1.0, 1, 0, 0, -1),), ((1, 1, 0, 0),), "rows", (C1, (0, 0, 1))):
        refused(make_linear_quotient_observer(SQUARE, rows), RefusalCode.INVALID_INPUT)
    refused(make_linear_quotient_observer("K", (C1,)), RefusalCode.INVALID_INPUT)


OBSERVERS = {
    "cycle_one": (C1,),
    "both_cycles": (C1, C2),
    "sum": (tuple(a + b for a, b in zip(C1, C2)),),
    "zero": (),
}


@pytest.mark.parametrize("name", tuple(OBSERVERS))
def test_passivity_exhaustively_on_a_cochain_box(name) -> None:
    lens = observer(*OBSERVERS[name])
    for values in product((0, 1, -1), repeat=5):
        receipt = accepted(check_passivity(lens, dict(zip(SQUARE.edges, values))))
        assert receipt.observer_norm <= receipt.phi1
        assert receipt.exact_stays_exact
        if receipt.phi1 == 0:
            assert receipt.observer_norm == 0 and all(value == 0 for value in receipt.report)
        assert type(receipt.observer_norm) is Fraction


def test_passivity_can_be_strict_and_core_identifications_survive() -> None:
    lens = observer(C1)
    delta = {(0, 1): 1, (1, 2): 0, (2, 3): 1, (0, 3): 0, (0, 2): 0}
    receipt = accepted(check_passivity(lens, delta))
    assert (receipt.phi1, receipt.observer_norm) == (2, 1)
    for potential in product((-1, 0, 2), repeat=4):
        gradient = d0(SQUARE, dict(zip(SQUARE.vertices, potential)))
        moved = {edge: delta[edge] + gradient[edge] for edge in SQUARE.edges}
        assert observer_report(lens, tuple(moved[edge] for edge in SQUARE.edges)) == receipt.report
        assert accepted(exact_quotient_l1(SQUARE, moved)).value == receipt.phi1


def test_induced_norm_values_and_refusals() -> None:
    doubled = observer(C1, tuple(2 * value for value in C1))
    assert accepted(induced_observer_norm(doubled, (1, 2))) == 1
    assert accepted(induced_observer_norm(observer(C1), ("3/2",))) == Fraction(3, 2)
    weights = {edge: 5 for edge in SQUARE.edges}
    assert accepted(induced_observer_norm(observer(C1), (1,), weights)) == 5
    assert accepted(induced_observer_norm(observer(), ())) == 0
    refused(induced_observer_norm(doubled, (1, 1)), RefusalCode.INFEASIBLE)
    refused(induced_observer_norm(doubled, (1,)), RefusalCode.INVALID_INPUT)
    refused(induced_observer_norm(doubled, (1.0, 2)), RefusalCode.INVALID_INPUT)
    refused(induced_observer_norm(doubled, (1, 2), {(0, 1): 1}), RefusalCode.INVALID_INPUT)
    refused(induced_observer_norm("observer", (1,)), RefusalCode.INVALID_INPUT)
    refused(induced_observer_norm(doubled, (1, 2), max_pivots=0), RefusalCode.BUDGET_EXHAUSTED)


def test_passivity_refusals_and_violation_detection(monkeypatch) -> None:
    lens = observer(C1)
    delta = dict(zip(SQUARE.edges, (1, 0, 0, 0, 0)))
    refused(check_passivity("observer", delta), RefusalCode.INVALID_INPUT)
    refused(check_passivity(lens, {(0, 1): 1}), RefusalCode.INVALID_INPUT)
    monkeypatch.setattr(quotient_observer, "induced_observer_norm", lambda *args: Accepted(Fraction(9)))
    refused(check_passivity(lens, delta), RefusalCode.CERTIFICATE_MISMATCH, "exceeds")
    monkeypatch.setattr(
        quotient_observer, "induced_observer_norm", lambda *args: Refused(RefusalCode.INFEASIBLE, "stub")
    )
    refused(check_passivity(lens, delta), RefusalCode.INFEASIBLE, "stub")


@pytest.mark.parametrize(
    ("requested", "code"),
    [
        (("memory",), RefusalCode.MISSING_ADAPTER),
        (("presentation", "policy"), RefusalCode.MISSING_ADAPTER),
        (("evaluator", "authority"), RefusalCode.SCOPE_VIOLATION),
        (("gossip",), RefusalCode.INVALID_INPUT),
        (["presentation"], RefusalCode.INVALID_INPUT),
    ],
)
def test_quotient_observer_supplies_only_presentation_and_evaluator(requested, code) -> None:
    lens = observer(C1)
    layers = accepted(quotient_observer_layers(lens, ("presentation", "evaluator")))
    assert layers.presentation == lens.report_rows and layers.evaluator == "induced_l1_quotient_norm"
    assert not any(hasattr(layers, name) for name in ("memory", "policy", "authority"))
    refused(quotient_observer_layers(lens, requested), code)
    refused(quotient_observer_layers("observer", ()), RefusalCode.INVALID_INPUT)


IDENTITY = tuple(tuple(int(i == j) for j in range(5)) for i in range(5))
FAMILY = {
    "identity": IDENTITY,
    "quotient": (C1, C2),
    "quotient_swapped": (C2, C1),
    "cycle_one": (C1,),
    "cycle_one_doubled": (tuple(2 * value for value in C1),),
    "sum": (tuple(a + b for a, b in zip(C1, C2)),),
    "zero": ((0, 0, 0, 0, 0),),
}


def test_observer_family_is_a_preorder_and_a_partial_order_on_kernels() -> None:
    order = accepted(observer_family_order({**FAMILY, "admitted": observer(C1)}))
    relation = order.relation
    names = order.names
    assert all((name, name) in relation for name in names)
    for (a, b), (c, d) in product(relation, repeat=2):
        if b == c:
            assert (a, d) in relation
    assert all(("identity", name) in relation and (name, "zero") in relation for name in names)
    assert ("zero", "identity") not in relation
    blocks = {frozenset(block) for block in order.kernel_classes}
    assert frozenset({"quotient", "quotient_swapped"}) in blocks
    assert frozenset({"cycle_one", "cycle_one_doubled", "admitted"}) in blocks
    assert sum(len(block) for block in order.kernel_classes) == len(names)
    for i, j in order.class_order:
        assert (j, i) not in order.class_order or i == j
    assert ("cycle_one", "sum") not in relation and ("sum", "cycle_one") not in relation


def test_kernel_inclusion_is_exact() -> None:
    assert kernel_le(((1, 0),), ((2, 0),)) and kernel_le(((2, 0),), ((1, 0),))
    assert kernel_le(((1, 0), (0, 1)), ((1, 1),)) and not kernel_le(((1, 1),), ((1, 0),))
    assert kernel_le(((0, 0),), ((0, 0),))
    with pytest.raises(ValueError, match="zero rows"):
        kernel_le((), ((0, 0),))
    assert kernel_le((("1/3", 0),), ((1, 0),))
    with pytest.raises(ValueError):
        kernel_le(((1, 0),), ((1, 0, 0),))
    with pytest.raises(ValueError):
        kernel_le(((1.0, 0),), ((1, 0),))


@pytest.mark.parametrize(
    "family",
    [{}, {"": IDENTITY}, {1: IDENTITY}, {"a": ((1, 0),), "b": ((1, 0, 0),)}, "family"],
)
def test_observer_family_refusals(family) -> None:
    refused(observer_family_order(family), RefusalCode.INVALID_INPUT)


def test_grammar_resolution_bounds_visible_classes() -> None:
    receipt = accepted(grammar_resolution(("q0", "q1", "q2", "q3"), {"q0": "", "q1": "a", "q2": "b", "q3": "a"}, ("", "a", "b")))
    assert (receipt.core_classes, receipt.capacity, receipt.visible_classes) == (4, 3, 3)
    assert receipt.pigeonhole_forced and receipt.collision == ("q1", "q3")
    injective = accepted(grammar_resolution(("q0", "q1"), {"q0": "a", "q1": "b"}, frozenset({"a", "b", "c"})))
    assert injective.collision is None and not injective.pigeonhole_forced and injective.visible_classes == 2
    voluntary = accepted(grammar_resolution(("q0", "q1"), {"q0": "a", "q1": "a"}, ("a", "b")))
    assert voluntary.collision == ("q0", "q1") and not voluntary.pigeonhole_forced
    refused(grammar_resolution(("q0",), {"q0": "zz"}, ("a",)), RefusalCode.GRAMMAR_VIOLATION)
    refused(grammar_resolution(("q0", "q1"), {"q0": "a"}, ("a",)), RefusalCode.INVALID_INPUT)
    refused(grammar_resolution(("q0", "q0"), {"q0": "a"}, ("a",)), RefusalCode.INVALID_INPUT)
    refused(grammar_resolution(["q0"], {"q0": "a"}, ("a",)), RefusalCode.INVALID_INPUT)


def test_pigeonhole_is_exhaustive_for_small_report_maps() -> None:
    classes = ("q0", "q1", "q2")
    grammar = ("a", "b")
    for words in product(grammar, repeat=3):
        receipt = accepted(grammar_resolution(classes, dict(zip(classes, words)), grammar))
        assert receipt.visible_classes <= receipt.capacity and receipt.collision is not None


def test_bounded_string_capacity_matches_enumeration() -> None:
    for size, length in product(range(4), repeat=2):
        alphabet = "abc"[:size]
        strings = {"".join(word) for ell in range(length + 1) for word in product(alphabet, repeat=ell)}
        assert bounded_string_capacity(size, length) == len(strings)
    for bad in ((-1, 2), (2, -1), (True, 2), (2, 1.0)):
        with pytest.raises(ValueError):
            bounded_string_capacity(*bad)


def test_a_hand_built_observer_is_re_admitted_at_every_entry_point() -> None:
    forged = LinearQuotientObserver(SQUARE, ((Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0)),))
    delta = dict(zip(SQUARE.edges, (0, 0, 0, 0, 0)))
    refused(check_passivity(forged, delta), RefusalCode.NOT_REPAIR_COMPATIBLE)
    refused(induced_observer_norm(forged, (0,)), RefusalCode.NOT_REPAIR_COMPATIBLE)
    refused(quotient_observer_layers(forged, ("presentation",)), RefusalCode.NOT_REPAIR_COMPATIBLE)
    with pytest.raises(ValueError, match="not admissible"):
        kernel_le(forged, observer(C1))
    refused(observer_family_order({"forged": forged, "cycle": observer(C1)}), RefusalCode.INVALID_INPUT, "not admissible")
    refused(induced_observer_norm("observer", (0,)), RefusalCode.INVALID_INPUT)
    spelled = LinearQuotientObserver(SQUARE, (("1", "1", "0", "0", "-1"),))
    refused(check_passivity(spelled, delta), RefusalCode.CERTIFICATE_MISMATCH, "re-admitted form")


def test_the_observer_norm_is_reported_only_with_a_verified_dual(monkeypatch) -> None:
    lens = observer(C1)
    assert accepted(induced_observer_norm(lens, (3,))) == 3
    from witnessed_difference import obstruction
    genuine = obstruction.evaluate

    def lying_dual(request, **kwargs):
        response = genuine(request, **kwargs)
        if request["operation"] == "solve_phi1":
            response["dual"] = [str(2 * Fraction(y)) for y in response["dual"]]
        return response

    monkeypatch.setattr(obstruction, "evaluate", lying_dual)
    refused(induced_observer_norm(lens, (3,)), RefusalCode.CERTIFICATE_MISMATCH)

    def lying_value(request, **kwargs):
        response = genuine(request, **kwargs)
        if request["operation"] == "solve_phi1":
            response["value"] = "0"
        return response

    monkeypatch.setattr(obstruction, "evaluate", lying_value)
    refused(induced_observer_norm(lens, (3,)), RefusalCode.CERTIFICATE_MISMATCH)


# Executable finite evidence; AuthorityEffect: None.
