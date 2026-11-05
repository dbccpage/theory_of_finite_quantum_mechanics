from fractions import Fraction

import pytest
from witnessed_difference.cochains import FiniteComplex
from witnessed_difference.duration import (
    ClockProfile,
    DurationClass,
    Occurrence,
    check_clock,
    classify_duration,
    duration_sum,
    occurrence_chain,
)
from witnessed_difference.histories import (
    FiniteHistoryGraph,
    WeightedEdge,
    cancellation_report,
    enumerate_paths,
    finite_history_sum,
    path_weight,
)
from witnessed_difference.outcomes import Accepted, RefusalCode, Refused
from witnessed_difference.probability import (
    FiniteWitnessSpace,
    conditional_probability,
    disjoint_additivity,
    event_probability,
)


def test_occurrences_preserve_repeated_labels_and_duration_is_exact() -> None:
    chain = occurrence_chain(("tick", "tick", "tock"))
    assert [(item.label, item.index) for item in chain] == [("tick", 0), ("tick", 1), ("tock", 2)]
    result = duration_sum((1, "1/2", Fraction(3, 2)))
    assert isinstance(result, Accepted) and result.value == 3
    with pytest.raises(ValueError, match="nonempty"):
        occurrence_chain(())
    with pytest.raises(ValueError, match="indices"):
        Occurrence("tick", 0.5)
    for weights in ((0,), (-1, 2)):
        refused = duration_sum(weights)
        assert isinstance(refused, Refused) and refused.code is RefusalCode.INVALID_INPUT
    malformed = duration_sum(("not-a-rational",))
    assert isinstance(malformed, Refused)
    assert malformed.code is RefusalCode.INVALID_INPUT


def test_four_way_duration_classifier() -> None:
    triangle = FiniteComplex(("a", "b", "c"), (("a", "b"), ("b", "c"), ("a", "c")), (("a", "b", "c"),))
    exact = {("a", "b"): 1, ("b", "c"): 1, ("a", "c"): 2}
    active = {("a", "b"): 1, ("b", "c"): 1, ("a", "c"): 3}
    assert classify_duration(triangle, exact).kind is DurationClass.EXACT
    assert classify_duration(triangle, exact, exactness_budget=False).kind is DurationClass.EXACTNESS_UNDETERMINED
    assert classify_duration(triangle, active).kind is DurationClass.ACTIVE_CLOSURE_FAILURE
    cycle = FiniteComplex(("a", "b", "c"), (("a", "b"), ("b", "c"), ("a", "c")))
    assert classify_duration(cycle, active).kind is DurationClass.CLOSED_NON_EXACT


def test_clock_adequacy_requires_unit_denominator_coverage_and_coupling() -> None:
    base = ClockProfile("s", 10, frozenset({0, 1}), frozenset({0, 1}), True)
    assert isinstance(check_clock(base), Accepted)
    invalid = [
        (ClockProfile("", 10, base.covered_occurrences, base.required_occurrences, True), RefusalCode.INVALID_INPUT),
        (ClockProfile("s", 0, base.covered_occurrences, base.required_occurrences, True), RefusalCode.INVALID_INPUT),
        (ClockProfile("s", True, base.covered_occurrences, base.required_occurrences, True), RefusalCode.INVALID_INPUT),
        (ClockProfile("s", 0.5, base.covered_occurrences, base.required_occurrences, True), RefusalCode.INVALID_INPUT),
        (ClockProfile("s", 10, frozenset({True}), base.required_occurrences, True), RefusalCode.INVALID_INPUT),
        (ClockProfile("s", 10, frozenset({0}), base.required_occurrences, True), RefusalCode.OUTSIDE_CARRIER),
        (ClockProfile("s", 10, base.covered_occurrences, base.required_occurrences, False), RefusalCode.REACCESS_FAILED),
    ]
    for profile, code in invalid:
        result = check_clock(profile)
        assert isinstance(result, Refused) and result.code is code


def test_finite_probability_counts_occurrences_not_labels() -> None:
    space = FiniteWitnessSpace(("a", "a", "b", "c"))
    assert space.multiplicities == {"a": 2, "b": 1, "c": 1}
    result = event_probability(space, frozenset({"a", "c"}))
    assert isinstance(result, Accepted) and result.value == Fraction(3, 4)
    assert event_probability(FiniteWitnessSpace(()), frozenset()).code is RefusalCode.EMPTY_SPACE
    assert event_probability(space, frozenset({"x"})).code is RefusalCode.EVENT_OUTSIDE_SPACE


def test_disjoint_additivity_and_conditioning() -> None:
    space = FiniteWitnessSpace(("a", "a", "b", "c"))
    additivity = disjoint_additivity(space, frozenset({"a"}), frozenset({"b"}))
    assert isinstance(additivity, Accepted) and additivity.value
    assert disjoint_additivity(space, frozenset({"a"}), frozenset({"a"})).code is RefusalCode.NOT_DISJOINT
    assert disjoint_additivity(space, frozenset({"x"}), frozenset()).code is RefusalCode.EVENT_OUTSIDE_SPACE
    conditional = conditional_probability(space, frozenset({"a"}), frozenset({"a", "b"}))
    assert isinstance(conditional, Accepted) and conditional.value == Fraction(2, 3)
    assert conditional_probability(space, frozenset({"a"}), frozenset()).code is RefusalCode.EMPTY_SPACE
    assert conditional_probability(space, frozenset({"a"}), frozenset({"x"})).code is RefusalCode.EVENT_OUTSIDE_SPACE
    assert conditional_probability(space, frozenset({"x"}), frozenset({"a"})).code is RefusalCode.EVENT_OUTSIDE_SPACE


def graph() -> FiniteHistoryGraph:
    return FiniteHistoryGraph(
        ("a", "b", "c"),
        (
            WeightedEdge("a", "b", Fraction(1, 2)),
            WeightedEdge("b", "c", Fraction(1, 3)),
            WeightedEdge("a", "c", Fraction(1, 5)),
            WeightedEdge("c", "c", Fraction(1, 10)),
        ),
    )


@pytest.mark.parametrize(
    "factory",
    [
        lambda: FiniteHistoryGraph((), ()),
        lambda: FiniteHistoryGraph(("a", "a"), ()),
        lambda: FiniteHistoryGraph(("a",), (WeightedEdge("a", "b", Fraction(1)),)),
        lambda: FiniteHistoryGraph(("a", "b"), (WeightedEdge("a", "b", Fraction(1)), WeightedEdge("a", "b", Fraction(2)))),
    ],
)
def test_history_graph_validation(factory) -> None:
    with pytest.raises(ValueError):
        factory()
    with pytest.raises(TypeError, match="exact"):
        WeightedEdge("a", "b", 0.5)


def test_history_graph_rejects_mutable_collection_aliases() -> None:
    edge = WeightedEdge("a", "b", 1)
    vertices = ["a", "b"]
    edges = [edge]
    with pytest.raises(ValueError, match="immutable tuples"):
        FiniteHistoryGraph(vertices, (edge,))
    with pytest.raises(ValueError, match="immutable tuples"):
        FiniteHistoryGraph(("a", "b"), edges)
    edges.append(WeightedEdge("b", "outside", 1))


def test_bounded_path_enumeration_and_history_sum() -> None:
    paths = enumerate_paths(graph(), "a", "c", 2)
    assert isinstance(paths, Accepted)
    assert paths.value == (("a", "c"), ("a", "b", "c"), ("a", "c", "c"))
    total = finite_history_sum(graph(), "a", "c", 2)
    assert isinstance(total, Accepted) and total.value == Fraction(29, 75)
    zero_step = enumerate_paths(graph(), "a", "a", 0)
    assert isinstance(zero_step, Accepted) and zero_step.value == (("a",),)


@pytest.mark.parametrize("budget", [None, -1, True, 1.5, "2"])
def test_unbounded_or_invalid_history_budget_is_refused(budget) -> None:
    assert enumerate_paths(graph(), "a", "c", budget).code is RefusalCode.BUDGET_REQUIRED
    assert finite_history_sum(graph(), "a", "c", budget).code is RefusalCode.BUDGET_REQUIRED


def test_history_endpoints_and_edges_are_checked() -> None:
    assert enumerate_paths(graph(), "x", "c", 2).code is RefusalCode.OUTSIDE_CARRIER
    assert path_weight(graph(), ()).code is RefusalCode.INVALID_INPUT
    assert path_weight(graph(), ("ghost",)).code is RefusalCode.OUTSIDE_CARRIER
    assert path_weight(graph(), ("a", "x")).code is RefusalCode.OUTSIDE_CARRIER
    assert path_weight(graph(), ("b", "a")).code is RefusalCode.MISSING_EDGE
    one = path_weight(graph(), ("a",))
    assert isinstance(one, Accepted) and one.value == 1
    weighted = path_weight(graph(), ("a", "b", "c"))
    assert isinstance(weighted, Accepted) and weighted.value == Fraction(1, 6)


def test_cancellation_keeps_aggregate_and_pointwise_claims_distinct() -> None:
    cancelled = cancellation_report((1, -1))
    assert cancelled == {"aggregate_zero": True, "pointwise_zero": False, "term_count": 2}
    pointwise = cancellation_report((0, 0))
    assert pointwise["aggregate_zero"] and pointwise["pointwise_zero"]
# Executable finite evidence; AuthorityEffect: None.
