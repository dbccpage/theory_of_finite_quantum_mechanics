"""Pytest configuration for omega_engine/_tests_unit."""

from __future__ import annotations

import pathlib
import sys

# Ensure root workspace is on sys.path
_repo_root = pathlib.Path(__file__).resolve().parents[2]
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))
