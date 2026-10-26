"""Release path containment, inventory integrity and verifier failure regressions."""

import importlib.util
import stat
import sys
import zipfile
from pathlib import Path
from types import SimpleNamespace

import pytest

PACKAGE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE / "scripts"))
import deposit_files as d  # noqa: E402
import lean_census  # noqa: E402
import mutation_audit  # noqa: E402


def seal(root):
    names = d.manifest_names(root)
    (root / d.MANIFEST).write_text(d.render_sums(root, names), encoding="utf-8")
    (root / d.SUMS).write_text(d.render_sums(root, sorted(names + [d.MANIFEST])), encoding="utf-8")


def test_standalone_archive_includes_both_manifests_and_no_outer_zip(tmp_path):
    (tmp_path / "payload.txt").write_text("exact payload", encoding="utf-8")
    seal(tmp_path)
    target = tmp_path / d.ARCHIVE
    d.build_archive(target, tmp_path)
    assert d.verify_hashes(tmp_path) == d.verify_archive(target, tmp_path) == []
    with zipfile.ZipFile(target) as archive:
        assert len(archive.namelist()) == 3
        assert all(info.create_system == 3 for info in archive.infolist())
        archive.extractall(tmp_path / "unpacked")
    extracted = tmp_path / "unpacked" / d.ARCHIVE_ROOT
    assert d.verify_hashes(extracted) == []
    assert not (extracted / d.ARCHIVE).exists()
    (extracted / "extra.txt").write_text("not declared", encoding="utf-8")
    assert d.verify_hashes(extracted)
    with pytest.raises(ValueError, match="unverified payload"):
        d.build_archive(extracted / d.ARCHIVE, extracted)


def test_changed_payload_and_changed_zip_are_detected(tmp_path):
    target = tmp_path / "payload.txt"
    target.write_text("original", encoding="utf-8")
    seal(tmp_path)
    d.build_archive(tmp_path / d.ARCHIVE, tmp_path)
    target.write_text("edited", encoding="utf-8")
    assert any("hash mismatch" in error for error in d.verify_hashes(tmp_path))
    assert d.verify_archive(tmp_path / d.ARCHIVE, tmp_path)
    target.unlink()
    assert d.verify_hashes(tmp_path)


@pytest.mark.parametrize("relative", ["extra.zip", "nested/extra.zip"])
def test_unexpected_zip_files_cannot_bypass_the_inventory(tmp_path, relative):
    (tmp_path / "payload.txt").write_text("payload", encoding="utf-8")
    seal(tmp_path)
    extra = tmp_path / relative
    extra.parent.mkdir(exist_ok=True)
    extra.write_bytes(b"unmanifested archive")
    assert any("unexpected ZIP" in error for error in d.verify_hashes(tmp_path))
    with pytest.raises(ValueError, match="unexpected ZIP"):
        d.build_archive(tmp_path / d.ARCHIVE, tmp_path)


@pytest.mark.parametrize("mode,system", [(stat.S_IFIFO, 3), (stat.S_IFCHR, 3),
                                        (stat.S_IFSOCK, 3), (stat.S_IFLNK, 3),
                                        (stat.S_IFREG, 0)])
def test_archive_rejects_special_members_and_undeclared_platform(tmp_path, mode, system):
    (tmp_path / "payload.txt").write_text("payload", encoding="utf-8")
    seal(tmp_path)
    archive_path = tmp_path / d.ARCHIVE
    d.build_archive(archive_path, tmp_path)
    with zipfile.ZipFile(archive_path) as archive:
        entries = [(info, archive.read(info)) for info in archive.infolist()]
    with zipfile.ZipFile(archive_path, "w") as archive:
        for info, data in entries:
            if info.filename.endswith("/payload.txt"):
                info.external_attr = (mode | 0o644) << 16
                info.create_system = system
            archive.writestr(info, data)
    assert any("nonregular archive member" in error for error in d.verify_archive(archive_path, tmp_path))


@pytest.mark.parametrize("path", ["", "../escape", "/absolute", "C:/absolute", "a\\b", "a//b", "./a", "a/../b", "a\nb"])
def test_noncanonical_manifest_paths_are_rejected(path):
    with pytest.raises(ValueError, match="unsafe deposit path"):
        d.canonical_path(path)


@pytest.mark.parametrize("body", ["bad line\n", "0" * 64 + "  ../escape\n",
                                  ("0" * 64 + "  a\n") * 2,
                                  "0" * 64 + "  z\n" + "0" * 64 + "  a\n"])
def test_malformed_duplicate_and_unsorted_checksum_entries_fail(tmp_path, body):
    manifest = tmp_path / d.MANIFEST
    manifest.write_text(body, encoding="utf-8")
    with pytest.raises(ValueError):
        d.parse_sums(manifest)
    assert d.verify_hashes(tmp_path)


def test_cache_directories_are_pruned_before_traversal(tmp_path, monkeypatch):
    (tmp_path / "payload").write_bytes(b"payload")
    for directory in (".lake", ".venv", ".mypy_cache", ".ruff_cache", ".git", "lean4/b", "code/ddc/ddc_core.egg-info"):
        cache = tmp_path / directory
        cache.mkdir(parents=True)
        (cache / "ignored").write_bytes(b"scratch")
    (tmp_path / ".coverage").write_bytes(b"scratch")
    assert d.deposit_files(tmp_path) == ["payload"]
    original = d.os.walk
    seen = []
    def walk(*args, **kwargs):
        for row in original(*args, **kwargs):
            seen.append(Path(row[0]).relative_to(tmp_path).as_posix())
            yield row
    monkeypatch.setattr(d.os, "walk", walk)
    assert d.deposit_files(tmp_path) == ["payload"]
    assert set(seen) == {".", "lean4", "code", "code/ddc"}


@pytest.mark.parametrize("mode,attributes", [(stat.S_IFLNK, 0), (stat.S_IFDIR, 0x400), (stat.S_IFIFO, 0)])
def test_links_reparse_points_and_nonregular_files_fail_closed(mode, attributes):
    path = SimpleNamespace(name="bad-entry", lstat=lambda: SimpleNamespace(st_mode=mode, st_file_attributes=attributes))
    with pytest.raises(ValueError):
        d.regular(path)


def test_lean_banner_normalization_preserves_version_and_commit():
    win = "Lean (version 4.34.0, x86_64-w64-windows-gnu, commit abc, Release)"
    linux = "Lean (version 4.34.0, x86_64-unknown-linux-gnu, commit abc, Release)"
    assert lean_census.normalize_version(win) == lean_census.normalize_version(linux)
    assert lean_census.report_body(win) != lean_census.report_body(linux.replace("abc", "def"))


@pytest.mark.parametrize("code", [2, 3, 4, 5])
def test_mutation_harness_errors_never_count_as_assertion_kills(tmp_path, monkeypatch, code):
    def failed(*args, **kwargs):
        (tmp_path / "pytest-result.xml").write_text('<testsuites><testsuite><testcase name="x"><error message="collection error"/></testcase></testsuite></testsuites>', encoding="utf-8")
        return SimpleNamespace(returncode=code)
    monkeypatch.setattr(mutation_audit.subprocess, "run", failed)
    status, assertions, error = mutation_audit.run_test(tmp_path, "test_missing.py")
    assert status == code and error and not assertions


def test_missing_pytest_report_is_a_harness_failure(tmp_path, monkeypatch):
    monkeypatch.setattr(mutation_audit.subprocess, "run", lambda *a, **kw: SimpleNamespace(returncode=1))
    assert mutation_audit.run_test(tmp_path, "test_missing.py") == (1, set(), True)


def test_verifier_rejects_missing_rebuilt_artifact(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("ddc_verifier_test", PACKAGE / "verify_deposit.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "run_script", lambda *args: [])
    assert len(module.check_artifacts()) == 2


def test_verifier_rejects_stale_deposited_tex(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("ddc_verifier_stale_tex", PACKAGE / "verify_deposit.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    (tmp_path / "discrete_deformation_calculus.tex").write_text("stale source", encoding="utf-8")
    def rebuilt(*args):
        target = Path(args[-1])
        target.mkdir(parents=True)
        (target / "discrete_deformation_calculus.tex").write_text("current source", encoding="utf-8")
        (target / "discrete_deformation_calculus.pdf").write_bytes(b"unused because source mismatch fails first")
        return []
    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "run_script", rebuilt)
    assert any("rebuilt TeX differs" in problem for problem in module.check_artifacts())
