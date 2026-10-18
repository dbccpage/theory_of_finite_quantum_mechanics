"""FSP test suite configuration and path setup."""
from pathlib import Path
import sys

_REPO_ROOT = next((p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").is_file()), Path(__file__).resolve().parents[3])
_SRC_FSP = _REPO_ROOT / "code" / "python" / "src" / "fsp"
_SRC_FSP_SQL = _SRC_FSP / "sign_sql"
_SRC = _REPO_ROOT / "code" / "python" / "src"
_ROOT_PY = _REPO_ROOT / "code" / "python"

for p in (_SRC_FSP, _SRC_FSP_SQL, _SRC, _ROOT_PY):
    if p.exists() and str(p) not in sys.path:
        sys.path.insert(0, str(p))
