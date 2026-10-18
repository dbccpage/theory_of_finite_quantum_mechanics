"""MUB(6) test suite configuration and path setup."""
from pathlib import Path
import sys

_PY_DIR = Path(__file__).resolve().parents[1]
if _PY_DIR.exists() and str(_PY_DIR) not in sys.path:
    sys.path.insert(0, str(_PY_DIR))
