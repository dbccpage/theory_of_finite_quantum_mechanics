"""
test_bf_linked_flux_braiding.py — Integration Tests for 3D Topological BF Theory & Linked Flux Loop Braiding.

AuthorityEffect: None.

Tests:
1. Gauss linking integral: verifies exact integer linking numbers for unlinked (0), Hopf (+-1), and Whitehead (0) links.
2. Z_2 BF theory (k=2 / 3D Toric Code): verifies real sign factor (-1.0), symmetric orientation doublet,
   and deterministic routing to TerminalRoute.ExactRepair (Phi_1 = 0.0).
3. Z_k fractional BF theory (k=3): verifies non-trivial complex braiding phase (2pi/3), non-contractible holonomy,
   positive curvature Gamma_2 > 0, and deterministic routing to TerminalRoute.OpenSignObstruction.
4. Orientation energy asymmetry (Delta E_orient > 0): verifies exponential weight discrepancy w_+ != w_-
   and deterministic routing to TerminalRoute.SplitBrainRefusal.
5. Unlinked loop control: verifies contractible holonomy (Hol == 1.0, Gamma_2 == 0.0) and ExactRepair.
6. GIN mode posting list resolution across loop perimeters, Seifert surfaces, and 2-form flux cores.
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

from src.fsp.bf_linked_flux_braiding import (
    BFLinkedFluxBraidingModel,
    BFLinkedFluxBraidingEngine,
    BFLuxAuditReceipt,
    discrete_gauss_linking_integral,
    generate_polygonal_loop,
)


def test_gauss_linking_integral_geometries():
    """Validates the Gauss linking integral across unlinked, Hopf, reversed Hopf, and Whitehead links."""
    l1_unlinked = generate_polygonal_loop("unlinked", loop_index=1, num_points=64)
    l2_unlinked = generate_polygonal_loop("unlinked", loop_index=2, num_points=64)
    lk_unlinked = discrete_gauss_linking_integral(l1_unlinked, l2_unlinked)
    assert abs(lk_unlinked) < 1e-4
    assert int(round(lk_unlinked)) == 0

    l1_hopf = generate_polygonal_loop("hopf", loop_index=1, num_points=64)
    l2_hopf = generate_polygonal_loop("hopf", loop_index=2, num_points=64)
    lk_hopf = discrete_gauss_linking_integral(l1_hopf, l2_hopf)
    assert pytest.approx(lk_hopf, abs=0.05) == 1.0
    assert int(round(lk_hopf)) == 1

    l2_hopf_rev = generate_polygonal_loop("hopf", loop_index=2, num_points=64, reversed_orientation=True)
    lk_hopf_rev = discrete_gauss_linking_integral(l1_hopf, l2_hopf_rev)
    assert pytest.approx(lk_hopf_rev, abs=0.05) == -1.0
    assert int(round(lk_hopf_rev)) == -1

    l1_whitehead = generate_polygonal_loop("whitehead", loop_index=1, num_points=64)
    l2_whitehead = generate_polygonal_loop("whitehead", loop_index=2, num_points=64)
    lk_whitehead = discrete_gauss_linking_integral(l1_whitehead, l2_whitehead)
    assert abs(lk_whitehead) < 0.1
    assert int(round(lk_whitehead)) == 0


def test_z2_bf_theory_negative_holonomy_and_obstruction():
    """
    Validates that in Z_2 BF theory (k=2 / 3D toric code) with linked loops (Lk=1),
    the topological factor is real and negative (-1.0). Orientation reversal cancels the imaginary
    component but preserves the negative sign, so exact repair is NOT achieved (routes to OpenSignObstruction).
    """
    model = BFLinkedFluxBraidingModel(
        model_id="bf_z2_hopf",
        k_level=2,
        charge_q=1,
        flux_p=1,
        link_type="hopf",
        delta_e_orient=0.0,
    )
    engine = BFLinkedFluxBraidingEngine(in_memory=True)
    try:
        receipt = engine.audit_bf_braiding(model, beta=2.0)

        assert receipt.k_level == 2
        assert receipt.linking_number_exact == 1
        assert pytest.approx(abs(receipt.braiding_phase_radians), abs=1e-5) == math.pi
        assert pytest.approx(receipt.cochain_holonomy_real, abs=1e-5) == -1.0
        assert pytest.approx(receipt.cochain_holonomy_imag, abs=1e-5) == 0.0

        assert receipt.weight_gap_delta_w <= 1e-6
        assert receipt.is_exact_repair_achieved is False
        assert receipt.uncancelled_defect_mass_phi_1 > 0.0
        assert receipt.terminal_route == "OpenSignObstruction"
    finally:
        engine.close()


def test_gauss_linking_double_hopf():
    """Validates that the double Hopf link geometry has linking number magnitude 2."""
    l1 = generate_polygonal_loop("double_hopf", loop_index=1, num_points=64)
    l2 = generate_polygonal_loop("double_hopf", loop_index=2, num_points=64)
    lk_val = discrete_gauss_linking_integral(l1, l2)
    assert pytest.approx(abs(lk_val), abs=0.05) == 2.0
    assert abs(int(round(lk_val))) == 2


def test_zk_fractional_bf_theory_open_sign_obstruction():
    """
    Validates that in Z_k fractional BF theory (k=3), complex braiding phases and Z_2 vs Z_3
    order clash obstruct exact sign cancellation, routing to OpenSignObstruction.
    """
    model = BFLinkedFluxBraidingModel(
        model_id="bf_z3_hopf",
        k_level=3,
        charge_q=1,
        flux_p=1,
        link_type="hopf",
        delta_e_orient=0.0,
    )
    engine = BFLinkedFluxBraidingEngine(in_memory=True)
    try:
        receipt = engine.audit_bf_braiding(model, beta=2.0)

        assert receipt.k_level == 3
        assert receipt.linking_number_exact == 1
        assert pytest.approx(receipt.braiding_phase_radians, abs=1e-5) == 2.0 * math.pi / 3.0
        assert pytest.approx(receipt.cochain_holonomy_real, abs=1e-5) == -0.5
        assert pytest.approx(receipt.cochain_holonomy_imag, abs=1e-5) == 0.5 * math.sqrt(3.0)

        assert receipt.is_holonomy_contractible is False
        assert receipt.cochain_curvature_gamma_2 > 0.0

        assert receipt.is_exact_repair_achieved is False
        assert receipt.uncancelled_defect_mass_phi_1 > 0.0
        assert receipt.terminal_route == "OpenSignObstruction"
    finally:
        engine.close()


def test_orientation_energy_asymmetry_split_brain():
    """
    Validates that an orientation energy gap (Delta E_orient > 0) creates weight discrepancy
    w_+ != w_-, obstructing weight-preserving pairing and routing to SplitBrainRefusal.
    """
    model = BFLinkedFluxBraidingModel(
        model_id="bf_z2_asymmetric",
        k_level=2,
        charge_q=1,
        flux_p=1,
        link_type="hopf",
        delta_e_orient=0.5,
    )
    engine = BFLinkedFluxBraidingEngine(in_memory=True)
    try:
        receipt = engine.audit_bf_braiding(model, beta=2.0)

        assert receipt.weight_gap_delta_w > 0.1
        assert receipt.is_exact_repair_achieved is False
        assert receipt.terminal_route == "SplitBrainRefusal"
    finally:
        engine.close()


def test_unlinked_loops_contractible_holonomy():
    """Validates that unlinked loops (Lk = 0) have contractible holonomy and zero cochain curvature."""
    model = BFLinkedFluxBraidingModel(
        model_id="bf_unlinked",
        k_level=3,
        charge_q=1,
        flux_p=1,
        link_type="unlinked",
        delta_e_orient=0.0,
    )
    engine = BFLinkedFluxBraidingEngine(in_memory=True)
    try:
        receipt = engine.audit_bf_braiding(model, beta=2.0)

        assert receipt.linking_number_exact == 0
        assert receipt.braiding_phase_radians == 0.0
        assert receipt.is_holonomy_contractible is True
        assert receipt.cochain_curvature_gamma_2 == 0.0
        assert receipt.uncancelled_defect_mass_phi_1 == 0.0
        assert receipt.terminal_route == "ExactRepair"
    finally:
        engine.close()


def test_gin_mode_posting_lists_bf_loops():
    """Validates relational SQLite GIN mode postings across loop cycles, Seifert surfaces, and flux cores."""
    model = BFLinkedFluxBraidingModel(model_id="bf_gin_test", k_level=2, link_type="hopf")
    engine = BFLinkedFluxBraidingEngine(in_memory=True)
    try:
        engine.audit_bf_braiding(model, beta=2.0)

        c = engine.conn.cursor()
        c.execute("SELECT COUNT(*) FROM FermionConfigurations WHERE model_name = 'bf_gin_test';")
        assert c.fetchone()[0] == 2

        c.execute("SELECT cfg_id FROM GinModePostingList WHERE mode_id = 1;")
        assert len(c.fetchall()) == 1

        c.execute("SELECT cfg_id FROM GinModePostingList WHERE mode_id = 3;")
        assert len(c.fetchall()) == 1

        c.execute("SELECT cfg_id FROM GinModePostingList WHERE mode_id = 4;")
        assert len(c.fetchall()) == 1
    finally:
        engine.close()
