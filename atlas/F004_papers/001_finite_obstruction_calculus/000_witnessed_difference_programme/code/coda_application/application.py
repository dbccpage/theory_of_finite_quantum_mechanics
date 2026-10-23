"""Composition root for canonical native evaluation and separate authorization."""
from __future__ import annotations
from typing import Any, Optional, Tuple
from sympy import Matrix
from coda_application.domain.authority import AuthorityGrant, AuthorityKeyring
from coda_application.domain.budget import NonTerminalBudgetGuard
from coda_application.domain.contracts import EvaluationContract, ProposalContract, AuthorityContract
from coda_application.domain.entities import MasterNormalFormOutcome, ProblemInstance
from coda_application.infrastructure.native_functional_adapter import NativeFunctionalEvaluator
from coda_application.use_cases import evaluate_pipeline as pipeline
from coda_application.use_cases import solve_l1_repair as repair
from coda_application.use_cases import audit_firewall as audit


def evaluate_evidence(problem: ProblemInstance, max_seconds: float=NonTerminalBudgetGuard.DEFAULT_MAX_SECONDS, max_steps: int=NonTerminalBudgetGuard.DEFAULT_MAX_STEPS):
    return pipeline.evaluate_evidence(problem=problem, max_seconds=max_seconds, max_steps=max_steps, evaluator=NativeFunctionalEvaluator())


def evaluate_triad_pipeline(proposal: ProposalContract, caller_role: Any='PROPOSER', external_license_granted: Any=None, is_self_referential_or_undecidable: Any=None, max_seconds: float=NonTerminalBudgetGuard.DEFAULT_MAX_SECONDS, max_steps: int=NonTerminalBudgetGuard.DEFAULT_MAX_STEPS, keyring: Optional[AuthorityKeyring]=None):
    return pipeline.evaluate_triad_pipeline(proposal=proposal, caller_role=caller_role, external_license_granted=external_license_granted, is_self_referential_or_undecidable=is_self_referential_or_undecidable, max_seconds=max_seconds, max_steps=max_steps, keyring=keyring, evaluator=NativeFunctionalEvaluator())


def evaluate_coda_pipeline(problem: ProblemInstance, grant: Optional[AuthorityGrant]=None, keyring: Optional[AuthorityKeyring]=None, max_seconds: float=NonTerminalBudgetGuard.DEFAULT_MAX_SECONDS, max_steps: int=NonTerminalBudgetGuard.DEFAULT_MAX_STEPS):
    return pipeline.evaluate_coda_pipeline(problem=problem, grant=grant, keyring=keyring, max_seconds=max_seconds, max_steps=max_steps, evaluator=NativeFunctionalEvaluator())


def solve_exact_l1_repair(d: Matrix, cochain: Matrix):
    return repair.solve_exact_l1_repair(d=d, cochain=cochain, evaluator=NativeFunctionalEvaluator())


def _certificate_checks(problem: ProblemInstance, outcome: MasterNormalFormOutcome):
    return audit._certificate_checks(problem=problem, outcome=outcome, evaluator=NativeFunctionalEvaluator())


def audit_authority_firewall(problem: ProblemInstance, grant: Optional[AuthorityGrant]=None, keyring: Optional[AuthorityKeyring]=None):
    return audit.audit_authority_firewall(problem=problem, grant=grant, keyring=keyring, evaluator=NativeFunctionalEvaluator())


class CodaPipelineEvaluator:
    evaluate = staticmethod(evaluate_coda_pipeline)
