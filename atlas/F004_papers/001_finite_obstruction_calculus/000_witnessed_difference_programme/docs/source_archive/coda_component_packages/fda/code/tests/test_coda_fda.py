# -*- coding: utf-8 -*-
"""
Non-vacuous mutation tests for CODA-FDA finite authorization gate.

Lev Landau discipline: each test states the invariant, then a real mutation
must flip the outcome.
Zero Floats Invariant: exact rational numbers only; floats and booleans in
scalar positions strictly raise TypeError.
AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np
import pytest
from coda_fda_core import (
    RESIDUAL_AUTH_STANDING,
    RESIDUAL_GUARD_FAIL_NONZERO,
    RESIDUAL_GUARD_FAIL_OTHER,
    RESIDUAL_NO_PACKET,
    DescentPacket,
    GuardEvidence,
    HaltGuards,
    RefusalCode,
    all_guards_true,
    compute_cochain_residual_quotient,
    derive_guards,
    evaluate_authority,
    evaluate_authorization,
    evidence_from_cochain_repair,
)
from sympy import Matrix, Rational


def _valid_packet() -> DescentPacket:
    return DescentPacket(
        carrier_k="carrier_demo",
        evaluator_class_e=["e0", "e1"],
        verifier_v="verifier_replay_v1",
        terminalizer_tau="tau_standing",
        discipline_lambda="no_self_promote",
    )


def _green_evidence(**overrides) -> GuardEvidence:
    base = dict(
        pipeline_accepted=True,
        replay_deterministic=True,
        residual_mass=Rational(0, 1),
        residual_zero_tol=Rational(0, 1),
        skeleton_preserved=True,
        candidates_checked=2,
        candidates_declared=2,
        pending_lifts=0,
        active_refusal=False,
    )
    base.update(overrides)
    if "checked_candidate_ids" not in overrides:
        checked_n = base.get("candidates_checked", 0)
        if isinstance(checked_n, int) and not isinstance(checked_n, bool):
            base["checked_candidate_ids"] = tuple(f"e{i}" for i in range(checked_n))
    return GuardEvidence(**base)


def test_valid_packet_and_guards_inhabits_authority():
    """Invariant: valid packet + all derived guards green => standing inhabited."""
    packet = _valid_packet()
    result = evaluate_authorization("prop_ok", packet, _green_evidence())
    assert result.inhabited is True
    assert result.refusal_code is None
    assert result.authority_effect == "None"
    assert result.residual_mass == RESIDUAL_AUTH_STANDING
    assert result.guards.is_auth() is True
    assert result.terminal_state == "term_standing_tau_standing_prop_ok"


def test_incomplete_packet_fields_refuse():
    """Invariant: empty carrier invalidates packet even if guards green."""
    bad = DescentPacket(
        carrier_k="",
        evaluator_class_e=["e0"],
        verifier_v="v",
        terminalizer_tau="t",
        discipline_lambda="L",
    )
    assert bad.is_valid() is False
    result = evaluate_authorization("prop_bad", bad, _green_evidence())
    assert result.inhabited is False
    assert result.refusal_code == "R_nopacket"
    assert result.residual_mass == RESIDUAL_NO_PACKET


def test_missing_packet_refuses_even_with_high_confidence():
    """Invariant: logit_confidence never mints standing without packet (GTFDA-03)."""
    result = evaluate_authorization(
        "prop_fluent",
        None,
        _green_evidence(),
        logit_confidence=Rational(999, 1000),
    )
    assert result.inhabited is False
    assert result.refusal_code == "R_nopacket"
    assert result.residual_mass == RESIDUAL_NO_PACKET

    # Same with compatibility entry + all-true guards (caller cannot bypass).
    result2 = evaluate_authority(
        "prop_fluent2",
        None,
        all_guards_true(),
        logit_confidence=Rational(999, 1000),
    )
    assert result2.inhabited is False
    assert result2.refusal_code == "R_nopacket"
    assert result2.residual_mass == RESIDUAL_NO_PACKET


def test_mutation_single_guard_failure_kills_authority():
    """Invariant: flipping any one derived guard kills inhabitation."""
    packet = _valid_packet()
    mutations = [
        dict(pipeline_accepted=False),
        dict(replay_deterministic=False),
        dict(residual_mass=Rational(1, 1)),
        dict(skeleton_preserved=False),
        dict(candidates_checked=1, candidates_declared=2),
        dict(pending_lifts=1),
        dict(active_refusal=True),
    ]
    for mut in mutations:
        result = evaluate_authorization(
            "prop_mut", packet, _green_evidence(**mut)
        )
        assert result.inhabited is False, f"mutation {mut} should refuse"
        assert result.refusal_code in ("R_candidate", "R_unreplayable")


def test_derive_guards_exhaustive_requires_full_coverage():
    """Mutation: partial candidate coverage => exhaustive false."""
    g = derive_guards(
        _green_evidence(candidates_checked=1, candidates_declared=3)
    )
    assert g.exhaustive is False
    assert g.is_auth() is False


def test_compat_evaluate_authority_with_prederived_guards():
    """Compat path: pre-derived all-green guards + valid packet inhabits."""
    result = evaluate_authority("p", _valid_packet(), all_guards_true())
    assert result.inhabited is True
    assert result.refusal_code is None
    assert result.residual_mass == RESIDUAL_AUTH_STANDING

    # Failed pre-derived guards
    bad_guards = HaltGuards(
        accepted=True,
        deterministic=False,
        zero_residual_mass=True,
        skeleton_preserving=True,
        exhaustive=True,
        no_pending_lift=True,
        no_refusal=True,
    )
    res_bad = evaluate_authority("p_bad", _valid_packet(), bad_guards)
    assert res_bad.inhabited is False
    assert res_bad.refusal_code == "R_unreplayable"


def test_zero_declared_candidates_not_exhaustive():
    """Mutation: declared=0 is not exhaustive green."""
    g = derive_guards(
        _green_evidence(candidates_checked=0, candidates_declared=0)
    )
    assert g.exhaustive is False


def test_derive_guards_negative_validation_errors():
    """Invariant: negative candidate, lift, or tolerance counts raise ValueError."""
    with pytest.raises(ValueError, match="candidates_declared must be non-negative"):
        _green_evidence(candidates_declared=-1)

    with pytest.raises(ValueError, match="candidates_checked must be non-negative"):
        _green_evidence(candidates_checked=-1)

    with pytest.raises(ValueError, match="pending_lifts must be non-negative"):
        _green_evidence(pending_lifts=-1)

    with pytest.raises(ValueError, match="residual_zero_tol must be non-negative"):
        _green_evidence(residual_zero_tol=Rational(-1, 1))

    with pytest.raises(ValueError, match="residual_mass must be non-negative"):
        _green_evidence(residual_mass=Rational(-1, 1))


def test_refusal_codes_and_residual_mass_branches():
    """Invariant: test specific refusal code and residual mass assignments."""
    packet = _valid_packet()

    # Non-deterministic guard failure -> R_unreplayable
    res_unrep = evaluate_authorization(
        "p1", packet, _green_evidence(replay_deterministic=False, residual_mass=Rational(1, 1))
    )
    assert res_unrep.refusal_code == "R_unreplayable"
    assert res_unrep.residual_mass == RESIDUAL_GUARD_FAIL_NONZERO

    # Deterministic failure with zero residual mass -> RESIDUAL_GUARD_FAIL_OTHER
    res_other = evaluate_authorization(
        "p2", packet, _green_evidence(pipeline_accepted=False, residual_mass=Rational(0, 1))
    )
    assert res_other.refusal_code == "R_candidate"
    assert res_other.residual_mass == RESIDUAL_GUARD_FAIL_OTHER


def test_unauth_guard_branches_coverage():
    """Test all guard failure branches in evaluate_authorization for 100% coverage."""
    packet = _valid_packet()

    # Non-deterministic guard failure (deterministic=False) -> R_unreplayable
    r1 = evaluate_authorization("p", packet, _green_evidence(replay_deterministic=False))
    assert r1.inhabited is False
    assert r1.refusal_code == "R_unreplayable"

    # Deterministic failure with nonzero residual mass (deterministic=True, zero_residual_mass=False)
    r2 = evaluate_authorization(
        "p", packet, _green_evidence(replay_deterministic=True, residual_mass=Rational(1, 1))
    )
    assert r2.inhabited is False
    assert r2.refusal_code == "R_candidate"
    assert r2.residual_mass == RESIDUAL_GUARD_FAIL_NONZERO

    # Deterministic failure with zero residual mass (deterministic=True, zero_residual_mass=True, pipeline_accepted=False)
    r3 = evaluate_authorization(
        "p",
        packet,
        _green_evidence(replay_deterministic=True, residual_mass=Rational(0, 1), pipeline_accepted=False),
    )
    assert r3.inhabited is False
    assert r3.refusal_code == "R_candidate"
    assert r3.residual_mass == RESIDUAL_GUARD_FAIL_OTHER


def test_strict_float_rejection():
    """Zero Floats Invariant: passing float or boolean as scalar strictly raises TypeError."""
    # float residual_mass
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        _green_evidence(residual_mass=0.0)

    with pytest.raises(TypeError, match="floats strictly forbidden"):
        _green_evidence(residual_mass=1.5)

    # numpy float
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        _green_evidence(residual_mass=np.float64(0.0))

    # bool passed as residual_mass
    with pytest.raises(TypeError, match="got bool"):
        _green_evidence(residual_mass=True)

    # float residual_zero_tol
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        _green_evidence(residual_zero_tol=0.01)

    # bool passed as residual_zero_tol
    with pytest.raises(TypeError, match="got bool"):
        _green_evidence(residual_zero_tol=False)

    # float candidates_checked
    with pytest.raises(TypeError, match="must be an integer"):
        _green_evidence(candidates_checked=1.0)

    # bool candidates_checked
    with pytest.raises(TypeError, match="must be an integer, got bool"):
        _green_evidence(candidates_checked=True)

    # float pending_lifts
    with pytest.raises(TypeError, match="must be an integer"):
        _green_evidence(pending_lifts=0.0)

    # unsupported object type (e.g. list) to residual_mass
    with pytest.raises(TypeError, match="must be an exact rational or integer, got list"):
        _green_evidence(residual_mass=[1, 2])


def test_exact_fraction_and_string_coercion():
    """Fractions and valid string rationals are accepted and converted to sympy Rational."""
    ev = _green_evidence(
        residual_mass=Fraction(1, 3),
        residual_zero_tol="1/2",
    )
    assert ev.residual_mass == Rational(1, 3)
    assert ev.residual_zero_tol == Rational(1, 2)

    with pytest.raises(TypeError, match="string could not be converted"):
        _green_evidence(residual_mass="invalid_not_a_fraction")


def test_cochain_quotient_bridge_zero_residual():
    """
    Homology Theory Bridge: cochain in im(d0) yields exact quotient distance 0.
    Satisfies g3 (zero_residual_mass) with dual certified primal-dual L1 gap 0.
    """
    # Simple coboundary operator d0 : V0 -> V1
    # d0 = [1, -1]^T
    d0 = Matrix([[1], [-1]])
    # omega = [2, -2]^T = 2 * d0 -> distance to im(d0) is 0
    omega = Matrix([[2], [-2]])

    cert = compute_cochain_residual_quotient(d0, omega)
    assert cert.distance == Rational(0, 1)
    assert cert.dual_pairing == Rational(0, 1)
    assert cert.verify() is True

    evidence, quotient_cert = evidence_from_cochain_repair(
        repair_map=d0,
        cochain=omega,
        pipeline_accepted=True,
        replay_deterministic=True,
        skeleton_preserved=True,
        candidates_checked=2,
        candidates_declared=2,
        pending_lifts=0,
        active_refusal=False,
    )
    assert evidence.residual_mass == Rational(0, 1)

    guards = derive_guards(evidence)
    assert guards.zero_residual_mass is True
    assert guards.is_auth() is True

    res = evaluate_authorization("prop_cochain_zero", _valid_packet(), evidence, residual_certificate=quotient_cert)
    assert res.inhabited is True
    assert res.residual_mass == RESIDUAL_AUTH_STANDING
    assert res.residual_certificate is not None
    assert res.residual_certificate.distance == Rational(0, 1)


def test_cochain_quotient_bridge_nonzero_residual():
    """
    Homology Theory Bridge: cochain not in im(d0) yields positive exact quotient distance.
    Fails g3 (zero_residual_mass), triggering refusal with certified distance.
    """
    # d0 = [1, -1]^T
    d0 = Matrix([[1], [-1]])
    # omega = [1, 1]^T -> orthogonal to [1, -1], distance to im(d0) is 2
    omega = Matrix([[1], [1]])

    cert = compute_cochain_residual_quotient(d0, omega)
    assert cert.distance == Rational(2, 1)
    assert cert.dual_pairing == Rational(2, 1)
    assert cert.verify() is True

    evidence, quotient_cert = evidence_from_cochain_repair(
        repair_map=d0,
        cochain=omega,
    )
    assert evidence.residual_mass == Rational(2, 1)

    guards = derive_guards(evidence)
    assert guards.zero_residual_mass is False
    assert guards.is_auth() is False

    res = evaluate_authorization("prop_cochain_nonzero", _valid_packet(), evidence, residual_certificate=quotient_cert)
    assert res.inhabited is False
    assert res.refusal_code == "R_candidate"
    assert res.residual_mass == RESIDUAL_GUARD_FAIL_NONZERO
    assert res.residual_certificate is not None
    assert res.residual_certificate.distance == Rational(2, 1)


def test_strict_bool_type_enforcement():
    """Boolean fields must strictly satisfy type(val) is bool; truthy strings/ints raise TypeError."""
    for bad_bool in ("False", "True", 1, 0, [True], None):
        with pytest.raises(TypeError, match="must be strictly a bool"):
            _green_evidence(pipeline_accepted=bad_bool)

        with pytest.raises(TypeError, match="must be strictly a bool"):
            _green_evidence(replay_deterministic=bad_bool)

        with pytest.raises(TypeError, match="must be strictly a bool"):
            _green_evidence(skeleton_preserved=bad_bool)

        with pytest.raises(TypeError, match="must be strictly a bool"):
            _green_evidence(active_refusal=bad_bool)


def test_g5_candidate_identifier_binding():
    """g5 binds candidate checks to packet.evaluator_class_e."""
    packet = _valid_packet()  # evaluator_class_e is ["e0", "e1"]

    # Exactly matching candidate IDs -> exhaustive True
    ev_ok = _green_evidence(
        candidates_checked=2,
        candidates_declared=2,
        checked_candidate_ids=["e0", "e1"],
    )
    g_ok = derive_guards(ev_ok, packet)
    assert g_ok.exhaustive is True

    # Missing one candidate ID -> exhaustive False
    ev_missing = _green_evidence(
        candidates_checked=1,
        candidates_declared=2,
        checked_candidate_ids=["e0"],
    )
    g_missing = derive_guards(ev_missing, packet)
    assert g_missing.exhaustive is False

    # Disallow duplicates in checked_candidate_ids
    with pytest.raises(ValueError, match="duplicate entries"):
        _green_evidence(checked_candidate_ids=["e0", "e0"])


def test_residual_certificate_validation_and_mismatch_refusal():
    """A forged or contradictory certificate must be refused with R_contradictory_evidence."""
    d0 = Matrix([[1], [-1]])
    omega = Matrix([[2], [-2]])
    cert = compute_cochain_residual_quotient(d0, omega)
    assert cert.verify() is True

    # Distance mismatch between evidence and certificate
    bad_evidence = _green_evidence(residual_mass=Rational(1, 1))  # cert.distance is 0
    res_mismatch = evaluate_authorization(
        "p_mismatch",
        _valid_packet(),
        bad_evidence,
        residual_certificate=cert,
    )
    assert res_mismatch.inhabited is False
    assert res_mismatch.refusal_code == RefusalCode.R_contradictory_evidence.value


def test_refusal_code_enum_membership():
    """Ensure RefusalCode enum constants are available and match expected strings."""
    assert RefusalCode.R_nopacket == "R_nopacket"
    assert RefusalCode.R_candidate == "R_candidate"
    assert RefusalCode.R_unreplayable == "R_unreplayable"
    assert RefusalCode.R_contradictory_evidence == "R_contradictory_evidence"
    assert RefusalCode.R_obstruction == "R_obstruction"

