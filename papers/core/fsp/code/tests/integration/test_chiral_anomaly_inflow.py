"""
test_chiral_anomaly_inflow.py — Integration Tests for Chiral Chemical Potential mu_5 and Anomaly Inflow.

AuthorityEffect: None.

Tests:
1. Callan-Harvey anomaly inflow conservation: Q_bulk + Q_surf == 0 throughout adiabatic spectral flow theta in [0, 2pi].
2. Chiral-symmetric limit (mu_5 = 0): Equal weights w_+ == w_-, contractible cochain holonomy (Hol == 1), vanishing defect mass (Phi_1 = 0.0) -> ExactRepair.
3. Broken chiral symmetry (mu_5 > 0): Exponential weight asymmetry w_+ / w_- = exp(2 beta mu_5) > 1, non-contractible cochain holonomy (Hol != 1), non-vanishing defect mass (Phi_1 > 0) -> SplitBrainRefusal.
4. Parametric scaling across mu_5: Monotonic defect mass growth with mu_5.
5. GIN mode posting list resolution separating chiral node modes and surface arc modes.
"""

from __future__ import annotations

import math
from pathlib import Path
import sys
import pytest

current_dir = Path(__file__).resolve().parent
code_dir = current_dir.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from chiral_anomaly_inflow import (
    WeylSlabLattice,
    ChiralAnomalyInflowEngine,
    ChiralAnomalyAuditReceipt,
)


def test_callan_harvey_anomaly_inflow_conservation():
    """Validates Callan-Harvey anomaly inflow conservation Q_bulk + Q_surf == 0 across flux insertion."""
    lattice = WeylSlabLattice(lattice_id="weyl_inflow_test", mu_5=0.0)

    n_steps = 10
    for step in range(n_steps + 1):
        theta = 2.0 * math.pi * step / n_steps
        q_bulk, q_surf, q_net = lattice.compute_spectral_flow(theta)
        assert pytest.approx(q_bulk + q_surf, abs=1e-9) == 0.0
        assert pytest.approx(q_net, abs=1e-9) == 0.0

    # At full cycle theta = 2pi: 1 unit pumped from bulk, exactly counter-balanced by surface arc
    q_bulk_2pi, q_surf_2pi, q_net_2pi = lattice.compute_spectral_flow(2.0 * math.pi)
    assert pytest.approx(q_bulk_2pi, abs=1e-7) == 1.0
    assert pytest.approx(q_surf_2pi, abs=1e-7) == -1.0
    assert pytest.approx(q_net_2pi, abs=1e-7) == 0.0


def test_chiral_symmetric_limit_mu5_zero():
    """
    Validates that at mu_5 = 0, chiral involution symmetry yields equal weights (w_+ == w_-),
    contractible cochain holonomy, and exact sign cancellation -> ExactRepair.
    """
    lattice = WeylSlabLattice(lattice_id="weyl_symmetric", mu_5=0.0)
    engine = ChiralAnomalyInflowEngine(in_memory=True)
    try:
        receipt = engine.audit_chiral_inflow(lattice, beta=2.0)

        assert receipt.mu_5 == 0.0
        assert receipt.spectral_flow_net_anomaly == 0
        assert receipt.chiral_weight_plus == pytest.approx(receipt.chiral_weight_minus, abs=1e-6)
        assert receipt.weight_gap_delta_w == pytest.approx(0.0, abs=1e-6)

        # Holonomy is strictly contractible: exp(i * 0) = 1.0 + 0.0i
        assert receipt.cochain_holonomy_real == pytest.approx(1.0, abs=1e-6)
        assert receipt.cochain_holonomy_imag == pytest.approx(0.0, abs=1e-6)
        assert receipt.is_holonomy_contractible is True

        # Exact cochain closure and defect mass vanishing
        assert receipt.uncancelled_defect_mass_phi_1 == pytest.approx(0.0, abs=1e-6)
        assert receipt.cochain_curvature_gamma_2 == pytest.approx(0.0, abs=1e-6)
        assert receipt.terminal_route == "ExactRepair"
    finally:
        engine.close()


def test_chiral_chemical_potential_broken_symmetry_mu5_positive():
    """
    Validates that at mu_5 > 0, spectral flow induces exponential weight asymmetry,
    non-contractible cochain holonomy, and non-vanishing defect mass -> SplitBrainRefusal.
    """
    # Set mu_5 = 0.25, omega_0 = 1.0 -> phase = 2pi * 0.25 = pi/2
    lattice = WeylSlabLattice(lattice_id="weyl_broken_mu5", mu_5=0.25, omega_0=1.0)
    engine = ChiralAnomalyInflowEngine(in_memory=True)
    try:
        receipt = engine.audit_chiral_inflow(lattice, beta=2.0)

        assert receipt.mu_5 == 0.25
        assert receipt.spectral_flow_net_anomaly == 0

        # Exponential weight asymmetry: w_+ / w_- = exp(2 * 2.0 * 0.25) = exp(1.0) approx 2.71828
        ratio = receipt.chiral_weight_plus / receipt.chiral_weight_minus
        assert ratio == pytest.approx(math.exp(1.0), rel=1e-4)
        assert receipt.weight_gap_delta_w > 0.0

        # Holonomy is non-contractible: exp(i * pi/2) = 0.0 + 1.0i
        assert receipt.cochain_holonomy_real == pytest.approx(0.0, abs=1e-6)
        assert receipt.cochain_holonomy_imag == pytest.approx(1.0, abs=1e-6)
        assert receipt.is_holonomy_contractible is False

        # Non-zero cochain curvature and defect mass
        assert receipt.uncancelled_defect_mass_phi_1 > 0.0
        assert receipt.cochain_curvature_gamma_2 == pytest.approx(0.5 * math.pi, rel=1e-4)

        # Exact sign cancellation broken -> SplitBrainRefusal
        assert receipt.terminal_route == "SplitBrainRefusal"
    finally:
        engine.close()


def test_parametric_scaling_with_mu5():
    """Validates monotonic defect mass growth as chiral chemical potential mu_5 increases."""
    beta = 1.5
    engine = ChiralAnomalyInflowEngine(in_memory=True)
    try:
        prev_defect = -1.0
        for mu5 in (0.0, 0.1, 0.2, 0.3, 0.5):
            lattice = WeylSlabLattice(lattice_id=f"weyl_scale_{mu5}", mu_5=mu5)
            receipt = engine.audit_chiral_inflow(lattice, beta=beta)
            assert receipt.uncancelled_defect_mass_phi_1 > prev_defect
            prev_defect = receipt.uncancelled_defect_mass_phi_1
            if mu5 == 0.0:
                assert receipt.terminal_route == "ExactRepair"
            else:
                assert receipt.terminal_route == "SplitBrainRefusal"
    finally:
        engine.close()


def test_gin_mode_posting_list_chiral_resolution():
    """Validates GIN mode indexing of chiral bulk nodes and surface arc channels."""
    lattice = WeylSlabLattice(lattice_id="weyl_gin_test", mu_5=0.2)
    engine = ChiralAnomalyInflowEngine(in_memory=True)
    try:
        receipt = engine.audit_chiral_inflow(lattice, beta=2.0)

        c = engine.conn.cursor()
        c.execute("SELECT COUNT(*) FROM FermionConfigurations WHERE model_name = ?;", (lattice.lattice_id,))
        cfg_count = c.fetchone()[0]
        assert cfg_count == 2

        # 4 distinct modes: 1 (Node_R), 2 (Node_L), 3 (Arc_Top), 4 (Arc_Bottom)
        c.execute("SELECT COUNT(DISTINCT mode_id) FROM GinModePostingList;")
        distinct_modes = c.fetchone()[0]
        assert distinct_modes == 4

        # Mode 1 occupied only by cfg 1 (positive chirality)
        assert 1 in engine.posting_index[1]
        assert 2 not in engine.posting_index[1]

        # Mode 2 occupied only by cfg 2 (negative chirality)
        assert 2 in engine.posting_index[2]
        assert 1 not in engine.posting_index[2]
    finally:
        engine.close()
