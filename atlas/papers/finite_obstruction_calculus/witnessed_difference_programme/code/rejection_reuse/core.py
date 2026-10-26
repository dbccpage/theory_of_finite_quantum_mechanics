"""Finite carriers and explicitly different named-proposal and blind-scan arenas."""

import hashlib
import json
from fractions import Fraction as Q
from itertools import product

from certified_progress.model import graph_model

TASKS = (-1, 0, 1, 2)
X0 = tuple(product((-1, 0, 1), repeat=2))


def f01(p):
    x, y = p
    return x + y, x - y


def g10(p):
    u, v = p
    return Q(u + v, 2), Q(u - v, 2)


def f12(p):
    u, v = p
    return u, v + u


def g21(p):
    r, t = p
    return r, t - r


X1 = tuple(map(f01, X0))
X2 = tuple(map(f12, X1))
CARRIERS = (X0, X1, X2)


def parent_packet(d=1, level=1):
    return {"task": d, "level": level, "carrier": [list(p) for p in CARRIERS[level]],
            "checker_verdicts": [valid(level, d, p) for p in CARRIERS[level]],
            "prices": {"propose": "1", "check": "2", "emit": "1", "guard": "1/2",
                       "transport": "1", "installation": "3"}}


def packet_digest(packet):
    raw = json.dumps(packet, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()


def bundle_matches(bundle, packet):
    return (bundle["parent_sha256"] == packet_digest(packet)
            and bundle["task"] == packet["task"]
            and bundle["level"] == packet["level"])


def decode(level, p):
    if p not in CARRIERS[level]:
        raise ValueError("candidate outside the declared image carrier")
    return p if level == 0 else g10(p if level == 1 else g21(p))


def valid(level, d, p):
    return p in CARRIERS[level] and (sum(p) == d if level == 0 else p[0] == d)


def rejects(level, d, p, mode):
    if mode == "none":
        return False
    if mode not in ("parameterized", "fixed_one"):
        raise ValueError("unknown rule")
    target = d if mode == "parameterized" else 1
    # The level-0 pullback is R o f01, not R o g10 (wrong domain).
    source = f01(p) if level == 0 else p if level == 1 else g21(p)
    return source[0] != target


def named_arena(d, *, level=0, guard="none", original_route=False):
    """Any in-carrier candidate can be named. No scan-order adversary is added.

    Failed checks and rejections return to the same root. A guarded installation
    here makes the guard mandatory on that level. Optional fallback explicitly
    adds two adjacent transports from level 2 to an unguarded original root.
    Every action has a single strictly positive, outcome-independent price.
    """
    if original_route and level != 2:
        raise ValueError("fallback example starts at level 2")
    graph, targets, resolutions, emissions = {}, [], {}, {}

    def add(root, at, mode):
        graph[root] = []
        for i, p in enumerate(CARRIERS[at]):
            proposed, checked, emitted = f"{root}.p{i}", f"{root}.c{i}", f"{root}.t{i}"
            graph[root].append((f"propose_{i}", "1", [proposed]))
            check_start = proposed
            if mode != "none":
                check_start = f"{root}.g{i}"
                graph[proposed] = [("guard", "1/2", [
                    root if rejects(at, d, p, mode) else check_start])]
            graph[check_start] = [("check", "2", [checked if valid(at, d, p) else root])]
            if valid(at, d, p):
                action = f"emit_{root}_{i}"
                graph[checked] = [(action, "1", [emitted])]
                targets.append(emitted)
                resolutions[checked] = resolutions[emitted] = str(tuple(decode(at, p)))
                emissions[action] = resolutions[checked]

    add("s", level, guard)
    if original_route:
        graph["s"].append(("transport_21", "1", ["back1"]))
        graph["back1"] = [("transport_10", "1", ["original"])]
        add("original", 0, "none")
    return graph_model(graph, targets=tuple(targets), emissions=emissions,
                       valid_resolutions={t: [r] for t, r in resolutions.items()},
                       task_id=f"named-d{d}-l{level}-{guard}-fallback{original_route}")


def scan_arena(v, s=0, *, guarded=False):
    """Restricted blind scan without replacement, stopping at first valid answer.

    v valid, s rejected invalid, 9-v-s checked invalid. Agent cannot name an
    element or install a method. Adversary chooses the next category; identifying
    members of one category changes neither prices nor continuation counts.
    Category reports are observed. This is a cost quotient, not an answer decoder.
    """
    if not (1 <= v <= 9 and 0 <= s <= 9-v) or (s and not guarded):
        raise ValueError("invalid scan counts")
    bad = 9 - v - s
    graph = {}
    for i in range(bad + 1):
        for j in range(s + 1):
            root = f"n{i}_{j}"
            outcomes = []
            for category in ("good", "bad", "reject"):
                if category == "bad" and not i or category == "reject" and not j:
                    continue
                proposed = root + "." + category
                outcomes.append(proposed)
                after_guard = proposed
                if guarded:
                    after_guard = proposed + ".g"
                    graph[proposed] = [("guard", "1/2", [
                        f"n{i}_{j-1}" if category == "reject" else after_guard])]
                if category != "reject":
                    checked = proposed + ".c"
                    graph[after_guard] = [("check", "2", [
                        checked if category == "good" else f"n{i-1}_{j}"])]
                    if category == "good":
                        graph[checked] = [("emit", "1", ["t"])]
            graph[root] = [("draw", "1", outcomes)]
    return graph_model(graph, initial=f"n{bad}_{s}",
                       task_id=f"restricted-scan-v{v}-s{s}-guard{guarded}")


def ledger():
    operations = [("parent proposal X1 (1,-1)", 1), ("parent check", 2), ("parent emit (0,1)", 1),
                  ("learn", 1), ("bundle check", 1), ("install", 1),
                  ("transport 12", 1), ("child proposal (1,0)", 1),
                  ("guard", Q(1, 2)), ("child check", 2), ("emit (0,1)", 1),
                  ("child proposal (1,2)", 1), ("guard", Q(1, 2)),
                  ("child check", 2), ("emit (1,0)", 1)]
    spent, rows = Q(0), []
    for operation, charge in operations:
        if spent + charge > 18:
            raise ValueError("shared budget exhausted")
        spent += charge
        rows.append({"parent": "finite-d1-parent", "task": 1, "operation": operation,
                     "charge": str(charge), "spent": str(spent)})
    return rows
