"""Pytest bootstrap for the GR-002 paper-local suite.

`code/` is a flat module directory: solvers, DDA modules, and diagnostics all
sit directly under it and import each other by bare module name. Putting that
one directory on `sys.path` here replaces the per-file `sys.path` surgery the
suite used to carry when the modules lived in `solvers/`, `dda/`, and
`diagnostics/` subpackages.

AuthorityEffect: None.
"""

from __future__ import annotations

import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = CODE_DIR.parent
REPO_ROOT = CODE_DIR.parents[4]

for path in (CODE_DIR, PACKAGE_ROOT, REPO_ROOT):
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))
