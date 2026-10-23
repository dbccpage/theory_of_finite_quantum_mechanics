"""Finite d=2 fixed-R1 arenas on the nine-pair rejection-reuse carrier.

The no-fallback menu and the two-transport restoration are different arenas.
WDP-CHS-N03: this check does not prove A1 or A3 and does not close WDP-CHS-O02.
"""

from __future__ import annotations

from fractions import Fraction

D = (-1, 0, 1)
TASKS = (-1, 0, 1, 2)
PROPOSE = Fraction(1)
CHECK = Fraction(2)
EMIT = Fraction(1)
GUARD = Fraction(1, 2)
TRANSPORT = Fraction(1)
INSTALL = Fraction(1) + Fraction(1) + Fraction(1)
BUDGET = Fraction(18)

# Printed rows of rejection-reuse section 1. Maps below have to reproduce them.
ROWS = (
    ((-1, -1), (-2, 0), (-2, -2)),
    ((-1, 0), (-1, -1), (-1, -2)),
    ((-1, 1), (0, -2), (0, -2)),
    ((0, -1), (-1, 1), (-1, 0)),
    ((0, 0), (0, 0), (0, 0)),
    ((0, 1), (1, -1), (1, 0)),
    ((1, -1), (0, 2), (0, 2)),
    ((1, 0), (1, 1), (1, 2)),
    ((1, 1), (2, 0), (2, 2)),
)

X0 = tuple(row[0] for row in ROWS)
X1 = tuple(row[1] for row in ROWS)
X2 = tuple(row[2] for row in ROWS)
CARRIERS = (X0, X1, X2)

Graph = dict[str, tuple[tuple[str, Fraction, tuple[str, ...]], ...]]


def _f01(pair: tuple[int, int]) -> tuple[int, int]:
    x, y = pair
    return (x + y, x - y)


def _f12(pair: tuple[int, int]) -> tuple[int, int]:
    u, v = pair
    return (u, v + u)


def _g21(pair: tuple[int, int]) -> tuple[int, int]:
    r, t = pair
    return (r, t - r)


def _g10(pair: tuple[int, int]) -> tuple[Fraction, Fraction]:
    u, v = pair
    return (Fraction(u + v, 2), Fraction(u - v, 2))


def _H(pair: tuple[int, int]) -> tuple[Fraction, Fraction]:
    """Level-2 decoder H(r, t) = (t/2, r - t/2)."""
    r, t = pair
    return (Fraction(t, 2), Fraction(r) - Fraction(t, 2))


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _carriers() -> None:
    generated0 = tuple((x, y) for x in D for y in D)
    _require(generated0 == X0, "X0 is not D^2 in printed order")
    _require(len(X0) == len(set(X0)) == 9, "X0 is not nine pairs")
    for original, level1, level2 in ROWS:
        _require(_f01(original) == level1, "f01 left the printed table")
        _require(_f12(level1) == level2, "f12 left the printed table")
        _require(_g10(level1) == original, "g10 is not inverse to f01 on X1")
        _require(_g21(level2) == level1, "g21 is not inverse to f12 on X2")
        _require(_H(level2) == _g10(_g21(level2)) == original, "H is not g10 o g21")
    _require(len(set(X1)) == 9 and len(set(X2)) == 9, "image carrier is not bijective")
    off = _g10((1, 0))
    _require(off == (Fraction(1, 2), Fraction(1, 2)), "formal level-1 decoder drifted")
    _require((1, 0) not in X1 and off not in X0 and (1, 0) in X2, "field name is not carrier admission")
    one_dimensional = sum(1 for coord in D if coord == 2)
    _require(one_dimensional == 0, "D was enlarged")
    counts = tuple(sum(1 for pair in X0 if pair[0] + pair[1] == task) for task in TASKS)
    _require(counts == (2, 3, 2, 1), "solution counts are not 2, 3, 2, 1")
    _require(one_dimensional != counts[-1], "a 1D constant was copied into the d=2 count")


def _valid(level: int, task: int, pair: tuple[int, int]) -> bool:
    if pair not in CARRIERS[level]:
        return False
    if level == 0:
        return pair[0] + pair[1] == task
    return pair[0] == task


def _rejects(level: int, task: int, pair: tuple[int, int], mode: str) -> bool:
    if mode == "none":
        return False
    if mode not in ("parameterized", "fixed_one"):
        raise RuntimeError("unknown rejection mode")
    target = task if mode == "parameterized" else 1
    if level == 0:
        source = _f01(pair)
    elif level == 1:
        source = pair
    elif level == 2:
        source = _g21(pair)
    else:
        raise RuntimeError("level outside 0, 1, 2")
    return source[0] != target


def _decode(level: int, pair: tuple[int, int]) -> tuple[int, int]:
    decoded = pair if level == 0 else _g10(pair if level == 1 else _g21(pair))
    coords = []
    for coord in decoded:
        if type(coord) is int:
            coords.append(coord)
            continue
        if type(coord) is not Fraction or coord.denominator != 1:
            raise RuntimeError("decoder left the integer carrier")
        coords.append(coord.numerator)
    return (coords[0], coords[1])


def _named_graph(task: int, level: int, guard: str, original_route: bool) -> tuple[Graph, frozenset[str], dict[str, tuple[int, int]]]:
    graph: Graph = {}
    targets: set[str] = set()
    emitted: dict[str, tuple[int, int]] = {}

    def add(root: str, at: int, mode: str) -> None:
        actions = []
        for index, pair in enumerate(CARRIERS[at]):
            proposed = f"{root}.p{index}"
            checked = f"{root}.c{index}"
            terminal = f"{root}.t{index}"
            actions.append((f"propose_{index}", PROPOSE, (proposed,)))
            check_start = proposed
            if mode != "none":
                check_start = f"{root}.g{index}"
                nxt = root if _rejects(at, task, pair, mode) else check_start
                graph[proposed] = (("guard", GUARD, (nxt,)),)
            graph[check_start] = (("check", CHECK, ((checked if _valid(at, task, pair) else root),)),)
            if _valid(at, task, pair):
                graph[checked] = ((f"emit_{index}", EMIT, (terminal,)),)
                targets.add(terminal)
                emitted[terminal] = pair
        graph[root] = tuple(actions)

    add("s", level, guard)
    if original_route:
        _require(level == 2, "fallback example starts at level 2")
        graph["s"] = tuple([*graph["s"], ("transport_21", TRANSPORT, ("back1",))])
        graph["back1"] = (("transport_10", TRANSPORT, ("original",)),)
        add("original", 0, "none")
    return graph, frozenset(targets), emitted


def _reachable(graph: Graph, initial: str) -> frozenset[str]:
    seen: set[str] = set()
    pending = [initial]
    while pending:
        state = pending.pop()
        if state in seen:
            continue
        seen.add(state)
        for _action, _cost, succs in graph.get(state, ()):
            pending.extend(succs)
    return frozenset(seen)


def _attractor(graph: Graph, reached: frozenset[str], targets: frozenset[str]) -> tuple[frozenset[str], dict[str, int]]:
    winning = set(targets) & set(reached)
    rank = {state: 0 for state in winning}
    changed = True
    while changed:
        changed = False
        for state in reached:
            if state in winning:
                continue
            for _action, _cost, succs in graph.get(state, ()):
                if succs and all(nxt in winning for nxt in succs):
                    winning.add(state)
                    rank[state] = 1 + max(rank[nxt] for nxt in succs)
                    changed = True
                    break
    return frozenset(winning), rank


def _strategy_count(graph: Graph, targets: frozenset[str], initial: str) -> int:
    """Rank-decreasing memoryless strategies. A losing initial state contributes none."""
    reached = _reachable(graph, initial)
    winning, rank = _attractor(graph, reached, targets)
    if initial not in winning:
        return 0

    def count(state: str, seen: frozenset[str]) -> int:
        if state in targets:
            return 1
        if state in seen or state not in winning:
            return 0
        total = 0
        nxt_seen = seen | {state}
        for _action, _cost, succs in graph.get(state, ()):
            if not succs or any(nxt not in winning or rank[nxt] >= rank[state] for nxt in succs):
                continue
            ways = 1
            for nxt in succs:
                ways *= count(nxt, nxt_seen)
            total += ways
        return total

    return count(initial, frozenset())


def _minimax(graph: Graph, targets: frozenset[str], initial: str) -> Fraction | None:
    reached = _reachable(graph, initial)
    _require(initial in reached, "initial state missing")
    value: dict[str, Fraction | None] = {
        state: Fraction(0) if state in targets else None for state in reached
    }
    for _round in range(len(reached)):
        updated = dict(value)
        for state in reached:
            if state in targets:
                updated[state] = Fraction(0)
                continue
            best: Fraction | None = None
            for _action, cost, succs in graph.get(state, ()):
                if not succs or any(value[nxt] is None for nxt in succs):
                    continue
                peak = value[succs[0]]
                for nxt in succs[1:]:
                    if value[nxt] > peak:
                        peak = value[nxt]
                total = cost + peak
                if best is None or total < best:
                    best = total
            updated[state] = best
        value = updated
    return value[initial]


def _number(value: Fraction) -> int | Fraction:
    _require(type(value) is Fraction, "non-rational arena value")
    if value.denominator == 1:
        return value.numerator
    return value


def _scan_graph(valid_count: int, rejected: int) -> tuple[Graph, frozenset[str], str]:
    _require(1 <= valid_count <= 9 and 0 <= rejected <= 9 - valid_count, "invalid scan counts")
    bad = 9 - valid_count - rejected
    graph: Graph = {}
    for invalid_left in range(bad + 1):
        for rejected_left in range(rejected + 1):
            root = f"n{invalid_left}_{rejected_left}"
            outcomes = []
            for category in ("good", "bad", "reject"):
                if (category == "bad" and invalid_left == 0) or (category == "reject" and rejected_left == 0):
                    continue
                proposed = f"{root}.{category}"
                outcomes.append(proposed)
                after_guard = proposed + ".g"
                nxt = f"n{invalid_left}_{rejected_left - 1}" if category == "reject" else after_guard
                graph[proposed] = (("guard", GUARD, (nxt,)),)
                if category == "reject":
                    continue
                checked = proposed + ".c"
                nxt = checked if category == "good" else f"n{invalid_left - 1}_{rejected_left}"
                graph[after_guard] = (("check", CHECK, (nxt,)),)
                if category == "good":
                    graph[checked] = (("emit", EMIT, ("t",)),)
            graph[root] = (("draw", PROPOSE, tuple(outcomes)),)
    return graph, frozenset({"t"}), f"n{bad}_{rejected}"


def _ledger() -> Fraction:
    charges = (
        PROPOSE, CHECK, EMIT,
        Fraction(1), Fraction(1), Fraction(1),
        TRANSPORT,
        PROPOSE, GUARD, CHECK, EMIT,
        PROPOSE, GUARD, CHECK, EMIT,
    )
    _require(len(charges) == 15, "ledger is not the fifteen-row run")
    spent = Fraction(0)
    for charge in charges:
        _require(charge > 0 and spent + charge <= BUDGET, "ledger charge missed the shared budget")
        spent += charge
    return spent


def _loss_trap(graph: Graph, targets: frozenset[str]) -> int:
    reached = _reachable(graph, "s")
    _require("s" in reached, "no-fallback root missing")
    _require(not any(state in targets for state in reached), "no-fallback arena emitted a target")
    proposals = graph["s"]
    _require(len(proposals) == 9, "level-2 root does not name the nine candidates")
    _require(all(action.startswith("propose_") for action, _cost, _succs in proposals), "root is not the named menu")
    _require(not any(action.startswith("transport_") for action, _cost, _succs in proposals), "no-fallback arena contains the restored route")
    for state in reached:
        for _action, _cost, succs in graph.get(state, ()):
            _require(succs and all(nxt in reached and nxt not in targets for nxt in succs), "reachable set is not a target-disjoint trap")
    winning, _rank = _attractor(graph, reached, targets)
    _require(not winning, "target-free trap was marked winning")
    # Emit nodes of rejected candidates stay in the graph and are not emittable.
    emitted = [state for state in targets if state in reached]
    return len(emitted)


def witness() -> dict[str, int | Fraction | tuple[int, int, int]]:
    _carriers()
    solutions = tuple(pair for pair in X0 if pair[0] + pair[1] == 2)
    _require(solutions == ((1, 1),), "d=2 solution set is not {(1,1)}")
    _require(X1[X0.index((1, 1))] == (2, 0) and X2[X0.index((1, 1))] == (2, 2), "images of (1,1) drifted")
    _require(_rejects(1, 2, (2, 0), "fixed_one") and _rejects(2, 2, (2, 2), "fixed_one"), "fixed R1 did not reject both images")
    _require(not _rejects(1, 2, (2, 0), "parameterized"), "parameterized R_d was replaced by fixed R1")
    _require(not _rejects(2, 2, (2, 2), "parameterized"), "parameterized level-2 rule rejected (2,2)")
    level1_valid = tuple(pair for pair in X1 if _valid(1, 2, pair))
    level2_valid = tuple(pair for pair in X2 if _valid(2, 2, pair))
    _require(level1_valid == ((2, 0),) and level2_valid == ((2, 2),), "d=2 valid images are not unique")

    blocked, blocked_targets, blocked_emitted = _named_graph(2, 2, "fixed_one", False)
    valid_index = X2.index((2, 2))
    _require(blocked[f"s.p{valid_index}"] == (("guard", GUARD, ("s",)),), "fixed R1 did not return (2,2) to the root")
    emittable_valid = _loss_trap(blocked, blocked_targets)
    reached_blocked = _reachable(blocked, "s")
    decoded_emitted = tuple(
        _decode(2, pair) for state, pair in blocked_emitted.items() if state in reached_blocked
    )
    _require(decoded_emitted == () and emittable_valid == 0, "emittable valid set is not empty")
    strategy_count = _strategy_count(blocked, blocked_targets, "s")
    _require(_minimax(blocked, blocked_targets, "s") is None, "no-fallback arena has a finite value")
    sol = set(solutions)
    emitted_set = set(decoded_emitted)
    vacuous_soundness = 1 if emitted_set <= sol else 0
    coverage = 1 if sol <= emitted_set else 0
    _require(vacuous_soundness == 1 and coverage == 0, "empty acceptance was read as coverage")

    restored, restored_targets, _restored_emitted = _named_graph(2, 2, "fixed_one", True)
    _require(any(action == "transport_21" for action, _cost, _succs in restored["s"]), "restored route missing")
    restored_value = _minimax(restored, restored_targets, "s")
    _require(restored_value is not None, "restored route has no finite value")
    _require(_strategy_count(restored, restored_targets, "s") > 0, "finite restored value has no winning strategy")

    named, named_targets, _named_emitted = _named_graph(2, 0, "none", False)
    named_value = _minimax(named, named_targets, "s")
    guarded, guarded_targets, _guarded_emitted = _named_graph(2, 2, "parameterized", False)
    guarded_value = _minimax(guarded, guarded_targets, "s")
    _require(named_value is not None and guarded_value is not None, "named menu failed to emit")

    scan, scan_targets, scan_initial = _scan_graph(1, 8)
    scan_operating = _minimax(scan, scan_targets, scan_initial)
    scan_formula = 36 - Fraction(7, 2) * 1 - 2 * 8
    _require(scan_operating == scan_formula == Fraction(33, 2), "blind-scan operating value drifted")
    scan_with_setup = scan_operating + INSTALL
    _require(scan_with_setup == Fraction(39, 2) and scan_with_setup > BUDGET, "blind-scan setup value drifted")
    guarded_with_setup = guarded_value + INSTALL
    ledger = _ledger()
    _require(INSTALL == 3 and ledger == 17 and ledger <= BUDGET, "ledger total drifted")

    original_solutions = len(solutions)
    restored_exact = _number(restored_value)
    named_exact = _number(named_value)
    guarded_exact = _number(guarded_value)
    setup_exact = _number(guarded_with_setup)
    scan_exact = _number(scan_with_setup)
    ledger_exact = _number(ledger)
    _require(type(restored_exact) is int and type(named_exact) is int and type(ledger_exact) is int, "integer arena value drifted")
    _require(
        strategy_count not in (original_solutions, named_exact, guarded_exact, setup_exact, scan_exact, ledger_exact, restored_exact),
        "strategy count collided with another menu",
    )
    return {
        "witness": (original_solutions, strategy_count, restored_exact),
        "original_solutions": original_solutions,
        "winning_strategies_from_initial": strategy_count,
        "restored_value": restored_exact,
        "emittable_valid": emittable_valid,
        "vacuous_soundness": vacuous_soundness,
        "coverage": coverage,
        "carrier_rows": len(X0),
        "named_proposal": named_exact,
        "guarded_operating": guarded_exact,
        "guarded_with_setup": setup_exact,
        "blind_scan_with_setup": scan_exact,
        "ledger": ledger_exact,
        "a1_proved": 0,
        "a3_proved": 0,
        "goal_closed": 0,
    }


def refuse_as_strategy_count(claimed: object) -> None:
    """Refuse another menu's value, or an A1-A3 label, as the no-fallback strategy count."""
    result = witness()
    if type(claimed) is str:
        if claimed in {"A1", "A2", "A3", "A1-A3"}:
            raise ValueError(
                "WDP-CHS-N03: an effective check does not prove A1 or A3, "
                "and declaring A1-A3 does not discharge the adapter duties"
            )
        raise ValueError("refused: not the no-fallback winning-strategy count")
    if type(claimed) is not int and type(claimed) is not Fraction:
        raise TypeError("exact int or Fraction required; float tolerance is not a claim")
    count = result["winning_strategies_from_initial"]
    for key, value in result.items():
        if key in {"witness", "winning_strategies_from_initial"}:
            continue
        if value == count:
            continue
        if claimed == value:
            raise ValueError(
                "other menu, solution count, or restored route is not the no-fallback winning-strategy count"
            )
    if type(claimed) is not int or claimed != count:
        raise ValueError("refused: not the no-fallback winning-strategy count")
