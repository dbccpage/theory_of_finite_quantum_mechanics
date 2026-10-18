"""Unit tests for coboundary scoring and Clean-Spine T0 laws.

Tests:
1. Discrete birth-death scoring of open obstruction sets.
2. Structural cost penalty on normalized efficiency s(alpha) = Delta / (1 + c).
3. Legality gates: kill condition triggers, authority_effect non-None, unadmitted constructors.
4. Exactness law: post_residual == 0 AND dual witness -> exact candidate; post_residual == 0 without dual witness -> NOT exact.
5. Vector 1-norm cochain scoring.
6. Candidate proposal ranking and tie-breaking.
7. Clean-spine T0 quiescence and FORCED_A_FROM_EMPTY_REGIME refusal.
"""

from __future__ import annotations

from fractions import Fraction
import math
import pytest

from omega_engine_pfp.domain import (
    COBOUNDARY_SCORE_SCHEMA,
    REFUSAL_AUTHORITY_NON_NONE,
    REFUSAL_EXACT_WITHOUT_DUAL_WITNESS,
    REFUSAL_PROSE_PROMPT_REFUSED,
    CandidateProposal,
    CoboundaryScoreResult,
)
from omega_engine_pfp.use_cases import (
    KILL_CONDITION_MAP,
    rank_candidate_proposals,
    score_cochain_proposal,
    score_discrete_proposal,
)

SAMPLE_HEX64 = "a" * 64
SAMPLE_HEX64_B = "b" * 64


def test_discrete_coboundary_scoring_basic() -> None:
    open_obs = ("OBS-01", "OBS-02", "OBS-03")

    prop1 = CandidateProposal(
        proposal_id="prop-1",
        repaired_obstruction_ids=("OBS-01", "OBS-02"),
        structural_cost=0.0,
    )
    res1 = score_discrete_proposal(open_obs, prop1)
    assert res1.is_legal
    assert res1.prior_residual_norm == 3.0
    assert res1.post_residual_norm == 1.0
    assert res1.residual_drop == 2.0
    assert res1.structural_cost == 0.0
    assert res1.normalized_efficiency == 2.0
    assert not res1.is_exact_candidate

    prop2 = CandidateProposal(
        proposal_id="prop-2",
        repaired_obstruction_ids=("OBS-01", "OBS-02"),
        structural_cost=1.0,
    )
    res2 = score_discrete_proposal(open_obs, prop2)
    assert res2.is_legal
    assert res2.residual_drop == 2.0
    assert res2.structural_cost == 1.0
    assert res2.normalized_efficiency == 1.0


def test_exactness_requires_dual_witness() -> None:
    open_obs = ("OBS-01", "OBS-02")

    prop_no_witness = CandidateProposal(
        proposal_id="prop-no-witness",
        repaired_obstruction_ids=("OBS-01", "OBS-02"),
        dual_witness_ref=None,
    )
    res_no_witness = score_discrete_proposal(open_obs, prop_no_witness)
    assert res_no_witness.is_legal
    assert res_no_witness.post_residual_norm == 0.0
    assert not res_no_witness.is_exact_candidate
    assert res_no_witness.dual_witness_ref is None

    prop_with_witness = CandidateProposal(
        proposal_id="prop-with-witness",
        repaired_obstruction_ids=("OBS-01", "OBS-02"),
        dual_witness_ref=SAMPLE_HEX64,
    )
    res_with_witness = score_discrete_proposal(open_obs, prop_with_witness)
    assert res_with_witness.is_legal
    assert res_with_witness.post_residual_norm == 0.0
    assert res_with_witness.is_exact_candidate
    assert res_with_witness.dual_witness_ref == SAMPLE_HEX64


def test_legality_gates_and_refusals() -> None:
    open_obs = ("OBS-01",)

    prop_auth = CandidateProposal(
        proposal_id="prop-auth",
        authority_effect="Promote",
    )
    res_auth = score_discrete_proposal(open_obs, prop_auth)
    assert not res_auth.is_legal
    assert res_auth.refusal_reason == REFUSAL_AUTHORITY_NON_NONE
    assert res_auth.normalized_efficiency == -math.inf

    prop_kill = CandidateProposal(
        proposal_id="prop-kill",
        kill_triggers=("SYNTAX_VALID_IMPLIES_SEMANTIC_TRUE",),
    )
    res_kill = score_discrete_proposal(open_obs, prop_kill)
    assert not res_kill.is_legal
    assert "CLAIM_EVALUATOR" in (res_kill.refusal_reason or "")
    assert res_kill.normalized_efficiency == -math.inf

    prop_unadmitted = CandidateProposal(
        proposal_id="prop-unadmitted",
        admitted_constructors_used=("unadmitted_op",),
    )
    res_unadmitted = score_discrete_proposal(
        open_obs,
        prop_unadmitted,
        admitted_constructors=("op_a", "op_b"),
    )
    assert not res_unadmitted.is_legal
    assert REFUSAL_PROSE_PROMPT_REFUSED in (res_unadmitted.refusal_reason or "")


def test_cochain_scoring_vector_norm() -> None:
    omega = {"edge_01": Fraction(2), "edge_02": Fraction(3)}

    prop = CandidateProposal(
        proposal_id="cochain-prop",
        cochain_delta=(("edge_01", Fraction(2)), ("edge_02", Fraction(3, 2))),
        structural_cost=0.5,
    )
    res = score_cochain_proposal(omega, prop)
    assert res.is_legal
    assert res.prior_residual_norm == Fraction(5)
    assert res.post_residual_norm == Fraction(3, 2)
    assert res.residual_drop == Fraction(7, 2)
    assert pytest.approx(res.normalized_efficiency) == 3.5 / 1.5


def test_ranking_candidate_proposals() -> None:
    open_obs = ("OBS-01", "OBS-02", "OBS-03")

    prop_best = CandidateProposal(
        proposal_id="best",
        repaired_obstruction_ids=("OBS-01", "OBS-02", "OBS-03"),
        structural_cost=0.0,
    )
    prop_mid = CandidateProposal(
        proposal_id="mid",
        repaired_obstruction_ids=("OBS-01",),
        structural_cost=0.0,
    )
    prop_expensive = CandidateProposal(
        proposal_id="expensive",
        repaired_obstruction_ids=("OBS-01", "OBS-02"),
        structural_cost=5.0,
    )
    prop_illegal = CandidateProposal(
        proposal_id="illegal",
        kill_triggers=("FORCED_A_FROM_EMPTY_REGIME",),
    )

    ranked = rank_candidate_proposals(
        open_obs,
        [prop_expensive, prop_illegal, prop_best, prop_mid],
    )

    assert len(ranked) == 4
    assert ranked[0].proposal_id == "best"
    assert ranked[1].proposal_id == "mid"
    assert ranked[2].proposal_id == "expensive"
    assert ranked[3].proposal_id == "illegal"
    assert not ranked[3].is_legal


def test_clean_spine_t0_quiescence_laws() -> None:
    assert "FORCED_A_FROM_EMPTY_REGIME" in KILL_CONDITION_MAP
    refusal_code = KILL_CONDITION_MAP["FORCED_A_FROM_EMPTY_REGIME"]
    assert refusal_code == REFUSAL_PROSE_PROMPT_REFUSED

    assert "ONE_RULE_BUNDLES_UNDECLARED_PRIMITIVES" in KILL_CONDITION_MAP

    prop_forced = CandidateProposal(
        proposal_id="t0-forced-a",
        kill_triggers=("FORCED_A_FROM_EMPTY_REGIME",),
    )
    res = score_discrete_proposal(("no_transition_rule",), prop_forced)
    assert not res.is_legal
    assert res.refusal_reason == REFUSAL_PROSE_PROMPT_REFUSED


def test_coboundary_score_result_wire_roundtrip() -> None:
    res = CoboundaryScoreResult(
        proposal_id="test-prop-01",
        prior_residual_norm=Fraction(4),
        post_residual_norm=Fraction(1),
        residual_drop=Fraction(3),
        structural_cost=0.5,
        normalized_efficiency=2.0,
        is_legal=True,
    )
    wire = res.to_dict()
    assert wire["schema_version"] == COBOUNDARY_SCORE_SCHEMA
    reparsed = CoboundaryScoreResult.from_dict(wire)
    assert reparsed == res
