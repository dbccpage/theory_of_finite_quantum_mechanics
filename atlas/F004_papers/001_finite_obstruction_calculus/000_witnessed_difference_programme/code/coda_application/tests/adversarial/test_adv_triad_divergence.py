# -*- coding: utf-8 -*-
"""
Adversarial tests for the Proposal -> Evaluation -> Authority triad
(evaluate_triad_pipeline) and the non-terminal budget guard (budget.py).

Claims under attack: the triad and the nine-layer pipeline are two routes to the
same Master Normal Form, so they must agree on the terminal; Paper 004 role
separation ("Proposers cannot self-grant authority"); EvaluationContract is
"Pure epistemic evidence"; Paper 028 ("Execution time T and step count N must
stay strictly within declared bounds", "halts closed into BudgetUnknown /
Refusal"); Paper 030 fail-closed limits.

AuthorityEffect: None.
"""

from __future__ import annotations

import inspect
import random
import time

import pytest
from sympy import Matrix, Rational

from coda_application.domain.budget import BudgetExhaustedError, NonTerminalBudgetGuard
from coda_application.domain.contracts import ProposalContract
from coda_application.domain.entities import TerminalKind
from coda_application.domain.value_objects import ExactRational
from coda_application.tests.adversarial._support import make_problem, obstructed_problem, proposal, rejects
from coda_application.application import evaluate_coda_pipeline, evaluate_triad_pipeline

AUTH, RES, REF = TerminalKind.AUTHORIZED, TerminalKind.CLOSED_RESIDUAL, TerminalKind.REFUSED


def triad(problem, **kw):
    return evaluate_triad_pipeline(proposal(problem), **kw)


# ------------------------------------------------ triad vs pipeline


# FIXED 2026-09-23 (was BREAK TRI-01: the triad discards the Layer-7 refusal: an empty sieve + license is AUTHORIZED (pipeline: REFUSED))
def test_triad_honours_empty_sieve():
    _, auth = triad(make_problem(candidate_sieve=()), external_license_granted=True)
    assert auth.terminal_kind == REF


# FIXED 2026-09-23 (was BREAK TRI-02: the triad ignores declared-incompatible overlaps: AUTHORIZED (pipeline: REFUSED))
def test_triad_honours_incompatible_overlap():
    _, auth = triad(make_problem(overlaps={("U0", "U0"): False}), external_license_granted=True)
    assert auth.terminal_kind == REF


# FIXED 2026-09-23 (was BREAK TRI-03: Gamma_2 > 0 is a registered anomalon in the triad but REFUSED in the pipeline)
def test_triad_and_pipeline_agree_on_incoherent_residual():
    p = make_problem(defect_cochain=Matrix([1, 0]), d1=Matrix([[1, 0]]))
    _, auth = triad(p)
    assert auth.terminal_kind == evaluate_coda_pipeline(p).terminal_kind


# FIXED 2026-09-23 (was BREAK TRI-04: seeded differential: triad and pipeline disagree on unlicensed random instances)
def test_triad_and_pipeline_agree_on_random_instances():
    rng = random.Random(20260923)
    disagreements = []
    for i in range(40):
        p = make_problem(
            problem_id=f"r{i}",
            candidate_sieve=() if rng.random() < 0.3 else ("c",),
            overlaps={("U0", "U0"): rng.random() > 0.3},
            defect_cochain=Matrix([rng.randint(-1, 1), rng.randint(-1, 1)]),
            d1=Matrix([[rng.choice([0, 0, 1]), 0]]),
        )
        a = evaluate_coda_pipeline(p).terminal_kind
        b = triad(p)[1].terminal_kind
        if a != b:
            disagreements.append((i, a.value, b.value))
    assert not disagreements, f"{len(disagreements)}/40: {disagreements[:3]}"


# FIXED 2026-09-23 (was BREAK TRI-05: the triad trace has 7 layer records; the outcome claims a comprehensive 9-layer trace)
def test_triad_trace_covers_nine_layers():
    _, auth = triad(make_problem())
    assert len(auth.outcome.layer_records) == 9


# ------------------------------------------------ proposal integrity


# FIXED 2026-09-23 (was BREAK TRI-06: ProblemInstance is mutable: the license flag is flipped after ProposalContract checked it)
def test_proposal_problem_cannot_be_mutated_after_check():
    prop = proposal(make_problem())

    def mutate():
        prop.problem.fda_license_granted = True

    assert rejects(mutate, AttributeError, TypeError)


# FIXED 2026-09-23 (was BREAK TRI-07: after the TOCTOU flip the same proposal's problem is AUTHORIZED by the plain pipeline)
def test_mutated_proposal_problem_not_authorized():
    prop = proposal(make_problem())
    try:
        prop.problem.fda_license_granted = True
    except (AttributeError, TypeError):
        return
    assert evaluate_coda_pipeline(prop.problem).terminal_kind != AUTH


def test_proposal_rejects_embedded_string_license():
    """HELD: a truthy embedded license (even the string 'yes') is refused at construction."""
    assert rejects(lambda: ProposalContract(proposer_id="p", problem=make_problem(fda_license_granted="yes")), ValueError)


def test_proposal_rejects_empty_proposer():
    """HELD: an empty proposer_id is refused."""
    assert rejects(lambda: ProposalContract(proposer_id="", problem=make_problem()), ValueError)


# FIXED 2026-09-23 (was BREAK TRI-08: ProposalContract.budget_limit_seconds is ignored: a 1 ns budget still runs to AUTHORIZED)
def test_proposal_budget_limit_is_enforced():
    prop = ProposalContract(proposer_id="p", problem=make_problem(), budget_limit_seconds=ExactRational(1, 10**9))
    _, auth = evaluate_triad_pipeline(prop, external_license_granted=True)
    assert auth.terminal_kind == REF


# --------------------------------------------------------- budget guard


# FIXED 2026-09-23 (was BREAK TRI-09: on budget exhaustion the EvaluationContract reports fabricated Phi_1 = Gamma_2 = 1 as evidence)
def test_budget_exhaustion_does_not_fabricate_evidence():
    ev, auth = triad(make_problem(), max_seconds=1e-12)
    assert auth.terminal_kind == REF
    # Unknown evidence is reported as unknown (None), never as a fabricated value.
    assert (ev.phi1 is None and ev.gamma2 is None) or (ev.phi1.sympy_rational, ev.gamma2.sympy_rational) != (1, 1)


# FIXED 2026-09-23 (was BREAK TRI-10: max_seconds = NaN is accepted and can never be exceeded)
def test_budget_rejects_nan():
    assert rejects(lambda: NonTerminalBudgetGuard(max_seconds=float("nan")), ValueError)


# FIXED 2026-09-23 (was BREAK TRI-11: max_seconds = inf is accepted: an unbounded 'finite' budget)
def test_budget_rejects_infinity():
    assert rejects(lambda: NonTerminalBudgetGuard(max_seconds=float("inf")), ValueError)


def test_budget_rejects_negative_seconds():
    """HELD: a negative budget is refused."""
    assert rejects(lambda: NonTerminalBudgetGuard(max_seconds=-1), ValueError)


def test_budget_step_limit_trips():
    """HELD: the step counter raises once max_steps is exceeded."""
    guard = NonTerminalBudgetGuard(max_steps=5)
    with guard:
        with pytest.raises(BudgetExhaustedError):
            guard.tick(6)


def test_tiny_time_budget_refuses():
    """HELD: an exhausted time budget routes to REFUSED via GUARD_6."""
    _, auth = triad(make_problem(), max_seconds=1e-12)
    assert auth.terminal_kind == REF and "GUARD_6" in auth.decision_reason


# FIXED 2026-09-23 (was BREAK TRI-12: the budget is only checked between layers: a 0.05 s budget lets Layer 1 run for seconds)
def test_budget_interrupts_a_long_layer():
    # A general (non-incidence) boundary forces the exact simplex path, which takes seconds.
    rng = random.Random(20260923)
    rows, cols = 60, 40
    d0 = Matrix(rows, cols, [rng.choice([-2, -1, 0, 1, 2, 3]) for _ in range(rows * cols)])
    p = make_problem(d0=d0, defect_cochain=Matrix([rng.randint(-5, 5) for _ in range(rows)]), d1=Matrix.zeros(1, rows))
    start = time.perf_counter()
    _, auth = evaluate_triad_pipeline(ProposalContract(proposer_id="p", problem=p), max_seconds=0.05)
    elapsed = time.perf_counter() - start
    assert auth.terminal_kind == REF
    assert elapsed < 0.5, f"budget 0.05 s, wall time {elapsed:.2f} s"


# FIXED 2026-09-23 (was BREAK TRI-13: the triad exposes no step budget: it ticks 70 steps against a fixed 100,000 limit)
def test_triad_exposes_step_budget():
    assert "max_steps" in inspect.signature(evaluate_triad_pipeline).parameters


# ------------------------------------------------ fail-closed triad


# FIXED 2026-09-23 (was BREAK TRI-14: a wrong-width d1 raises ShapeError out of the triad instead of an AuthorityContract)
def test_triad_refuses_shape_error():
    _, auth = triad(make_problem(defect_cochain=Matrix([1, 0]), d1=Matrix.zeros(1, 3)))
    assert auth.terminal_kind == REF


# FIXED 2026-09-23 (was BREAK TRI-15: a float section raises TypeError out of the triad (only BudgetExhaustedError is caught))
def test_triad_refuses_type_error():
    _, auth = triad(make_problem(local_sections={"U0": (0.5,), "U1": (Rational(1),)}))
    assert auth.terminal_kind == REF


def test_triad_genuine_residual_retained():
    """HELD: a correctly witnessed obstruction is retained as a registered anomalon."""
    _, auth = triad(obstructed_problem())
    assert auth.terminal_kind == RES and auth.anomalon_fingerprint
