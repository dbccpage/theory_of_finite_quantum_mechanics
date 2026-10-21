"""Versioned refusal semantics for the experimental lettered algebra."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from omega_engine_governance.contracts.dda_packets import (
    DDATapeDFA,
    DDATapeValidationError,
)
from omega_engine.crates.discrete_deformation_algebra.dda_dag_builder import build_dda_dag
from omega_engine.crates.discrete_deformation_algebra.dda_trace_logger import TraceLogger
from omega_engine.crates.type.runtime_axes import DdaDialect


def test_experimental_z_requires_terminal_t() -> None:
    assert DDATapeDFA.validate("R.C.Z.T", dialect=DdaDialect.EXPERIMENTAL_Z_V1)
    with pytest.raises(DDATapeValidationError, match="must be followed by T"):
        DDATapeDFA.validate("R.C.Z", dialect=DdaDialect.EXPERIMENTAL_Z_V1)


def test_experimental_dialect_is_fail_closed_at_both_boundaries() -> None:
    with pytest.raises(DDATapeValidationError, match="must start with E or R"):
        DDATapeDFA.validate("C.R.Z.T", dialect=DdaDialect.EXPERIMENTAL_Z_V1)
    with pytest.raises(DDATapeValidationError, match="must end with terminal T"):
        DDATapeDFA.validate("R.C.E", dialect=DdaDialect.EXPERIMENTAL_Z_V1)
    with pytest.raises(
        DDATapeValidationError, match="Invalid experimental DDA transition"
    ):
        DDATapeDFA.validate("R.I.E.T", dialect=DdaDialect.EXPERIMENTAL_Z_V1)


def test_z_is_rejected_by_canonical_dialects() -> None:
    with pytest.raises(DDATapeValidationError, match="Invalid DDA letter 'Z'"):
        DDATapeDFA.validate("R.C.Z.T", dialect=DdaDialect.LEGACY_V1)
    assert DDATapeDFA.validate("C.R.M", dialect=DdaDialect.OEARS_V1)
    with pytest.raises(DDATapeValidationError, match="M is terminal"):
        DDATapeDFA.validate("C.R.M.T", dialect=DdaDialect.OEARS_V1)


def test_refused_z_trace_retains_obstruction(tmp_path: Path) -> None:
    logger = TraceLogger(
        "experimental-refusal",
        trace_dir=tmp_path,
        dialect=DdaDialect.EXPERIMENTAL_Z_V1,
        auto_lifecycle=False,
    )
    logger.record_step(
        letter="R",
        action_name="measure_unresolved_residual",
        input_state="UNEXAMINED",
        output_state="MEASURED",
        witness="WIT_MEASURE",
        residual_before=3.0,
        residual_after=3.0,
    )
    logger.record_step(
        letter="C",
        action_name="expose_target_context",
        input_state="MEASURED",
        output_state="UNRESOLVED",
        witness="WIT_CONTEXT",
        residual_before=3.0,
        residual_after=3.0,
    )
    logger.refuse(
        reason="detector scope is finite-only",
        input_state="UNRESOLVED",
        output_state="REFUSED",
        witness="WIT_REFUSAL",
        residual=3.0,
        obstruction_id="OBS_SCOPE",
    )

    records = [
        json.loads(line)
        for line in logger.jsonl_path.read_text("utf-8").splitlines()
        if line.strip()
    ]
    assert [record["letter"] for record in records] == ["R", "C", "Z", "T"]
    assert records[2]["effect"] == "refusal"
    assert records[2]["residual_delta"] == 0.0

    dag = build_dda_dag(tmp_path)
    assert dag["valid_runs"] == 1
    assert dag["refusal_steps"] == 1
    assert dag["obstructions_removed_steps"] == 0
    assert dag["measured_residual_reduction"] == 0.0


def test_z_cannot_be_laundered_as_removal(tmp_path: Path) -> None:
    logger = TraceLogger(
        "adversarial-z",
        trace_dir=tmp_path,
        dialect=DdaDialect.EXPERIMENTAL_Z_V1,
        auto_lifecycle=False,
    )
    logger.record_step("R", "measure", "A", "B", "W", residual_energy=1.0)
    with pytest.raises(ValueError, match="cannot carry another effect"):
        logger.record_step(
            "Z",
            "launder_refusal",
            "B",
            "C",
            "BAD",
            residual_before=1.0,
            residual_after=0.0,
            effect="obstruction_eliminated",
        )


@pytest.mark.parametrize(
    ("residual_before", "residual_after", "obstruction_id", "message"),
    (
        (None, None, "OBS", "before/after"),
        (1.0, 1.0, "OBS", "strict residual decrease"),
        (1.0, 0.0, None, "obstruction id"),
    ),
)
def test_elimination_requires_semantic_evidence(
    tmp_path: Path,
    residual_before: float | None,
    residual_after: float | None,
    obstruction_id: str | None,
    message: str,
) -> None:
    logger = TraceLogger(
        "semantic-e",
        trace_dir=tmp_path,
        dialect=DdaDialect.EXPERIMENTAL_Z_V1,
        auto_lifecycle=False,
    )
    logger.record_step("R", "measure", "A", "B", "W", residual_energy=1.0)

    with pytest.raises(ValueError, match=message):
        logger.record_step(
            "E",
            "unsupported-elimination",
            "B",
            "C",
            "BAD",
            residual_before=residual_before,
            residual_after=residual_after,
            effect="obstruction_eliminated",
            obstruction_id=obstruction_id,
        )


def test_structure_addition_requires_a_nonempty_delta(tmp_path: Path) -> None:
    logger = TraceLogger(
        "semantic-lambda",
        trace_dir=tmp_path,
        dialect=DdaDialect.EXPERIMENTAL_Z_V1,
        auto_lifecycle=False,
    )
    logger.record_step("R", "measure", "A", "B", "W", residual_energy=1.0)

    with pytest.raises(ValueError, match="nonempty structure delta"):
        logger.record_step(
            "Lambda",
            "unsupported-lift",
            "B",
            "C",
            "BAD",
            residual_before=1.0,
            residual_after=1.0,
            effect="structure_added",
        )


def test_semantic_letters_cannot_launder_their_effects(tmp_path: Path) -> None:
    logger = TraceLogger(
        "semantic-effect-binding",
        trace_dir=tmp_path,
        dialect=DdaDialect.EXPERIMENTAL_Z_V1,
        auto_lifecycle=False,
    )
    logger.record_step("R", "measure", "A", "B", "W", residual_energy=1.0)

    with pytest.raises(ValueError, match="letter E requires"):
        logger.record_step(
            "E",
            "launder-elimination",
            "B",
            "C",
            "BAD",
            residual_before=1.0,
            residual_after=0.0,
            effect="context_exposed",
            obstruction_id="OBS",
        )

    with pytest.raises(ValueError, match="lift letter requires"):
        logger.record_step(
            "Lambda",
            "launder-lift",
            "B",
            "C",
            "BAD",
            residual_before=1.0,
            residual_after=1.0,
            effect="context_exposed",
            structure_delta={"added": "fake"},
        )


def test_invalid_trace_does_not_pollute_dag_aggregates(tmp_path: Path) -> None:
    logger = TraceLogger(
        "valid-refusal",
        trace_dir=tmp_path,
        dialect=DdaDialect.EXPERIMENTAL_Z_V1,
        auto_lifecycle=False,
    )
    logger.record_step("R", "measure", "A", "B", "W", residual_energy=2.0)
    logger.refuse("unresolved", "B", "C", "Z", residual=2.0)

    records = [
        json.loads(line)
        for line in logger.jsonl_path.read_text("utf-8").splitlines()
        if line.strip()
    ]
    poisoned = dict(records[0])
    poisoned.update(
        {
            "run_id": "tampered",
            "runner_id": "tampered",
            "letter": "E",
            "effect": "obstruction_eliminated",
            "residual_before": 100.0,
            "residual_after": 0.0,
            "residual_delta": -100.0,
        }
    )
    (tmp_path / "tampered_dda_trace.jsonl").write_text(
        json.dumps(poisoned) + "\n", encoding="utf-8"
    )

    dag = build_dda_dag(tmp_path)
    assert dag["total_runs"] == 2
    assert dag["valid_runs"] == 1
    assert dag["invalid_runs"] == 1
    assert dag["obstructions_removed_steps"] == 0
    assert dag["measured_residual_reduction"] == 0.0


