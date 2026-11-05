# -*- coding: utf-8 -*-
"""
test_high_dim_stress.py: End-to-end stress tests piping high-dimensional graph instances
through CODA: bounded certificate checks, large fixture shapes, and budget refusal.

AuthorityEffect: None.
"""

from __future__ import annotations

import dataclasses
import pytest
from coda_application.application import _certificate_checks
import random
import time
from sympy import Matrix, Rational

from coda_application.domain.anomalon_registry import AnomalonRegistry
from coda_application.domain.contracts import ProposalContract
from coda_application.domain.entities import TerminalKind
from coda_application.domain.value_objects import FirewallDecision
from coda_application.infrastructure.rust_bridge import RustCrateBridge
from coda_application.presentation.cli import cmd_stress_test
from coda_application.tests._authority import granted
from coda_application.application import evaluate_coda_pipeline, evaluate_triad_pipeline


def _conservative(prob, v, chord):
    """The same instance with an exact coboundary defect: potential f(i) = i."""
    edges = [(i, (i + 1) % v) for i in range(v)] + [(i, (i + chord) % v) for i in range(0, v, chord)]
    return dataclasses.replace(prob, defect_cochain=Matrix([Rational(t - s) for s, t in edges]))


@pytest.mark.parametrize(("vertices", "chord"), [(20, 10), (30, 15)])
def test_graph_certificate_has_expected_cycle_value(vertices, chord):
    problem = RustCrateBridge.generate_high_dim_graph_instance(vertices, chord)
    outcome = evaluate_coda_pipeline(problem)
    assert outcome.terminal_kind == TerminalKind.CLOSED_RESIDUAL
    assert outcome.residual_pair.phi1.fraction == vertices
    assert outcome.residual_pair.gamma2.fraction == 0
    assert all(valid for _, valid, _ in _certificate_checks(problem, outcome))


@pytest.mark.parametrize(("vertices", "chord", "edges"), [(1000, 10, 1100), (1500, 15, 1600)])
def test_large_fixture_shape_only(vertices, chord, edges):
    # This checks construction, not solve speed or a performance theorem.
    problem = RustCrateBridge.generate_high_dim_graph_instance(vertices, chord)
    assert problem.d0.shape == (edges, vertices)
    assert problem.defect_cochain.shape == (edges, 1)


def test_conservative_flow_with_grant_and_without_grant():
    vertices = 20
    problem = _conservative(RustCrateBridge.generate_high_dim_graph_instance(vertices, 10), vertices, 10)
    authorized = granted(problem)
    assert authorized.is_authorized and authorized.residual_pair.is_exact_zero
    unlicensed = evaluate_coda_pipeline(problem)
    assert unlicensed.terminal_kind == TerminalKind.REFUSED
    assert unlicensed.authority_token is None


def test_coda_cli_stress_test_entrypoint(capsys):
    assert cmd_stress_test(num_vertices=20, chord_interval=10) == 0
    text = capsys.readouterr().out
    assert "dual_witness: PASS" in text and "gamma2: PASS" in text
    assert "no universal runtime bound" in text


def test_budget_exhaustion_inside_layer_one_refuses():
    """OR-T10 / GTLA-09: an exhausted budget stops Layer 1 mid-solve and terminalizes REFUSED.

    The native process is polled under the budget, so a 0.05 s limit interrupts an exact
    simplex that would otherwise run for seconds. No value is fabricated: the evidence
    reports Phi_1 and Gamma_2 as unknown (None).
    """
    rng = random.Random(20260923)
    rows, cols = 60, 40
    d0 = Matrix(rows, cols, [rng.choice([-2, -1, 0, 1, 2, 3]) for _ in range(rows * cols)])
    base = RustCrateBridge.generate_high_dim_graph_instance(num_vertices=10, chord_interval=0, licensed=False)
    prob = dataclasses.replace(
        base, d0=d0, d1=Matrix.zeros(1, rows), defect_cochain=Matrix([rng.randint(-5, 5) for _ in range(rows)])
    )

    t0 = time.perf_counter()
    evidence, authority = evaluate_triad_pipeline(ProposalContract(proposer_id="stress", problem=prob), max_seconds=0.05)
    elapsed = time.perf_counter() - t0

    assert authority.terminal_kind == TerminalKind.REFUSED
    assert authority.authority_token is None
    assert evidence.phi1 is None and evidence.gamma2 is None
    assert "budget exhausted" in (evidence.refusal_reason or "")
    assert elapsed < 0.5, f"max_seconds=0.05, wall time {elapsed:.2f} s"


def test_budget_exhaustion_by_step_limit_refuses():
    """OR-T10: a step budget exhausts deterministically, independent of machine speed."""
    prob = RustCrateBridge.generate_high_dim_graph_instance(num_vertices=20, chord_interval=10, licensed=False)
    outcome = evaluate_coda_pipeline(prob, max_steps=1)
    assert outcome.terminal_kind == TerminalKind.REFUSED
    assert outcome.residual_pair is None
    assert outcome.authority_token is None


def test_surviving_residual_is_read_back_from_the_register():
    """GTLA-10 / A-T8: a surviving residual is recorded in the persistent Anomalon register.

    The record is read back by fingerprint through a fresh registry handle on the same
    store, so it outlives the handle that wrote it (``reset`` drops the handle only).
    """
    prob = RustCrateBridge.generate_high_dim_graph_instance(num_vertices=20, chord_interval=10, licensed=False)
    outcome = evaluate_coda_pipeline(prob)
    assert outcome.terminal_kind == TerminalKind.CLOSED_RESIDUAL
    assert outcome.residual_pair.phi1.sympy_rational == Rational(20)

    AnomalonRegistry.reset()
    registry = AnomalonRegistry.get_global_registry()
    records = [r for r in registry.list_all() if r.problem_id == prob.problem_id]
    assert len(records) == 1
    assert records[0].phi1.sympy_rational == Rational(20)
    assert records[0].status == "RETAINED_OPEN"
