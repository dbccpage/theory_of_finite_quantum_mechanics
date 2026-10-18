from __future__ import annotations

from pathlib import Path

from omega_engine.crates.discrete_deformation_algebra.dda_dag_builder import build_dda_dag
from omega_engine.crates.discrete_deformation_algebra.dda_trace_logger import TraceLogger


def test_build_dda_dag(tmp_path: Path) -> None:
    r_id = "test-dag-runner"
    with TraceLogger(r_id, trace_dir=tmp_path) as logger:
        logger.record_step(
            letter="E",
            action_name="remove_obstruction",
            input_state="OBSTRUCTED",
            output_state="REPAIRED",
            witness="WIT_REPAIR_01",
            residual_before=1.0,
            residual_after=0.0,
            obstruction_id="TEST_OBSTRUCTION",
        )

    summary = build_dda_dag(tmp_path)
    assert summary["total_runs"] == 1
    assert summary["total_steps"] == 4
    assert summary["structure_built_steps"] == 2
    assert summary["obstructions_removed_steps"] == 1
    assert summary["terminal_steps"] == 1

    assert (tmp_path / "dda_dag.json").exists()
    assert (tmp_path / "dda_dag_summary.md").exists()


