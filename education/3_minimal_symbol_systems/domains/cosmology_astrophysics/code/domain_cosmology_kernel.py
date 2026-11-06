"""Finite order and simplicial boundary examples.
AuthorityEffect: None. The staged scenario records declared transitions;
it does not establish cosmology, horizons, a dimension estimator, or quantum gravity.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class PrimitiveDifferenceSetting:
    """Root W Witnessed Irreflexive Difference Germ: (X, R, a, b)."""

    carrier: Set[str]
    relation: Set[Tuple[str, str]]
    a: str
    b: str

    def is_irrefl(self) -> bool:
        """Verifies irreflexivity: forall x in carrier, (x, x) not in relation."""
        return all((x, x) not in self.relation for x in self.carrier)

    def is_witnessed(self) -> bool:
        """Verifies witness existence: (a, b) in relation."""
        return (self.a, self.b) in self.relation

    def is_distinct(self) -> bool:
        """Theorem of Distinctness: a != b under witnessed irreflexivity."""
        return self.a != self.b and self.is_witnessed() and self.is_irrefl()

    def transpose(self, edge: Tuple[str, str]) -> Tuple[str, str]:
        """Transposition operator sigma = (u, v) -> (v, u)."""
        return (edge[1], edge[0])

    def evaluate_1chain_boundary(self, edge: Tuple[str, str]) -> Dict[str, int]:
        """Oriented 1-chain boundary: partial_1(u, v) = {v: +1, u: -1}."""
        u, v = edge
        if u == v:
            return {}
        return {v: 1, u: -1}

    def verify_transposition_sign_inversion(self, edge: Tuple[str, str]) -> bool:
        """Verifies partial_1(sigma(e)) == -partial_1(e)."""
        u, v = edge
        if u == v:
            return False
        b_orig = self.evaluate_1chain_boundary(edge)
        b_trans = self.evaluate_1chain_boundary(self.transpose(edge))
        for pt in [u, v]:
            if b_trans.get(pt, 0) != -b_orig.get(pt, 0):
                return False
        return True


@dataclass
class CausalIntervalReceipt:
    """Certified Alexandrov interval I(x, y) in a causal set."""

    x: str
    y: str
    interval_elements: List[str]
    cardinality: int
    is_locally_finite: bool
    authority_effect: str = "None"


@dataclass
class CausalSetReceipt:
    """Certified discrete causal set (C, prec) properties."""

    num_elements: int
    num_causal_relations: int
    num_irreducible_links: int
    is_acyclic: bool
    is_locally_finite: bool
    interval_comparable_fraction: Optional[float]
    hasse_links: List[Tuple[str, str]]
    authority_effect: str = "None"


@dataclass
class ReggeSpacetimeReceipt:
    """Finite tetrahedron boundary products; no spacetime or Hamiltonian claim."""

    num_vertices: int
    num_edges: int
    num_faces: int
    num_tetrahedra: int
    b1_matrix: List[List[int]]
    b2_matrix: List[List[int]]
    b3_matrix: List[List[int]]
    is_b1_b2_nilpotent: bool
    is_b2_b3_nilpotent: bool
    euler_characteristic: int
    boundary_defect: int
    authority_effect: str = "None"

    def __bool__(self) -> bool:
        return self.is_b1_b2_nilpotent and self.is_b2_b3_nilpotent


@dataclass
class SimplicialBoundaryReceipt:
    """Certified receipt of simplicial boundary nilpotency B_1 * B_2 = 0."""

    vertices: List[str]
    edges: List[Tuple[str, str]]
    faces: List[Tuple[str, str, str]]
    b1_matrix: List[List[int]]
    b2_matrix: List[List[int]]
    product_matrix: List[List[int]]
    is_nilpotent: bool
    num_cycles: int
    euler_characteristic: int
    authority_effect: str = "None"

    def __bool__(self) -> bool:
        return self.is_nilpotent


@dataclass
class DomainState:
    step: int
    name: str
    carrier: Set[str] = field(default_factory=set)
    relations: Set[Tuple[str, str]] = field(default_factory=set)
    invariants: Dict[str, Any] = field(default_factory=dict)
    history: List[str] = field(default_factory=list)
    branches_retained: List[str] = field(default_factory=list)
    branch_metadata: Dict[str, Dict[str, Any]] = field(default_factory=dict)


class CausalSet:
    """
    Locally finite partially ordered set (C, prec) representing discrete spacetime.
    Satisfies irreflexivity, transitivity, acyclicity, and finite Alexandrov intervals.
    """

    def __init__(self, elements: List[str], causal_relations: Set[Tuple[str, str]]):
        self.elements = list(elements)
        self.element_set = set(elements)
        self.relations: Set[Tuple[str, str]] = set()

        # Validate elements
        for u, v in causal_relations:
            if u not in self.element_set or v not in self.element_set:
                raise ValueError(f"Relation ({u}, {v}) references non-existent element.")
            if u == v:
                raise ValueError(f"Causal self-loop ({u}, {u}) violates irreflexivity.")
            self.relations.add((u, v))

        # Enforce transitive closure
        self._enforce_transitive_closure()

        # Check acyclicity
        self._check_acyclicity()

    def _enforce_transitive_closure(self) -> None:
        changed = True
        while changed:
            changed = False
            new_rel = set()
            for u, v in self.relations:
                for x, y in self.relations:
                    if v == x and (u, y) not in self.relations:
                        if u == y:
                            raise ValueError(f"Causal cycle detected involving element '{u}'.")
                        new_rel.add((u, y))
            if new_rel:
                self.relations.update(new_rel)
                changed = True

    def _check_acyclicity(self) -> None:
        for u, v in self.relations:
            if (v, u) in self.relations:
                raise ValueError(f"Acyclicity violated: causal cycle between '{u}' and '{v}'.")

    def alexandrov_interval(self, x: str, y: str) -> List[str]:
        """Alexandrov interval I(x, y) = {z in C | x prec z prec y}."""
        if (x, y) not in self.relations:
            return []
        interval = [
            z for z in self.elements if (x, z) in self.relations and (z, y) in self.relations
        ]
        return sorted(interval)

    def hasse_links(self) -> List[Tuple[str, str]]:
        """Unrefinable causal links: x prec* y iff x prec y and I(x, y) == empty."""
        links = []
        for x, y in self.relations:
            if len(self.alexandrov_interval(x, y)) == 0:
                links.append((x, y))
        return sorted(links)

    def interval_relation_fraction(self, x, y):
        """Fraction of comparable pairs in a declared interval; not a dimension estimator."""
        if x not in self.elements or y not in self.elements or (x,y) not in self.relations:
            return None
        elements = [x] + self.alexandrov_interval(x,y) + [y]
        possible = len(elements) * (len(elements)-1) // 2
        count = sum((u,v) in self.relations for u in elements for v in elements)
        return count / possible if possible else None

    def compute_bipartite_link_cut(self, past_set: Set[str], future_set: Set[str]) -> int:
        """
        Counts causal links crossing from past_set to future_set (finite crossing-link count).
        """
        links = self.hasse_links()
        crossing = sum(1 for (u, v) in links if u in past_set and v in future_set)
        return crossing

    def emit_receipt(self) -> CausalSetReceipt:
        links = self.hasse_links()
        dim = None
        if len(self.elements) >= 3:
            # find an endpoint pair with maximal interval
            max_pair = None
            max_len = -1
            for x, y in sorted(self.relations):
                iv_len = len(self.alexandrov_interval(x, y))
                if iv_len > max_len:
                    max_len = iv_len
                    max_pair = (x, y)
            if max_pair and max_len > 0:
                dim = self.interval_relation_fraction(max_pair[0], max_pair[1])

        return CausalSetReceipt(
            num_elements=len(self.elements),
            num_causal_relations=len(self.relations),
            num_irreducible_links=len(links),
            is_acyclic=True,
            is_locally_finite=True,
            interval_comparable_fraction=dim,
            hasse_links=links,
            authority_effect="None",
        )


class DomainEngine:
    """Deterministic transition engine for cosmology_astrophysics domain."""

    def __init__(self):
        self.state = DomainState(step=0, name="state_empty_void")
        self.setting: Optional[PrimitiveDifferenceSetting] = None
        self.causal_set: Optional[CausalSet] = None
        self.gap_detected: bool = False

    def step_01_admit_root(self, mark: str = "<>") -> bool:
        """Admits initial opaque root mark <> (change class: create_structure)."""
        self.state.carrier.add(mark)
        self.state.step = 1
        self.state.name = "state_initialized_with_root_reference"
        self.state.branches_retained = ["branch_root_single"]
        self.state.history.append("step_01: initial_datum (create_structure)")
        return True

    def step_02_admit_germ(self, a: str = "a", b: str = "b") -> bool:
        """Admits primitive difference pair (a, b) (change class: create_structure)."""
        if self.state.step < 1:
            return False
        self.state.carrier.update([a, b])
        self.state.relations.add((a, b))
        self.setting = PrimitiveDifferenceSetting(
            carrier=self.state.carrier, relation=self.state.relations, a=a, b=b
        )
        self.state.step = 2
        self.state.name = "state_with_distinguished_difference_pair"
        self.state.history.append("step_02: create_structure")
        return self.setting.is_witnessed()

    def step_03_enforce_irrefl(self) -> bool:
        """Purges reflexive loops to protect carrier irreflexivity (change class: remove_obstruction)."""
        if not self.setting:
            return False
        self.state.relations = {pair for pair in self.state.relations if pair[0] != pair[1]}
        self.setting.relation = self.state.relations
        valid = self.setting.is_distinct()
        self.state.invariants["irreflexive"] = valid
        self.state.step = 3
        self.state.name = "state_irreflexive_carrier_protected"
        self.state.history.append("step_03: remove_obstruction")
        return valid

    def step_04_admit_orientation(self) -> bool:
        """
        Admits directed orientation while enforcing tie-retention.
        Retains both directed causal cut D_2 and symmetric spatial link S_2 branches.
        """
        if self.state.step < 3 or not self.setting or not self.setting.is_distinct():
            return False
        a, b = self.setting.a, self.setting.b
        self.state.branches_retained = ["branch_D2", "branch_S2"]
        self.state.branch_metadata = {
            "branch_D2": {
                "type": "directed_causal_germ",
                "relation": {(a, b)},
                "symmetric": False,
                "automorphism_group": "id",
            },
            "branch_S2": {
                "type": "spatial_link",
                "relation": {(a, b), (b, a)},
                "symmetric": True,
                "automorphism_group": "Z2",
            },
        }
        self.state.invariants["tie_retention_active"] = True
        self.state.step = 4
        self.state.name = "state_oriented_germ_retained"
        self.state.history.append("step_04: admit_orientation_tie_retention (create_structure)")
        return True

    def step_05_admit_transposition(self) -> bool:
        """
        Verifies pre-natal transposition operator sigma(a, b) = (b, a)
        and oriented 1-chain boundary sign inversion partial_1(sigma(e)) = -partial_1(e).
        """
        if self.state.step < 4 or not self.setting:
            return False
        edge = (self.setting.a, self.setting.b)
        sigma_edge = self.setting.transpose(edge)
        if edge == sigma_edge:
            return False
        sign_flip = self.setting.verify_transposition_sign_inversion(edge)
        if not sign_flip:
            return False
        self.state.invariants["transposition_sign_inversion"] = True
        self.state.step = 5
        self.state.name = "state_bounded_queue_isolated"
        self.state.history.append("step_05: transposition_antisymmetry (remove_obstruction)")
        return True

    def step_06_instantiate_causal_alphabet(self, event_names: Optional[List[str]] = None) -> bool:
        """Admits caller-supplied labels (create_structure)."""
        if self.state.step < 5:
            return False
        if event_names is None:
            event_names = ["e0", "e1", "e2", "e3"]
        for ev in event_names:
            self.state.carrier.add(ev)
        self.state.invariants["causal_alphabet"] = list(event_names)
        self.state.step = 6
        self.state.name = "state_cosmology_astrophysics_alphabet_admitted"
        self.state.history.append("step_06: rule_causal_alphabet_instantiation (create_structure)")
        return True

    def step_07_evaluate_boundary_closure(self) -> SimplicialBoundaryReceipt:
        """Evaluates boundary nilpotency B_1 * B_2 = 0 on simplicial 2-complex."""
        vertices = ["e0", "e1", "e2"]
        edges = [("e0", "e1"), ("e1", "e2"), ("e0", "e2")]
        faces = [("e0", "e1", "e2")]
        receipt = self.evaluate_simplicial_boundary_matrices(vertices, edges, faces)
        self.state.invariants["boundary_nilpotence"] = receipt.is_nilpotent
        self.state.step = 7
        self.state.name = "state_cosmology_astrophysics_boundary_enforced"
        self.state.history.append("step_07: rule_boundary_closure (remove_obstruction)")
        return receipt

    def step_08_synthesize_causal_poset(self) -> bool:
        """Synthesizes transitive causal set poset (C, prec)."""
        if self.state.step < 7:
            return False
        events = ["e0", "e1", "e2", "e3"]
        rels = {("e0", "e1"), ("e0", "e2"), ("e1", "e3"), ("e2", "e3")}
        self.causal_set = CausalSet(events, rels)
        self.state.invariants["causal_poset_active"] = True
        self.state.step = 8
        self.state.name = "state_cosmology_astrophysics_transition_poset_active"
        self.state.history.append("step_08: rule_poset_synthesis (create_structure)")
        return True

    def step_09_resolve_parity(self) -> bool:
        """Checks that a witnessed pair differs from its transposition."""
        if self.state.step < 8 or not self.setting:
            return False
        edge = (self.setting.a, self.setting.b)
        sigma = self.setting.transpose(edge)
        parity_distinct = edge != sigma
        self.state.invariants["parity_stabilized"] = parity_distinct
        self.state.step = 9
        self.state.name = "state_cosmology_astrophysics_parity_stabilized"
        self.state.history.append("step_09: rule_parity_resolution (remove_obstruction)")
        return parity_distinct

    def step_10_admit_higher_complexes(self) -> bool:
        """Evaluates a supplied finite simplicial complex."""
        if self.state.step < 9:
            return False
        regge = self.evaluate_regge_spacetime_complex()
        self.state.invariants["regge_spacetime_admitted"] = bool(regge)
        self.state.step = 10
        self.state.name = "state_cosmology_astrophysics_higher_complexes_admitted"
        self.state.history.append("step_10: rule_complex_admission (create_structure)")
        return bool(regge)

    def step_11_enforce_conservation(self):
        """Recompute the finite boundary products before recording nilpotence."""
        if self.state.step < 10:
            return False
        receipt = self.evaluate_regge_spacetime_complex()
        valid = bool(receipt) and receipt.boundary_defect == 0
        self.state.invariants["boundary_nilpotence"] = valid
        if valid:
            self.state.step = 11
            self.state.name = "state_boundary_products_checked"
            self.state.history.append("step_11: checked_boundary_nilpotence")
        return valid

    def step_12_quotient_observer_interface(self) -> bool:
        """Records the scenario observer-interface flag; no projection is computed."""
        if self.state.step < 11:
            return False
        self.state.invariants["horizon_observer_active"] = True
        self.state.step = 12
        self.state.name = "state_cosmology_astrophysics_observer_interface_active"
        self.state.history.append("step_12: rule_quotient_projection (create_structure)")
        return True

    def step_13_prune_fuel_bounded_branches(self) -> bool:
        """Records the scenario pruning flag; no branch-pruning algorithm is executed."""
        if self.state.step < 12:
            return False
        self.state.invariants["branches_pruned"] = True
        self.state.step = 13
        self.state.name = "state_cosmology_astrophysics_fuel_pruned_state"
        self.state.history.append("step_13: rule_fuel_bounded_pruning (remove_obstruction)")
        return True

    def step_14_establish_frontier(self) -> bool:
        """Records the final scenario marker; no physical frontier is established."""
        if self.state.step < 13:
            return False
        self.state.invariants["cosmological_frontier"] = True
        self.state.step = 14
        self.state.name = "state_cosmology_astrophysics_frontier_active"
        self.state.history.append("step_14: establish_frontier (create_structure)")
        return True

    def step_15_isolate_gap_obstruction(self) -> Dict[str, str]:
        """Reports the declared smooth-curvature gap label; no impossibility theorem is proved."""
        self.state.step = 15
        self.state.name = "state_cosmology_astrophysics_gap_isolated"
        self.state.history.append("step_15: isolate_gap_obstruction (remove_obstruction)")
        return self.check_gap_obstruction()

    def step_16_terminal_certification(self) -> Dict[str, Any]:
        """Reports the staged scenario state; this is not a physical certificate."""
        self.state.step = 16
        self.state.name = "state_cosmology_astrophysics_certified"
        self.state.history.append("step_16: terminal_certification")
        return {
            "status": "SCENARIO_RECORDED",
            "domain": "cosmology_astrophysics",
            "reported_step": self.state.step,
            "invariants": self.state.invariants,
            "branches_retained": self.state.branches_retained,
            "authority_effect": "None",
        }

    def evaluate_simplicial_boundary_matrices(
        self, vertices: List[str], edges: List[Tuple[str, str]], faces: List[Tuple[str, str, str]]
    ) -> SimplicialBoundaryReceipt:
        """Evaluates exact integer simplicial boundary matrices B_1 and B_2."""
        if not vertices or not edges or not faces:
            raise ValueError("Vertices, edges, and faces must be non-empty.")

        v_idx = {v: i for i, v in enumerate(vertices)}
        e_idx = {e: j for j, e in enumerate(edges)}

        n0 = len(vertices)
        n1 = len(edges)
        n2 = len(faces)

        # B_1: vertices x edges
        b1 = [[0] * n1 for _ in range(n0)]
        for j, (u, v) in enumerate(edges):
            if u not in v_idx or v not in v_idx:
                raise KeyError("Edge vertex missing from vertices list")
            b1[v_idx[v]][j] += 1
            b1[v_idx[u]][j] -= 1

        # B_2: edges x faces
        b2 = [[0] * n2 for _ in range(n1)]
        for k, (v0, v1, v2) in enumerate(faces):
            boundary_terms = [(1, (v1, v2)), (-1, (v0, v2)), (1, (v0, v1))]
            for sign, (src, dst) in boundary_terms:
                if (src, dst) in e_idx:
                    b2[e_idx[(src, dst)]][k] += sign
                elif (dst, src) in e_idx:
                    b2[e_idx[(dst, src)]][k] -= sign
                else:
                    raise KeyError(f"Face boundary edge ({src}, {dst}) missing from edge list")

        # Integer matrix multiplication B_1 * B_2
        prod = [[0] * n2 for _ in range(n0)]
        is_nilpotent = True
        for i in range(n0):
            for k in range(n2):
                s = sum(b1[i][j] * b2[j][k] for j in range(n1))
                prod[i][k] = s
                if s != 0:
                    is_nilpotent = False

        euler_char = n0 - n1 + n2
        num_cycles = max(0, n1 - n0 + 1)

        return SimplicialBoundaryReceipt(
            vertices=vertices,
            edges=edges,
            faces=faces,
            b1_matrix=b1,
            b2_matrix=b2,
            product_matrix=prod,
            is_nilpotent=is_nilpotent,
            num_cycles=num_cycles,
            euler_characteristic=euler_char,
            authority_effect="None",
        )

    def evaluate_boundary_closure(self) -> SimplicialBoundaryReceipt:
        """Evaluates boundary nilpotency B_1 * B_2 = 0 on standard oriented 2-simplex."""
        vertices = ["a", "b", "c"]
        edges = [("a", "b"), ("b", "c"), ("a", "c")]
        faces = [("a", "b", "c")]
        receipt = self.evaluate_simplicial_boundary_matrices(vertices, edges, faces)
        self.state.invariants["boundary_nilpotence"] = receipt.is_nilpotent
        return receipt

    def evaluate_regge_spacetime_complex(self) -> ReggeSpacetimeReceipt:
        """
        Evaluates a complete 3D Regge tetrahedron simplicial complex with
        4 vertices, 6 edges, 4 faces, 1 tetrahedron.
        Verifies both B_1 * B_2 = 0 and B_2 * B_3 = 0 identically over Z.
        """
        vertices = ["v0", "v1", "v2", "v3"]
        v_idx = {v: i for i, v in enumerate(vertices)}

        edges = [("v0", "v1"), ("v0", "v2"), ("v0", "v3"), ("v1", "v2"), ("v1", "v3"), ("v2", "v3")]
        e_idx = {e: i for i, e in enumerate(edges)}

        faces = [
            ("v1", "v2", "v3"),  # Face opposite v0
            ("v0", "v2", "v3"),  # Face opposite v1
            ("v0", "v1", "v3"),  # Face opposite v2
            ("v0", "v1", "v2"),  # Face opposite v3
        ]
        f_idx = {f: i for i, f in enumerate(faces)}

        tetrahedra = [("v0", "v1", "v2", "v3")]

        n0, n1, n2, n3 = len(vertices), len(edges), len(faces), len(tetrahedra)

        # B_1: vertices x edges
        b1 = [[0] * n1 for _ in range(n0)]
        for j, (u, v) in enumerate(edges):
            b1[v_idx[v]][j] += 1
            b1[v_idx[u]][j] -= 1

        # B_2: edges x faces
        b2 = [[0] * n2 for _ in range(n1)]
        for k, (u0, u1, u2) in enumerate(faces):
            boundary_terms = [(1, (u1, u2)), (-1, (u0, u2)), (1, (u0, u1))]
            for sign, (src, dst) in boundary_terms:
                if (src, dst) in e_idx:
                    b2[e_idx[(src, dst)]][k] += sign
                elif (dst, src) in e_idx:
                    b2[e_idx[(dst, src)]][k] -= sign

        # B_3: faces x tetrahedra
        # partial_3(v0, v1, v2, v3) = +(v1, v2, v3) - (v0, v2, v3) + (v0, v1, v3) - (v0, v1, v2)
        b3 = [[0] * n3 for _ in range(n2)]
        t_terms = [
            (1, ("v1", "v2", "v3")),
            (-1, ("v0", "v2", "v3")),
            (1, ("v0", "v1", "v3")),
            (-1, ("v0", "v1", "v2")),
        ]
        for sign, f in t_terms:
            if f in f_idx:
                b3[f_idx[f]][0] += sign

        # Verify B_1 * B_2 = 0
        prod12 = [[0] * n2 for _ in range(n0)]
        is_nilpotent_12 = True
        for i in range(n0):
            for k in range(n2):
                s = sum(b1[i][j] * b2[j][k] for j in range(n1))
                prod12[i][k] = s
                if s != 0:
                    is_nilpotent_12 = False

        # Verify B_2 * B_3 = 0
        prod23 = [[0] * n3 for _ in range(n1)]
        is_nilpotent_23 = True
        for j in range(n1):
            for l in range(n3):
                s = sum(b2[j][k] * b3[k][l] for k in range(n2))
                prod23[j][l] = s
                if s != 0:
                    is_nilpotent_23 = False

        euler_char = n0 - n1 + n2 - n3  # 4 - 6 + 4 - 1 = 1 (contractible 3-ball)
        boundary_defect = sum(abs(v) for row in prod12 for v in row) + sum(
            abs(v) for row in prod23 for v in row
        )

        return ReggeSpacetimeReceipt(
            num_vertices=n0,
            num_edges=n1,
            num_faces=n2,
            num_tetrahedra=n3,
            b1_matrix=b1,
            b2_matrix=b2,
            b3_matrix=b3,
            is_b1_b2_nilpotent=is_nilpotent_12,
            is_b2_b3_nilpotent=is_nilpotent_23,
            euler_characteristic=euler_char,
            boundary_defect=boundary_defect,
            authority_effect="None",
        )

    def check_gap_obstruction(self) -> Dict[str, str]:
        """Detects the unbridged domain recovery gap: SmoothCurvatureObstruction."""
        self.gap_detected = True
        return {
            "gap_id": "SmoothCurvatureObstruction",
            "status": "UNBRIDGED_OBSTRUCTION",
            "domain": "cosmology_astrophysics",
            "reason": "Finite discrete difference cannot derive continuous parameters without ungrounded admissions.",
        }
