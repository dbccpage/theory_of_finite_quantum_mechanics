"""Port of ``omega_solvers/src/network_simplex/basis.rs``.

Spanning-tree basis: BFS rebuild of parent / parent_arc / depth from the
set of in-tree arcs, rooted at ``root``.
"""

from __future__ import annotations
from collections import deque
from typing import List, Optional

from omega_engine.crates.linear_algebra_theory.basis import BasisDescriptor, BasisId

from omega_engine.crates.type.network_simplex_error import NetworkSimplexError
from omega_engine.crates.type.network_simplex_graph import Arc


class Basis:
    def __init__(self, num_nodes_with_root: int):
        if num_nodes_with_root < 0:
            raise NetworkSimplexError.invalid_basis()
        self.coordinate_basis = BasisDescriptor.new(
            BasisId.new("network-simplex-node-coordinates"),
            num_nodes_with_root,
        )
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
            num_nodes_with_root != self.coordinate_basis.dimension
            or root < 0
            or root >= num_nodes_with_root
            or len(in_tree) != len(arcs)
        ):
            raise NetworkSimplexError.invalid_basis()
        self.parent = [None] * num_nodes_with_root
        self.parent_arc = [None] * num_nodes_with_root
        self.depth = [0] * num_nodes_with_root

        adj: List[list] = [[] for _ in range(num_nodes_with_root)]
        for i, in_t in enumerate(in_tree):
            if in_t:
                arc = arcs[i]
                if arc.tail >= num_nodes_with_root or arc.head >= num_nodes_with_root:
                    raise NetworkSimplexError.invalid_basis()
                adj[arc.tail].append((arc.head, i))
                adj[arc.head].append((arc.tail, i))

        visited = [False] * num_nodes_with_root
        queue: deque[int] = deque()
        queue.append(root)
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

        if any(not v for v in visited):
            raise NetworkSimplexError.invalid_basis()

    def descriptor(self) -> BasisDescriptor:
        """Return the immutable coordinate-basis audit descriptor."""

        return self.coordinate_basis
