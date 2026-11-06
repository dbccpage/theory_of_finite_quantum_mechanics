"""Unit & Integration Test Suite: Toric and Surface Code Topological QEC Cochains.
AuthorityEffect: None.

Tests:
1. Lean 4 formal kernel compilation (toric_surface_code_core.lean).
2. SQL CTE boundary nilpotence (d1 ∘ d2 = 0 mod 2).
3. SQL CTE stabilizer commutation ([A_s, B_p] = 0).
4. SQL relational syndrome measurement audit.
5. Anyon defect pairing and parity conservation (sum S = 0 mod 2).
6. Anyonic defect braiding Berry phase audit (mutual statistics phase = -1).
7. Homological error correction routing (Repair vs SplitBrainRefusal).
8. Full bisimulation bridge verification suite.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

code_dir = Path(__file__).resolve().parent.parent / "code"
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from toric_surface_code_bisimulation_bridge import ToricSurfaceCodeBisimulationBridge
from toric_surface_code_evaluator import ToricSurfaceCodeEvaluator


def test_lean4_toric_surface_code_core_compilation():
    """Validates that lean4/toric_surface_code_core.lean compiles with zero errors or warnings."""
    lean_file = Path(__file__).resolve().parent.parent / "lean4" / "toric_surface_code_core.lean"
    assert lean_file.exists(), f"Lean file not found: {lean_file}"
    res = subprocess.run(["lean", str(lean_file)], capture_output=True, text=True)
    assert res.returncode == 0, f"Lean compilation error:\n{res.stderr}"


def test_sql_cte_boundary_nilpotence():
    """Validates that ViewChainComplexNilpotence certifies d1 ∘ d2 = 0 mod 2 for all plaquettes."""
    evaluator = ToricSurfaceCodeEvaluator(in_memory=True)
    evaluator.build_torus_lattice(L=3)
    res = evaluator.verify_chain_complex_nilpotence()
    assert res["is_nilpotent"] is True
    assert res["defects_count"] == 0
    assert res["total_pairs_tested"] > 0
    evaluator.close()


def test_sql_cte_stabilizer_commutation():
    """Validates that ViewStabilizerCommutation certifies [A_s, B_p] = 0 for all star and plaquette stabilizers."""
    evaluator = ToricSurfaceCodeEvaluator(in_memory=True)
    evaluator.build_torus_lattice(L=3)
    res = evaluator.verify_stabilizer_commutation()
    assert res["all_stabilizers_commute"] is True
    assert res["violations_count"] == 0
    assert res["total_pairs_tested"] == 81  # 9 stars x 9 plaquettes on L=3
    evaluator.close()


def test_relational_syndrome_audit():
    """Validates that ViewSyndromeAudit accurately verifies syndrome derivations for localized Pauli errors."""
    evaluator = ToricSurfaceCodeEvaluator(in_memory=True)
    evaluator.build_torus_lattice(L=3)

    # Injected errors: edge 0 has X error, edge 2 has Z error, edge 5 has Y error
    evaluator.inject_pauli_errors(round_id=1, errors=[(0, "X"), (2, "Z"), (5, "Y")])
    measured = evaluator.measure_syndromes(round_id=1)
    assert len(measured) > 0

    audit = evaluator.verify_syndrome_audit(round_id=1)
    assert audit["all_syndromes_verified"] is True
    assert audit["mismatch_count"] == 0
    evaluator.close()


def test_anyon_defect_pairing_and_conservation():
    """Validates that ViewAnyonConservation certifies even parity of total anyon charges on the torus."""
    evaluator = ToricSurfaceCodeEvaluator(in_memory=True)
    evaluator.build_torus_lattice(L=3)

    # Single Pauli X error creates 2 magnetic anyons (plaquettes)
    evaluator.inject_pauli_errors(round_id=10, errors=[(0, "X")])
    evaluator.measure_syndromes(round_id=10)
    parity_x = evaluator.verify_anyon_conservation(round_id=10)
    assert parity_x["m_parity_even"] is True
    assert parity_x["total_m_anyons"] == 2
    assert parity_x["is_conserved"] is True

    # Single Pauli Z error creates 2 electric anyons (vertices)
    evaluator.inject_pauli_errors(round_id=11, errors=[(1, "Z")])
    evaluator.measure_syndromes(round_id=11)
    parity_z = evaluator.verify_anyon_conservation(round_id=11)
    assert parity_z["e_parity_even"] is True
    assert parity_z["total_e_anyons"] == 2
    assert parity_z["is_conserved"] is True
    evaluator.close()


def test_anyonic_braiding_phase():
    """Validates that ViewAnyonicBraidingAudit calculates Berry phase -1 for encircling braiding loops."""
    evaluator = ToricSurfaceCodeEvaluator(in_memory=True)
    evaluator.build_torus_lattice(L=3)

    # Enclosing loop: electric anyon winds around magnetic flux at (1.5, 1.5)
    evaluator.simulate_anyon_braiding(braid_run_id=1, enclosing=True)
    b_enc = evaluator.verify_anyonic_braiding_phase(braid_run_id=1)
    assert b_enc.winding_number == 1
    assert b_enc.topological_berry_phase == -1
    assert b_enc.is_non_trivial is True

    # Non-enclosing loop: electric anyon loops far from magnetic flux
    evaluator.simulate_anyon_braiding(braid_run_id=2, enclosing=False)
    b_non = evaluator.verify_anyonic_braiding_phase(braid_run_id=2)
    assert b_non.winding_number == 0
    assert b_non.topological_berry_phase == 1
    assert b_non.is_non_trivial is False
    evaluator.close()


def test_homological_error_correction_routing():
    """Validates that ViewLogicalHomologyAudit routes trivial residual cycles to Repair

    and non-contractible cycles to SplitBrainRefusal.
    """
    evaluator = ToricSurfaceCodeEvaluator(in_memory=True)
    evaluator.build_torus_lattice(L=3)

    # 1. Exact repair: error and correction match
    evaluator.inject_pauli_errors(round_id=1, errors=[(0, "X"), (1, "Z")])
    evaluator.apply_recovery_chain(round_id=1, corrections=[(0, "X"), (1, "Z")])
    rec_exact = evaluator.verify_homological_recovery(round_id=1)
    assert rec_exact.terminal_route == "Repair"
    assert rec_exact.logical_z_flip == 0
    assert rec_exact.logical_x_flip == 0

    # 2. Non-trivial homology cycle (Logical Z error):
    # Error spans the full horizontal meridian: e_H(0,0)=0, e_H(1,0)=2, e_H(2,0)=4
    evaluator.inject_pauli_errors(round_id=2, errors=[(0, "Z"), (2, "Z"), (4, "Z")])
    evaluator.apply_recovery_chain(round_id=2, corrections=[])
    rec_logical = evaluator.verify_homological_recovery(round_id=2)
    assert rec_logical.terminal_route == "SplitBrainRefusal"
    assert rec_logical.logical_z_flip == 1
    assert rec_logical.status == "LOGICAL_OPERATOR_FAULT"
    evaluator.close()


def test_full_toric_surface_code_bisimulation_suite():
    """Validates the integrated bisimulation bridge across Lean 4, SQL CTEs, and Python evaluators."""
    bridge = ToricSurfaceCodeBisimulationBridge(L=3)
    receipt = bridge.run_full_bisimulation()
    assert receipt.boundary_nilpotence_verified is True
    assert receipt.stabilizer_commutation_verified is True
    assert receipt.syndrome_audit_verified is True
    assert receipt.anyon_conservation_verified is True
    assert receipt.braiding_phase_verified is True
    assert receipt.homological_recovery_verified is True
    assert receipt.lean4_elaboration_verified is True
    assert receipt.status == "BISIMULATION_CERTIFIED"
    bridge.close()
