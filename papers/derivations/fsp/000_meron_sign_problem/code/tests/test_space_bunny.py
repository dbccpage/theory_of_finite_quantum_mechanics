"""Offline checks on the retained stealth/space-bunny-alpha output, plus the live probe.

The live probe below is the script formerly committed as ``code/test_space_bunny.py``
(source commit 0ad428e36), moved into ``code/tests/``. As committed it could not
have produced the retained result: it passes guard dictionaries without a
``correction`` key to ``build_prompt_arm5_hybrid`` (KeyError), calls a scorer
method that does not exist, and writes no result file. The probe here corrects
only those defects and no longer reads a ``.env`` file implicitly. The live test
is always skipped: it would send a paid request to an external provider, and the
package tests make no network calls.
"""

from __future__ import annotations

import json
import os
import time
import urllib.request
from pathlib import Path

import pytest

from antibody_miner import AntibodyMiner
from blind_problem import generate_blind_problem_packet
from oracle import BlindClusterOracle
from prompt_builder import (
    JSON_SCHEMA_ARM1,
    build_prompt_arm1_constrained_decoding,
    build_prompt_arm5_hybrid,
)

RESULT = Path(__file__).resolve().parents[1] / "results" / "space_bunny_arm5_result.json"
PROBE_MODEL = "stealth/space-bunny-alpha"
PROBE_GUARDS = [
    {
        "code": "ANTI_PARTITION_DRIFT",
        "correction": "The exact integer partition sum Z must equal 912. No approximation or empirical sample average is permitted.",
    },
    {
        "code": "ANTI_NEGATIVE_CONTRIBUTION_LEAK",
        "correction": "All 57 subgraphs with odd-winding cycles sum to zero. The non-negative partition is computed strictly by summing the remaining 199 zero-odd-charge subgraphs.",
    },
    {
        "code": "ANTI_MISSING_PAIRWISE_CANCELLATION",
        "correction": "The cycle parity characters must factor into independent product terms, where odd cycles yield (+1 + -1) = 0.",
    },
]


@pytest.fixture(scope="module")
def miner() -> AntibodyMiner:
    return AntibodyMiner(BlindClusterOracle())


@pytest.fixture(scope="module")
def retained() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_retained_record_fields(retained: dict) -> None:
    """The retained file holds content and usage only: no model, prompt, score or latency."""
    assert set(retained) == {"content", "content_len", "finish_reason", "reasoning_len", "usage"}
    assert retained["finish_reason"] == "stop"
    assert retained["content_len"] == len(retained["content"]) == 1159
    assert retained["reasoning_len"] == 9683


def test_retained_output_scores_four_of_four(miner: AntibodyMiner, retained: dict) -> None:
    """Re-applying the package scorer to the retained content gives 4/4."""
    result, _ = miner.evaluate_and_mine(retained["content"], [])
    assert result["score"] == 4


def test_retained_output_does_not_conform_to_schema(miner: AntibodyMiner, retained: dict) -> None:
    """The schema requires booleans and a string; the scorer's bool() coercion accepts a string."""
    parsed = miner.parse_proposer_response(retained["content"])
    properties = JSON_SCHEMA_ARM1["properties"]
    assert properties["cycle_independence"]["type"] == "boolean"
    assert properties["scratchpad"]["type"] == "string"
    assert type(parsed["cycle_independence"]) is str
    assert type(parsed["scratchpad"]) is list


def test_counts_in_output_come_only_from_guard_text(retained: dict) -> None:
    """57 and 199 appear in the output and the guard text, not in the unguarded Arm 5 prompt."""
    packet = generate_blind_problem_packet()
    unguarded = build_prompt_arm5_hybrid(packet)
    guarded = build_prompt_arm5_hybrid(packet, PROBE_GUARDS)
    for count in ("57", "199"):
        assert count in retained["content"]
        assert count not in unguarded
        assert count in guarded
    assert "Z must equal 912" in guarded


def query_openrouter(api_key: str, prompt: str, max_tokens: int = 4096) -> dict:
    """One chat-completion request, with the committed probe's parameters."""
    payload = {
        "model": PROBE_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.0,
        "response_format": JSON_SCHEMA_ARM1,
    }
    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    start = time.time()
    with urllib.request.urlopen(request, timeout=300) as response:
        data = json.loads(response.read().decode("utf-8"))
    data["client_latency"] = time.time() - start
    return data


def run_live_probe(api_key: str) -> dict:
    """Arm 1 and Arm 5 (with the probe guards) against the probe model."""
    miner = AntibodyMiner(BlindClusterOracle())
    packet = generate_blind_problem_packet()
    prompts = {
        "arm1": build_prompt_arm1_constrained_decoding(packet),
        "arm5": build_prompt_arm5_hybrid(packet, PROBE_GUARDS),
    }
    results = {}
    for arm, prompt in prompts.items():
        data = query_openrouter(api_key, prompt)
        content = data["choices"][0]["message"].get("content") or ""
        score, _ = miner.evaluate_and_mine(content, [])
        results[arm] = {"score": score["score"], "content": content, "usage": data.get("usage", {})}
    return results


@pytest.mark.skip(
    reason="Live OpenRouter request to an unidentified model; never run by the package "
    "tests (requires explicit authorization and OPENROUTER_API_KEY)."
)
def test_live_probe() -> None:
    results = run_live_probe(os.environ["OPENROUTER_API_KEY"])
    assert set(results) == {"arm1", "arm5"}
