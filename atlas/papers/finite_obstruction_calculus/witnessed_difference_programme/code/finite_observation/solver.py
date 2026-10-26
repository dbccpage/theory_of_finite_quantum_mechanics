"""Complete finite certificates for fixed and adaptive priced observation.

Prices and outcome equality are supplied data. Verification checks the submitted
tables directly; it never calls the proposal generator to replace a bad table.
None denotes mathematical infeasibility, never a large finite cost.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations

MAX_STATES = 10
MAX_INSTRUMENTS = 12
MAX_PRICE_BITS = 256
# Every cost sums at most twelve 256-bit prices: fewer than 2,000 decimal
# characters after reduction. Bound text before Fraction can expand exponents.
MAX_COST_TEXT = 4096


@dataclass(frozen=True)
class Instrument:
    name: str
    outcomes: tuple[str, ...]
    cost: Fraction


@dataclass(frozen=True)
class Instance:
    states: tuple[str, ...]
    visible: tuple[str, ...]
    query: tuple[str, ...]
    instruments: tuple[Instrument, ...]


@dataclass(frozen=True)
class Verification:
    accepted: bool
    code: str
    detail: str


def validate_instance(instance: Instance) -> None:
    if type(instance) is not Instance:
        raise TypeError("expected an Instance")
    n = len(instance.states)
    if n > MAX_STATES or len(instance.instruments) > MAX_INSTRUMENTS:
        raise ValueError("finite reference cap exceeded")
    for labels in (instance.states, instance.visible, instance.query):
        if type(labels) is not tuple or len(labels) != n or any(type(x) is not str for x in labels):
            raise TypeError("state, visible and query tables require aligned string tuples")
    if len(set(instance.states)) != n:
        raise ValueError("state labels must be unique")
    if type(instance.instruments) is not tuple:
        raise TypeError("instrument shelf must be an immutable tuple")
    names = []
    for item in instance.instruments:
        if type(item) is not Instrument or type(item.name) is not str or not item.name:
            raise TypeError("invalid instrument")
        names.append(item.name)
        if type(item.outcomes) is not tuple or len(item.outcomes) != n or any(type(x) is not str for x in item.outcomes):
            raise TypeError("instrument outcomes must be aligned string tuples")
        if type(item.cost) is not Fraction or item.cost <= 0:
            raise TypeError("prices must be positive exact Fractions")
        if max(item.cost.numerator.bit_length(), item.cost.denominator.bit_length()) > MAX_PRICE_BITS:
            raise ValueError("price bit cap exceeded")
    if len(set(names)) != len(names):
        raise ValueError("instrument names must be unique")


def instance_data(instance: Instance) -> dict:
    validate_instance(instance)
    return {
        "states": list(instance.states), "visible": list(instance.visible), "query": list(instance.query),
        "instruments": [{"name": i.name, "outcomes": list(i.outcomes), "cost": str(i.cost)} for i in instance.instruments],
    }


def instance_hash(instance: Instance) -> str:
    payload = json.dumps(instance_data(instance), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def unresolved_pairs(instance: Instance) -> tuple[tuple[int, int], ...]:
    validate_instance(instance)
    return tuple((x, y) for x, y in combinations(range(len(instance.states)), 2)
                 if instance.visible[x] == instance.visible[y] and instance.query[x] != instance.query[y])


def _cover(instance: Instance, pairs: tuple[tuple[int, int], ...], mask: int) -> bool:
    return all(any(mask & (1 << i) and item.outcomes[x] != item.outcomes[y]
                   for i, item in enumerate(instance.instruments)) for x, y in pairs)


def _cost(instance: Instance, mask: int) -> Fraction:
    return sum((item.cost for i, item in enumerate(instance.instruments) if mask & (1 << i)), Fraction(0))


def _members(mask: int, size: int) -> tuple[int, ...]:
    return tuple(i for i in range(size) if mask & (1 << i))


def _branches(instance: Instance, mask: int, instrument: int) -> tuple[int, ...]:
    groups: dict[str, int] = {}
    for state in _members(mask, len(instance.states)):
        outcome = instance.instruments[instrument].outcomes[state]
        groups[outcome] = groups.get(outcome, 0) | (1 << state)
    return tuple(groups.values())


def _initial_fibers(instance: Instance) -> tuple[int, ...]:
    fibers: dict[str, int] = {}
    for state, report in enumerate(instance.visible):
        fibers[report] = fibers.get(report, 0) | (1 << state)
    return tuple(fibers.values())


def _leaf(instance: Instance, mask: int) -> bool:
    return len({instance.query[x] for x in _members(mask, len(instance.states))}) <= 1


def _options(instance: Instance, mask: int, values: list[Fraction | None]) -> list[tuple[Fraction, int]]:
    options = []
    for index, item in enumerate(instance.instruments):
        branches = _branches(instance, mask, index)
        if len(branches) < 2:
            continue
        children = [values[child] for child in branches]
        if all(value is not None for value in children):
            options.append((item.cost + max(children), index))
    return options


def _global_value(instance: Instance, values: list[Fraction | None]) -> Fraction | None:
    initial = [values[mask] for mask in _initial_fibers(instance)]
    return None if any(value is None for value in initial) else max(initial, default=Fraction(0))


def solve(instance: Instance) -> dict:
    """Propose full 2^m subset and 2^n Bellman tables within explicit caps."""
    validate_instance(instance)
    pairs = unresolved_pairs(instance)
    fixed_table = [{"mask": mask, "cost": str(_cost(instance, mask)), "sufficient": _cover(instance, pairs, mask)}
                   for mask in range(1 << len(instance.instruments))]
    feasible = [row for row in fixed_table if row["sufficient"]]
    best = min(feasible, key=lambda row: (Fraction(row["cost"]), row["mask"]), default=None)
    values: list[Fraction | None] = []
    adaptive_table = []
    for mask in range(1 << len(instance.states)):
        options = [] if _leaf(instance, mask) else _options(instance, mask, values)
        value, choice = (Fraction(0), None) if _leaf(instance, mask) else min(options, default=(None, None))
        values.append(value)
        adaptive_table.append({"mask": mask, "value": None if value is None else str(value), "choice": choice})
    collision = next(([x, y] for x, y in pairs if all(i.outcomes[x] == i.outcomes[y] for i in instance.instruments)), None)
    total = _global_value(instance, values)
    return {
        "schema_version": 1, "instance_sha256": instance_hash(instance), "authority_effect": "None",
        "fixed": {"suite_mask": None if best is None else best["mask"], "value": None if best is None else best["cost"], "table": fixed_table},
        "adaptive": {"value": None if total is None else str(total), "table": adaptive_table},
        "infeasible_pair": collision,
    }


def _keys(value: object, keys: set[str]) -> dict:
    if type(value) is not dict or set(value) != keys:
        raise ValueError("missing, extra or malformed certificate fields")
    return value


def _rational(value: object, *, infinity: bool = False) -> Fraction | None:
    if value is None and infinity:
        return None
    if (type(value) is not str or len(value) > MAX_COST_TEXT
            or re.fullmatch(r"(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", value) is None):
        raise TypeError("certificate costs require canonical rational strings")
    result = Fraction(value)
    if str(result) != value or result < 0:
        raise ValueError("certificate cost is not canonical nonnegative rational")
    return result


def verify(instance: Instance, certificate: object) -> Verification:
    """Replay every supplied table row, all competing choices, and the final claim."""
    try:
        validate_instance(instance)
        c = _keys(certificate, {"schema_version", "instance_sha256", "authority_effect", "fixed", "adaptive", "infeasible_pair"})
        if type(c["schema_version"]) is not int or c["schema_version"] != 1 or c["authority_effect"] != "None":
            raise ValueError("invalid schema or authority effect")
        if c["instance_sha256"] != instance_hash(instance):
            return Verification(False, "INPUT_MISMATCH", "certificate is for different task, outcomes or prices")
        fixed = _keys(c["fixed"], {"suite_mask", "value", "table"})
        if type(fixed["table"]) is not list or len(fixed["table"]) != 1 << len(instance.instruments):
            raise ValueError("fixed table does not exhaust every subset")
        pairs = unresolved_pairs(instance)
        feasible = []
        for mask, supplied in enumerate(fixed["table"]):
            row = _keys(supplied, {"mask", "cost", "sufficient"})
            if type(row["mask"]) is not int or row["mask"] != mask or type(row["sufficient"]) is not bool:
                raise ValueError("fixed table mask or truth type mismatch")
            cost = _rational(row["cost"])
            if cost != _cost(instance, mask) or row["sufficient"] != _cover(instance, pairs, mask):
                raise ValueError("fixed table cost or coverage mismatch")
            if row["sufficient"]:
                feasible.append((cost, mask))
        fixed_value = _rational(fixed["value"], infinity=True)
        if feasible:
            mask = fixed["suite_mask"]
            if type(mask) is not int or not 0 <= mask < len(fixed["table"]):
                raise ValueError("invalid sufficient suite mask")
            if not _cover(instance, pairs, mask) or _cost(instance, mask) != fixed_value or fixed_value != min(feasible)[0]:
                raise ValueError("suite is insufficient or claimed optimum is not minimal")
        elif fixed_value is not None or fixed["suite_mask"] is not None:
            raise ValueError("infeasible shelf claimed a finite optimum")
        adaptive = _keys(c["adaptive"], {"value", "table"})
        if type(adaptive["table"]) is not list or len(adaptive["table"]) != 1 << len(instance.states):
            raise ValueError("adaptive table does not exhaust every candidate subset")
        values: list[Fraction | None] = []
        for mask, supplied in enumerate(adaptive["table"]):
            row = _keys(supplied, {"mask", "value", "choice"})
            if type(row["mask"]) is not int or row["mask"] != mask:
                raise ValueError("adaptive table mask mismatch")
            value = _rational(row["value"], infinity=True)
            if _leaf(instance, mask):
                if value != 0 or row["choice"] is not None:
                    raise ValueError("nonzero cost or action at a resolved leaf")
            else:
                options = _options(instance, mask, values)
                if not options:
                    if value is not None or row["choice"] is not None:
                        raise ValueError("unresolvable subset given a finite strategy")
                elif (type(row["choice"]) is not int or (value, row["choice"]) not in options
                      or value != min(options)[0]):
                    raise ValueError("adaptive choice or Bellman optimum mismatch")
            values.append(value)
        total = _rational(adaptive["value"], infinity=True)
        if total != _global_value(instance, values):
            raise ValueError("adaptive result is not the maximum over initial visible fibers")
        if (fixed_value is None) != (total is None):
            raise ValueError("fixed/adaptive feasibility mismatch")
        pair = c["infeasible_pair"]
        if fixed_value is None:
            if type(pair) is not list or len(pair) != 2 or any(type(x) is not int for x in pair):
                raise ValueError("infeasibility needs an explicit pair")
            if tuple(pair) not in pairs or any(i.outcomes[pair[0]] != i.outcomes[pair[1]] for i in instance.instruments):
                raise ValueError("pair is not an indistinguishable conflicting pair")
        elif pair is not None:
            raise ValueError("feasible instance has an infeasibility claim")
        return Verification(True, "VERIFIED", "complete fixed and adaptive optimality tables replayed; AuthorityEffect None")
    except (TypeError, ValueError, KeyError, IndexError, ZeroDivisionError) as error:
        return Verification(False, "INVALID_CERTIFICATE", str(error))


def verify_lp_pair(instance: Instance, primal: tuple[Fraction, ...], dual: tuple[Fraction, ...]) -> Fraction:
    """Verify a supplied matching rational LP pair; return only the LP optimum."""
    pairs = unresolved_pairs(instance)
    if type(primal) is not tuple or type(dual) is not tuple or len(primal) != len(instance.instruments) or len(dual) != len(pairs):
        raise ValueError("LP witness shape mismatch")
    if any(type(x) is not Fraction or x < 0 for x in primal + dual):
        raise TypeError("LP witnesses require nonnegative Fractions")
    if any(sum((primal[i] for i, item in enumerate(instance.instruments) if item.outcomes[x] != item.outcomes[y]), Fraction(0)) < 1 for x, y in pairs):
        raise ValueError("LP primal does not cover the unresolved pairs")
    for item in instance.instruments:
        if sum((value for value, (x, y) in zip(dual, pairs) if item.outcomes[x] != item.outcomes[y]), Fraction(0)) > item.cost:
            raise ValueError("LP dual exceeds an instrument price")
    primal_value = sum((value * item.cost for value, item in zip(primal, instance.instruments)), Fraction(0))
    if primal_value != sum(dual, Fraction(0)):
        raise ValueError("LP primal and dual values do not match")
    return primal_value
