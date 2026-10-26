# -*- coding: utf-8 -*-
"""
conftest.py: Ensures the local code/ directory is always prioritized in sys.path
for hermetic test execution without requiring ambient PYTHONPATH environment variables.
"""

import sys
from pathlib import Path

_CODE_DIR = str(Path(__file__).resolve().parents[1])
if _CODE_DIR not in sys.path:
    sys.path.insert(0, _CODE_DIR)
