"""Finite definite Horn inference with independently checked task-bound witnesses."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass


def _index(value: int, size: int) -> bool:
    return type(value) is int and 0 <= value < size


@dataclass(frozen=True)
class Rule:
    premises: tuple[int, ...]
    conclusion: int


@dataclass(frozen=True)
class Theory:
    atoms: tuple[str, ...]
    facts: frozenset[int]
    rules: tuple[Rule, ...]

    def __post_init__(self) -> None:
        if (type(self.atoms) is not tuple or
                any(type(a) is not str or not a for a in self.atoms) or
                len(set(self.atoms)) != len(self.atoms)):
            raise ValueError("atoms must be distinct nonempty names")
        n = len(self.atoms)
        if type(self.facts) is not frozenset or any(not _index(a, n) for a in self.facts):
            raise ValueError("facts must be atom indices")
        if type(self.rules) is not tuple:
            raise ValueError("rules must be a tuple")
        for r in self.rules:
            if (type(r) is not Rule or type(r.premises) is not tuple or
                    not _index(r.conclusion, n) or
                    any(not _index(a, n) for a in r.premises)):
                raise ValueError("rules must refer to this atom carrier")

    def digest(self) -> str:
        payload = ["wdp-horn-v1", self.atoms, sorted(self.facts),
                   [[r.premises, r.conclusion] for r in self.rules]]
        return hashlib.sha256(json.dumps(payload, separators=(",", ":"),
                                         ensure_ascii=True).encode("ascii")).hexdigest()


@dataclass(frozen=True)
class ProofStep:
    conclusion: int
    rule: int | None
    premises: tuple[int, ...] = ()


@dataclass(frozen=True)
class Proof:
    theory_digest: str
    goal: int
    steps: tuple[ProofStep, ...]


@dataclass(frozen=True)
class Countermodel:
    theory_digest: str
    goal: int
    true_atoms: frozenset[int]


@dataclass(frozen=True)
class BudgetExhausted:
    additions: int


def check_proof(theory: Theory, goal: int, proof: Proof) -> bool:
    """Check each premise against an earlier step; never call the searcher."""
    if (not _index(goal, len(theory.atoms)) or type(proof) is not Proof or
            type(proof.goal) is not int or proof.goal != goal or
            proof.theory_digest != theory.digest() or type(proof.steps) is not tuple):
        return False
    known: list[int] = []
    for step in proof.steps:
        if (type(step) is not ProofStep or
                not _index(step.conclusion, len(theory.atoms)) or
                type(step.premises) is not tuple):
            return False
        if step.rule is None:
            if step.conclusion not in theory.facts or step.premises:
                return False
        else:
            if not _index(step.rule, len(theory.rules)):
                return False
            rule = theory.rules[step.rule]
            if (step.conclusion != rule.conclusion or
                    len(step.premises) != len(rule.premises) or
                    any(not _index(i, len(known)) for i in step.premises) or
                    tuple(known[i] for i in step.premises) != rule.premises):
                return False
        known.append(step.conclusion)
    return bool(known) and known[-1] == goal


def check_countermodel(theory: Theory, goal: int, model: Countermodel) -> bool:
    """A model omitting the goal certifies non-entailment, not world falsity."""
    if (not _index(goal, len(theory.atoms)) or type(model) is not Countermodel or
            type(model.goal) is not int or model.goal != goal or
            model.theory_digest != theory.digest() or
            type(model.true_atoms) is not frozenset or
            any(not _index(a, len(theory.atoms)) for a in model.true_atoms)):
        return False
    values = model.true_atoms
    return (goal not in values and theory.facts <= values and
            all(not all(a in values for a in r.premises) or r.conclusion in values
                for r in theory.rules))


def solve(theory: Theory, goal: int, budget: int | None = None) -> Proof | Countermodel | BudgetExhausted:
    """Saturate a finite carrier. Budget counts new atoms, not runtime or checking."""
    n = len(theory.atoms)
    if not _index(goal, n):
        raise ValueError("goal outside the atom carrier")
    if budget is None:
        budget = n
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    steps: list[ProofStep] = []
    positions: dict[int, int] = {}
    while True:
        candidate = next((ProofStep(a, None) for a in sorted(theory.facts)
                          if a not in positions), None)
        if candidate is None:
            for i, rule in enumerate(theory.rules):
                if rule.conclusion not in positions and all(a in positions for a in rule.premises):
                    candidate = ProofStep(rule.conclusion, i,
                                          tuple(positions[a] for a in rule.premises))
                    break
        if candidate is None:
            return Countermodel(theory.digest(), goal, frozenset(positions))
        if len(steps) == budget:
            return BudgetExhausted(len(steps))
        positions[candidate.conclusion] = len(steps)
        steps.append(candidate)
        if candidate.conclusion == goal:
            return Proof(theory.digest(), goal, tuple(steps))


def report_collision(reports: tuple[object, ...], answers: tuple[object, ...]) -> tuple[int, int] | None:
    """Return an actual target-separating fiber pair on the supplied world table."""
    if len(reports) != len(answers):
        raise ValueError("reports and answers must describe the same worlds")
    return next(((i, j) for i in range(len(reports)) for j in range(i)
                 if reports[i] == reports[j] and answers[i] != answers[j]), None)


def graph_theory(nodes: tuple[str, ...], edges: tuple[tuple[int, int], ...], start: int) -> Theory:
    """Atom i means a directed path from start to node i in this supplied graph."""
    if not _index(start, len(nodes)) or type(edges) is not tuple:
        raise ValueError("invalid graph source")
    if any(type(e) is not tuple or len(e) != 2 or
           any(not _index(a, len(nodes)) for a in e) for e in edges):
        raise ValueError("invalid edge")
    return Theory(nodes, frozenset({start}), tuple(Rule((a,), b) for a, b in edges))


def decode_path(nodes: tuple[str, ...], edges: tuple[tuple[int, int], ...],
                start: int, goal: int, proof: Proof) -> tuple[int, ...] | None:
    theory = graph_theory(nodes, edges, start)
    if not check_proof(theory, goal, proof):
        return None
    paths: list[tuple[int, ...]] = []
    for step in proof.steps:
        paths.append((start,) if step.rule is None else
                     paths[step.premises[0]] + (step.conclusion,))
    return paths[-1]


def check_path(nodes: tuple[str, ...], edges: tuple[tuple[int, int], ...],
               start: int, goal: int, path: tuple[int, ...]) -> bool:
    """Original graph checker: no access to Horn rules, certificates or solver."""
    return (type(path) is tuple and bool(path) and
            _index(start, len(nodes)) and _index(goal, len(nodes)) and
            all(_index(a, len(nodes)) for a in path) and
            path[0] == start and path[-1] == goal and
            all((a, b) in edges for a, b in zip(path, path[1:])))
