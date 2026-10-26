"""Adversarial custody checks for the source relocation, without model calls."""
from __future__ import annotations

import copy
import importlib.util
import os
from pathlib import Path

import pytest

PACKAGE = Path(__file__).resolve().parents[4]
SPEC = importlib.util.spec_from_file_location("wdp_consolidation", PACKAGE / "scripts/verify_consolidation.py")
assert SPEC and SPEC.loader
CUSTODY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CUSTODY)


@pytest.fixture
def fixture(tmp_path):
    (tmp_path / "retained.txt").write_bytes(b"original")
    digest = CUSTODY.sha256(b"original")
    manifest = {"schema": "wdp-source-consolidation-v1", "removed_roots": ["retired"],
                "assets": [{"source_path": "old/original.txt", "destination_path": "retained.txt",
                            "source_sha256": digest, "destination_sha256": digest,
                            "content_amended": False, "disposition": "moved"}]}
    return tmp_path, manifest


def test_retained_original_passes(fixture):
    root, manifest = fixture
    assert CUSTODY.verify(manifest, root)["source_assets"] == 1


def test_changed_bytes_refused(fixture):
    root, manifest = fixture
    (root / "retained.txt").write_bytes(b"changed")
    with pytest.raises(ValueError, match="bytes changed"):
        CUSTODY.verify(manifest, root)


def test_missing_asset_refused(fixture):
    root, manifest = fixture
    (root / "retained.txt").unlink()
    with pytest.raises(FileNotFoundError):
        CUSTODY.verify(manifest, root)


def test_duplicate_source_refused(fixture):
    root, manifest = fixture
    manifest["assets"].append(copy.deepcopy(manifest["assets"][0]))
    with pytest.raises(ValueError, match="duplicated"):
        CUSTODY.verify(manifest, root)


def test_retired_root_refused(fixture):
    root, manifest = fixture
    (root / "retired").mkdir()
    with pytest.raises(ValueError, match="retired root"):
        CUSTODY.verify(manifest, root)


def test_path_escape_refused(fixture):
    root, manifest = fixture
    manifest["assets"][0]["destination_path"] = "../escaped.txt"
    with pytest.raises(ValueError):
        CUSTODY.verify(manifest, root)


def test_same_byte_symlink_refused(fixture):
    root, manifest = fixture
    original = root / "retained.txt"
    link = root / "redirect.txt"
    try:
        os.symlink(original, link)
    except OSError as error:
        pytest.skip(f"host cannot create symlinks: {error}")
    manifest["assets"][0]["destination_path"] = link.name
    with pytest.raises(ValueError, match="redirected"):
        CUSTODY.verify(manifest, root)


def test_non_regular_entry_refused(fixture):
    root, manifest = fixture
    (root / "directory").mkdir()
    manifest["assets"][0]["destination_path"] = "directory"
    with pytest.raises(ValueError, match="regular file"):
        CUSTODY.verify(manifest, root)
