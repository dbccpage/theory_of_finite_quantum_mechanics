"""Gauge oracle sources and controls remain regular across execution."""

from __future__ import annotations

import hashlib
import importlib.util
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]


def verifier():
    spec = importlib.util.spec_from_file_location(
        "gauge_result", ROOT / "scripts/verify_gauge_result.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("control", ["inputs.json", "verifier.py", "source.py"])
def test_same_byte_controls_refuse_symlinks(control, tmp_path):
    module = verifier()
    original = tmp_path / "original"
    original.write_bytes(b"identical bytes\n")
    substitute = tmp_path / control
    os.symlink(original, substitute)
    with pytest.raises(ValueError, match="regular"):
        module.regular(substitute)


def test_same_byte_control_under_linked_parent_refuses(tmp_path):
    module = verifier()
    original = tmp_path / "original"
    original.mkdir()
    (original / "control").write_bytes(b"identical bytes\n")
    link = tmp_path / "linked"
    os.symlink(original, link, target_is_directory=True)
    with pytest.raises(ValueError, match="parent is not a regular"):
        module.regular(link / "control")


def test_post_execution_digest_and_regular_custody_are_rechecked(tmp_path):
    module = verifier()
    source = tmp_path / "source.py"
    original = b"original bytes\n"
    source.write_bytes(original)
    snapshot = {source: hashlib.sha256(original).hexdigest()}
    module.verify_unchanged(snapshot)
    source.write_bytes(b"changed during execution\n")
    with pytest.raises(ValueError, match="replay input changed"):
        module.verify_unchanged(snapshot)
    target = tmp_path / "same-byte-target"
    target.write_bytes(original)
    source.unlink()
    os.symlink(target, source)
    with pytest.raises(ValueError, match="regular"):
        module.verify_unchanged(snapshot)


def test_directory_control_refuses(tmp_path):
    module = verifier()
    with pytest.raises(ValueError, match="regular"):
        module.regular(tmp_path)
