"""Unit & Integration Test Suite: Non-Abelian Anyon Fusion, Braiding & Topological Compiling.
AuthorityEffect: None.

Tests:
1. Lean 4 formal kernel compilation (nonabelian_anyon_core.lean).
2. SQL CTE Fibonacci fusion associativity audit (16 quadruples).
3. SQL CTE Ising fusion associativity audit (81 quadruples).
4. SQL CTE F-matrix involution equation consistency (F^2 = Id).
5. SQL CTE Hexagon braiding-associator consistency audit.
6. Fibonacci braid generator B_3 braid relation (sigma_1 sigma_2 sigma_1 = sigma_2 sigma_1 sigma_2).
7. Topological quantum compiling target rotation -> Repair.
8. Negative control: Excess approximation error -> SplitBrainRefusal.
9. Negative control: Non-unitary braid matrix -> SplitBrainRefusal.
10. Negative control: Invalid braid word alphabet -> ClosureFailure.
11. SQL CTE Braid matrix unitarity audit view.
12. Full bisimulation bridge verification suite.
"""

from __future__ import annotations

import cmath
import math
import subprocess
import sys
from pathlib import Path

code_dir = Path(__file__).resolve().parent.parent / "code"
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from nonabelian_anyon_bisimulation_bridge import NonAbelianAnyonFixtureChecks
from nonabelian_anyon_evaluator import NonAbelianAnyonEvaluator


def test_lean4_nonabelian_anyon_core_compilation():
    """Validates that lean4/nonabelian_anyon_core.lean compiles with zero errors or warnings."""
    lean_file = Path(__file__).resolve().parent.parent / "lean4" / "nonabelian_anyon_core.lean"
    assert lean_file.exists(), f"Lean file not found: {lean_file}"
    res = subprocess.run(["lean", str(lean_file)], capture_output=True, text=True)
    assert res.returncode == 0, f"Lean compilation error:\n{res.stderr}"


def test_fibonacci_fusion_associativity_sql_cte():
    """Validates that ViewFusionAssociativityAudit certifies all 16 Fibonacci species quadruples."""
    evaluator = NonAbelianAnyonEvaluator(in_memory=True)
    evaluator.populate_fibonacci_model()
    res = evaluator.verify_fusion_associativity("FIBONACCI")
    assert res["is_associative"] is True
    assert res["defect_count"] == 0
    assert res["quadruples_checked"] == 16
    evaluator.close()


def test_ising_fusion_associativity_sql_cte():
    """Validates that ViewFusionAssociativityAudit certifies all 81 Ising species quadruples."""
    evaluator = NonAbelianAnyonEvaluator(in_memory=True)
    evaluator.populate_ising_model()
    res = evaluator.verify_fusion_associativity("ISING")
    assert res["is_associative"] is True
    assert res["defect_count"] == 0
    assert res["quadruples_checked"] == 81
    evaluator.close()


def test_f_matrix_involution():
    """Validates that ViewFMatrixInvolutionAudit certifies F^2 = Id for Fibonacci and Ising models."""
    evaluator = NonAbelianAnyonEvaluator(in_memory=True)
    evaluator.populate_fibonacci_model()
    evaluator.populate_ising_model()

    fibo_res = evaluator.verify_f_matrix_involution("FIBONACCI")
    assert fibo_res["is_consistent"] is True
    assert fibo_res["violations_count"] == 0
    assert fibo_res["max_residual"] < 1e-10

    ising_res = evaluator.verify_f_matrix_involution("ISING")
    assert ising_res["is_consistent"] is True
    assert ising_res["violations_count"] == 0
    assert ising_res["max_residual"] < 1e-10
    evaluator.close()


def test_stored_braid_relation():
    """Validates that ViewHexagonEquationAudit audits braiding and associator sectors."""
    evaluator = NonAbelianAnyonEvaluator(in_memory=True)
    evaluator.populate_fibonacci_model()
    res = evaluator.verify_braid_relation("FIBONACCI")
    assert res["is_consistent"] is True
    assert res["sectors_checked"] > 0
    evaluator.close()


def test_fibonacci_braid_generators_braid_relation():
    """Validates that Fibonacci braid generators sigma_1 and sigma_2 satisfy B_3 braid relation:

    sigma_1 sigma_2 sigma_1 = sigma_2 sigma_1 sigma_2
    """
    evaluator = NonAbelianAnyonEvaluator(in_memory=True)
    s1, s2 = evaluator.get_fibonacci_braid_generators()

    lhs = evaluator._mat_mul_2x2(evaluator._mat_mul_2x2(s1, s2), s1)
    rhs = evaluator._mat_mul_2x2(evaluator._mat_mul_2x2(s2, s1), s2)

    diff = max(abs(lhs[r][c] - rhs[r][c]) for r in range(2) for c in range(2))
    assert diff < 1e-12, f"Braid relation defect {diff} exceeds tolerance"
    evaluator.close()


def test_topological_quantum_compiling_repair():
    """Validates that compiling a target gate within tolerance routes to Repair."""
    evaluator = NonAbelianAnyonEvaluator(in_memory=True)
    evaluator.populate_fibonacci_model()

    # Target: Phase gate R_z(-4pi/5) = diag(e^{-i 4pi/5}, e^{i 3pi/5})
    theta_1 = -4.0 * math.pi / 5.0
    theta_tau = 3.0 * math.pi / 5.0
    target_unitary = [
        [cmath.exp(1j * theta_1), 0.0j],
        [0.0j, cmath.exp(1j * theta_tau)],
    ]
    rec = evaluator.compile_topological_gate(
        target_name="PhaseRotation",
        target_unitary=target_unitary,
        candidate_words=[[1], [2], [-1], [-2]],
        tolerance=0.05,
    )
    assert rec.terminal_route == "Repair"
    assert rec.compilation_status == "TOPOLOGICAL_COMPILATION_CERTIFIED"
    assert rec.is_strictly_unitary is True
    assert rec.approximation_error < 1e-12
    evaluator.close()


def test_negative_control_excess_error_refusal():
    """Validates that candidate braid words exceeding approximation tolerance route to SplitBrainRefusal."""
    evaluator = NonAbelianAnyonEvaluator(in_memory=True)
    evaluator.populate_fibonacci_model()

    # Target: Pauli-X gate
    target_x = [
        [0.0j, 1.0 + 0j],
        [1.0 + 0j, 0.0j],
    ]
    rec = evaluator.compile_topological_gate(
        target_name="PauliX_Underrepresented",
        target_unitary=target_x,
        candidate_words=[[1], [-1]],  # Diagonal gates cannot represent Pauli-X
        tolerance=0.01,
    )
    assert rec.terminal_route == "SplitBrainRefusal"
    assert rec.compilation_status == "COMPILATION_DEFECT"
    assert rec.approximation_error > 0.01
    evaluator.close()


def test_negative_control_non_unitary_refusal():
    """Validates that non-unitary matrices route to SplitBrainRefusal."""
    evaluator = NonAbelianAnyonEvaluator(in_memory=True)
    evaluator.populate_fibonacci_model()

    non_unitary_mat = [
        [2.0 + 0j, 0.0j],
        [0.0j, 0.5 + 0j],
    ]
    rec = evaluator.record_compilation(
        target_name="NonUnitaryTest",
        braid_word=[1, 2],
        matrix=non_unitary_mat,
        approximation_error=0.01,
        tolerance=0.05,
    )
    assert rec.terminal_route == "SplitBrainRefusal"
    assert rec.is_strictly_unitary is False
    assert rec.compilation_status == "COMPILATION_DEFECT"
    evaluator.close()


def test_negative_control_invalid_braid_closure_failure():
    """Validates that invalid braid words (out-of-alphabet generator or empty) route to ClosureFailure."""
    evaluator = NonAbelianAnyonEvaluator(in_memory=True)
    evaluator.populate_fibonacci_model()

    dummy_mat = [[1.0 + 0j, 0.0j], [0.0j, 1.0 + 0j]]
    rec = evaluator.record_compilation(
        target_name="AlphabetBreachTest",
        braid_word=[999],  # 999 is not in {-2, -1, 1, 2}
        matrix=dummy_mat,
        approximation_error=0.0,
    )
    assert rec.terminal_route == "ClosureFailure"
    assert rec.compilation_status == "INVALID_BRAID_CLOSURE_FAILURE"
    evaluator.close()


def test_braid_unitarity_view_audit():
    """Validates that ViewBraidUnitarityAudit accurately identifies unitary vs non-unitary matrices."""
    evaluator = NonAbelianAnyonEvaluator(in_memory=True)
    evaluator.populate_fibonacci_model()

    id_mat = [[1.0 + 0j, 0.0j], [0.0j, 1.0 + 0j]]
    rec1 = evaluator.record_compilation("Unitary", [1], id_mat, 0.0)

    non_unitary = [[1.5 + 0j, 0.0j], [0.0j, 1.0 + 0j]]
    rec2 = evaluator.record_compilation("NonUnitary", [1], non_unitary, 0.0)

    c = evaluator.conn.cursor()
    c.execute(
        "SELECT is_strictly_unitary FROM ViewBraidUnitarityAudit WHERE compilation_id = ?;",
        (rec1.compilation_id,),
    )
    assert c.fetchone()[0] == 1

    c.execute(
        "SELECT is_strictly_unitary FROM ViewBraidUnitarityAudit WHERE compilation_id = ?;",
        (rec2.compilation_id,),
    )
    assert c.fetchone()[0] == 0
    evaluator.close()


def test_full_nonabelian_anyon_bisimulation_bridge():
    """Validates full end-to-end bisimulation bridging between Lean 4 and ANSI SQL relational CTEs."""
    bridge = NonAbelianAnyonFixtureChecks(in_memory=True)
    receipt = bridge.run_fixture_checks()

    assert receipt.fibonacci_associativity_verified is True
    assert receipt.ising_associativity_verified is True
    assert receipt.fibonacci_involution_verified is True
    assert receipt.ising_involution_verified is True
    assert receipt.fibonacci_b3_verified is True
    assert receipt.braid_unitarity_verified is True
    assert receipt.compilation_repair_verified is True
    assert receipt.compilation_refusal_verified is True
    assert receipt.compilation_closure_failure_verified is True
    assert receipt.lean4_elaboration_verified is True
    assert receipt.status == "FIXTURE_CHECKS_PASSED"
    bridge.close()
