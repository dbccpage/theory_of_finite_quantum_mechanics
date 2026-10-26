"""
Pytest configuration for Domain 1 (Physics) tests.
AuthorityEffect: None
"""

import sys
from pathlib import Path

# Insert domain code directory to sys.path so modules in code/ can be imported cleanly
_code_dir = Path(__file__).resolve().parent.parent / "code"
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))
