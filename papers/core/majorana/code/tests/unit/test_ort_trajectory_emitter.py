from __future__ import annotations
"""Lev Landau tests for ORT INTEGRITY_V1 emitter (STORY-ORT-DDA-002).

Defects caught:

- emitter output refused by integrity gate
- missing phi1 / state fingerprint still passes
- legacy upgrade without step_index accepted as integrity
- chain break after upgrade
- authority_effect smuggling
"""


from pathlib import Path


from omega_engine.crates.discrete_deformation_algebra.ort_trajectory_emitter import (
    OrtTrajectoryEmitter,
    emit_integrity_v1_record,
    emit_upgraded_tape_from_legacy,
    upgrade_legacy_record,
)
from omega_engine.crates.discrete_deformation_algebra.sprint_trajectory_gate import (
    CLASS_INTEGRITY_V1,
    CLASS_LEGACY,
    validate_dda_sprint_trajectory,
)


def test_emitter_passes_integrity_gate(tmp_path: Path):
    em = OrtTrajectoryEmitter(run_id="ort_emit_001")
    em.emit_step(phi1=1.0, state={"stage": 1}, dda_letter="R", name="planning")
    em.emit_step(phi1=0.5, state={"stage": 2}, dda_letter="E", name="execution")
    result = em.validate()
    assert result.ok, result.as_dict()
    assert result.classification == CLASS_INTEGRITY_V1

    path = tmp_path / "dda_sprint_trajectory.ndjson"
    em.append_ndjson(path)
    file_result = validate_dda_sprint_trajectory(path)
    assert file_result.ok, file_result.as_dict()
    assert file_result.classification == CLASS_INTEGRITY_V1


def test_mutation_kill_strip_phi1():
    rec = emit_integrity_v1_record(
        run_id="r",
        step_index=0,
        phi1=1.0,
        state_fingerprint="abc",
        chain=False,
    )
    assert validate_dda_sprint_trajectory([rec]).ok
    bad = dict(rec)
    del bad["phi1"]
    killed = validate_dda_sprint_trajectory([bad])
    assert not killed.ok
    assert any(v.code == "MISSING_PHI1" for v in killed.violations)


def test_upgrade_legacy_to_integrity():
    legacy = {
        "run_id": "sprint_planning_ort_003_ppos",
        "date": "2026-07-30",
        "authority_effect": "None",
        "stage": 1,
        "dda_letter": "R",
        "name": "sprint-planning",
        "note": "process tape",
    }
    assert validate_dda_sprint_trajectory([legacy]).classification == CLASS_LEGACY
    upgraded = upgrade_legacy_record(legacy, step_index=0, phi1=0.0)
    result = validate_dda_sprint_trajectory([upgraded])
    assert result.ok, result.as_dict()
    assert result.classification == CLASS_INTEGRITY_V1
    assert upgraded["upgraded_from"] == "LEGACY_PROCESS_TAPE"


def test_upgrade_chain_of_legacy_lines():
    legs = [
        {
            "run_id": "r",
            "authority_effect": "None",
            "stage": i,
            "dda_letter": "C",
            "name": f"s{i}",
            "note": "n",
        }
        for i in range(3)
    ]
    tape = emit_upgraded_tape_from_legacy(legs, phi1_per_step=[1.0, 0.5, 0.0])
    result = validate_dda_sprint_trajectory(tape)
    assert result.ok, result.as_dict()
    assert tape[1]["prev_step_hash"] == tape[0]["step_hash"]


def test_authority_not_none_refused():
    rec = emit_integrity_v1_record(
        run_id="r", step_index=0, phi1=0.0, state_fingerprint="x", chain=False
    )
    rec["authority_effect"] = "Minted"
    assert not validate_dda_sprint_trajectory([rec]).ok


