"""MUB(6) test suite configuration and path setup."""
from pathlib import Path
import sys

_REPO_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").is_file()), Path(__file__).resolve().parents[3])
_SRC_MUB = _REPO_ROOT / "code" / "python" / "src" / "mub"
_SRC = _REPO_ROOT / "code" / "python" / "src"
for p in (_SRC_MUB, _SRC):
    if p.exists() and str(p) not in sys.path:
        sys.path.insert(0, str(p))
