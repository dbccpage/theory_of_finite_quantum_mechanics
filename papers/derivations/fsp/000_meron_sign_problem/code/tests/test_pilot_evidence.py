"""Ties the paper's account of the retained pilot run to the retained files.

All checks are offline. They read ``code/results/`` and rebuild prompts with the
package code; the prompt strings are unchanged since the run.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

import pytest

from antibody_miner import AntibodyMiner
from blind_problem import generate_blind_problem_packet
from oracle import BlindClusterOracle
from prompt_builder import (
    build_prompt_arm1_constrained_decoding,
    build_prompt_arm2_attention_masking,
    build_prompt_arm3_hieroglyphics,
    build_prompt_arm4_immune_round,
    build_prompt_arm5_hybrid,
)

RESULTS = Path(__file__).resolve().parents[1] / "results"
LLAMA = "meta-llama/llama-3.3-70b-instruct"
DEEPSEEK = "deepseek/deepseek-v4-flash-0731"
GLM = "z-ai/glm-5.3-flash"
RUN_ORDER = (LLAMA, DEEPSEEK, GLM)


@pytest.fixture(scope="module")
def report() -> dict:
    return json.loads((RESULTS / "master_evaluation_report.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def miner() -> AntibodyMiner:
    return AntibodyMiner(BlindClusterOracle())


@pytest.fixture(scope="module")
def packet() -> dict:
    return generate_blind_problem_packet()


def harvested_guards(report: dict) -> list[dict]:
    """Arm 5 guards as the harness collected them from the Arm 4 runs."""
    guards: list[dict] = []
    for model in RUN_ORDER:
        for guard in report["arms"]["arm4_immune_mining"][model]["final_antibodies"]:
            if guard["code"] not in {g["code"] for g in guards}:
                guards.append(guard)
    return guards


def test_receipt_digest_matches_report() -> None:
    """receipt.json records the SHA-256 of the report bytes; its status is a constant."""
    receipt = json.loads((RESULTS / "receipt.json").read_text(encoding="utf-8"))
    digest = hashlib.sha256((RESULTS / "master_evaluation_report.json").read_bytes()).hexdigest()
    assert receipt["sha256"] == digest
    assert receipt["receipt_id"] == "REC_FSP_BLIND_1790605314"


def test_recorded_call_ledger(report: dict) -> None:
    """22 calls, n = 1 per model and arm, estimated spend 0.01496 USD at configured prices."""
    budget = report["budget_summary"]
    assert report["dry_run"] is False
    assert budget["total_calls"] == len(budget["call_history"]) == 22
    assert round(budget["total_spent_usd"], 5) == 0.01496
    models = {call["model"] for call in budget["call_history"]}
    assert models == {LLAMA, DEEPSEEK, GLM, "tencent/hy4-preview", "qwen/qwen3.7-max"}


def test_recorded_scores_by_arm(report: dict) -> None:
    """The scores reported in the paper's results table."""
    arms = report["arms"]
    single = {
        "arm1_constrained": {LLAMA: 2, DEEPSEEK: 0, GLM: 0},
        "arm2_attention_masking": {LLAMA: 1, DEEPSEEK: 0, GLM: 0},
        "arm3_hieroglyphics": {LLAMA: 0, DEEPSEEK: 0, GLM: 0},
        "arm5_hybrid": {LLAMA: 3, "tencent/hy4-preview": 0, "qwen/qwen3.7-max": 4},
    }
    for arm, expected in single.items():
        assert {model: cell["score"] for model, cell in arms[arm].items()} == expected
    arm4 = arms["arm4_immune_mining"]
    assert [round_["score"] for round_ in arm4[LLAMA]["history"]] == [2, 4]
    assert [round_["score"] for round_ in arm4[GLM]["history"]] == [0, 0, 4]
    assert [round_["score"] for round_ in arm4[DEEPSEEK]["history"]] == [0, 0, 3, 0, 0]
    assert arm4[DEEPSEEK]["converged"] is False


def test_recorded_scores_reproduce_under_package_scorer(report: dict, miner: AntibodyMiner) -> None:
    """Re-scoring each retained single-turn answer gives the recorded score."""
    for arm in ("arm1_constrained", "arm2_attention_masking", "arm3_hieroglyphics", "arm5_hybrid"):
        for model, cell in report["arms"][arm].items():
            result, _ = miner.evaluate_and_mine(json.dumps(cell["parsed"]), [])
            assert result["score"] == cell["score"], (arm, model)


def test_glm_arm2_answer_used_keys_outside_the_schema(report: dict) -> None:
    """GLM-5.3-Flash wrote Z = 912 under a key the schema does not define; it scored 0."""
    cell = report["arms"]["arm2_attention_masking"][GLM]
    assert cell["parsed"] == {
        "Z": 912,
        "cancellation_proof": cell["parsed"]["cancellation_proof"],
        "zero_odd_winding_subgraphs": 4,
    }
    assert cell["score"] == 0


def test_arm4_corrections_state_the_target(report: dict, miner: AntibodyMiner) -> None:
    """The scorer's correction strings, fed back in Arm 4, contain Z = 912 and the 57/199 split."""
    failing = json.dumps({"exact_partition_z": 128, "zero_odd_sector_subgraphs": 128})
    _, guards = miner.evaluate_and_mine(failing, [])
    corrections = {guard["code"]: guard["correction"] for guard in guards}
    assert "Z must equal 912" in corrections["ANTI_PARTITION_DRIFT"]
    assert "All 57 subgraphs" in corrections["ANTI_NEGATIVE_CONTRIBUTION_LEAK"]
    assert "remaining 199" in corrections["ANTI_NEGATIVE_CONTRIBUTION_LEAK"]
    recorded = report["arms"]["arm4_immune_mining"][LLAMA]["final_antibodies"]
    assert [guard["correction"] for guard in recorded] == [
        corrections["ANTI_PARTITION_DRIFT"],
        corrections["ANTI_NEGATIVE_CONTRIBUTION_LEAK"],
    ]
    round_two = build_prompt_arm4_immune_round(generate_blind_problem_packet(), 2, recorded)
    assert "Z must equal 912" in round_two and "remaining 199" in round_two


def test_arm5_prompt_as_run_states_target_and_method(report: dict, packet: dict) -> None:
    """The Arm 5 prompt carried the answer, the counts, and the cancellation argument."""
    prompt = build_prompt_arm5_hybrid(packet, harvested_guards(report))
    for fragment in (
        "Z must equal 912",
        "All 57 subgraphs",
        "remaining 199",
        "sigma(C) = prod_i s_i^{I(c_i)}",
        "the sum factors as (1 + (-1)) * prod_{j != i} (...) = 0",
        "1,296 total orientation states",
        "<sigma> = 19/27",
    ):
        assert fragment in prompt


def test_unassisted_prompts_state_quantities_that_fix_z(packet: dict) -> None:
    """Arms 1-3 do not state 912 or 199, but 1,296 and 19/27 give Z = 912 by one product."""
    prompts = [
        build_prompt_arm1_constrained_decoding(packet),
        build_prompt_arm2_attention_masking(packet),
        build_prompt_arm3_hieroglyphics(packet),
    ]
    for prompt in prompts:
        assert "912" not in prompt and "199" not in prompt
        assert "19/27" in prompt and "1,296" in prompt
    assert Fraction(19, 27) * 1296 == 912 == 1104 - 192
    assert "1,104 configurations have sign sigma = +1" in prompts[0]
    assert "vanishes IDENTICALLY" in prompts[0]
    assert "vanishes identically" in prompts[1]
    assert "any subgraph with I_odd >= 1" in prompts[2]


def test_sample_subgraphs_in_prompts_have_no_odd_cycles(packet: dict) -> None:
    """The four listed samples all have zero odd-winding cycles and weight 1."""
    assert [(s["odd_parity_cycles"], s["base_weight"]) for s in packet["samples"]] == [(0, "1")] * 4


def test_arm3_prompt_is_shorter_because_it_omits_content(packet: dict) -> None:
    """Arm 3 is 1,124 characters against 4,320 for Arm 1; it drops the narrative and listings."""
    arm1 = build_prompt_arm1_constrained_decoding(packet)
    arm3 = build_prompt_arm3_hieroglyphics(packet)
    assert (len(arm1), len(arm3)) == (4320, 1124)
    assert "Flip Mask" in arm1 and "Flip Mask" not in arm3
    assert "YOUR OBJECTIVE" in arm1 and "YOUR OBJECTIVE" not in arm3
