"""Pytest fixtures for WDP native Rust integration test suite.

# Executable finite evidence; AuthorityEffect: None.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

# Ensure code/ is on sys.path
CODE_DIR = Path(__file__).resolve().parent.parent.parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from native_wdp import find_binary


@pytest.fixture(scope="session")
def rust_dir() -> Path:
    """Return path to code/rust crate directory."""
    return CODE_DIR / "rust"


@pytest.fixture(scope="session")
def obstruction_bin() -> Path:
    """Return path to compiled solve_wdp_obstruction executable."""
    bin_path = find_binary("solve_wdp_obstruction", "WDP_OBSTRUCTION_BIN")
    if bin_path is None or not bin_path.is_file():
        pytest.skip("solve_wdp_obstruction binary not compiled or not found")
    return bin_path


@pytest.fixture(scope="session")
def genesis_bin() -> Path:
    """Return path to compiled solve_genesis_observer executable."""
    bin_path = find_binary("solve_genesis_observer", "WDP_GENESIS_BIN")
    if bin_path is None or not bin_path.is_file():
        pytest.skip("solve_genesis_observer binary not compiled or not found")
    return bin_path
