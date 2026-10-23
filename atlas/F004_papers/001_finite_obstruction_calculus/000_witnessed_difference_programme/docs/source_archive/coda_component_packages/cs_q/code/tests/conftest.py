"""Pytest configuration for CODA-CS-Q ensuring package paths are on sys.path."""

import sys
from pathlib import Path

_code_dir = Path(__file__).resolve().parents[1]
for path_entry in [_code_dir, _code_dir.parent]:
    if str(path_entry) not in sys.path:
        sys.path.insert(0, str(path_entry))
