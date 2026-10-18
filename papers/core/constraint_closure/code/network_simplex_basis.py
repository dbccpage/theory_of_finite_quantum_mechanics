"""Local Basis class for network simplex in paper 002.

AuthorityEffect: None.
"""
from __future__ import annotations
from collections import deque
from typing import List, Optional

from network_simplex_error import NetworkSimplexError
from network_simplex_graph import Arc


class Basis:
    def __init__(self, num_nodes_with_root: int):
        if num_nodes_with_root < 0:
            raise NetworkSimplexError.invalid_basis()
        self.dimension = num_nodes_with_root
        self.parent: List[Optional[int]] = [None] * num_nodes_with_root
        self.parent_arc: List[Optional[int]] = [None] * num_nodes_with_root
        self.depth: List[int] = [0] * num_nodes_with_root

    def rebuild(
        self,
        num_nodes_with_root: int,
        root: int,
        arcs: List[Arc],
        in_tree: List[bool],
    ) -> None:
        if (
            num_nodes_with_root != self.dimension
            or root < 0
            or root >= num_nodes_with_root
            or len(in_tree) != len(arcs)
        ):
            raise NetworkSimplexError.invalid_basis()
        self.parent = [None] * num_nodes_with_root
        self.parent_arc = [None] * num_nodes_with_root
        self.depth = [0] * num_nodes_with_root

        adj: List[List[tuple[int, int]]] = [[] for _ in range(num_nodes_with_root)]
        for arc_idx, arc in enumerate(arcs):
            if in_tree[arc_idx]:
                adj[arc.tail].append((arc.head, arc_idx))
                adj[arc.head].append((arc.tail, arc_idx))

        visited = [False] * num_nodes_with_root
        queue: deque[int] = deque([root])
        visited[root] = True

        while queue:
            u = queue.popleft()
            for v, arc_idx in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    self.parent[v] = u
                    self.parent_arc[v] = arc_idx
                    self.depth[v] = self.depth[u] + 1
                    queue.append(v)

        if not all(visited):
            raise NetworkSimplexError.invalid_basis()


__all__ = ["Basis"]
