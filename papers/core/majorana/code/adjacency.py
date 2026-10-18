from typing import List, Tuple, Dict, Any


def build_adjacency(
    nodes: List[Any], edges: List[Tuple[Any, Any]]
) -> Dict[Any, List[Any]]:
    adj: Dict[Any, List[Any]] = {v: [] for v in nodes}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return adj

