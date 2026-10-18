"""
test_ising_majorana_braiding.py — Integration tests for non-abelian Ising anyon / Majorana braiding,
Clifford group stability, non-Clifford T-gate injection, and magic state defects.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e)
"""

from __future__ import annotations

import math
from pathlib import Path
import sys

import pytest

code_dir = Path(__file__).resolve().parent.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from src.fsp.ising_majorana_braiding import IsingMajoranaBraidingEngine, IsingMajoranaModel


def test_ising_quantum_dimensions_and_fusion() -> None:
    """Verifies Ising anyon quantum dimensions and total quantum dimension D = 2."""
    model = IsingMajoranaModel()
    d_1, d_psi, d_sigma, total_d = model.compute_quantum_dimensions()

    assert abs(d_1 - 1.0) < 1e-12
    assert abs(d_psi - 1.0) < 1e-12
    assert abs(d_sigma - math.sqrt(2.0)) < 1e-12
    assert abs(total_d - 2.0) < 1e-12


def test_clifford_braid_pauli_conjugation_closure() -> None:
    """Verifies that Clifford braid generators H and S preserve the Pauli group under conjugation."""
    model = IsingMajoranaModel()
    is_closed, max_dist = model.verify_clifford_closure()

    assert is_closed
    assert max_dist < 1e-12


def test_clifford_sign_free_stabilizer_repair() -> None:
    """Verifies that pure Clifford braiding circuits preserve stabilizer parity and route to ExactRepair."""
    model = IsingMajoranaModel()
    engine = IsingMajoranaBraidingEngine(in_memory=True)
    receipt = engine.audit_majorana_braiding(model, inject_t_gate=False)
    engine.close()

    assert receipt.is_clifford_closed
    assert receipt.is_stabilizer_preserved
    assert abs(receipt.bloch_vector_l1_norm - 1.0) < 1e-12
    assert receipt.robustness_of_magic == 0.0
    assert receipt.wigner_negativity == 0.0
    assert receipt.cochain_curvature_gamma_2 == 0.0
    assert receipt.is_holonomy_contractible
    assert receipt.uncancelled_defect_mass_phi_1 == 0.0
    assert receipt.terminal_route == "ExactRepair"


def test_t_gate_pauli_violation() -> None:
    """Verifies that T-gate conjugation T X T^dagger breaks Pauli closure."""
    model = IsingMajoranaModel()
    pauli_dist = model.compute_t_gate_pauli_violation()

    assert pauli_dist > 1.0
    assert abs(pauli_dist - 1.082392) < 1e-3


def test_magic_state_wigner_negativity_and_defect() -> None:
    """Verifies Bloch vector L1 norm = sqrt(2) and non-vanishing Wigner negativity for magic state |T>."""
    model = IsingMajoranaModel()
    bloch_l1, robustness, wigner_neg = model.compute_state_bloch_and_magic(use_t_gate=True)

    expected_l1 = math.sqrt(2.0)
    expected_robustness = math.sqrt(2.0) - 1.0
    expected_neg = expected_robustness / 2.0

    assert abs(bloch_l1 - expected_l1) < 1e-12
    assert abs(robustness - expected_robustness) < 1e-12
    assert abs(wigner_neg - expected_neg) < 1e-12


def test_non_stabilizer_cochain_holonomy_and_curvature() -> None:
    """Verifies non-contractibility of non-Clifford loop holonomy and positive curvature Gamma_2."""
    model = IsingMajoranaModel()
    dist, is_contractible, gamma_2 = model.compute_cochain_holonomy(use_t_gate=True)

    assert not is_contractible
    assert dist > 0.75
    assert gamma_2 > 0.75
    assert abs(dist - 0.765367) < 1e-3


def test_t_gate_open_sign_obstruction_routing() -> None:
    """Verifies that T-gate injection routes deterministically to OpenSignObstruction."""
    model = IsingMajoranaModel()
    engine = IsingMajoranaBraidingEngine(in_memory=True)
    receipt = engine.audit_majorana_braiding(model, inject_t_gate=True)
    engine.close()

    assert not receipt.is_stabilizer_preserved
    assert not receipt.is_holonomy_contractible
    assert receipt.robustness_of_magic > 0.4
    assert receipt.wigner_negativity > 0.2
    assert receipt.cochain_curvature_gamma_2 > 0.7
    assert receipt.uncancelled_defect_mass_phi_1 > 0.9
    assert receipt.terminal_route == "OpenSignObstruction"


def test_gin_mode_posting_list_resolution() -> None:
    """Verifies relational SQLite GIN mode posting list queries."""
    model = IsingMajoranaModel()
    engine = IsingMajoranaBraidingEngine(in_memory=True)
    receipt = engine.audit_majorana_braiding(model, inject_t_gate=True)

    # Check posting index contains expected modes
    assert 1 in engine.posting_index  # Vacuum parity channel |0>
    assert 2 in engine.posting_index  # Occupied parity channel |1>
    assert 3 in engine.posting_index  # tau_1 loop (Phase gate)
    assert 4 in engine.posting_index  # tau_2 loop (Hadamard generator)
    assert 5 in engine.posting_index  # T-gate injection loop

    # Query SQLite database directly
    c = engine.conn.cursor()
    c.execute("SELECT COUNT(*) FROM FermionConfigurations WHERE model_name = ?;", (model.model_id,))
    cfg_count = c.fetchone()[0]
    assert cfg_count == 2

    c.execute("SELECT COUNT(*) FROM GinModePostingList WHERE mode_id = 5;")
    t_gate_mode_count = c.fetchone()[0]
    assert t_gate_mode_count == 2  # Both configurations share the non-Clifford injection boundary

    engine.close()
