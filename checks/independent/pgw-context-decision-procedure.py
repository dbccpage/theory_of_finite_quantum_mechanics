"""Independent exact finite Genesis context audit; no repository imports.

AuthorityEffect: None. The Lean theorem is general in the finite regime; this
checker exhausts the explicitly printed small domains and selected larger cases.
All arithmetic is integer arithmetic. Enumeration is output-sensitive and can
be exponential in compact arity; the executable rejects oversized inputs.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import json
from typing import Callable

import sympy as sp  # type: ignore[import-untyped]

Slot = int | None
Context = tuple[int, tuple[Slot, ...]]
Instance = tuple[int, tuple[int, ...]]


class DomainError(ValueError):
    """Malformed or out-of-envelope regime."""


class CheckFailure(RuntimeError):
    """A claimed identity, witness or refusal failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


@dataclass(frozen=True)
class Regime:
    data: int
    forms: tuple[int, ...]
    instances: frozenset[Instance]
    rules: frozenset[int]

    def __post_init__(self) -> None:
        if type(self.data) is not int or not 0 <= self.data <= 3:
            raise DomainError("data must be an integer in the declared envelope")
        if type(self.forms) is not tuple or len(self.forms) > 3:
            raise DomainError("forms must be a finite immutable tuple")
        if any(type(a) is not int or not 1 <= a <= 4 for a in self.forms):
            raise DomainError("arity must be a positive integer in the declared envelope")
        if sum((self.data + 1)**a for a in self.forms) > 5000:
            raise DomainError("slot enumeration exceeds the executable envelope")
        if type(self.instances) is not frozenset or type(self.rules) is not frozenset:
            raise DomainError("instances and rules must be immutable sets")
        for inst in self.instances:
            self.validate_instance(inst)
        if any(type(f) is not int or not 0 <= f < len(self.forms) for f in self.rules):
            raise DomainError("rule must name an admitted form")

    def validate_instance(self, inst: Instance) -> None:
        if type(inst) is not tuple or len(inst) != 2:
            raise DomainError("instance must be a form/argument pair")
        f, args = inst
        if type(f) is not int or not 0 <= f < len(self.forms):
            raise DomainError("instance form is not admitted")
        if type(args) is not tuple or len(args) != self.forms[f]:
            raise DomainError("instance argument arity mismatch")
        if any(type(d) is not int or not 0 <= d < self.data for d in args):
            raise DomainError("instance argument is not an admitted datum")


def contexts(regime: Regime) -> tuple[Context, ...]:
    """Cartesian route corresponding to the Lean recursive enumerator."""
    options: tuple[Slot, ...] = (None, *range(regime.data))
    return tuple((f, slots) for f, arity in enumerate(regime.forms)
                 for slots in product(options, repeat=arity) if None in slots)


def observes(regime: Regime, context: Context, datum: int, ignore_rules: bool = False) -> bool:
    f, slots = context
    instance = (f, tuple(datum if s is None else s for s in slots))
    return (f in regime.rules and not ignore_rules) or instance in regime.instances


def oracle(regime: Regime) -> dict[Context, tuple[bool, ...]]:
    """Independent route: nonempty hole masks and assignments to fixed positions.

    This route does not call contexts(), observes(), or a shared plugging helper.
    """
    result: dict[Context, tuple[bool, ...]] = {}
    for f, arity in enumerate(regime.forms):
        for mask in range(1, 1 << arity):
            fixed = tuple(j for j in range(arity) if not mask & (1 << j))
            for values in product(range(regime.data), repeat=len(fixed)):
                binding = dict(zip(fixed, values))
                slots = tuple(None if mask & (1 << j) else binding[j] for j in range(arity))
                bits = []
                for datum in range(regime.data):
                    ground = tuple(datum if mask & (1 << j) else binding[j] for j in range(arity))
                    bits.append(f in regime.rules or (f, ground) in regime.instances)
                result[f, slots] = tuple(bits)
    return result


def verify(regime: Regime) -> dict[str, object]:
    cs = contexts(regime)
    truth = oracle(regime)
    require(len(cs) == len(set(cs)), "duplicate context")
    require(set(cs) == set(truth), "context coverage differs from hole-mask construction")
    exact_count = sum((sp.Integer(regime.data) + 1)**a - sp.Integer(regime.data)**a
                      for a in regime.forms)
    require(len(cs) == exact_count, "context count polynomial mismatch")
    profiles = tuple(frozenset(c for c in cs if observes(regime, c, d)) for d in range(regime.data))
    oracle_profiles = tuple(frozenset(c for c, bits in truth.items() if bits[d])
                            for d in range(regime.data))
    require(profiles == oracle_profiles, "derivability or plugging mismatch")
    # Construct the quotient a second way by grouping equal oracle truth vectors.
    groups: list[list[int]] = []
    for datum in range(regime.data):
        for group in groups:
            if all(bits[datum] == bits[group[0]] for bits in truth.values()):
                group.append(datum)
                break
        else:
            groups.append([datum])
    require(len(set(profiles)) == len(groups), "class count differs from quotient partition")
    witnesses: list[dict[str, object]] = []
    for i, j in product(range(regime.data), repeat=2):
        first = next((c for c in cs if observes(regime, c, i) != observes(regime, c, j)), None)
        collapsed = all(bits[i] == bits[j] for bits in truth.values())
        require((first is None) == collapsed, "witness completeness")
        require((profiles[i] == profiles[j]) == collapsed, "profile/collapse equivalence")
        if first is not None:
            require(truth[first][i] != truth[first][j], "unsound witness")
            witnesses.append({"pair": [i, j], "first_context": first})
    holds_two = any(profiles[i] != profiles[j] for i in range(regime.data) for j in range(regime.data))
    require(holds_two == (len(groups) >= 2), "holding-two/class-count equivalence")
    exhausted = [all(bits[i] == bits[j] for (form, _), bits in truth.items() if form == f
                     for i, j in product(range(regime.data), repeat=2)) for f in range(len(regime.forms))]
    require(all(exhausted[f] for f in regime.rules), "uniform rule not exhausted")
    return {"data": regime.data, "forms": regime.forms, "contexts": len(cs), "class_count": len(groups),
            "classes": groups, "holds_two": holds_two, "exhausted": exhausted, "witnesses": witnesses}


def small_regimes() -> tuple[Regime, ...]:
    output = []
    for data, forms in product(range(3), ((), (1,), (2,), (3,), (1, 2))):
        atoms = tuple((f, args) for f, arity in enumerate(forms)
                      for args in product(range(data), repeat=arity))
        for facts_mask, rules_mask in product(range(1 << len(atoms)), range(1 << len(forms))):
            instances = frozenset(atom for k, atom in enumerate(atoms) if facts_mask & (1 << k))
            rules = frozenset(f for f in range(len(forms)) if rules_mask & (1 << f))
            output.append(Regime(data, forms, instances, rules))
    return tuple(output)


def rejected(operation: Callable[[], object]) -> None:
    try:
        operation()
    except DomainError:
        return
    raise CheckFailure("expected DomainError")


def challenges() -> dict[str, object]:
    empty: frozenset[Instance] = frozenset()
    no_rules: frozenset[int] = frozenset()
    rejected(lambda: Regime(True, (), empty, no_rules))
    rejected(lambda: Regime(4, (), empty, no_rules))
    rejected(lambda: Regime(2, (0,), empty, no_rules))
    rejected(lambda: Regime(2, (True,), empty, no_rules))
    rejected(lambda: Regime(2, (1,), frozenset({(0, (2,))}), no_rules))
    rejected(lambda: Regime(2, (1,), frozenset({(0, (0, 1))}), no_rules))
    rejected(lambda: Regime(2, (1,), empty, frozenset({1})))
    binary = Regime(2, (2,), frozenset({(0, (0, 1))}), no_rules)
    multi = Regime(2, (2,), frozenset({(0, (0, 0))}), no_rules)
    ruled = Regime(2, (2,), binary.instances, frozenset({0}))
    require(not any(observes(binary, c, 0) != observes(binary, c, 1)
                    for c in contexts(binary) if len(c[1]) == 1), "unary mutation fixture changed")
    require(verify(binary)["holds_two"] is True, "unary-only mutant not killed")
    first_full = next(c for c in contexts(multi) if observes(multi, c, 0) != observes(multi, c, 1))
    first_one = next(c for c in contexts(multi) if c[1].count(None) == 1
                     and observes(multi, c, 0) != observes(multi, c, 1))
    require(first_full != first_one, "single-hole-only first-witness mutant not killed")
    require(any(observes(ruled, c, 0, True) != observes(ruled, c, 1, True)
                for c in contexts(ruled)), "ignore-uniform-rule mutant not killed")
    require(verify(ruled)["class_count"] != ruled.data, "count-data mutant not killed")
    return {"domain_refusals": 7, "mutations": {"killed": 4, "survived": 0,
            "demonstrably_equivalent": 0, "invalid": 0, "inconclusive": 0, "unrun": 0},
            "one_hole_note": "one-hole filtering changes deterministic witness order; no claim that one-hole contexts cannot decide collapse"}


def main() -> None:
    checked = small_regimes()
    counts: dict[str, int] = {}
    for regime in checked:
        result = verify(regime)
        key = str(result["class_count"])
        counts[key] = counts.get(key, 0) + 1
    fixtures = [Regime(2, (2,), frozenset({(0, (0, 1))}), frozenset()),
                Regime(2, (2,), frozenset({(0, (0, 0))}), frozenset()),
                Regime(2, (2,), frozenset({(0, (0, 1))}), frozenset({0})),
                Regime(3, (4,), frozenset({(0, (0, 0, 1, 2))}), frozenset())]
    print(json.dumps({"node": "PGW-CONTEXT-DECISION-PROCEDURE", "authority_effect": "None",
                      "exhaustive_domain": "data 0..2; forms (), (1), (2), (3), (1,2); all admitted instance and uniform-rule subsets",
                      "regimes_checked": len(checked), "class_count_histogram": counts,
                      "challenges": challenges(), "fixtures": [verify(r) for r in fixtures]},indent=2))


if __name__ == "__main__":
    main()
