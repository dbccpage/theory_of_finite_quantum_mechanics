# -*- coding: utf-8 -*-
"""
Shared helpers for the adversarial CODA suite.

Every test asserts an invariant CODA claims for itself (README, docstrings,
docs/test_catalog_and_failure_modes.md, or an F005 claim ID). A test that
exposes a break is marked with ``BREAK(...)``: a strict xfail pinned to the
exception the break raises, so a fix turns it into an XPASS failure and a
different crash is not mistaken for the recorded break.

Phi_1 values are evaluated by omega_functional. Algebraic counterexamples
and fixed expected values provide independent controls; agreement between
two adapters to that same owner is only an integration check.

AuthorityEffect: None.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
from sympy import Matrix, Rational

from coda_application.domain.entities import ProblemInstance
from coda_application.domain.contracts import EvaluationContract, ProposalContract
from coda_application.domain.value_objects import DualWitness, ExactRational

APP_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = next((p for p in APP_ROOT.parents if (p / ".git").exists()), APP_ROOT.parent.parent)


def BREAK(break_id: str, why: str, raises=AssertionError):
    """Strict xfail recording a confirmed break of a claimed CODA invariant."""
    return pytest.mark.xfail(strict=True, raises=raises, reason=f"{break_id}: {why}")


def foc_phi1(d0: Matrix, cochain: Matrix) -> Rational:
    """Canonical native value; independent expected values live in the tests."""
    from coda_application.infrastructure.exact_solver_adapter import ExactSolverAdapter
    value, _, _ = ExactSolverAdapter.compute_quotient_distance(d0, cochain)
    return Rational(value.numerator, value.denominator)


GRAPH_D0 = Matrix([[-1, 1], [1, -1]])


def make_problem(**overrides) -> ProblemInstance:
    """A benign licensed-or-not instance; every field can be overridden."""
    cochain = overrides.pop("defect_cochain", Matrix([0, 0]))
    fields = dict(
        problem_id="adv",
        raw_data="adversarial",
        candidate_sieve=("cand",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(1, 2),)},
        overlaps={("U0", "U0"): True},
        d0=GRAPH_D0,
        d1=Matrix.zeros(1, cochain.rows) if hasattr(cochain, "rows") else Matrix.zeros(1, 2),
        defect_cochain=cochain,
        fda_license_granted=False,
    )
    fields.update(overrides)
    return ProblemInstance(**fields)


ZERO = ExactRational(0, 1)


def er(value) -> ExactRational:
    return ExactRational.from_rational(value)


def witness(*entries) -> DualWitness:
    """Proposed witness data; the native evaluator must check its feasibility."""
    values = [Rational(e) for e in entries]
    return DualWitness(
        witness_vector=tuple((int(v.p), int(v.q)) for v in values),
        pairing_value=ZERO,
    )


def evaluation(problem_id="adv", phi1=0, gamma2=0, dual_witness=None, valid=True,
               records=(), budget=True) -> EvaluationContract:
    """Unsealed proposed evidence; the firewall must recompute it through its trusted evaluator."""
    return EvaluationContract(
        problem_id=problem_id,
        phi1=er(phi1),
        gamma2=er(gamma2),
        dual_witness=dual_witness,
        is_mathematically_valid=valid,
        layer_records=tuple(records),
        elapsed_seconds=ZERO,
        budget_satisfied=budget,
    )


def proposal(problem=None, proposer_id="proposer") -> ProposalContract:
    return ProposalContract(proposer_id=proposer_id, problem=problem or make_problem())


def obstructed_problem(**overrides) -> ProblemInstance:
    """d0 = [[1], [-1]], omega = [1, 1]; true Phi_1 = 2, witness y = [1, 1]."""
    overrides.setdefault("d0", Matrix([[1], [-1]]))
    overrides.setdefault("defect_cochain", Matrix([1, 1]))
    return make_problem(**overrides)


def rejects(fn, *exc_types) -> bool:
    """True when fn refuses its input by raising one of the given validation errors."""
    exc_types = exc_types or (ValueError, TypeError)
    try:
        fn()
    except exc_types:
        return True
    return False


def run_python(args, timeout=120, optimize=False, env_extra=None):
    """Run the current interpreter from the repo root; return CompletedProcess."""
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = os.pathsep.join((str(APP_ROOT.parent), str(REPO_ROOT)))
    if env_extra:
        env.update(env_extra)
    cmd = [sys.executable] + (["-O"] if optimize else []) + list(args)
    return subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True,
                          timeout=timeout, env=env)


def run_cli(*cli_args, timeout=120):
    return run_python(["-m", "coda_application.presentation.cli", *cli_args], timeout=timeout)
