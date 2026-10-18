"""
L1 Symbol Game Governor: P_S^2 = P_S and Monotonic Defect Descent

Exact discrete L1 projection governor for formal deduction and reasoning governance:
- Integer/Fraction cochain representation over finite constraint graphs.
- Simplicial boundary operator: partial_1(u -> v) = v - u.
- Section defect norm:
    D(s) = sum_{e=(u,v)} w_e |claim_e - (s(v) - s(u))|
- Exact rational primary obstruction evaluation:
    Phi_1([claim]) = min_{f in C^0(G)} sum_{e=(u,v)} w_e |claim_e - (f(v) - f(u))|
- Idempotent projection governor:
    P_S(s) = s + f* such that D(P_S(s)) = Phi_1([claim]), satisfying P_S(P_S(s)) = P_S(s).
- Strict monotonic defect descent:
    D(s_{t+1}) <= D(s_t) on potential cuts, and Phi_1(R_{t+1}) <= Phi_1(R_t) on relational repairs.
- 4-move state machine: ASSERT, CUT, VERIFY, RETRACT with history snapshotting.
- Strict invariant preservation: diagonal excision (sigma_{x=y} = empty).
- Zero floating-point arithmetic.

AuthorityEffect: None.
Firewall Line: stated region only; mints no authority
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from enum import Enum
from fractions import Fraction
from typing import (
    Any,
    Dict,
    FrozenSet,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)


def require_exact(value):
    if type(value) not in (int, Fraction):
        raise TypeError("exact integer or Fraction required")
    return Fraction(value)


@dataclass(frozen=True)
class Edge:
    """Directed edge (cut) in a constraint graph: u -> v with weight >= 1."""
    u: str
    v: str
    weight: Union[int, Fraction] = 1

    def __post_init__(self) -> None:
        if self.u == self.v:
            raise ValueError(f"Self-loop {self.u} -> {self.v} violates irreflexivity.")
        require_exact(self.weight)
        if self.weight <= 0:
            raise ValueError(f"Edge weight must be positive, got {self.weight}.")

    @property
    def key(self) -> Tuple[str, str]:
        return (self.u, self.v)


@dataclass
class ConstraintGraph:
    """Finite constraint graph with carrier vertices and directed edges."""
    vertices: Tuple[str, ...] = ()
    edges: Tuple[Edge, ...] = ()

    def __post_init__(self) -> None:
        v_set = set(self.vertices)
        for e in self.edges:
            if e.u not in v_set:
                raise ValueError(f"Edge source '{e.u}' not in declared vertices.")
            if e.v not in v_set:
                raise ValueError(f"Edge target '{e.v}' not in declared vertices.")

    def add_edge(self, u: str, v: str, weight: Union[int, Fraction] = 1) -> Edge:
        """Add a directed edge u -> v, adding endpoints to vertices if needed."""
        edge = Edge(u=u, v=v, weight=weight)
        v_list = list(self.vertices)
        if u not in v_list:
            v_list.append(u)
        if v not in v_list:
            v_list.append(v)
        self.vertices = tuple(v_list)
        self.edges = self.edges + (edge,)
        return edge

    def edge_by_pair(self, u: str, v: str) -> Optional[Edge]:
        for e in self.edges:
            if e.u == u and e.v == v:
                return e
        return None

    def connected_components(self) -> List[List[str]]:
        """Computes connected components of the underlying undirected graph."""
        adj: Dict[str, Set[str]] = {v: set() for v in self.vertices}
        for e in self.edges:
            adj[e.u].add(e.v)
            adj[e.v].add(e.u)

        visited: Set[str] = set()
        components: List[List[str]] = []
        for v in self.vertices:
            if v not in visited:
                comp: List[str] = []
                stack = [v]
                visited.add(v)
                while stack:
                    curr = stack.pop()
                    comp.append(curr)
                    for nxt in adj[curr]:
                        if nxt not in visited:
                            visited.add(nxt)
                            stack.append(nxt)
                components.append(sorted(comp))
        return components


@dataclass(frozen=True)
class Cochain1:
    """
    1-Cochain over graph edges with exact rational coefficients.
    Maps directed edges (u, v) or Edge instances to Fraction values.
    """
    values: Dict[Any, Fraction]

    def get(self, u: str, v: str) -> Fraction:
        if (u, v) in self.values:
            return self.values[(u, v)]
        for k, val in self.values.items():
            if isinstance(k, Edge) and k.u == u and k.v == v:
                return val
        return Fraction(0)

    def support(self) -> Set[Tuple[str, str]]:
        """Set of edges (u, v) where cochain value is non-zero."""
        res: Set[Tuple[str, str]] = set()
        for k, val in self.values.items():
            if val != Fraction(0):
                if isinstance(k, Edge):
                    res.add((k.u, k.v))
                else:
                    res.add(k)
        return res

    def l1_norm(self, weights: Optional[Dict[Tuple[str, str], Union[int, Fraction]]] = None) -> Fraction:
        """Computes exact L1 norm sum_e w_e |delta_e|."""
        total = Fraction(0)
        for k, val in self.values.items():
            key = (k.u, k.v) if isinstance(k, Edge) else k
            w = weights.get(key, 1) if weights else 1
            total += Fraction(w) * abs(val)
        return total


def boundary_operator_c1_to_c0(u: str, v: str) -> Dict[str, int]:
    """
    Simplicial boundary operator partial_1: C_1 -> C_0.
    partial_1(u -> v) = v - u.
    """
    if u == v:
        return {}  # Self-loop boundary cancels to 0
    return {v: 1, u: -1}


def compute_coboundary(section: Dict[str, Fraction], edges: Sequence[Edge]) -> Cochain1:
    """
    Coboundary operator d_0: C^0 -> C^1.
    (d_0 s)(u, v) = s(v) - s(u).
    """
    values: Dict[Tuple[str, str], Fraction] = {}
    for e in edges:
        val_u = section.get(e.u, Fraction(0))
        val_v = section.get(e.v, Fraction(0))
        values[e.key] = val_v - val_u
    return Cochain1(values=values)


def find_spanning_forest_potentials(
    graph: ConstraintGraph,
    claims: Cochain1,
) -> List[Dict[str, Fraction]]:
    """
    Enumerates candidate gauge potentials f in C^0(G) by finding all spanning trees
    per connected component.
    By polyhedral theory (LP on totally unimodular node-arc incidence matrix),
    every basic feasible solution to min_f sum_e w_e |claim_e - (f_v - f_u)|
    corresponds to a spanning tree where claim_e = f_v - f_u along tree edges.
    """
    components = graph.connected_components()
    candidate_component_potentials: List[List[Dict[str, Fraction]]] = []

    for comp in components:
        comp_set = set(comp)
        comp_edges = [e for e in graph.edges if e.u in comp_set and e.v in comp_set]
        comp_candidates: List[Dict[str, Fraction]] = []

        # Trivial baseline: all zero potential
        comp_candidates.append({v: Fraction(0) for v in comp})

        if len(comp) == 1 or not comp_edges:
            candidate_component_potentials.append(comp_candidates)
            continue

        target_tree_edges = len(comp) - 1

        def get_all_trees(
            edge_idx: int,
            current_edges: List[Edge],
            parent: Dict[str, str],
        ) -> Iterator[List[Edge]]:
            if len(current_edges) == target_tree_edges:
                yield list(current_edges)
                return
            if edge_idx >= len(comp_edges):
                return
            if len(current_edges) + (len(comp_edges) - edge_idx) < target_tree_edges:
                return

            e = comp_edges[edge_idx]

            def find(node: str) -> str:
                curr = node
                while parent[curr] != curr:
                    curr = parent[curr]
                return curr

            root_u = find(e.u)
            root_v = find(e.v)

            if root_u != root_v:
                new_parent = dict(parent)
                new_parent[root_u] = root_v
                current_edges.append(e)
                yield from get_all_trees(edge_idx + 1, current_edges, new_parent)
                current_edges.pop()

            yield from get_all_trees(edge_idx + 1, current_edges, parent)

        init_parent = {v: v for v in comp}
        spanning_trees = list(get_all_trees(0, [], init_parent))

        for tree in spanning_trees:
            root = comp[0]
            f_tree: Dict[str, Fraction] = {root: Fraction(0)}

            tree_adj: Dict[str, List[Tuple[str, Fraction]]] = {v: [] for v in comp}
            for e in tree:
                d_val = claims.get(e.u, e.v)
                tree_adj[e.u].append((e.v, d_val))
                tree_adj[e.v].append((e.u, -d_val))

            stack = [root]
            visited = {root}
            while stack:
                u = stack.pop()
                for v, delta_uv in tree_adj[u]:
                    if v not in visited:
                        visited.add(v)
                        f_tree[v] = f_tree[u] + delta_uv
                        stack.append(v)

            comp_candidates.append(f_tree)

        candidate_component_potentials.append(comp_candidates)

    # Combine component potentials by Cartesian product
    total_potentials: List[Dict[str, Fraction]] = [{}]
    for comp_cands in candidate_component_potentials:
        next_totals: List[Dict[str, Fraction]] = []
        for base in total_potentials:
            for cand in comp_cands:
                merged = dict(base)
                merged.update(cand)
                next_totals.append(merged)
        total_potentials = next_totals

    return total_potentials


def compute_phi1(
    graph: ConstraintGraph,
    claims: Cochain1,
) -> Tuple[Fraction, Dict[str, Fraction]]:
    """Transport graph Phi1 evaluation to the pinned native functional adapter."""
    from omega_engine_woland.infrastructure.providers.adapters.native_functional import compute_graph_phi1

    for value in claims.values.values():
        require_exact(value)
    known = {edge.key for edge in graph.edges}
    claimed = {(key.u, key.v) if isinstance(key, Edge) else key for key in claims.values}
    if claimed - known:
        raise ValueError("claim edge absent from declared carrier")
    return compute_graph_phi1(
        graph.vertices,
        [(edge.u, edge.v, edge.weight) for edge in graph.edges],
        {edge.key: claims.get(edge.u, edge.v) for edge in graph.edges},
    )


class MoveType(Enum):
    """The 4-move vocabulary of the discrete Symbol Game Governor."""
    ASSERT = "ASSERT"    # Asserts ground edge claim (u -> v with expected value)
    CUT = "CUT"          # Applies deduction / repair step targeting defect
    VERIFY = "VERIFY"    # Mechanically evaluates formal obligation
    RETRACT = "RETRACT"  # Reverts state to snapshot in history


@dataclass(frozen=True)
class MoveProposal:
    """Proposal envelope submitted to the Governor."""
    step_id: str
    move_type: MoveType
    payload: Dict[str, Any]
    parent_step_id: Optional[str] = None
    expected_delta_phi: Optional[Fraction] = None


@dataclass(frozen=True)
class GovernorVerdict:
    """Audit outcome emitted by the Governor."""
    admitted: bool
    status: str
    defect_before: Fraction
    defect_after: Fraction
    details: str
    step_id: str


@dataclass
class ExecutionRecord:
    """Audit trail record stored in derivation history."""
    step_id: str
    parent_step_id: Optional[str]
    move_type: MoveType
    payload: Dict[str, Any]
    defect_before: Fraction
    defect_after: Fraction
    admitted: bool
    status: str
    details: str
    snapshot_section: Dict[str, Fraction]
    snapshot_edge_claims: Dict[Tuple[str, str], Fraction]


class L1SymbolGameGovernor:
    """
    Discrete L1 projection governor maintaining an exact state machine:
    P_S: section -> projected_section such that P_S^2 = P_S.
    Enforces monotonic defect descent and diagonal excision.
    """

    def __init__(self, graph: ConstraintGraph) -> None:
        self.graph = graph
        self.section: Dict[str, Fraction] = {v: Fraction(0) for v in graph.vertices}
        self.edge_claims: Dict[Tuple[str, str], Fraction] = {}
        self.history: List[ExecutionRecord] = []
        self._step_counter: int = 0

    def claims_cochain(self) -> Cochain1:
        """Returns active edge claims as a 1-cochain."""
        return Cochain1(values=dict(self.edge_claims))

    def section_defect(self, section: Optional[Dict[str, Fraction]] = None) -> Fraction:
        """
        Computes the L1 defect norm of section s against active edge claims:
        D(s) = sum_e w_e |claim_e - (s(v) - s(u))|.
        """
        s = self.section if section is None else section
        total = Fraction(0)
        for e in self.graph.edges:
            claim = self.edge_claims.get(e.key, Fraction(0))
            diff = s.get(e.v, Fraction(0)) - s.get(e.u, Fraction(0))
            total += Fraction(e.weight) * abs(claim - diff)
        return total

    def primary_obstruction(self) -> Fraction:
        """
        Computes the irreducible primary obstruction:
        Phi_1([claim]) = min_f D(f) = D(P_S(s)).
        """
        norm, _ = compute_phi1(self.graph, self.claims_cochain())
        return norm

    def project(self, section: Dict[str, Fraction]) -> Dict[str, Fraction]:
        """
        Idempotent Projection Operator P_S.
        Finds optimal gauge repair f* minimizing D(s + f*).
        Yields P_S(s) = s + f* with D(P_S(s)) = Phi_1([claim]).
        Satisfies P_S(P_S(s)) = P_S(s).
        """
        res_values: Dict[Tuple[str, str], Fraction] = {}
        for e in self.graph.edges:
            claim = self.edge_claims.get(e.key, Fraction(0))
            pot_diff = section.get(e.v, Fraction(0)) - section.get(e.u, Fraction(0))
            res_values[e.key] = claim - pot_diff

        res_cochain = Cochain1(values=res_values)
        _, best_gauge = compute_phi1(self.graph, res_cochain)

        projected: Dict[str, Fraction] = {}
        for v in self.graph.vertices:
            projected[v] = section.get(v, Fraction(0)) + best_gauge.get(v, Fraction(0))
        return projected

    def verify_idempotence(self, section: Dict[str, Fraction]) -> bool:
        """Verifies the projection identity P_S^2 = P_S."""
        p1 = self.project(section)
        p2 = self.project(p1)

        diff_p1 = compute_coboundary(p1, self.graph.edges)
        diff_p2 = compute_coboundary(p2, self.graph.edges)
        return diff_p1.values == diff_p2.values

    def step_assert(
        self,
        u: str,
        v: str,
        value: Union[int, Fraction],
        step_id: Optional[str] = None,
    ) -> GovernorVerdict:
        """
        ASSERT Move:
        Asserts an edge claim u -> v with declared difference value.
        Enforces irreflexivity: u != v (rejects self-loops).
        """
        val_frac = require_exact(value)
        self._step_counter += 1
        sid = step_id or f"step_{self._step_counter:03d}"
        defect_before = self.section_defect()

        # Invariant 1: Diagonal Excision (Irreflexivity)
        if u == v:
            return GovernorVerdict(
                admitted=False,
                status="InvariantViolation",
                defect_before=defect_before,
                defect_after=defect_before,
                details=f"Diagonal self-cut '{u} -> {v}' violates irreflexivity (sigma_{{x=y}} = empty).",
                step_id=sid,
            )

        if u not in self.graph.vertices or v not in self.graph.vertices:
            return GovernorVerdict(
                admitted=False,
                status="InvariantViolation",
                defect_before=defect_before,
                defect_after=defect_before,
                details=f"Vertices ({u}, {v}) exceed declared carrier {self.graph.vertices}.",
                step_id=sid,
            )

        if self.graph.edge_by_pair(u, v) is None:
            return GovernorVerdict(
                admitted=False,
                status="MoveViolation",
                defect_before=defect_before,
                defect_after=defect_before,
                details=f"Edge ({u}, {v}) is not in the declared constraint graph.",
                step_id=sid,
            )

        # Apply proposed assertion
        self.edge_claims[(u, v)] = val_frac
        defect_after = self.section_defect()

        rec = ExecutionRecord(
            step_id=sid,
            parent_step_id=self.history[-1].step_id if self.history else None,
            move_type=MoveType.ASSERT,
            payload={"u": u, "v": v, "value": val_frac},
            defect_before=defect_before,
            defect_after=defect_after,
            admitted=True,
            status="Asserted",
            details=f"Asserted relation claim '{u} -> {v}' = {val_frac}.",
            snapshot_section=dict(self.section),
            snapshot_edge_claims=dict(self.edge_claims),
        )
        self.history.append(rec)

        return GovernorVerdict(
            admitted=True,
            status="Asserted",
            defect_before=defect_before,
            defect_after=defect_after,
            details=f"Asserted relation claim '{u} -> {v}' = {val_frac}.",
            step_id=sid,
        )

    def step_cut(
        self,
        proposed_section: Optional[Dict[str, Fraction]] = None,
        proposed_claims: Optional[Dict[Tuple[str, str], Fraction]] = None,
        step_id: Optional[str] = None,
    ) -> GovernorVerdict:
        """
        CUT Move:
        Proposes either:
        1. An updated section (potential assignment) to resolve active defects, or
        2. An updated set of edge claims (relational repair) resolving a contradiction.
        Enforces monotonic defect non-increase: D(s_new) <= D(s_old) or Phi_1(new) <= Phi_1(old).
        """
        self._step_counter += 1
        sid = step_id or f"step_{self._step_counter:03d}"

        if proposed_section is not None:
            defect_before = self.section_defect()
            defect_after = self.section_defect(proposed_section)

            if defect_after > defect_before:
                return GovernorVerdict(
                    admitted=False,
                    status="DefectIncrease",
                    defect_before=defect_before,
                    defect_after=defect_after,
                    details=f"Section defect increased from {defect_before} to {defect_after}. Monotonic descent violated.",
                    step_id=sid,
                )

            # Commit proposed section
            self.section = {v: proposed_section.get(v, Fraction(0)) for v in self.graph.vertices}

            status = "ExactRepair" if (defect_after == Fraction(0) and defect_before > Fraction(0)) else (
                "MonotonicDescent" if defect_after < defect_before else "IdempotentStationary"
            )

            rec = ExecutionRecord(
                step_id=sid,
                parent_step_id=self.history[-1].step_id if self.history else None,
                move_type=MoveType.CUT,
                payload={"proposed_section": dict(proposed_section)},
                defect_before=defect_before,
                defect_after=defect_after,
                admitted=True,
                status=status,
                details=f"CUT move accepted with status {status} ({defect_before} -> {defect_after}).",
                snapshot_section=dict(self.section),
                snapshot_edge_claims=dict(self.edge_claims),
            )
            self.history.append(rec)

            return GovernorVerdict(
                admitted=True,
                status=status,
                defect_before=defect_before,
                defect_after=defect_after,
                details=f"CUT move accepted with status {status} ({defect_before} -> {defect_after}).",
                step_id=sid,
            )

        if proposed_claims is not None:
            # 1. Diagonal Excision (Irreflexivity: u != v)
            for (u, v) in proposed_claims.keys():
                if u == v:
                    return GovernorVerdict(
                        admitted=False,
                        status="InvariantViolation",
                        defect_before=self.primary_obstruction(),
                        defect_after=self.primary_obstruction(),
                        details=f"Diagonal self-cut '({u}, {v})' violates irreflexivity (sigma_{{x=y}} = empty).",
                        step_id=sid,
                    )

            # 2. Carrier Boundary Check (u, v in carrier)
            for (u, v) in proposed_claims.keys():
                if u not in self.graph.vertices or v not in self.graph.vertices:
                    return GovernorVerdict(
                        admitted=False,
                        status="CarrierViolation",
                        defect_before=self.primary_obstruction(),
                        defect_after=self.primary_obstruction(),
                        details=f"Vertices ({u}, {v}) exceed declared carrier {self.graph.vertices}.",
                        step_id=sid,
                    )

            # 3. Production surface check: claims may update only declared edges.
            for (u, v) in proposed_claims.keys():
                if self.graph.edge_by_pair(u, v) is None:
                    return GovernorVerdict(
                        admitted=False,
                        status="MoveViolation",
                        defect_before=self.primary_obstruction(),
                        defect_after=self.primary_obstruction(),
                        details=f"Edge ({u}, {v}) is not in the declared constraint graph.",
                        step_id=sid,
                    )

            # 4. Anti-erasure check: cannot erase constraints or omit asserted edges.
            if not proposed_claims and self.edge_claims:
                return GovernorVerdict(
                    admitted=False,
                    status="UnlicensedClaimChange",
                    defect_before=self.primary_obstruction(),
                    defect_after=self.primary_obstruction(),
                    details="Claim changes cannot erase declared problem constraints.",
                    step_id=sid,
                )
            if not set(self.edge_claims.keys()).issubset(set(proposed_claims.keys())):
                return GovernorVerdict(
                    admitted=False,
                    status="UnlicensedClaimChange",
                    defect_before=self.primary_obstruction(),
                    defect_after=self.primary_obstruction(),
                    details="Claim changes cannot omit asserted edges.",
                    step_id=sid,
                )

            for value in proposed_claims.values():
                require_exact(value)

            phi_before = self.primary_obstruction()
            phi_after, _ = compute_phi1(self.graph, Cochain1(values=dict(proposed_claims)))

            if phi_after > phi_before:
                return GovernorVerdict(
                    admitted=False,
                    status="DefectIncrease",
                    defect_before=phi_before,
                    defect_after=phi_after,
                    details=f"Primary obstruction increased from {phi_before} to {phi_after}. Monotonic descent violated.",
                    step_id=sid,
                )

            self.edge_claims = dict(proposed_claims)
            self.section = self.project(self.section)
            status = "ExactRepair" if (phi_after == Fraction(0) and phi_before > Fraction(0)) else (
                "MonotonicDescent" if phi_after < phi_before else "IdempotentStationary"
            )

            rec = ExecutionRecord(
                step_id=sid,
                parent_step_id=self.history[-1].step_id if self.history else None,
                move_type=MoveType.CUT,
                payload={"proposed_claims": dict(proposed_claims)},
                defect_before=phi_before,
                defect_after=phi_after,
                admitted=True,
                status=status,
                details=f"Relational CUT move accepted ({phi_before} -> {phi_after}).",
                snapshot_section=dict(self.section),
                snapshot_edge_claims=dict(self.edge_claims),
            )
            self.history.append(rec)

            return GovernorVerdict(
                admitted=True,
                status=status,
                defect_before=phi_before,
                defect_after=phi_after,
                details=f"Relational CUT move accepted ({phi_before} -> {phi_after}).",
                step_id=sid,
            )

        return GovernorVerdict(
            admitted=False,
            status="Refused",
            defect_before=self.section_defect(),
            defect_after=self.section_defect(),
            details="CUT proposal must provide either proposed_section or proposed_claims.",
            step_id=sid,
        )

    def step_verify(
        self,
        obligation: str,
        step_id: Optional[str] = None,
    ) -> GovernorVerdict:
        """
        VERIFY Move:
        Mechanically verifies whether active defects are zero (exact cocycle)
        or whether a specific edge condition holds.
        """
        self._step_counter += 1
        sid = step_id or f"step_{self._step_counter:03d}"
        d_val = self.section_defect()

        if obligation == "ZERO_DEFECT":
            passed = (d_val == Fraction(0))
            details = "Defect is exactly zero (exact cocycle)." if passed else f"Non-zero obstruction/defect: {d_val}."
        elif obligation == "ZERO_OBSTRUCTION":
            phi = self.primary_obstruction()
            passed = (phi == Fraction(0))
            details = "Primary obstruction Phi_1 is zero." if passed else f"Obstruction Phi_1 = {phi}."
        elif obligation.startswith("EDGE_MATCH:"):
            _, pair = obligation.split(":", 1)
            if "," not in pair:
                passed = False
                details = f"Malformed EDGE_MATCH pair: '{pair}'."
            else:
                u, v = pair.split(",", 1)
                u, v = u.strip(), v.strip()
                if u not in self.graph.vertices or v not in self.graph.vertices:
                    passed = False
                    details = f"Vertices '{u}' or '{v}' not declared in graph."
                elif not any(e.u == u and e.v == v for e in self.graph.edges):
                    passed = False
                    details = f"Edge '{u}->{v}' is not a declared edge in graph."
                elif (u, v) not in self.edge_claims:
                    passed = False
                    details = f"Edge '{u}->{v}' has no asserted claim."
                else:
                    claim = self.edge_claims[(u, v)]
                    actual = self.section.get(v, Fraction(0)) - self.section.get(u, Fraction(0))
                    passed = (claim == actual)
                    details = f"Edge {u}->{v}: claim={claim}, actual={actual}."
        else:
            passed = False
            details = f"Unknown obligation '{obligation}'."

        status = "Verified" if passed else "VerificationFailed"
        return GovernorVerdict(
            admitted=passed,
            status=status,
            defect_before=d_val,
            defect_after=d_val,
            details=details,
            step_id=sid,
        )

    def step_retract(
        self,
        target_step_id: str,
        reason: str = "",
        step_id: Optional[str] = None,
    ) -> GovernorVerdict:
        """
        RETRACT Move:
        Rolls back to the snapshot of target_step_id in history.
        Restores section and edge claims to that point.
        """
        self._step_counter += 1
        sid = step_id or f"step_{self._step_counter:03d}"
        defect_before = self.section_defect()

        target_idx = -1
        for i, rec in enumerate(self.history):
            if rec.step_id == target_step_id:
                target_idx = i
                break

        if target_idx < 0:
            return GovernorVerdict(
                admitted=False,
                status="Refused",
                defect_before=defect_before,
                defect_after=defect_before,
                details=f"Target step '{target_step_id}' not found in derivation history.",
                step_id=sid,
            )

        target_rec = self.history[target_idx]
        self.section = dict(target_rec.snapshot_section)
        self.edge_claims = dict(target_rec.snapshot_edge_claims)
        defect_after = self.section_defect()

        retract_rec = ExecutionRecord(
            step_id=sid,
            parent_step_id=self.history[-1].step_id,
            move_type=MoveType.RETRACT,
            payload={"target_step_id": target_step_id, "reason": reason},
            defect_before=defect_before,
            defect_after=defect_after,
            admitted=True,
            status="Retracted",
            details=f"State reverted to snapshot at '{target_step_id}'. Reason: {reason}",
            snapshot_section=dict(self.section),
            snapshot_edge_claims=dict(self.edge_claims),
        )
        self.history.append(retract_rec)

        return GovernorVerdict(
            admitted=True,
            status="Retracted",
            defect_before=defect_before,
            defect_after=defect_after,
            details=f"State reverted to snapshot at '{target_step_id}'. Reason: {reason}",
            step_id=sid,
        )

    def execute_proposal(self, proposal: MoveProposal) -> GovernorVerdict:
        """Dispatches a structured MoveProposal envelope to the appropriate handler."""
        if proposal.move_type == MoveType.ASSERT:
            return self.step_assert(
                u=proposal.payload["u"],
                v=proposal.payload["v"],
                value=proposal.payload.get("value", Fraction(1)),
                step_id=proposal.step_id,
            )
        if proposal.move_type == MoveType.CUT:
            return self.step_cut(
                proposed_section=proposal.payload.get("proposed_section"),
                proposed_claims=proposal.payload.get("proposed_claims"),
                step_id=proposal.step_id,
            )
        if proposal.move_type == MoveType.VERIFY:
            return self.step_verify(
                obligation=proposal.payload["obligation"],
                step_id=proposal.step_id,
            )
        if proposal.move_type == MoveType.RETRACT:
            return self.step_retract(
                target_step_id=proposal.payload["target_step_id"],
                reason=proposal.payload.get("reason", ""),
                step_id=proposal.step_id,
            )
        raise ValueError(f"Unknown move type: {proposal.move_type}")

    def evaluate_proposal(self, proposal: MoveProposal) -> GovernorVerdict:
        """Alias for execute_proposal conforming to interface contracts."""
        return self.execute_proposal(proposal)


__all__ = [
    "Edge",
    "ConstraintGraph",
    "Cochain1",
    "boundary_operator_c1_to_c0",
    "compute_coboundary",
    "find_spanning_forest_potentials",
    "compute_phi1",
    "MoveType",
    "MoveProposal",
    "GovernorVerdict",
    "ExecutionRecord",
    "L1SymbolGameGovernor",
]
