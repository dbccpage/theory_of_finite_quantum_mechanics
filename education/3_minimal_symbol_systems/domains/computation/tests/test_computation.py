"""
Tests for Theoretical Computer Science & Automata Theory Domain Kernel
AuthorityEffect: None
"""

import sys
from pathlib import Path

# Add domain code directory to sys.path
_code_dir = Path(__file__).resolve().parent.parent / "code"
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

import pytest
from domain_computation_kernel import (
    DomainEngine,
    FuelStatus,
    SimplicialBoundaryReceipt,
    TuringConfiguration,
)


def test_initial_void_to_root():
    engine = DomainEngine()
    assert engine.state.step == 0
    assert engine.step_01_admit_root("<>")
    assert engine.state.step == 1
    assert "<>" in engine.state.carrier
    assert "branch_root_single" in engine.state.branches_retained


def test_germ_creation_and_witness():
    engine = DomainEngine()
    engine.step_01_admit_root("<>")
    assert engine.step_02_admit_germ("pt_alpha", "pt_beta")
    assert engine.state.step == 2
    assert ("pt_alpha", "pt_beta") in engine.state.relations


def test_irreflexive_enforcement_and_distinctness():
    engine = DomainEngine()
    engine.step_01_admit_root("<>")
    engine.step_02_admit_germ("pt_alpha", "pt_beta")
    # inject reflexive defect
    engine.state.relations.add(("pt_alpha", "pt_alpha"))
    assert not engine.setting.is_irrefl()

    # Discharge obstruction
    assert engine.step_03_enforce_irrefl()
    assert engine.setting.is_irrefl()
    assert engine.setting.is_distinct()


def test_boundary_closure_invariant():
    engine = DomainEngine()
    engine.step_01_admit_root("<>")
    engine.step_02_admit_germ("pt_alpha", "pt_beta")
    engine.step_03_enforce_irrefl()
    receipt = engine.evaluate_boundary_closure()
    assert isinstance(receipt, SimplicialBoundaryReceipt)
    assert receipt.is_nilpotent
    assert bool(receipt) is True
    assert engine.state.invariants["boundary_nilpotence"] is True


def test_explicit_recovery_gap_detection():
    engine = DomainEngine()
    gap_info = engine.check_gap_obstruction()
    assert gap_info["gap_id"] == "HaltingIncompletenessObstruction"
    assert gap_info["status"] == "UNBRIDGED_OBSTRUCTION"
    assert engine.gap_detected


def test_computation_kernel_bisimulation_bridge_contract():
    """Validates that DomainEngine states satisfy the relational SQL-CTE bisimulation bridge contract."""
    _sql_code_dir = Path(__file__).resolve().parent.parent.parent / "ansi_sql" / "code"
    if str(_sql_code_dir) not in sys.path:
        sys.path.insert(0, str(_sql_code_dir))
    from bisimulation_bridge import ComputationBisimulationBridge

    bridge = ComputationBisimulationBridge()
    cert1 = bridge.step_01_root("<>")
    assert cert1.is_bisimilar and cert1.bisimulation_defect == 0.0

    cert2 = bridge.step_02_germ("A", "B")
    assert cert2.is_bisimilar and cert2.bisimulation_defect == 0.0

    cert3 = bridge.step_03_enforce_irrefl("A", "B")
    assert cert3.is_bisimilar and cert3.bisimulation_defect == 0.0
    assert cert3.lean_core_theorem_valid


def test_fuel_bounded_execution_halted():
    """Validates that execute_fuel_bounded halts normally when reduction path is shorter than fuel."""
    engine = DomainEngine()
    graph = {"A": "B", "B": "C"}
    receipt = engine.execute_fuel_bounded("A", fuel=5, transition_graph=graph)
    assert receipt.status == "HALTED"
    assert receipt.terminal_node == "C"
    assert receipt.steps_taken == 2
    assert receipt.fuel_remaining == 3
    assert receipt.trace == ["A", "B", "C"]


def test_fuel_bounded_execution_out_of_fuel():
    """Validates that execute_fuel_bounded returns OUT_OF_FUEL when budget is exhausted with pending transitions."""
    engine = DomainEngine()
    graph = {"A": "B", "B": "C", "C": "D"}
    receipt = engine.execute_fuel_bounded("A", fuel=2, transition_graph=graph)
    assert receipt.status == "OUT_OF_FUEL"
    assert receipt.terminal_node == "C"
    assert receipt.steps_taken == 2
    assert receipt.fuel_remaining == 0
    assert receipt.trace == ["A", "B", "C"]
    assert receipt.obstruction is not None
    assert not receipt.obstruction.cycle_detected


def test_fuel_bounded_execution_zero_fuel():
    """Validates immediate fuel exhaustion when fuel is zero and outgoing transitions exist."""
    engine = DomainEngine()
    graph = {"A": "B"}
    receipt = engine.execute_fuel_bounded("A", fuel=0, transition_graph=graph)
    assert receipt.status == "OUT_OF_FUEL"
    assert receipt.terminal_node == "A"
    assert receipt.steps_taken == 0
    assert receipt.fuel_remaining == 0
    assert receipt.trace == ["A"]


def test_step_01_through_16_complete_progression():
    """Verifies all 16 steps of the Genesis Domain Computation scenario progression."""
    engine = DomainEngine()

    # Step 01: Initial datum
    assert engine.step_01_admit_root("<>")
    assert engine.state.step == 1
    assert "branch_root_single" in engine.state.branches_retained

    # Step 02: Primitive distinction germ
    assert engine.step_02_admit_germ("a", "b")
    assert engine.state.step == 2

    # Step 03: Enforce irreflexivity
    assert engine.step_03_enforce_irrefl()
    assert engine.state.step == 3

    # Step 04: Admit orientation with tie retention (D2 and S2)
    assert engine.step_04_admit_orientation()
    assert engine.state.step == 4
    assert set(engine.state.branches_retained) == {"branch_D2", "branch_S2"}
    assert "branch_D2" in engine.state.branch_metadata
    assert "branch_S2" in engine.state.branch_metadata

    # Step 05: Transposition antisymmetry
    assert engine.step_05_admit_transposition()
    assert engine.state.step == 5
    assert engine.state.invariants["transposition_sign_inversion"] is True

    # Step 06: Instantiate alphabet
    assert engine.step_06_instantiate_alphabet(["0", "1", "_"])
    assert engine.state.step == 6

    # Step 07: Evaluate boundary closure
    b_receipt = engine.step_07_evaluate_boundary_closure()
    assert engine.state.step == 7
    assert b_receipt.is_nilpotent

    # Step 08: Synthesize transition poset
    assert engine.step_08_synthesize_transition_poset()
    assert engine.state.step == 8

    # Step 09: Resolve parity
    assert engine.step_09_resolve_parity()
    assert engine.state.step == 9

    # Step 10: Higher complexes
    assert engine.step_10_admit_higher_complexes()
    assert engine.state.step == 10

    # Step 11: Enforce conservation
    assert engine.step_11_enforce_conservation()
    assert engine.state.step == 11

    # Step 12: Quotient observer interface
    assert engine.step_12_quotient_observer_interface()
    assert engine.state.step == 12

    # Step 13: Prune branches
    assert engine.step_13_prune_fuel_bounded_branches()
    assert engine.state.step == 13

    # Step 14: Establish frontier
    assert engine.step_14_establish_frontier()
    assert engine.state.step == 14

    # Step 15: Isolate gap obstruction
    gap = engine.step_15_isolate_gap_obstruction()
    assert engine.state.step == 15
    assert gap["gap_id"] == "HaltingIncompletenessObstruction"

    # Step 16: Terminal certification
    cert = engine.step_16_terminal_certification()
    assert engine.state.step == 16
    assert cert["status"] == "CERTIFIED"
    assert cert["steps_completed"] == 16
    assert cert["authority_effect"] == "None"


def test_transposition_sign_inversion():
    """Verifies partial_1(sigma(e)) == -partial_1(e) on directed edges."""
    engine = DomainEngine()
    engine.step_01_admit_root()
    engine.step_02_admit_germ("q0", "q1")
    engine.step_03_enforce_irrefl()

    edge = ("q0", "q1")
    trans_edge = engine.setting.transpose(edge)
    assert trans_edge == ("q1", "q0")

    b_orig = engine.setting.evaluate_1chain_boundary(edge)
    b_trans = engine.setting.evaluate_1chain_boundary(trans_edge)

    assert b_orig == {"q1": 1, "q0": -1}
    assert b_trans == {"q0": 1, "q1": -1}
    assert engine.setting.verify_transposition_sign_inversion(edge)


def test_simplicial_boundary_nilpotency_matrix():
    """Verifies exact B_1 * B_2 = 0 matrix multiplication on 2-simplex triangle."""
    engine = DomainEngine()
    vertices = ["v0", "v1", "v2"]
    edges = [("v0", "v1"), ("v1", "v2"), ("v0", "v2")]
    faces = [("v0", "v1", "v2")]

    receipt = engine.evaluate_simplicial_boundary_matrices(vertices, edges, faces)
    assert receipt.is_nilpotent
    assert receipt.num_cycles == 1
    assert receipt.euler_characteristic == 1  # 3 - 3 + 1 = 1
    for row in receipt.product_matrix:
        for val in row:
            assert val == 0


def test_turing_machine_busy_beaver_2state():
    """
    2-state 2-symbol Busy Beaver executes in exactly 6 steps on blank tape
    and produces 4 ones before halting in state H.
    """
    engine = DomainEngine()

    # Delta table: (state, symbol) -> (new_state, write_symbol, direction)
    # Directions: +1 (Right), -1 (Left)
    table = {
        ("A", "_"): ("B", "1", 1),
        ("A", "1"): ("B", "1", -1),
        ("B", "_"): ("A", "1", -1),
        ("B", "1"): ("H", "1", 1),
    }
    halting = {"H"}
    init_cfg = TuringConfiguration(state="A", head_pos=0, tape=())

    # Execution with sufficient fuel (fuel=10)
    receipt = engine.execute_turing_machine(
        initial_config=init_cfg,
        transition_table=table,
        halting_states=halting,
        fuel=10,
        blank_symbol="_",
    )

    assert receipt.status == FuelStatus.HALTED
    assert receipt.steps_taken == 6
    assert receipt.fuel_remaining == 4
    assert receipt.terminal_config.state == "H"
    # Verify exactly 4 ones on tape
    ones_count = sum(1 for sym in receipt.terminal_config.tape_dict().values() if sym == "1")
    assert ones_count == 4
    assert len(receipt.step_receipts) == 6


def test_turing_machine_cycle_detection():
    """
    An oscillating Turing machine (q0 -> q1 -> q0) detects periodic repetition.
    """
    engine = DomainEngine()
    table = {
        ("q0", "_"): ("q1", "_", 0),  # Stay in place, flip state
        ("q1", "_"): ("q0", "_", 0),
    }
    halting = {"q_halt"}
    init_cfg = TuringConfiguration(state="q0", head_pos=0, tape=())

    receipt = engine.execute_turing_machine(
        initial_config=init_cfg,
        transition_table=table,
        halting_states=halting,
        fuel=10,
        blank_symbol="_",
    )

    assert receipt.status == FuelStatus.CYCLE_DETECTED
    assert receipt.obstruction is not None
    assert receipt.obstruction.cycle_detected is True
    assert receipt.obstruction.cycle_period == 2


def test_graph_reduction_cycle_detection():
    """
    Graph reduction with cycle A -> B -> A detects cycle.
    """
    engine = DomainEngine()
    graph = {"A": "B", "B": "A"}
    receipt = engine.execute_fuel_bounded("A", fuel=10, transition_graph=graph, detect_cycles=True)

    assert receipt.status == FuelStatus.CYCLE_DETECTED
    assert receipt.obstruction is not None
    assert receipt.obstruction.cycle_detected is True
    assert receipt.obstruction.cycle_period == 2
    assert receipt.trace == ["A", "B", "A"]


def test_fuel_exact_boundary():
    """
    Machine requiring 5 steps halts when fuel=5 (with 0 remaining),
    and returns OUT_OF_FUEL when fuel=4.
    """
    engine = DomainEngine()
    graph = {f"n{i}": f"n{i + 1}" for i in range(5)}  # n0 -> n1 -> n2 -> n3 -> n4 -> n5 (5 steps)

    receipt_exact = engine.execute_fuel_bounded("n0", fuel=5, transition_graph=graph)
    assert receipt_exact.status == FuelStatus.HALTED
    assert receipt_exact.steps_taken == 5
    assert receipt_exact.fuel_remaining == 0
    assert receipt_exact.terminal_node == "n5"

    receipt_under = engine.execute_fuel_bounded("n0", fuel=4, transition_graph=graph)
    assert receipt_under.status == FuelStatus.OUT_OF_FUEL
    assert receipt_under.steps_taken == 4
    assert receipt_under.fuel_remaining == 0
    assert receipt_under.terminal_node == "n4"


def test_negative_control_self_loop_rejected():
    """Negative Control: Self loop (a, a) is purged during step 03."""
    engine = DomainEngine()
    engine.step_01_admit_root()
    engine.step_02_admit_germ("a", "b")
    engine.state.relations.add(("a", "a"))
    assert not engine.setting.is_irrefl()

    # Step 03 cleans it out
    engine.step_03_enforce_irrefl()
    assert ("a", "a") not in engine.state.relations
    assert engine.setting.is_irrefl()


def test_negative_control_negative_fuel_raises():
    """Negative Control: Negative fuel budget raises ValueError."""
    engine = DomainEngine()
    with pytest.raises(ValueError, match="Fuel budget must be non-negative"):
        engine.execute_fuel_bounded("A", fuel=-1)

    init_cfg = TuringConfiguration("q0", 0, ())
    with pytest.raises(ValueError, match="Fuel budget must be non-negative"):
        engine.execute_turing_machine(init_cfg, {}, set(), fuel=-3)


def test_negative_control_boundary_matrices_empty_raises():
    """Negative Control: Empty complex inputs raise ValueError."""
    engine = DomainEngine()
    with pytest.raises(ValueError, match="must be non-empty"):
        engine.evaluate_simplicial_boundary_matrices([], [], [])
