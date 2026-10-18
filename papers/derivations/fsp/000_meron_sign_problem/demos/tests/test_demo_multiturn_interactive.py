"""Tests for multi-turn interactive PFP trials in demos/code/demo_multiturn_interactive_pfp.py.
AuthorityEffect: None.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

DEMOS_DIR = Path(__file__).resolve().parent.parent
CODE_DIR = DEMOS_DIR.parent / "code"
if str(DEMOS_DIR / "code") not in sys.path:
    sys.path.insert(0, str(DEMOS_DIR / "code"))
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from demo_multiturn_interactive_pfp import (
    build_turn_prompts,
    extract_turn_metrics,
    replay_certified_multiturn_trial,
)
from blind_problem import assert_lexical_hygiene


def test_multiturn_interactive_replay():
    """Verify that the certified multi-turn interactive receipt validates both models."""
    receipt = replay_certified_multiturn_trial()

    assert receipt["trial_id"] == "CERT-MULTITURN-PFP-2026-10-02"
    assert receipt["models_evaluated"] == 2
    assert receipt["lift_emission_probability_overall"] == 1.0
    assert receipt["terminal_repair_rate"] == 1.0
    assert receipt["verified"] is False
    assert receipt["live_provider_evidence"] is False
    assert receipt["evidence_scope"] == "synthetic_example_without_raw_provider_custody"

    model_map = {r["model_id"]: r for r in receipt["results"]}
    assert "stealth/space-bunny-alpha" in model_map
    assert "meta-llama/llama-3.3-70b-instruct" in model_map

    sb = model_map["stealth/space-bunny-alpha"]
    assert sb["tier"] == "Deep Reasoning (Free tier)"
    assert sb["total_reasoning_tokens"] > 3000
    assert sb["total_latency_seconds"] > 10.0
    assert sb["lift_request_emission_rate"] == 1.0
    assert sb["terminal_repair_passed"] is True
    assert len(sb["turns"]) == 4

    assert sb["turns"][0]["stage"] == "PLAQUETTE_BREAKUP"
    assert sb["turns"][1]["stage"] == "MEASURE_HOLONOMY"
    assert sb["turns"][2]["stage"] == "LIFT_REQUEST"
    assert sb["turns"][2]["lift_requested"] is True
    assert "tau" in sb["turns"][2]["proposed_involution"]
    assert sb["turns"][3]["stage"] == "EXACT_REPAIR"
    assert sb["turns"][3]["exact_repair_achieved"] is True

    llama = model_map["meta-llama/llama-3.3-70b-instruct"]
    assert llama["tier"] == "70B Open-Weights Instruct"
    assert llama["total_reasoning_tokens"] == 0
    assert llama["total_latency_seconds"] < 10.0
    assert llama["lift_request_emission_rate"] == 1.0
    assert llama["terminal_repair_passed"] is True
    assert len(llama["turns"]) == 4

    assert llama["turns"][2]["stage"] == "LIFT_REQUEST"
    assert llama["turns"][2]["lift_requested"] is True
    assert llama["turns"][3]["stage"] == "EXACT_REPAIR"
    assert llama["turns"][3]["exact_repair_achieved"] is True


def test_multiturn_prompts_lexical_hygiene():
    """Verify that all sequential turn queries pass strict zero-smuggling lexical hygiene."""
    prompts = build_turn_prompts()
    assert len(prompts) == 4

    for p in prompts:
        query = p["query"]
        assert_lexical_hygiene(query)

        lower = query.lower()
        forbidden = [
            "meron", "fermion", "hamiltonian", "hubbard",
            "chandrasekharan", "wiese", "trotter", "fock",
            "anticommut", "quantum monte carlo", "qmc", "physics"
        ]
        for term in forbidden:
            assert term not in lower, f"Forbidden term '{term}' found in Turn {p['turn']} query"


def test_multiturn_turn_metrics_extraction():
    """Verify extraction of latency, tokens, lift requests, and exact repair flags from response objects."""
    turn3_spec = {"turn": 3, "stage": "LIFT_REQUEST"}
    mock_resp3 = {
        "choices": [
            {
                "message": {
                    "content": "We propose the discrete involution tau_i: s_i -> -s_i which flips cycle orientation.",
                    "reasoning": "Analyzing cycle holonomy and sign inversion under parity.",
                }
            }
        ],
        "usage": {"prompt_tokens": 150, "completion_tokens": 80},
        "client_latency": 2.5,
    }
    m3 = extract_turn_metrics(mock_resp3, turn3_spec, has_reasoning_tokens=True)
    assert m3["turn"] == 3
    assert m3["stage"] == "LIFT_REQUEST"
    assert m3["lift_requested"] is True
    assert "tau_i" in m3["proposed_involution"]
    assert m3["client_latency_seconds"] == 2.5
    assert m3["reasoning_tokens"] is None
    assert m3["reasoning_word_count"] == 8
    assert m3["raw_provider_response"] == mock_resp3

    turn4_spec = {"turn": 4, "stage": "EXACT_REPAIR"}
    mock_resp4 = {
        "choices": [
            {
                "message": {
                    "content": "Summing the remaining 199 zero-odd subgraphs yields the exact partition sum Z = 912.",
                    "reasoning": "",
                }
            }
        ],
        "usage": {"prompt_tokens": 180, "completion_tokens": 50},
        "client_latency": 1.2,
    }
    m4 = extract_turn_metrics(mock_resp4, turn4_spec, has_reasoning_tokens=False)
    assert m4["turn"] == 4
    assert m4["stage"] == "EXACT_REPAIR"
    assert m4["exact_repair_achieved"] is True
    assert m4["lift_requested"] is False
    assert m4["client_latency_seconds"] == 1.2
    assert m4["reasoning_tokens"] is None


def test_missing_fixture_cannot_manufacture_provider_evidence(tmp_path, monkeypatch):
    import demo_multiturn_interactive_pfp as runner
    target = tmp_path / "missing.json"
    monkeypatch.setattr(runner, "CERTIFIED_MULTITURN_RECEIPT", target)
    with pytest.raises(FileNotFoundError):
        runner.replay_certified_multiturn_trial()
    assert not target.exists()


def test_reasoning_tokens_use_provider_usage():
    response = {"choices": [{"message": {"content": "", "reasoning": "three prose words"}}],
                "usage": {"completion_tokens_details": {"reasoning_tokens": 17}}}
    result = extract_turn_metrics(response, {"turn": 1, "stage": "PLAQUETTE_BREAKUP"}, True)
    assert result["reasoning_tokens"] == 17
    assert result["reasoning_word_count"] == 3
