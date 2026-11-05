# -*- coding: utf-8 -*-
"""
Adversarial tests for AuthorityFirewallEngine (firewall_engine.py).

Claims under attack: "Passes proposal and evaluation evidence through all 7 halt
guards"; "Proposers cannot self-grant authority" (Paper 004); "Mathematical
validity alone does NOT grant authorization" (Paper 005); "Verify dual witness
pairing and norm bounds"; AuthorityContract "Guarantees under declared
assumptions that authority tokens require an authenticated external license".
Evidence here is hand-built; the firewall must replay unsealed claims and
bind their source before routing.

AuthorityEffect: None.
"""

from __future__ import annotations

import pytest

from coda_application.infrastructure.native_functional_adapter import NativeFunctionalEvaluator
from coda_application.domain.entities import LayerExecutionRecord, TerminalKind
from coda_application.domain.firewall_engine import AuthorityFirewallEngine as FW
from coda_application.domain.value_objects import ExactRational, LayerId
from coda_application.domain.anomalon_registry import AnomalonRegistry
from coda_application.tests.adversarial._support import (
    evaluation,
    make_problem,
    obstructed_problem,
    proposal,
    witness,
)
from coda_application.application import evaluate_triad_pipeline


def fire(problem, ev, prop=None, **kw):
    return FW.evaluate_authority(functional_evaluator=NativeFunctionalEvaluator(), proposal=prop or proposal(problem), evaluation=ev, problem=problem, **kw)


def zero_ev(**kw):
    return evaluation(phi1=0, gamma2=0, valid=True, **kw)


# ------------------------------------------------------ forged evidence


# FIXED 2026-09-23 (was BREAK FW-01: is_mathematically_valid is trusted: Phi_1 = 2 with a genuine witness is AUTHORIZED)
def test_forged_validity_flag_with_nonzero_phi1():
    p = obstructed_problem()
    auth = fire(p, evaluation(phi1=2, dual_witness=witness(1, 1), valid=True), external_license_granted=True)
    assert auth.terminal_kind != TerminalKind.AUTHORIZED


# FIXED 2026-09-23 (was BREAK FW-02: is_mathematically_valid is trusted: Gamma_2 = 3 is AUTHORIZED (GUARD_4 only rejects negatives))
def test_forged_validity_flag_with_nonzero_gamma2():
    auth = fire(make_problem(), evaluation(gamma2=3, valid=True), external_license_granted=True)
    assert auth.terminal_kind != TerminalKind.AUTHORIZED


# FIXED 2026-09-23 (was BREAK FW-03: GUARD_3 checks only the pairing: a witness outside ker(D0^T) certifies a registered anomalon)
def test_witness_outside_left_kernel_refused():
    p = obstructed_problem()  # D0 = [[1], [-1]]; y = [2, 0] pairs to 2 but D0^T y = 2
    auth = fire(p, evaluation(phi1=2, dual_witness=witness(2, 0), valid=False))
    assert auth.terminal_kind == TerminalKind.REFUSED


# FIXED 2026-09-23 (was BREAK FW-04: GUARD_3 never checks ||y||_inf <= 1: y = [100, 100] inflates Phi_1 from 2 to 200)
def test_unbounded_witness_refused():
    p = obstructed_problem()
    auth = fire(p, evaluation(phi1=200, dual_witness=witness(100, 100), valid=False))
    assert auth.terminal_kind == TerminalKind.REFUSED


# FIXED 2026-09-23 (was BREAK FW-05: the inflated Phi_1 = 200 is written into the anomalon register as fact)
def test_inflated_phi1_not_registered():
    p = obstructed_problem()
    fire(p, evaluation(phi1=200, dual_witness=witness(100, 100), valid=False))
    phis = [r.phi1.sympy_rational for r in AnomalonRegistry.get_global_registry().list_all()]
    assert 200 not in phis


# FIXED 2026-09-23 (was BREAK FW-06: a negative Phi_1 skips GUARD_3 (phi1 > 0 test) and is AUTHORIZED)
def test_negative_phi1_refused():
    auth = fire(make_problem(), evaluation(phi1=-3, valid=True), external_license_granted=True)
    assert auth.terminal_kind == TerminalKind.REFUSED


# FIXED 2026-09-23 (was BREAK FW-07: GUARD_2 validates .sympy_rational, already a Rational: a float-born ExactRational(1.5, 1) passes)
def test_guard2_catches_float_born_scalars():
    """A float-born scalar never reaches GUARD_2: ExactRational refuses the float field (EXA-09)."""
    from coda_application.tests.adversarial._support import rejects

    assert rejects(lambda: ExactRational(1.5, 1), TypeError, ValueError)


# FIXED 2026-09-23 (was BREAK FW-08: a garbage witness rides along on an AUTHORIZED outcome when Phi_1 = 0 (GUARD_3 skipped))
def test_authorized_outcome_carries_no_unverified_witness():
    auth = fire(make_problem(), zero_ev(dual_witness=witness(7, -7, 7)), external_license_granted=True)
    assert auth.outcome.dual_witness is None or auth.terminal_kind != TerminalKind.AUTHORIZED


# FIXED 2026-09-23 (was BREAK FW-09: layer records are ignored: evidence carrying a FAILED OR refusal record is AUTHORIZED)
def test_failed_refusal_record_blocks_authorization():
    refused = LayerExecutionRecord(
        layer_id=LayerId.OR, succeeded=False, diagnostic_message="OR Hard Refusal", defect_mass=ExactRational(1, 1)
    )
    auth = fire(make_problem(), zero_ev(records=(refused,)), external_license_granted=True)
    assert auth.terminal_kind != TerminalKind.AUTHORIZED


# FIXED 2026-09-23 (was BREAK FW-10: is_valid=False with zero defects crashes the registry with ValueError instead of a refusal)
def test_invalid_zero_evidence_refused_not_crashed():
    auth = fire(make_problem(), evaluation(phi1=0, gamma2=0, valid=False))
    assert auth.terminal_kind == TerminalKind.REFUSED


# ------------------------------------------------------ instance mixing


# FIXED 2026-09-23 (was BREAK FW-11: evaluation.problem_id is never matched: evidence for A authorizes obstructed problem B)
def test_evaluation_for_other_problem_rejected():
    b = obstructed_problem(problem_id="B")
    auth = fire(b, zero_ev(problem_id="A"), external_license_granted=True)
    assert auth.terminal_kind != TerminalKind.AUTHORIZED


# FIXED 2026-09-23 (was BREAK FW-12: proposal.problem and problem are never matched: a proposal for A yields a token for B)
def test_proposal_for_other_problem_rejected():
    a, b = make_problem(problem_id="A"), obstructed_problem(problem_id="B")
    ev, _ = evaluate_triad_pipeline(proposal(a))
    auth = FW.evaluate_authority(functional_evaluator=NativeFunctionalEvaluator(), proposal=proposal(a), evaluation=ev, problem=b, external_license_granted=True)
    assert auth.terminal_kind != TerminalKind.AUTHORIZED


# ------------------------------------------------------- caller roles


# FIXED 2026-09-23 (was BREAK FW-13: unknown caller roles pass GUARD_1 untouched (fail-open role check))
def test_unknown_role_refused():
    auth = fire(make_problem(), zero_ev(), caller_role="ADMIN")
    assert auth.terminal_kind == TerminalKind.REFUSED


# FIXED 2026-09-23 (was BREAK FW-14: 'AUTHORITY ' with a trailing space dodges the impersonation check)
def test_whitespace_authority_role_refused():
    auth = fire(make_problem(), zero_ev(), caller_role="AUTHORITY ")
    assert "HALT_GUARD_1" in auth.decision_reason


# FIXED 2026-09-23 (was BREAK FW-15: 'AUTHΟRITY' with a Greek Omicron dodges the impersonation check)
def test_homoglyph_authority_role_refused():
    auth = fire(make_problem(), zero_ev(), caller_role="AUTHΟRITY")
    assert "HALT_GUARD_1" in auth.decision_reason


def test_lowercase_authority_role_refused():
    """HELD: role matching upper-cases, so 'authority' without a license is refused."""
    auth = fire(make_problem(), zero_ev(), caller_role="authority")
    assert "HALT_GUARD_1" in auth.decision_reason


# FIXED 2026-09-23 (was BREAK FW-16: caller_role=None crashes with AttributeError instead of a refusal)
def test_none_role_refused_not_crashed():
    auth = fire(make_problem(), zero_ev(), caller_role=None)
    assert auth.terminal_kind == TerminalKind.REFUSED


# FIXED 2026-09-23 (was BREAK FW-17: the PROPOSER role obtains AUTHORIZED simply by passing external_license_granted=True)
def test_proposer_cannot_obtain_authority():
    auth = fire(make_problem(), zero_ev(), caller_role="PROPOSER", external_license_granted=True)
    assert auth.terminal_kind != TerminalKind.AUTHORIZED


# FIXED 2026-09-23 (was BREAK FW-18: the minted token names the proposer as its own licensee (self-licensing))
def test_token_licensee_is_not_the_proposer():
    auth = fire(make_problem(), zero_ev(), prop=proposal(proposer_id="mallory"), external_license_granted=True)
    assert auth.authority_token is None or auth.authority_token.licensee != "mallory"


# ----------------------------------------------------- license typing


# FIXED 2026-09-23 (was BREAK FW-19: external_license_granted is truth-tested: non-bool truthy values authorize)
@pytest.mark.parametrize("license_value", ["false", "0", [False]], ids=["str-false", "str-0", "list-false"])
def test_license_must_be_a_real_grant(license_value):
    auth = fire(make_problem(), zero_ev(), external_license_granted=license_value)
    assert auth.terminal_kind != TerminalKind.AUTHORIZED


def test_self_reference_flag_as_string_fails_closed():
    """HELD: a truthy string for is_self_referential_or_undecidable halts into refusal."""
    auth = fire(make_problem(), zero_ev(), is_self_referential_or_undecidable="False")
    assert auth.terminal_kind == TerminalKind.REFUSED


# --------------------------------------------------- decorative guards


# FIXED 2026-09-23 (was BREAK FW-20: GUARD_5 (Authority Gap) has no refusal path: it is appended unconditionally)
def test_guard5_can_refuse():
    import inspect

    assert "HALT_GUARD_5" in inspect.getsource(inspect.getmodule(FW))


# FIXED 2026-09-23 (was BREAK FW-21: halt_guards_passed lists GUARD_3 as passed when no witness was checked (Phi_1 = 0))
def test_vacuous_guard_not_reported_as_passed():
    auth = fire(make_problem(), zero_ev(), external_license_granted=True)
    assert FW.GUARD_3_DUAL_WITNESS_VALIDATION not in auth.halt_guards_passed


# ------------------------------------------------------ controls (HELD)


def test_budget_exhaustion_refused():
    """HELD: budget_satisfied=False halts into GUARD_6 refusal."""
    auth = fire(make_problem(), zero_ev(budget=False), external_license_granted=True)
    assert auth.terminal_kind == TerminalKind.REFUSED and "GUARD_6" in auth.decision_reason


def test_missing_witness_refused():
    """HELD: Phi_1 > 0 without a witness is refused by GUARD_3."""
    auth = fire(obstructed_problem(), evaluation(phi1=2, valid=False))
    assert auth.terminal_kind == TerminalKind.REFUSED and "GUARD_3" in auth.decision_reason


def test_witness_shape_mismatch_refused():
    """HELD: a witness of the wrong length is refused by GUARD_3."""
    auth = fire(obstructed_problem(), evaluation(phi1=2, dual_witness=witness(1, 1, 0), valid=False))
    assert "shape mismatch" in auth.decision_reason


def test_wrong_pairing_refused():
    """HELD: a witness whose pairing differs from Phi_1 is refused."""
    auth = fire(obstructed_problem(), evaluation(phi1=3, dual_witness=witness(1, 1), valid=False))
    assert auth.terminal_kind == TerminalKind.REFUSED


def test_self_referential_envelope_refused():
    """HELD: GUARD_7 refuses a self-referential envelope even with a license."""
    auth = fire(make_problem(), zero_ev(), external_license_granted=True, is_self_referential_or_undecidable=True)
    assert "GUARD_7" in auth.decision_reason


def test_authority_role_without_license_refused():
    """HELD: GUARD_1 refuses an unlicensed AUTHORITY caller."""
    auth = fire(make_problem(), zero_ev(), caller_role="AUTHORITY")
    assert "HALT_GUARD_1" in auth.decision_reason


def test_zero_defect_unlicensed_not_authorized():
    """HELD: GTLA-T9 Non-Promotion Firewall routes unlicensed zero-defect evidence to REFUSED."""
    auth = fire(make_problem(), zero_ev())
    assert auth.terminal_kind == TerminalKind.REFUSED and auth.authority_token is None


def test_negative_gamma2_refused():
    """HELD: GUARD_4 refuses a negative cocycle defect."""
    auth = fire(make_problem(), evaluation(gamma2=-1, valid=False))
    assert "GUARD_4" in auth.decision_reason


def test_genuine_residual_registered():
    """HELD: a correctly certified residual is retained as an anomalon with a fingerprint."""
    auth = fire(obstructed_problem(), evaluation(phi1=2, dual_witness=witness(1, 1), valid=False))
    assert auth.terminal_kind == TerminalKind.CLOSED_RESIDUAL and auth.anomalon_fingerprint


def test_rejected_dual_is_not_recorded_as_a_passed_guard():
    from coda_application.domain.firewall_engine import AuthorityFirewallEngine as FW
    from coda_application.infrastructure.native_functional_adapter import NativeFunctionalEvaluator
    from coda_application.tests.adversarial._support import obstructed_problem, evaluation, proposal, witness

    problem = obstructed_problem()
    result = FW.evaluate_authority(
        proposal=proposal(problem), problem=problem,
        evaluation=evaluation(phi1=2, gamma2=0, dual_witness=witness(-1, -1), valid=False),
        functional_evaluator=NativeFunctionalEvaluator(),
    )
    assert result.terminal_kind.value == "REFUSED"
    assert "HALT_GUARD_3_BREACH" in result.decision_reason
    assert FW.GUARD_3_DUAL_WITNESS_VALIDATION not in result.halt_guards_passed


@pytest.mark.parametrize("sealed", [False, True])
def test_exhausted_reverification_budget_is_not_recorded_as_passed(sealed):
    from coda_application.application import evaluate_evidence

    problem = obstructed_problem() if sealed else make_problem()
    ev = evaluate_evidence(problem) if sealed else evaluation()
    result = fire(problem, ev, max_steps=1)
    assert result.terminal_kind is TerminalKind.REFUSED
    assert "HALT_GUARD_6_BREACH" in result.decision_reason
    assert FW.GUARD_6_NON_TERMINAL_BUDGET not in result.halt_guards_passed


def test_contradictory_evidence_is_not_recorded_as_a_passed_guard():
    result = fire(make_problem(), evaluation(valid=False))
    assert result.terminal_kind is TerminalKind.REFUSED
    assert "HALT_GUARD_2_BREACH" in result.decision_reason
    assert FW.GUARD_2_EXACT_ARITHMETIC not in result.halt_guards_passed
