"""Put the package's ``code/`` and ``demos/code/`` on ``sys.path`` before tests run."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CODE_DIR = str(ROOT / "code")
DEMO_CODE_DIR = str(ROOT / "demos" / "code")

for p in (CODE_DIR, DEMO_CODE_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)
