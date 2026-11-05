"""Exact source custody and attribution refusals, independent of adapter proofs."""

import importlib.util
import json
import shutil
from pathlib import Path

import pytest

PAPER = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "observer_source_archive", PAPER / "scripts" / "verify_observer_source_archive.py"
)
assert SPEC is not None and SPEC.loader is not None
ARCHIVE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ARCHIVE)


def copy_custody(tmp_path):
    for relative in ("source_provenance.json", "docs/legacy_observer_inventory.json"):
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(PAPER / relative, destination)
    shutil.copytree(PAPER / "docs" / "source_archive", tmp_path / "docs" / "source_archive")
    return tmp_path


def test_exact_original_corpus_is_replayable_without_network():
    result = ARCHIVE.verify()
    assert result["original_files_checked"] == 44
    assert result["total_bytes"] == 1967435
    assert result["source_occurrences_indexed"] == 573
    assert result["cue_records_reviewed"] == 79


def test_changed_source_bytes_cannot_become_original_custody(tmp_path):
    root = copy_custody(tmp_path)
    member = next((root / "docs" / "source_archive" / "coda_original_source_snapshot").glob("*.txt"))
    member.write_bytes(member.read_bytes() + b"\nchanged")
    with pytest.raises(ValueError, match="bytes differ"):
        ARCHIVE.verify(root)


def test_education_six_cannot_replace_the_original_genesis_six(tmp_path):
    root = copy_custody(tmp_path)
    path = root / "docs" / "legacy_observer_inventory.json"
    inventory = json.loads(path.read_text(encoding="utf-8"))
    family = next(f for f in inventory["identified_families"] if f["family"] == "six-component genesis")
    family["fields"] = ["C", "p", "comparison", "W", "V", "tau"]
    path.write_text(json.dumps(inventory), encoding="utf-8")
    with pytest.raises(ValueError, match="actual source vocabulary"):
        ARCHIVE.verify(root)


def test_source_index_cannot_omit_a_recorded_semantic_occurrence(tmp_path):
    root = copy_custody(tmp_path)
    path = root / "docs" / "legacy_observer_inventory.json"
    inventory = json.loads(path.read_text(encoding="utf-8"))
    inventory["source_family_index"].pop()
    path.write_text(json.dumps(inventory), encoding="utf-8")
    with pytest.raises(ValueError, match="every recorded occurrence"):
        ARCHIVE.verify(root)
