# -*- coding: utf-8 -*-
"""
Adversarial tests for the nine-layer pipeline (evaluate_coda_pipeline) and the
routing of problem instances into T_auth + T_res + F_term.

Claims under attack: docs catalog PIP-01 ("All 9 layers succeed; outcome
AUTHORIZED"), G4 "Transport loss must equal 0", G5 "Observation profiles must be
fiber-constant", README "fail-closed", Layer 8 "All seven halt guards satisfied",
ProblemInstance field types, and GTLA-T8 (every run ends in exactly one of three
disjoint terminals - so an exception is a fourth, unclaimed outcome).

AuthorityEffect: None.
"""

from __future__ import annotations

import inspect
import re

import pytest
from coda_application.infrastructure.native_functional_adapter import NativeFunctionalEvaluator

from sympy import Matrix, Rational, Symbol

from coda_application.domain.anomalon_registry import AnomalonRegistry
from coda_application.domain.entities import TerminalKind
from coda_application.domain.layers import layer8_fda
from coda_application.domain.layers.layer2_mur import Layer2MUR
from coda_application.domain.layers.layer4_cs_q import Layer4CSQ
from coda_application.tests.adversarial._support import make_problem, obstructed_problem, rejects
from coda_application.application import evaluate_coda_pipeline as run

AUTH, RES, REF = TerminalKind.AUTHORIZED, TerminalKind.CLOSED_RESIDUAL, TerminalKind.REFUSED


def licensed(**kw):
    return make_problem(fda_license_granted=True, **kw)


# ------------------------------------------------------- license typing


# FIXED 2026-09-23 (was BREAK PIPE-01: fda_license_granted is truth-tested: non-bool truthy values mint a token)
@pytest.mark.parametrize("value", ["no", "False", [False]], ids=["str-no", "str-False", "list-False"])
def test_license_flag_must_be_bool_true(value):
    assert run(make_problem(fda_license_granted=value)).terminal_kind != AUTH


def test_license_none_not_authorized():
    """HELD: a falsy None license keeps the instance out of T_auth and routes to REF per GTLA-T9."""
    assert run(make_problem(fda_license_granted=None)).terminal_kind == REF


# ----------------------------------------------- failed layers still pass


# FIXED 2026-09-23 (was BREAK PIPE-02: Layer 5 marks an inverted enclosure [5, 1] as FAILED, yet the run is AUTHORIZED)
def test_inverted_enclosure_blocks_authorization():
    assert run(licensed(enclosure_interval=(Rational(5), Rational(1)))).terminal_kind != AUTH


# FIXED 2026-09-23 (was BREAK PIPE-03: Layer 3 FAILS on an empty projection map, yet the run is AUTHORIZED (catalog G5))
def test_empty_projection_blocks_authorization():
    assert run(licensed(projection_map={})).terminal_kind != AUTH


# FIXED 2026-09-23 (was BREAK PIPE-04: Layer 3 FAILS on a projection outside the coarse profile, yet the run is AUTHORIZED)
def test_inconsistent_fiber_blocks_authorization():
    assert run(licensed(projection_map={0: 9, 1: 9})).terminal_kind != AUTH


# FIXED 2026-09-23 (was BREAK PIPE-05: declared-compatible overlap with measured transport loss 13/2 is AUTHORIZED (catalog G4))
def test_measured_transport_loss_blocks_authorization():
    problem = licensed(
        local_sections={"U0": (Rational(1, 2),), "U1": (Rational(7),)},
        overlaps={("U0", "U1"): True},
    )
    out = run(problem)
    assert out.layer_records[1].defect_mass.sympy_rational > 0
    assert out.terminal_kind != AUTH


# FIXED 2026-09-23 (was BREAK PIPE-06: sections of unequal length are zip-truncated: (1,) vs (1, 999) measures zero loss)
def test_section_length_mismatch_not_truncated():
    problem = make_problem(local_sections={"U0": (Rational(1),), "U1": (Rational(1), Rational(999))},
                           overlaps={("U0", "U1"): True})
    rec, loss = Layer2MUR.evaluate(problem, evaluator=NativeFunctionalEvaluator())
    assert loss.sympy_rational > 0 or not rec.succeeded


# FIXED 2026-09-23 (was BREAK PIPE-07: an overlap naming a section that does not exist is silently skipped)
def test_overlap_with_missing_section_rejected():
    rec, _ = Layer2MUR.evaluate(make_problem(overlaps={("U0", "GHOST"): True}), evaluator=NativeFunctionalEvaluator())
    assert not rec.succeeded


# FIXED 2026-09-23 (was BREAK PIPE-08: Layer 4 has no failing branch: near-collisions at 10^-30 still 'verify metric separation')
def test_layer4_can_detect_a_collision():
    tiny = Rational(1, 10**30)
    cases = [
        {"U0": (Rational(0),), "U1": (Rational(0),)},
        {"U0": (Rational(0),), "U1": (tiny,)},
        {"U0": (Rational(0),), "U1": (tiny,), "U2": (2 * tiny,)},
    ]
    assert any(not Layer4CSQ.evaluate(make_problem(local_sections=s), evaluator=NativeFunctionalEvaluator())[0].succeeded for s in cases)


# FIXED 2026-09-23 (was BREAK PIPE-09: property: an AUTHORIZED outcome carries a FAILED layer record (catalog PIP-01))
def test_authorized_implies_every_layer_succeeded():
    variants = [
        dict(enclosure_interval=(Rational(2), Rational(1))),
        dict(projection_map={}),
        dict(local_sections={"U0": (Rational(1),), "U1": (Rational(1), Rational(2))},
             overlaps={("U0", "U1"): True}),
    ]
    for v in variants:
        out = run(licensed(**v))
        if out.terminal_kind == AUTH:
            assert all(r.succeeded for r in out.layer_records), v


# ------------------------------------------------ malformed input shapes


# FIXED 2026-09-23 (was BREAK PIPE-10: a 2-char string overlap key 'UV' is unpacked into ('U', 'V') and accepted)
def test_string_overlap_key_rejected():
    problem = make_problem(overlaps={"UV": True})
    try:
        out = run(problem)
    except (TypeError, ValueError):
        return
    assert out.terminal_kind == REF


# FIXED 2026-09-23 (was BREAK PIPE-11: a 3-char string overlap key crashes Layer 2 with ValueError (no terminal))
def test_three_char_overlap_key_refused_not_crashed():
    assert run(make_problem(overlaps={"UVW": True})).terminal_kind == REF


# FIXED 2026-09-23 (was BREAK PIPE-12: d0 as a list of lists crashes with AttributeError (no boundary validation))
def test_list_d0_refused_not_crashed():
    assert run(make_problem(d0=[[-1, 1], [1, -1]], defect_cochain=Matrix([1, 0]))).terminal_kind == REF


# FIXED 2026-09-23 (was BREAK PIPE-13: d0 as a numpy array crashes with AttributeError)
def test_numpy_d0_refused_not_crashed():
    np = pytest.importorskip("numpy")
    assert run(make_problem(d0=np.array([[-1, 1], [1, -1]]), defect_cochain=Matrix([1, 0]))).terminal_kind == REF


# FIXED 2026-09-23 (was BREAK PIPE-14: a Python float in a local section escapes as TypeError from Layer 4)
def test_float_section_refused_not_crashed():
    assert run(make_problem(local_sections={"U0": (0.5,), "U1": (Rational(1),)})).terminal_kind == REF


# FIXED 2026-09-23 (was BREAK PIPE-15: a Python float enclosure bound escapes as TypeError from Layer 5)
def test_float_enclosure_refused_not_crashed():
    assert run(make_problem(enclosure_interval=(0.0, 1.0))).terminal_kind == REF


# FIXED 2026-09-23 (was BREAK PIPE-16: a symbolic d1 entry escapes as TypeError from the Gamma_2 computation)
def test_symbolic_d1_refused_not_crashed():
    problem = make_problem(defect_cochain=Matrix([1, 0]), d1=Matrix([[Symbol("t"), 0]]))
    assert run(problem).terminal_kind == REF


# FIXED 2026-09-23 (was BREAK PIPE-17: candidate_sieve=None crashes Layer 7 with TypeError)
def test_none_sieve_refused_not_crashed():
    assert run(make_problem(candidate_sieve=None)).terminal_kind == REF


# FIXED 2026-09-23 (was BREAK PIPE-18: a sieve holding only the empty string counts as an admitted hypothesis (OR-T5 bypass))
def test_blank_hypothesis_does_not_inhabit_sieve():
    assert run(licensed(candidate_sieve=("",))).terminal_kind == REF


# FIXED 2026-09-23 (was BREAK PIPE-19: a whitespace problem_id passes the 'cannot be empty' check)
def test_blank_problem_id_rejected():
    assert rejects(lambda: make_problem(problem_id="   "), ValueError)


# FIXED 2026-09-23 (was BREAK PIPE-20: a non-string problem_id (7) is accepted and minted into token 'AUTH-7')
def test_non_string_problem_id_rejected():
    assert rejects(lambda: make_problem(problem_id=7), ValueError, TypeError)


# ------------------------------------------------- narrative overclaims


# FIXED 2026-09-23 (was BREAK PIPE-21: Layer 8 says 'All seven halt guards satisfied' but evaluates four guard_* conditions)
def test_layer8_guard_count_matches_message():
    src = inspect.getsource(layer8_fda.Layer8FDA.evaluate)
    guards = set(re.findall(r"^\s*(guard_\w+)\s*=", src, flags=re.M))
    assert "seven" not in src or len(guards) == 7, sorted(guards)


# FIXED 2026-09-23 (was BREAK PIPE-22: Layer 6 says the residual is 'retained ... as Anomalon' but the pipeline never registers one (catalog PIP-02))
def test_pipeline_closed_residual_registers_anomalon():
    out = run(obstructed_problem())
    assert out.terminal_kind == RES
    assert AnomalonRegistry.get_global_registry().count() == 1


# FIXED 2026-09-23 (was BREAK PIPE-23: Layer 6 metadata claims residual_retained_in_cokernel=True when there is no residual)
def test_layer6_metadata_consistent_for_zero_residual():
    out = run(make_problem())
    assert out.layer_records[5].metadata["residual_retained_in_cokernel"] is False


# FIXED 2026-09-23 (was BREAK PIPE-24: zero-defect unlicensed runs are labelled '(Anomalon)', which the registry itself refuses to register)
def test_zero_defect_not_labelled_anomalon():
    assert "Anomalon" not in run(make_problem()).reason


# ------------------------------------------------------ controls (HELD)


def test_pipeline_is_deterministic():
    """HELD: the same instance yields the same outcome twice."""
    a, b = run(obstructed_problem()), run(obstructed_problem())
    assert (a.terminal_kind, a.residual_pair, a.reason) == (b.terminal_kind, b.residual_pair, b.reason)


def test_incoherent_residual_refused():
    """HELD: Gamma_2 > 0 routes to REFUSED even under license."""
    out = run(licensed(defect_cochain=Matrix([1, 0]), d1=Matrix([[1, 0]])))
    assert out.terminal_kind == REF


def test_zero_defect_unlicensed_is_closed_residual():
    """HELD: GTLA-T9 Non-Promotion Firewall routes unlicensed zero-defect to REF."""
    out = run(make_problem())
    assert out.terminal_kind == REF and out.authority_token is None


def test_empty_sieve_refused_under_license():
    """HELD: an empty support sieve is refused (OR-T5) in the plain pipeline."""
    assert run(licensed(candidate_sieve=())).terminal_kind == REF


def test_incompatible_overlap_refused_under_license():
    """HELD: a declared-incompatible overlap is refused (OR-T3)."""
    assert run(licensed(overlaps={("U0", "U0"): False})).terminal_kind == REF


def test_terminal_flags_disjoint():
    """HELD: exactly one of is_authorized / is_closed_residual / is_refused holds."""
    for problem in (make_problem(), licensed(), obstructed_problem(), licensed(candidate_sieve=())):
        out = run(problem)
        assert [out.is_authorized, out.is_closed_residual, out.is_refused].count(True) == 1


def test_genuine_obstruction_is_closed_residual():
    """HELD: a correctly computed obstruction is not promoted even with a license."""
    out = run(obstructed_problem(fda_license_granted=True))
    assert out.terminal_kind == RES and out.residual_pair.phi1.sympy_rational == 2
