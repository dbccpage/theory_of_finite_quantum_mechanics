"""Preprint release controls, including resealed stale renders and archive tampering."""
import hashlib
import importlib.util
import json
import shutil
import sys
import zipfile
from pathlib import Path

import pytest

_REPO_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").is_file()), Path(__file__).resolve().parents[3])
ROOT = _REPO_ROOT / "papers" / "core" / "mub6" if (_REPO_ROOT / "papers" / "core" / "mub6").exists() else Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("verify_publication", ROOT / "scripts/verify_publication.py")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


@pytest.fixture
def sealed(tmp_path):
    target = tmp_path / "preprint"
    shutil.copytree(ROOT / "zenodo/preprint", target, ignore=shutil.ignore_patterns("__pycache__"))
    return target


def reseal(root):
    entries = {}
    for p in root.rglob("*"):
        if p.is_file() and p.name not in {"manifest.sha256", "sha256sums"}:
            entries[p.relative_to(root).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    manifest = root / "manifest.sha256"
    manifest.write_text("".join(f"{digest}  {name}\n" for name, digest in sorted(entries.items())), encoding="utf-8")
    entries["manifest.sha256"] = hashlib.sha256(manifest.read_bytes()).hexdigest()
    (root / "sha256sums").write_text("".join(f"{digest}  {name}\n" for name, digest in sorted(entries.items())), encoding="utf-8")


def test_sealed_preprint_and_archive(sealed):
    module.verify(sealed, ROOT / "mub6_publication.zip")


def test_outer_envelope_seals_nested_manifests(tmp_path, monkeypatch):
    regen_spec = importlib.util.spec_from_file_location("regen_mub6_sums", ROOT / "scripts/regen_sha256sums.py")
    regen = importlib.util.module_from_spec(regen_spec)
    regen_spec.loader.exec_module(regen)
    outer_spec = importlib.util.spec_from_file_location("verify_mub6_outer", ROOT / "verify_deposit.py")
    outer = importlib.util.module_from_spec(outer_spec)
    outer_spec.loader.exec_module(outer)
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "manifest.sha256").write_text("nested manifest bytes")
    (nested / "sha256sums").write_text("nested sums bytes")
    manifest = tmp_path / "manifest.sha256"
    manifest.write_text(regen.render(tmp_path), encoding="utf-8")
    (tmp_path / "sha256sums").write_text(regen.render_sums(tmp_path, manifest), encoding="utf-8")
    monkeypatch.setattr(outer, "ROOT", tmp_path)
    monkeypatch.setattr(outer, "REQUIRED_PATTERNS", ())
    assert outer.check_manifest(tmp_path / "sha256sums") == []
    assert "nested/manifest.sha256" in manifest.read_text(encoding="utf-8")
    assert "nested/sha256sums" in manifest.read_text(encoding="utf-8")
    (nested / "sha256sums").write_text("mutated nested sums")
    assert "Hash mismatch: nested/sha256sums" in outer.check_manifest(tmp_path / "sha256sums")


def test_unmanifested_file_refused(sealed):
    (sealed / "unreviewed.md").write_text("unreviewed")
    with pytest.raises(ValueError, match="Manifest/tree disagreement"):
        module.verify(sealed)


def test_payload_mutation_refused(sealed):
    with (sealed / "mub6.pdf").open("ab") as stream:
        stream.write(b"tampered")
    with pytest.raises(ValueError, match="Hash mismatch"):
        module.verify(sealed)


def test_resealed_stale_render_refused(sealed):
    with (sealed / "mub6.md").open("a", encoding="utf-8") as stream:
        stream.write("\nA new substantive paragraph.\n")
    reseal(sealed)
    with pytest.raises(ValueError, match="Stale render binding"):
        module.verify(sealed)


def test_resealed_metadata_mismatch_refused(sealed):
    p = sealed / "zenodo_metadata.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["version"] = "9.0.0"
    p.write_text(json.dumps(data), encoding="utf-8")
    reseal(sealed)
    with pytest.raises(ValueError, match="header disagreement"):
        module.verify(sealed)


def test_incomplete_related_identifier_refused(sealed):
    p = sealed / "zenodo_metadata.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    del data["related_identifiers"][0]["identifier"]
    p.write_text(json.dumps(data), encoding="utf-8")
    reseal(sealed)
    with pytest.raises(ValueError, match="Incomplete related identifier"):
        module.verify(sealed)


def test_resealed_publication_promotion_refused(sealed):
    p = sealed / "release_identity.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["publication_ready"] = True
    p.write_text(json.dumps(data), encoding="utf-8")
    reseal(sealed)
    with pytest.raises(ValueError, match="cannot assert publication approval"):
        module.verify(sealed)


def test_archive_member_tamper_even_with_new_sidecar_refused(sealed, tmp_path):
    altered = tmp_path / "mub6_publication.zip"
    with zipfile.ZipFile(ROOT / "mub6_publication.zip") as source, zipfile.ZipFile(altered, "w") as target:
        for info in source.infolist():
            data = source.read(info)
            target.writestr(info, data + b"tampered" if info.filename == "mub6.pdf" else data)
    altered.with_suffix(".zip.sha256").write_text(
        f"{hashlib.sha256(altered.read_bytes()).hexdigest()}  {altered.name}\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Archive member mismatch"):
        module.verify(sealed, altered)


@pytest.mark.parametrize("prefix,suffix", [(b"prepended", b""), (b"", b"appended")])
def test_complete_archive_envelope_refuses_extra_bytes(sealed, tmp_path, prefix, suffix):
    altered = tmp_path / "mub6_publication.zip"
    altered.write_bytes(prefix + (ROOT / altered.name).read_bytes() + suffix)
    altered.with_suffix(".zip.sha256").write_text(
        f"{hashlib.sha256(altered.read_bytes()).hexdigest()}  {altered.name}\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Noncanonical complete archive bytes"):
        module.verify(sealed, altered)


def test_directory_traversal_errors_are_fatal(tmp_path, monkeypatch):
    import deposit_paths

    def unreadable_walk(root, **kwargs):
        kwargs["onerror"](PermissionError("retained directory unreadable"))
        return iter(())

    monkeypatch.setattr(deposit_paths.os, "walk", unreadable_walk)
    with pytest.raises(PermissionError, match="retained directory unreadable"):
        deposit_paths.walk_files(tmp_path, set(), set(), set())


@pytest.mark.parametrize("control", ["manifest.sha256", "sha256sums", "archive", "sidecar"])
def test_same_byte_control_symlinks_refused(sealed, tmp_path, control):
    archive = tmp_path / "mub6_publication.zip"
    shutil.copy2(ROOT / archive.name, archive)
    shutil.copy2(ROOT / (archive.name + ".sha256"), archive.with_suffix(".zip.sha256"))
    path = archive if control == "archive" else archive.with_suffix(".zip.sha256") if control == "sidecar" else sealed / control
    retained = tmp_path / (control.replace("/", "_") + ".retained")
    path.replace(retained)
    path.symlink_to(retained)
    with pytest.raises(ValueError, match="symlink or junction"):
        module.verify(sealed, archive)
