"""Port of ``omega_solvers/src/phi1/l1_boundary_solver.rs``.

Integer L1 boundary / Phi1 solvers built on the ported network simplex. The
objective is uniquely determined and validated; the dual/flow vectors follow
the same deterministic pivot rules as Rust (the minimizer itself is not unique
up to ker(B)). Do NOT substitute the float LP in ``SOLVERS/phi_l1_lp.py``
(different return shape / float vs integer).
"""

from __future__ import annotations
from dataclasses import field
from dataclasses import dataclass
from typing import List

try:
    from .network_simplex_error import NetworkSimplexError
    from .network_simplex_graph import Arc
except ImportError:
    from network_simplex_error import NetworkSimplexError
    from network_simplex_graph import Arc


try:
    from solv_network_simplex import NetworkSimplex
except ImportError:
    from .solv_network_simplex import NetworkSimplex


@dataclass
class BoundaryEdge:
    tail: int
    head: int
    weight: int


@dataclass
class Boundary1:
    num_vertices: int
    edges: List[BoundaryEdge] = field(default_factory=list)


@dataclass
class Phi1Solution:
    objective: int
    z: List[int]
    vertex_potential: List[int]
    reduced_costs: List[int]


def _validate_boundary(boundary: Boundary1) -> None:
    """Reject malformed carriers before any arc/index is created (fail closed)."""
    if boundary.num_vertices <= 0:
        raise NetworkSimplexError.invalid_carrier("num_vertices must be positive")
    n = boundary.num_vertices
    for i, e in enumerate(boundary.edges):
        if e.tail < 0 or e.head < 0 or e.tail >= n or e.head >= n:
            raise NetworkSimplexError.invalid_carrier(
                f"edge endpoint out of range at {i}: ({e.tail}, {e.head})"
            )
        if e.tail == e.head:
            raise NetworkSimplexError.invalid_carrier(
                f"self-loop at edge {i}: {e.tail}"
            )
        if e.weight < 0:
            raise NetworkSimplexError.negative_weight(edge=i, weight=e.weight)


def solve_l1_boundary(boundary: Boundary1, x: List[int]) -> Phi1Solution:
    _validate_boundary(boundary)
    if boundary.num_vertices != len(x):
        raise NetworkSimplexError.demand_length_mismatch(
            expected=boundary.num_vertices, found=len(x)
        )

    arcs: List[Arc] = []
    for i, e in enumerate(boundary.edges):
        if e.weight < 0:
            raise NetworkSimplexError.negative_weight(edge=i, weight=e.weight)
        arcs.append(
            Arc(
                tail=e.tail,
                head=e.head,
                cost=e.weight,
                lower=0,
                upper=None,
                original_edge=i,
                orientation_sign=1,
            )
        )
        arcs.append(
            Arc(
                tail=e.head,
                head=e.tail,
                cost=e.weight,
                lower=0,
                upper=None,
                original_edge=i,
                orientation_sign=-1,
            )
        )

    solver = NetworkSimplex(boundary.num_vertices, arcs, list(x))
    sol = solver.solve()

    z = [0] * len(boundary.edges)
    for a_idx, arc in enumerate(solver.arcs):
        if arc.original_edge is not None:
            e_idx = arc.original_edge
            flow_val = sol.flow[a_idx]
            sign_val = arc.orientation_sign
            z[e_idx] = z[e_idx] + flow_val * sign_val

    objective = 0
    for e, ze in zip(boundary.edges, z):
        objective += e.weight * abs(ze)

    reduced_costs = []
    for e in boundary.edges:
        rc = e.weight + sol.potential[e.tail] - sol.potential[e.head]
        reduced_costs.append(rc)

    return Phi1Solution(
        objective=objective,
        z=z,
        vertex_potential=sol.potential,
        reduced_costs=reduced_costs,
    )


def solve_phi1(boundary: Boundary1, omega: List[int]) -> Phi1Solution:
    _validate_boundary(boundary)
    if len(boundary.edges) != len(omega):
        raise NetworkSimplexError.demand_length_mismatch(
            expected=len(boundary.edges), found=len(omega)
        )

    num_v = boundary.num_vertices
    num_e = len(boundary.edges)
    trans_nodes = num_v + num_e

    arcs: List[Arc] = []
    demand = [0] * trans_nodes

    for e_idx, e in enumerate(boundary.edges):
        if e.weight < 0:
            raise NetworkSimplexError.negative_weight(edge=e_idx, weight=e.weight)

        u = e.tail
        v = e.head
        w = e.weight
        om = omega[e_idx]

        c_e = om if om > 0 else 0
        y_node = num_v + e_idx

        arcs.append(
            Arc(
                tail=u,
                head=y_node,
                cost=-om + c_e,
                lower=0,
                upper=None,
                original_edge=e_idx,
                orientation_sign=1,
            )
        )
        arcs.append(
            Arc(
                tail=v,
                head=y_node,
                cost=c_e,
                lower=0,
                upper=None,
                original_edge=e_idx,
                orientation_sign=-1,
            )
        )

        demand[y_node] = 2 * w
        demand[u] = demand[u] - w
        demand[v] = demand[v] - w

    solver = NetworkSimplex(trans_nodes, arcs, demand)
    sol = solver.solve()

    alpha = [-p for p in sol.potential[0:num_v]]

    z = [0] * num_e
    objective = 0
    for e_idx, e in enumerate(boundary.edges):
        diff = alpha[e.head] - alpha[e.tail]
        ze = omega[e_idx] - diff
        z[e_idx] = ze
        objective += e.weight * abs(ze)

    phi = [0] * num_e
    for e_idx in range(num_e):
        f_plus = sol.flow[2 * e_idx]
        phi[e_idx] = f_plus - boundary.edges[e_idx].weight

    return Phi1Solution(
        objective=objective,
        z=z,
        vertex_potential=alpha,
        reduced_costs=phi,
    )
