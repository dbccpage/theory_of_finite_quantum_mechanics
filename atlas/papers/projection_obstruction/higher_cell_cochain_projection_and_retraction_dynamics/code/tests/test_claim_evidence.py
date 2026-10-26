"""Regression checks for written-only, numerical and abstract formal evidence."""

import copy
import importlib.util
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("po034_verifier", ROOT / "verify_deposit.py")
verifier = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = verifier
spec.loader.exec_module(verifier)


@pytest.fixture
def ledger():
    return yaml.safe_load((ROOT / "claim_ledger.yaml").read_text(encoding="utf-8"))


def check(ledger):
    return verifier.check_evidence(
        ledger, (ROOT / "claim_ledger.md").read_text(encoding="utf-8")
    )


def test_expanded_ledger_keeps_evidence_counts_separate(ledger):
    assert check(ledger) == {
        "claims": 13, "written_only": 6, "numerical_examples": 7,
        "conditional_lean_targets": 7,
    }


def test_written_only_records_do_not_import_modules(ledger, monkeypatch):
    original = verifier.importlib.import_module

    def import_numerical(name):
        assert name != "none"
        return original(name)

    monkeypatch.setattr(verifier.importlib, "import_module", import_numerical)
    assert check(ledger)["written_only"] == 6


@pytest.mark.parametrize("change", ["assumptions", "proof_heading", "proof_path", "execution", "tests"])
def test_written_claims_require_real_proof_locations_and_honest_status(ledger, change):
    claim = ledger["claims"][3]
    if change == "assumptions":
        claim["written_evidence"]["assumptions"] = ""
    elif change == "proof_heading":
        claim["written_evidence"]["proof_location"]["heading"] = "### Lemma 4.3a (Missing)"
    elif change == "proof_path":
        claim["written_evidence"]["proof_location"]["path"] = "../outside.md"
    elif change == "execution":
        claim["written_evidence"]["execution_status"] = "passed"
    else:
        claim["code_evidence"]["tests"] = []
    with pytest.raises(ValueError):
        check(ledger)


def test_unmechanized_scope_cannot_advertise_theorems(ledger):
    formal = ledger["claims"][3]["lean4_evidence"]
    formal.update(module="HigherCell.Theorem41_Idempotence", theorems=["invented"])
    with pytest.raises(ValueError, match="unmechanized"):
        check(ledger)


def test_missing_claim_or_conditional_target_fails(ledger):
    missing_claim = copy.deepcopy(ledger)
    del missing_claim["claims"][3]
    with pytest.raises(ValueError, match="claim IDs"):
        check(missing_claim)
    ledger["claims"][0]["lean4_evidence"]["theorems"].pop()
    with pytest.raises(ValueError, match="census inventory"):
        check(ledger)


def test_numerical_mapping_requires_existing_regression(ledger):
    ledger["claims"][0]["code_evidence"]["tests"] = [
        "code/tests/test_k_cell_retraction.py::nonexistent_test"
    ]
    with pytest.raises(ValueError, match="missing regression"):
        check(ledger)
