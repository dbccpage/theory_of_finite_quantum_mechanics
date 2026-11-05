"""Release integrity regressions for complete, canonical envelopes."""

import importlib.util
import json
import os
import stat
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("po034_release", ROOT / "tools/rebuild_release.py")
release = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = release
spec.loader.exec_module(release)


@pytest.fixture
def package(tmp_path):
    p = tmp_path / "sample_paper"
    (p / "code").mkdir(parents=True)
    (p / "code/deposit_paths.py").write_bytes((ROOT / "code/deposit_paths.py").read_bytes())
    (p / "zenodo_metadata.json").write_text(json.dumps({"publication_date": "2026-10-02"}))
    (p / "README.md").write_text("A finite test payload.\n")
    release.refresh(p)
    return p


def test_manifest_and_archive_rebuild_are_complete_and_repeatable(package):
    assert release.validate(package) == []
    archive = release.archive_path(package)
    before = archive.read_bytes()
    release.refresh(package)
    assert archive.read_bytes() == before
    assert release.validate(package) == []


def test_new_unlisted_payload_invalidates_old_envelope(package):
    (package / "new_evidence.md").write_text("New payload.\n")
    assert any("current regular payload" in e for e in release.validate(package))
    release.refresh(package)
    assert release.validate(package) == []


def test_changed_payload_is_not_hidden_by_archive(package):
    (package / "README.md").write_text("Changed.\n")
    errors = release.validate(package)
    assert any("hash mismatch" in e for e in errors)


def test_duplicate_control_records_fail(package):
    sums = package / "SHA256SUMS"
    sums.write_text(sums.read_text() + sums.read_text().splitlines()[0] + "\n")
    assert release.validate(package)


def test_escaping_manifest_path_is_rejected(package):
    (package / "MANIFEST.sha256").write_text("0" * 64 + "  ../outside\n")
    assert release.validate(package)


def test_timestamp_is_pinned_to_metadata_and_old_archive_removed(package):
    metadata = package / "zenodo_metadata.json"
    metadata.write_text(json.dumps({"publication_date": "2026-10-03"}))
    assert any("publication_date" in e for e in release.validate(package))
    release.refresh(package)
    assert release.archive_path(package).name.endswith("_2026-10-03.zip")
    assert len(list(package.glob("*.zip"))) == 1
    assert release.validate(package) == []


def test_control_files_cannot_be_payload_includes(package):
    with pytest.raises(ValueError):
        release.refresh(package, ("SHA256SUMS",))


@pytest.mark.parametrize("mode", ["prefix", "suffix", "duplicate", "case_collision"])
def test_full_archive_envelope_rejects_extra_bytes_and_members(package, mode):
    archive = release.archive_path(package)
    if mode == "prefix":
        archive.write_bytes(b"prefix" + archive.read_bytes())
    elif mode == "suffix":
        archive.write_bytes(archive.read_bytes() + b"suffix")
    else:
        with zipfile.ZipFile(archive, "a") as output:
            name = f"{package.name}/README.md"
            if mode == "case_collision":
                name = f"{package.name}/readme.md"
            output.writestr(name, b"A finite test payload.\n")
    assert release.validate(package)


def test_exact_selected_archive_is_qualified(package, tmp_path):
    selected = tmp_path / release.archive_path(package).name
    selected.write_bytes(release.archive_path(package).read_bytes())
    assert release.validate(package, selected) == []
    selected.write_bytes(selected.read_bytes() + b"not canonical")
    assert release.validate(package, selected)
    selected.unlink()
    assert release.validate(package, selected)


def alter_control_type(path, kind, monkeypatch):
    original_lstat = Path.lstat

    def altered_lstat(item, *args, **kwargs):
        result = original_lstat(item, *args, **kwargs)
        if item == path:
            if kind == "nonregular":
                values = list(result)
                values[0] = stat.S_IFIFO | 0o644
                return os.stat_result(values)
            if kind == "reparse":
                from types import SimpleNamespace

                return SimpleNamespace(st_mode=result.st_mode, st_file_attributes=0x400)
        return result

    original_symlink = Path.is_symlink
    monkeypatch.setattr(Path, "lstat", altered_lstat)
    monkeypatch.setattr(
        Path, "is_symlink",
        lambda item: (item == path and kind == "symlink") or original_symlink(item),
    )


@pytest.mark.parametrize("control", ["MANIFEST.sha256", "SHA256SUMS", "archive"])
@pytest.mark.parametrize("kind", ["symlink", "reparse", "nonregular"])
def test_nonregular_release_controls_are_refused(package, monkeypatch, control, kind):
    path = release.archive_path(package) if control == "archive" else package / control
    alter_control_type(path, kind, monkeypatch)
    assert release.validate(package)


def test_walk_errors_are_fatal(package, monkeypatch):
    spec = importlib.util.spec_from_file_location("po034_paths", package / "code/deposit_paths.py")
    paths = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(paths)

    def inaccessible(*args, **kwargs):
        kwargs["onerror"](PermissionError("retained directory unreadable"))
        return iter(())

    monkeypatch.setattr(os, "walk", inaccessible)
    with pytest.raises(PermissionError, match="unreadable"):
        paths.walk_files(package, set(), set(), set())
    assert release.validate(package)


@pytest.mark.parametrize("mutation", ["payload", "unlisted", "manifest", "sums", "archive"])
def test_post_replay_custody_refuses_successful_mutating_process(package, monkeypatch, mutation):
    spec = importlib.util.spec_from_file_location("po034_custody", ROOT / "verify_deposit.py")
    verifier = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = verifier
    spec.loader.exec_module(verifier)
    monkeypatch.setattr(verifier, "ROOT", package)
    initial = verifier.release_snapshot()

    def mutate(*args, **kwargs):
        target = {
            "payload": package / "README.md", "unlisted": package / "new.txt",
            "manifest": package / "MANIFEST.sha256", "sums": package / "SHA256SUMS",
            "archive": release.archive_path(package),
        }[mutation]
        target.write_bytes(target.read_bytes() + b"drift" if target.exists() else b"new")
        return subprocess.CompletedProcess(args[0], 0, stdout="success", stderr="")

    monkeypatch.setattr(verifier.subprocess, "run", mutate)
    assert not verifier.run(["synthetic-replay"], "mutation probe", initial, None)


@pytest.mark.parametrize("control", ["MANIFEST.sha256", "SHA256SUMS", "archive"])
@pytest.mark.parametrize("kind", ["symlink", "reparse", "nonregular"])
def test_post_replay_refuses_same_byte_control_type_changes(package, monkeypatch, control, kind):
    spec = importlib.util.spec_from_file_location("po034_control_custody", ROOT / "verify_deposit.py")
    verifier = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = verifier
    spec.loader.exec_module(verifier)
    monkeypatch.setattr(verifier, "ROOT", package)
    initial = verifier.release_snapshot()
    path = release.archive_path(package) if control == "archive" else package / control
    before = path.read_bytes()

    def replace_control(*args, **kwargs):
        alter_control_type(path, kind, monkeypatch)
        # Content bytes remain identical; changed file type alone must refuse.
        return subprocess.CompletedProcess(args[0], 0, stdout="success", stderr="")

    monkeypatch.setattr(verifier.subprocess, "run", replace_control)
    assert not verifier.run(["synthetic-replay"], "same-byte control probe", initial, None)
    assert path.read_bytes() == before


def test_extracted_mode_is_explicit_and_still_checks_payload(package):
    release.archive_path(package).unlink()
    assert release.validate(package)
    assert release.validate(package, extracted=True) == []
    (package / "tampered.txt").write_text("not in manifest")
    assert release.validate(package, extracted=True)
