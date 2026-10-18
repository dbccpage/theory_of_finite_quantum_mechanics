"""
Integration tests for 4D Instanton-Dyon Gas Expansions and Monopole Loop Braiding.

Paper: 002_projection_obstruction/023_fermion_sign_and_computational_hardness
Test: test_instanton_dyon_gas_braiding.py
AuthorityEffect: None
"""

import math
from pathlib import Path
import sys
import numpy as np
import pytest

code_dir = Path(__file__).resolve().parent.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from src.fsp.instanton_dyon_gas_braiding import (
    DyonEnsemble,
    DyonGasBuilder,
    DyonGasConfig,
    DyonParticle,
    DyonType,
    GasRegime,
    InstantonDyonEngine,
    MonopoleLoopBraiding,
    TerminalRoute,
)


@pytest.fixture
def default_config() -> DyonGasConfig:
    return DyonGasConfig(
        g_coupling=1.0,
        nu_holonomy=0.5,
        theta_angle=math.pi,
        temperature=1.0,
        core_radius=0.2
    )


@pytest.fixture
def engine(default_config: DyonGasConfig) -> InstantonDyonEngine:
    return InstantonDyonEngine(default_config)


def test_kvbll_fractional_topological_charge_and_action_conservation(default_config: DyonGasConfig):
    """KvBLL caloron constituent dyons partition topological charge and action."""
    p_m = DyonGasBuilder.create_dyon(1, DyonType.M_DYON, (0, 0, 0), default_config)
    p_l = DyonGasBuilder.create_dyon(2, DyonType.L_DYON, (0, 0, 0), default_config)

    assert p_m.magnetic_charge == +1
    assert p_l.magnetic_charge == -1
    assert math.isclose(p_m.topological_charge, 0.5, abs_tol=1e-12)
    assert math.isclose(p_l.topological_charge, 0.5, abs_tol=1e-12)

    total_q = p_m.topological_charge + p_l.topological_charge
    assert math.isclose(total_q, 1.0, abs_tol=1e-12)

    s_0 = (8.0 * math.pi ** 2) / (default_config.g_coupling ** 2)
    assert math.isclose(p_m.core_action + p_l.core_action, s_0, abs_tol=1e-12)

    p_m_bar = DyonGasBuilder.create_dyon(3, DyonType.M_BAR, (0, 0, 0), default_config)
    p_l_bar = DyonGasBuilder.create_dyon(4, DyonType.L_BAR, (0, 0, 0), default_config)
    assert p_m_bar.magnetic_charge == -1
    assert p_l_bar.magnetic_charge == +1
    assert math.isclose(p_m_bar.topological_charge, -0.5, abs_tol=1e-12)
    assert math.isclose(p_l_bar.topological_charge, -0.5, abs_tol=1e-12)


def test_dyon_coulomb_interaction_and_dipole_binding(default_config: DyonGasConfig):
    """Opposite magnetic charges attract (V < 0) and like charges repel (V > 0)."""
    p_m1 = DyonGasBuilder.create_dyon(1, DyonType.M_DYON, (0, 0, 0.5), default_config)
    p_m2 = DyonGasBuilder.create_dyon(2, DyonType.M_DYON, (0, 0, -0.5), default_config)
    p_m_bar = DyonGasBuilder.create_dyon(3, DyonType.M_BAR, (0, 0, -0.5), default_config)

    ensemble = DyonEnsemble(particles=[p_m1, p_m2, p_m_bar], config=default_config)

    v_repulsive = ensemble.pair_coulomb_potential(p_m1, p_m2)
    v_attractive = ensemble.pair_coulomb_potential(p_m1, p_m_bar)

    assert v_repulsive > 0.0, "Like magnetic charges must repel"
    assert v_attractive < 0.0, "Opposite magnetic charges must attract"
    assert math.isclose(v_repulsive, -v_attractive, abs_tol=1e-12)


def test_molecular_cluster_involution_pairing_exact_repair(engine: InstantonDyonEngine):
    """Neutral dipole molecular cluster admits exact involution pairing and routes to EXACT_REPAIR."""
    audit = engine.audit_molecular_cluster_regime(separation=0.5)

    assert audit["regime"] == GasRegime.MOLECULAR_CLUSTER.value
    assert audit["net_topological_charge"] == 0.0
    assert audit["net_magnetic_charge"] == 0
    assert math.isclose(audit["action_difference"], 0.0, abs_tol=1e-12)
    assert audit["defect_mass_phi1"] == 0.0
    assert audit["cochain_curvature_gamma2"] == 0.0
    assert audit["average_sign_recovered"] == 1.0
    assert audit["terminal_route"] == TerminalRoute.EXACT_REPAIR.value


def test_neutral_caloron_quartet_invariance(default_config: DyonGasConfig, engine: InstantonDyonEngine):
    """Neutral caloron quartet (M, M̄, L, L̄) preserves action under dyonic involution."""
    quartet = DyonGasBuilder.build_neutral_caloron_quartet(center=(0, 0, 0), d=0.6, config=default_config)
    inv_quartet = engine.dyonic_involution_transform(quartet)

    assert quartet.net_topological_charge == 0.0
    assert quartet.net_magnetic_charge == 0
    s1 = quartet.compute_total_action()
    s2 = inv_quartet.compute_total_action()
    assert math.isclose(s1, s2, abs_tol=1e-12)


def test_ionized_plasma_action_gap_and_split_brain_refusal(engine: InstantonDyonEngine):
    """Ionized plasma creates Coulomb action gap ΔS > 0 and routes to SPLIT_BRAIN_REFUSAL."""
    audit = engine.audit_ionized_plasma_regime(num_dyons=6, box_size=4.0)

    assert audit["regime"] == GasRegime.IONIZED_PLASMA.value
    assert audit["action_gap"] > 0.0
    assert audit["supports_disjoint"] is True
    assert audit["defect_mass_phi1"] > 0.0
    assert audit["cochain_curvature_gamma2"] > 0.0
    assert audit["terminal_route"] == TerminalRoute.SPLIT_BRAIN_REFUSAL.value


def test_monopole_loop_gauss_linking_and_unlinking():
    """Calculates Gauss linking integral for linked vs unlinked loops."""
    u1, u2 = MonopoleLoopBraiding.build_unlinked_loops(radius=1.0, num_points=64)
    lk_unlinked = MonopoleLoopBraiding.compute_gauss_linking(u1, u2)
    assert abs(lk_unlinked) < 0.05, f"Unlinked loops should have Lk ≈ 0, got {lk_unlinked}"
    phase_unlinked = MonopoleLoopBraiding.compute_dirac_aharonov_bohm_phase(lk_unlinked)
    assert phase_unlinked == 1.0

    h1, h2 = MonopoleLoopBraiding.build_hopf_link(radius=1.0, num_points=64)
    lk_linked = MonopoleLoopBraiding.compute_gauss_linking(h1, h2)
    assert abs(abs(lk_linked) - 1.0) < 0.05, f"Hopf link should have |Lk| ≈ 1, got {lk_linked}"
    phase_linked = MonopoleLoopBraiding.compute_dirac_aharonov_bohm_phase(lk_linked)
    assert phase_linked == -1.0


def test_monopole_loop_braiding_open_sign_obstruction(engine: InstantonDyonEngine):
    """Monopole loop braiding with center vortices yields Lk=1, Dirac phase -1, and OPEN_SIGN_OBSTRUCTION."""
    audit = engine.audit_monopole_loop_braiding(num_points=64)

    assert audit["regime"] == GasRegime.MONOPOLE_BRAIDING.value
    assert audit["rounded_linking"] in (-1, 1)
    assert audit["dirac_aharonov_bohm_phase"] == -1.0
    assert audit["monopole_matrix_trace"] == -2.0
    assert audit["defect_mass_phi1"] == 2.0
    assert math.isclose(audit["cochain_curvature_gamma2"], math.pi, abs_tol=1e-12)
    assert audit["terminal_route"] == TerminalRoute.OPEN_SIGN_OBSTRUCTION.value


def test_complete_three_regime_trichotomy(engine: InstantonDyonEngine):
    """Verifies the complete three-regime classification trichotomy."""
    full_audit = engine.audit_complete_instanton_dyon_system()
    routes = full_audit["summary_routes"]

    assert routes["molecular_cluster"] == TerminalRoute.EXACT_REPAIR.value
    assert routes["ionized_plasma"] == TerminalRoute.SPLIT_BRAIN_REFUSAL.value
    assert routes["monopole_braiding"] == TerminalRoute.OPEN_SIGN_OBSTRUCTION.value
