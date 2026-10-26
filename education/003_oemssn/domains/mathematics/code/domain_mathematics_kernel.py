"""
Domain Kernel: Pure Mathematics, Category Theory & Homological Algebra
AuthorityEffect: None
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class PrimitiveDifferenceSetting:
    """Root W Witnessed Irreflexive Difference Germ: (X, R, a, b)."""

    carrier: Set[str]
    relation: Set[Tuple[str, str]]
    a: str
    b: str

    def is_irrefl(self) -> bool:
        return all((x, x) not in self.relation for x in self.carrier)

    def is_witnessed(self) -> bool:
        return (self.a, self.b) in self.relation

    def is_distinct(self) -> bool:
        return self.a != self.b and self.is_witnessed() and self.is_irrefl()


@dataclass(frozen=True)
class Simplex0:
    """0-simplex (vertex)."""

    id: str

    def __post_init__(self):
        if not self.id:
            raise ValueError("Vertex id cannot be empty.")


@dataclass(frozen=True)
class Simplex1:
    """Oriented 1-simplex (edge)."""

    src: str
    dst: str

    def __post_init__(self):
        if self.src == self.dst:
            raise ValueError(
                f"Degenerate 1-simplex rejected: reflexive edge ({self.src}, {self.dst})"
            )

    def reversal(self) -> "Simplex1":
        """Transposition operator sigma exchanging endpoints."""
        return Simplex1(src=self.dst, dst=self.src)

    def boundary(self) -> Dict[str, int]:
        """Evaluates boundary 1-chain: +1*dst - 1*src."""
        return {self.dst: 1, self.src: -1}


@dataclass(frozen=True)
class Simplex2:
    """Oriented 2-simplex (triangle)."""

    v0: str
    v1: str
    v2: str

    def __post_init__(self):
        if len({self.v0, self.v1, self.v2}) < 3:
            raise ValueError(
                f"Degenerate 2-simplex rejected: non-distinct vertices ({self.v0}, {self.v1}, {self.v2})"
            )

    def boundary_edges(self) -> List[Tuple[int, Tuple[str, str]]]:
        """Returns signed boundary edges: [(+1, (v1, v2)), (-1, (v0, v2)), (+1, (v0, v1))]."""
        return [(1, (self.v1, self.v2)), (-1, (self.v0, self.v2)), (1, (self.v0, self.v1))]


class SimplicialComplex:
    """
    Exact integer simplicial complex supporting 0-, 1-, and 2-simplices.
    Evaluates boundary matrices B_1 and B_2 and verifies B_1 B_2 = 0.
    """

    def __init__(self):
        self.vertices: List[str] = []
        self._vertex_indices: Dict[str, int] = {}
        self.edges: List[Tuple[str, str]] = []
        self._edge_indices: Dict[Tuple[str, str], int] = {}
        self.triangles: List[Tuple[str, str, str]] = []

    def add_vertex(self, v: str) -> None:
        if v not in self._vertex_indices:
            self._vertex_indices[v] = len(self.vertices)
            self.vertices.append(v)

    def add_edge(self, src: str, dst: str) -> None:
        if src == dst:
            raise ValueError(f"Self-loop edge ({src}, {dst}) is rejected by irreflexivity.")
        self.add_vertex(src)
        self.add_vertex(dst)
        edge = (src, dst)
        if edge not in self._edge_indices and (dst, src) not in self._edge_indices:
            self._edge_indices[edge] = len(self.edges)
            self.edges.append(edge)

    def add_triangle(self, v0: str, v1: str, v2: str) -> None:
        if len({v0, v1, v2}) < 3:
            raise ValueError(f"Triangle vertices must be pairwise distinct: ({v0}, {v1}, {v2})")
        # Ensure faces exist in oriented edge basis
        self.add_edge(v1, v2)
        self.add_edge(v0, v2)
        self.add_edge(v0, v1)
        triangle = (v0, v1, v2)
        if triangle not in self.triangles:
            self.triangles.append(triangle)

    def boundary_matrix_d1(self) -> List[List[int]]:
        """
        Matrix representation of d_1: C_1 -> C_0.
        Dimensions: len(vertices) x len(edges).
        For edge (src, dst): matrix[dst_idx][edge_idx] = +1, matrix[src_idx][edge_idx] = -1.
        """
        n0 = len(self.vertices)
        n1 = len(self.edges)
        matrix = [[0] * n1 for _ in range(n0)]
        for j, (src, dst) in enumerate(self.edges):
            u_idx = self._vertex_indices[src]
            v_idx = self._vertex_indices[dst]
            matrix[u_idx][j] = -1
            matrix[v_idx][j] = 1
        return matrix

    def boundary_matrix_d2(self) -> List[List[int]]:
        """
        Matrix representation of d_2: C_2 -> C_1.
        Dimensions: len(edges) x len(triangles).
        d_2(v0, v1, v2) = +(v1, v2) - (v0, v2) + (v0, v1).
        """
        n1 = len(self.edges)
        n2 = len(self.triangles)
        matrix = [[0] * n2 for _ in range(n1)]
        for k, (v0, v1, v2) in enumerate(self.triangles):
            for sign, (e_src, e_dst) in [(1, (v1, v2)), (-1, (v0, v2)), (1, (v0, v1))]:
                if (e_src, e_dst) in self._edge_indices:
                    edge_idx = self._edge_indices[(e_src, e_dst)]
                    matrix[edge_idx][k] += sign
                elif (e_dst, e_src) in self._edge_indices:
                    edge_idx = self._edge_indices[(e_dst, e_src)]
                    matrix[edge_idx][k] += -sign
                else:
                    raise KeyError(f"Face edge ({e_src}, {e_dst}) not found in complex edges.")
        return matrix

    def compute_boundary_nilpotency(self) -> Tuple[bool, List[List[int]]]:
        """
        Computes exact matrix product B_1 * B_2.
        Returns: (is_zero_matrix, product_matrix).
        """
        b1 = self.boundary_matrix_d1()
        b2 = self.boundary_matrix_d2()
        n0 = len(self.vertices)
        n1 = len(self.edges)
        n2 = len(self.triangles)

        if n2 == 0 or n1 == 0:
            return True, [[0] * max(n2, 1) for _ in range(n0)]

        product = [[0] * n2 for _ in range(n0)]
        is_zero = True
        for i in range(n0):
            for k in range(n2):
                val = 0
                for j in range(n1):
                    val += b1[i][j] * b2[j][k]
                product[i][k] = val
                if val != 0:
                    is_zero = False
        return is_zero, product

    def euler_characteristic(self) -> int:
        """chi = |V| - |E| + |F|"""
        return len(self.vertices) - len(self.edges) + len(self.triangles)


@dataclass
class DomainState:
    step: int
    name: str
    carrier: Set[str] = field(default_factory=set)
    relations: Set[Tuple[str, str]] = field(default_factory=set)
    invariants: Dict[str, bool] = field(default_factory=dict)
    history: List[str] = field(default_factory=list)


class DomainEngine:
    """Deterministic transition engine for mathematics domain."""

    def __init__(self):
        self.state = DomainState(step=0, name="state_empty_void")
        self.setting: Optional[PrimitiveDifferenceSetting] = None
        self.gap_detected: bool = False
        self.complex = SimplicialComplex()

    def step_01_admit_root(self, mark: str = "<>") -> bool:
        self.state.carrier.add(mark)
        self.complex.add_vertex(mark)
        self.state.step = 1
        self.state.name = "state_initialized_with_root_reference"
        self.state.history.append("step_01: initial_datum")
        return True

    def step_02_admit_germ(self, a: str = "a", b: str = "b") -> bool:
        self.state.carrier.update([a, b])
        self.state.relations.add((a, b))
        self.setting = PrimitiveDifferenceSetting(
            carrier=self.state.carrier, relation=self.state.relations, a=a, b=b
        )
        self.complex.add_edge(a, b)
        self.state.step = 2
        self.state.name = "state_with_distinguished_difference_pair"
        self.state.history.append("step_02: create_structure")
        return self.setting.is_witnessed()

    def step_03_enforce_irrefl(self) -> bool:
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

    def admit_triangle(self, v0: str, v1: str, v2: str) -> bool:
        """Admit an oriented 2-simplex into the mathematical simplicial complex."""
        self.complex.add_triangle(v0, v1, v2)
        return True

    def evaluate_boundary_closure(self, custom_complex: Optional[SimplicialComplex] = None) -> bool:
        """
        Verifies boundary nilpotency d_1 d_2 = 0 via exact integer matrix multiplication.
        If no triangles exist in the current complex, synthesizes a canonical
        2-simplex closure over the active difference germ with witness point to verify nilpotency.
        """
        comp = custom_complex or self.complex
        if len(comp.triangles) == 0:
            comp = SimplicialComplex()
            a = self.setting.a if self.setting else "pt_a"
            b = self.setting.b if self.setting else "pt_b"
            c = "pt_c_witness"
            comp.add_triangle(a, b, c)

        is_nilpotent, _ = comp.compute_boundary_nilpotency()
        self.state.invariants["boundary_nilpotence"] = is_nilpotent
        return is_nilpotent

    def check_gap_obstruction(self) -> Dict[str, str]:
        """Reports the declared scenario scope limit UncountableContinuumObstruction; no impossibility is calculated."""
        self.gap_detected = True
        return {
            "gap_id": "UncountableContinuumObstruction",
            "status": "UNBRIDGED_OBSTRUCTION",
            "domain": "mathematics",
            "reason": "Finite discrete difference cannot derive continuous parameters without ungrounded admissions.",
        }
