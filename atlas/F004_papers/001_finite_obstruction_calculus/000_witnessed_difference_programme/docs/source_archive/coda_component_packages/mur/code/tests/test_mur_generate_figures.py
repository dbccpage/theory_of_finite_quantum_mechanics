# -*- coding: utf-8 -*-
"""Test figure generation for CODA-MUR.
"""

from __future__ import annotations

from coda_mur_core import (
    DIAGNOSTIC_NO_TERMINAL,
    DIAGNOSTIC_NO_TRANSPORT,
    DIAGNOSTIC_SUCCESS,
    DIAGNOSTIC_TARGET_UNAUTH,
    DIAGNOSTIC_UNPRICED_LOSS,
    LossLedger,
    MorphismKind,
    TerminalRegime,
    evaluate_transport_authority,
)
from finite_fixtures import finite_certificate
from generate_figures import generate_fig1


def test_generate_fig1():
    """Ensure schematic figure 1 generates properly and exists on disk."""
    out_path = generate_fig1()
    assert out_path.is_file()
    assert out_path.stat().st_size > 0


def test_fig1_step_diagnostics():
    """Verify exact diagnostic codes and residual mass across all 5 schematic ladder cases."""
    regime_ok = TerminalRegime("regime_B", lambda x: f"term_{x}", lambda t: True)
    regime_no_term = TerminalRegime("regime_B_noterm", lambda x: None, lambda t: True)
    regime_unauth = TerminalRegime("regime_B_unauth", lambda x: f"term_{x}", lambda t: False)

    # Step 0: No cert
    res0 = evaluate_transport_authority("source", regime_ok, "art", None)
    assert res0.inhabited is False
    assert res0.refusal_code == "R_notransport"
    assert res0.residual_mass == DIAGNOSTIC_NO_TRANSPORT

    # Step 1: Lossy no ledger
    cert1 = finite_certificate("A", "regime_B", "F", MorphismKind.QUOTIENT, True, True, None)
    res1 = evaluate_transport_authority("source", regime_ok, "art", cert1)
    assert res1.inhabited is False
    assert res1.refusal_code == "R_unpriced_loss"
    assert res1.residual_mass == DIAGNOSTIC_UNPRICED_LOSS

    # Step 2: No terminal
    cert2 = finite_certificate("A", "regime_B_noterm", "F", MorphismKind.QUOTIENT, True, True, LossLedger(e=True, loss_mass=1))
    res2 = evaluate_transport_authority("source", regime_no_term, "art", cert2)
    assert res2.inhabited is False
    assert res2.refusal_code == "R_noterminal"
    assert res2.residual_mass == DIAGNOSTIC_NO_TERMINAL

    # Step 3: Target unauth
    cert3 = finite_certificate("A", "regime_B_unauth", "F", MorphismKind.QUOTIENT, True, True, LossLedger(e=True, loss_mass=1))
    res3 = evaluate_transport_authority("source", regime_unauth, "art", cert3)
    assert res3.inhabited is False
    assert res3.refusal_code == "R_target_unauth"
    assert res3.residual_mass == DIAGNOSTIC_TARGET_UNAUTH

    # Step 4: Certified auth
    cert4 = finite_certificate("A", "regime_B", "F", MorphismKind.QUOTIENT, True, True, LossLedger(e=True, loss_mass=1))
    res4 = evaluate_transport_authority("source", regime_ok, "art", cert4)
    assert res4.inhabited is True
    assert res4.refusal_code is None
    assert res4.residual_mass == DIAGNOSTIC_SUCCESS

