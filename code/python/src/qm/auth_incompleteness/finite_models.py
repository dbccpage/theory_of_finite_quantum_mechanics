"""Executable twins of the recovered finite Lean models (DTM0, DTM1 token code, tape transition table).

Origin: lean4/AuthIncompleteness/{DirectTM,TokenCode,TapeTransition}.lean (ported 2026-10-21 from
C:/.ana/coda_university/coda_research/authorization_an_incompleteness_theory/formal).
Claim: urn:omega:fqm:authincomp:finite-models-python-twin:v1
AuthorityEffect: None

DTM0 is a finite rule list over a two-symbol alphabet with a total (here: sparse, finitely
overridden) integer tape, a designated halt state, left-biased rule lookup and a fuel-bounded
evaluator whose results are halted / stuck / fuel_exhausted. DTM1 is the List-Nat token grammar
`halt_state, (state, scanned, next, written, move)*` with an all-consuming decoder. The transition
table is the four-configuration model with the clean-terminal and marked-cell contracts.

These twins replay the Lean fixtures; they do not extend the Lean statements. DTM0 here is NOT
claimed equivalent to Mathlib's Turing.TM0, is not proved universal, and fuel exhaustion is not
non-halting.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

BLANK, MARKED = 0, 1  # token tags used by the DTM1 grammar
LEFT, RIGHT, STAY = 0, 1, 2

Result = Literal["halted", "stuck", "fuel_exhausted"]


@dataclass(frozen=True)
class Rule:
    state: int
    scanned: int
    next_state: int
    write: int
    move: int


@dataclass(frozen=True)
class Machine:
    halt_state: int
    rules: tuple[Rule, ...] = ()


@dataclass(frozen=True)
class Configuration:
    state: int
    head: int
    overrides: tuple[tuple[int, int], ...] = field(default_factory=tuple)  # blank everywhere else

    def read(self, position: int) -> int:
        return dict(self.overrides).get(position, BLANK)


def declared_halt(machine: Machine, configuration: Configuration) -> bool:
    return configuration.state == machine.halt_state


def lookup(machine: Machine, configuration: Configuration) -> Rule | None:
    scanned = configuration.read(configuration.head)
    for rule in machine.rules:  # left-biased, as List.find?
        if rule.state == configuration.state and rule.scanned == scanned:
            return rule
    return None


def apply_rule(rule: Rule, configuration: Configuration) -> Configuration:
    tape = dict(configuration.overrides)
    tape[configuration.head] = rule.write
    delta = {LEFT: -1, RIGHT: 1, STAY: 0}[rule.move]
    return Configuration(rule.next_state, configuration.head + delta, tuple(sorted(tape.items())))


def execute(machine: Machine, fuel: int, configuration: Configuration) -> tuple[Result, Configuration | None]:
    """Mirror of `execute`: halt test first, then one lookup+apply per unit of fuel."""
    while True:
        if declared_halt(machine, configuration):
            return "halted", None
        if fuel == 0:
            return "fuel_exhausted", configuration
        rule = lookup(machine, configuration)
        if rule is None:
            return "stuck", None
        configuration = apply_rule(rule, configuration)
        fuel -= 1


WRITE_AND_HALT = Machine(1, (Rule(0, BLANK, 1, MARKED, STAY),))
STUCK = Machine(1, ())
LOOPING = Machine(1, (Rule(0, BLANK, 0, BLANK, STAY),))
INITIAL = Configuration(0, 0)


def encode_machine(machine: Machine) -> list[int]:
    out = [machine.halt_state]
    for r in machine.rules:
        out += [r.state, r.scanned, r.next_state, r.write, r.move]
    return out


def decode_machine(tokens: list[int]) -> Machine | None:
    """All-consuming parser: rejects empty input, truncated frames and invalid tags."""
    if not tokens:
        return None
    body = tokens[1:]
    if len(body) % 5 != 0:
        return None
    rules = []
    for i in range(0, len(body), 5):
        state, scanned, nxt, written, move = body[i:i + 5]
        if scanned not in (BLANK, MARKED) or written not in (BLANK, MARKED) or move not in (LEFT, RIGHT, STAY):
            return None
        rules.append(Rule(state, scanned, nxt, written, move))
    return Machine(tokens[0], tuple(rules))


CONFIGURATIONS = ("runningBlank", "runningMarked", "haltedBlank", "haltedMarked")
TRANSITION: dict[str, tuple[str, str]] = {  # configuration -> (outcome, next)
    "runningBlank": ("halt", "haltedBlank"),
    "runningMarked": ("advance", "runningBlank"),
    "haltedBlank": ("stay", "haltedBlank"),
    "haltedMarked": ("stay", "haltedBlank"),
}
CLEAN_TERMINAL = {"runningBlank": True, "runningMarked": True, "haltedBlank": True, "haltedMarked": False}
MARKED_CELL = {"runningBlank": False, "runningMarked": True, "haltedBlank": False, "haltedMarked": True}


def preserves(contract: dict[str, bool]) -> bool:
    return all(not contract[c] or contract[TRANSITION[c][1]] for c in CONFIGURATIONS)


def adequate(report, contract: dict[str, bool]) -> bool:
    """A report is adequate iff the contract is constant on every report fiber."""
    return all(contract[a] == contract[b] for a in CONFIGURATIONS for b in CONFIGURATIONS if report(a) == report(b))


def control_report(configuration: str) -> str:
    return TRANSITION[configuration][0]
