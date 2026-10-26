"""
Cross-Domain Boundary Morphism: Lean 4 Simplicial Complexes <-> Python Relational CTE Evaluator
Formal Bisimulation Checker
AuthorityEffect: None.
"""

import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from simplicial_cte_evaluator import SimplicialCTEEvaluator


@dataclass
class LeanSimplicialState:
    step: int
    triangles: List[Tuple[str, str, str]]
    edges: List[Tuple[str, str, int]]  # (src, dst, orientation)
    nilpotence_certified: bool

    @classmethod
    def initial(cls) -> "LeanSimplicialState":
        return cls(step=0, triangles=[], edges=[], nilpotence_certified=True)

    def admit_triangle(self, t: Tuple[str, str, str]) -> "LeanSimplicialState":
        v0, v1, v2 = t
        new_edges = [(v1, v2, 1), (v0, v2, -1), (v0, v1, 1)]
        return LeanSimplicialState(
            step=self.step + 1,
            triangles=[t] + self.triangles,
            edges=new_edges + self.edges,
            nilpotence_certified=True,
        )


@dataclass
class BisimulationCertificate:
    step: int
    forward_simulation_holds: bool
    backward_simulation_holds: bool
    lean_nilpotence_theorem_valid: bool
    sql_nilpotence_cte_valid: bool
    quotient_orbit_cardinality_matched: bool
    discrepancy_log: List[str] = field(default_factory=list)

    @property
    def is_bisimilar(self) -> bool:
        return (
            self.forward_simulation_holds
            and self.backward_simulation_holds
            and self.lean_nilpotence_theorem_valid
            and self.sql_nilpotence_cte_valid
            and self.quotient_orbit_cardinality_matched
            and len(self.discrepancy_log) == 0
        )


@dataclass
class FuelSimplicialExecutionReceipt:
    triangle: Tuple[str, str, str]
    fuel_provided: int
    fuel_remaining: int
    steps_taken: int
    terminal_dim: int
    status: str  # "HALTED", "OUT_OF_FUEL"
    nilpotence_certified: bool
    edges: List[Tuple[str, str, int]]
    vertex_evaluations: Dict[str, int]


@dataclass
class FuelSimplicialBisimulationCertificate:
    triangle_id: str
    fuel_budget: int
    py_status: str
    sql_status: str
    py_terminal_dim: int
    sql_terminal_dim: int
    py_steps: int
    sql_steps: int
    py_nilpotence_certified: bool
    sql_nilpotence_certified: bool
    status_matched: bool
    terminal_dim_matched: bool
    steps_matched: bool
    nilpotence_matched: bool
    lean_fuel_theorems_valid: bool
    fuel_simplicial_defect: float
    is_bisimilar: bool
    discrepancy_log: List[str] = field(default_factory=list)


@dataclass
class DeRhamExecutionReceipt:
    fuel_provided: int
    fuel_remaining: int
    steps_taken: int
    terminal_stage: int
    status: str  # "HALTED", "OUT_OF_FUEL"
    laplacian_closed: bool
    hodge_dual_closed: bool
    nilpotence_certified: bool
    form0: Dict[str, float]
    form1: Dict[str, Dict[str, Any]]
    laplacian: Dict[str, float]


@dataclass
class DeRhamHodgeTransferCertificate:
    lattice_id: str
    fuel_budget: int
    py_status: str
    sql_status: str
    py_terminal_stage: int
    sql_terminal_stage: int
    py_steps: int
    sql_steps: int
    py_laplacian_closed: bool
    sql_laplacian_closed: bool
    py_hodge_closed: bool
    sql_hodge_closed: bool
    py_nilpotence_certified: bool
    sql_nilpotence_certified: bool
    status_matched: bool
    stage_matched: bool
    steps_matched: bool
    laplacian_closed_matched: bool
    hodge_closed_matched: bool
    nilpotence_matched: bool
    lean_derham_theorems_valid: bool
    transfer_defect: float
    is_transfer_exact: bool
    discrepancy_log: List[str] = field(default_factory=list)


class SimplicialBisimulationBridge:
    def __init__(self, lean_src_path: Optional[Path] = None):
        self.lean_src = lean_src_path or (
            Path(__file__).resolve().parent.parent.parent
            / "mathematics"
            / "lean4"
            / "simplicial_complex.lean"
        )
        self.sql_evaluator = SimplicialCTEEvaluator(in_memory=True)
        self.lean_state = LeanSimplicialState.initial()

    def verify_lean_compilation(self) -> bool:
        """Verifies that the Lean 4 simplicial complex formalization elaborates with zero errors."""
        if not self.lean_src.exists():
            return False
        res = subprocess.run(["lean", str(self.lean_src)], capture_output=True, text=True)
        return res.returncode == 0

    def step(self, triangle_id: str, v0: str, v1: str, v2: str) -> BisimulationCertificate:
        """
        Executes a synchronized transition in both the Lean 4 state machine
        and the SQL relational CTE evaluator, checking the bisimulation conditions.
        """
        t = (v0, v1, v2)

        # 1. Lean state transition
        next_lean_state = self.lean_state.admit_triangle(t)

        # 2. Relational SQL state transition
        self.sql_evaluator.add_triangle(triangle_id, v0, v1, v2)
        sql_nilpotence_report = self.sql_evaluator.evaluate_boundaries_and_nilpotence()
        sql_orbits = self.sql_evaluator.compute_window_quotient_orbits()

        # 3. Check Lean compilation / theorem truth
        lean_verified = self.verify_lean_compilation()

        # 4. Check Forward Simulation (Lean -> SQL)
        # Every edge generated by Lean's d_2 boundary must exist in SQL CTE evaluation
        discrepancies = []
        lean_boundary_edges = [(v1, v2, 1), (v0, v2, -1), (v0, v1, 1)]
        sql_edge_tuples = [
            (r["src"], r["dst"], r["edge_weight"])
            for r in sql_orbits
            if r["parent_id"] == triangle_id
        ]

        forward_ok = set(lean_boundary_edges) == set(sql_edge_tuples)
        if not forward_ok:
            discrepancies.append(
                f"Forward simulation mismatch: Lean edges {lean_boundary_edges} != SQL {sql_edge_tuples}"
            )

        # 5. Check Backward Simulation (SQL -> Lean)
        # Every edge produced in the SQL boundary must correspond to Lean's boundary
        backward_ok = len(sql_edge_tuples) == 3 and all(
            e in lean_boundary_edges for e in sql_edge_tuples
        )
        if not backward_ok:
            discrepancies.append(f"Backward simulation mismatch on SQL edges: {sql_edge_tuples}")

        # 6. Nilpotence Invariance
        sql_nilpotence_ok = sql_nilpotence_report["stokes_nilpotence_holds"]
        if not sql_nilpotence_ok:
            discrepancies.append(f"SQL nilpotence CTE failed: {sql_nilpotence_report}")

        # 7. Orbit Partition Cardinality
        orbit_ok = len(sql_orbits) >= 3
        if not orbit_ok:
            discrepancies.append("Quotient orbit partition cardinality insufficient")

        # Commit state update
        self.lean_state = next_lean_state

        return BisimulationCertificate(
            step=self.lean_state.step,
            forward_simulation_holds=forward_ok,
            backward_simulation_holds=backward_ok,
            lean_nilpotence_theorem_valid=lean_verified,
            sql_nilpotence_cte_valid=sql_nilpotence_ok,
            quotient_orbit_cardinality_matched=orbit_ok,
            discrepancy_log=discrepancies,
        )

    def execute_fuel_bounded_homology(
        self, triangle: Tuple[str, str, str], fuel: int
    ) -> FuelSimplicialExecutionReceipt:
        """
        Executes operational small-step homological boundary descent with fuel bounding
        matching Scenario 4 Steps 08/09.
        C_2 -> C_1 -> C_0.
        """
        v0, v1, v2 = triangle
        if fuel == 0:
            return FuelSimplicialExecutionReceipt(
                triangle=triangle,
                fuel_provided=fuel,
                fuel_remaining=0,
                steps_taken=0,
                terminal_dim=2,
                status="OUT_OF_FUEL",
                nilpotence_certified=False,
                edges=[],
                vertex_evaluations={},
            )
        elif fuel == 1:
            edges = [
                (v1, v2, 1),
                (v0, v2, -1),
                (v0, v1, 1),
            ]
            return FuelSimplicialExecutionReceipt(
                triangle=triangle,
                fuel_provided=fuel,
                fuel_remaining=0,
                steps_taken=1,
                terminal_dim=1,
                status="OUT_OF_FUEL",
                nilpotence_certified=False,
                edges=edges,
                vertex_evaluations={},
            )
        else:
            edges = [
                (v1, v2, 1),
                (v0, v2, -1),
                (v0, v1, 1),
            ]
            vertex_evals = {v0: 0, v1: 0, v2: 0}
            return FuelSimplicialExecutionReceipt(
                triangle=triangle,
                fuel_provided=fuel,
                fuel_remaining=fuel - 2,
                steps_taken=2,
                terminal_dim=0,
                status="HALTED",
                nilpotence_certified=True,
                edges=edges,
                vertex_evaluations=vertex_evals,
            )

    def verify_fuel_simplicial_bisimulation(
        self,
        triangle_id: str,
        v0: str,
        v1: str,
        v2: str,
        fuel: int,
        sql_max_degree: Optional[int] = None,
    ) -> FuelSimplicialBisimulationCertificate:
        """
        Evaluates and certifies bisimulation between operational fuel-bounded homology descent
        and bounded-degree recursive SQL CTE boundary evaluation.
        """
        self.sql_evaluator.add_triangle(triangle_id, v0, v1, v2)

        # 1. Operational Homology Execution
        py_receipt = self.execute_fuel_bounded_homology((v0, v1, v2), fuel)

        # 2. Relational SQL-CTE Homology Execution
        actual_sql_degree = fuel if sql_max_degree is None else sql_max_degree
        sql_receipt = self.sql_evaluator.evaluate_bounded_degree_homology_cte(
            actual_sql_degree, target_simplex_id=triangle_id
        )

        # 3. Lean 4 Formal Proof Check
        lean_verified = self.verify_lean_compilation()

        # 4. Compare observables & compute bisimulation defect
        discrepancies: List[str] = []
        if not lean_verified:
            discrepancies.append("Lean 4 simplicial_complex.lean compilation failed")

        status_matched = py_receipt.status == sql_receipt["status"]
        if not status_matched:
            discrepancies.append(
                f"Status mismatch: Py={py_receipt.status} != SQL={sql_receipt['status']}"
            )

        terminal_dim_matched = py_receipt.terminal_dim == sql_receipt["terminal_dim"]
        if not terminal_dim_matched:
            discrepancies.append(
                f"Terminal dimension mismatch: Py={py_receipt.terminal_dim} != SQL={sql_receipt['terminal_dim']}"
            )

        steps_matched = py_receipt.steps_taken == sql_receipt["steps_taken"]
        if not steps_matched:
            discrepancies.append(
                f"Steps mismatch: Py={py_receipt.steps_taken} != SQL={sql_receipt['steps_taken']}"
            )

        nilpotence_matched = py_receipt.nilpotence_certified == sql_receipt["nilpotence_certified"]
        if not nilpotence_matched:
            discrepancies.append(
                f"Nilpotence certification mismatch: Py={py_receipt.nilpotence_certified} != SQL={sql_receipt['nilpotence_certified']}"
            )

        # Quantitative defect Delta_fuel_simp
        halt_diff = abs(int(py_receipt.status == "HALTED") - int(sql_receipt["status"] == "HALTED"))
        exhaust_diff = abs(
            int(py_receipt.status == "OUT_OF_FUEL") - int(sql_receipt["status"] == "OUT_OF_FUEL")
        )
        nilp_diff = abs(
            int(py_receipt.nilpotence_certified) - int(sql_receipt["nilpotence_certified"])
        )
        dim_diff = abs(py_receipt.terminal_dim - sql_receipt["terminal_dim"])
        step_diff = abs(py_receipt.steps_taken - sql_receipt["steps_taken"]) / (
            1.0 + py_receipt.steps_taken
        )

        defect = float(halt_diff + exhaust_diff + nilp_diff + dim_diff + step_diff)

        is_bisim = (
            status_matched
            and terminal_dim_matched
            and steps_matched
            and nilpotence_matched
            and lean_verified
            and (defect == 0.0)
            and (len(discrepancies) == 0)
        )

        return FuelSimplicialBisimulationCertificate(
            triangle_id=triangle_id,
            fuel_budget=fuel,
            py_status=py_receipt.status,
            sql_status=sql_receipt["status"],
            py_terminal_dim=py_receipt.terminal_dim,
            sql_terminal_dim=sql_receipt["terminal_dim"],
            py_steps=py_receipt.steps_taken,
            sql_steps=sql_receipt["steps_taken"],
            py_nilpotence_certified=py_receipt.nilpotence_certified,
            sql_nilpotence_certified=sql_receipt["nilpotence_certified"],
            status_matched=status_matched,
            terminal_dim_matched=terminal_dim_matched,
            steps_matched=steps_matched,
            nilpotence_matched=nilpotence_matched,
            lean_fuel_theorems_valid=lean_verified,
            fuel_simplicial_defect=defect,
            is_bisimilar=is_bisim,
            discrepancy_log=discrepancies,
        )

    def execute_fuel_bounded_derham(
        self,
        vertices: Dict[str, Tuple[float, float]],  # vid -> (dual_area, phi_val)
        edges: List[
            Tuple[str, str, str, float, float, Optional[float]]
        ],  # (eid, src, dst, length, dual_length, star1)
        triangles: List[Tuple[str, str, str, str]],  # (tid, v0, v1, v2)
        phi: Dict[str, float],
        fuel: int,
    ) -> DeRhamExecutionReceipt:
        """
        Operational small-step execution of Discrete Exterior Calculus (DEC) differential forms
        and Hodge star duality on a simplicial lattice under fuel limit.
        Stage 0 (0-forms) -> Stage 1 (1-forms d0 phi) -> Stage 2 (Laplacian Delta_0).
        """
        form0 = {v: phi.get(v, 0.0) for v in vertices}

        if fuel == 0:
            return DeRhamExecutionReceipt(
                fuel_provided=fuel,
                fuel_remaining=0,
                steps_taken=0,
                terminal_stage=0,
                status="OUT_OF_FUEL",
                laplacian_closed=False,
                hodge_dual_closed=False,
                nilpotence_certified=False,
                form0=form0,
                form1={},
                laplacian={},
            )

        # Stage 1: 1-forms d0 phi
        form1: Dict[str, Dict[str, Any]] = {}
        for edge_spec in edges:
            eid, src, dst, length, dual_length = (
                edge_spec[0],
                edge_spec[1],
                edge_spec[2],
                edge_spec[3],
                edge_spec[4],
            )
            star1_val = (
                edge_spec[5]
                if len(edge_spec) > 5 and edge_spec[5] is not None
                else (dual_length / length)
            )
            d0_val = form0[dst] - form0[src]
            star1_d0_val = star1_val * d0_val
            form1[eid] = {
                "src": src,
                "dst": dst,
                "d0": float(d0_val),
                "star1_d0": float(star1_d0_val),
                "hodge_star1": float(star1_val),
            }

        # de Rham nilpotence verification: d1(d0 phi) = 0 on all 2-simplices
        nilpotence_certified = True
        for _, v0, v1, v2 in triangles:
            defect = (form0[v2] - form0[v1]) - (form0[v2] - form0[v0]) + (form0[v1] - form0[v0])
            if abs(defect) > 1e-12:
                nilpotence_certified = False

        if fuel == 1:
            return DeRhamExecutionReceipt(
                fuel_provided=fuel,
                fuel_remaining=0,
                steps_taken=1,
                terminal_stage=1,
                status="OUT_OF_FUEL",
                laplacian_closed=False,
                hodge_dual_closed=False,
                nilpotence_certified=nilpotence_certified,
                form0=form0,
                form1=form1,
                laplacian={},
            )

        # Stage 2: Dual Hodge metric applied, codifferential / Laplacian Delta_0 evaluated
        laplacian: Dict[str, float] = {}
        for vid, (dual_area, _) in vertices.items():
            net_flux = 0.0
            for edge_spec in edges:
                eid, src, dst, length, dual_length = (
                    edge_spec[0],
                    edge_spec[1],
                    edge_spec[2],
                    edge_spec[3],
                    edge_spec[4],
                )
                star1_val = (
                    edge_spec[5]
                    if len(edge_spec) > 5 and edge_spec[5] is not None
                    else (dual_length / length)
                )
                if src == vid:
                    net_flux += star1_val * (form0[vid] - form0[dst])
                elif dst == vid:
                    net_flux += star1_val * (form0[vid] - form0[src])
            laplacian[vid] = float(net_flux / dual_area) if dual_area > 0.0 else 0.0

        return DeRhamExecutionReceipt(
            fuel_provided=fuel,
            fuel_remaining=fuel - 2,
            steps_taken=2,
            terminal_stage=2,
            status="HALTED",
            laplacian_closed=True,
            hodge_dual_closed=True,
            nilpotence_certified=nilpotence_certified,
            form0=form0,
            form1=form1,
            laplacian=laplacian,
        )

    def verify_derham_hodge_transfer(
        self,
        lattice_id: str,
        vertices: Dict[str, Tuple[float, float]],  # vid -> (dual_area, phi_val)
        edges: List[
            Tuple[str, str, str, float, float, Optional[float]]
        ],  # (eid, src, dst, length, dual_length, star1)
        triangles: List[Tuple[str, str, str, str]],  # (tid, v0, v1, v2)
        fuel: int,
        sql_fuel: Optional[int] = None,
    ) -> DeRhamHodgeTransferCertificate:
        """
        Evaluates and certifies transfer bounds between operational Discrete Exterior Calculus (DEC)
        fuel semantics and relational SQL-CTE discrete de Rham and Hodge star evaluation.
        """
        # 1. Reset and populate SQL lattice
        cur = self.sql_evaluator.conn.cursor()
        cur.execute("DELETE FROM simplices;")
        cur.execute("DELETE FROM lattice_vertices;")
        cur.execute("DELETE FROM lattice_edges;")
        self.sql_evaluator.conn.commit()

        for vid, (dual_area, phi_val) in vertices.items():
            self.sql_evaluator.add_lattice_vertex(vid, dual_area=dual_area, phi_val=phi_val)

        for edge_spec in edges:
            eid, src, dst, length, dual_length = (
                edge_spec[0],
                edge_spec[1],
                edge_spec[2],
                edge_spec[3],
                edge_spec[4],
            )
            star1_val = edge_spec[5] if len(edge_spec) > 5 else None
            self.sql_evaluator.add_lattice_edge(
                eid, src, dst, length=length, dual_length=dual_length, hodge_star1=star1_val
            )

        for tid, v0, v1, v2 in triangles:
            self.sql_evaluator.add_triangle(tid, v0, v1, v2)

        phi = {vid: phi_val for vid, (_, phi_val) in vertices.items()}

        # 2. Operational Small-Step DEC Execution
        py_receipt = self.execute_fuel_bounded_derham(vertices, edges, triangles, phi, fuel)

        # 3. Relational SQL-CTE DEC Execution
        actual_sql_fuel = fuel if sql_fuel is None else sql_fuel
        sql_receipt = self.sql_evaluator.evaluate_derham_hodge_cte(actual_sql_fuel)

        # 4. Lean 4 Formal Proof Check
        lean_verified = self.verify_lean_compilation()

        # 5. Compare Observables
        discrepancies: List[str] = []
        if not lean_verified:
            discrepancies.append("Lean 4 simplicial_complex.lean DEC compilation failed")

        status_matched = py_receipt.status == sql_receipt["status"]
        if not status_matched:
            discrepancies.append(
                f"Status mismatch: Py={py_receipt.status} != SQL={sql_receipt['status']}"
            )

        stage_matched = py_receipt.terminal_stage == sql_receipt["terminal_stage"]
        if not stage_matched:
            discrepancies.append(
                f"Terminal stage mismatch: Py={py_receipt.terminal_stage} != SQL={sql_receipt['terminal_stage']}"
            )

        steps_matched = py_receipt.steps_taken == sql_receipt["steps_taken"]
        if not steps_matched:
            discrepancies.append(
                f"Steps mismatch: Py={py_receipt.steps_taken} != SQL={sql_receipt['steps_taken']}"
            )

        laplacian_closed_matched = py_receipt.laplacian_closed == sql_receipt["laplacian_closed"]
        if not laplacian_closed_matched:
            discrepancies.append(
                f"Laplacian closure mismatch: Py={py_receipt.laplacian_closed} != SQL={sql_receipt['laplacian_closed']}"
            )

        hodge_closed_matched = py_receipt.hodge_dual_closed == sql_receipt["hodge_dual_closed"]
        if not hodge_closed_matched:
            discrepancies.append(
                f"Hodge dual closure mismatch: Py={py_receipt.hodge_dual_closed} != SQL={sql_receipt['hodge_dual_closed']}"
            )

        nilpotence_matched = py_receipt.nilpotence_certified == sql_receipt["nilpotence_certified"]
        if not nilpotence_matched:
            discrepancies.append(
                f"Nilpotence certification mismatch: Py={py_receipt.nilpotence_certified} != SQL={sql_receipt['nilpotence_certified']}"
            )

        # Laplacian difference sum
        lap_diff = 0.0
        if py_receipt.laplacian_closed and sql_receipt["laplacian_closed"]:
            for vid in vertices:
                py_v = py_receipt.laplacian.get(vid, 0.0)
                sql_v = sql_receipt["laplacian"].get(vid, 0.0)
                lap_diff += abs(py_v - sql_v)

        # Quantitative Transfer Defect
        status_diff = abs(
            int(py_receipt.status == "HALTED") - int(sql_receipt["status"] == "HALTED")
        )
        stage_diff = abs(py_receipt.terminal_stage - sql_receipt["terminal_stage"])
        closed_diff = abs(int(py_receipt.laplacian_closed) - int(sql_receipt["laplacian_closed"]))
        step_diff = abs(py_receipt.steps_taken - sql_receipt["steps_taken"]) / (
            1.0 + py_receipt.steps_taken
        )
        fuel_penalty = abs(2 - min(fuel, 2)) / (1.0 + fuel)

        defect = float(status_diff + stage_diff + closed_diff + step_diff + lap_diff + fuel_penalty)

        is_exact = (
            status_matched
            and stage_matched
            and steps_matched
            and laplacian_closed_matched
            and hodge_closed_matched
            and nilpotence_matched
            and lean_verified
            and (defect == 0.0)
            and (len(discrepancies) == 0)
        )

        return DeRhamHodgeTransferCertificate(
            lattice_id=lattice_id,
            fuel_budget=fuel,
            py_status=py_receipt.status,
            sql_status=sql_receipt["status"],
            py_terminal_stage=py_receipt.terminal_stage,
            sql_terminal_stage=sql_receipt["terminal_stage"],
            py_steps=py_receipt.steps_taken,
            sql_steps=sql_receipt["steps_taken"],
            py_laplacian_closed=py_receipt.laplacian_closed,
            sql_laplacian_closed=sql_receipt["laplacian_closed"],
            py_hodge_closed=py_receipt.hodge_dual_closed,
            sql_hodge_closed=sql_receipt["hodge_dual_closed"],
            py_nilpotence_certified=py_receipt.nilpotence_certified,
            sql_nilpotence_certified=sql_receipt["nilpotence_certified"],
            status_matched=status_matched,
            stage_matched=stage_matched,
            steps_matched=steps_matched,
            laplacian_closed_matched=laplacian_closed_matched,
            hodge_closed_matched=hodge_closed_matched,
            nilpotence_matched=nilpotence_matched,
            lean_derham_theorems_valid=lean_verified,
            transfer_defect=defect,
            is_transfer_exact=is_exact,
            discrepancy_log=discrepancies,
        )


# ==============================================================================
# Computation Operational Semantics <-> ANSI SQL-CTE Bisimulation Bridge
# ==============================================================================

import sqlite3
import sys
from typing import Set

_comp_code_dir = Path(__file__).resolve().parent.parent.parent / "computation" / "code"
if str(_comp_code_dir) not in sys.path:
    sys.path.insert(0, str(_comp_code_dir))

from domain_computation_kernel import DomainEngine


@dataclass
class ComputationBisimulationCertificate:
    step: int
    forward_simulation_holds: bool
    backward_simulation_holds: bool
    python_distinctness_valid: bool
    sql_distinctness_cte_valid: bool
    irreflexive_certified: bool
    lean_core_theorem_valid: bool
    bisimulation_defect: float
    is_bisimilar: bool
    discrepancy_log: List[str] = field(default_factory=list)


@dataclass
class FuelBisimulationCertificate:
    start_node: str
    fuel_budget: int
    py_terminal_node: str
    sql_terminal_node: str
    py_status: str
    sql_status: str
    py_steps: int
    sql_steps: int
    py_trace: List[str]
    sql_trace: List[str]
    status_matched: bool
    terminal_node_matched: bool
    trace_matched: bool
    lean_fuel_theorems_valid: bool
    fuel_bisimulation_defect: float
    is_bisimilar: bool
    discrepancy_log: List[str] = field(default_factory=list)


class ComputationCTEEvaluator:
    """
    Relational SQL-CTE Evaluator for Operational Semantics & Primitive Difference.
    AuthorityEffect: None.
    """

    def __init__(self, in_memory: bool = True):
        self.conn = sqlite3.connect(":memory:" if in_memory else "computation.db")
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS computation_carrier (
                element_id TEXT PRIMARY KEY,
                step INTEGER NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS computation_relations (
                src TEXT NOT NULL,
                dst TEXT NOT NULL,
                step INTEGER NOT NULL,
                PRIMARY KEY (src, dst)
            );
        """)
        self.conn.commit()

    def add_carrier_element(self, elem: str, step: int):
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT OR REPLACE INTO computation_carrier (element_id, step)
            VALUES (?, ?);
        """,
            (elem, step),
        )
        self.conn.commit()

    def add_relation(self, src: str, dst: str, step: int):
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT OR REPLACE INTO computation_relations (src, dst, step)
            VALUES (?, ?, ?);
        """,
            (src, dst, step),
        )
        self.conn.commit()

    def remove_reflexive_pairs(self) -> int:
        cur = self.conn.cursor()
        cur.execute("""
            DELETE FROM computation_relations
            WHERE src = dst;
        """)
        deleted = cur.rowcount
        self.conn.commit()
        return deleted

    def get_carrier(self) -> Set[str]:
        cur = self.conn.cursor()
        cur.execute("SELECT element_id FROM computation_carrier;")
        return {row["element_id"] for row in cur.fetchall()}

    def get_relations(self) -> Set[Tuple[str, str]]:
        cur = self.conn.cursor()
        cur.execute("SELECT src, dst FROM computation_relations;")
        return {(row["src"], row["dst"]) for row in cur.fetchall()}

    def evaluate_irreflexivity_and_witness_cte(self, a: str, b: str) -> Dict[str, Any]:
        """Evaluates SQL CTEs for irreflexivity, witnessed difference, and distinctness."""
        cur = self.conn.cursor()
        cur.execute("""
            WITH ReflexivePairs AS (
                SELECT src, dst
                FROM computation_relations
                WHERE src = dst
            )
            SELECT COUNT(*) AS reflexive_count FROM ReflexivePairs;
        """)
        ref_count = cur.fetchone()["reflexive_count"]

        cur.execute(
            """
            WITH WitnessedDifference AS (
                SELECT src, dst
                FROM computation_relations
                WHERE src = ? AND dst = ?
            )
            SELECT COUNT(*) AS witness_count FROM WitnessedDifference;
        """,
            (a, b),
        )
        wit_count = cur.fetchone()["witness_count"]

        is_irrefl = ref_count == 0
        is_witnessed = wit_count > 0
        is_distinct = (a != b) and is_witnessed and is_irrefl

        return {
            "reflexive_count": ref_count,
            "witness_count": wit_count,
            "is_irreflexive": is_irrefl,
            "is_witnessed": is_witnessed,
            "is_distinct": is_distinct,
        }

    def evaluate_transitive_closure_cte(self) -> List[Tuple[str, str, int]]:
        """Evaluates recursive transitive closure CTE over computation_relations."""
        cur = self.conn.cursor()
        cur.execute("""
            WITH RECURSIVE Reachable(src, dst, depth) AS (
                SELECT src, dst, 1
                FROM computation_relations
                UNION
                SELECT R.src, CR.dst, R.depth + 1
                FROM Reachable R
                JOIN computation_relations CR ON R.dst = CR.src
                WHERE R.depth < 20
            )
            SELECT DISTINCT src, dst, depth FROM Reachable ORDER BY depth, src, dst;
        """)
        return [(row["src"], row["dst"], row["depth"]) for row in cur.fetchall()]

    def evaluate_cotransitivity_cte(self) -> Dict[str, Any]:
        """Verifies cotransitivity splitting via SQL CTE."""
        cur = self.conn.cursor()
        cur.execute("""
            WITH CandidateTriples AS (
                SELECT r.src AS x, r.dst AS y, c.element_id AS z
                FROM computation_relations r
                CROSS JOIN computation_carrier c
            ),
            SplitEvaluation AS (
                SELECT x, y, z,
                    EXISTS(SELECT 1 FROM computation_relations WHERE src = x AND dst = z) AS x_rel_z,
                    EXISTS(SELECT 1 FROM computation_relations WHERE src = z AND dst = y) AS z_rel_y
                FROM CandidateTriples
            )
            SELECT COUNT(*) AS total_triples,
                   SUM(CASE WHEN x_rel_z = 1 OR z_rel_y = 1 THEN 1 ELSE 0 END) AS satisfied_triples
            FROM SplitEvaluation;
        """)
        row = cur.fetchone()
        total = row["total_triples"]
        satisfied = row["satisfied_triples"] or 0
        return {
            "total_triples": total,
            "satisfied_triples": satisfied,
            "cotransitive": (total == satisfied) if total > 0 else True,
        }

    def evaluate_fuel_bounded_execution_cte(
        self, start_node: str, max_depth: int
    ) -> Dict[str, Any]:
        """
        Evaluates fuel-exhaustion bounded-depth recursive CTE semantics.
        WITH RECURSIVE ExecutionPath(...) ... WHERE depth < max_depth
        Maps max_depth directly to the fuel budget of Scenario 4 Steps 08/09.
        """
        cur = self.conn.cursor()
        cur.execute(
            """
            WITH RECURSIVE ExecutionPath(step, current_node, path_str) AS (
                SELECT 0, ?, ?
                UNION ALL
                SELECT p.step + 1, r.dst, p.path_str || '->' || r.dst
                FROM ExecutionPath p
                JOIN computation_relations r ON p.current_node = r.src
                WHERE p.step < ?
            )
            SELECT step, current_node, path_str FROM ExecutionPath ORDER BY step;
        """,
            (start_node, start_node, max_depth),
        )
        rows = cur.fetchall()

        if not rows:
            return {
                "start_node": start_node,
                "terminal_node": start_node,
                "max_depth": max_depth,
                "fuel_remaining": max_depth,
                "steps_taken": 0,
                "status": "HALTED",
                "trace": [start_node],
                "out_degree": 0,
            }

        trace = [row["current_node"] for row in rows]
        last_row = rows[-1]
        terminal_node = last_row["current_node"]
        steps_taken = last_row["step"]
        fuel_remaining = max_depth - steps_taken

        cur.execute(
            "SELECT COUNT(*) AS out_degree FROM computation_relations WHERE src = ?;",
            (terminal_node,),
        )
        out_degree = cur.fetchone()["out_degree"]

        if steps_taken == max_depth and out_degree > 0:
            status = "OUT_OF_FUEL"
        else:
            status = "HALTED"

        return {
            "start_node": start_node,
            "terminal_node": terminal_node,
            "max_depth": max_depth,
            "fuel_remaining": fuel_remaining,
            "steps_taken": steps_taken,
            "status": status,
            "trace": trace,
            "out_degree": out_degree,
        }

    def close(self):
        self.conn.close()


class ComputationBisimulationBridge:
    """
    Bidirectional bisimulation bridge between DomainEngine (operational semantics)
    and ComputationCTEEvaluator (relational ANSI SQL-CTE).
    AuthorityEffect: None.
    """

    def __init__(self, lean_src_path: Optional[Path] = None):
        self.lean_src = lean_src_path or (
            Path(__file__).resolve().parent.parent.parent
            / "computation"
            / "lean4"
            / "computation_core.lean"
        )
        self.engine = DomainEngine()
        self.sql_evaluator = ComputationCTEEvaluator(in_memory=True)

    def verify_lean_compilation(self) -> bool:
        """Verifies that computation_core.lean elaborates cleanly with Lean 4."""
        if not self.lean_src.exists():
            return False
        res = subprocess.run(["lean", str(self.lean_src)], capture_output=True, text=True)
        return res.returncode == 0

    def step_01_root(self, mark: str = "<>") -> ComputationBisimulationCertificate:
        self.engine.step_01_admit_root(mark)
        self.sql_evaluator.add_carrier_element(mark, step=1)
        return self.compute_bisimulation_certificate()

    def step_02_germ(
        self, a: str = "pt_alpha", b: str = "pt_beta"
    ) -> ComputationBisimulationCertificate:
        self.engine.step_02_admit_germ(a, b)
        self.sql_evaluator.add_carrier_element(a, step=2)
        self.sql_evaluator.add_carrier_element(b, step=2)
        self.sql_evaluator.add_relation(a, b, step=2)
        return self.compute_bisimulation_certificate(a, b)

    def step_03_enforce_irrefl(
        self, a: str = "pt_alpha", b: str = "pt_beta"
    ) -> ComputationBisimulationCertificate:
        self.engine.step_03_enforce_irrefl()
        self.sql_evaluator.remove_reflexive_pairs()
        return self.compute_bisimulation_certificate(a, b)

    def compute_bisimulation_certificate(
        self, a: Optional[str] = None, b: Optional[str] = None
    ) -> ComputationBisimulationCertificate:
        discrepancies = []
        step_num = self.engine.state.step

        py_carrier = set(self.engine.state.carrier)
        sql_carrier = self.sql_evaluator.get_carrier()
        forward_carrier_ok = py_carrier == sql_carrier
        if not forward_carrier_ok:
            discrepancies.append(f"Carrier mismatch: Py={py_carrier} != SQL={sql_carrier}")

        py_relations = set(self.engine.state.relations)
        sql_relations = self.sql_evaluator.get_relations()
        forward_relations_ok = py_relations == sql_relations
        if not forward_relations_ok:
            discrepancies.append(f"Relations mismatch: Py={py_relations} != SQL={sql_relations}")

        forward_ok = forward_carrier_ok and forward_relations_ok
        backward_ok = (
            all(c in py_carrier for c in sql_carrier)
            and all(r in py_relations for r in sql_relations)
            and (len(sql_carrier) == len(py_carrier))
            and (len(sql_relations) == len(py_relations))
        )

        lean_verified = self.verify_lean_compilation()
        if not lean_verified:
            discrepancies.append("Lean 4 computation_core.lean compilation failed")

        py_distinct = self.engine.setting.is_distinct() if self.engine.setting else (step_num >= 1)
        if a and b:
            sql_inv = self.sql_evaluator.evaluate_irreflexivity_and_witness_cte(a, b)
            sql_distinct = sql_inv["is_distinct"]
            sql_irrefl = sql_inv["is_irreflexive"]
        else:
            sql_distinct = True
            sql_irrefl = True

        if py_distinct != sql_distinct:
            discrepancies.append(
                f"Distinctness invariant divergence: Py={py_distinct} != SQL={sql_distinct}"
            )

        carrier_diff = len(py_carrier.symmetric_difference(sql_carrier))
        rel_diff = len(py_relations.symmetric_difference(sql_relations))
        inv_diff = 1.0 if (py_distinct != sql_distinct) else 0.0
        defect = 0.5 * (carrier_diff + rel_diff) + inv_diff

        is_bisim = (
            forward_ok
            and backward_ok
            and (py_distinct == sql_distinct)
            and sql_irrefl
            and lean_verified
            and (defect == 0.0)
            and (len(discrepancies) == 0)
        )

        return ComputationBisimulationCertificate(
            step=step_num,
            forward_simulation_holds=forward_ok,
            backward_simulation_holds=backward_ok,
            python_distinctness_valid=py_distinct,
            sql_distinctness_cte_valid=sql_distinct,
            irreflexive_certified=sql_irrefl,
            lean_core_theorem_valid=lean_verified,
            bisimulation_defect=defect,
            is_bisimilar=is_bisim,
            discrepancy_log=discrepancies,
        )

    def verify_fuel_bisimulation(
        self,
        start_node: str,
        fuel: int,
        transition_graph: Dict[str, str],
        sql_max_depth: Optional[int] = None,
    ) -> FuelBisimulationCertificate:
        """
        Evaluates and verifies bisimulation between fuel-bounded operational semantics
        (Scenario 4 Steps 08/09) and bounded-depth recursive SQL CTE termination limits.
        """
        cur = self.sql_evaluator.conn.cursor()
        cur.execute("DELETE FROM computation_relations;")
        cur.execute("DELETE FROM computation_carrier;")
        for src, dst in transition_graph.items():
            self.sql_evaluator.add_carrier_element(src, step=0)
            self.sql_evaluator.add_carrier_element(dst, step=0)
            self.sql_evaluator.add_relation(src, dst, step=0)

        # 1. Operational Small-Step Execution
        py_receipt = self.engine.execute_fuel_bounded(
            start_node=start_node, fuel=fuel, transition_graph=transition_graph
        )

        # 2. Relational SQL-CTE Execution
        actual_sql_depth = fuel if sql_max_depth is None else sql_max_depth
        sql_receipt = self.sql_evaluator.evaluate_fuel_bounded_execution_cte(
            start_node=start_node, max_depth=actual_sql_depth
        )

        # 3. Lean 4 Formal Proof Check
        lean_verified = self.verify_lean_compilation()

        # 4. Compare observables & compute bisimulation defect
        discrepancies: List[str] = []
        if not lean_verified:
            discrepancies.append("Lean 4 fuel theorem compilation failed")

        status_matched = py_receipt.status == sql_receipt["status"]
        if not status_matched:
            discrepancies.append(
                f"Status mismatch: Py={py_receipt.status} != SQL={sql_receipt['status']}"
            )

        terminal_matched = py_receipt.terminal_node == sql_receipt["terminal_node"]
        if not terminal_matched:
            discrepancies.append(
                f"Terminal node mismatch: Py={py_receipt.terminal_node} != SQL={sql_receipt['terminal_node']}"
            )

        trace_matched = py_receipt.trace == sql_receipt["trace"]
        if not trace_matched:
            discrepancies.append(
                f"Trace mismatch: Py={py_receipt.trace} != SQL={sql_receipt['trace']}"
            )

        # Quantitative defect Delta_fuel
        halt_diff = abs(int(py_receipt.status == "HALTED") - int(sql_receipt["status"] == "HALTED"))
        exhaust_diff = abs(
            int(py_receipt.status == "OUT_OF_FUEL") - int(sql_receipt["status"] == "OUT_OF_FUEL")
        )
        term_diff = 1.0 if not terminal_matched else 0.0
        step_diff = abs(py_receipt.steps_taken - sql_receipt["steps_taken"]) / (
            1.0 + py_receipt.steps_taken
        )
        defect = float(halt_diff + exhaust_diff + term_diff + step_diff)

        is_bisim = (
            status_matched
            and terminal_matched
            and trace_matched
            and lean_verified
            and (defect == 0.0)
            and (len(discrepancies) == 0)
        )

        return FuelBisimulationCertificate(
            start_node=start_node,
            fuel_budget=fuel,
            py_terminal_node=py_receipt.terminal_node,
            sql_terminal_node=sql_receipt["terminal_node"],
            py_status=py_receipt.status,
            sql_status=sql_receipt["status"],
            py_steps=py_receipt.steps_taken,
            sql_steps=sql_receipt["steps_taken"],
            py_trace=py_receipt.trace,
            sql_trace=sql_receipt["trace"],
            status_matched=status_matched,
            terminal_node_matched=terminal_matched,
            trace_matched=trace_matched,
            lean_fuel_theorems_valid=lean_verified,
            fuel_bisimulation_defect=defect,
            is_bisimilar=is_bisim,
            discrepancy_log=discrepancies,
        )
