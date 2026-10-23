"""Construct an observation arena from actual finite transition/report tables.

Search remains in the existing certified_progress producer. The original input,
not a certificate or its target list, determines the arena and stopping condition.
All arithmetic is exact. This is a finite mathematical model, not a physical sensor.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product

from certified_progress.model import compile_model, graph_model
from certified_progress.observation import refine_observation


def future_model():
    """One Appendix-S information-state model; mode is irrelevant to its futures."""
    states = [f"{b}{v}{m}" for b, v, m in product("AB", "01", "01")]
    graph = {"root": [("prepare", "1", states)]}
    graph.update({s: [("resolve_" + s[0], str(1 + int(s[1])), ["t"]),
                     ("wait", "1", [s])] for s in states})
    reports = {(s, "prepare"): s for s in states}
    reports.update({(s, "wait"): s[:2] for s in states})
    return graph_model(graph, initial="root", observations=reports,
                       task_id="realizable-observation-future-contract")


def protected_classes(model):
    arena = compile_model(model)
    groups = defaultdict(list)
    for b in arena.reachable:
        groups[b in arena.targets].append(list(b))
    result = refine_observation(model, list(groups.values()))
    return {tuple(b): i for i, block in enumerate(result["blocks"]) for b in block}, result


def example(*, restore_cost="1/4", safe=True, flip=True, restore=True):
    """Eight possible post-states; four originals. Every allowed outcome is listed."""
    model = future_model()
    classes, refinement = protected_classes(model)
    states = [f"{b}{v}{m}" for b, v, m in product("AB", "01", "01")]
    actions = ["read_A", "read_B"]
    if safe:
        actions += ["read_branch", "read_all"]
    if flip:
        actions += ["flip_read"]
    if restore:
        actions += ["restore"]
    prices = {"read_A": "3", "read_B": "3", "read_branch": "1", "read_all": "6",
              "flip_read": "1/2", "restore": restore_cost}
    rows = []
    for s in states:
        for a in actions:
            if a == "flip_read" and s[2] != "0" or a == "restore" and s[2] != "1":
                continue
            y = s
            if a in ("flip_read", "restore"):
                y = ("B" if s[0] == "A" else "A") + s[1] + ("1" if a == "flip_read" else "0")
            o = "0" if a in ("read_A", "read_B") else "*"
            if a in ("read_branch", "flip_read"):
                o = y[0]
            elif a == "read_all":
                o = y[:2]
            elif a == "read_A" and y[0] == "A" or a == "read_B" and y[0] == "B":
                o = y[1]
            rows.append({"state": s, "action": a, "successors": [y],
                         "reports": {y: o}, "cost": prices[a]})
    return {"schema": "wdp-realizable-observation-v1", "future_model": model,
            "class_refinement": refinement, "states": states,
            "protected_class": {s: classes[(s,)] for s in states},
            "initial": [s for s in states if s[2] == "0"], "actions": actions, "rows": rows}


def construct(instance, *, answers_only=False):
    """Relations retain the immutable original coordinate through each post-update."""
    if instance["schema"] != "wdp-realizable-observation-v1":
        raise ValueError("unknown instance schema")
    classes, refinement = protected_classes(instance["future_model"])
    expected = {s: classes[(s,)] for s in instance["states"]}
    if expected != instance["protected_class"] or refinement != instance["class_refinement"]:
        raise ValueError("protected classes do not match original future operations and prices")
    states, actions = set(instance["states"]), instance["actions"]
    if len(states) != len(instance["states"]) or len(set(actions)) != len(actions):
        raise ValueError("duplicate state or action")
    if not instance["initial"] or not set(instance["initial"]) <= states:
        raise ValueError("initial state outside carrier")
    table, post_reports = {}, {}
    for row in instance["rows"]:
        s, a, ys = row["state"], row["action"], row["successors"]
        key = (s, a)
        if s not in states or a not in actions or key in table:
            raise ValueError("duplicate or invalid transition")
        if not ys or len(set(ys)) != len(ys) or not set(ys) <= states:
            raise ValueError("invalid nonempty successor set")
        if set(row["reports"]) != set(ys) or any(type(o) is not str for o in row["reports"].values()):
            raise ValueError("incomplete actual post-state reports")
        for post, observation in row["reports"].items():
            if (post, a) in post_reports and post_reports[post, a] != observation:
                raise ValueError("report is not a function of the actual post-state and action")
            post_reports[post, a] = observation
        if type(row["cost"]) is not str or Fraction(row["cost"]) <= 0:
            raise ValueError("prices must be positive exact rational strings")
        table[key] = row
    initial = tuple(sorted((s, s) for s in instance["initial"]))
    relations, indices, moves, terminal, decoders = [initial], {initial: "n0"}, {}, set(), {}
    for z in relations:
        node = indices[z]
        originals = {expected[x] for x, _ in z}
        good = len(originals) == 1 and (answers_only or all(expected[x] == expected[y] for x, y in z))
        if good:
            terminal.add(node)
            decoders[node] = next(iter(originals))
            moves[node] = []
            continue
        moves[node] = []
        for a in actions:
            if any((y, a) not in table for _, y in z):
                continue
            # A known price is charged for the action; it cannot secretly depend on a hidden state.
            costs = {Fraction(table[y, a]["cost"]) for _, y in z}
            if len(costs) != 1:
                raise ValueError("price is not observable at this relation")
            groups = defaultdict(set)
            for x, y in z:
                row = table[y, a]
                for post in row["successors"]:
                    groups[row["reports"][post]].add((x, post))
            successors = []
            for pairs in groups.values():
                child = tuple(sorted(pairs))
                if child not in indices:
                    indices[child] = f"n{len(relations)}"
                    relations.append(child)
                successors.append(indices[child])
            moves[node].append((a, str(next(iter(costs))), sorted(set(successors))))
    model = graph_model(moves, initial="n0", targets=sorted(terminal),
                        task_id="realizable-observation/" + ("answers-only" if answers_only else "preserved-futures"))
    return {"model": model, "relations": {indices[z]: [list(p) for p in z] for z in relations},
            "decoders": decoders}


def fixed_suite_cost(instance):
    """Exact §14.6 enumeration of non-disturbing measurements on the original carrier."""
    initial, cls = instance["initial"], instance["protected_class"]
    table = {(r["state"], r["action"]): r for r in instance["rows"]}
    safe = [a for a in instance["actions"] if all((s, a) in table and
             table[s, a]["successors"] == [s] for s in instance["states"])]
    optimum, selected = None, None
    for n in range(len(safe) + 1):
        for suite in combinations(safe, n):
            groups = defaultdict(set)
            for s in initial:
                groups[tuple(table[s, a]["reports"][s] for a in suite)].add(cls[s])
            if any(len(g) > 1 for g in groups.values()):
                continue
            cost = sum((Fraction(table[initial[0], a]["cost"]) for a in suite), Fraction())
            if optimum is None or cost < optimum:
                optimum, selected = cost, suite
    return optimum, selected


def coordinate_example():
    """Full two-coordinate product, with only non-disturbing coordinate measurements."""
    instance = example(safe=False, flip=False, restore=False)
    instance["actions"] = ["coordinate_branch", "coordinate_price"]
    instance["rows"] = [{"state": s, "action": a, "successors": [s],
                         "reports": {s: s[0] if a == "coordinate_branch" else s[1]},
                         "cost": "1" if a == "coordinate_branch" else "2"}
                        for s in instance["states"] for a in instance["actions"]]
    return instance
