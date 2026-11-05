"""Build custody controls, including Cargo's externally configured target."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

PAPER = next(parent for parent in Path(__file__).resolve().parents
             if (parent / "witnessed_difference_programme.md").is_file())
SPEC = importlib.util.spec_from_file_location(
    "native_build_custody_subject", PAPER / "code/causal_certificates/native/build_native.py"
)
assert SPEC is not None and SPEC.loader is not None
BUILDER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = BUILDER
SPEC.loader.exec_module(BUILDER)


def dependency_tree(tmp_path):
    root = tmp_path / "repo"
    workspace = root / "omega_engine/crates_rs"
    owner = workspace / "omega_wdp"
    (owner / "src").mkdir(parents=True)
    for path, text in ((workspace / "Cargo.toml", "[workspace]\n"),
                       (workspace / "Cargo.lock", "version = 4\n"),
                       (owner / "Cargo.toml", "[package]\n"),
                       (owner / "src/lib.rs", "// retained\n")):
        path.write_text(text, encoding="utf-8")
    package = {"manifest_path": str(owner / "Cargo.toml"), "source": None,
               "name": "omega_wdp", "version": "0.1.0"}
    return root, owner, package


def test_build_uses_metadata_target_and_retains_source_custody(tmp_path, monkeypatch):
    root, _, package = dependency_tree(tmp_path)
    target = tmp_path / "shared_cache"
    build = tmp_path / "adapter"
    binary = target / "debug/wdp_causal_replay.exe"

    def run(command, **kwargs):
        if command[0:2] == ["cargo", "metadata"]:
            stdout = json.dumps({"packages": [package], "target_directory": str(target)})
        elif command[0:2] == ["cargo", "build"]:
            binary.parent.mkdir(parents=True)
            binary.write_bytes(b"test-built-binary")
            stdout = ""
        elif command == ["rustc", "--version"]:
            stdout = "rustc test-version\n"
        else:
            raise AssertionError(command)
        assert kwargs["check"] is True
        return subprocess.CompletedProcess(command, 0, stdout, "")

    monkeypatch.setattr(BUILDER.subprocess, "run", run)
    monkeypatch.setattr(sys, "argv", ["build_native.py", "--source-root", str(root),
                                     "--build-dir", str(build)])
    BUILDER.main()
    receipt = json.loads((build / "native_build_receipt.json").read_text())
    assert receipt["binary_sha256"] == BUILDER.sha(binary)
    assert receipt["sources"] == BUILDER.source_snapshot(root, [package])
    assert not (build / "target").exists()


def test_inventory_detects_new_dependency_file(tmp_path):
    root, owner, package = dependency_tree(tmp_path)
    before = BUILDER.source_snapshot(root, [package])
    (owner / "src/late.rs").write_text("// new source\n", encoding="utf-8")
    assert BUILDER.source_snapshot(root, [package]) != before


def test_non_regular_control_refuses_same_byte_target(tmp_path, monkeypatch):
    control = tmp_path / "control"
    control.write_bytes(b"same bytes")
    original = Path.lstat

    def lstat(path, *args, **kwargs):
        value = original(path, *args, **kwargs)
        if path == control:
            fields = list(value)
            fields[0] = 0o120777
            return os.stat_result(fields)
        return value

    monkeypatch.setattr(Path, "lstat", lstat)
    with pytest.raises(ValueError, match="non-regular source file"):
        BUILDER.sha(control)


def test_dependency_traversal_errors_refuse(tmp_path, monkeypatch):
    root, _, package = dependency_tree(tmp_path)

    def walk(path, *, onerror):
        onerror(PermissionError("injected unreadable dependency"))
        return iter(())

    monkeypatch.setattr(BUILDER.os, "walk", walk)
    with pytest.raises(PermissionError, match="unreadable dependency"):
        BUILDER.source_snapshot(root, [package])
