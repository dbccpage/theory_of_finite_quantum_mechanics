"""Regression support for governance evidence custody and mutation outcomes."""
from __future__ import annotations
import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType
import pytest


def load(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    if spec is None or spec.loader is None:
        raise RuntimeError("missing evidence tool")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


capture = load("capture_evidence")
mutation = load("mutation_campaign")


@pytest.mark.parametrize("code,output,expected", [
    (101, "error: failed to download dependency", "INCONCLUSIVE"),
    (101, "error: could not compile due to a linker failure", "INCONCLUSIVE"),
    (101, "error[E0308]: mismatched types", "INVALID"),
    (101, "test result: FAILED. 4 passed; 1 failed; 0 ignored;", "KILLED"),
    (0, "test result: ok. 5 passed; 0 failed; 0 ignored;", "SURVIVED"),
    (0, "test result: ok. 0 passed; 0 failed; 0 ignored;", "INCONCLUSIVE"),
    (101, "arbitrary failure", "INCONCLUSIVE"),
    (0, "", "INCONCLUSIVE"),
])
def test_outcomes_require_libtest_evidence(code: int, output: str, expected: str) -> None:
    assert mutation.classify_outcome(code, output) == expected


def test_existing_destination_is_preserved(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "Cargo.toml").write_text("source")
    destination = tmp_path / "valuable"
    destination.mkdir()
    sentinel = destination / "keep.txt"
    sentinel.write_bytes(b"unrelated work")
    with pytest.raises(FileExistsError):
        capture.prepare_copy(source, destination)
    assert sentinel.read_bytes() == b"unrelated work"
    assert (source / "Cargo.toml").read_text() == "source"


@pytest.mark.parametrize("nested", [False, True])
def test_source_or_nested_destination_is_refused(tmp_path: Path, nested: bool) -> None:
    source = tmp_path / "source"
    source.mkdir()
    destination = source / "nested" if nested else source
    with pytest.raises(ValueError):
        capture.prepare_copy(source, destination)
    assert list(source.iterdir()) == []


def test_snapshot_hashes_tested_bytes(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "Cargo.toml").write_bytes(b"captured")
    snapshot = capture.prepare_copy(source, tmp_path / "snapshot")
    before = capture.source_hashes(snapshot)
    (source / "Cargo.toml").write_bytes(b"changed later")
    assert capture.source_hashes(snapshot) == before
    assert capture.source_hashes(source) != before


def test_every_mutant_uses_a_fresh_snapshot(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    crate = tmp_path / "crate"
    (crate / "src").mkdir(parents=True)
    source = crate / "src/lib.rs"
    source.write_bytes(b"pub fn value() -> bool { true }\n")
    item = next(mutation.mutants(crate))
    def fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(["cargo"], 101, "dependency missing", "")
    monkeypatch.setattr(mutation.subprocess, "run", fake_run)
    first = mutation.run_one(item, crate, tmp_path / "scratch", 1)
    (crate / "src/helper.rs").write_bytes(b"new source")
    second = mutation.run_one(item, crate, tmp_path / "scratch", 1)
    assert first["snapshot"] != second["snapshot"]
    assert not (Path(first["snapshot"]) / "src/helper.rs").exists()
    assert (Path(second["snapshot"]) / "src/helper.rs").read_bytes() == b"new source"
    assert first["outcome"] == second["outcome"] == "INCONCLUSIVE"
    assert source.read_bytes() == b"pub fn value() -> bool { true }\n"
