"""Regression tests for the exact meron-cluster fixture and the benchmark harness.

Covers:
1. Exact rational ground truth (Z = 912) from two independent computations.
2. One six-site census (Z = 33012) matched to its transfer trace.
3. Orbit cancellation on the four-site subgraphs.
4. The lexical filter and the five prompt builders.
5. Scorer behaviour on fixed positive and mutated responses.
6. Budget guard, dry-run mode, and deterministic JSON output (no network).
"""

from __future__ import annotations

import json

import pytest

from antibody_miner import AntibodyMiner
from blind_problem import (
    FORBIDDEN_WORDS,
    assert_lexical_hygiene,
    generate_blind_problem_packet,
)
from oracle import BlindClusterOracle
from prompt_builder import (
    build_prompt_arm1_constrained_decoding,
    build_prompt_arm2_attention_masking,
    build_prompt_arm3_hieroglyphics,
    build_prompt_arm4_immune_round,
    build_prompt_arm5_hybrid,
)
from run_blind_benchmark import (
    BudgetExceededError,
    BudgetGuard,
    collect_runtime_errors,
    query_openrouter,
    write_json,
)


@pytest.fixture(scope="module")
def oracle() -> BlindClusterOracle:
    return BlindClusterOracle(sites=4, repetitions=2, q="3")


@pytest.fixture(scope="module")
def miner(oracle: BlindClusterOracle) -> AntibodyMiner:
    return AntibodyMiner(oracle)




def test_oracle_ground_truth_invariants(oracle: BlindClusterOracle) -> None:
    """Verify exact discrete combinatorial invariants of the 4-site Trotter ensemble."""
    assert oracle.total_subgraphs == 256
    assert oracle.total_configurations == 1296
    assert oracle.negative_configurations == 192
    assert oracle.signed_partition == "912"
    assert oracle.absolute_partition == "1296"
    assert oracle.average_sign == "19/27"
    assert oracle.zero_charge_subgraphs == 199
    assert oracle.cancelling_subgraphs == 57
    assert oracle.reduced_partition == "912"


def test_orbit_exact_cancellation_on_odd_cycle_subgraphs(oracle: BlindClusterOracle) -> None:
    """Every one of the 256 subgraphs: meron orbits sum to 0, the others to 2^k W_0 > 0."""
    from fractions import Fraction

    samples = oracle.get_sample_subgraphs(limit=256)
    assert len(samples) == 256
    cancelling = [s for s in samples if s["odd_parity_cycles"] > 0]
    assert len(cancelling) == 57
    surviving_total = Fraction(0)
    for s in samples:
        signed_sum = sum(c["sign"] * Fraction(c["weight"]) for c in s["configurations"])
        assert len(s["configurations"]) == 2 ** s["cycle_count"]
        if s["odd_parity_cycles"] > 0:
            assert signed_sum == 0, f"Subgraph {s['subgraph_id']} failed exact cancellation"
            assert Fraction(s["reduced_weight"]) == 0
        else:
            assert signed_sum == 2 ** s["cycle_count"] * Fraction(s["base_weight"]) > 0
            assert signed_sum == Fraction(s["reduced_weight"])
            surviving_total += signed_sum
    assert surviving_total == 912


def test_cluster_sum_matches_independent_transfer_trace(oracle: BlindClusterOracle) -> None:
    """The occupation-basis transfer-matrix trace, computed without clusters, is also 912."""
    assert oracle.independent_transfer_trace == oracle.signed_partition == "912"


def test_six_site_q3_census_matches_transfer_trace() -> None:
    """Six sites, two repetitions, q=3: summary counters match the transfer trace."""
    six = BlindClusterOracle(sites=6, repetitions=2, q="3")
    assert six.total_subgraphs == 4096
    assert six.total_configurations == 33396
    assert six.negative_configurations == 192
    assert six.zero_charge_subgraphs == 4024
    assert six.cancelling_subgraphs == 72
    assert six.signed_partition == "33012"
    assert six.absolute_partition == "33396"
    assert six.reduced_partition == "33012"
    assert six.average_sign == "2751/2783"
    assert six.independent_transfer_trace == six.signed_partition


def test_fixture_satisfies_character_law_and_equal_orbit_weights() -> None:
    """The model's own checks: sign is a character of the flips; weights are constant on orbits."""
    from meron_exact_model import meron_database, meron_summary

    summary = meron_summary(meron_database(4, 2, "3"))
    assert summary["invalid_characters"] == 0
    assert summary["unequal_orbit_weights"] == 0
    assert summary["incomplete_orbits"] == 0
    assert summary["orientation_key_defects"] == 0
    assert summary["model_relation_defects"] == {}
    assert summary["reconstruction"] is True




def test_lexical_hygiene_blocks_all_forbidden_tokens() -> None:
    """Verify that any appearance of forbidden physics keywords raises ValueError."""
    for token in FORBIDDEN_WORDS:
        test_str = f"This contains the word {token} in lowercase."
        with pytest.raises(ValueError, match="LEXICAL HYGIENE VIOLATION"):
            assert_lexical_hygiene(test_str)

        test_upper = f"THIS CONTAINS {token.upper()} IN UPPERCASE."
        with pytest.raises(ValueError, match="LEXICAL HYGIENE VIOLATION"):
            assert_lexical_hygiene(test_upper)


def test_all_five_prompt_arms_pass_lexical_hygiene() -> None:
    """Verify that all 5 prompt builders construct prompts with 0 domain token leaks."""
    packet = generate_blind_problem_packet()

    p1 = build_prompt_arm1_constrained_decoding(packet)
    p2 = build_prompt_arm2_attention_masking(packet)
    p3 = build_prompt_arm3_hieroglyphics(packet)
    p4 = build_prompt_arm4_immune_round(packet, round_number=1, accumulated_antibodies=[])
    p5 = build_prompt_arm5_hybrid(packet)

    for i, p in enumerate([p1, p2, p3, p4, p5], 1):
        assert_lexical_hygiene(p)
        assert len(p) > 100, f"Prompt Arm {i} is unexpectedly short"




def test_positive_control_scores_perfect(miner: AntibodyMiner) -> None:
    """A mathematically valid derivation scores 4/4 and generates no antibodies."""
    response = json.dumps(
        {
            "cycle_independence": True,
            "cycle_parity_invariant_found": True,
            "cancellation_mechanism": (
                "Flipping an odd-winding cycle reverses global sign, causing identical "
                "pairwise (1 + (-1)) = 0 cancellation across the 2^k flip orbit."
            ),
            "zero_odd_sector_subgraphs": 199,
            "exact_partition_z": 912,
            "scratchpad": "Summing 199 zero-meron subgraphs yields Z = 912.",
        }
    )

    result, antibodies = miner.evaluate_and_mine(response, [])
    assert result["score"] == 4
    assert result["perfect"] is True
    assert antibodies == []


def test_hallucination_mutation_mines_antibodies(miner: AntibodyMiner) -> None:
    """Mutating responses with specific errors triggers corresponding typed antibodies."""
    resp_drift = json.dumps(
        {
            "cycle_independence": True,
            "cycle_parity_invariant_found": True,
            "cancellation_mechanism": "Odd cycle flips cancel pairwise to zero.",
            "zero_odd_sector_subgraphs": 199,
            "exact_partition_z": 128,
            "scratchpad": "Got 128.",
        }
    )
    res, abs_drift = miner.evaluate_and_mine(resp_drift, [])
    assert res["score"] == 3
    assert any(a["code"] == "ANTI_PARTITION_DRIFT" for a in abs_drift)

    resp_coupled = json.dumps(
        {
            "cycle_independence": False,
            "cycle_parity_invariant_found": True,
            "cancellation_mechanism": "Odd cycle flips cancel pairwise to zero.",
            "zero_odd_sector_subgraphs": 199,
            "exact_partition_z": 912,
            "scratchpad": "Entangled cycles.",
        }
    )
    res, abs_coupled = miner.evaluate_and_mine(resp_coupled, [])
    assert res["score"] == 3
    assert any(a["code"] == "ANTI_COUPLED_CYCLE_HALLUCINATION" for a in abs_coupled)

    resp_leak = json.dumps(
        {
            "cycle_independence": True,
            "cycle_parity_invariant_found": True,
            "cancellation_mechanism": "Odd cycle flips cancel pairwise to zero.",
            "zero_odd_sector_subgraphs": 256,
            "exact_partition_z": 912,
            "scratchpad": "Used all 256 subgraphs.",
        }
    )
    res, abs_leak = miner.evaluate_and_mine(resp_leak, [])
    assert res["score"] == 3
    assert any(a["code"] == "ANTI_NEGATIVE_CONTRIBUTION_LEAK" for a in abs_leak)




def test_dry_run_executes_safely_without_spend() -> None:
    """Dry run mode provides deterministic mock responses without provider calls."""
    guard = BudgetGuard(ceiling_usd=0.05)
    resp, meta = query_openrouter(
        model="meta-llama/llama-3.3-70b-instruct",
        prompt="Abstract graph partition problem.",
        api_key="",
        budget_guard=guard,
        dry_run=True,
    )
    data = json.loads(resp)
    assert data["exact_partition_z"] == 912
    assert meta["cost"] == 0.0
    assert guard.total_spent == 0.0


def test_budget_guard_blocks_over_ceiling() -> None:
    """Budget guard refuses calls that would exceed the configured ceiling."""
    guard = BudgetGuard(ceiling_usd=0.0001)
    with pytest.raises(BudgetExceededError, match="refusing request"):
        guard.reserve_call(
            model="qwen/qwen3.7-max",
            prompt="x" * 2000,
            max_output_tokens=3000,
        )


def test_runtime_error_collection() -> None:
    """Runtime errors in nested dictionary are collected accurately."""
    report_data = {
        "arm1": {"model_a": {"score": 4}, "model_b": {"error": "Connection timed out"}},
        "arm2": {"model_c": {"score": 2}},
    }
    errors = collect_runtime_errors(report_data)
    assert errors == ["arms.arm1.model_b: Connection timed out"]


def test_json_writer_emits_lf_only(tmp_path) -> None:
    """JSON output writer strictly outputs UTF-8 without CR-LF."""
    dest = tmp_path / "test.json"
    payload = write_json(dest, {"z": 912, "verified": True})
    assert b"\r\n" not in payload
    assert dest.read_bytes() == payload
