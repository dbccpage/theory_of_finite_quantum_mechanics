"""Pytest configuration and environment fixtures for E2E tests."""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

# Ensure code/python and code/python/src are properly mounted in sys.path
_PY_DIR = Path(__file__).resolve().parents[2]
_SRC_DIR = _PY_DIR / "src"
_REPO_ROOT = Path(__file__).resolve().parents[4]

for directory in [str(_SRC_DIR), str(_PY_DIR)]:
    if directory not in sys.path:
        sys.path.insert(0, directory)


@pytest.fixture(autouse=True)
def verify_pythonpath():
    """Verify that source modules are importable."""
    assert str(_SRC_DIR) in sys.path or str(_PY_DIR) in sys.path
