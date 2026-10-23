from itertools import product

import pytest
from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused
from witnessed_difference.pointed_relation import (
    PointedCensus,
    PointedPredicates,
    PointedRelation,
    apartness_countermodels,
    closed_form_census,
    enumerate_pointed_relations,
    make_pointed_relation,
    pointed_predicates,
)


def accepted(outcome):
    assert isinstance(outcome, Accepted), outcome
    assert outcome.authority_effect is AuthorityEffect.NONE
    return outcome.value


def refused(outcome, code: RefusalCode, fragment: str = "") -> Refused:
    assert isinstance(outcome, Refused), outcome
    assert outcome.code is code, outcome
    assert fragment in outcome.detail, outcome.detail
    return outcome


def test_census_matches_the_closed_forms_on_carriers_up_to_three() -> None:
    census = accepted(enumerate_pointed_relations(3))
    assert census == accepted(closed_form_census(3))
    assert census == PointedCensus(3, 4674, 2337, 196, 3104, 1552, 785, 1552, 0)
    for bound in (1, 2):
        assert accepted(enumerate_pointed_relations(bound)) == accepted(closed_form_census(bound))
    assert accepted(closed_form_census(1)) == PointedCensus(1, 2, 1, 0, 0, 0, 1, 0, 0)


def test_the_three_implications_on_the_exhaustive_census() -> None:
    census = accepted(enumerate_pointed_relations())
    assert census.related_not_distinct > 0
    assert census.distinct_not_related > 0
    assert census.irreflexive_related_not_distinct == 0


def test_explicit_countermodels_separate_relatedness_from_apartness() -> None:
    loop, empty = apartness_countermodels()
    assert accepted(pointed_predicates(loop)) == PointedPredicates(True, False, False)
    assert accepted(pointed_predicates(empty)) == PointedPredicates(False, True, True)


def test_irreflexive_relatedness_forces_distinct_poles_exhaustively() -> None:
    carrier = (0, 1, 2)
    pairs = tuple(product(carrier, repeat=2))
    for mask in range(1 << len(pairs)):
        relation = {pair for index, pair in enumerate(pairs) if mask >> index & 1}
        for first, second in pairs:
            seen = accepted(pointed_predicates(accepted(make_pointed_relation(carrier, relation, first, second))))
            if seen.related and seen.irreflexive:
                assert seen.distinct


@pytest.mark.parametrize(
    ("carrier", "relation", "first", "second", "code", "fragment"),
    [
        ((), set(), 0, 0, RefusalCode.INVALID_INPUT, "carrier"),
        ((0, 0), set(), 0, 0, RefusalCode.INVALID_INPUT, "distinct"),
        ([0, 1], set(), 0, 1, RefusalCode.INVALID_INPUT, "carrier"),
        ((0, 1), "01", 0, 1, RefusalCode.INVALID_INPUT, "collection"),
        ((0, 1), {0: 1}, 0, 1, RefusalCode.INVALID_INPUT, "collection"),
        ((0, 1), 7, 0, 1, RefusalCode.INVALID_INPUT, "collection"),
        ((0, 1), [(0, 1, 1)], 0, 1, RefusalCode.INVALID_INPUT, "not an ordered pair"),
        ((0, 1), [[0, 1]], 0, 1, RefusalCode.INVALID_INPUT, "not an ordered pair"),
        ((0, 1), [(0, 2)], 0, 1, RefusalCode.OUTSIDE_CARRIER, "leaves the carrier"),
        ((0, 1), [(2, 0)], 0, 1, RefusalCode.OUTSIDE_CARRIER, "leaves the carrier"),
        ((0, 1), [(0, 1)], 0, 2, RefusalCode.OUTSIDE_CARRIER, "poles"),
        ((0, 1), [(0, 1)], 3, 1, RefusalCode.OUTSIDE_CARRIER, "poles"),
    ],
)
def test_checker_refuses_non_relations_and_poles_outside(carrier, relation, first, second, code, fragment) -> None:
    refused(make_pointed_relation(carrier, relation, first, second), code, fragment)


def test_admitted_pointed_relation_is_normalized_and_tamper_is_refused() -> None:
    pointed = accepted(make_pointed_relation(("a", "b"), [("a", "b"), ("a", "b")], "a", "b"))
    assert pointed.relation == frozenset({("a", "b")})
    refused(pointed_predicates("not a relation"), RefusalCode.INVALID_INPUT)
    tampered = PointedRelation(("a", "b"), frozenset({("a", "c")}), "a", "b")
    refused(pointed_predicates(tampered), RefusalCode.OUTSIDE_CARRIER)


@pytest.mark.parametrize("bound", [0, -1, True, 2.0, "3"])
def test_census_bound_must_be_a_positive_integer(bound) -> None:
    refused(enumerate_pointed_relations(bound), RefusalCode.INVALID_INPUT)
    refused(closed_form_census(bound), RefusalCode.INVALID_INPUT)


def test_census_is_budgeted() -> None:
    refused(enumerate_pointed_relations(4), RefusalCode.BUDGET_EXHAUSTED, "<= 3")
    refused(closed_form_census(4), RefusalCode.BUDGET_EXHAUSTED)


# Executable finite evidence; AuthorityEffect: None.
