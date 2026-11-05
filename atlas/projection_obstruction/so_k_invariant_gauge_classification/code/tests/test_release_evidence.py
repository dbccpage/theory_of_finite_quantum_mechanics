"""Metadata and receipt regressions: reject evidence that looks complete but is false."""

import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location("gs002_release_verifier", ROOT / "verify_deposit.py")
assert spec is not None and spec.loader is not None
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


@pytest.fixture
def metadata_tree(tmp_path, monkeypatch):
    metadata = json.loads((ROOT / "zenodo_metadata.json").read_text())
    monkeypatch.setattr(verifier, "ROOT", tmp_path)
    return tmp_path, metadata


def test_metadata_accepts_the_completed_preprint_shape(metadata_tree):
    root, metadata = metadata_tree
    (root / "zenodo_metadata.json").write_text(json.dumps(metadata))
    verifier.verify_metadata()


@pytest.mark.parametrize("mutation", ["missing_identifier", "empty_identifier", "bad_url", "bad_date", "article", "no_relations"])
def test_metadata_rejects_incomplete_release_identity(metadata_tree, mutation):
    root, metadata = metadata_tree
    if mutation == "missing_identifier":
        del metadata["related_identifiers"][1]["identifier"]
    elif mutation == "empty_identifier":
        metadata["related_identifiers"][1]["identifier"] = " "
    elif mutation == "bad_url":
        metadata["related_identifiers"][1]["identifier"] = "repo/path"
    elif mutation == "bad_date":
        metadata["publication_date"] = "2026-02-30"
    elif mutation == "article":
        metadata["publication_type"] = "article"
    else:
        metadata["related_identifiers"] = []
    (root / "zenodo_metadata.json").write_text(json.dumps(metadata))
    with pytest.raises(verifier.ReleaseContractError):
        verifier.verify_metadata()


def test_fresh_axiom_census_must_match_the_stored_dependencies(tmp_path, monkeypatch):
    lean = tmp_path / "lean4"
    lean.mkdir()
    (lean / "probe.lean").write_text("theorem probe : True := by trivial\n#print axioms probe\n")
    (lean / "axiom_report.txt").write_text("'probe' depends on axioms: [propext]\n")
    monkeypatch.setattr(verifier, "ROOT", tmp_path)
    monkeypatch.setattr(verifier.subprocess, "run", lambda *a, **kw: SimpleNamespace(
        returncode=0, stdout="'probe' does not depend on any axioms\n", stderr="",
    ))
    with pytest.raises(verifier.ReleaseContractError, match="differ from the stored"):
        verifier.verify_lean_build_and_axioms()


@pytest.mark.parametrize("receipt", [
    "'probe' depends on axioms: [sorryAx]\n",
    "'probe' does not depend on any axioms\n'extra' does not depend on any axioms\n",
])
def test_forged_stored_axiom_receipt_is_rejected(tmp_path, monkeypatch, receipt):
    lean = tmp_path / "lean4"
    lean.mkdir()
    (lean / "probe.lean").write_text("theorem probe : True := by trivial\n#print axioms probe\n")
    (lean / "axiom_report.txt").write_text(receipt)
    monkeypatch.setattr(verifier, "ROOT", tmp_path)
    with pytest.raises(verifier.ReleaseContractError):
        verifier.verify_lean_build_and_axioms()
