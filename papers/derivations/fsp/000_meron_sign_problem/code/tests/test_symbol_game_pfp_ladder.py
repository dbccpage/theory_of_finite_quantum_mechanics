"""Unit tests for the certified Symbol Game PFP model ladder results.

AuthorityEffect: None.
"""

from __future__ import annotations

import json
from pathlib import Path

from blind_problem import assert_lexical_hygiene
from oracle import BlindClusterOracle
from symbol_game_pfp import build_pfp_prompt_4site, replay_certified_ladder

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"


def test_build_pfp_prompt_4site_passes_lexical_hygiene():
    """The live 4-site prompt must clear the substring filter before any request."""
    prompt = build_pfp_prompt_4site(BlindClusterOracle())
    assert isinstance(prompt, str) and prompt
    assert_lexical_hygiene(prompt)
    assert "odd-winding clusters" in prompt
    assert "meron" not in prompt.lower()


def test_certified_model_ladder_all_pass_four_of_four():
    """Verify that all four models on the certified ladder score 4/4 against BlindClusterOracle."""
    report = replay_certified_ladder(RESULTS_DIR)
    assert report["models_tested"] == 4
    assert report["all_perfect"] is True

    scores = {r["model"]: r["score"] for r in report["results"]}
    assert scores["stealth/space-bunny-alpha"] == 4
    assert scores["meta-llama/llama-3.3-70b-instruct"] == 4
    assert scores["meta-llama/llama-3.1-8b-instruct"] == 4
    assert scores["z-ai/glm-5.3-flash"] == 4


def test_certified_model_ladder_reproducible_records():
    """Verify that every model on the ladder records required fields and valid JSON structure."""
    ladder_file = RESULTS_DIR / "certified_4site_ladder_results.json"
    assert ladder_file.exists()
    data = json.loads(ladder_file.read_text(encoding="utf-8"))

    assert len(data["model_results"]) == 4
    for item in data["model_results"]:
        assert item["score"] == 4
        assert item["perfect"] is True
        assert item["rubric_breakdown"]["exact_partition_z"] is True
        assert item["rubric_breakdown"]["cycle_independence"] is True
        assert item["rubric_breakdown"]["parity_cancellation_proved"] is True
        assert item["rubric_breakdown"]["zero_odd_sector_used"] is True
        assert "cancellation_mechanism" in item
