"""Winning-set cardinality on the five-belief carrier parity_alt_osc.

The controller wins when the highest priority seen infinitely often is even.
WDP-CHS-N04: a reachability attractor is not this count. The count is the
size of the winning set on this table, not a priority sum or a continuum limit.
"""

from __future__ import annotations

BELIEFS: tuple[str, ...] = ("hi", "lo", "fork", "sink", "bait")
PRIORITY: dict[str, int] = {"hi": 2, "lo": 1, "fork": 1, "sink": 1, "bait": 2}
ACTIONS: dict[str, tuple[tuple[str, tuple[str, ...]], ...]] = {
    "hi": (("down", ("lo",)),),
    "lo": (("up", ("hi",)), ("fall", ("sink",))),
    "fork": (("risky", ("hi", "sink")),),
    "sink": (("stay", ("sink",)),),
    "bait": (("drop", ("sink",)),),
}


def _action_map(belief: str) -> dict[str, tuple[str, ...]]:
    return {name: succs for name, succs in ACTIONS[belief]}


def _check_table() -> None:
    if BELIEFS != ("hi", "lo", "fork", "sink", "bait"):
        raise RuntimeError("carrier is not parity_alt_osc")
    if tuple(PRIORITY[belief] for belief in BELIEFS) != (2, 1, 1, 1, 2):
        raise RuntimeError("priorities are not 2, 1, 1, 1, 2")
    expected = {
        "hi": {"down": ("lo",)},
        "lo": {"up": ("hi",), "fall": ("sink",)},
        "fork": {"risky": ("hi", "sink")},
        "sink": {"stay": ("sink",)},
        "bait": {"drop": ("sink",)},
    }
    if set(ACTIONS) != set(BELIEFS):
        raise RuntimeError("action table does not cover the carrier")
    multi: list[tuple[str, str, tuple[str, ...]]] = []
    for belief, actions in expected.items():
        got = _action_map(belief)
        if got != actions:
            raise RuntimeError("action table mismatch")
        for name, succs in got.items():
            if len(succs) == 0:
                raise RuntimeError("empty successor list")
            if any(nxt not in PRIORITY for nxt in succs):
                raise RuntimeError("successor outside the carrier")
            if len(succs) > 1:
                multi.append((belief, name, succs))
    if multi != [("fork", "risky", ("hi", "sink"))]:
        raise RuntimeError("adversarial action is not fork/risky")


def _cycle(start: str, step) -> tuple[str, ...]:
    seen: dict[str, int] = {}
    order: list[str] = []
    pos = start
    while pos not in seen:
        if len(order) >= len(BELIEFS):
            raise RuntimeError("play left the five-belief carrier")
        seen[pos] = len(order)
        order.append(pos)
        pos = step(pos)
        if pos not in PRIORITY:
            raise RuntimeError("successor outside the carrier")
    return tuple(order[seen[pos] :])


def _marks(cycle: tuple[str, ...]) -> tuple[int, int, int]:
    if len(cycle) == 0:
        raise RuntimeError("empty cycle")
    maximum = PRIORITY[cycle[0]]
    saw_one = 0
    saw_two = 0
    for belief in cycle:
        priority = PRIORITY[belief]
        if priority > maximum:
            maximum = priority
        if priority == 1:
            saw_one = 1
        elif priority == 2:
            saw_two = 1
        else:
            raise RuntimeError("priority outside {1, 2}")
    return maximum, saw_one, saw_two


def _oscillation(belief: str) -> str:
    actions = _action_map(belief)
    if belief == "hi":
        if actions["down"] != ("lo",):
            raise RuntimeError("hi/down is not {lo}")
        return "lo"
    if belief == "lo":
        if actions["up"] != ("hi",):
            raise RuntimeError("lo/up is not {hi}")
        return "hi"
    raise RuntimeError("oscillation leaves hi and lo")


def _odd_reply(belief: str) -> str:
    actions = _action_map(belief)
    if belief == "fork":
        if actions["risky"] != ("hi", "sink"):
            raise RuntimeError("fork/risky is not {hi, sink}")
        return "sink"
    if belief == "sink":
        if actions["stay"] != ("sink",):
            raise RuntimeError("sink/stay is not {sink}")
        return "sink"
    if belief == "bait":
        if actions["drop"] != ("sink",):
            raise RuntimeError("bait/drop is not {sink}")
        return "sink"
    if belief == "lo":
        if actions["fall"] != ("sink",):
            raise RuntimeError("lo/fall is not {sink}")
        return "sink"
    if belief == "hi":
        return _oscillation(belief)
    raise RuntimeError("belief outside the carrier")


def _fall(belief: str) -> str:
    if belief == "lo":
        return _odd_reply("lo")
    if belief == "sink":
        return _odd_reply("sink")
    raise RuntimeError("fall left the sink tail")


def _cooperative(belief: str) -> str:
    if belief == "fork":
        if "hi" not in _action_map("fork")["risky"]:
            raise RuntimeError("cooperative successor missing")
        return "hi"
    if belief in ("hi", "lo"):
        return _oscillation(belief)
    raise RuntimeError("cooperative path left the oscillation")


def _strategy_win(belief: str) -> int:
    _check_table()
    if belief in ("hi", "lo"):
        maximum, saw_one, saw_two = _marks(_cycle(belief, _oscillation))
        if maximum == 2 and maximum % 2 == 0 and saw_one == 1 and saw_two == 1:
            return 1
        return 0
    if belief in ("fork", "sink", "bait"):
        if len(_action_map(belief)) != 1:
            raise RuntimeError("loss side has an alternative action; inspection stops")
        maximum, saw_one, saw_two = _marks(_cycle(belief, _odd_reply))
        if maximum == 1 and maximum % 2 == 1 and saw_one == 1 and saw_two == 0:
            return 0
        raise RuntimeError("odd reply did not force the sink cycle")
    raise RuntimeError("belief outside the carrier")


def _forces_even(start: str) -> bool:
    """Existential controller choice, universal successor, on this table only."""
    _check_table()

    def rec(state: str, seen: tuple[str, ...]) -> bool:
        if state in seen:
            maximum, _saw_one, _saw_two = _marks(seen[seen.index(state) :])
            return maximum % 2 == 0
        actions = _action_map(state)
        if len(actions) == 0:
            raise RuntimeError("dead-end reading is not the parity objective")
        path = seen + (state,)
        for succs in actions.values():
            if all(rec(nxt, path) for nxt in succs):
                return True
        return False

    return rec(start, ())


def _agreed(belief: str) -> int:
    strategic = _strategy_win(belief)
    branched = 1 if _forces_even(belief) else 0
    if strategic != branched:
        raise RuntimeError("certificates disagree")
    return strategic


def _reachable_sink_reply(start: str) -> frozenset[str]:
    seen: set[str] = set()
    pending = [start]
    while pending:
        state = pending.pop()
        if state in seen:
            continue
        seen.add(state)
        for name, succs in _action_map(state).items():
            if len(succs) > 1:
                if (state, name) != ("fork", "risky") or "sink" not in succs:
                    raise RuntimeError("unexpected adversarial action")
                pending.append("sink")
            else:
                pending.append(succs[0])
    return frozenset(seen)


def _losses_stay_in_odd_sink() -> None:
    for belief in ("fork", "sink", "bait"):
        reached = _reachable_sink_reply(belief)
        if not reached <= frozenset({"fork", "sink", "bait"}):
            raise RuntimeError("sink reply escaped the losing set")
        if "sink" not in reached or "hi" in reached or "lo" in reached:
            raise RuntimeError("sink reply did not separate the oscillation")
    if _action_map("sink")["stay"] != ("sink",):
        raise RuntimeError("sink does not loop")


def _attractor_size(targets: frozenset[str]) -> int:
    """P01 reachability attractor. Not a parity certificate."""
    _check_table()
    if any(target not in PRIORITY for target in targets):
        raise RuntimeError("target outside the carrier")
    inside = set(targets)
    changed = True
    while changed:
        changed = False
        for belief in BELIEFS:
            if belief in inside:
                continue
            for succs in _action_map(belief).values():
                if len(succs) > 0 and all(nxt in inside for nxt in succs):
                    inside.add(belief)
                    changed = True
                    break
    return len(inside)


def _trap_contains_hi() -> int:
    """P04 on all five beliefs: every action has a successor inside the carrier."""
    _check_table()
    for belief in BELIEFS:
        actions = _action_map(belief)
        if len(actions) == 0:
            continue
        for succs in actions.values():
            if not any(nxt in BELIEFS for nxt in succs):
                return 0
    return 1 if "hi" in BELIEFS else 0


def witness() -> dict[str, int]:
    _check_table()
    _losses_stay_in_odd_sink()
    hi_wins = _agreed("hi")
    lo_wins = _agreed("lo")
    fork_wins = _agreed("fork")
    sink_wins = _agreed("sink")
    bait_wins = _agreed("bait")
    winning_cardinality = hi_wins + lo_wins + fork_wins + sink_wins + bait_wins
    oscillation_max, saw_one, saw_two = _marks(_cycle("hi", _oscillation))
    lo_max, lo_one, lo_two = _marks(_cycle("lo", _oscillation))
    if oscillation_max != lo_max or saw_one != 1 or saw_two != 1 or lo_one != 1 or lo_two != 1:
        raise RuntimeError("hi/lo oscillation is not the even cycle of priorities 1 and 2")
    sink_max = _marks(_cycle("sink", _odd_reply))[0]
    bait_max = _marks(_cycle("bait", _odd_reply))[0]
    fork_max = _marks(_cycle("fork", _odd_reply))[0]
    if len({sink_max, bait_max, fork_max}) != 1:
        raise RuntimeError("losing tails disagree")
    fall_max = _marks(_cycle("lo", _fall))[0]
    coop_max = _marks(_cycle("fork", _cooperative))[0]
    empty_size = _attractor_size(frozenset())
    even_targets = frozenset(belief for belief in BELIEFS if PRIORITY[belief] % 2 == 0)
    even_size = _attractor_size(even_targets)
    priority_sum = 0
    for belief in BELIEFS:
        priority_sum += PRIORITY[belief]
    trap_hi = _trap_contains_hi()
    if winning_cardinality in (empty_size, even_size, priority_sum, len(BELIEFS)):
        raise RuntimeError("parity cardinality collided with a fenced stand-in")
    if trap_hi == 1 and hi_wins != 1:
        raise RuntimeError("reachability trap and parity win no longer disagree at hi")
    return {
        "beliefs": len(BELIEFS),
        "winning_cardinality": winning_cardinality,
        "hi_wins": hi_wins,
        "lo_wins": lo_wins,
        "fork_wins": fork_wins,
        "sink_wins": sink_wins,
        "bait_wins": bait_wins,
        "oscillation_max_priority": oscillation_max,
        "sink_cycle_max_priority": sink_max,
        "fall_cycle_max_priority": fall_max,
        "cooperative_fork_cycle_max": coop_max,
        "empty_target_attractor": empty_size,
        "even_priority_attractor": even_size,
        "priority_sum": priority_sum,
        "reachability_trap_contains_hi": trap_hi,
    }


def refuse_reachability_as_parity(claimed: int) -> None:
    """Refuse a reachability count or priority sum as the parity cardinality."""
    if isinstance(claimed, bool) or not isinstance(claimed, int):
        raise TypeError("claimed cardinality must be an int")
    result = witness()
    if claimed in (
        result["empty_target_attractor"],
        result["even_priority_attractor"],
        result["beliefs"],
    ):
        raise ValueError("WDP-CHS-N04: reachability stand-in is not the parity cardinality")
    if claimed == result["priority_sum"]:
        raise ValueError("refused: priority sum is not the parity winning cardinality")
    if claimed != result["winning_cardinality"]:
        raise ValueError("refused: not the parity winning-set cardinality on parity_alt_osc")
