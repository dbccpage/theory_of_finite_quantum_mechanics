from fractions import Fraction
from itertools import product

import pytest
from witnessed_difference.context_witness import (
    ContextualSystem,
    ContextWitness,
    apply_coordinate_change,
    contextual_congruence,
    critical_context_witnesses,
    relabel,
    witness_rank,
)
from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused

STATES = ("a", "b", "c", "d", "e", "f")
PROFILE = {"a": (0, 0), "b": (0, 0), "c": (1, 0), "d": (0, 1), "e": (2, 2), "f": ("2", 2)}
CONTEXTS = {
    "t": {"a": "c", "b": "d", "c": "c", "d": "d", "e": "e", "f": "f"},
    "u": {"a": "a", "b": "b", "c": "c", "d": "d", "e": "c", "f": "a"},
}


def accepted(outcome):
    assert isinstance(outcome, Accepted), outcome
    assert outcome.authority_effect is AuthorityEffect.NONE
    return outcome.value


def refused(outcome, code: RefusalCode, fragment: str = "") -> Refused:
    assert isinstance(outcome, Refused), outcome
    assert outcome.code is code, outcome
    assert fragment in outcome.detail, outcome.detail
    return outcome


def system() -> ContextualSystem:
    return ContextualSystem(STATES, CONTEXTS, PROFILE)


def test_contextual_congruence_and_critical_witnesses() -> None:
    source = system()
    assert source.dimension == 2 and source.profile["f"] == (Fraction(2), Fraction(2))
    classes = accepted(contextual_congruence(source))
    assert classes == (frozenset("ab"), frozenset("c"), frozenset("d"), frozenset("ef"))
    witnesses = accepted(critical_context_witnesses(source))
    assert witnesses == (
        ContextWitness("a", "b", "t", (Fraction(1), Fraction(-1))),
        ContextWitness("e", "f", "u", (Fraction(1), Fraction(0))),
    )
    for witness in witnesses:
        assert source.profile[witness.x] == source.profile[witness.y]
        assert all(type(value) is Fraction for value in witness.exposed)
    assert accepted(witness_rank(source)) == 2


def test_a_congruence_complete_system_has_no_witnesses() -> None:
    collapsing = {"t": dict.fromkeys(STATES, "a")}
    complete = ContextualSystem(STATES, collapsing, PROFILE)
    assert accepted(critical_context_witnesses(complete)) == ()
    assert accepted(witness_rank(complete)) == 0
    assert accepted(witness_rank(ContextualSystem(STATES, {}, PROFILE))) == 0


def test_witness_rank_is_invariant_under_every_small_invertible_coordinate_change() -> None:
    source = system()
    base = accepted(critical_context_witnesses(source))
    checked = 0
    for a, b, c, d in product((-1, 0, 1, 2), repeat=4):
        matrix = ((a, b), (c, d))
        if a * d - b * c == 0:
            refused(apply_coordinate_change(source, matrix), RefusalCode.NOT_INVERTIBLE)
            continue
        moved = accepted(apply_coordinate_change(source, matrix))
        assert accepted(witness_rank(moved)) == 2
        witnesses = accepted(critical_context_witnesses(moved))
        assert [(w.x, w.y, w.context) for w in witnesses] == [(w.x, w.y, w.context) for w in base]
        for old, new in zip(base, witnesses):
            assert new.exposed == (a * old.exposed[0] + b * old.exposed[1], c * old.exposed[0] + d * old.exposed[1])
        checked += 1
    assert checked > 100


def test_rational_coordinate_change_and_its_refusals() -> None:
    source = system()
    moved = accepted(apply_coordinate_change(source, (("1/2", "1/3"), (0, "-7/5"))))
    assert accepted(witness_rank(moved)) == 2
    refused(apply_coordinate_change(source, ((1, 0),)), RefusalCode.INVALID_INPUT)
    refused(apply_coordinate_change(source, ((1, 0), (0,))), RefusalCode.INVALID_INPUT)
    refused(apply_coordinate_change(source, ((1.0, 0), (0, 1))), RefusalCode.INVALID_INPUT)
    refused(apply_coordinate_change("system", ((1,),)), RefusalCode.INVALID_INPUT)


def test_witness_rank_is_invariant_under_admissible_relabeling() -> None:
    source = system()
    states = {state: f"s{index}" for index, state in enumerate(reversed(STATES))}
    contexts = {"t": "tau", "u": "upsilon"}
    moved = accepted(relabel(source, states, contexts))
    assert accepted(witness_rank(moved)) == accepted(witness_rank(source))
    transported = {
        (frozenset({states[w.x], states[w.y]}), contexts[w.context]) for w in accepted(critical_context_witnesses(source))
    }
    assert {(frozenset({w.x, w.y}), w.context) for w in accepted(critical_context_witnesses(moved))} == transported


@pytest.mark.parametrize(
    ("state_map", "context_map"),
    [
        (dict.fromkeys(STATES, "same"), {"t": "t", "u": "u"}),
        ({"a": "a"}, {"t": "t", "u": "u"}),
        ({state: state for state in STATES}, {"t": "x", "u": "x"}),
        ({state: state for state in STATES}, {"t": "", "u": "u"}),
        ({state: state for state in STATES}, "names"),
    ],
)
def test_non_admissible_relabelings_are_refused(state_map, context_map) -> None:
    refused(relabel(system(), state_map, context_map), RefusalCode.INVALID_INPUT)


def test_every_operation_refuses_a_non_system() -> None:
    for outcome in (
        contextual_congruence("S"),
        critical_context_witnesses("S"),
        witness_rank("S"),
        relabel("S", {}, {}),
    ):
        refused(outcome, RefusalCode.INVALID_INPUT)


@pytest.mark.parametrize(
    ("states", "contexts", "profile"),
    [
        (("a", "a"), {}, {"a": (0,)}),
        ((), {}, {}),
        (["a"], {}, {"a": (0,)}),
        (("a", "b"), {"t": {"a": "a"}}, {"a": (0,), "b": (0,)}),
        (("a", "b"), {"t": {"a": "z", "b": "a"}}, {"a": (0,), "b": (0,)}),
        (("a", "b"), {"": {"a": "a", "b": "b"}}, {"a": (0,), "b": (0,)}),
        (("a", "b"), "contexts", {"a": (0,), "b": (0,)}),
        (("a", "b"), {}, {"a": (0,)}),
        (("a", "b"), {}, {"a": (0,), "b": (0, 1)}),
        (("a",), {}, {"a": ()}),
    ],
)
def test_contextual_system_validation(states, contexts, profile) -> None:
    with pytest.raises(ValueError):
        ContextualSystem(states, contexts, profile)


def test_float_profiles_are_refused() -> None:
    with pytest.raises(TypeError):
        ContextualSystem(("a",), {}, {"a": (0.5,)})


def test_strings_are_not_read_as_digit_sequences() -> None:
    from witnessed_difference.context_witness import ContextualSystem, apply_coordinate_change

    contexts = {"swap": {"a": "b", "b": "a"}}
    with pytest.raises(TypeError, match="not a string"):
        ContextualSystem(("a", "b"), contexts, {"a": "12", "b": (1, 2)})
    system = ContextualSystem(("a", "b"), contexts, {"a": (1, 2), "b": (2, 1)})
    for matrix in (["10", "01"], "1001"):
        assert isinstance(apply_coordinate_change(system, matrix), Refused)
    assert isinstance(apply_coordinate_change(system, [[1, 0], [0, 1]]), Accepted)


def test_contextual_system_inner_dict_is_immutable() -> None:
    source = system()
    with pytest.raises(TypeError):
        source.contexts["t"]["a"] = "b"
    with pytest.raises(TypeError):
        source.profile["a"] = (1, 1)


# Executable finite evidence; AuthorityEffect: None.
