# -*- coding: utf-8 -*-
"""
Test isolation for apps/coda: every test gets its own persistent anomalon register.

The register is append-only by design (``reset`` deletes nothing), so isolation comes
from pointing ``CODA_ANOMALON_REGISTER`` at a fresh file per test. Subprocesses started
by a test inherit the variable.

AuthorityEffect: None.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Support a checkout replay without installing the relocated application.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest

from coda_application.domain.anomalon_registry import AnomalonRegistry


@pytest.fixture(autouse=True)
def _private_anomalon_register(tmp_path, monkeypatch):
    monkeypatch.setenv("CODA_ANOMALON_REGISTER", str(tmp_path / "anomalon_register.jsonl"))
    AnomalonRegistry.reset()
    yield
    AnomalonRegistry.reset()
