"""Public export launcher for Paper Package 002 Jupyter Notebook suite (Levels 1-5).
AuthorityEffect: None.
"""
import sys
from pathlib import Path

pkg_root = Path(__file__).resolve().parent.parent
code_dir = pkg_root / "code"
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from run_notebook import main

if __name__ == "__main__":
    main()
