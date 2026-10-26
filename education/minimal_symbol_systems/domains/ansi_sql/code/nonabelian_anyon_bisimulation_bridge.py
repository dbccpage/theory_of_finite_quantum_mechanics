"""Finite anyon-model fixture checks and independent Lean elaboration.
AuthorityEffect: None.

Fixture comparisons for fusion counts, F-matrix involution and the B3 relation.
Lean elaboration is checked separately. No SQL-to-Lean bisimulation theorem,
full pentagon equation or full hexagon equation is established.
"""

from __future__ import annotations

import cmath
import math
import subprocess
from dataclasses import dataclass
from pathlib import Path

from nonabelian_anyon_evaluator import (
    NonAbelianAnyonEvaluator,
)


@dataclass(frozen=True)
class NonAbelianFixtureReceipt:
    receipt_id: str
    fibonacci_associativity_verified: bool
    ising_associativity_verified: bool
    fibonacci_involution_verified: bool
    ising_involution_verified: bool
    fibonacci_b3_verified: bool
    braid_unitarity_verified: bool
    compilation_repair_verified: bool
    compilation_refusal_verified: bool
    compilation_closure_failure_verified: bool
    lean4_elaboration_verified: bool
    status: str


class NonAbelianAnyonFixtureChecks:
    """Runs finite SQL/Python fixture checks; legacy module filename retained."""

    def __init__(self, in_memory: bool = True):
        self.evaluator = NonAbelianAnyonEvaluator(in_memory=in_memory)
        self.evaluator.populate_fibonacci_model()
        self.evaluator.populate_ising_model()

    def verify_lean4_kernel(self) -> bool:
        """Verifies that lean4/nonabelian_anyon_core.lean elaborates cleanly."""
        lean_path = Path(__file__).resolve().parent.parent / "lean4" / "nonabelian_anyon_core.lean"
        if not lean_path.exists():
            return False
        res = subprocess.run(["lean", str(lean_path)], capture_output=True, text=True)
        return res.returncode == 0

    def run_fixture_checks(self) -> NonAbelianFixtureReceipt:
        """Runs fixture checks and separately records Lean elaboration."""
        # 1. Fibonacci Fusion Associativity Audit (16 quadruples)
        fibo_assoc = self.evaluator.verify_fusion_associativity("FIBONACCI")
        assert fibo_assoc["is_associative"], (
            "Fibonacci fusion associativity audit failed in SQL CTE"
        )
        assert fibo_assoc["quadruples_checked"] == 16, (
            f"Expected 16 quadruples, got {fibo_assoc['quadruples_checked']}"
        )

        # 2. Ising Fusion Associativity Audit (81 quadruples)
        ising_assoc = self.evaluator.verify_fusion_associativity("ISING")
        assert ising_assoc["is_associative"], "Ising fusion associativity audit failed in SQL CTE"
        assert ising_assoc["quadruples_checked"] == 81, (
            f"Expected 81 quadruples, got {ising_assoc['quadruples_checked']}"
        )

        # 3. F-matrix involution Consistency (F^2 = Id)
        fibo_pent = self.evaluator.verify_f_matrix_involution("FIBONACCI")
        assert fibo_pent["is_consistent"], (
            f"Fibonacci involution condition violated: residual {fibo_pent['max_residual']}"
        )

        ising_pent = self.evaluator.verify_f_matrix_involution("ISING")
        assert ising_pent["is_consistent"], (
            f"Ising involution condition violated: residual {ising_pent['max_residual']}"
        )

        # 4. Stored-matrix B3 relation
        fibo_hex = self.evaluator.verify_braid_relation("FIBONACCI")
        assert fibo_hex["is_consistent"], "Fibonacci B3 relation audit failed in SQL CTE"

        # 5. Topological Gate Compiling: Single-qubit rotation -> Repair
        # Target: Phase gate R_z(-4pi/5) = diag(e^{-i 4pi/5}, e^{i 3pi/5})
        theta_1 = -4.0 * math.pi / 5.0
        theta_tau = 3.0 * math.pi / 5.0
        target_phase_gate = [
            [cmath.exp(1j * theta_1), 0.0j],
            [0.0j, cmath.exp(1j * theta_tau)],
        ]
        # Braid words: [1] generates target_phase_gate exactly
        rec_repair = self.evaluator.compile_topological_gate(
            target_name="PhaseGate_sigma1",
            target_unitary=target_phase_gate,
            candidate_words=[[1], [2], [-1], [-2]],
            tolerance=0.05,
        )
        assert rec_repair.terminal_route == "Repair", (
            f"Expected Repair, got {rec_repair.terminal_route}"
        )
        assert rec_repair.approximation_error < 1e-9, (
            f"Expected exact compilation, error {rec_repair.approximation_error}"
        )

        # 6. Negative Control 1: Compilation Distance Excess -> SplitBrainRefusal
        # Target Hadamard gate with high tolerance threshold breached
        inv_sqrt2 = 1.0 / math.sqrt(2.0)
        target_hadamard = [
            [inv_sqrt2 + 0j, inv_sqrt2 + 0j],
            [inv_sqrt2 + 0j, -inv_sqrt2 + 0j],
        ]
        rec_refusal = self.evaluator.compile_topological_gate(
            target_name="Hadamard_ShortWord_ExcessError",
            target_unitary=target_hadamard,
            candidate_words=[[1], [-1]],  # Short word cannot approximate Hadamard within 0.01
            tolerance=0.01,
        )
        assert rec_refusal.terminal_route == "SplitBrainRefusal", (
            f"Expected SplitBrainRefusal, got {rec_refusal.terminal_route}"
        )

        # 7. Negative Control 2: Invalid Braid Word (alphabet violation) -> ClosureFailure
        dummy_mat = [[1.0 + 0j, 0j], [0j, 1.0 + 0j]]
        rec_closure = self.evaluator.record_compilation(
            target_name="InvalidBraid_AlphabetBreach",
            braid_word=[99, -42],  # Not in {-2, -1, 1, 2}
            matrix=dummy_mat,
            approximation_error=0.0,
            model="FIBONACCI",
        )
        assert rec_closure.terminal_route == "ClosureFailure", (
            f"Expected ClosureFailure, got {rec_closure.terminal_route}"
        )

        # 8. Braid Matrix Unitarity Audit across ViewBraidUnitarityAudit
        c = self.evaluator.conn.cursor()
        c.execute(
            "SELECT COUNT(*) FROM ViewBraidUnitarityAudit WHERE compilation_id = ? AND is_strictly_unitary = 1;",
            (rec_repair.compilation_id,),
        )
        repair_unitary = c.fetchone()[0] == 1

        # 9. Lean 4 Kernel Elaboration
        lean_ok = self.verify_lean4_kernel()

        return NonAbelianFixtureReceipt(
            receipt_id="nonabelian_anyon_bisim_v1",
            fibonacci_associativity_verified=fibo_assoc["is_associative"],
            ising_associativity_verified=ising_assoc["is_associative"],
            fibonacci_involution_verified=fibo_pent["is_consistent"],
            ising_involution_verified=ising_pent["is_consistent"],
            fibonacci_b3_verified=fibo_hex["is_consistent"],
            braid_unitarity_verified=repair_unitary,
            compilation_repair_verified=(rec_repair.terminal_route == "Repair"),
            compilation_refusal_verified=(rec_refusal.terminal_route == "SplitBrainRefusal"),
            compilation_closure_failure_verified=(rec_closure.terminal_route == "ClosureFailure"),
            lean4_elaboration_verified=lean_ok,
            status="FIXTURE_CHECKS_PASSED" if lean_ok and repair_unitary else "FIXTURE_CHECKS_FAILED",
        )

    def close(self) -> None:
        self.evaluator.close()
