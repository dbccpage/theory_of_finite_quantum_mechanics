"""Pytest configuration for WDP paper code tests.

# Executable finite evidence; AuthorityEffect: None.
"""

import sys
from pathlib import Path

# Ensure code/ is on sys.path
CODE_DIR = Path(__file__).resolve().parent.parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))
