from itertools import product

import pytest
from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused
from witnessed_difference.presentation_descent import (
    Factorization,
    all_sections,
    count_factorizations,
    factor_through,
    obstruction_set,
    section_test,
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


DOMAIN = (0, 1, 2, 3)
CODOMAIN = ("p", "q")


def test_descent_uniqueness_and_sections_exhaustively_on_small_surjections() -> None:
    cases = 0
    for images in product(CODOMAIN, repeat=len(DOMAIN)):
        quotient = dict(zip(DOMAIN, images))
        if set(images) != set(CODOMAIN):
            continue
        sections = accepted(all_sections(DOMAIN, CODOMAIN, quotient))
        assert len(sections) == images.count("p") * images.count("q")
        for values in product((0, 1, 2), repeat=len(DOMAIN)):
            target = dict(zip(DOMAIN, values))
            obstruction = accepted(obstruction_set(DOMAIN, CODOMAIN, quotient, target))
            factored = factor_through(DOMAIN, CODOMAIN, quotient, target)
            assert isinstance(factored, Accepted) == (not obstruction)
            if isinstance(factored, Accepted):
                factor = dict(factored.value.factor)
                assert all(factor[quotient[x]] == target[x] for x in DOMAIN)
                assert factored.value.unique
                assert accepted(count_factorizations(DOMAIN, CODOMAIN, quotient, target, (0, 1, 2))) == 1
            else:
                refused(factored, RefusalCode.DOES_NOT_DESCEND, "obstruction pair")
                assert accepted(count_factorizations(DOMAIN, CODOMAIN, quotient, target, (0, 1, 2))) == 0
            for section in sections:
                record = accepted(section_test(DOMAIN, CODOMAIN, quotient, target, dict(section)))
                assert record.zero_defect == record.obstruction_empty == (not obstruction)
                cases += 1
    assert cases > 1000


def test_forgotten_bit_does_not_descend() -> None:
    states = ((0, 0), (0, 1), (1, 0), (1, 1))
    quotient = {state: state[0] for state in states}
    transported = {state: (state[1], state[0])[0] for state in states}
    obstruction = accepted(obstruction_set(states, (0, 1), quotient, transported))
    assert ((0, 0), (0, 1)) in obstruction and ((0, 1), (0, 0)) in obstruction
    refused(factor_through(states, (0, 1), quotient, transported), RefusalCode.DOES_NOT_DESCEND)
    remembered = {state: state[0] for state in states}
    assert accepted(factor_through(states, (0, 1), quotient, remembered)) == Factorization(((0, 0), (1, 1)), True)


def test_without_surjectivity_the_factor_is_not_unique_and_sections_do_not_exist() -> None:
    quotient, target = {0: "a"}, {0: 0}
    assert accepted(count_factorizations((0,), ("a", "b"), quotient, target, (0, 1))) == 2
    refused(factor_through((0,), ("a", "b"), quotient, target), RefusalCode.NOT_SURJECTIVE, "not unique")
    refused(all_sections((0,), ("a", "b"), quotient), RefusalCode.NOT_SURJECTIVE)
    refused(section_test((0,), ("a", "b"), quotient, target, {"a": 0, "b": 0}), RefusalCode.NOT_SURJECTIVE)
    assert accepted(obstruction_set((0,), ("a", "b"), quotient, target)) == frozenset()


@pytest.mark.parametrize(
    ("domain", "codomain", "quotient", "target", "code"),
    [
        ([0, 1], ("p",), {0: "p", 1: "p"}, {0: 0, 1: 0}, RefusalCode.INVALID_INPUT),
        ((0, 0), ("p",), {0: "p"}, {0: 0}, RefusalCode.INVALID_INPUT),
        ((0, [1]), ("p",), {0: "p"}, {0: 0}, RefusalCode.INVALID_INPUT),
        ((0, 1), ("p", "p"), {0: "p", 1: "p"}, {0: 0, 1: 0}, RefusalCode.INVALID_INPUT),
        ((0, 1), ("p",), {0: "p"}, {0: 0, 1: 0}, RefusalCode.INVALID_INPUT),
        ((0, 1), ("p",), [("p", "p")], {0: 0, 1: 0}, RefusalCode.INVALID_INPUT),
        ((0, 1), ("p",), {0: "p", 1: "p"}, {0: 0}, RefusalCode.INVALID_INPUT),
        ((0, 1), ("p",), {0: "p", 1: "z"}, {0: 0, 1: 0}, RefusalCode.OUTSIDE_CARRIER),
    ],
)
def test_declared_map_refusals(domain, codomain, quotient, target, code) -> None:
    refused(obstruction_set(domain, codomain, quotient, target), code)
    refused(factor_through(domain, codomain, quotient, target), code)
    refused(count_factorizations(domain, codomain, quotient, target, (0, 1)), code)
    refused(section_test(domain, codomain, quotient, target, {"p": 0}), code)


def test_section_and_census_refusals() -> None:
    quotient, target = {0: "p", 1: "p", 2: "q"}, {0: 0, 1: 0, 2: 1}
    domain, codomain = (0, 1, 2), ("p", "q")
    refused(all_sections([0], codomain, quotient), RefusalCode.INVALID_INPUT)
    for bad in ({"p": 2, "q": 2}, {"p": 0}, {"p": 7, "q": 2}, [("p", 0), ("q", 2)]):
        refused(section_test(domain, codomain, quotient, target, bad), RefusalCode.INVALID_INPUT, "not a section")
    refused(count_factorizations(domain, codomain, quotient, target, [0, 1]), RefusalCode.INVALID_INPUT, "value set")
    refused(count_factorizations(domain, codomain, quotient, target, (0, 0)), RefusalCode.INVALID_INPUT, "value set")
    refused(count_factorizations(domain, codomain, quotient, target, tuple(range(65))), RefusalCode.BUDGET_EXHAUSTED)
    record = accepted(section_test(domain, codomain, quotient, {0: 0, 1: 1, 2: 1}, {"p": 0, "q": 2}))
    assert record.defect == frozenset({1}) and not record.zero_defect and not record.obstruction_empty
    assert record.section == (("p", 0), ("q", 2))


def test_the_section_census_is_budgeted() -> None:
    domain = tuple(range(26))
    codomain = tuple(range(13))
    quotient = {x: x // 2 for x in domain}
    refused(all_sections(domain, codomain, quotient), RefusalCode.BUDGET_EXHAUSTED, "section census")
    smaller = {x: x // 2 for x in domain[:24]}
    assert len(accepted(all_sections(domain[:24], codomain[:12], smaller))) == 4096


# Executable finite evidence; AuthorityEffect: None.
