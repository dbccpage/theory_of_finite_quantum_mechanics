"""Replay of the recovered Lean fixtures (DirectTM, TokenCode, TapeTransition) against the Python twins.

Origin: lean4/AuthIncompleteness/{DirectTM,TokenCode,TapeTransition}.lean
Claim: urn:omega:fqm:authincomp:finite-models-twin-fixtures:v1
AuthorityEffect: None
Mutation-Kills: the malformed-code fixtures reject tag 2 / tag 3 / truncation / empty; the looping and
stuck fixtures distinguish fuel exhaustion from stuck from halt.
Scope Fence: fixture agreement with Lean is evidence of a faithful twin, not a theorem about all machines.
"""

from __future__ import annotations

import importlib
import json
import sys
import types
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
_pkg = types.ModuleType("staged_auth_incompleteness")
_pkg.__path__ = [str(REPO / "code/python/src/qm/auth_incompleteness")]
sys.modules.setdefault(_pkg.__name__, _pkg)
fm = importlib.import_module("staged_auth_incompleteness.finite_models")
rp = importlib.import_module("staged_auth_incompleteness.replay_packet")


def test_write_and_halt_fixture() -> None:
    cfg = fm.apply_rule(fm.WRITE_AND_HALT.rules[0], fm.INITIAL)
    assert cfg.read(0) == fm.MARKED
    assert fm.declared_halt(fm.WRITE_AND_HALT, cfg)
    assert fm.execute(fm.WRITE_AND_HALT, 1, fm.INITIAL) == ("halted", None)


def test_stuck_and_looping_fixtures_are_distinct_outcomes() -> None:
    assert fm.execute(fm.STUCK, 1, fm.INITIAL) == ("stuck", None)
    kind, cfg = fm.execute(fm.LOOPING, 1, fm.INITIAL)
    assert kind == "fuel_exhausted"
    assert cfg == fm.apply_rule(fm.LOOPING.rules[0], fm.INITIAL)
    # More fuel never turns the looping fixture into a halt: exhaustion is a bounded-evaluator result.
    assert fm.execute(fm.LOOPING, 10_000, fm.INITIAL)[0] == "fuel_exhausted"


def test_declared_halt_is_reported_at_any_fuel() -> None:
    halted = fm.Configuration(1, 0)
    for fuel in (0, 1, 7):
        assert fm.execute(fm.WRITE_AND_HALT, fuel, halted) == ("halted", None)


def test_zero_fuel_on_non_halt_exhausts() -> None:
    assert fm.execute(fm.WRITE_AND_HALT, 0, fm.INITIAL)[0] == "fuel_exhausted"


def test_left_biased_lookup() -> None:
    first = fm.Rule(0, fm.BLANK, 1, fm.MARKED, fm.STAY)
    second = fm.Rule(0, fm.BLANK, 2, fm.BLANK, fm.LEFT)
    assert fm.lookup(fm.Machine(1, (first, second)), fm.INITIAL) == first
    assert fm.lookup(fm.Machine(1, (second, first)), fm.INITIAL) == second


@pytest.mark.parametrize("machine", [fm.WRITE_AND_HALT, fm.STUCK, fm.LOOPING])
def test_token_code_round_trip(machine) -> None:
    assert fm.decode_machine(fm.encode_machine(machine)) == machine


def test_token_code_round_trip_exhaustive_small_space() -> None:
    rules = [fm.Rule(s, a, n, w, m) for s in (0, 1) for a in (0, 1) for n in (0, 2) for w in (0, 1) for m in (0, 1, 2)]
    for r in rules:
        machine = fm.Machine(3, (r,))
        assert fm.decode_machine(fm.encode_machine(machine)) == machine
    for r1 in rules[:8]:
        for r2 in rules[8:16]:
            machine = fm.Machine(5, (r1, r2))
            assert fm.decode_machine(fm.encode_machine(machine)) == machine


@pytest.mark.parametrize(
    "tokens",
    [[], [0, 0, 0, 1], [0, 0, 2, 1, 0, 0], [0, 0, 0, 1, 0, 3]],
    ids=["empty", "truncated", "invalid_symbol", "invalid_move"],
)
def test_malformed_codes_are_rejected(tokens) -> None:
    assert fm.decode_machine(tokens) is None


def test_header_only_code_is_the_empty_rule_machine() -> None:
    assert fm.decode_machine([4]) == fm.Machine(4, ())


def test_transition_table_matches_the_recovered_packet_proposal() -> None:
    proposal = json.loads((REPO / rp.map_path(rp.EXPECTED_ARTIFACT["proposal"]["path"], rp.PREFIX_MAP)).read_text(encoding="utf-8"))
    table = {row["from"]: (row["outcome"], row["to"]) for row in proposal["transitions"]}
    assert table == fm.TRANSITION


def test_contracts_and_adequacy_match_lean_theorems() -> None:
    assert fm.preserves(fm.CLEAN_TERMINAL) is True          # transition_preserves_clean_terminal_contract
    assert fm.preserves(fm.MARKED_CELL) is False            # transition_does_not_preserve_marked_cell_contract
    assert fm.adequate(lambda c: c, fm.MARKED_CELL) is True  # full_configuration_report_adequate_...
    assert fm.adequate(fm.control_report, fm.MARKED_CELL) is False  # control_report_not_adequate_...
    # The control report cannot decide the clean-terminal contract either: both 'stay' configurations differ.
    assert fm.adequate(fm.control_report, fm.CLEAN_TERMINAL) is False


def test_packet_countertraces_agree_with_the_twin() -> None:
    result = rp.invoke_replay_packet(REPO)
    twin = [c for c in fm.CONFIGURATIONS if fm.MARKED_CELL[c] and not fm.MARKED_CELL[fm.TRANSITION[c][1]]]
    assert [c["source"] for c in result["evaluation"]["marked_countertraces"]] == twin
