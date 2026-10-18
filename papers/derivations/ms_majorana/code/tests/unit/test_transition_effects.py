from __future__ import annotations

from dataclasses import replace

import pytest

from omega_engine.kernel.higher_operad import Err, Ok
from omega_engine.kernel.transition_effects import (
    EffectKind,
    EffectOwner,
    EventV1,
    FiniteTransitionSystemV1,
    effect_receipt,
    events_commute,
    semantic_effect_classes,
    solver_trace_allowed,
    trace_rewrite_equivalent,
)


def _system() -> FiniteTransitionSystemV1:
    states = ("s00", "s10", "s01", "s11", "terminal")
    return FiniteTransitionSystemV1(
        states=states,
        events=(
            EventV1(
                "event.admit-duplicate",
                EffectOwner.DECLARATION,
                EffectKind.ADMISSION,
                states,
            ),
            EventV1(
                "event.hash-noop",
                EffectOwner.SOLVER,
                EffectKind.SAME_LEVEL_REPAIR,
                states,
            ),
            EventV1(
                "event.set-a",
                EffectOwner.SOLVER,
                EffectKind.SAME_LEVEL_REPAIR,
                ("s10", "s10", "s11", "s11", "terminal"),
            ),
            EventV1(
                "event.set-b",
                EffectOwner.SOLVER,
                EffectKind.SAME_LEVEL_REPAIR,
                ("s01", "s11", "s01", "s11", "terminal"),
            ),
            EventV1(
                "event.extend-a",
                EffectOwner.SOLVER,
                EffectKind.STRUCTURE_EXTENSION,
                ("s10", "s10", "s11", "s11", "terminal"),
            ),
            EventV1(
                "event.budget",
                EffectOwner.HOST,
                EffectKind.BUDGET_CONTROL,
                states,
            ),
            EventV1(
                "event.license",
                EffectOwner.HOST,
                EffectKind.CAPABILITY_CONTROL,
                states,
            ),
            EventV1(
                "event.halt",
                EffectOwner.TERMINALIZER,
                EffectKind.TERMINAL,
                ("terminal", "terminal", "terminal", "terminal", "terminal"),
            ),
        ),
        terminal_states=("terminal",),
    )


def test_raw_semantic_equality_does_not_erase_governance() -> None:
    system = _system()
    raw = semantic_effect_classes(system, governed=False)
    governed = semantic_effect_classes(system, governed=True)
    raw_class = next(group for group in raw if "event.admit-duplicate" in group)
    assert "event.hash-noop" in raw_class
    governed_class = next(
        group for group in governed if "event.admit-duplicate" in group
    )
    assert "event.hash-noop" not in governed_class


def test_same_action_repair_and_extension_remain_different_effects() -> None:
    system = _system()
    raw = semantic_effect_classes(system, governed=False)
    governed = semantic_effect_classes(system, governed=True)
    assert any(
        "event.set-a" in group and "event.extend-a" in group for group in raw
    )
    assert not any(
        "event.set-a" in group and "event.extend-a" in group
        for group in governed
    )


def test_disjoint_solver_effects_commute_on_every_state() -> None:
    assert events_commute(_system(), "event.set-a", "event.set-b")


def test_commuting_trace_swap_is_replay_equivalent() -> None:
    result = trace_rewrite_equivalent(
        _system(),
        ("event.set-a", "event.set-b"),
        ("event.set-b", "event.set-a"),
    )
    assert isinstance(result, Ok)
    assert result.value


def test_replay_equivalence_is_checked_from_every_declared_state() -> None:
    result = trace_rewrite_equivalent(
        _system(),
        ("event.set-a",),
        ("event.set-b",),
    )
    assert isinstance(result, Ok)
    assert not result.value


def test_host_controls_cannot_be_renamed_by_state_only_equivalence() -> None:
    result = trace_rewrite_equivalent(
        _system(),
        ("event.budget",),
        ("event.license",),
    )
    assert isinstance(result, Ok)
    assert not result.value


def test_solver_trace_cannot_emit_host_or_terminalizer_events() -> None:
    allowed = solver_trace_allowed(_system(), ("event.set-a", "event.set-b"))
    budget = solver_trace_allowed(_system(), ("event.set-a", "event.budget"))
    halt = solver_trace_allowed(_system(), ("event.halt",))
    assert isinstance(allowed, Ok) and allowed.value
    assert isinstance(budget, Ok) and not budget.value
    assert isinstance(halt, Ok) and not halt.value


def test_terminal_is_absorbing_under_every_event() -> None:
    system = _system()
    for event in system.events:
        assert system.step("terminal", event.event_id) == "terminal"


def test_nonabsorbing_terminal_declaration_is_rejected() -> None:
    system = _system()
    broken = replace(
        system.events[0],
        transitions=("s00", "s10", "s01", "s11", "s00"),
    )
    with pytest.raises(ValueError, match="absorb"):
        FiniteTransitionSystemV1(
            states=system.states,
            events=(broken,) + system.events[1:],
            terminal_states=system.terminal_states,
        )


def test_effect_receipt_binds_transition_and_governance() -> None:
    system = _system()
    receipt = effect_receipt(system, "event.set-a")
    assert receipt.system_id == system.canonical_id
    assert receipt.kind is EffectKind.SAME_LEVEL_REPAIR
    assert receipt.owner is EffectOwner.SOLVER
    assert receipt.authority_effect.value == "None"


def test_unknown_event_fails_closed() -> None:
    replay = _system().replay("s00", ("event.unknown",))
    assert isinstance(replay, Err)
    assert replay.error.code == "TRACE_OUTSIDE_SYSTEM"


def test_malformed_trace_container_fails_closed() -> None:
    replay = _system().replay("s00", ["event.set-a"])
    assert isinstance(replay, Err)
    assert replay.error.code == "MALFORMED_TRACE"


def test_mutated_event_table_is_rejected_on_reconstruction() -> None:
    system = _system()
    event = system.events[0]
    object.__setattr__(event, "transitions", list(event.transitions))
    with pytest.raises(TypeError):
        EventV1(
            event.event_id,
            event.owner,
            event.kind,
            event.transitions,
        )


def test_trace_kind_multiset_is_preserved_even_when_state_action_matches() -> None:
    result = trace_rewrite_equivalent(
        _system(),
        ("event.set-a",),
        ("event.extend-a",),
    )
    assert isinstance(result, Ok)
    assert not result.value
