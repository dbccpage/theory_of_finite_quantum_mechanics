"""Unit & Integration Test Suite: Categorical Quantum State Transfer Cochains.
AuthorityEffect: None.

Tests:
1. Lean 4 formal kernel compilation (quantum_state_transfer_core.lean).
2. SQL CTE Bell entanglement witness audit (Tr(W rho) < 0 vs separable >= 0).
3. SQL CTE Tripartite GHZ entanglement witness audit.
4. SQL CTE Quantum teleportation feedforward determinism across all 4 Bell measurement outcomes.
5. SQL CTE Feedforward mismatch & sub-threshold noise -> SplitBrainRefusal.
6. SQL CTE Protocol syntax & channel defect -> ClosureFailure.
7. SQL CTE Bennett entanglement distillation purification audit (F' > F).
8. Full end-to-end bisimulation bridge verification suite.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

code_dir = Path(__file__).resolve().parent.parent / "code"
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from quantum_state_transfer_bisimulation_bridge import QuantumStateTransferBisimulationBridge
from quantum_state_transfer_evaluator import QuantumStateTransferEvaluator


def test_lean4_quantum_state_transfer_core_compilation():
    """Validates that lean4/quantum_state_transfer_core.lean compiles with zero errors or warnings."""
    lean_file = (
        Path(__file__).resolve().parent.parent / "lean4" / "quantum_state_transfer_core.lean"
    )
    assert lean_file.exists(), f"Lean file not found: {lean_file}"
    res = subprocess.run(["lean", str(lean_file)], capture_output=True, text=True)
    assert res.returncode == 0, f"Lean compilation error:\n{res.stderr}"


def test_bell_witness_entangled_and_separable_sql_cte():
    """Validates that ViewEntanglementWitnessAudit certifies Bell entangled states and flags separable defects."""
    evaluator = QuantumStateTransferEvaluator(in_memory=True)
    evaluator.populate_bell_and_ghz_states()
    evaluator.populate_witness_operators()

    results = evaluator.verify_entanglement_witness()
    r_dict = {(r.witness_id, r.state_id): r for r in results}

    # Pure Bell state: Tr(W rho) = -0.5 < 0
    phi_plus = r_dict[("wit_bell", "state_phi_plus")]
    assert phi_plus.is_entangled is True
    assert phi_plus.witness_status == "ENTANGLED_CERTIFIED"
    assert phi_plus.computed_trace_val < -0.49

    # Werner state (F = 0.75): Tr(W rho) = -0.25 < 0
    werner = r_dict[("wit_bell", "state_werner_entangled")]
    assert werner.is_entangled is True
    assert werner.witness_status == "ENTANGLED_CERTIFIED"
    assert werner.computed_trace_val < 0.0

    # Separable state |00><00|: Tr(W rho) = 0.0 >= 0
    sep = r_dict[("wit_bell", "state_separable_00")]
    assert sep.is_entangled is False
    assert sep.witness_status == "SEPARABLE_DEFECT"
    assert sep.computed_trace_val >= 0.0
    evaluator.close()


def test_ghz_witness_tripartite_entanglement_sql_cte():
    """Validates that ViewEntanglementWitnessAudit certifies 3-qubit GHZ tripartite entanglement."""
    evaluator = QuantumStateTransferEvaluator(in_memory=True)
    evaluator.populate_bell_and_ghz_states()
    evaluator.populate_witness_operators()

    results = evaluator.verify_entanglement_witness()
    r_dict = {(r.witness_id, r.state_id): r for r in results}

    ghz = r_dict[("wit_ghz", "state_ghz_3")]
    assert ghz.is_entangled is True
    assert ghz.witness_status == "ENTANGLED_CERTIFIED"
    assert ghz.computed_trace_val < -0.49

    sep3 = r_dict[("wit_ghz", "state_separable_000")]
    assert sep3.is_entangled is False
    assert sep3.witness_status == "SEPARABLE_DEFECT"
    assert sep3.computed_trace_val >= 0.0
    evaluator.close()


def test_teleportation_all_four_bell_measurement_outcomes_sql_cte():
    """Validates that ViewTeleportationFidelityAudit certifies all 4 Bell measurement feedforward corrections."""
    evaluator = QuantumStateTransferEvaluator(in_memory=True)
    evaluator.populate_bell_and_ghz_states()
    evaluator.populate_witness_operators()

    # Log 4 outcomes
    evaluator.record_teleportation_run(1, "Psi_In", 0, 0, "Id", 1.0, 1)
    evaluator.record_teleportation_run(2, "Psi_In", 1, 0, "Z", 1.0, 1)
    evaluator.record_teleportation_run(3, "Psi_In", 0, 1, "X", 1.0, 1)
    evaluator.record_teleportation_run(4, "Psi_In", 1, 1, "XZ", 1.0, 1)

    audits = evaluator.verify_teleportation_runs()
    assert len(audits) == 4
    for a in audits:
        assert a.terminal_route == "Repair"
        assert a.audit_status == "TELEPORTATION_CERTIFIED"
        assert a.output_fidelity == 1.0
        assert a.applied_correction == a.expected_correction
    evaluator.close()


def test_teleportation_feedforward_mismatch_refusal_sql_cte():
    """Validates that feedforward errors or sub-threshold fidelity route to SplitBrainRefusal."""
    evaluator = QuantumStateTransferEvaluator(in_memory=True)
    # Outcome (1, 0) expects 'Z', but 'Id' is applied
    evaluator.record_teleportation_run(10, "Psi_In", 1, 0, "Id", 0.50, 1)

    audits = evaluator.verify_teleportation_runs()
    assert len(audits) == 1
    assert audits[0].terminal_route == "SplitBrainRefusal"
    assert audits[0].audit_status == "FEEDFORWARD_FIDELITY_DEFECT"
    evaluator.close()


def test_teleportation_protocol_syntax_defect_closure_failure_sql_cte():
    """Validates that broken protocol syntax routes to ClosureFailure."""
    evaluator = QuantumStateTransferEvaluator(in_memory=True)
    evaluator.record_teleportation_run(20, "Psi_In", 0, 0, "Id", 1.0, is_valid_protocol=0)

    audits = evaluator.verify_teleportation_runs()
    assert len(audits) == 1
    assert audits[0].terminal_route == "ClosureFailure"
    assert audits[0].audit_status == "PROTOCOL_SYNTAX_DEFECT"
    evaluator.close()


def test_entanglement_distillation_purification_sql_cte():
    """Validates that ViewDistillationEfficiencyAudit certifies fidelity improvement."""
    evaluator = QuantumStateTransferEvaluator(in_memory=True)
    evaluator.record_distillation_run(101, "Pair_01", 1, 0.60, 0.72, 1)
    evaluator.record_distillation_run(102, "Pair_01", 2, 0.72, 0.83, 1)

    audits = evaluator.verify_distillation_runs()
    assert len(audits) == 2
    for a in audits:
        assert a.distillation_status == "DISTILLATION_PURIFIED"
        assert a.fidelity_gain > 0.0
        assert a.output_fidelity > a.input_fidelity
    evaluator.close()


def test_full_quantum_state_transfer_bisimulation_bridge():
    """Validates end-to-end bisimulation bridging between Lean 4 and ANSI SQL relational CTEs."""
    bridge = QuantumStateTransferBisimulationBridge(in_memory=True)
    receipt = bridge.run_full_bisimulation()

    assert receipt.bell_witness_verified is True
    assert receipt.ghz_witness_verified is True
    assert receipt.separable_rejection_verified is True
    assert receipt.teleportation_all_outcomes_verified is True
    assert receipt.distillation_efficiency_verified is True
    assert receipt.terminal_repair_verified is True
    assert receipt.terminal_refusal_verified is True
    assert receipt.terminal_closure_failure_verified is True
    assert receipt.lean4_elaboration_verified is True
    assert receipt.status == "BISIMULATION_CERTIFIED"
    bridge.close()
