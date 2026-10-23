"""Pytest fixtures for Python tests under code/tests/python/.

# Executable finite evidence; AuthorityEffect: None.
"""

from __future__ import annotations

import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent.parent.parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))
