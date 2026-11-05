# -*- coding: utf-8 -*-
"""
test_coda_firewall.py: Adversarial authority conservation and non-promotion tests for CODA.

AuthorityEffect: None.
"""

from __future__ import annotations

import pytest
from sympy import Matrix, Rational

from coda_application.domain.entities import AuthorityToken, ProblemInstance, TerminalKind
from coda_application.domain.value_objects import FirewallDecision
from coda_application.tests._authority import grant_for
from coda_application.application import audit_authority_firewall
from coda_application.application import evaluate_coda_pipeline


def test_firewall_blocks_zero_defect_unlicensed():
    """
    CRITICAL FIREWALL TEST:
    A problem with zero defect (Phi_1=0, Gamma_2=0) but WITHOUT an external license
    must route to REFUSED and cannot mint an AuthorityToken.
    """
    d0 = Matrix([[-1, 1], [1, -1]])
    d1 = Matrix.zeros(1, 2)
    defect = Matrix([Rational(0), Rational(0)])

    problem = ProblemInstance(
        problem_id="unlicensed_zero_defect",
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
        fda_license_granted=False,  # UNLICENSED
    )

    outcome = evaluate_coda_pipeline(problem)

    assert outcome.terminal_kind != TerminalKind.AUTHORIZED
    assert outcome.terminal_kind == TerminalKind.REFUSED
    assert outcome.authority_token is None
    assert outcome.firewall_decision == FirewallDecision.ROUTE_REFUSED


def test_authority_token_cannot_be_internally_minted():
    """Verifies that AuthorityToken constructor strictly forbids internal creation without external license."""
    with pytest.raises(PermissionError, match="AUTHORITY CONSERVATION BREACH"):
        AuthorityToken(
            token_id="FAKE-001",
            licensee="InternalHeuristicSolver",
            granted_externally=False,  # Internal minting rejected!
            halt_guards_satisfied=True,
        )


def test_token_minting_requires_a_verified_spent_grant():
    """The firewall's minting helper refuses a fabricated grant and an unspent genuine one."""
    from coda_application.domain.authority import AuthorityGrant, _mint_token

    problem = ProblemInstance(
        problem_id="mint_probe",
        raw_data="mint_probe",
        candidate_sieve=("cand1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(1, 2),)},
        overlaps={("U0", "U0"): True},
        d0=Matrix([[-1, 1], [1, -1]]),
        d1=Matrix.zeros(1, 2),
        defect_cochain=Matrix([0, 0]),
    )
    genuine, ring = grant_for(problem)
    fabricated = AuthorityGrant(
        authority_id=genuine.authority_id,
        licensee=genuine.licensee,
        problem_digest=genuine.problem_digest,
        evidence_digest=genuine.evidence_digest,
        nonce="forged-nonce",
        mac="0" * 64,
    )
    with pytest.raises(PermissionError):
        _mint_token(fabricated, ring)
    with pytest.raises(PermissionError):
        _mint_token(genuine, ring)  # verified, but the firewall has not spent its nonce
    assert ring.spend(genuine)
    assert _mint_token(genuine, ring).is_valid()


def test_audit_authority_firewall_suite():
    """Runs the audit_authority_firewall use case across authorized and residual instances."""
    d0 = Matrix([[-1, 1], [1, -1]])
    d1 = Matrix.zeros(1, 2)
    defect = Matrix([Rational(0), Rational(0)])

    prob_licensed = ProblemInstance(
        problem_id="licensed_audit",
        raw_data="data",
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

    grant, ring = grant_for(prob_licensed)
    audit_res = audit_authority_firewall(prob_licensed, grant=grant, keyring=ring)
    assert audit_res["firewall_audit_passed"] is True
    assert audit_res["terminal_kind"] == TerminalKind.AUTHORIZED.value
    assert audit_res["token_issued"] is True
