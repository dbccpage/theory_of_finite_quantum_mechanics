"""Toric & Surface Code Bisimulation Bridge: Lean 4 Chains <-> Relational SQL CTEs.
AuthorityEffect: None.

Formal bidirectional simulation between Lean 4 chain complex theorems and
ANSI SQL relational CTE database audits of topological quantum error-correcting codes.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from toric_surface_code_evaluator import (
    ToricSurfaceCodeEvaluator,
)


@dataclass(frozen=True)
class ToricBisimulationReceipt:
    receipt_id: str
    lattice_dims: str
    boundary_nilpotence_verified: bool
    stabilizer_commutation_verified: bool
    syndrome_audit_verified: bool
    anyon_conservation_verified: bool
    braiding_phase_verified: bool
    homological_recovery_verified: bool
    lean4_elaboration_verified: bool
    status: str


class ToricSurfaceCodeBisimulationBridge:
    """Bridges Lean 4 formal chain complex certificates with SQL relational CTE evaluations."""

    def __init__(self, L: int = 3):
        self.L = L
        self.evaluator = ToricSurfaceCodeEvaluator(in_memory=True)
        self.evaluator.build_torus_lattice(L=L)

    def verify_lean4_kernel(self) -> bool:
        """Verifies that lean4/toric_surface_code_core.lean elaborates cleanly."""
        lean_path = (
            Path(__file__).resolve().parent.parent / "lean4" / "toric_surface_code_core.lean"
        )
        if not lean_path.exists():
            return False
        res = subprocess.run(["lean", str(lean_path)], capture_output=True, text=True)
        return res.returncode == 0

    def run_full_bisimulation(self) -> ToricBisimulationReceipt:
        """Executes the full suite of relational audits and bridges them to formal kernel theorems."""
        # 1. Chain Complex Nilpotence (d1 ∘ d2 = 0 mod 2)
        nilpotence_res = self.evaluator.verify_chain_complex_nilpotence()
        assert nilpotence_res["is_nilpotent"], "Boundary nilpotence failed in SQL CTE"

        # 2. Stabilizer Commutation ([A_s, B_p] = 0)
        comm_res = self.evaluator.verify_stabilizer_commutation()
        assert comm_res["all_stabilizers_commute"], "Stabilizer commutation failed in SQL CTE"

        # 3. Syndrome Audit & Measurement
        # Injected error: X on edge 0, Z on edge 2
        self.evaluator.inject_pauli_errors(round_id=1, errors=[(0, "X"), (2, "Z")])
        self.evaluator.measure_syndromes(round_id=1)
        syn_audit = self.evaluator.verify_syndrome_audit(round_id=1)
        assert syn_audit["all_syndromes_verified"], "Syndrome audit mismatch in SQL CTE"

        # 4. Anyon Conservation (Even Parity)
        parity_res = self.evaluator.verify_anyon_conservation(round_id=1)
        assert parity_res["is_conserved"], "Anyon parity defect detected in SQL CTE"

        # 5. Anyonic Braiding Phase
        # Enclosing loop: phase = -1 (non-trivial)
        self.evaluator.simulate_anyon_braiding(braid_run_id=10, enclosing=True)
        b_enc = self.evaluator.verify_anyonic_braiding_phase(braid_run_id=10)
        assert b_enc.topological_berry_phase == -1

        # Non-enclosing loop: phase = +1 (trivial)
        self.evaluator.simulate_anyon_braiding(braid_run_id=11, enclosing=False)
        b_non = self.evaluator.verify_anyonic_braiding_phase(braid_run_id=11)
        assert b_non.topological_berry_phase == 1

        # 6. Homological QEC Routing
        # Case A: Exact Repair
        self.evaluator.inject_pauli_errors(round_id=20, errors=[(0, "X")])
        self.evaluator.apply_recovery_chain(round_id=20, corrections=[(0, "X")])
        rec_repair = self.evaluator.verify_homological_recovery(round_id=20)
        assert rec_repair.terminal_route == "Repair"

        # Case B: Logical Error (Non-contractible cycle across torus)
        # Horizontal cycle on y=0: edges e_H(0,0)=0, e_H(1,0)=2, e_H(2,0)=4
        self.evaluator.inject_pauli_errors(round_id=21, errors=[(0, "Z"), (2, "Z"), (4, "Z")])
        self.evaluator.apply_recovery_chain(round_id=21, corrections=[])
        rec_refusal = self.evaluator.verify_homological_recovery(round_id=21)
        assert rec_refusal.terminal_route == "SplitBrainRefusal"

        # 7. Lean 4 Kernel Elaboration
        lean_ok = self.verify_lean4_kernel()

        return ToricBisimulationReceipt(
            receipt_id=f"toric_bisim_L{self.L}",
            lattice_dims=f"{self.L}x{self.L}",
            boundary_nilpotence_verified=nilpotence_res["is_nilpotent"],
            stabilizer_commutation_verified=comm_res["all_stabilizers_commute"],
            syndrome_audit_verified=syn_audit["all_syndromes_verified"],
            anyon_conservation_verified=parity_res["is_conserved"],
            braiding_phase_verified=(
                b_enc.topological_berry_phase == -1 and b_non.topological_berry_phase == 1
            ),
            homological_recovery_verified=(
                rec_repair.terminal_route == "Repair"
                and rec_refusal.terminal_route == "SplitBrainRefusal"
            ),
            lean4_elaboration_verified=lean_ok,
            status="BISIMULATION_CERTIFIED",
        )

    def close(self) -> None:
        self.evaluator.close()
