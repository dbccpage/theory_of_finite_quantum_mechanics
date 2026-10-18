from __future__ import annotations

import hashlib
import json
from pathlib import Path
import pytest

from omega_engine.crates.discrete_deformation_algebra.dda_trace_logger import TraceLogger
from omega_engine.crates.discrete_deformation_algebra.trajectory_recorder import verify_trajectory_chain


def _replay_step_hash(record: dict) -> str:
    payload = {key: value for key, value in record.items() if key != "step_hash"}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def test_trace_logger_lifecycle(tmp_path: Path) -> None:
    runner_id = "test-runner-alpha"
    with TraceLogger(runner_id, trace_dir=tmp_path) as logger:
        logger.record_step(
            letter="E",
            action_name="repair_test_defect",
            input_state="STATE_BEFORE",
            output_state="STATE_AFTER",
            witness="WIT_TEST_REPAIR",
            residual_before=1.0,
            residual_after=0.0,
            obstruction_id="TEST_DEFECT",
        )

    jsonl_files = list(tmp_path.glob("*.jsonl"))
    assert len(jsonl_files) == 1

    records = [json.loads(line) for line in jsonl_files[0].read_text("utf-8").splitlines() if line.strip()]
    assert len(records) == 4

    assert records[0]["letter"] == "C"
    assert records[1]["letter"] == "E"
    assert records[2]["letter"] == "I"
    assert records[3]["letter"] == "T"

    for r in records:
        assert r["authority_effect"] == "None"
        assert r["runner_id"] == runner_id

    ok, detail = verify_trajectory_chain(records)
    assert ok, f"chain failed: {detail}"


def test_trace_logger_emits_independently_parseable_hash_chained_jsonl(
    tmp_path: Path,
) -> None:
    with TraceLogger("inspectable-run", trace_dir=tmp_path) as logger:
        logger.record_step(
            letter="E",
            action_name="exact_repair",
            input_state="OBSTRUCTED",
            output_state="REPAIRED",
            witness="WIT_EXACT_REPAIR",
            residual_before=1.0,
            residual_after=0.0,
            obstruction_id="OBS_EXACT",
            evidence={"replay": "passed"},
        )

    assert logger.jsonl_path.suffix == ".jsonl"
    raw_lines = logger.jsonl_path.read_text(encoding="utf-8").splitlines()
    assert raw_lines
    records = [json.loads(line) for line in raw_lines]
    expected_parent = None
    for record in records:
        assert record["prev_step_hash"] == expected_parent
        assert record["step_hash"] == _replay_step_hash(record)
        expected_parent = record["step_hash"]


def test_trace_logger_failure_path(tmp_path: Path) -> None:
    runner_id = "test-runner-failing"
    with pytest.raises(RuntimeError, match="simulated failure"):
        with TraceLogger(runner_id, trace_dir=tmp_path) as logger:
            logger.record_step(
                letter="R",
                action_name="project_residual",
                input_state="STATE_ACTIVE",
                output_state="STATE_RESIDUAL",
                witness="WIT_RESIDUAL",
            )
            raise RuntimeError("simulated failure")

    jsonl_files = list(tmp_path.glob("*.jsonl"))
    assert len(jsonl_files) == 1

    records = [json.loads(line) for line in jsonl_files[0].read_text("utf-8").splitlines() if line.strip()]
    assert len(records) == 4

    assert records[0]["letter"] == "C"
    assert records[1]["letter"] == "R"
    assert records[2]["letter"] == "M"
    assert records[2]["refusal_reason"] == "simulated failure"
    assert records[3]["letter"] == "T"

    ok, detail = verify_trajectory_chain(records)
    assert ok, f"chain failed: {detail}"


