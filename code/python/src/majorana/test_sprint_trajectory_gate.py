from __future__ import annotations
"""Lev Landau tests for dda_sprint_trajectory.v1 integrity gate.

Production defects caught:

- ``test_integrity_v1_golden_passes`` fails if a complete v1 record is refused.
- ``test_strip_phi1_kills_gate`` fails if missing Φ₁ is silent (mutation kill).
- ``test_ort_process_tape_is_legacy_and_fails_integrity`` fails if ORT process
  NDJSON is falsely accepted as integrity v1.
- ``test_authority_effect_not_none_is_refused`` fails if non-None authority is
  allowed.
- ``test_chain_break_is_detected`` fails if step_hash tampering is silent.
- ``test_legacy_mode_classifies_without_hard_fail`` fails if optional classify
  mode still red-lights pure process tapes for missing integrity fields.
"""


import json
from pathlib import Path


from omega_engine.crates.discrete_deformation_algebra.sprint_trajectory_gate import (
    CLASS_INTEGRITY_V1,
    CLASS_LEGACY,
    SCHEMA_ID,
    validate_dda_sprint_trajectory,
)
from omega_engine.crates.discrete_deformation_algebra.trajectory_recorder import _step_hash


def _v1_record(**overrides):
    base = {
        "run_id": "run_golden_v1",
        "step_index": 0,
        "phi1": 1.0,
        "state_fingerprint": "abc123",
        "authority_effect": "None",
        "dda_letter": "C",
        "name": "step",
    }
    base.update(overrides)
    return base


def _legacy_record(**overrides):
    base = {
        "run_id": "sprint_planning_ort_003_ppos",
        "date": "2026-07-30",
        "authority_effect": "None",
        "stage": 1,
        "dda_letter": "R",
        "name": "sprint-planning",
        "note": "process tape",
    }
    base.update(overrides)
    return base


def test_integrity_v1_golden_passes():
    result = validate_dda_sprint_trajectory([_v1_record()])
    assert result.ok, result.as_dict()
    assert result.classification == CLASS_INTEGRITY_V1
    assert result.schema_id == SCHEMA_ID
    assert result.authority_effect == "None"


def test_strip_phi1_kills_gate():
    """Mutation kill: remove phi1 → red; restore → green."""
    good = _v1_record()
    bad = dict(good)
    del bad["phi1"]

    assert validate_dda_sprint_trajectory([good]).ok
    killed = validate_dda_sprint_trajectory([bad])
    assert not killed.ok
    codes = {v.code for v in killed.violations}
    assert "MISSING_PHI1" in codes


def test_strip_step_index_kills_gate():
    bad = _v1_record()
    del bad["step_index"]
    result = validate_dda_sprint_trajectory([bad])
    assert not result.ok
    assert any(v.code == "MISSING_STEP_INDEX" for v in result.violations)


def test_strip_state_fingerprint_kills_gate():
    bad = _v1_record()
    del bad["state_fingerprint"]
    result = validate_dda_sprint_trajectory([bad])
    assert not result.ok
    assert any(v.code == "MISSING_STATE_FINGERPRINT" for v in result.violations)


def test_authority_effect_not_none_is_refused():
    bad = _v1_record(authority_effect="Minted")
    result = validate_dda_sprint_trajectory([bad])
    assert not result.ok
    assert any(v.code == "AUTHORITY_EFFECT_NOT_NONE" for v in result.violations)


def test_residual_energy_alias_accepted():
    rec = _v1_record()
    del rec["phi1"]
    rec["residual_energy"] = 0.5
    assert validate_dda_sprint_trajectory([rec]).ok


def test_input_output_hash_state_alias_accepted():
    rec = _v1_record()
    del rec["state_fingerprint"]
    rec["input_hash"] = "in"
    rec["output_hash"] = "out"
    assert validate_dda_sprint_trajectory([rec]).ok


def test_ort_process_tape_is_legacy_and_fails_integrity():
    result = validate_dda_sprint_trajectory(
        [_legacy_record(), _legacy_record(name="x")]
    )
    assert not result.ok
    assert result.classification == CLASS_LEGACY
    codes = {v.code for v in result.violations}
    assert "MISSING_PHI1" in codes or "LEGACY_NOT_INTEGRITY_V1" in codes
    assert "MISSING_STEP_INDEX" in codes or "LEGACY_NOT_INTEGRITY_V1" in codes


def test_legacy_mode_classifies_without_hard_fail():
    result = validate_dda_sprint_trajectory(
        [_legacy_record()], require_integrity_v1=False
    )
    assert result.ok, result.as_dict()
    assert result.classification == CLASS_LEGACY


def test_live_ort_tape_path_is_legacy(tmp_path):
    """If the ORT corpus path exists, classify it; else use a fixture twin."""
    live = (
        Path(__file__).resolve().parents[3]
        / "omega_engine"
        / "research"
        / "product_planning_office"
        / "sprints"
        / "sprint-ort-003"
        / "dda_sprint_trajectory.ndjson"
    )
    if live.is_file():
        path = live
    else:
        path = tmp_path / "dda_sprint_trajectory.ndjson"
        path.write_text(json.dumps(_legacy_record()) + "\n", encoding="utf-8")

    result = validate_dda_sprint_trajectory(path)
    assert not result.ok
    assert result.classification == CLASS_LEGACY
    assert result.record_count >= 1


def test_chain_break_is_detected():
    r0 = _v1_record(step_index=0, name="one")
    r0["prev_step_hash"] = None
    r0["step_hash"] = _step_hash(r0)

    r1 = _v1_record(step_index=1, name="two", phi1=0.5)
    r1["prev_step_hash"] = r0["step_hash"]
    r1["step_hash"] = _step_hash(r1)

    ok = validate_dda_sprint_trajectory([r0, r1])
    assert ok.ok, ok.as_dict()

    r0_edit = dict(r0)
    r0_edit["phi1"] = 99.0
    broken = validate_dda_sprint_trajectory([r0_edit, r1])
    assert not broken.ok
    assert any(v.code == "CHAIN_BROKEN" for v in broken.violations)


def test_empty_tape_is_ok_empty():
    result = validate_dda_sprint_trajectory([])
    assert result.ok
    assert result.classification == "EMPTY"


