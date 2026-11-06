# -*- coding: utf-8 -*-
"""
Non-vacuous mutation tests for CODA-MUR (Certified Representation Transport).

Lev Landau discipline: each test states the invariant, then a real mutation
must flip the outcome.
Zero Floats Invariant: exact rational numbers only; floats and booleans in
scalar positions strictly raise TypeError.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from fractions import Fraction

import numpy as np
import pytest
from coda_mur_core import (
    RESIDUAL_NO_TERMINAL,
    RESIDUAL_NO_TRANSPORT,
    RESIDUAL_SUCCESS,
    RESIDUAL_TARGET_UNAUTH,
    RESIDUAL_UNPRICED_LOSS,
    DescentSquareCertificate,
    FiniteCoreAction,
    LossLedger,
    MorphismKind,
    TerminalRegime,
    compute_transport_quotient_obstruction,
    evaluate_transport_authority,
    paste_certificates,
)
from finite_fixtures import finite_certificate
from sympy import Matrix, Rational


def _exact_certificate() -> DescentSquareCertificate:
    return finite_certificate(
        source_regime="Regime_A",
        target_regime="Regime_B",
        morphism_name="F_exact",
        morphism_kind=MorphismKind.EXACT,
        chi_certified=True,
        commutes=True,
    )


def _quotient_certificate(**ledger_kwargs) -> DescentSquareCertificate:
    base_kwargs = dict(e=True, loss_mass=Rational(1, 10))
    base_kwargs.update(ledger_kwargs)
    return finite_certificate(
        source_regime="Regime_A",
        target_regime="Regime_B",
        morphism_name="F_quot",
        morphism_kind=MorphismKind.QUOTIENT,
        chi_certified=True,
        commutes=True,
        loss_ledger=LossLedger(**base_kwargs),
    )


def _target_regime(can_terminalize: bool = True, is_authorized: bool = True) -> TerminalRegime:
    return TerminalRegime(
        regime_id="Regime_B",
        terminalize=lambda x: f"term_{x}" if can_terminalize else None,
        is_auth=lambda t: is_authorized,
    )


def test_valid_exact_transport_inhabits_authority():
    """Invariant: exact certified transport + target terminalization => target authority inhabited."""
    cert = _exact_certificate()
    regime = _target_regime(can_terminalize=True, is_authorized=True)
    res = evaluate_transport_authority("source_01", regime, "artifact_01", cert)

    assert res.inhabited is True
    assert res.target_terminal == "term_artifact_01"
    assert res.refusal_code is None
    assert res.residual_mass == RESIDUAL_SUCCESS
    assert res.authority_effect == "None"


def test_certificate_necessity_refuses_without_cert():
    """Invariant (GTMUR-02): representation transport requires certified modification chi_F."""
    regime = _target_regime(can_terminalize=True, is_authorized=True)

    # Missing certificate
    res_none = evaluate_transport_authority("source_01", regime, "artifact_01", None)
    assert res_none.inhabited is False
    assert res_none.refusal_code == "R_notransport"
    assert res_none.residual_mass == RESIDUAL_NO_TRANSPORT

    # Uncertified certificate
    bad_cert = finite_certificate(
        source_regime="Regime_A",
        target_regime="Regime_B",
        morphism_name="F_bad",
        morphism_kind=MorphismKind.EXACT,
        chi_certified=False,
        commutes=True,
    )
    res_uncert = evaluate_transport_authority("source_01", regime, "artifact_01", bad_cert)
    assert res_uncert.inhabited is False
    assert res_uncert.refusal_code == "R_notransport"

    # Non-commuting certificate
    non_comm = finite_certificate(
        source_regime="Regime_A",
        target_regime="Regime_B",
        morphism_name="F_bad",
        morphism_kind=MorphismKind.EXACT,
        chi_certified=True,
        commutes=False,
    )
    res_comm = evaluate_transport_authority("source_01", regime, "artifact_01", non_comm)
    assert res_comm.inhabited is False
    assert res_comm.refusal_code == "R_notransport"


def test_loss_ledger_necessity_for_lossy_morphisms():
    """Invariant (GTMUR-04 / GTMUR-T03): lossy morphisms without declared loss ledger refuse."""
    regime = _target_regime(can_terminalize=True, is_authorized=True)

    lossy_kinds = [
        MorphismKind.QUOTIENT,
        MorphismKind.APPROXIMATION,
        MorphismKind.UNMEASURED,
    ]

    for kind in lossy_kinds:
        # None loss ledger
        cert_none = finite_certificate(
            source_regime="Regime_A",
            target_regime="Regime_B",
            morphism_name=f"F_{kind.value}",
            morphism_kind=kind,
            chi_certified=True,
            commutes=True,
            loss_ledger=None,
        )
        res_none = evaluate_transport_authority("source_01", regime, "artifact_01", cert_none)
        assert res_none.inhabited is False
        assert res_none.refusal_code == "R_unpriced_loss"
        assert res_none.residual_mass == RESIDUAL_UNPRICED_LOSS

        # Empty loss ledger
        cert_empty = finite_certificate(
            source_regime="Regime_A",
            target_regime="Regime_B",
            morphism_name=f"F_{kind.value}",
            morphism_kind=kind,
            chi_certified=True,
            commutes=True,
            loss_ledger=LossLedger.empty(),
        )
        res_empty = evaluate_transport_authority("source_01", regime, "artifact_01", cert_empty)
        assert res_empty.inhabited is False
        assert res_empty.refusal_code == "R_unpriced_loss"
        assert res_empty.residual_mass == RESIDUAL_UNPRICED_LOSS


def test_terminal_non_bypass_firewall():
    """Invariant (GTMUR-03 / GTMUR-L02): chi_F alone does NOT suffice for target authority."""
    cert = _exact_certificate()

    # Target cannot terminalize
    regime_noterm = _target_regime(can_terminalize=False, is_authorized=True)
    res_noterm = evaluate_transport_authority("source_01", regime_noterm, "artifact_01", cert)
    assert res_noterm.inhabited is False
    assert res_noterm.target_terminal is None
    assert res_noterm.refusal_code == "R_noterminal"
    assert res_noterm.residual_mass == RESIDUAL_NO_TERMINAL

    # Target terminalizes but fails target authorization
    regime_unauth = _target_regime(can_terminalize=True, is_authorized=False)
    res_unauth = evaluate_transport_authority("source_01", regime_unauth, "artifact_01", cert)
    assert res_unauth.inhabited is False
    assert res_unauth.target_terminal == "term_artifact_01"
    assert res_unauth.refusal_code == "R_target_unauth"
    assert res_unauth.residual_mass == RESIDUAL_TARGET_UNAUTH


def test_loss_algebra_monoid_laws():
    """Invariant (GTMUR-T04): loss ledger forms an associative monoid with identity."""
    l1 = LossLedger(e=True, loss_mass=Rational(1, 4))
    l2 = LossLedger(i=True, loss_mass=Rational(1, 8))
    l3 = LossLedger(a=True, loss_mass=Rational(3, 8))
    empty = LossLedger.empty()

    # Left & Right Unit
    assert empty.accumulate(l1) == l1
    assert l1.accumulate(empty) == l1

    # Associativity: (l1 + l2) + l3 == l1 + (l2 + l3)
    lhs = (l1.accumulate(l2)).accumulate(l3)
    rhs = l1.accumulate(l2.accumulate(l3))
    assert lhs == rhs
    assert lhs.loss_mass == Rational(3, 4)
    assert lhs.e is True and lhs.i is True and lhs.a is True and lhs.u is False


def test_certificate_pasting_law():
    """Invariant (GTMUR-05 / GTMUR-T01): descent square certificates paste composably."""
    chi_f = finite_certificate(
        source_regime="Regime_A",
        target_regime="Regime_B",
        morphism_name="F",
        morphism_kind=MorphismKind.QUOTIENT,
        chi_certified=True,
        commutes=True,
        loss_ledger=LossLedger(e=True, loss_mass=Rational(1, 5)),
    )
    chi_g = finite_certificate(
        source_regime="Regime_B",
        target_regime="Regime_C",
        morphism_name="G",
        morphism_kind=MorphismKind.APPROXIMATION,
        chi_certified=True,
        commutes=True,
        loss_ledger=LossLedger(a=True, loss_mass=Rational(2, 5)),
    )

    pasted = paste_certificates(chi_f, chi_g)
    assert pasted.source_regime == "Regime_A"
    assert pasted.target_regime == "Regime_C"
    assert pasted.morphism_kind == MorphismKind.APPROXIMATION
    assert pasted.chi_certified is True
    assert pasted.commutes is True
    assert pasted.loss_ledger is not None
    assert pasted.loss_ledger.e is True
    assert pasted.loss_ledger.a is True
    assert pasted.loss_ledger.loss_mass == Rational(3, 5)

    # Regime mismatch failure
    chi_bad = finite_certificate(
        source_regime="Regime_MISMATCH",
        target_regime="Regime_C",
        morphism_name="G_bad",
        morphism_kind=MorphismKind.EXACT,
        chi_certified=True,
        commutes=True,
    )
    with pytest.raises(ValueError, match="Cannot paste certificates"):
        paste_certificates(chi_f, chi_bad)


def test_cochain_quotient_solver_bridge():
    """Invariant: exact cochain quotient obstruction Q^1_chi = C^1_chi / im(d0)."""
    # d0 map: [1, -1]^T
    d0 = Matrix([[1], [-1]])

    # Case 1: Exact commuting cochain in im(d0)
    omega_zero = Matrix([[3], [-3]])
    cert_zero = compute_transport_quotient_obstruction(d0, omega_zero)
    assert cert_zero.distance == Rational(0, 1)
    assert cert_zero.verify() is True

    regime = _target_regime(can_terminalize=True, is_authorized=True)
    res_zero = evaluate_transport_authority(
        "src_01", regime, "art_01", replace(_exact_certificate(), defect_vector=omega_zero, repair_map=d0), quotient_certificate=cert_zero
    )
    assert res_zero.inhabited is True
    assert res_zero.residual_mass == RESIDUAL_SUCCESS

    # Case 2: Obstruction cochain not in im(d0)
    omega_defect = Matrix([[1], [1]])
    cert_defect = compute_transport_quotient_obstruction(d0, omega_defect)
    assert cert_defect.distance == Rational(2, 1)
    assert cert_defect.verify() is True

    res_defect = evaluate_transport_authority(
        "src_01", regime, "art_01", replace(_exact_certificate(), defect_vector=omega_defect, repair_map=d0), quotient_certificate=cert_defect
    )
    assert res_defect.inhabited is False
    assert res_defect.refusal_code == "R_obstruction"
    assert res_defect.residual_mass == Rational(2, 1)


def test_strict_float_rejection():
    """Zero Floats Invariant: passing float or boolean as scalar raises TypeError."""
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        LossLedger(loss_mass=0.5)

    with pytest.raises(TypeError, match="floats strictly forbidden"):
        LossLedger(loss_mass=np.float64(1.0))

    with pytest.raises(TypeError, match="got bool"):
        LossLedger(loss_mass=True)

    with pytest.raises(ValueError, match="loss_mass must be non-negative"):
        LossLedger(loss_mass=Rational(-1, 2))

    # String rational and fractions
    l_frac = LossLedger(loss_mass=Fraction(1, 3))
    assert l_frac.loss_mass == Rational(1, 3)

    l_str = LossLedger(loss_mass="2/7")
    assert l_str.loss_mass == Rational(2, 7)

    with pytest.raises(TypeError, match="string could not be converted"):
        LossLedger(loss_mass="not_a_rational")

    with pytest.raises(TypeError, match="must be an exact rational"):
        LossLedger(loss_mass=[1, 2])


def test_validate_exact_int_coverage():
    from coda_mur_core import _validate_exact_int
    assert _validate_exact_int(5, "k") == 5
    with pytest.raises(TypeError, match="got bool"):
        _validate_exact_int(True, "k")
    with pytest.raises(TypeError, match="must be an integer"):
        _validate_exact_int(3.14, "k")
    with pytest.raises(ValueError, match="must be non-negative"):
        _validate_exact_int(-1, "k")


def test_certificate_is_valid_and_pasting_branches():
    # is_valid checks
    c_unauth = finite_certificate("A", "B", "F", MorphismKind.EXACT, chi_certified=False, commutes=True)
    assert c_unauth.is_valid() is False

    c_lossy_empty = finite_certificate("A", "B", "F", MorphismKind.QUOTIENT, chi_certified=True, commutes=True)
    assert c_lossy_empty.is_valid() is False

    # Mass alone without erasure dimension fails quotient obligation (§3.7)
    c_lossy_mass_only = finite_certificate("A", "B", "F", MorphismKind.QUOTIENT, chi_certified=True, commutes=True, loss_ledger=LossLedger(e=False, loss_mass=Rational(1, 2)))
    assert c_lossy_mass_only.is_valid() is False

    c_lossy_ok = finite_certificate("A", "B", "F", MorphismKind.QUOTIENT, chi_certified=True, commutes=True, loss_ledger=LossLedger(e=True, loss_mass=Rational(1, 2)))
    assert c_lossy_ok.is_valid() is True

    # Pasting kinds with valid legs
    c_unmeas = finite_certificate("B", "C", "G1", MorphismKind.UNMEASURED, chi_certified=True, commutes=True, loss_ledger=LossLedger(u=True, loss_mass=Rational(1, 4)))
    p_unmeas = paste_certificates(c_lossy_ok, c_unmeas)
    assert p_unmeas.morphism_kind == MorphismKind.UNMEASURED

    c_approx = finite_certificate("B", "C", "G2", MorphismKind.APPROXIMATION, chi_certified=True, commutes=True, loss_ledger=LossLedger(a=True, loss_mass=Rational(1, 4)))
    p_approx = paste_certificates(c_lossy_ok, c_approx)
    assert p_approx.morphism_kind == MorphismKind.APPROXIMATION

    # quotient pasting with exact
    c_exact_tgt = finite_certificate("B", "C", "X", MorphismKind.EXACT, chi_certified=True, commutes=True)
    p_quot_exact = paste_certificates(c_lossy_ok, c_exact_tgt)
    assert p_quot_exact.morphism_kind == MorphismKind.QUOTIENT

    c_embed1 = finite_certificate("A", "B", "E1", MorphismKind.EMBEDDING, chi_certified=True, commutes=True)
    c_embed2 = finite_certificate("B", "C", "E2", MorphismKind.EMBEDDING, chi_certified=True, commutes=True)
    p_embed = paste_certificates(c_embed1, c_embed2)
    assert p_embed.morphism_kind == MorphismKind.EMBEDDING

    c_exact1 = finite_certificate("A", "B", "X1", MorphismKind.EXACT, chi_certified=True, commutes=True)
    c_exact2 = finite_certificate("B", "C", "X2", MorphismKind.EXACT, chi_certified=True, commutes=True)
    p_exact = paste_certificates(c_exact1, c_exact2)
    assert p_exact.morphism_kind == MorphismKind.EXACT

    # Pasting invalid leg raises ValueError (§3.5)
    c_invalid_leg = finite_certificate("B", "C", "G_bad", MorphismKind.QUOTIENT, chi_certified=True, commutes=True, loss_ledger=None)
    with pytest.raises(ValueError, match="Cannot paste"):
        paste_certificates(c_lossy_ok, c_invalid_leg)

    with pytest.raises(ValueError, match="Cannot paste certificates"):
        paste_certificates(c_exact1, c_exact1)


def test_finite_core_action_algebra():
    from coda_mur_core import FiniteCoreAction

    act_ab = FiniteCoreAction(
        source_regime="Regime_A",
        target_regime="Regime_B",
        action_map=lambda c: f"{c}_coreB",
        is_loss_free=True,
    )
    assert act_ab.apply("repA") == "repA_coreB"

    act_bc = FiniteCoreAction(
        source_regime="Regime_B",
        target_regime="Regime_C",
        action_map=lambda c: f"{c}_coreC",
        is_loss_free=True,
    )
    comp = act_ab.compose(act_bc)
    assert comp.source_regime == "Regime_A"
    assert comp.target_regime == "Regime_C"
    assert comp.apply("repA") == "repA_coreB_coreC"
    assert comp.is_loss_free is True

    with pytest.raises(ValueError, match="Cannot compose actions"):
        act_ab.compose(act_ab)


def test_evaluate_transport_authority_with_action():
    from coda_mur_core import FiniteCoreAction

    cert = _exact_certificate()
    regime = _target_regime(can_terminalize=True, is_authorized=True)

    action = FiniteCoreAction(
        source_regime="Regime_A",
        target_regime="Regime_B",
        action_map=lambda src: f"{src}_mapped",
    )

    # When transported_artifact is None, action.apply is invoked
    res = evaluate_transport_authority(
        source_artifact_id="art0",
        target_regime=regime,
        transported_artifact=None,
        certificate=cert,
        action=action,
    )
    assert res.inhabited is True
    assert res.target_terminal == "term_art0_mapped"

    # Mismatched regime raises ValueError
    bad_action = FiniteCoreAction(
        source_regime="Regime_Wrong",
        target_regime="Regime_B",
        action_map=lambda src: src,
    )
    with pytest.raises(ValueError, match="FiniteCoreAction regimes"):
        evaluate_transport_authority(
            source_artifact_id="art0",
            target_regime=regime,
            transported_artifact="art0",
            certificate=cert,
            action=bad_action,
        )


def test_target_regime_mismatch_refused():
    """Invariant (§3.4): certificate for Regime_B cannot authorize Regime_C."""
    cert = _exact_certificate()  # target is Regime_B
    regime_c = TerminalRegime(
        regime_id="Regime_C",
        terminalize=lambda x: f"term_{x}",
        is_auth=lambda t: True,
    )
    res = evaluate_transport_authority("source_01", regime_c, "artifact_01", cert)
    assert res.inhabited is False
    assert res.refusal_code == "R_regime_mismatch"


def test_source_regime_mismatch_refused():
    """Invariant (§3.4): certificate source must match declared source regime."""
    cert = _exact_certificate()  # source is Regime_A
    regime = _target_regime()
    res = evaluate_transport_authority(
        "source_01", regime, "artifact_01", cert, source_regime="Regime_Wrong"
    )
    assert res.inhabited is False
    assert res.refusal_code == "R_regime_mismatch"


def test_substituted_target_artifact_refused():
    """Invariant (§3.4): caller cannot substitute an unrelated target artifact."""
    cert = _exact_certificate()
    regime = _target_regime()
    action = FiniteCoreAction(
        source_regime="Regime_A",
        target_regime="Regime_B",
        action_map=lambda s: f"genuine_{s}",
    )
    # Action produces "genuine_source_01", but caller provides "fraudulent_artifact"
    res = evaluate_transport_authority(
        source_artifact_id="source_01",
        target_regime=regime,
        transported_artifact="fraudulent_artifact",
        certificate=cert,
        action=action,
    )
    assert res.inhabited is False
    assert res.refusal_code == "R_substituted_artifact"


def test_kind_composition_monoid_5x5():
    """Invariant (§3.5): 5x5 kind monoid has left/right identity and associativity."""
    from coda_mur_core import compose_kinds

    kinds = list(MorphismKind)
    assert len(kinds) == 5

    # Left and right identity for EXACT
    for k in kinds:
        assert compose_kinds(MorphismKind.EXACT, k) == k
        assert compose_kinds(k, MorphismKind.EXACT) == k

    # Exact bug check (§3.5): EXACT composing with EMBEDDING must be EMBEDDING, not EXACT
    assert compose_kinds(MorphismKind.EXACT, MorphismKind.EMBEDDING) == MorphismKind.EMBEDDING
    assert compose_kinds(MorphismKind.EMBEDDING, MorphismKind.EXACT) == MorphismKind.EMBEDDING

    # UNMEASURED absorbs all kinds
    for k in kinds:
        assert compose_kinds(MorphismKind.UNMEASURED, k) == MorphismKind.UNMEASURED
        assert compose_kinds(k, MorphismKind.UNMEASURED) == MorphismKind.UNMEASURED

    # Associativity across all 5^3 = 125 triples
    for a in kinds:
        for b in kinds:
            for c in kinds:
                lhs = compose_kinds(compose_kinds(a, b), c)
                rhs = compose_kinds(a, compose_kinds(b, c))
                assert lhs == rhs, f"Associativity failed for triple ({a}, {b}, {c})"


def test_pasting_preserves_per_leg_ledgers():
    """Invariant (§3.5): composite preserves per-leg ledger receipts."""
    chi_f = finite_certificate(
        source_regime="A",
        target_regime="B",
        morphism_name="F",
        morphism_kind=MorphismKind.QUOTIENT,
        chi_certified=True,
        commutes=True,
        loss_ledger=LossLedger(e=True, loss_mass=Rational(1, 4)),
    )
    chi_g = finite_certificate(
        source_regime="B",
        target_regime="C",
        morphism_name="G",
        morphism_kind=MorphismKind.APPROXIMATION,
        chi_certified=True,
        commutes=True,
        loss_ledger=LossLedger(a=True, loss_mass=Rational(1, 2)),
    )
    pasted = paste_certificates(chi_f, chi_g)
    assert pasted.leg_ledgers is not None
    assert pasted.leg_ledgers[0] == chi_f.loss_ledger
    assert pasted.leg_ledgers[1] == chi_g.loss_ledger


def test_quotient_certificate_verification_gate():
    """Invariant (§3.6): quotient certificates must verify, be typed, and non-negative."""
    from coda_mur_core import QuotientDistanceCertificate

    cert = _exact_certificate()
    regime = _target_regime()

    # 1. Unverified certificate (verify returns False)
    bad_verify_cert = QuotientDistanceCertificate(
        distance=Rational(1, 2),
        repair_witness=Matrix([[0]]),
        residual=Matrix([[1]]),  # Doesn't match cochain - d0*witness
        cochain=Matrix([[2]]),
        dual_witness=Matrix([[1]]),
        dual_pairing=Rational(1, 2),
        repair_map=Matrix([[1]]),
    )
    res_unver = evaluate_transport_authority(
        "s", regime, "art", cert, quotient_certificate=bad_verify_cert
    )
    assert res_unver.inhabited is False
    assert res_unver.refusal_code == "R_malformed_quotient"

    # 2. Negative distance certificate
    class FakeCert:
        distance = Rational(-5, 1)
        def verify(self):
            return True

    res_neg = evaluate_transport_authority(
        "s", regime, "art", cert, quotient_certificate=FakeCert()  # type: ignore[arg-type]
    )
    assert res_neg.inhabited is False
    assert res_neg.refusal_code == "R_malformed_quotient"

    # 3. Duck-typed object passing distance > 0 without verify method
    class UntypedCert:
        distance = Rational(2, 1)

    res_untyped = evaluate_transport_authority(
        "s", regime, "art", cert, quotient_certificate=UntypedCert()  # type: ignore[arg-type]
    )
    assert res_untyped.inhabited is False
    assert res_untyped.refusal_code == "R_malformed_quotient"


def test_loss_ledger_strict_booleans():
    """Invariant (§3.7): boolean ledger and certificate fields strictly reject truthy strings."""
    with pytest.raises(TypeError, match="must be bool"):
        LossLedger(e="False")  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="must be bool"):
        LossLedger(e=1)  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="must be bool"):
        finite_certificate(
            source_regime="A",
            target_regime="B",
            morphism_name="F",
            morphism_kind=MorphismKind.EXACT,
            chi_certified="False",  # type: ignore[arg-type]
            commutes=True,
        )


def test_kind_to_ledger_dimension_obligations():
    """Invariant (§3.7): each lossy kind requires its declared loss dimension bit."""
    # Quotient requires e=True
    q_mass_only = finite_certificate(
        "A", "B", "Q1", MorphismKind.QUOTIENT, chi_certified=True, commutes=True,
        loss_ledger=LossLedger(e=False, a=True, loss_mass=Rational(1, 2)),
    )
    assert q_mass_only.is_valid() is False

    q_ok = finite_certificate(
        "A", "B", "Q2", MorphismKind.QUOTIENT, chi_certified=True, commutes=True,
        loss_ledger=LossLedger(e=True, loss_mass=Rational(1, 2)),
    )
    assert q_ok.is_valid() is True

    # Approximation requires a=True or i=True
    approx_bad = finite_certificate(
        "A", "B", "App1", MorphismKind.APPROXIMATION, chi_certified=True, commutes=True,
        loss_ledger=LossLedger(e=True, loss_mass=Rational(1, 2)),
    )
    assert approx_bad.is_valid() is False

    approx_ok1 = finite_certificate(
        "A", "B", "App2", MorphismKind.APPROXIMATION, chi_certified=True, commutes=True,
        loss_ledger=LossLedger(a=True, loss_mass=Rational(1, 2)),
    )
    assert approx_ok1.is_valid() is True

    # Unmeasured requires u=True
    unm_bad = finite_certificate(
        "A", "B", "U1", MorphismKind.UNMEASURED, chi_certified=True, commutes=True,
        loss_ledger=LossLedger(e=True, a=True, loss_mass=Rational(1, 2)),
    )
    assert unm_bad.is_valid() is False

    unm_ok = finite_certificate(
        "A", "B", "U2", MorphismKind.UNMEASURED, chi_certified=True, commutes=True,
        loss_ledger=LossLedger(u=True, loss_mass=Rational(1, 2)),
    )
    assert unm_ok.is_valid() is True


def test_finite_verification_evaluates_square():
    """Invariant (§3.3): finite verification model evaluates four maps on declared carrier."""
    # Integer to parity: carrier {0, 1, 2, 3, 4, 5}
    carrier = (0, 1, 2, 3, 4, 5)

    def f_states(n: int) -> int:
        return n % 2

    def f_obs(n: int) -> int:
        return n % 2

    def p_look(n: int) -> int:
        return n

    def q_look(b: int) -> int:
        return b

    cert_verified = DescentSquareCertificate(
        source_regime="integers",
        target_regime="parity",
        morphism_name="mod2",
        morphism_kind=MorphismKind.QUOTIENT,
        chi_certified=True,
        commutes=True,
        loss_ledger=LossLedger(e=True, loss_mass=Rational(1, 10)),
        state_map=f_states,
        observation_map=f_obs,
        source_look=p_look,
        target_look=q_look,
        carrier=carrier,
    )
    assert cert_verified.verify() is True
    assert cert_verified.is_valid() is True

    # Mismatched square where observation map returns wrong value
    def f_obs_wrong(n: int) -> int:
        return (n + 1) % 2
    cert_mismatch = DescentSquareCertificate(
        source_regime="integers",
        target_regime="parity",
        morphism_name="mod2_wrong",
        morphism_kind=MorphismKind.QUOTIENT,
        chi_certified=True,
        commutes=True,
        loss_ledger=LossLedger(e=True, loss_mass=Rational(1, 10)),
        state_map=f_states,
        observation_map=f_obs_wrong,
        source_look=p_look,
        target_look=q_look,
        carrier=carrier,
    )
    assert cert_mismatch.verify() is False
    assert cert_mismatch.is_valid() is False


# =========================================================================
# Reviewer Regression Test Cases (§1 - §6)
# =========================================================================

def test_reviewer_state_map_exception_returns_refusal():
    """§1: A failed provenance check (state_map raises) must refuse, not fall through to success."""
    regime = _target_regime(can_terminalize=True, is_authorized=True)
    mapping = {"seen": "target_seen"}

    cert = DescentSquareCertificate(
        source_regime="Regime_A",
        target_regime="Regime_B",
        morphism_name="F_lookup",
        morphism_kind=MorphismKind.EXACT,
        chi_certified=True,
        commutes=True,
        state_map=lambda s: mapping[s],
        observation_map=lambda o: o,
        source_look=lambda x: x,
        target_look=lambda y: y,
        carrier=("seen",),
    )

    # Requested source 'outside' raises KeyError in state_map
    res = evaluate_transport_authority("outside", regime, "unrelated_target", cert)
    assert res.inhabited is False
    assert res.refusal_code in ("R_substituted_artifact", "R_notransport")


def test_reviewer_action_conflicting_with_state_map_refuses():
    """§1: Action conflicting with certified state map must be refused (cannot substitute certified map)."""
    regime = _target_regime(can_terminalize=True, is_authorized=True)

    cert = DescentSquareCertificate(
        source_regime="Regime_A",
        target_regime="Regime_B",
        morphism_name="F_cert",
        morphism_kind=MorphismKind.EXACT,
        chi_certified=True,
        commutes=True,
        state_map=lambda s: "certified",
        observation_map=lambda o: "certified",
        source_look=lambda x: x,
        target_look=lambda y: y,
        carrier=("s",),
    )

    action_sub = FiniteCoreAction(
        source_regime="Regime_A",
        target_regime="Regime_B",
        action_map=lambda s: "substituted",
    )

    # Action maps to "substituted" while certified map maps to "certified"
    res = evaluate_transport_authority(
        "s", regime, "substituted", cert, action=action_sub
    )
    assert res.inhabited is False
    assert res.refusal_code == "R_substituted_artifact"


def test_reviewer_incomplete_finite_verification_rejected():
    """§2: Incomplete finite verification record must not fall back to Boolean attestation."""
    # Deleting target_look from finite model must fail verification
    cert_incomplete = DescentSquareCertificate(
        source_regime="Regime_A",
        target_regime="Regime_B",
        morphism_name="F_partial",
        morphism_kind=MorphismKind.EXACT,
        chi_certified=True,
        commutes=True,
        carrier=(1, 2),
        state_map=lambda x: x,
        observation_map=lambda o: o,
        source_look=lambda x: x,
        target_look=None,  # Missing target_look
    )
    assert cert_incomplete.verify() is False
    assert cert_incomplete.is_valid() is False


def test_reviewer_requested_source_outside_carrier_and_noncommuting_refuses():
    """§2: Requested source outside carrier that fails commutation must refuse."""
    regime = _target_regime(can_terminalize=True, is_authorized=True)

    # Routes agree on ("checked",) but disagree on "outside"
    def s_map(x): return x
    def o_map(x): return x if x == "checked" else "different"
    def src_lk(x): return x
    def tgt_lk(x): return x

    cert = DescentSquareCertificate(
        source_regime="Regime_A",
        target_regime="Regime_B",
        morphism_name="F_carrier",
        morphism_kind=MorphismKind.EXACT,
        chi_certified=True,
        commutes=True,
        state_map=s_map,
        observation_map=o_map,
        source_look=src_lk,
        target_look=tgt_lk,
        carrier=("checked",),
    )
    assert cert.verify() is True

    # 'outside' fails commutation
    res = evaluate_transport_authority("outside", regime, "outside", cert)
    assert res.inhabited is False
    assert res.refusal_code == "R_notransport"


def test_reviewer_quotient_cochain_bound_to_defect_vector():
    """§3: Quotient certificate must prove the declared transport defect, not an arbitrary problem."""
    regime = _target_regime(can_terminalize=True, is_authorized=True)
    d0 = Matrix([[0]])
    defect = Matrix([[1]])

    cert = finite_certificate(
        source_regime="Regime_A",
        target_regime="Regime_B",
        morphism_name="F_defect",
        morphism_kind=MorphismKind.QUOTIENT,
        chi_certified=True,
        commutes=True,
        loss_ledger=LossLedger(e=True, loss_mass=1),
        defect_vector=defect,
        repair_map=d0,
    )

    # Certificate proving [0] (distance 0) instead of declared defect [1]
    wrong_q = compute_transport_quotient_obstruction(d0, Matrix([[0]]))
    assert wrong_q.distance == 0
    assert wrong_q.verify() is True

    res_wrong = evaluate_transport_authority("s", regime, "art", cert, quotient_certificate=wrong_q)
    assert res_wrong.inhabited is False
    assert res_wrong.refusal_code == "R_malformed_quotient"

    # Correct certificate proving declared defect [1] (distance 1)
    correct_q = compute_transport_quotient_obstruction(d0, defect)
    assert correct_q.distance == 1
    assert correct_q.verify() is True

    res_correct = evaluate_transport_authority("s", regime, "art", cert, quotient_certificate=correct_q)
    assert res_correct.inhabited is False
    assert res_correct.refusal_code == "R_obstruction"


def test_reviewer_pasting_loss_ledger_associativity():
    """§4.1: Pasting loss accumulation and leaf preservation must be associative."""
    # F: A -> B (QUOTIENT, loss 1/3)
    f = finite_certificate(
        "A", "B", "F", MorphismKind.QUOTIENT, True, True,
        loss_ledger=LossLedger(e=True, loss_mass=Rational(1, 3)),
    )
    # G: B -> C (EXACT, no loss)
    g = finite_certificate("B", "C", "G", MorphismKind.EXACT, True, True)
    # H: C -> D (QUOTIENT, loss 1/5)
    h = finite_certificate(
        "C", "D", "H", MorphismKind.QUOTIENT, True, True,
        loss_ledger=LossLedger(e=True, loss_mass=Rational(1, 5)),
    )

    # (F circ G) circ H
    fg = paste_certificates(f, g)
    fg_h = paste_certificates(fg, h)

    # F circ (G circ H)
    gh = paste_certificates(g, h)
    f_gh = paste_certificates(f, gh)

    expected_mass = Rational(1, 3) + Rational(1, 5)  # 8/15
    assert fg_h.loss_ledger.loss_mass == expected_mass
    assert f_gh.loss_ledger.loss_mass == expected_mass
    assert fg_h.leg_ledgers == f_gh.leg_ledgers


def test_reviewer_exact_morphism_with_loss_is_invalid():
    """§4.1: EXACT morphisms carrying positive loss are strictly invalid."""
    cert = finite_certificate(
        "Regime_A", "Regime_B", "F_exact_bad", MorphismKind.EXACT, True, True,
        loss_ledger=LossLedger(loss_mass=Rational(1, 3)),
    )
    assert cert.is_valid() is False
    res = evaluate_transport_authority("s", _target_regime(), "art", cert)
    assert res.inhabited is False
    assert res.refusal_code == "R_unpriced_loss"


def test_reviewer_pasting_inconsistent_intermediate_observation_raises():
    """§4.2: Pasting must fail if intermediate observation maps disagree."""
    f = DescentSquareCertificate(
        "A", "B", "F", MorphismKind.EXACT, True, True,
        state_map=lambda x: "mid",
        observation_map=lambda o: "look_F",
        source_look=lambda x: "x",
        target_look=lambda y: "look_F",
        carrier=("x",),
    )
    assert f.is_valid() is True

    g = DescentSquareCertificate(
        "B", "C", "G", MorphismKind.EXACT, True, True,
        state_map=lambda y: "out",
        observation_map=lambda o: "look_G",
        source_look=lambda y: "look_G",  # Disagrees with f.target_look on "mid"
        target_look=lambda z: "look_G",
        carrier=("mid",),
    )
    assert g.is_valid() is True

    with pytest.raises(ValueError, match="intermediate observation/look maps disagree"):
        paste_certificates(f, g)


def test_reviewer_pasting_uncovered_carrier_raises():
    """§4.2: Pasting must fail if intermediate states are not covered by the second leg."""
    f = DescentSquareCertificate(
        "A", "B", "F", MorphismKind.EXACT, True, True,
        state_map=lambda x: "uncovered_state",
        observation_map=lambda o: "look",
        source_look=lambda x: "x",
        target_look=lambda y: "look",
        carrier=("x",),
    )
    assert f.is_valid() is True

    # Second leg only verifies on 'covered_state', disagrees on 'uncovered_state'
    g = DescentSquareCertificate(
        "B", "C", "G", MorphismKind.EXACT, True, True,
        state_map=lambda y: y,
        observation_map=lambda o: "look",
        source_look=lambda y: "look",
        target_look=lambda z: "look" if z == "covered_state" else "other",
        carrier=("covered_state",),
    )
    assert g.is_valid() is True

    with pytest.raises(ValueError, match="not covered"):
        paste_certificates(f, g)



def test_reviewer_pasting_incompatible_defect_vectors_raises():
    """§4.3: Pasting defect vectors of incompatible shapes must raise, not discard the first defect."""
    f = finite_certificate("A", "B", "F", MorphismKind.EXACT, True, True, defect_vector=Matrix([[1]]))
    g = finite_certificate("B", "C", "G", MorphismKind.EXACT, True, True, defect_vector=Matrix([[2], [3]]))
    with pytest.raises(ValueError, match="incompatible defect vector spaces/shapes"):
        paste_certificates(f, g)


def test_reviewer_nonrational_quotient_certificate_fails_verify():
    """§5: Non-rational entries (Float, sqrt(2), Symbol) in QuotientDistanceCertificate must fail verify."""
    from cochain_presentation import QuotientDistanceCertificate
    from sympy import Float, Symbol, sqrt

    for bad_scalar in [Float(1.0), sqrt(2), Symbol("x")]:
        q = QuotientDistanceCertificate(
            distance=Rational(0),
            repair_witness=Matrix([[bad_scalar]]),
            residual=Matrix([[0]]),
            cochain=Matrix([[bad_scalar]]),
            dual_witness=Matrix([[0]]),
            dual_pairing=Rational(0),
            repair_map=Matrix([[bad_scalar]]),
        )
        assert q.verify() is False


def test_reviewer_multicolumn_cochain_fails_verify():
    """§5: Two-column cochain in QuotientDistanceCertificate must fail verify."""
    from cochain_presentation import QuotientDistanceCertificate
    q = QuotientDistanceCertificate(
        distance=Rational(0),
        repair_witness=Matrix([[0]]),
        residual=Matrix([[0, 0]]),
        cochain=Matrix([[0, 0]]),  # 2 columns
        dual_witness=Matrix([[0]]),
        dual_pairing=Rational(0),
        repair_map=Matrix([[1]]),
    )
    assert q.verify() is False


def test_reviewer_quotient_certificate_snapshot_immutable():
    """§5: Mutating caller's quotient certificate must not corrupt returned TransportResult."""
    regime = _target_regime(can_terminalize=True, is_authorized=True)
    d0 = Matrix([[1]])
    cochain = Matrix([[0]])
    q = compute_transport_quotient_obstruction(d0, cochain)
    assert q.distance == 0
    assert q.verify() is True

    cert = finite_certificate("A", "Regime_B", "F", MorphismKind.EXACT, True, True)
    res = evaluate_transport_authority("s", regime, "art", replace(cert, defect_vector=cochain, repair_map=d0), quotient_certificate=q)
    assert res.inhabited is True
    assert res.quotient_certificate is not None
    assert res.quotient_certificate.verify() is True

    # Original and returned records both reject mutation.
    with pytest.raises(TypeError):
        q.cochain[0, 0] = 999
    with pytest.raises(TypeError):
        res.quotient_certificate.cochain[0, 0] = 999
    with pytest.raises(FrozenInstanceError):
        res.quotient_certificate.distance = 999
    cochain[0, 0] = 999
    assert q.verify() is True

    # Result snapshot remains valid and unchanged
    assert res.quotient_certificate.cochain[0, 0] == 0
    assert res.quotient_certificate.verify() is True


def test_reviewer_target_is_auth_truthiness_rejected():
    """§6: target_regime.is_auth returning non-bool truthy values must raise TypeError."""
    for truthy_val in ["False", 1, [False]]:
        regime = TerminalRegime(
            regime_id="Regime_B",
            terminalize=lambda x: "term",
            is_auth=lambda t: truthy_val,  # returns non-bool
        )
        cert = _exact_certificate()
        with pytest.raises(TypeError, match="target_regime.is_auth must return strictly of type bool"):
            evaluate_transport_authority("s", regime, "art", cert)


def test_reviewer_target_terminalize_non_string_rejected():
    """§6: target_regime.terminalize returning non-string must raise TypeError."""
    for bad_term in [123, True, [1]]:
        regime = TerminalRegime(
            regime_id="Regime_B",
            terminalize=lambda x: bad_term,
            is_auth=lambda t: True,
        )
        cert = _exact_certificate()
        with pytest.raises(TypeError, match="target_regime.terminalize must return Optional\\[str\\]"):
            evaluate_transport_authority("s", regime, "art", cert)




