"""Ensure finite_to_continuum/code/ is on sys.path for pytest and unittest."""

from __future__ import annotations

from pathlib import Path
import sys

CODE_DIR = str(Path(__file__).resolve().parents[1] / "code")
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)
