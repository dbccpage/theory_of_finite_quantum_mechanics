"""Receipt integrity for the real-world DDA trajectory recorder.

Each test names the production defect it catches:

- ``test_square_zero_is_not_computed_without_a_complex`` fails if the report
  stamps VERIFIED for a check that never ran.
- ``test_square_zero_is_refuted_for_a_broken_complex`` fails if the square-zero
  check cannot report a negative — a check that cannot fail is not a check.
- ``test_steps_are_hash_chained`` / ``test_tampering_breaks_the_chain`` fail if
  receipts can be reordered, dropped, or edited undetectably.
- ``test_reruns_are_distinguishable_in_the_jsonl`` fails if two runs append
  colliding step ids with no way to tell them apart.
- ``test_markdown_carries_receipt_hashes`` fails if the tracked artifact carries
  no evidence.
"""

import json


from omega_engine.crates.discrete_deformation_algebra import FiniteCochainComplex
from omega_engine.crates.discrete_deformation_algebra.trajectory_recorder import (
    RealWorldDdaTrajectoryRecorder,
    verify_trajectory_chain,
)
from omega_engine.crates.type.runtime_axes import DdaLetter


def _square_zero_complex() -> FiniteCochainComplex:
    """Filled triangle: d1 . d0 = 0."""
    return FiniteCochainComplex.from_rows(
        dimensions=(3, 3, 1),
        d0=((-1, 1, 0), (0, -1, 1), (-1, 0, 1)),
        d1=((1, 1, -1),),
    )


def _broken_complex() -> FiniteCochainComplex:
    """Same carrier with d1 perturbed: d1 . d0 = (-2, 0, 2) != 0."""
    return FiniteCochainComplex.from_rows(
        dimensions=(3, 3, 1),
        d0=((-1, 1, 0), (0, -1, 1), (-1, 0, 1)),
        d1=((1, 1, 1),),
    )


def _record(recorder, letter=DdaLetter.C, name="step"):
    return recorder.record_step(
        action_name=name,
        input_state_desc="in",
        output_state_desc="out",
        dda_letter=letter,
        witness_desc="witness",
    )


def test_square_zero_is_not_computed_without_a_complex(tmp_path):
    recorder = RealWorldDdaTrajectoryRecorder("no_complex", log_dir=tmp_path)
    _record(recorder)

    assert recorder.square_zero_status() == "NOT_COMPUTED"
    body = recorder.markdown_path.read_text(encoding="utf-8")
    assert "NOT_COMPUTED" in body
    assert "VERIFIED" not in body


def test_square_zero_is_verified_for_a_real_complex(tmp_path):
    recorder = RealWorldDdaTrajectoryRecorder(
        "good_complex", log_dir=tmp_path, cochain_complex=_square_zero_complex()
    )
    _record(recorder)

    assert recorder.square_zero_status() == "VERIFIED"
    assert "VERIFIED" in recorder.markdown_path.read_text(encoding="utf-8")


def test_square_zero_is_refuted_for_a_broken_complex(tmp_path):
    recorder = RealWorldDdaTrajectoryRecorder(
        "bad_complex", log_dir=tmp_path, cochain_complex=_broken_complex()
    )
    _record(recorder)

    assert recorder.square_zero_status() == "REFUTED"
    body = recorder.markdown_path.read_text(encoding="utf-8")
    assert "REFUTED" in body
    assert "VERIFIED" not in body


def test_square_zero_is_vacuous_when_there_are_no_two_cochains(tmp_path):
    """With C2 = 0 there is no composite to check; VERIFIED would overclaim."""
    one_dimensional = FiniteCochainComplex.from_rows(
        dimensions=(3, 2, 0), d0=((-1, 1, 0), (0, -1, 1)), d1=()
    )
    recorder = RealWorldDdaTrajectoryRecorder(
        "vacuous", log_dir=tmp_path, cochain_complex=one_dimensional
    )
    _record(recorder)

    assert recorder.square_zero_status() == "VACUOUS"
    body = recorder.markdown_path.read_text(encoding="utf-8")
    assert "VACUOUS" in body
    assert "VERIFIED" not in body


def test_steps_are_hash_chained(tmp_path):
    recorder = RealWorldDdaTrajectoryRecorder("chained", log_dir=tmp_path)
    _record(recorder, DdaLetter.C, "one")
    _record(recorder, DdaLetter.R, "two")
    _record(recorder, DdaLetter.T, "three")

    rows = [
        json.loads(line)
        for line in recorder.jsonl_path.read_text(encoding="utf-8").splitlines()
    ]
    assert len(rows) == 3
    assert rows[0]["prev_step_hash"] is None
    for earlier, later in zip(rows, rows[1:]):
        assert later["prev_step_hash"] == earlier["step_hash"]

    ok, detail = verify_trajectory_chain(rows)
    assert ok, detail


def test_tampering_breaks_the_chain(tmp_path):
    recorder = RealWorldDdaTrajectoryRecorder("tampered", log_dir=tmp_path)
    _record(recorder, DdaLetter.C, "one")
    _record(recorder, DdaLetter.R, "two")

    rows = [
        json.loads(line)
        for line in recorder.jsonl_path.read_text(encoding="utf-8").splitlines()
    ]
    rows[0]["output_state"] = "silently edited"

    ok, detail = verify_trajectory_chain(rows)
    assert not ok
    assert "DDA_STEP_001" in detail


def test_dropping_a_step_breaks_the_chain(tmp_path):
    recorder = RealWorldDdaTrajectoryRecorder("dropped", log_dir=tmp_path)
    _record(recorder, DdaLetter.C, "one")
    _record(recorder, DdaLetter.R, "two")
    _record(recorder, DdaLetter.I, "three")

    rows = [
        json.loads(line)
        for line in recorder.jsonl_path.read_text(encoding="utf-8").splitlines()
    ]
    ok, _ = verify_trajectory_chain([rows[0], rows[2]])
    assert not ok


def test_reruns_are_distinguishable_in_the_jsonl(tmp_path):
    first = RealWorldDdaTrajectoryRecorder("rerun", log_dir=tmp_path)
    _record(first)
    second = RealWorldDdaTrajectoryRecorder("rerun", log_dir=tmp_path)
    _record(second)

    assert first.run_id != second.run_id

    rows = [
        json.loads(line)
        for line in first.jsonl_path.read_text(encoding="utf-8").splitlines()
    ]
    assert len(rows) == 2
    assert rows[0]["step_id"] == rows[1]["step_id"] == "DDA_STEP_001"
    assert rows[0]["run_id"] != rows[1]["run_id"]

    # A consumer must be able to recover a single coherent run.
    only_second = [r for r in rows if r["run_id"] == second.run_id]
    ok, detail = verify_trajectory_chain(only_second)
    assert ok, detail


def test_markdown_carries_receipt_hashes(tmp_path):
    recorder = RealWorldDdaTrajectoryRecorder("evidence", log_dir=tmp_path)
    step = _record(recorder)

    body = recorder.markdown_path.read_text(encoding="utf-8")
    assert recorder.run_id in body
    assert step["step_hash"][:16] in body
    assert step["witness_hash"][:16] in body


def test_residual_energy_is_not_derived_from_the_letter(tmp_path):
    """An E step carrying nonzero residual must report it, not zero it by fiat."""
    recorder = RealWorldDdaTrajectoryRecorder("energy", log_dir=tmp_path)
    step = recorder.record_step(
        action_name="claimed exact repair",
        input_state_desc="in",
        output_state_desc="out",
        dda_letter=DdaLetter.E,
        witness_desc="witness",
        residual_obstruction_energy=5.0,
    )

    assert step["residual_energy"] == 5.0
    assert step["diagnostic_after"] == "Energy=5.00"


