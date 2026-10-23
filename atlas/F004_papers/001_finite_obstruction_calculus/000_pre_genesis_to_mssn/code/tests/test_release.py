"""Release-gate regressions using small standalone package fixtures."""
from __future__ import annotations

import datetime
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "code"))


def load_module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


release = load_module("pre_mssn_release", "tools/rebuild_release.py")
verifier = load_module("pre_mssn_deposit", "verify_deposit.py")
deposit_paths = load_module("pre_mssn_paths", "code/deposit_paths.py")


@pytest.fixture
def package(tmp_path):
    package = tmp_path / "paper"
    package.mkdir()
    for relative in ("verify_deposit.py", "tools/rebuild_release.py", "code/deposit_paths.py"):
        target = package / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    for relative in ("paper.md", "paper_change_log.md", "README.md", "LICENSE", "LICENSE-CODE",
                     "pyproject.toml", "docs/descriptions.md", "docs/references.md"):
        target = package / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("fixture\n", encoding="utf-8")
    day = "2026-10-09"
    (package / "zenodo_metadata.json").write_text(
        json.dumps({"publication_date": day, "description": "fixture"}) + "\n", encoding="utf-8")
    release.refresh(package)
    assert release.validate(package) == []
    return package


def run_verifier(package):
    return subprocess.run([sys.executable, "verify_deposit.py"], cwd=package,
                          capture_output=True, text=True, check=False)


def test_documented_gate_accepts_complete_archive(package):
    result = run_verifier(package)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("mutation", ["missing", "invalid", "member", "prefix", "suffix", "duplicate"])
def test_documented_gate_rejects_archive_mutations(package, mutation):
    archive = release.archive_path(package)
    original = archive.read_bytes()
    if mutation == "missing":
        archive.unlink()
    elif mutation == "invalid":
        archive.write_bytes(b"not a ZIP")
    elif mutation == "prefix":
        archive.write_bytes(b"prefix" + original)
    elif mutation == "suffix":
        archive.write_bytes(original + b"suffix")
    else:
        with zipfile.ZipFile(archive) as source:
            rows = [(info, source.read(info)) for info in source.infolist()]
        with zipfile.ZipFile(archive, "w") as target:
            for index, (info, data) in enumerate(rows):
                target.writestr(info, data + b"changed" if mutation == "member" and index == 0 else data)
            if mutation == "duplicate":
                info, data = rows[0]
                info.filename = info.filename.upper()
                target.writestr(info, data)
    result = run_verifier(package)
    assert result.returncode != 0, result.stdout + result.stderr
    assert "Verification PASSED" not in result.stdout


def test_manifest_agreement_checked_independently(package):
    manifest = package / "MANIFEST.sha256"
    manifest.write_bytes(manifest.read_bytes().splitlines(keepends=True)[0])
    sums = package / "SHA256SUMS"
    entries = release.read_manifest(sums, package)
    entries = [(name, release.sha256_file(manifest) if name == manifest.name else digest)
               for name, digest in entries]
    sums.write_bytes(release.render(entries))
    archive = release.archive_path(package)
    release.build_archive(package, archive, sorted(entries + [(sums.name, release.sha256_file(sums))]))
    result = run_verifier(package)
    assert result.returncode != 0, result.stdout + result.stderr
    assert "SHA256SUMS does not equal" in result.stdout


def test_rebuild_uses_declared_date_across_calendar_days(package, monkeypatch):
    metadata = package / "zenodo_metadata.json"
    metadata.write_text(json.dumps({"publication_date": "2026-10-09"}) + "\n", encoding="utf-8")
    outputs = []
    for day in (datetime.date(2026, 10, 10), datetime.date(2027, 4, 20)):
        class Clock(datetime.date):
            @classmethod
            def today(cls):
                return day
        monkeypatch.setattr(release.datetime, "date", Clock)
        release.refresh(package)
        assert release.validate(package) == []
        archive = release.archive_path(package)
        assert archive.name == "paper_2026-10-09.zip"
        outputs.append(archive.read_bytes())
    assert outputs[0] == outputs[1]


@pytest.mark.parametrize("control", ["MANIFEST.sha256", "SHA256SUMS", "zenodo_metadata.json", "archive"])
@pytest.mark.parametrize("mutation", ["directory", "symlink", "reparse"])
def test_release_controls_refuse_nonregular_entries(package, monkeypatch, control, mutation):
    path = release.archive_path(package) if control == "archive" else package / control
    original = path.read_bytes()
    if mutation == "directory":
        path.unlink()
        path.mkdir()
    elif mutation == "symlink":
        source = package.parent / "same-bytes"
        source.write_bytes(original)
        path.unlink()
        try:
            path.symlink_to(source)
        except OSError as error:
            pytest.skip(f"host does not allow symlinks: {error}")
    else:
        lstat = Path.lstat
        def reparse_stat(candidate, *args, **kwargs):
            if candidate == path:
                return SimpleNamespace(st_mode=lstat(candidate, *args, **kwargs).st_mode,
                                       st_file_attributes=0x400)
            return lstat(candidate, *args, **kwargs)
        monkeypatch.setattr(Path, "lstat", reparse_stat)
    assert release.validate(package)


def test_traversal_errors_are_fatal(package, monkeypatch):
    def broken_walk(*args, onerror=None, **kwargs):
        if onerror:
            onerror(PermissionError("unreadable retained directory"))
        return iter(())
    monkeypatch.setattr(os, "walk", broken_walk)
    with pytest.raises(PermissionError, match="unreadable retained"):
        deposit_paths.walk_files(package, set(), set(), set())


def test_mutable_checks_cannot_replace_verified_release(package, monkeypatch, capsys):
    monkeypatch.setattr(verifier, "ROOT", package)
    monkeypatch.setattr(verifier, "MANIFEST", package / "SHA256SUMS")
    monkeypatch.setattr(sys, "argv", ["verify_deposit.py", "--test", "code/tests/test_fixture.py"])
    def replacing_tests(targets):
        (package / "paper.md").write_text("replaced during subprocess\n", encoding="utf-8")
        release.refresh(package)
        return []
    monkeypatch.setattr(verifier, "check_tests", replacing_tests)
    assert verifier.main() == 1
    assert "changed during" in capsys.readouterr().out


def test_lean_subprocess_cannot_mutate_payload(package, monkeypatch, capsys):
    monkeypatch.setattr(verifier, "ROOT", package)
    monkeypatch.setattr(sys, "argv", ["verify_deposit.py", "--lean"])
    def mutating_lean():
        (package / "paper.md").write_text("changed during Lean\n", encoding="utf-8")
        return []
    monkeypatch.setattr(verifier, "check_lean", mutating_lean)
    assert verifier.main() == 1
    assert "hash mismatch" in capsys.readouterr().out.lower()
