# -*- coding: utf-8 -*-
"""
Pipeline evaluation use case.
Orchestrates sequential data flow through all 9 CODA layers to produce the MasterNormalFormOutcome.

There is one code path. ``evaluate_triad_pipeline`` computes sealed evidence (Layers 1-7,
``compute_evidence``) under a budget and hands it to the authority firewall (Layers 8-9).
``evaluate_coda_pipeline`` is the same path with an internal proposal, so the two entry
points cannot disagree on a terminal. The budget is the smaller of the caller's limit and
the proposal's declared ``budget_limit_seconds``, and it interrupts the exact solver.

AuthorityEffect: None.
"""

from __future__ import annotations

import dataclasses
import time
from typing import Any, Optional, Tuple

from coda_application.domain.l1_quotient import FunctionalEvaluator
from coda_application.domain.authority import AuthorityGrant, AuthorityKeyring
from coda_application.domain.budget import NonTerminalBudgetGuard
from coda_application.domain.contracts import (
    AuthorityContract,
    EvaluationContract,
    ProposalContract,
)
from coda_application.domain.entities import MasterNormalFormOutcome, ProblemInstance
from coda_application.domain.evaluator import compute_evidence
from coda_application.domain.firewall_engine import AuthorityFirewallEngine

DIRECT_PROPOSER = "direct-pipeline"


def _guard(max_seconds: float, max_steps: int, proposal: Optional[ProposalContract]) -> NonTerminalBudgetGuard:
    seconds = max_seconds
    if proposal is not None and proposal.budget_limit_seconds is not None:
        declared = proposal.budget_limit_seconds.fraction
        if declared < seconds:
            seconds = declared
    return NonTerminalBudgetGuard(max_seconds=seconds, max_steps=max_steps, clock=time.perf_counter)


def evaluate_evidence(
    problem: ProblemInstance,
    max_seconds: float = NonTerminalBudgetGuard.DEFAULT_MAX_SECONDS,
    max_steps: int = NonTerminalBudgetGuard.DEFAULT_MAX_STEPS,
    *, evaluator: FunctionalEvaluator,
) -> EvaluationContract:
    """Sealed evidence for ``problem`` (Layers 1-7); an external authority grants against it."""
    guard = _guard(max_seconds, max_steps, None)
    with guard:
        return compute_evidence(problem, guard, evaluator=evaluator)


def evaluate_triad_pipeline(
    proposal: ProposalContract,
    caller_role: Any = "PROPOSER",
    external_license_granted: Any = None,
    is_self_referential_or_undecidable: Any = None,
    max_seconds: float = NonTerminalBudgetGuard.DEFAULT_MAX_SECONDS,
    max_steps: int = NonTerminalBudgetGuard.DEFAULT_MAX_STEPS,
    keyring: Optional[AuthorityKeyring] = None,
    *, evaluator: FunctionalEvaluator,
) -> Tuple[EvaluationContract, AuthorityContract]:
    """
    Executes the Triad Proposal-Evaluation-Authority workflow.

    1. Enforces the non-terminal budget (time and steps), including the proposal's own limit.
    2. Runs Layers 1-7 to produce sealed evidence (E).
    3. Passes the evidence through the 7 halt guards to emit the AuthorityContract (T).
    """
    guard = _guard(max_seconds, max_steps, proposal)
    with guard:
        evidence = compute_evidence(proposal.problem, guard, evaluator=evaluator)
    authority = AuthorityFirewallEngine.evaluate_authority(
        functional_evaluator=evaluator,
        proposal=proposal,
        evaluation=evidence,
        problem=proposal.problem,
        caller_role=caller_role,
        external_license_granted=external_license_granted,
        is_self_referential_or_undecidable=is_self_referential_or_undecidable,
        keyring=keyring,
        max_seconds=max_seconds,
        max_steps=max_steps,
        clock=time.perf_counter,
    )
    return evidence, authority


def evaluate_coda_pipeline(
    problem: ProblemInstance,
    grant: Optional[AuthorityGrant] = None,
    keyring: Optional[AuthorityKeyring] = None,
    max_seconds: float = NonTerminalBudgetGuard.DEFAULT_MAX_SECONDS,
    max_steps: int = NonTerminalBudgetGuard.DEFAULT_MAX_STEPS,
    *, evaluator: FunctionalEvaluator,
) -> MasterNormalFormOutcome:
    """Passes the problem instance through all 9 layers (the triad path with an internal proposal).

    ``problem.fda_license_granted`` is treated as a license claim: a bare value never
    authorizes. Authorization needs ``grant`` (signed by an authority in ``keyring`` for
    this problem's evidence).
    """
    claim = grant if grant is not None else getattr(problem, "fda_license_granted", None)
    proposer = grant.licensee if isinstance(grant, AuthorityGrant) else DIRECT_PROPOSER
    unclaimed = dataclasses.replace(problem, fda_license_granted=False) if isinstance(problem, ProblemInstance) else problem
    proposal = ProposalContract(proposer_id=proposer, problem=unclaimed)
    _evidence, authority = evaluate_triad_pipeline(
        proposal,
        caller_role="PROPOSER",
        external_license_granted=claim,
        max_seconds=max_seconds,
        max_steps=max_steps,
        keyring=keyring,
        evaluator=evaluator,
    )
    return authority.outcome


class CodaPipelineEvaluator:
    """Executes the complete 9-layer CODA evaluation pipeline."""

    @classmethod
    def evaluate(cls, problem: ProblemInstance, grant: Optional[AuthorityGrant] = None,
                 keyring: Optional[AuthorityKeyring] = None, *, evaluator: FunctionalEvaluator) -> MasterNormalFormOutcome:
        """Passes the problem instance through all 9 layers deterministically."""
        return evaluate_coda_pipeline(problem, grant=grant, keyring=keyring, evaluator=evaluator)
