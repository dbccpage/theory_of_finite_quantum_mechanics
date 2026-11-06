"""
Pytest configuration for Domain 2 (Pure Mathematics) tests.
AuthorityEffect: None
"""

import sys
from pathlib import Path

# Insert domain code directory to sys.path
_code_dir = Path(__file__).resolve().parent.parent / "code"
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))
