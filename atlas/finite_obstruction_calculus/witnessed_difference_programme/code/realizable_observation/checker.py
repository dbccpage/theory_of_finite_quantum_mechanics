"""Replay the observation-to-reachability construction without its producer.

Shared dependencies: original input, future-contract partition refinement, and
the established finite-game model/checker. No search or construct() import.
"""

from fractions import Fraction

from certified_progress.model import compile_model
from certified_progress.observation import refine_observation


def check_construction(instance, built):
    if not __debug__:
        raise RuntimeError("optimized Python disables construction assertions")
    future = compile_model(instance["future_model"])
    blocks = [[list(b) for b in future.reachable if b in future.targets],
              [list(b) for b in future.reachable if b not in future.targets]]
    refined = refine_observation(instance["future_model"], [b for b in blocks if b])
    cls = {b[0]: i for i, block in enumerate(refined["blocks"]) for b in block if len(b) == 1}
    assert {s: cls[s] for s in instance["states"]} == instance["protected_class"]
    table = {(r["state"], r["action"]): r for r in instance["rows"]}
    assert len(table) == len(instance["rows"])
    arena = compile_model(built["model"])
    relations = {node: frozenset(map(tuple, pairs)) for node, pairs in built["relations"].items()}
    assert len(set(relations.values())) == len(relations)
    assert set(relations) == set(arena.states)
    assert arena.initial == ("n0",)
    assert relations["n0"] == frozenset((s, s) for s in instance["initial"])
    reverse = {pairs: node for node, pairs in relations.items()}
    checked_edges = 0
    targets, decoders = set(), {}
    for node, pairs in relations.items():
        assert pairs and all(x in instance["initial"] and y in instance["states"] for x, y in pairs)
        original_classes = {cls[x] for x, _ in pairs}
        target = len(original_classes) == 1 and all(cls[x] == cls[y] for x, y in pairs)
        actual = {a: (c, {child[0] for child in ys}) for a, c, ys in arena.moves((node,))}
        if target:
            targets.add((node,))
            decoders[node] = next(iter(original_classes))
            assert not actual
            continue
        enabled = {a for a in instance["actions"] if all((y, a) in table for _, y in pairs)}
        assert set(actual) == enabled
        for a in enabled:
            outcomes = {(x, post, table[y, a]["reports"][post])
                        for x, y in pairs for post in table[y, a]["successors"]}
            reports = {o for _, _, o in outcomes}
            children = {frozenset((x, post) for x, post, o in outcomes if o == report)
                        for report in reports}
            assert children and all(child in reverse for child in children)
            costs = {Fraction(table[y, a]["cost"]) for _, y in pairs}
            assert len(costs) == 1 and next(iter(costs)) > 0
            assert actual[a] == (next(iter(costs)), {reverse[child] for child in children})
            checked_edges += 1
    assert arena.targets == frozenset(targets)
    assert built["decoders"] == decoders
    assert {b[0] for b in arena.reachable} == set(relations)
    return {"accepted": True, "relations": len(relations), "enabled_pairs": checked_edges,
            "terminal_decoders": len(decoders), "shared_dependencies": "future partition and finite-game model"}
