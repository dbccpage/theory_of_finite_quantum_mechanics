"""Focused regression tests for the blind cluster recovery benchmark."""

from __future__ import annotations

import json

import pytest

from omega_engine_projects.fsp.demos.blind_cluster_recovery.antibody_miner import (
    AntibodyMiner,
)
from omega_engine_projects.fsp.demos.blind_cluster_recovery.oracle import BlindClusterOracle
from omega_engine_projects.fsp.demos.blind_cluster_recovery.run_blind_benchmark import (
    BudgetExceededError,
    BudgetGuard,
    collect_runtime_errors,
    query_openrouter,
    write_json,
)


@pytest.fixture(scope="module")
def miner() -> AntibodyMiner:
    return AntibodyMiner(BlindClusterOracle())


def test_exact_integer_strings_are_scored_consistently(miner: AntibodyMiner) -> None:
    response = json.dumps(
        {
            "cycle_independence": True,
            "cycle_parity_invariant_found": True,
            "cancellation_mechanism": "An odd flip gives pairwise cancellation to zero.",
            "zero_odd_sector_subgraphs": "199",
            "exact_partition_z": "912",
            "scratchpad": "Exact integer spellings.",
        }
    )

    result, antibodies = miner.evaluate_and_mine(response, [])

    assert result["perfect"] is True
    assert antibodies == []


def test_wrong_zero_sector_count_cannot_pass_by_word_match(miner: AntibodyMiner) -> None:
    response = json.dumps(
        {
            "cycle_independence": True,
            "cycle_parity_invariant_found": True,
            "cancellation_mechanism": "Odd flips cancel to zero.",
            "zero_odd_sector_subgraphs": 0,
            "exact_partition_z": 912,
            "scratchpad": "Wrong surviving-sector count.",
        }
    )

    result, antibodies = miner.evaluate_and_mine(response, [])

    assert result["score"] == 3
    assert any(item["code"] == "ANTI_NEGATIVE_CONTRIBUTION_LEAK" for item in antibodies)


def test_dry_run_has_no_live_provider_dependency() -> None:
    guard = BudgetGuard(ceiling_usd=0.01)

    response, metadata = query_openrouter(
        model="test/model",
        prompt="abstract graph prompt",
        api_key="",
        budget_guard=guard,
        dry_run=True,
    )

    assert json.loads(response)["exact_partition_z"] == 912
    assert metadata["cost"] == 0.0
    assert guard.total_spent == 0.0


def test_budget_guard_refuses_before_network_request() -> None:
    guard = BudgetGuard(ceiling_usd=0.000001)

    with pytest.raises(BudgetExceededError, match="refusing request"):
        guard.reserve_call(
            model="qwen/qwen3.7-max",
            prompt="x" * 100,
            max_output_tokens=3000,
        )


def test_runtime_error_receipt_status_input() -> None:
    arms = {"arm1": {"model": {"error": "provider unavailable"}}}

    assert collect_runtime_errors(arms) == ["arms.arm1.model: provider unavailable"]


def test_json_writer_returns_exact_artifact_bytes(tmp_path) -> None:
    path = tmp_path / "artifact.json"

    payload = write_json(path, {"z": 912, "status": "PASS"})

    assert path.read_bytes() == payload
    assert b"\r\n" not in payload
