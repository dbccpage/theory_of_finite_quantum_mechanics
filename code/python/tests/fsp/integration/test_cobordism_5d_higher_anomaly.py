"""
test_cobordism_5d_higher_anomaly.py — Integration tests for 5D cobordism invariants,
Omega_5^{Spin}(BG) anomaly matching, and mapping torus sign obstructions.

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
from src.fsp.cobordism_5d_higher_anomaly import (
    CobordismAnomalyEngine,
    CobordismAuditReceipt,
    CobordismGroup5D,
    FiveComplexLattice,
    MappingTorusCobordismModel,
)


def test_5complex_boundary_nilpotence() -> None:
    """Verifies cellular boundary nilpotence partial_4 @ partial_5 == 0 on the 5-simplex lattice."""
    lattice = FiveComplexLattice()
    p4, p5 = lattice.boundary_operators()

    assert p4.shape == (15, 6)
    assert p5.shape == (6, 1)

    p4_p5 = p4 @ p5
    assert np.allclose(p4_p5, 0.0), f"Boundary partial_4 @ partial_5 != 0: {p4_p5}"


def test_ahss_cobordism_group_decomposition() -> None:
    """Verifies the Atiyah-Hirzebruch spectral sequence decomposition and invariant evaluation."""
    cob = CobordismGroup5D(has_postnikov_arf=True, has_mixed_gravitational=True)

    assert cob.evaluate_invariant_nu5(postnikov_eval=0, k3_signature_div16=0, w1_gauge_eval=0) == 0

    assert cob.evaluate_invariant_nu5(postnikov_eval=1, k3_signature_div16=0, w1_gauge_eval=0) == 1

    assert cob.evaluate_invariant_nu5(postnikov_eval=0, k3_signature_div16=1, w1_gauge_eval=1) == 1

    assert cob.evaluate_invariant_nu5(postnikov_eval=1, k3_signature_div16=1, w1_gauge_eval=1) == 0


def test_anomaly_free_cobordism_exact_repair() -> None:
    """When nu_5 == 0 (anomaly-free 5D cobordism), system is sign-free (ExactRepair)."""
    model = MappingTorusCobordismModel(
        four_manifold_type="T4",
        is_spin=True,
        is_orientable=True,
        postnikov_eval=0,
        w1_gauge_eval=0,
    )
    receipt = CobordismAnomalyEngine.audit_cobordism_anomaly(model, use_higher_2double=True)
    assert receipt.terminal_route == TerminalRoute.EXACT_REPAIR
    assert receipt.nu_5_cobordism_invariant == 0
    assert receipt.involution_pairing_phi1 == 0.0
    assert receipt.cochain_curvature_gamma2 == 0.0
    assert receipt.average_sign_gin == 1.0


def test_global_gravitational_anomaly_obstructs_2double() -> None:
    """
    When nu_5 == 1 (non-perturbative global gravitational anomaly in Omega_5^{Spin}(BG)),
    the large diffeomorphism twist U(f) = -I induces an irreducible sign flip that
    OBSTRUCTS higher 2-double sign cancellation, routing to OPEN_SIGN_OBSTRUCTION.
    """
    model = MappingTorusCobordismModel(
        four_manifold_type="K3",
        is_spin=True,
        is_orientable=True,
        postnikov_eval=0,
        w1_gauge_eval=1,
    )
    assert model.evaluate_5d_invariant() == 1

    receipt_bare = CobordismAnomalyEngine.audit_cobordism_anomaly(model, use_higher_2double=False)
    assert receipt_bare.terminal_route == TerminalRoute.OPEN_SIGN_OBSTRUCTION
    assert receipt_bare.involution_pairing_phi1 == 2.0
    assert math.isclose(receipt_bare.cochain_curvature_gamma2, math.pi, abs_tol=1e-5)
    assert receipt_bare.average_sign_gin == 0.0

    receipt_2qd = CobordismAnomalyEngine.audit_cobordism_anomaly(model, use_higher_2double=True)
    assert receipt_2qd.terminal_route == TerminalRoute.OPEN_SIGN_OBSTRUCTION
    assert receipt_2qd.involution_pairing_phi1 == 2.0
    assert math.isclose(receipt_2qd.cochain_curvature_gamma2, math.pi, abs_tol=1e-5)
    assert receipt_2qd.average_sign_gin == 0.0
    assert receipt_2qd.is_higher_2double_projected is True


def test_non_orientable_pin_minus_anomaly() -> None:
    """On non-orientable RP^4 with Pin^- anomaly, complex phases route to OPEN_SIGN_OBSTRUCTION."""
    model = MappingTorusCobordismModel(
        four_manifold_type="RP4",
        is_spin=False,
        is_orientable=False,
        pin_minus_nu16=2,
    )
    receipt = CobordismAnomalyEngine.audit_cobordism_anomaly(model, use_higher_2double=True)
    assert receipt.terminal_route == TerminalRoute.OPEN_SIGN_OBSTRUCTION
    assert receipt.involution_pairing_phi1 > 0.0
    assert receipt.cochain_curvature_gamma2 > 0.0


def test_thermal_weight_asymmetry_refusal() -> None:
    """Thermal weight asymmetry Delta E_orient > 0 routes to REFUSED."""
    model = MappingTorusCobordismModel(
        four_manifold_type="K3",
        is_spin=True,
        is_orientable=True,
        postnikov_eval=0,
        w1_gauge_eval=0,
        energy_gap_orient=2.0,
        temperature=1.0,
    )
    receipt = CobordismAnomalyEngine.audit_cobordism_anomaly(model, use_higher_2double=True)
    assert receipt.terminal_route == TerminalRoute.REFUSED
    assert receipt.involution_pairing_phi1 > 0.0
