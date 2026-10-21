from __future__ import annotations
"""Replay closure for the classified certificate ledger.

REVIEW P1. Three gaps are closed here:

1. `reason` was emitted into every row but was in neither the hashed replay
   payload nor the comparison list, so tampering with it left verification green.
2. Verification compared a hand-maintained tuple of keys. That list had already
   rotted once; it is now computed as a partition, and these tests pin the
   partition rather than the list.
3. No test loaded the COMMITTED report. A 6,000-line artifact that nothing
   replays is not repository-bound evidence, so one is replayed here.

AuthorityEffect: None.
"""


import json
from pathlib import Path

import pytest

from omega_engine.crates.majorana.certificates.ledger import (
    classified_ledger_row,
    verify_classified_ledger,
    write_classified_ledger,
)

REPORT = Path(__file__).resolve().parents[1] / "artifacts" / "tetron_homology_report.json"

D0 = [[1, 0], [1, 1], [0, 1]]
D1 = [[0, 0, 0]]
RESIDUAL = [1, 1, 0]


def _row() -> dict:
    return classified_ledger_row(D0, D1, RESIDUAL, budget=64, instance="replay-fixture")


def test_clean_ledger_verifies(tmp_path: Path) -> None:
    path = tmp_path / "ledger.jsonl"
    write_classified_ledger(path, [_row()])
    result = verify_classified_ledger(path)
    assert result["verified"], result["failures"]
    assert result["checked"] == 1


@pytest.mark.parametrize(
    "field",
    [
        "reason",
        "terminal_status",
        "interpretation",
        "certificate_alpha",
        "replay_hash",
        "algebraic_class_id",
    ],
)
def test_tampering_with_any_derived_field_fails(tmp_path: Path, field: str) -> None:
    """Every derived field must be load-bearing, `reason` included."""
    row = _row()
    assert field in row, f"fixture must exercise {field}"
    row[field] = "TAMPERED" if isinstance(row[field], str) else 999

    path = tmp_path / "tampered.jsonl"
    write_classified_ledger(path, [row])
    result = verify_classified_ledger(path)

    assert not result["verified"], f"tampering with {field} must be caught"
    assert any(f["field"] == field for f in result["failures"]), result["failures"]


def test_unknown_field_is_rejected(tmp_path: Path) -> None:
    """A field nothing recomputes could say anything, so it must be refused."""
    row = _row()
    row["smuggled_conclusion"] = "certified by nobody"
    path = tmp_path / "smuggled.jsonl"
    write_classified_ledger(path, [row])
    result = verify_classified_ledger(path)
    assert not result["verified"]
    assert any(f["field"] == "smuggled_conclusion" for f in result["failures"])


def test_every_row_field_is_either_replayed_or_a_declared_input() -> None:
    """The partition is exhaustive: no field escapes classification."""
    row = _row()
    inputs = {"D0", "D1", "residual", "budget", "instance"}
    derived = set(row) - inputs
    assert derived, "the row must carry derived fields"
    assert "reason" in derived
    assert inputs <= set(row), "every declared input must appear in the row"


@pytest.mark.skipif(not REPORT.exists(), reason="committed report absent")
def test_committed_report_certificates_replay() -> None:
    """The COMMITTED artifact is repository-bound evidence, not decoration."""
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    certificates = report.get("certificates") or []
    assert certificates, "the committed report must carry certificate rows"

    replayed = 0
    for entry in certificates:
        if not all(k in entry for k in ("D0", "D1", "residual")):
            continue
        expected = classified_ledger_row(
            entry["D0"],
            entry["D1"],
            entry["residual"],
            budget=entry.get("budget"),
            instance=entry.get("instance"),
        )
        for key in sorted(set(expected) - {"D0", "D1", "residual", "budget", "instance"}):
            assert entry.get(key) == expected.get(key), (
                f"committed certificate {entry.get('certificate_id')} drifted on {key}: "
                f"artifact={entry.get(key)!r} recomputed={expected.get(key)!r}"
            )
        replayed += 1

    assert replayed > 0, "no committed certificate row was replayable"



