"""Adversarial policy/custody tests. Synthetic inputs are never saved as execution evidence."""
import json
from pathlib import Path
import sys
import pytest
sys.path.insert(0, str(Path(__file__).parent))
from replay import ROOT, inventory
from mutations import classify
from records import apply_individual_engineering_review, main

def test_snapshot_inventory_covers_copied_arithmetic_and_fixtures():
    sources = inventory()
    assert "code/rust/Cargo.lock" in sources
    assert "code/rust/src/linear_algebra/scalars.rs" in sources
    assert any(p.endswith(".json") for p in sources)

def test_fault_attribution_distinguishes_compile_resource_and_assertion_failures(tmp_path):
    log = tmp_path / "diagnostic.log"
    run = dict(timed_out=False, exit_code=101, log=str(log))
    for text, expected in [("error[E0308]: could not compile", "invalid"),
                           ("error: could not compile: os error 112", "inconclusive"),
                           ("test result: FAILED", "killed")]:
        log.write_text(text)
        assert classify(run)[0] == expected
    assert classify({**run, "timed_out": True})[0] == "inconclusive"

def test_known_failure_does_not_complete_an_unassessed_review():
    record = dict(artifact=dict(sha256="policy-fixture"), level="L3",
        gates=dict(G1=None, G2="E", G3=None, G4=None, G5=None),
        structure=dict(metric_ceiling="A"), grade_ceiling="A", open_findings=[],
        is_complete=False, composite_grade=None, score_token=None)
    specification = dict(engineering_assessment=dict(source_sha256="policy-fixture",
        gates={gate: dict(grade=None, basis="Unassessed synthetic policy input")
               for gate in record["gates"]}))
    apply_individual_engineering_review(record, specification)
    assert record["gates"]["G2"] == "E"
    assert record["grade_ceiling"] == "E"
    assert not record["is_complete"] and record["score_token"] is None

def test_corrupt_receipt_manifest_refused_before_any_sidecars_written(tmp_path, monkeypatch):
    (tmp_path / "source_manifest.json").write_text("{}")
    receipt = tmp_path / "receipt.json"
    receipt.write_text(json.dumps(dict(source_manifest_sha256="wrong")))
    monkeypatch.setattr(sys, "argv", ["records.py", "--receipt", str(receipt)])
    with pytest.raises(RuntimeError, match="manifest digest"):
        main()
