"""
test_bf_topological_braiding.py — Integration tests for 3D topological BF theory,
Gauss linking numbers, higher-dimensional loop braiding holonomies, and GIN mode indexing.

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

from src.fsp.bf_topological_braiding import BFTopologicalBraidingEngine, BFTopologicalModel


def test_gauss_linking_hopf_link() -> None:
    """Verifies that Gauss linking integral evaluates to +1 for Hopf link, -1 for reversed, and 0 for unlinked."""
    model = BFTopologicalModel(num_loop_points=120)
    c1, c2_linked, c2_rev, c2_unlinked = model.generate_hopf_link_geometry()

    lk_linked = model.compute_gauss_linking_number(c1, c2_linked)
    lk_rev = model.compute_gauss_linking_number(c1, c2_rev)
    lk_unlinked = model.compute_gauss_linking_number(c1, c2_unlinked)

    assert abs(lk_linked - 1.0) < 5e-3
    assert abs(lk_rev - (-1.0)) < 5e-3
    assert abs(lk_unlinked) < 1e-6
    assert round(lk_linked) == 1
    assert round(lk_rev) == -1
    assert round(lk_unlinked) == 0


def test_bf_statistical_phase_and_holonomy_z2() -> None:
    """Verifies that for Z_2 BF theory (K=2), Hopf link produces theta_BF = pi, Hol = -1, and Gamma_2 = 2.0."""
    model = BFTopologicalModel(level_k=2)
    theta_bf, hol, gamma_2 = model.evaluate_loop_phase_and_holonomy(lk=1)

    assert abs(theta_bf - math.pi) < 1e-12
    assert abs(hol.real - (-1.0)) < 1e-12
    assert abs(hol.imag) < 1e-12
    assert abs(gamma_2 - 2.0) < 1e-12


def test_bf_statistical_phase_and_holonomy_z3() -> None:
    """Verifies that for Z_3 BF theory (K=3), Hopf link produces theta_BF = 2pi/3 and Gamma_2 = sqrt(3)."""
    model = BFTopologicalModel(level_k=3)
    theta_bf, hol, gamma_2 = model.evaluate_loop_phase_and_holonomy(lk=1)

    assert abs(theta_bf - 2.0 * math.pi / 3.0) < 1e-12
    assert abs(hol.real - (-0.5)) < 1e-12
    assert abs(hol.imag - math.sqrt(3.0) / 2.0) < 1e-12
    assert abs(gamma_2 - math.sqrt(3.0)) < 1e-12


def test_unlinked_loops_contractible_holonomy() -> None:
    """Verifies that unlinked loops (Lk=0) have contractible holonomy and route to ExactRepair."""
    model = BFTopologicalModel(level_k=2)
    engine = BFTopologicalBraidingEngine(in_memory=True)
    receipt = engine.audit_bf_braiding(model, test_unlinked=True)
    engine.close()

    assert receipt.linking_number == 0
    assert receipt.statistical_phase_radians == 0.0
    assert abs(receipt.cochain_holonomy_real - 1.0) < 1e-12
    assert abs(receipt.cochain_holonomy_imag) < 1e-12
    assert receipt.cochain_curvature_gamma_2 == 0.0
    assert receipt.is_holonomy_contractible
    assert receipt.uncancelled_defect_mass_phi_1 == 0.0
    assert receipt.average_sign == 1.0
    assert receipt.terminal_route == "ExactRepair"


def test_orientation_symmetric_parity_cancellation() -> None:
    """Verifies that in an orientation-symmetric ensemble (mu_L=0), parity pairing cancels imaginary phase but preserves real obstruction."""
    model = BFTopologicalModel(level_k=3, mu_l=0.0)
    engine = BFTopologicalBraidingEngine(in_memory=True)
    receipt = engine.audit_bf_braiding(model, is_chiral=False, is_z2_energy_split=False)
    engine.close()

    assert receipt.is_orientation_symmetric
    assert receipt.weight_asymmetry_delta_w == 0.0
    # Parity cancels imaginary phase (sin theta -> 0), but real holonomy is cos(2pi/3) = -0.5 != 1
    assert not receipt.is_exact_parity_paired
    assert abs(receipt.average_sign - (-0.5)) < 1e-12
    assert receipt.uncancelled_defect_mass_phi_1 > 0.0
    assert receipt.terminal_route == "OpenSignObstruction"


def test_chiral_asymmetry_open_sign_obstruction() -> None:
    """Verifies that non-zero linking potential mu_L > 0 breaks parity pairing and routes to OpenSignObstruction."""
    model = BFTopologicalModel(level_k=3, beta=1.0, mu_l=0.5)
    engine = BFTopologicalBraidingEngine(in_memory=True)
    receipt = engine.audit_bf_braiding(model, is_chiral=True)
    engine.close()

    expected_delta_w = abs(math.exp(0.5) - math.exp(-0.5))
    assert not receipt.is_orientation_symmetric
    assert abs(receipt.weight_asymmetry_delta_w - expected_delta_w) < 1e-6
    assert not receipt.is_exact_parity_paired
    assert receipt.uncancelled_defect_mass_phi_1 > 0.0
    assert receipt.terminal_route == "OpenSignObstruction"


def test_z2_link_energy_cost_open_sign_obstruction() -> None:
    """Verifies that in Z_2 BF theory, finite link creation cost Delta E > 0 depresses average sign."""
    model = BFTopologicalModel(level_k=2, beta=1.0, delta_e_link=1.2)
    engine = BFTopologicalBraidingEngine(in_memory=True)
    receipt = engine.audit_bf_braiding(model, is_z2_energy_split=True)
    engine.close()

    expected_avg_sign = math.tanh(1.2 / 2.0)
    assert abs(receipt.average_sign - expected_avg_sign) < 1e-6
    assert receipt.average_sign < 1.0
    assert receipt.cochain_curvature_gamma_2 == 2.0
    assert receipt.uncancelled_defect_mass_phi_1 > 0.0
    assert receipt.terminal_route == "OpenSignObstruction"


def test_gin_relational_schema_and_views() -> None:
    """Verifies relational SQLite GIN mode posting tables and involution pairing queries."""
    model = BFTopologicalModel(level_k=2)
    engine = BFTopologicalBraidingEngine(in_memory=True)
    receipt = engine.audit_bf_braiding(model, is_chiral=False, is_z2_energy_split=False)

    cur = engine.conn.cursor()
    cur.execute("SELECT COUNT(*) FROM FermionConfigurations")
    cfg_count = cur.fetchone()[0]
    assert cfg_count == 2

    cur.execute("SELECT COUNT(*) FROM GinModePostingList")
    posting_count = cur.fetchone()[0]
    assert posting_count == 8

    cur.execute("SELECT COUNT(*) FROM GinInvolutionPairs")
    pair_count = cur.fetchone()[0]
    assert pair_count == 1

    engine.close()
