"""Mutation controls for the source-bound verification envelope."""

import importlib.util
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]


def verifier():
    spec = importlib.util.spec_from_file_location(
        "three_derivations_custody", ROOT / "scripts/verify_locality_smearing_progress.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_same_byte_control_substitution_is_refused(tmp_path):
    module = verifier()
    original = tmp_path / "original.json"
    original.write_bytes(b'{"status":"PASS"}\n')
    substitute = tmp_path / "substitute.json"
    os.symlink(original, substitute)
    with pytest.raises(ValueError, match="regular"):
        module.regular(substitute)


def test_retained_directory_substitution_is_refused(tmp_path):
    module = verifier()
    original = tmp_path / "original"
    original.mkdir()
    (original / "proof.py").write_text("witness = 1\n", encoding="utf-8")
    retained = tmp_path / "retained"
    retained.mkdir()
    os.symlink(original, retained / "redirected", target_is_directory=True)
    with pytest.raises(ValueError, match="source directory"):
        list(module.tree_files(retained))


def test_unreadable_retained_directory_is_fatal(tmp_path, monkeypatch):
    module = verifier()

    def unreadable(_root, *, onerror, followlinks):
        assert followlinks is False
        onerror(PermissionError("unreadable retained input"))
        yield

    monkeypatch.setattr(module.os, "walk", unreadable)
    with pytest.raises(ValueError, match="traversal failed"):
        list(module.tree_files(tmp_path))
