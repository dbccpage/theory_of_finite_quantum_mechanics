"""Causal order as a DAG of events, with ranks from a Kahn pass.

Origin: code/python/src/qm/campaigns/causal_order.py
Claim: every edge increases the computed rank, and the interval from 0 to 3 contains 4 events.
AuthorityEffect: None.
"""
from fractions import Fraction


class CausalOrderError(Exception):
    """The relation was cyclic or an edge failed to increase rank."""


def causal_ranks(node_count: int, edges) -> list:
    """Longest-path rank. A back edge or a cycle raises CausalOrderError."""
    indegree = [0] * node_count
    outgoing = [[] for _ in range(node_count)]
    for src, dst in edges:
        if not (0 <= src < node_count and 0 <= dst < node_count):
            raise CausalOrderError(f"edge {(src, dst)} leaves the event set")
        outgoing[src].append(dst)
        indegree[dst] += 1
    ready = [node for node in range(node_count) if indegree[node] == 0]
    rank = [0] * node_count
    seen = 0
    while ready:
        node = ready.pop()
        seen += 1
        for dst in outgoing[node]:
            rank[dst] = max(rank[dst], rank[node] + 1)
            indegree[dst] -= 1
            if indegree[dst] == 0:
                ready.append(dst)
    if seen != node_count:
        raise CausalOrderError("causal relation has a cycle")
    for src, dst in edges:
        if rank[dst] <= rank[src]:
            raise CausalOrderError(f"edge {(src, dst)} does not increase rank")
    return rank


def diamond_interval_size() -> int:
    """Events that 0 can reach and that can reach 3, on the diamond 0→1, 0→2, 1→3, 2→3."""
    edges = ((0, 1), (0, 2), (1, 3), (2, 3))
    ranks = causal_ranks(4, edges)
    reachable = {0}
    changed = True
    while changed:
        changed = False
        for src, dst in edges:
            if src in reachable and dst not in reachable:
                reachable.add(dst)
                changed = True
    can_reach_sink = {3}
    changed = True
    while changed:
        changed = False
        for src, dst in edges:
            if dst in can_reach_sink and src not in can_reach_sink:
                can_reach_sink.add(src)
                changed = True
    interval = reachable & can_reach_sink
    if Fraction(ranks[3], 1) != 2:
        raise CausalOrderError(f"diamond height is {ranks[3]}, not 2")
    return len(interval)
