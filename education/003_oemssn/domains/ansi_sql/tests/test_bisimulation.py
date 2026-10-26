"""
Pytest Suite: Formal Bisimulation Checks between Lean 4 Simplicial Complex & Python Relational CTE Evaluator
AuthorityEffect: None.
"""

import sys
from pathlib import Path

_code_dir = Path(__file__).resolve().parent.parent / "code"
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

from bisimulation_bridge import (
    ComputationBisimulationBridge,
    ComputationCTEEvaluator,
    SimplicialBisimulationBridge,
)
from simplicial_cte_evaluator import SimplicialCTEEvaluator


def test_lean4_formal_compilation():
    """Validates that the Lean 4 simplicial complex formalization compiles with 0 errors."""
    bridge = SimplicialBisimulationBridge()
    assert bridge.verify_lean_compilation(), "Lean 4 simplicial_complex.lean failed to elaborate"


def test_sql_cte_nilpotence_evaluation():
    """Validates that SQL CTE evaluates boundary nilpotence (d_1 ∘ d_2 = 0) on a 2-simplex."""
    evaluator = SimplicialCTEEvaluator(in_memory=True)
    evaluator.add_triangle("T1", "A", "B", "C")
    report = evaluator.evaluate_boundaries_and_nilpotence()

    assert report["stokes_nilpotence_holds"]
    assert report["total_vertex_evaluations"] == 3
    for ev in report["evaluations"]:
        assert ev["net_multiplicity"] == 0
        assert ev["nilpotence_verified"]
    evaluator.close()


def test_sql_window_quotient_partitions():
    """Validates that window quotient OVER (PARTITION BY ...) groups geometric orbits correctly."""
    evaluator = SimplicialCTEEvaluator(in_memory=True)
    evaluator.add_triangle("T1", "A", "B", "C")
    evaluator.add_triangle("T2", "B", "A", "D")  # Shares edge A-B with T1

    orbits = evaluator.compute_window_quotient_orbits()
    assert len(orbits) == 6  # 3 edges per triangle

    # Check shared edge A-B orbit multiplicity
    ab_orbits = [o for o in orbits if o["geometric_orbit_id"] in ("A<->B", "B<->A")]
    assert len(ab_orbits) == 2
    assert all(o["orbit_multiplicity"] == 2 for o in ab_orbits)
    evaluator.close()


def test_forward_simulation_morphism():
    """Validates forward simulation: Lean state transition maps to exact relational boundary tuples."""
    bridge = SimplicialBisimulationBridge()
    cert = bridge.step("T1", "v0", "v1", "v2")
    assert cert.forward_simulation_holds
    assert cert.lean_nilpotence_theorem_valid
    assert cert.sql_nilpotence_cte_valid
    assert cert.is_bisimilar


def test_backward_simulation_extraction():
    """Validates backward simulation: SQL CTE boundary tuples decode into valid Lean chain states."""
    bridge = SimplicialBisimulationBridge()
    cert = bridge.step("T1", "x", "y", "z")
    assert cert.backward_simulation_holds
    assert len(cert.discrepancy_log) == 0
    assert cert.is_bisimilar


def test_multi_step_bisimulation_trajectory():
    """
    Validates a multi-step tetrahedral surface trajectory (4 triangles glued together),
    verifying bisimilarity at every single discrete step.
    """
    bridge = SimplicialBisimulationBridge()

    # 4 faces of a tetrahedron: (0,1,2), (0,2,3), (0,3,1), (1,3,2)
    tetra_faces = [
        ("F0", "v0", "v1", "v2"),
        ("F1", "v0", "v2", "v3"),
        ("F2", "v0", "v3", "v1"),
        ("F3", "v1", "v3", "v2"),
    ]

    for step_num, (fid, v0, v1, v2) in enumerate(tetra_faces, start=1):
        cert = bridge.step(fid, v0, v1, v2)
        assert cert.step == step_num
        assert cert.is_bisimilar, f"Bisimulation failed at step {step_num}: {cert.discrepancy_log}"
        assert cert.lean_nilpotence_theorem_valid
        assert cert.sql_nilpotence_cte_valid


# ==============================================================================
# Computation Operational Semantics <-> SQL-CTE Bisimulation Tests
# ==============================================================================


def test_computation_lean4_formal_compilation():
    """Validates that Lean 4 computation_core.lean formal core elaborates cleanly."""
    bridge = ComputationBisimulationBridge()
    assert bridge.verify_lean_compilation(), "computation_core.lean failed to elaborate"


def test_computation_sql_cte_evaluator_standalone():
    """Validates standalone SQL CTE execution for carrier, relations, and irreflexivity."""
    evaluator = ComputationCTEEvaluator(in_memory=True)
    evaluator.add_carrier_element("pt_alpha", step=1)
    evaluator.add_carrier_element("pt_beta", step=1)
    evaluator.add_relation("pt_alpha", "pt_beta", step=1)

    inv = evaluator.evaluate_irreflexivity_and_witness_cte("pt_alpha", "pt_beta")
    assert inv["is_irreflexive"]
    assert inv["is_witnessed"]
    assert inv["is_distinct"]
    evaluator.close()


def test_computation_bisimulation_step_01_root():
    """Validates Step 1 forward/backward simulation on root mark admission."""
    bridge = ComputationBisimulationBridge()
    cert = bridge.step_01_root("<>")
    assert cert.step == 1
    assert cert.forward_simulation_holds
    assert cert.backward_simulation_holds
    assert cert.bisimulation_defect == 0.0
    assert cert.is_bisimilar


def test_computation_bisimulation_step_02_germ():
    """Validates Step 2 forward/backward simulation on germ difference pair admission."""
    bridge = ComputationBisimulationBridge()
    bridge.step_01_root("<>")
    cert = bridge.step_02_germ("x0", "x1")
    assert cert.step == 2
    assert cert.forward_simulation_holds
    assert cert.backward_simulation_holds
    assert cert.python_distinctness_valid
    assert cert.sql_distinctness_cte_valid
    assert cert.bisimulation_defect == 0.0
    assert cert.is_bisimilar


def test_computation_bisimulation_step_03_irreflexive_enforcement():
    """Validates Step 3 irreflexivity enforcement and distinctness preservation."""
    bridge = ComputationBisimulationBridge()
    bridge.step_01_root("<>")
    bridge.step_02_germ("a", "b")
    cert = bridge.step_03_enforce_irrefl("a", "b")
    assert cert.step == 3
    assert cert.irreflexive_certified
    assert cert.python_distinctness_valid
    assert cert.sql_distinctness_cte_valid
    assert cert.bisimulation_defect == 0.0
    assert cert.is_bisimilar


def test_computation_bisimulation_multi_step_trajectory():
    """Validates complete 3-step operational trajectory ensuring defect Delta_bisim = 0."""
    bridge = ComputationBisimulationBridge()
    c1 = bridge.step_01_root("<>")
    assert c1.is_bisimilar and c1.bisimulation_defect == 0.0

    c2 = bridge.step_02_germ("node_A", "node_B")
    assert c2.is_bisimilar and c2.bisimulation_defect == 0.0

    c3 = bridge.step_03_enforce_irrefl("node_A", "node_B")
    assert c3.is_bisimilar and c3.bisimulation_defect == 0.0
    assert c3.lean_core_theorem_valid


def test_computation_bisimulation_defect_detection_negative_control():
    """
    Negative control: injects reflexive defect into relational SQL state
    and asserts that bisimulation bounds strictly detect divergence (Delta_bisim >= 1.0).
    """
    bridge = ComputationBisimulationBridge()
    bridge.step_01_root("<>")
    bridge.step_02_germ("a", "b")
    # Invalidate relational state by injecting reflexive self-loop
    bridge.sql_evaluator.add_relation("a", "a", step=2)

    cert = bridge.compute_bisimulation_certificate("a", "b")
    assert not cert.is_bisimilar
    assert cert.bisimulation_defect >= 1.0
    assert any("Relations mismatch" in d for d in cert.discrepancy_log)
    assert any("Distinctness invariant divergence" in d for d in cert.discrepancy_log)


def test_computation_sql_cte_transitive_closure_and_cotransitivity():
    """Validates recursive transitive closure CTE and cotransitivity evaluation."""
    evaluator = ComputationCTEEvaluator(in_memory=True)
    for n in ["n1", "n2", "n3"]:
        evaluator.add_carrier_element(n, step=1)
    evaluator.add_relation("n1", "n2", step=1)
    evaluator.add_relation("n2", "n3", step=1)

    closure = evaluator.evaluate_transitive_closure_cte()
    edges = [(r[0], r[1]) for r in closure]
    assert ("n1", "n2") in edges
    assert ("n2", "n3") in edges
    assert ("n1", "n3") in edges  # Inferred by recursive CTE

    cotrans = evaluator.evaluate_cotransitivity_cte()
    assert cotrans["total_triples"] == 6  # 2 relations x 3 carrier elements
    evaluator.close()


def test_fuel_bisimulation_normal_halt():
    """
    Validates lockstep bisimulation between fuel-exhaustion operational semantics
    and bounded-depth recursive SQL CTE when the reduction sequence terminates normally.
    Defect Delta_fuel must evaluate to 0.0.
    """
    bridge = ComputationBisimulationBridge()
    graph = {"A": "B", "B": "C", "C": "D"}
    cert = bridge.verify_fuel_bisimulation(start_node="A", fuel=5, transition_graph=graph)

    assert cert.is_bisimilar
    assert cert.fuel_bisimulation_defect == 0.0
    assert cert.status_matched
    assert cert.terminal_node_matched
    assert cert.trace_matched
    assert cert.py_status == "HALTED"
    assert cert.sql_status == "HALTED"
    assert cert.py_terminal_node == "D"
    assert cert.sql_terminal_node == "D"
    assert cert.py_steps == 3
    assert cert.sql_steps == 3
    assert cert.py_trace == ["A", "B", "C", "D"]
    assert cert.lean_fuel_theorems_valid


def test_fuel_bisimulation_exhaustion():
    """
    Validates lockstep bisimulation when operational reduction exhausts its fuel budget
    and SQL CTE terminates at max_depth with pending outgoing transitions.
    Both systems must agree on OUT_OF_FUEL and Delta_fuel must be 0.0.
    """
    bridge = ComputationBisimulationBridge()
    graph = {"A": "B", "B": "C", "C": "D", "D": "E"}
    cert = bridge.verify_fuel_bisimulation(start_node="A", fuel=2, transition_graph=graph)

    assert cert.is_bisimilar
    assert cert.fuel_bisimulation_defect == 0.0
    assert cert.status_matched
    assert cert.py_status == "OUT_OF_FUEL"
    assert cert.sql_status == "OUT_OF_FUEL"
    assert cert.py_terminal_node == "C"
    assert cert.sql_terminal_node == "C"
    assert cert.py_steps == 2
    assert cert.sql_steps == 2
    assert cert.py_trace == ["A", "B", "C"]
    assert cert.lean_fuel_theorems_valid


def test_fuel_bisimulation_cycle_exhaustion():
    """
    Validates fuel-bounded reduction and CTE termination over a cyclic graph.
    Both systems execute exactly fuel=7 steps and report OUT_OF_FUEL with defect Delta_fuel = 0.0.
    """
    bridge = ComputationBisimulationBridge()
    cycle_graph = {"s0": "s1", "s1": "s2", "s2": "s0"}
    cert = bridge.verify_fuel_bisimulation(start_node="s0", fuel=7, transition_graph=cycle_graph)

    assert cert.is_bisimilar
    assert cert.fuel_bisimulation_defect == 0.0
    assert cert.status_matched
    assert cert.py_status == "OUT_OF_FUEL"
    assert cert.sql_status == "OUT_OF_FUEL"
    assert cert.py_terminal_node == "s1"
    assert cert.sql_terminal_node == "s1"
    assert cert.py_steps == 7
    assert cert.sql_steps == 7
    assert cert.lean_fuel_theorems_valid


def test_fuel_bisimulation_depth_mismatch_negative_control():
    """
    Negative control: deliberately desynchronizes operational fuel budget (fuel=2)
    from SQL CTE termination limit (max_depth=5), asserting that bisimulation bounds
    detect the defect with Delta_fuel >= 1.0.
    """
    bridge = ComputationBisimulationBridge()
    graph = {"A": "B", "B": "C", "C": "D"}
    # Py runs with fuel=2 (stops at C, OUT_OF_FUEL); SQL runs with depth=5 (stops at D, HALTED)
    cert = bridge.verify_fuel_bisimulation(
        start_node="A", fuel=2, transition_graph=graph, sql_max_depth=5
    )

    assert not cert.is_bisimilar
    assert cert.fuel_bisimulation_defect >= 1.0
    assert not cert.status_matched
    assert not cert.terminal_node_matched
    assert not cert.trace_matched
    assert cert.py_status == "OUT_OF_FUEL"
    assert cert.sql_status == "HALTED"
    assert any("Status mismatch" in d for d in cert.discrepancy_log)
    assert any("Terminal node mismatch" in d for d in cert.discrepancy_log)


# ==============================================================================
# Bounded-Degree Simplicial Homology Fuel Bisimulation Tests
# ==============================================================================


def test_simplicial_fuel_compilation():
    """Validates that Lean 4 simplicial_complex.lean with fuel theorems elaborates with 0 errors."""
    bridge = SimplicialBisimulationBridge()
    assert bridge.verify_lean_compilation(), "simplicial_complex.lean failed to elaborate"


def test_simplicial_fuel_full_descent_halted():
    """
    Validates lockstep bisimulation when fuel F=2 enables complete homology descent (C2 -> C1 -> C0).
    Status must be HALTED, Stokes nilpotence (d1 ∘ d2 = 0) certified, and defect Delta_fuel_simp = 0.0.
    """
    bridge = SimplicialBisimulationBridge()
    cert = bridge.verify_fuel_simplicial_bisimulation("T1", "v0", "v1", "v2", fuel=2)

    assert cert.is_bisimilar
    assert cert.fuel_simplicial_defect == 0.0
    assert cert.status_matched
    assert cert.terminal_dim_matched
    assert cert.steps_matched
    assert cert.nilpotence_matched
    assert cert.py_status == "HALTED"
    assert cert.sql_status == "HALTED"
    assert cert.py_terminal_dim == 0
    assert cert.sql_terminal_dim == 0
    assert cert.py_steps == 2
    assert cert.sql_steps == 2
    assert cert.py_nilpotence_certified
    assert cert.sql_nilpotence_certified
    assert cert.lean_fuel_theorems_valid


def test_simplicial_fuel_exhaustion_at_degree_1():
    """
    Validates lockstep bisimulation when fuel F=1 halts descent at degree 1 (edges).
    Status must be OUT_OF_FUEL, nilpotence uncertified, terminal_dim = 1, and defect Delta_fuel_simp = 0.0.
    """
    bridge = SimplicialBisimulationBridge()
    cert = bridge.verify_fuel_simplicial_bisimulation("T2", "a", "b", "c", fuel=1)

    assert cert.is_bisimilar
    assert cert.fuel_simplicial_defect == 0.0
    assert cert.status_matched
    assert cert.py_status == "OUT_OF_FUEL"
    assert cert.sql_status == "OUT_OF_FUEL"
    assert cert.py_terminal_dim == 1
    assert cert.sql_terminal_dim == 1
    assert cert.py_steps == 1
    assert cert.sql_steps == 1
    assert not cert.py_nilpotence_certified
    assert not cert.sql_nilpotence_certified
    assert cert.lean_fuel_theorems_valid


def test_simplicial_fuel_exhaustion_at_degree_2():
    """
    Validates lockstep bisimulation when fuel F=0 halts descent at degree 2 (triangles).
    Status must be OUT_OF_FUEL, steps = 0, terminal_dim = 2, and defect Delta_fuel_simp = 0.0.
    """
    bridge = SimplicialBisimulationBridge()
    cert = bridge.verify_fuel_simplicial_bisimulation("T3", "x", "y", "z", fuel=0)

    assert cert.is_bisimilar
    assert cert.fuel_simplicial_defect == 0.0
    assert cert.status_matched
    assert cert.py_status == "OUT_OF_FUEL"
    assert cert.sql_status == "OUT_OF_FUEL"
    assert cert.py_terminal_dim == 2
    assert cert.sql_terminal_dim == 2
    assert cert.py_steps == 0
    assert cert.sql_steps == 0
    assert not cert.py_nilpotence_certified
    assert not cert.sql_nilpotence_certified
    assert cert.lean_fuel_theorems_valid


def test_simplicial_fuel_depth_mismatch_negative_control():
    """
    Negative control: desynchronizes operational fuel budget (fuel=1) from SQL CTE limit (max_degree=2),
    asserting that bisimulation bounds strictly detect divergence (Delta_fuel_simp >= 1.0).
    """
    bridge = SimplicialBisimulationBridge()
    cert = bridge.verify_fuel_simplicial_bisimulation(
        "T4", "p0", "p1", "p2", fuel=1, sql_max_degree=2
    )

    assert not cert.is_bisimilar
    assert cert.fuel_simplicial_defect >= 1.0
    assert not cert.status_matched
    assert not cert.terminal_dim_matched
    assert not cert.steps_matched
    assert not cert.nilpotence_matched
    assert cert.py_status == "OUT_OF_FUEL"
    assert cert.sql_status == "HALTED"
    assert any("Status mismatch" in d for d in cert.discrepancy_log)
    assert any("Terminal dimension mismatch" in d for d in cert.discrepancy_log)


def test_simplicial_multi_triangle_fuel_trajectory():
    """
    Validates bounded-degree homology fuel bisimulation across all 4 faces of a tetrahedron,
    verifying lockstep bisimulation at both full descent (fuel=2) and partial descent (fuel=1).
    """
    bridge = SimplicialBisimulationBridge()
    tetra_faces = [
        ("F0", "v0", "v1", "v2"),
        ("F1", "v0", "v2", "v3"),
        ("F2", "v0", "v3", "v1"),
        ("F3", "v1", "v3", "v2"),
    ]

    for fid, v0, v1, v2 in tetra_faces:
        cert_full = bridge.verify_fuel_simplicial_bisimulation(fid, v0, v1, v2, fuel=2)
        assert cert_full.is_bisimilar and cert_full.fuel_simplicial_defect == 0.0
        assert cert_full.py_status == "HALTED"
        assert cert_full.py_nilpotence_certified

        cert_partial = bridge.verify_fuel_simplicial_bisimulation(fid, v0, v1, v2, fuel=1)
        assert cert_partial.is_bisimilar and cert_partial.fuel_simplicial_defect == 0.0
        assert cert_partial.py_status == "OUT_OF_FUEL"
        assert not cert_partial.py_nilpotence_certified


# ==============================================================================
# Discrete de Rham Differential Forms & Hodge Star Duality Transfer Tests
# ==============================================================================


def _create_sample_simplicial_lattice():
    """
    Creates a standard 2D simplicial lattice patch (two glued triangles sharing an edge).
    Vertices:
      v0: (x=0, y=0), dual_area = 1.0, phi = 2.0
      v1: (x=1, y=0), dual_area = 1.0, phi = 5.0
      v2: (x=0, y=1), dual_area = 1.0, phi = 3.0
      v3: (x=1, y=1), dual_area = 1.0, phi = 7.0
    Triangles:
      T0: (v0, v1, v2)
      T1: (v1, v3, v2)
    Edges:
      e01: v0 -> v1, len=1.0, dual=1.0, star1=1.0
      e02: v0 -> v2, len=1.0, dual=1.0, star1=1.0
      e12: v1 -> v2, len=1.414, dual=1.414, star1=1.0 (shared diagonal)
      e13: v1 -> v3, len=1.0, dual=1.0, star1=1.0
      e23: v2 -> v3, len=1.0, dual=1.0, star1=1.0
    """
    vertices = {
        "v0": (1.0, 2.0),
        "v1": (1.0, 5.0),
        "v2": (1.0, 3.0),
        "v3": (1.0, 7.0),
    }
    edges = [
        ("e01", "v0", "v1", 1.0, 1.0, 1.0),
        ("e02", "v0", "v2", 1.0, 1.0, 1.0),
        ("e12", "v1", "v2", 1.414, 1.414, 1.0),
        ("e13", "v1", "v3", 1.0, 1.0, 1.0),
        ("e23", "v2", "v3", 1.0, 1.0, 1.0),
    ]
    triangles = [
        ("T0", "v0", "v1", "v2"),
        ("T1", "v1", "v3", "v2"),
    ]
    return vertices, edges, triangles


def test_derham_lean4_formal_compilation():
    """Validates that Lean 4 DEC and de Rham / Hodge fuel theorems elaborate with 0 errors."""
    bridge = SimplicialBisimulationBridge()
    assert bridge.verify_lean_compilation(), "simplicial_complex.lean DEC compilation failed"


def test_derham_hodge_full_transfer_fuel_2():
    """
    Validates complete transfer closure at fuel F=2:
    Both exterior derivative d_0 and dual Hodge codifferential delta_1 close.
    Status is HALTED, terminal_stage = 2, Laplacian Delta_0 is fully evaluated,
    and transfer defect Delta_transfer == 0.0.
    """
    bridge = SimplicialBisimulationBridge()
    vertices, edges, triangles = _create_sample_simplicial_lattice()

    cert = bridge.verify_derham_hodge_transfer(
        lattice_id="Lattice2D_Quad",
        vertices=vertices,
        edges=edges,
        triangles=triangles,
        fuel=2,
    )

    assert cert.is_transfer_exact
    assert cert.transfer_defect == 0.0
    assert cert.status_matched
    assert cert.stage_matched
    assert cert.steps_matched
    assert cert.laplacian_closed_matched
    assert cert.hodge_closed_matched
    assert cert.nilpotence_matched
    assert cert.py_status == "HALTED"
    assert cert.sql_status == "HALTED"
    assert cert.py_terminal_stage == 2
    assert cert.sql_terminal_stage == 2
    assert cert.py_steps == 2
    assert cert.sql_steps == 2
    assert cert.py_laplacian_closed
    assert cert.sql_laplacian_closed
    assert cert.py_hodge_closed
    assert cert.sql_hodge_closed
    assert cert.py_nilpotence_certified
    assert cert.sql_nilpotence_certified
    assert cert.lean_derham_theorems_valid
    assert len(cert.discrepancy_log) == 0


def test_derham_hodge_partial_transfer_fuel_1():
    """
    Validates partial transfer at fuel F=1:
    1-forms d_0 phi are evaluated, de Rham nilpotence d_1(d_0 phi) = 0 is certified on triangles,
    but the dual Hodge codifferential is unclosed (OUT_OF_FUEL, Delta_transfer > 0).
    """
    bridge = SimplicialBisimulationBridge()
    vertices, edges, triangles = _create_sample_simplicial_lattice()

    cert = bridge.verify_derham_hodge_transfer(
        lattice_id="Lattice2D_Quad",
        vertices=vertices,
        edges=edges,
        triangles=triangles,
        fuel=1,
    )

    assert not cert.is_transfer_exact
    assert cert.transfer_defect > 0.0
    assert cert.status_matched
    assert cert.stage_matched
    assert cert.steps_matched
    assert cert.py_status == "OUT_OF_FUEL"
    assert cert.sql_status == "OUT_OF_FUEL"
    assert cert.py_terminal_stage == 1
    assert cert.sql_terminal_stage == 1
    assert cert.py_steps == 1
    assert cert.sql_steps == 1
    assert not cert.py_laplacian_closed
    assert not cert.sql_laplacian_closed
    assert not cert.py_hodge_closed
    assert not cert.sql_hodge_closed
    assert cert.py_nilpotence_certified
    assert cert.sql_nilpotence_certified
    assert cert.lean_derham_theorems_valid


def test_derham_hodge_zero_fuel_0():
    """
    Validates fuel exhaustion at F=0:
    No exterior derivatives evaluate, status is OUT_OF_FUEL, terminal_stage = 0,
    and Delta_transfer >= 2.0.
    """
    bridge = SimplicialBisimulationBridge()
    vertices, edges, triangles = _create_sample_simplicial_lattice()

    cert = bridge.verify_derham_hodge_transfer(
        lattice_id="Lattice2D_Quad",
        vertices=vertices,
        edges=edges,
        triangles=triangles,
        fuel=0,
    )

    assert not cert.is_transfer_exact
    assert cert.transfer_defect >= 2.0
    assert cert.status_matched
    assert cert.stage_matched
    assert cert.steps_matched
    assert cert.py_status == "OUT_OF_FUEL"
    assert cert.sql_status == "OUT_OF_FUEL"
    assert cert.py_terminal_stage == 0
    assert cert.sql_terminal_stage == 0
    assert cert.py_steps == 0
    assert cert.sql_steps == 0
    assert not cert.py_laplacian_closed
    assert not cert.sql_laplacian_closed
    assert not cert.py_nilpotence_certified


def test_derham_coboundary_nilpotence_exact():
    """
    Validates that de Rham coboundary nilpotence (d_1 ∘ d_0)(phi) = 0 holds
    identically for arbitrary, non-trivial 0-forms across multiple simplices.
    """
    evaluator = SimplicialCTEEvaluator(in_memory=True)
    evaluator.add_triangle("T_arb", "alpha", "beta", "gamma")

    evaluator.add_lattice_vertex("alpha", dual_area=1.0, phi_val=-123.456)
    evaluator.add_lattice_vertex("beta", dual_area=1.0, phi_val=789.101)
    evaluator.add_lattice_vertex("gamma", dual_area=1.0, phi_val=42.0)

    report = evaluator.evaluate_derham_hodge_cte(max_fuel=2)
    assert report["nilpotence_certified"], "de Rham coboundary nilpotence d1(d0 phi) failed"
    evaluator.close()


def test_derham_sql_desync_negative_control():
    """
    Negative control: desynchronizes operational fuel (fuel=1) from SQL CTE fuel (sql_fuel=2),
    asserting that transfer bounds strictly detect divergence (Delta_transfer >= 1.0).
    """
    bridge = SimplicialBisimulationBridge()
    vertices, edges, triangles = _create_sample_simplicial_lattice()

    cert = bridge.verify_derham_hodge_transfer(
        lattice_id="Lattice2D_Quad",
        vertices=vertices,
        edges=edges,
        triangles=triangles,
        fuel=1,
        sql_fuel=2,
    )

    assert not cert.is_transfer_exact
    assert cert.transfer_defect >= 1.0
    assert not cert.status_matched
    assert not cert.stage_matched
    assert not cert.steps_matched
    assert not cert.laplacian_closed_matched
    assert not cert.hodge_closed_matched
    assert cert.py_status == "OUT_OF_FUEL"
    assert cert.sql_status == "HALTED"
    assert any("Status mismatch" in d for d in cert.discrepancy_log)
    assert any("Terminal stage mismatch" in d for d in cert.discrepancy_log)


def test_derham_simplicial_lattice_cotan_laplacian():
    """
    Validates discrete cotangent Laplacian evaluation on a non-uniform simplicial lattice
    with varying edge lengths, dual lengths, and dual Voronoi areas.
    Confirms exact algebraic agreement between Python DEC formula and SQL CTE.
    """
    bridge = SimplicialBisimulationBridge()
    vertices = {
        "A": (2.5, 10.0),
        "B": (1.8, 3.0),
        "C": (3.2, 7.0),
    }
    edges = [
        ("eAB", "A", "B", 2.0, 1.0, 0.5),  # star1 = 0.5
        ("eBC", "B", "C", 1.0, 1.5, 1.5),  # star1 = 1.5
        ("eAC", "A", "C", 1.5, 3.0, 2.0),  # star1 = 2.0
    ]
    triangles = [
        ("T_ABC", "A", "B", "C"),
    ]

    cert = bridge.verify_derham_hodge_transfer(
        lattice_id="Lattice_NonUniform",
        vertices=vertices,
        edges=edges,
        triangles=triangles,
        fuel=2,
    )

    assert cert.is_transfer_exact
    assert cert.transfer_defect == 0.0
    assert cert.py_laplacian_closed
    assert cert.sql_laplacian_closed
