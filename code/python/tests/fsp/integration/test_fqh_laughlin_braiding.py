"""
test_fqh_laughlin_braiding.py — Integration Tests for 2D Fractional Quantum Hall Anyon Braiding.

AuthorityEffect: None.

Tests:
1. Fractional statistical exchange phase (theta_stat = pi/3) and braiding monodromy (theta_braid = 2pi/3).
2. Modular S-matrix unitarity (||S^dagger S - I|| <= 1e-12) and exact monodromy consistency.
3. 1-Cochain holonomy non-contractibility (Hol != 1.0) and strictly positive curvature Gamma_2 > 0.
4. Abelian involution pairing obstruction (Z_2 vs Z_3 order clash, Boltzmann gap Delta_qe > Delta_qh),
   yielding uncancelled defect mass Phi_1 > 0 and routing to TerminalRoute.OpenSignObstruction.
5. Trivial non-fractional control (m=1): contractible holonomy (Hol == 1, Gamma_2 == 0) -> ExactRepair.
6. GIN mode posting list resolution across quasiparticles, braiding perimeter, and fractional flux.
"""

from __future__ import annotations

import cmath
import math
from pathlib import Path
import sys
import pytest

current_dir = Path(__file__).resolve().parent
code_dir = current_dir.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from src.fsp.fqh_laughlin_braiding import (
    LaughlinStateAnyonModel,
    FQHLaughlinBraidingEngine,
    FQHAnyonAuditReceipt,
)


def test_fractional_statistical_and_braiding_phases():
    """Validates fractional statistical exchange phase pi/3 and braiding phase 2pi/3 for nu = 1/3."""
    model = LaughlinStateAnyonModel(model_id="laughlin_phases", laughlin_m=3)

    # 1. Elementary exchange phase
    theta_stat, eta_stat = model.compute_statistical_phase()
    assert pytest.approx(theta_stat, abs=1e-7) == math.pi / 3.0
    assert pytest.approx(eta_stat.real, abs=1e-7) == 0.5
    assert pytest.approx(eta_stat.imag, abs=1e-7) == 0.5 * math.sqrt(3.0)

    # 2. Full braiding monodromy (2 exchanges)
    theta_braid, eta_braid = model.compute_braiding_phase()
    assert pytest.approx(theta_braid, abs=1e-7) == 2.0 * math.pi / 3.0
    assert pytest.approx(eta_braid.real, abs=1e-7) == -0.5
    assert pytest.approx(eta_braid.imag, abs=1e-7) == 0.5 * math.sqrt(3.0)

    # Statistical phase is not +-1 (not bosonic and not fermionic)
    assert abs(eta_stat - 1.0) > 0.5
    assert abs(eta_stat - (-1.0)) > 0.5


def test_modular_s_matrix_unitarity_and_monodromy():
    """Validates m x m modular S-matrix unitarity and monodromy phase agreement."""
    model = LaughlinStateAnyonModel(model_id="laughlin_modular", laughlin_m=3)
    s_matrix, max_unitarity_err, m11 = model.compute_modular_s_matrix()

    assert len(s_matrix) == 3
    assert all(len(row) == 3 for row in s_matrix)
    assert max_unitarity_err <= 1e-12

    # Monodromy M_11 must equal exp(i * 2 pi / 3)
    theta_braid, eta_braid = model.compute_braiding_phase()
    assert pytest.approx(abs(m11 - eta_braid), abs=1e-10) == 0.0


def test_fractional_cochain_holonomy_non_contractibility():
    """Validates that anyon braiding accumulates non-contractible 1-cochain holonomy and Gamma_2 > 0."""
    model = LaughlinStateAnyonModel(model_id="laughlin_holonomy", laughlin_m=3)
    hol_real, hol_imag, is_contractible, gamma_2 = model.compute_cochain_holonomy()

    # Holonomy is exp(i * 2 pi / 3) = -0.5 + 0.866025i != 1.0
    assert pytest.approx(hol_real, abs=1e-6) == -0.5
    assert pytest.approx(hol_imag, abs=1e-6) == 0.5 * math.sqrt(3.0)
    assert is_contractible is False

    # Strictly positive cochain curvature
    assert gamma_2 == pytest.approx(2.0 * math.pi / 3.0, abs=1e-6)
    assert gamma_2 > 0.0


def test_abelian_involution_obstruction_and_open_sign_routing():
    """
    Validates that fractional anyon statistics obstruct exact abelian involution pairing,
    yielding uncancelled defect mass and routing to OpenSignObstruction.
    """
    model = LaughlinStateAnyonModel(model_id="laughlin_audit_nu_1_3", laughlin_m=3)
    engine = FQHLaughlinBraidingEngine(in_memory=True)
    try:
        receipt = engine.audit_fqh_braiding(model, beta=2.0)

        assert receipt.laughlin_m == 3
        assert receipt.filling_fraction == "1/3"
        assert receipt.is_holonomy_contractible is False
        assert receipt.cochain_curvature_gamma_2 > 0.0
        assert receipt.is_abelian_involution_obstructed is True

        # Boltzmann weight asymmetry: Delta_qe = 0.073 > Delta_qh = 0.026
        assert receipt.boltzmann_weight_quasihole > receipt.boltzmann_weight_quasielectron
        assert receipt.weight_gap_delta_w > 0.0
        assert receipt.uncancelled_defect_mass_phi_1 > 0.0

        # Deterministic BQNF routing
        assert receipt.terminal_route == "OpenSignObstruction"
    finally:
        engine.close()


def test_trivial_integer_control_m_1():
    """
    Validates that in the trivial non-fractional control (m=1),
    holonomy is contractible (Gamma_2 = 0), defect mass vanishes, and routing is ExactRepair.
    """
    model = LaughlinStateAnyonModel(
        model_id="laughlin_control_m1",
        laughlin_m=1,
        delta_qh=0.05,
        delta_qe=0.05,  # Symmetric control
    )
    engine = FQHLaughlinBraidingEngine(in_memory=True)
    try:
        receipt = engine.audit_fqh_braiding(model, beta=2.0)

        assert receipt.laughlin_m == 1
        assert receipt.is_holonomy_contractible is True
        assert receipt.cochain_curvature_gamma_2 == pytest.approx(0.0, abs=1e-6)
        assert receipt.uncancelled_defect_mass_phi_1 == pytest.approx(0.0, abs=1e-6)
        assert receipt.terminal_route == "ExactRepair"
    finally:
        engine.close()


def test_gin_mode_posting_list_resolution():
    """Validates GIN mode indexing across quasiparticles, braiding loop, and fractional flux."""
    model = LaughlinStateAnyonModel(model_id="laughlin_gin_test", laughlin_m=3)
    engine = FQHLaughlinBraidingEngine(in_memory=True)
    try:
        receipt = engine.audit_fqh_braiding(model, beta=2.0)

        c = engine.conn.cursor()
        c.execute("SELECT COUNT(*) FROM FermionConfigurations WHERE model_name = ?;", (model.model_id,))
        cfg_count = c.fetchone()[0]
        assert cfg_count == 2

        # 4 distinct modes:
        # 1: Quasihole Locus (eta_1), 2: Quasihole Locus (eta_2),
        # 3: Braiding loop boundary (gamma in Z_1), 4: Fractional flux core (Phi^* = Phi_0 / 3)
        c.execute("SELECT COUNT(DISTINCT mode_id) FROM GinModePostingList;")
        distinct_modes = c.fetchone()[0]
        assert distinct_modes == 4

        # Mode 1 occupied by quasihole configuration
        assert 1 in engine.posting_index[1]
        # Mode 2 occupied by quasielectron configuration
        assert 2 in engine.posting_index[2]
    finally:
        engine.close()
