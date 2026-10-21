"""Tests for 4-site replay demo in demos/code/demo_4site_symbol_game.py.

AuthorityEffect: None.
"""

from __future__ import annotations

from pathlib import Path

from oracle import BlindClusterOracle
from symbol_game_pfp import replay_certified_ladder

DEMO_RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"


def test_certified_ladder_offline_verification():
    """Verify that all certified model ladder receipts score 4/4 against the exact oracle."""
    report = replay_certified_ladder(DEMO_RESULTS_DIR)
    assert report["models_tested"] == 4
    assert report["all_perfect"] is True

    scores = {r["model"]: r["score"] for r in report["results"]}
    assert scores["stealth/space-bunny-alpha"] == 4
    assert scores["meta-llama/llama-3.3-70b-instruct"] == 4
    assert scores["meta-llama/llama-3.1-8b-instruct"] == 4
    assert scores["z-ai/glm-5.3-flash"] == 4


def test_oracle_4site_ground_truth():
    """Verify ground truth constants of the 4-site lattice."""
    oracle = BlindClusterOracle()
    assert oracle.total_subgraphs == 256
    assert oracle.total_configurations == 1296
    assert oracle.negative_configurations == 192
    assert oracle.signed_partition == "912"
    assert oracle.average_sign == "19/27"
    assert oracle.zero_charge_subgraphs == 199
    assert oracle.cancelling_subgraphs == 57
    assert oracle.independent_transfer_trace == "912"
