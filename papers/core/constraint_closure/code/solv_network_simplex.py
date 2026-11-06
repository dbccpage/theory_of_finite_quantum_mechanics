"""Port of ``omega_solvers/src/network_simplex/solver.rs``.

Integer (i128) min-cost-flow network simplex. Python ints are unbounded, so the
``checked_add``/``checked_mul`` overflow guards in Rust are effectively
unreachable; the ``ArithmeticOverflow`` error is retained for parity but will
not fire.
"""

from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from typing import List, Optional

try:
    from .network_simplex_basis import Basis
    from .network_simplex_error import NetworkSimplexError
    from .network_simplex_graph import Arc
    from .network_simplex_solution import NetworkSimplexSolution
except ImportError:
    from network_simplex_basis import Basis
    from network_simplex_error import NetworkSimplexError
    from network_simplex_graph import Arc
    from network_simplex_solution import NetworkSimplexSolution





@dataclass
class _CycleArc:
    arc: int
    direction: int


class NetworkSimplex:
    """Uncapacitated integer min-cost-flow network simplex solver.

    Requires all arcs to declare lower=0, upper=None.
    """
    def __init__(self, num_nodes: int, arcs: List[Arc], demand: List[int]):
        self.num_nodes = num_nodes
        self.num_nodes_with_root = num_nodes + 1
        self.arcs = arcs
        self.demand = demand
        self.flow: List[int] = []
        self.potential: List[int] = [0] * self.num_nodes_with_root
        self.in_tree: List[bool] = []
        self.basis = Basis(self.num_nodes_with_root)
        self.artificial_arc_start = 0

    def check_balanced_demand(self) -> None:
        if len(self.demand) != self.num_nodes:
            raise NetworkSimplexError.demand_length_mismatch(
                expected=self.num_nodes, found=len(self.demand)
            )
        s = sum(self.demand)
        if s != 0:
            raise NetworkSimplexError.unbalanced_demand(sum=s)

    def initialize_artificial_basis(self) -> None:
        self.artificial_arc_start = len(self.arcs)

        sum_costs = 0
        for arc in self.arcs:
            if arc.lower != 0 or arc.upper is not None:
                raise NetworkSimplexError.unsupported_arc_bounds(
                    f"Arc ({arc.tail} -> {arc.head}) declares lower={arc.lower}, upper={arc.upper}. "
                    f"NetworkSimplex is uncapacitated and requires lower=0, upper=None."
                )
            if arc.cost < 0:
                raise NetworkSimplexError.negative_weight(
                    edge=arc.original_edge if arc.original_edge is not None else 0,
                    weight=arc.cost,
                )
            sum_costs += abs(arc.cost)
        sum_demands = 0
        for d in self.demand:
            sum_demands += abs(d)

        m = 1 + sum_costs + sum_demands
        root = self.num_nodes

        self.flow = [0] * self.artificial_arc_start
        self.in_tree = [False] * self.artificial_arc_start

        for v in range(self.num_nodes):
            b_v = self.demand[v]
            if b_v > 0:
                self.arcs.append(
                    Arc(
                        tail=root,
                        head=v,
                        cost=m,
                        lower=0,
                        upper=None,
                        original_edge=None,
                        orientation_sign=0,
                    )
                )
                self.flow.append(b_v)
                self.in_tree.append(True)
            elif b_v < 0:
                self.arcs.append(
                    Arc(
                        tail=v,
                        head=root,
                        cost=m,
                        lower=0,
                        upper=None,
                        original_edge=None,
                        orientation_sign=0,
                    )
                )
                self.flow.append(-b_v)
                self.in_tree.append(True)
            else:
                self.arcs.append(
                    Arc(
                        tail=root,
                        head=v,
                        cost=m,
                        lower=0,
                        upper=None,
                        original_edge=None,
                        orientation_sign=0,
                    )
                )
                self.flow.append(0)
                self.in_tree.append(True)

        self.basis.rebuild(self.num_nodes_with_root, root, self.arcs, self.in_tree)

    def compute_potentials(self) -> None:
        self.potential = [0] * self.num_nodes_with_root
        root = self.num_nodes
        self.potential[root] = 0

        children: List[list] = [[] for _ in range(self.num_nodes_with_root)]
        for v in range(self.num_nodes_with_root):
            p = self.basis.parent[v]
            if p is not None:
                children[p].append(v)

        queue: deque[int] = deque()
        queue.append(root)
        while queue:
            u = queue.popleft()
            for v in children[u]:
                arc_idx = self.basis.parent_arc[v]
                assert arc_idx is not None
                arc = self.arcs[arc_idx]
                if arc.tail == u:
                    self.potential[v] = self.potential[u] + arc.cost
                else:
                    self.potential[v] = self.potential[u] - arc.cost
                queue.append(v)

    def find_entering_arc(self) -> Optional[int]:
        for a in range(len(self.arcs)):
            if not self.in_tree[a]:
                arc = self.arcs[a]
                reduced_cost = (
                    arc.cost + self.potential[arc.tail] - self.potential[arc.head]
                )
                if reduced_cost < 0:
                    return a
        return None

    def _cycle_for_entering_arc(self, entering: int) -> List[_CycleArc]:
        entering_arc = self.arcs[entering]
        u = entering_arc.tail
        v = entering_arc.head

        path_u = []
        path_v = []

        while u != v:
            depth_u = self.basis.depth[u]
            depth_v = self.basis.depth[v]
            if depth_u >= depth_v:
                parent_u = self.basis.parent[u]
                arc_u = self.basis.parent_arc[u]
                if parent_u is None or arc_u is None:
                    raise NetworkSimplexError.invalid_basis()
                path_u.append((u, arc_u))
                u = parent_u
            else:
                parent_v = self.basis.parent[v]
                arc_v = self.basis.parent_arc[v]
                if parent_v is None or arc_v is None:
                    raise NetworkSimplexError.invalid_basis()
                path_v.append((v, arc_v))
                v = parent_v

        cycle: List[_CycleArc] = []
        cycle.append(_CycleArc(arc=entering, direction=1))

        for x, arc_idx in path_v:
            arc = self.arcs[arc_idx]
            direction = 1 if arc.tail == x else -1
            cycle.append(_CycleArc(arc=arc_idx, direction=direction))

        for x, arc_idx in reversed(path_u):
            arc = self.arcs[arc_idx]
            direction = -1 if arc.tail == x else 1
            cycle.append(_CycleArc(arc=arc_idx, direction=direction))

        return cycle

    def pivot(self, entering: int) -> None:
        cycle = self._cycle_for_entering_arc(entering)

        theta = None
        found_reverse = False
        for ca in cycle:
            if ca.direction == -1:
                f = self.flow[ca.arc]
                if theta is None or f < theta:
                    theta = f
                found_reverse = True

        if not found_reverse or theta is None:
            raise NetworkSimplexError.arithmetic_overflow()

        for ca in cycle:
            if ca.direction == 1:
                self.flow[ca.arc] = self.flow[ca.arc] + theta
            else:
                self.flow[ca.arc] = self.flow[ca.arc] - theta

        leaving = None
        for ca in cycle:
            if ca.direction == -1 and self.flow[ca.arc] == 0:
                if leaving is None:
                    leaving = ca.arc
                else:
                    if ca.arc < leaving:
                        leaving = ca.arc

        if leaving is None:
            raise NetworkSimplexError.invalid_basis()

        self.in_tree[entering] = True
        self.in_tree[leaving] = False

        self.basis.rebuild(
            self.num_nodes_with_root, self.num_nodes, self.arcs, self.in_tree
        )

    def check_artificial_flows_zero(self) -> None:
        for a in range(self.artificial_arc_start, len(self.arcs)):
            if self.flow[a] > 0:
                raise NetworkSimplexError.infeasible()

    def extract_solution(self) -> NetworkSimplexSolution:
        objective = 0
        for a in range(self.artificial_arc_start):
            objective += self.flow[a] * self.arcs[a].cost

        potential = self.potential[0 : self.num_nodes]

        reduced_costs = []
        for a in range(self.artificial_arc_start):
            arc = self.arcs[a]
            rc = arc.cost + self.potential[arc.tail] - self.potential[arc.head]
            reduced_costs.append(rc)

        return NetworkSimplexSolution(
            objective=objective,
            flow=self.flow[0 : self.artificial_arc_start],
            potential=potential,
            reduced_costs=reduced_costs,
        )

    def solve(self) -> NetworkSimplexSolution:
        self.check_balanced_demand()
        self.initialize_artificial_basis()

        max_iter = max(10000, len(self.arcs) * 10)
        it = 0

        while True:
            if it >= max_iter:
                raise NetworkSimplexError.iteration_limit_exceeded(limit=max_iter)
            self.compute_potentials()
            entering = self.find_entering_arc()
            if entering is None:
                break
            self.pivot(entering)
            it += 1

        self.check_artificial_flows_zero()
        return self.extract_solution()
