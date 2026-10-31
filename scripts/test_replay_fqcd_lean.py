"""Regression tests for missing, mismatched and unsafe Lean replay evidence."""
import importlib.util
import json
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location("fqcd_replay", Path(__file__).with_name("replay_fqcd_lean.py"))
replay = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(replay)


def test_kernel_reports_preserve_actual_axioms():
    assert replay.parse_reports("'FQCD.a' depends on axioms: [propext, Quot.sound]\n"
                                "'FQCD.b' does not depend on any axioms\n",
                                ["FQCD.a", "FQCD.b"]) == {
        "FQCD.a": ["propext", "Quot.sound"], "FQCD.b": []}


@pytest.mark.parametrize("output,anchors", [
    ("", ["FQCD.a"]),
    ("'FQCD.a' depends on axioms: [propext]", ["FQCD.StrongCouplingAreaLaw.a"]),
    ("'FQCD.a' depends on axioms: [propext]", ["a"]),
    ("'FQCD.a' depends on axioms: [sorryAx]", ["FQCD.a"]),
    ("'FQCD.a' depends on axioms: [Lean.ofReduceBool]", ["FQCD.a"]),
    ("'FQCD.a' depends on axioms: []\n'FQCD.a' depends on axioms: []", ["FQCD.a"]),
    ("'FQCD.a' depends on axioms: []", ["FQCD.a", "FQCD.b"]),
    ("'FQCD.a' depends on axioms: []", ["FQCD.a", "FQCD.a"]),
    ("", []),
])
def test_unmatched_or_unsafe_reports_are_rejected(output, anchors):
    with pytest.raises(ValueError):
        replay.parse_reports(output, anchors)


def test_expected_names_use_the_declaration_namespace():
    assert replay.expected_anchors("namespace FQCD\n#print axioms a\nend FQCD\n") == ["FQCD.a"]
    with pytest.raises(ValueError):
        replay.expected_anchors("namespace Other\n#print axioms a\nend Other\n")


@pytest.fixture
def retained_receipt(tmp_path, monkeypatch):
    monkeypatch.setattr(replay, "ROOT", tmp_path)
    for name in replay.PIN_PATHS:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("namespace FQCD\n#print axioms a\nend FQCD\n" if name == replay.SOURCE else "fixture\n")
    log = tmp_path / replay.LOG
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text("'FQCD.a' depends on axioms: [propext]\n")
    digest = replay.sha((tmp_path / replay.SOURCE).read_bytes())
    result = dict(source=replay.SOURCE, module="FQCD.StrongCouplingAreaLaw", output=replay.LOG,
                  anchors=["FQCD.a"], axioms={"FQCD.a": ["propext"]},
                  output_sha256=replay.sha(log.read_bytes()), sha256=digest, sha256_after_build=digest,
                  source_unchanged_during_build=True, admission_scan_passed=True,
                  axiom_audit_passed=True, anchors_reported=True, exit_code=0)
    receipt = dict(lean_replay=dict(all_passed=True, results=[result]),
                   source_pins={p: replay.sha((tmp_path / p).read_bytes()) for p in replay.PIN_PATHS})
    (tmp_path / replay.RECEIPT).write_text(json.dumps(receipt))
    return tmp_path, receipt, result


def test_valid_retained_output_verifies(retained_receipt):
    replay.verify_receipt()


@pytest.mark.parametrize("defect", ["namespace", "missing_pin", "stale_source", "changed_log", "axioms", "exit_code"])
def test_retained_receipt_rejects_tampering(retained_receipt, defect):
    root, receipt, result = retained_receipt
    if defect == "namespace":
        result["anchors"] = ["FQCD.StrongCouplingAreaLaw.a"]
    elif defect == "missing_pin":
        receipt["source_pins"].pop("lean4/lean-toolchain")
    elif defect == "stale_source":
        (root / replay.SOURCE).write_text((root / replay.SOURCE).read_text() + "\n")
    elif defect == "changed_log":
        (root / replay.LOG).write_text("altered log")
    elif defect == "axioms":
        result["axioms"] = {"FQCD.a": []}
    else:
        result["exit_code"] = 1
    (root / replay.RECEIPT).write_text(json.dumps(receipt))
    with pytest.raises(ValueError):
        replay.verify_receipt()
