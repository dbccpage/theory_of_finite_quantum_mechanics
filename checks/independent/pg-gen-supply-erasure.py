"""Exact independent five-coordinate Genesis replay audit. AuthorityEffect: None.

No repository imports. Two transition implementations, partial failure,
state-dependent token erasure, and all supply-filtered histories are compared.
The general representation theorem is in Lean; this census has printed bounds.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import json
from typing import Callable, Literal

import sympy as sp  # type: ignore[import-untyped]

Kind = Literal["supply", "datum", "form", "inst", "rule", "impose"]
Instance = tuple[int, tuple[int, ...]]
Pair = tuple[int, int]
State = tuple[int, tuple[int, ...], tuple[Instance, ...], tuple[int, ...], tuple[Pair, ...]]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


@dataclass(frozen=True)
class Event:
    kind: Kind
    a: int = 0
    b: int = 0
    args: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if self.kind not in ("supply", "datum", "form", "inst", "rule", "impose"):
            raise ValueError("unknown event")
        if any(type(x) is not int or x < 0 for x in (self.a, self.b, *self.args)):
            raise ValueError("exact natural event coordinates required")
        if type(self.args) is not tuple:
            raise ValueError("immutable argument tuple required")


def step(r: State, e: Event) -> State | None:
    n, fs, ins, rules, qs = r
    if e.kind == "supply":
        return r
    if e.kind == "datum":
        return n + 1, fs, ins, rules, qs
    if e.kind == "form":
        return (n, (*fs, e.a), ins, rules, qs) if e.a >= 1 else None
    if e.kind == "inst":
        if not (e.a < len(fs) and len(e.args) == fs[e.a] and all(x < n for x in e.args)):
            return None
        item = (e.a, e.args)
        return n, fs, ins if item in ins else (*ins, item), rules, qs
    if e.kind == "rule":
        if e.a >= len(fs):
            return None
        return n, fs, ins, rules if e.a in rules else (*rules, e.a), qs
    if not e.a < e.b < n:
        return None
    q = (e.a, e.b)
    return n, fs, ins, rules, qs if q in qs else (*qs, q)


def array_step(r: State, e: Event) -> State | None:
    """Separate mutable-coordinate implementation, not a call to step()."""
    data, forms, instances, uniform, requirements = r
    f, i, u, q = list(forms), list(instances), list(uniform), list(requirements)
    if e.kind in ("form", "inst", "rule", "impose"):
        guards = {"form": e.a > 0,
                  "inst": e.a in range(len(f)) and len(e.args) == (f[e.a] if e.a < len(f) else 0)
                          and set(e.args).issubset(range(data)),
                  "rule": e.a in range(len(f)),
                  "impose": e.a in range(e.b) and e.b in range(data)}
        if not guards[e.kind]:
            return None
    if e.kind == "datum":
        data += 1
    elif e.kind == "form":
        f.append(e.a)
    elif e.kind == "inst" and (e.a, e.args) not in i:
        i.append((e.a, e.args))
    elif e.kind == "rule" and e.a not in u:
        u.append(e.a)
    elif e.kind == "impose" and (e.a, e.b) not in q:
        q.append((e.a, e.b))
    return data, tuple(f), tuple(i), tuple(u), tuple(q)


def replay(h: tuple[Event, ...], base: State, arrays: bool = False) -> State | None:
    state: State | None = base
    transition = array_step if arrays else step
    for e in h:
        if state is None:
            return None
        state = transition(state, e)
    return state


def potential(r: State) -> int:
    return r[0] + sum(len(xs) for xs in r[1:])


ALPHABET = (Event("supply", 7), Event("datum"), Event("form", 0), Event("form", 1),
            Event("form", 2), Event("inst", 0, args=()), Event("inst", 0, args=(0,)),
            Event("inst", 0, args=(1,)), Event("inst", 0, args=(0, 1)),
            Event("rule", 0), Event("rule", 2), Event("impose", 0, 1), Event("impose", 1, 0))
EMPTY: State = (0, (), (), (), ())
READING_L: State = (2, (), (), (), ((0, 1),))
READING_F: State = (3, (), (), (), ((1, 2),))


def history_census() -> tuple[int, int, set[State]]:
    cases = failures = 0
    seen: set[State] = set()
    for base in (EMPTY, READING_L, READING_F):
        for length in range(5):
            for history in product(ALPHABET, repeat=length):
                answer = replay(history, base)
                require(answer == replay(history, base, True), "array/source replay disagreement")
                filtered = tuple(e for e in history if e.kind != "supply")
                require(answer == replay(filtered, base), "supply erasure changed result or failure")
                cases += 1
                failures += answer is None
                if answer is not None:
                    seen.add(answer)
    expected = 3 * sum(sp.Integer(len(ALPHABET))**k for k in range(5))
    require(cases == expected, "history census count")
    return cases, failures, seen


def check_state_changes(seen: set[State]) -> int:
    changed = 0
    for r in seen:
        require(potential(r) == sp.Matrix([r[0], *(len(xs) for xs in r[1:])]).dot(sp.ones(5, 1)),
                "independent exact potential")
        for e in ALPHABET:
            s = step(r, e)
            require(s == array_step(r, e), "one-step coordinate disagreement")
            if s is not None:
                require(potential(r) <= potential(s), "potential decreased")
                if s != r:
                    require(potential(r) < potential(s), "real source change did not raise potential")
                    changed += 1
    return changed


def token_history_census() -> int:
    # Token-aware replay and state-dependent erasure: repeated tokens become supply.
    token_cases = 0
    token_alphabet = (Event("supply", 0), Event("datum", 0), Event("datum", 1),
                      Event("form", 0), Event("form", 1), Event("inst", 0, args=(0,)),
                      Event("rule", 0), Event("impose", 0, 1))
    for length in range(5):
        for history in product(token_alphabet, repeat=length):
            tokens: tuple[int, ...] = ()
            erased: list[Event] = []
            token_state: State | None = EMPTY
            for e in history:
                if token_state is None:
                    break
                ee = Event("supply", e.a) if e.kind == "datum" and e.a in tokens else e
                if e.kind == "datum" and e.a not in tokens:
                    tokens = (*tokens, e.a)
                erased.append(ee)
                token_state = step(token_state, ee)
            require(token_state == replay(tuple(erased), EMPTY, True), "state-dependent token erasure")
            token_cases += 1
    require(token_cases == sum(sp.Integer(len(token_alphabet))**k for k in range(5)), "token census")
    return token_cases


def negative_controls() -> tuple[tuple[str, State | None, State | None], ...]:
    # Fixed incorrect-output probes compare proposed results with independent references.
    # These probes do not execute altered source programs or measure mutation coverage.
    repeated = (Event("datum"), Event("form", 1), Event("inst", args=(0,)), Event("inst", args=(0,)))
    dup = replay(repeated, EMPTY)
    rules = replay((Event("form", 1), Event("rule", 0)), EMPTY)
    if dup is None or rules is None:
        raise RuntimeError("negative-control fixture failed admission")
    probes: tuple[tuple[str, State | None, State | None], ...] = (
        ("supply-admits", (1, (), (), (), ()), replay((Event("supply", 0),), EMPTY)),
        ("failure-as-noop", replay((Event("datum"),), EMPTY),
         replay((Event("form", 0), Event("datum")), EMPTY)),
        ("duplicate-append", (dup[0], dup[1], (*dup[2], dup[2][0]), dup[3], dup[4]), dup),
        ("unordered-requirement", replay((Event("impose", 0, 1),), READING_L),
         replay((Event("impose", 1, 0),), READING_L)),
        ("state-independent-token-erasure", replay((Event("datum", 0), Event("datum", 0)), EMPTY),
         replay((Event("datum", 0), Event("supply", 0)), EMPTY)),
        ("omit-rule-coordinate", (rules[0], rules[1], rules[2], (), rules[4]), rules))
    for name, proposed, reference in probes:
        require(proposed != reference, name + " was not a negative control")
    return probes


def malformed_event_refusals() -> int:
    refused = 0
    bad_inputs: tuple[Callable[[], Event], ...] = (
        lambda: Event("datum", True), lambda: Event("inst", -1), lambda: Event("form", False))
    for bad in bad_inputs:
        try:
            bad()
        except ValueError:
            refused += 1
        else:
            raise RuntimeError("malformed event admitted")
    return refused


def main() -> None:
    cases, failures, seen = history_census()
    changed = check_state_changes(seen)
    token_cases = token_history_census()
    probes = negative_controls()
    refused = malformed_event_refusals()
    print(json.dumps({"node": "PG-GEN-SUPPLY-ERASURE", "authority_effect": "None",
                      "alphabet_size": len(ALPHABET), "maximum_history_length": 4,
                      "bases": 3, "histories_checked": cases, "failed_histories": failures,
                      "distinct_successful_states": len(seen), "strict_changes_checked": changed,
                      "token_histories_checked": token_cases, "domain_refusals": refused,
                      "negative_controls": [{"name": name, "outcome": "rejected", "proposed": m, "reference": r}
                                            for name, m, r in probes],
                      "negative_control_count": len(probes),
                      "mutation_coverage": "not measured by these fixed-output probes"}, indent=2))


if __name__ == "__main__":
    main()
