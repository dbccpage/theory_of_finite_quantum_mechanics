"""Finite relation, orientation and boundary-matrix examples.
AuthorityEffect: None. These computations do not derive a physical model.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np


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
        """Transposition operator sigma = (u v) -> (v u)."""
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
        # Check sign inversion on all carrier vertices
        for pt in [u, v]:
            if b_trans.get(pt, 0) != -b_orig.get(pt, 0):
                return False
        return True


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


@dataclass
class DomainState:
    """State of the discrete physics derivation engine."""

    step: int
    name: str
    carrier: Set[str] = field(default_factory=set)
    relations: Set[Tuple[str, str]] = field(default_factory=set)
    invariants: Dict[str, bool] = field(default_factory=dict)
    history: List[str] = field(default_factory=list)
    branches_retained: List[str] = field(default_factory=list)
    branch_metadata: Dict[str, Dict[str, Any]] = field(default_factory=dict)


class DomainEngine:
    """Deterministic transition engine for physics domain."""

    def __init__(self):
        self.state = DomainState(step=0, name="state_empty_void")
        self.setting: Optional[PrimitiveDifferenceSetting] = None
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
        # Strip reflexive pairs
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
        Retains both directed cut D_2 and symmetric link S_2 branches.
        """
        if self.state.step < 3 or not self.setting or not self.setting.is_distinct():
            return False
        a, b = self.setting.a, self.setting.b
        self.state.branches_retained = ["branch_D2", "branch_S2"]
        self.state.branch_metadata = {
            "branch_D2": {
                "type": "directed_germ",
                "relation": {(a, b)},
                "symmetric": False,
                "automorphism_group": "id",
            },
            "branch_S2": {
                "type": "symmetrized_link",
                "relation": {(a, b), (b, a)},
                "symmetric": True,
                "automorphism_group": "Z2",
            },
        }
        self.state.invariants["tie_retention_active"] = True
        self.state.step = 4
        self.state.name = "state_orientation_admitted_with_tie_retention"
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
        self.state.name = "state_transposition_sign_verified"
        self.state.history.append("step_05: transposition_antisymmetry (create_structure)")
        return True

    def evaluate_simplicial_boundary_matrices(
        self, vertices: List[str], edges: List[Tuple[str, str]], faces: List[Tuple[str, str, str]]
    ) -> SimplicialBoundaryReceipt:
        """
        Evaluates exact integer simplicial boundary matrices B_1 and B_2
        and verifies B_1 * B_2 = 0.
        """
        v_idx = {v: i for i, v in enumerate(vertices)}
        e_idx = {e: j for j, e in enumerate(edges)}

        n0 = len(vertices)
        n1 = len(edges)
        n2 = len(faces)

        # B_1: vertices x edges
        b1 = [[0] * n1 for _ in range(n0)]
        for j, (u, v) in enumerate(edges):
            if u not in v_idx:
                raise KeyError(f"Edge vertex '{u}' missing from vertices list")
            if v not in v_idx:
                raise KeyError(f"Edge vertex '{v}' missing from vertices list")
            b1[v_idx[v]][j] += 1
            b1[v_idx[u]][j] -= 1

        # B_2: edges x faces
        b2 = [[0] * n2 for _ in range(n1)]
        for k, (v0, v1, v2) in enumerate(faces):
            # partial_2(v0, v1, v2) = +(v1, v2) - (v0, v2) + (v0, v1)
            boundary_terms = [(1, (v1, v2)), (-1, (v0, v2)), (1, (v0, v1))]
            for sign, (src, dst) in boundary_terms:
                if (src, dst) in e_idx:
                    b2[e_idx[(src, dst)]][k] += sign
                elif (dst, src) in e_idx:
                    b2[e_idx[(dst, src)]][k] -= sign
                else:
                    raise KeyError(f"Face boundary edge ({src}, {dst}) missing from edge list")

        # Exact integer matrix multiplication B_1 * B_2
        b1_np = np.array(b1, dtype=np.int64)
        b2_np = np.array(b2, dtype=np.int64)
        prod_np = np.dot(b1_np, b2_np) if n1 > 0 and n2 > 0 else np.zeros((n0, n2), dtype=np.int64)
        is_nilpotent = bool(np.all(prod_np == 0))

        euler_char = n0 - n1 + n2
        num_cycles = max(0, n1 - n0 + 1)

        return SimplicialBoundaryReceipt(
            vertices=vertices,
            edges=edges,
            faces=faces,
            b1_matrix=b1,
            b2_matrix=b2,
            product_matrix=prod_np.tolist(),
            is_nilpotent=is_nilpotent,
            num_cycles=num_cycles,
            euler_characteristic=euler_char,
            authority_effect="None",
        )

    def evaluate_boundary_closure(self) -> SimplicialBoundaryReceipt:
        """
        Genuine boundary nilpotence evaluation B_1 * B_2 = 0 on standard oriented 2-simplex.
        Replaces legacy boolean stub.
        """
        vertices = ["a", "b", "c"]
        edges = [("a", "b"), ("b", "c"), ("a", "c")]
        faces = [("a", "b", "c")]
        receipt = self.evaluate_simplicial_boundary_matrices(vertices, edges, faces)
        self.state.invariants["boundary_nilpotence"] = receipt.is_nilpotent
        return receipt


    def check_gap_obstruction(self) -> Dict[str, str]:
        """Detects the unbridged domain recovery gap: ContinuumMetricObstruction"""
        self.gap_detected = True
        return {
            "gap_id": "ContinuumMetricObstruction",
            "status": "UNBRIDGED_OBSTRUCTION",
            "domain": "physics",
            "reason": "Finite discrete difference cannot derive continuous parameters without ungrounded admissions.",
        }
