# -*- coding: utf-8 -*-
"""
test_triad_and_foundations.py: Tests for Proposal-Evaluation-Authority triad and F004 boundaries.

Covers:
- Paper 004: Role Non-Impersonation (P, E, A separation)
- Paper 005: The Authority Gap (Verification != Authorization)
- Paper 027: The Authority Firewall (7 Halt Guards, Coproduct separation)
- Paper 028: Finite Authority & Non-Terminal Computation (Budget guards)
- Paper 029: The Anomalon Boundary (Cokernel registration & anti-smoothing)
- Paper 030: Authority Firewall and Verification Limits (Fail-closed limits)

AuthorityEffect: None.
"""

from __future__ import annotations

import pytest
from sympy import Matrix, Rational

from coda_application.domain.anomalon_registry import AnomalonRegistry
from coda_application.domain.budget import BudgetExhaustedError, NonTerminalBudgetGuard
from coda_application.domain.contracts import (
    AuthorityContract,
    EvaluationContract,
    ProposalContract,
)
from coda_application.domain.entities import ProblemInstance, TerminalKind
from coda_application.domain.value_objects import ExactRational
from coda_application.tests._authority import grant_for
from coda_application.application import evaluate_triad_pipeline


@pytest.fixture(autouse=True)
def reset_registry():
    """Ensure clean registry state before each test."""
    AnomalonRegistry.reset()
    yield
    AnomalonRegistry.reset()


def make_zero_defect_problem(problem_id: str = "zero_defect_test") -> ProblemInstance:
    d0 = Matrix([[-1, 1], [1, -1]])
    d1 = Matrix.zeros(1, 2)
    defect = Matrix([Rational(0), Rational(0)])
    return ProblemInstance(
        problem_id=problem_id,
        raw_data="clean_data",
        candidate_sieve=("cand1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(1, 2),)},
        overlaps={("U0", "U0"): True},
        d0=d0,
        d1=d1,
        defect_cochain=defect,
        fda_license_granted=False,
    )


def make_surviving_defect_problem(problem_id: str = "surviving_defect_test") -> ProblemInstance:
    # d0 column has sum zero, so defect [1, 1]^T cannot be repaired by d0
    d0 = Matrix([[1], [-1]])
    d1 = Matrix.zeros(1, 2)
    defect = Matrix([Rational(1), Rational(1)])
    return ProblemInstance(
        problem_id=problem_id,
        raw_data="obstructed_data",
        candidate_sieve=("cand1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(1, 2),)},
        overlaps={("U0", "U0"): True},
        d0=d0,
        d1=d1,
        defect_cochain=defect,
        fda_license_granted=False,
    )


def test_role_non_impersonation_proposer():
    """
    Paper 004: a proposer submits strictly as PROPOSER.
    It cannot claim authority or mint authority tokens.

    (The Alpha client's own boundary test lives in apps/alpha/tests: apps/coda does not
    import a sibling app.)
    """
    problem = make_zero_defect_problem("alpha_prop_01")

    proposal = ProposalContract(
        proposer_id="alpha_agent_001",
        problem=problem,
        candidate_hypotheses=("H1_connected", "H2_conservative"),
        budget_limit_seconds=ExactRational(2, 1),
    )

    assert proposal.proposer_id == "alpha_agent_001"
    assert "H1_connected" in proposal.candidate_hypotheses

    eval_contract, auth_contract = evaluate_triad_pipeline(
        proposal=proposal, caller_role="PROPOSER", external_license_granted=False
    )

    assert isinstance(eval_contract, EvaluationContract)
    assert isinstance(auth_contract, AuthorityContract)
    assert eval_contract.is_mathematically_valid is True

    # Even though mathematically valid, Alpha cannot self-authorize
    assert auth_contract.terminal_kind != TerminalKind.AUTHORIZED
    assert auth_contract.terminal_kind == TerminalKind.REFUSED
    assert auth_contract.authority_token is None


def test_authority_gap_invariant():
    """
    Paper 005: Mathematical verification != Normative authorization.
    Phi_1 = 0 and Gamma_2 = 0 alone does NOT grant authorization without an external license.
    """
    problem = make_zero_defect_problem("gap_test")
    proposal = ProposalContract(proposer_id="test_proposer", problem=problem)

    # 1. Unlicensed submission: valid math, but REFUSED per GTLA-T9
    eval_c, auth_c = evaluate_triad_pipeline(
        proposal=proposal,
        external_license_granted=False,
    )
    assert eval_c.is_mathematically_valid is True
    assert auth_c.is_authorized is False
    assert auth_c.terminal_kind == TerminalKind.REFUSED

    # 2. A bare license claim is not a license: refused, no token.
    _, auth_c_claim = evaluate_triad_pipeline(
        proposal=proposal,
        external_license_granted=True,
    )
    assert auth_c_claim.is_authorized is False
    assert auth_c_claim.terminal_kind == TerminalKind.REFUSED
    assert auth_c_claim.authority_token is None

    # 3. Valid math AND a verified external grant for this evidence -> AUTHORIZED
    grant, ring = grant_for(problem, licensee="test_proposer")
    eval_c_lic, auth_c_lic = evaluate_triad_pipeline(
        proposal=proposal,
        external_license_granted=grant,
        keyring=ring,
    )
    assert eval_c_lic.is_mathematically_valid is True
    assert auth_c_lic.is_authorized is True
    assert auth_c_lic.terminal_kind == TerminalKind.AUTHORIZED
    assert auth_c_lic.authority_token is not None


def test_anomalon_boundary_and_anti_smoothing():
    """
    Paper 029: Surviving cokernel defect is retained as a typed anomalon with SHA-256 fingerprint.
    Zero defects cannot be registered.
    """
    problem = make_surviving_defect_problem("anomalon_01")
    proposal = ProposalContract(proposer_id="test_proposer", problem=problem)

    eval_c, auth_c = evaluate_triad_pipeline(
        proposal=proposal,
        external_license_granted=False,
    )

    assert eval_c.has_residual is True
    assert auth_c.terminal_kind == TerminalKind.CLOSED_RESIDUAL
    assert auth_c.anomalon_fingerprint is not None

    # Check registry retains the anomalon
    registry = AnomalonRegistry.get_global_registry()
    assert registry.count() == 1
    record = registry.get(auth_c.anomalon_fingerprint)
    assert record is not None
    assert record.problem_id == "anomalon_01"
    assert record.status == "RETAINED_OPEN"

    # Anti-smoothing check: zero defects refuse registration
    with pytest.raises(ValueError, match="ANOMALON REGISTRY REFUSAL"):
        registry.register_anomalon(
            problem_id="fake_zero",
            phi1=ExactRational.from_rational(0),
            gamma2=ExactRational.from_rational(0),
            d0=problem.d0,
            d1=problem.d1,
            defect=problem.defect_cochain,
            dual_witness=None,
        )


def test_non_terminal_budget_guard():
    """
    Paper 028: Non-terminal computation budget limits.
    Budget timeout halts closed into REFUSED with BudgetUnknown reason.
    """
    guard = NonTerminalBudgetGuard(max_seconds=0.0001, max_steps=5)

    with pytest.raises(BudgetExhaustedError, match="BUDGET EXHAUSTION"):
        with guard:
            for _ in range(10):
                guard.tick(1)

    # In pipeline evaluation, tight budget halts closed
    problem = make_zero_defect_problem("budget_test")
    proposal = ProposalContract(proposer_id="test_proposer", problem=problem)

    eval_c, auth_c = evaluate_triad_pipeline(
        proposal=proposal,
        max_seconds=0.000001,  # Force immediate budget exhaustion
    )

    assert eval_c.budget_satisfied is False
    assert auth_c.terminal_kind == TerminalKind.REFUSED
    assert "HALT_GUARD_6_BREACH" in auth_c.decision_reason


def test_verification_limits_firewall():
    """
    Paper 030: Self-referential or undecidable authorization envelopes halt closed into REFUSED.
    """
    problem = make_zero_defect_problem("undecidable_test")
    proposal = ProposalContract(proposer_id="test_proposer", problem=problem)

    eval_c, auth_c = evaluate_triad_pipeline(
        proposal=proposal,
        external_license_granted=True,
        is_self_referential_or_undecidable=True,
    )

    assert auth_c.terminal_kind == TerminalKind.REFUSED
    assert "HALT_GUARD_7_BREACH" in auth_c.decision_reason
    assert auth_c.authority_token is None


def test_halt_guard_1_role_impersonation_refusal():
    """
    Paper 027 & Paper 004: Caller role impersonating AUTHORITY without grant halts closed.
    """
    problem = make_zero_defect_problem("impersonation_test")
    proposal = ProposalContract(proposer_id="imposter_proposer", problem=problem)

    eval_c, auth_c = evaluate_triad_pipeline(
        proposal=proposal,
        caller_role="AUTHORITY",  # Caller claiming to be authority without license!
        external_license_granted=False,
    )

    assert auth_c.terminal_kind == TerminalKind.REFUSED
    assert "HALT_GUARD_1_BREACH" in auth_c.decision_reason
