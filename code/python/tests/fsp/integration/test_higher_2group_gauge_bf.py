"""
test_higher_2group_gauge_bf.py — Integration tests for 4D higher-categorical 2-group gauge theory,
Postnikov 3-cocycle invariants, and higher 2-double repairs.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e)
"""

import math
from pathlib import Path
import sys
import numpy as np
import pytest

code_dir = Path(__file__).resolve().parent.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from src.fsp.bqnf_sign_evaluator import TerminalRoute
from src.fsp.higher_2group_gauge_bf import (
    FourComplexLattice,
    Higher2GroupAuditReceipt,
    Higher2GroupEngine,
    Higher2GroupGaugeModel,
    PostnikovClass,
    StrictCrossedModule,
)


def test_crossed_module_axioms() -> None:
    """Verifies Peiffer identity and crossed-module condition for Z_2 crossed module."""
    cm = StrictCrossedModule.create_z2_z2_trivial_boundary()
    assert cm.g_order == 2
    assert cm.h_order == 2
    assert cm.partial_map == (0, 0)


def test_4complex_coboundary_nilpotence() -> None:
    """Verifies cellular boundary and coboundary nilpotence on the 4-simplex lattice."""
    lattice = FourComplexLattice()
    p1, p2, p3 = lattice.boundary_operators()

    p1_p2 = p1 @ p2
    assert np.allclose(p1_p2, 0.0), "Boundary partial_1 @ partial_2 != 0"

    p2_p3 = p2 @ p3
    assert np.allclose(p2_p3, 0.0), "Boundary partial_2 @ partial_3 != 0"

    d0 = p1.T
    d1 = p2.T
    d2 = p3.T

    assert np.allclose(d1 @ d0, 0.0), "Coboundary d_1 @ d_0 != 0"
    assert np.allclose(d2 @ d1, 0.0), "Coboundary d_2 @ d_1 != 0"


def test_postnikov_3cocycle_condition() -> None:
    """Verifies that the cup product w_1^3 satisfies the 3-cocycle condition delta_G a == 0."""
    cm = StrictCrossedModule.create_z2_z2_trivial_boundary()
    post_w1 = PostnikovClass.create_z2_cup_product(cm)
    assert not post_w1.is_trivial
    assert post_w1.evaluate(1, 1, 1) == 1
    assert post_w1.evaluate(0, 1, 1) == 0
    assert post_w1.verify_3cocycle_condition()

    post_triv = PostnikovClass.create_trivial(cm)
    assert post_triv.is_trivial
    assert post_triv.verify_3cocycle_condition()


def test_trivial_postnikov_exact_repair() -> None:
    """When Postnikov class [a] == 0, bare theory is sign-free (ExactRepair)."""
    cm = StrictCrossedModule.create_z2_z2_trivial_boundary()
    post_triv = PostnikovClass.create_trivial(cm)
    model = Higher2GroupGaugeModel(
        crossed_module=cm,
        postnikov_class=post_triv,
        surface_linking_number=1,
    )
    receipt = Higher2GroupEngine.audit_2group_gauge_theory(model, projection_mode="none")
    assert receipt.terminal_route == TerminalRoute.EXACT_REPAIR
    assert receipt.involution_pairing_phi1 == 0.0
    assert receipt.cochain_curvature_gamma2 == 0.0
    assert receipt.average_sign_gin == 1.0


def test_nontrivial_postnikov_obstructs_1form_quantum_double() -> None:
    """
    When Postnikov class [a] == w_1^3 != 0 and surface-loop are linked (Lk=1),
    ordinary 1-form quantum double P_QD^{(1)} FAILS to cancel the 3-cocycle sign,
    routing to OPEN_SIGN_OBSTRUCTION.
    """
    cm = StrictCrossedModule.create_z2_z2_trivial_boundary()
    post_w1 = PostnikovClass.create_z2_cup_product(cm)
    model = Higher2GroupGaugeModel(
        crossed_module=cm,
        postnikov_class=post_w1,
        surface_linking_number=1,
    )

    receipt_bare = Higher2GroupEngine.audit_2group_gauge_theory(model, projection_mode="none")
    assert receipt_bare.terminal_route == TerminalRoute.OPEN_SIGN_OBSTRUCTION
    assert receipt_bare.involution_pairing_phi1 == 2.0
    assert math.isclose(receipt_bare.cochain_curvature_gamma2, math.pi, abs_tol=1e-5)
    assert receipt_bare.average_sign_gin == 0.0

    receipt_1qd = Higher2GroupEngine.audit_2group_gauge_theory(model, projection_mode="1form_qd")
    assert receipt_1qd.terminal_route == TerminalRoute.OPEN_SIGN_OBSTRUCTION
    assert receipt_1qd.involution_pairing_phi1 == 2.0
    assert receipt_1qd.is_quantum_double_projected is True
    assert receipt_1qd.is_higher_2double_projected is False


def test_higher_2double_restores_exact_repair() -> None:
    """
    Higher-Categorical 2-Double Crossed-Module Projection P_{2-QD} doubles both 1-form
    and 2-form surface defects with the crossed-module conjugate, cancelling the 3-cocycle
    and restoring positive semi-definite trace and ExactRepair.
    """
    cm = StrictCrossedModule.create_z2_z2_trivial_boundary()
    post_w1 = PostnikovClass.create_z2_cup_product(cm)
    model = Higher2GroupGaugeModel(
        crossed_module=cm,
        postnikov_class=post_w1,
        surface_linking_number=1,
    )

    receipt_2qd = Higher2GroupEngine.audit_2group_gauge_theory(model, projection_mode="higher_2qd")
    assert receipt_2qd.terminal_route == TerminalRoute.EXACT_REPAIR
    assert receipt_2qd.involution_pairing_phi1 == 0.0
    assert receipt_2qd.cochain_curvature_gamma2 == 0.0
    assert receipt_2qd.average_sign_gin == 1.0
    assert receipt_2qd.is_higher_2double_projected is True


def test_thermal_weight_asymmetry_refusal() -> None:
    """Thermal weight asymmetry Delta E_orient > 0 routes to REFUSED."""
    cm = StrictCrossedModule.create_z2_z2_trivial_boundary()
    post_w1 = PostnikovClass.create_z2_cup_product(cm)
    model = Higher2GroupGaugeModel(
        crossed_module=cm,
        postnikov_class=post_w1,
        surface_linking_number=1,
        energy_gap_orient=1.5,
        temperature=1.0,
    )
    receipt = Higher2GroupEngine.audit_2group_gauge_theory(model, projection_mode="none")
    assert receipt.terminal_route == TerminalRoute.REFUSED
    assert receipt.involution_pairing_phi1 > 0.0
