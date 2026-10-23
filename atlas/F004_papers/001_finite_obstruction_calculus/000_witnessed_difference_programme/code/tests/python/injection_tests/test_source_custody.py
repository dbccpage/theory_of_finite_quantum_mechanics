"""Same-byte control substitutions and traversal errors must fail before replay."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[4]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def release_tree(tmp_path, monkeypatch):
    module = load("verify_release")
    root = tmp_path / "package"
    root.mkdir()
    for relative in module.REQUIRED_FILES:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture\n", encoding="utf-8")
    for prefix in module.REQUIRED_PREFIXES:
        path = root / prefix / "fixture.txt"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture\n", encoding="utf-8")
    monkeypatch.setattr(module, "ROOT", root)
    monkeypatch.setattr(module, "MANIFEST", root / "manifests/release_manifest.json")
    monkeypatch.setattr(module, "RECEIPT", root / "manifests/release_verification.json")
    module.write_release_files()
    module.check_release_files()
    return module, root


@pytest.mark.parametrize("name", ["MANIFEST", "RECEIPT"])
def test_same_byte_release_control_symlink_refuses_read_and_write(tmp_path, monkeypatch, name):
    module, _ = release_tree(tmp_path, monkeypatch)
    control = getattr(module, name)
    original = tmp_path / "original.json"
    original.write_bytes(control.read_bytes())
    control.unlink()
    os.symlink(original, control)
    with pytest.raises(module.ReleaseInventoryError, match="non-regular"):
        module.check_release_files()
    with pytest.raises(module.ReleaseInventoryError, match="non-regular"):
        module.write_release_files()


@pytest.mark.parametrize("name", ["MANIFEST.sha256", "SHA256SUMS"])
def test_same_byte_checksum_control_symlink_refuses(tmp_path, name):
    module = load("regen_sha256sums")
    root = tmp_path / "package"
    root.mkdir()
    original = tmp_path / "original.txt"
    original.write_bytes(b"same bytes\n")
    os.symlink(original, root / name)
    with pytest.raises(ValueError, match="non-regular"):
        module.iter_files(root)


@pytest.mark.parametrize("name", ["MANIFEST", "RECEIPT"])
def test_release_directory_control_refuses(tmp_path, monkeypatch, name):
    module, _ = release_tree(tmp_path, monkeypatch)
    control = getattr(module, name)
    control.unlink()
    control.mkdir()
    with pytest.raises(module.ReleaseInventoryError, match="non-regular"):
        module.check_release_files()
    with pytest.raises(module.ReleaseInventoryError, match="non-regular"):
        module.write_release_files()


@pytest.mark.parametrize("name", ["verify_finite_derivations", "verify_source_replays",
                                  "verify_certified_progress"])
def test_proof_and_source_controls_refuse_same_byte_symlinks(tmp_path, name):
    module = load(name)
    original = tmp_path / "original.txt"
    original.write_bytes(b"same bytes\n")
    substitute = tmp_path / "control.txt"
    os.symlink(original, substitute)
    with pytest.raises(ValueError, match="regular"):
        module.regular(substitute)


def test_retained_nested_build_names_are_inventoried(tmp_path, monkeypatch):
    module, root = release_tree(tmp_path, monkeypatch)
    for relative in ("docs/build/retained.txt", "docs/b/retained.txt", "build/cache.txt"):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"retained or declared cache\n")
    inventory = {p.relative_to(root).as_posix() for p in module._inventory_paths()}
    assert {"docs/build/retained.txt", "docs/b/retained.txt"} <= inventory
    assert "build/cache.txt" not in inventory
    checksum = load("regen_sha256sums")
    inventory = {p.relative_to(root).as_posix() for p in checksum.iter_files(root)}
    assert {"docs/build/retained.txt", "docs/b/retained.txt"} <= inventory
    assert "build/cache.txt" not in inventory


def test_retained_meron_source_remains_inventoried_and_hash_checked(tmp_path, monkeypatch):
    module, root = release_tree(tmp_path, monkeypatch)
    relative = "docs/meron_field_limit_derivations/meron_spacetime_field_theorems.md"
    source = root / relative
    source.parent.mkdir()
    source.write_bytes(b"retained upstream source\n")
    module.write_release_files()
    module.check_release_files()
    manifest = module.expected_manifest()
    assert relative in {item["path"] for item in manifest["files"]}
    assert manifest["publication_surfaces"]["retained_source_monographs"] == [relative]
    source.write_bytes(b"changed retained source\n")
    with pytest.raises(module.ReleaseInventoryError, match="size/hash drift"):
        module.check_release_files()


@pytest.mark.parametrize(
    "relative",
    ["docs/duplicate_monograph.md", "docs/meron_field_limit_derivations/duplicate_monograph.md"],
)
def test_unclassified_duplicate_manuscript_still_refuses(tmp_path, monkeypatch, relative):
    module, root = release_tree(tmp_path, monkeypatch)
    duplicate = root / relative
    duplicate.parent.mkdir(parents=True, exist_ok=True)
    duplicate.write_bytes(b"unclassified manuscript\n")
    with pytest.raises(module.ReleaseInventoryError, match="not singletons"):
        module.write_release_files()


def test_traversal_error_callbacks_are_fatal(tmp_path, monkeypatch):
    module, root = release_tree(tmp_path, monkeypatch)

    def unreadable(_root, *, onerror, followlinks):
        assert followlinks is False
        onerror(PermissionError("retained directory unreadable"))
        yield

    monkeypatch.setattr(module, "os", SimpleNamespace(walk=unreadable))
    with pytest.raises(module.ReleaseInventoryError, match="traversal failed"):
        module._inventory_paths()
    checksum = load("regen_sha256sums")
    monkeypatch.setattr(checksum, "os", SimpleNamespace(walk=unreadable))
    with pytest.raises(ValueError, match="traversal failed"):
        checksum.iter_files(root)


@pytest.mark.monorepo
def test_excluded_cache_symlink_is_not_hidden_by_teaching_walker(tmp_path):
    script = (
        ROOT.parents[4]
        / "omega_engine_education/documentation/070_witnessed_difference_programme_wdp/scripts/check_learning_paths.py"
    )
    spec = importlib.util.spec_from_file_location("learning_paths", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    outside = tmp_path / "outside"
    outside.mkdir()
    root = tmp_path / "teaching"
    root.mkdir()
    os.symlink(outside, root / "target", target_is_directory=True)
    with pytest.raises(ValueError, match="symlink/reparse"):
        list(module.files(root))
