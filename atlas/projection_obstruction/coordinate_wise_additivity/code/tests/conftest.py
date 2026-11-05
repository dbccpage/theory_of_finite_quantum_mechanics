"""Pytest bootstrap: avoid package-root `code/` shadowing the stdlib `code` module.

AuthorityEffect: None.

When pytest runs with CWD = package root, that directory is early on sys.path.
A local folder named `code/` then wins `import code` over the stdlib, and
pytest's pdb hook crashes (InteractiveConsole missing).

This conftest:
1. Removes the package root from sys.path so stdlib `code` is visible.
2. Prefers `*_lib/` (canonical library surface) for imports.
3. Falls back to the `code/` directory as a *module directory* (parent not on path).
"""

from __future__ import annotations

import sys
from pathlib import Path

_PACKAGE_ROOT = Path(__file__).resolve().parents[2]
_ROOT_RESOLVED = _PACKAGE_ROOT.resolve()


def _is_package_root(entry: str) -> bool:
    try:
        return Path(entry).resolve() == _ROOT_RESOLVED
    except OSError:
        return False


# Drop package root so `import code` is the stdlib.
sys.path[:] = [p for p in sys.path if not _is_package_root(p)]

# Prefer the named library package surface.
_lib_candidates = sorted(_PACKAGE_ROOT.glob("*_lib"))
for _lib in _lib_candidates:
    if _lib.is_dir():
        _s = str(_lib.resolve())
        if _s not in sys.path:
            sys.path.insert(0, _s)
        break
else:
    _code_dir = _PACKAGE_ROOT / "code"
    if _code_dir.is_dir():
        _s = str(_code_dir.resolve())
        if _s not in sys.path:
            sys.path.insert(0, _s)
