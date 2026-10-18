"""MUB(6) test suite configuration and path setup."""
from pathlib import Path
import sys

_CODE_DIR = Path(__file__).resolve().parents[1] / "code"
if _CODE_DIR.exists() and str(_CODE_DIR) not in sys.path:
    sys.path.insert(0, str(_CODE_DIR))
