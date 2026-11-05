from dataclasses import replace

import pytest
from witnessed_difference.observer_world_adapter import FiniteObserverWorld


def world():
    return FiniteObserverWorld(("a",), ((), (0,), (0, 0)), ("same", "distinct"), (0, 0, 1),
                               ("separate",), ((0, 2, 2),), ((0, 1, 0),), ("first", "all"),
                               (frozenset({0}), frozenset({0, 1})))


def test_world_keeps_history_noncongruence_and_exact_source_facts():
    source = world()
    assert source.context_system().related(0, 1)
    assert source.context_system().obstruction() is not None
    assert source.facts() == frozenset({frozenset({0, 1})})
    assert source.verify_against(source)


def test_source_image_context_closure_and_actual_witness_are_required():
    with pytest.raises(ValueError, match="actual image"):
        replace(world(), profiles=("same", "distinct", "unused"))
    with pytest.raises(ValueError, match="closed"):
        replace(world(), context_actions=((0, 3, 2),))
    with pytest.raises(ValueError, match="does not replay"):
        replace(world(), witnesses=((0, 2, 0),))


def test_grammar_names_do_not_supply_facts_and_receipts_retain_interpretation():
    source = world()
    with pytest.raises(ValueError, match="expressibility"):
        replace(source, grammar_interpretation=None).facts()
    other = replace(source, grammar_interpretation=(frozenset(), frozenset({0, 1})))
    assert other.grammar == source.grammar
    assert len(other.facts()) == 2
    with pytest.raises(ValueError, match="bound"):
        source.verify_against(other)


def test_replay_rechecks_the_domain_even_for_equal_untrusted_payloads():
    untrusted = world()
    object.__setattr__(untrusted, "context_actions", ((0, 3, 2),))
    with pytest.raises(ValueError, match="closed"):
        untrusted.verify_against(untrusted)
