"""Pytest fixtures for E2E Verification Suite.

AuthorityEffect: None.
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

import pytest

from .config import (
    ALL_PACKAGES,
    ESTATE_ROOT,
    PO000_DIR,
    SIBLING_PACKAGES,
    WORKSPACE_ROOT,
    PackageSpec,
)


@pytest.fixture(scope="session")
def workspace_root() -> Path:
    return WORKSPACE_ROOT


@pytest.fixture(scope="session")
def estate_root() -> Path:
    return ESTATE_ROOT


@pytest.fixture(scope="session")
def po000_dir() -> Path:
    return PO000_DIR


@pytest.fixture(scope="session")
def all_package_specs() -> dict[str, PackageSpec]:
    return ALL_PACKAGES


@pytest.fixture(scope="session")
def sibling_package_specs() -> dict[str, PackageSpec]:
    return SIBLING_PACKAGES


@pytest.fixture
def isolated_temp_dir():
    temp_dir = Path(tempfile.mkdtemp(prefix="e2e_po000_"))
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
