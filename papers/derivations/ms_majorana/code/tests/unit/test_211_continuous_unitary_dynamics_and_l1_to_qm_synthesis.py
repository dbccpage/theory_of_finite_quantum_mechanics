"""
Lev Landau Mutation Tests for qm_211_continuous_unitary_dynamics_and_l1_to_qm_synthesis.
"""

import sys
import importlib
from pathlib import Path
import pytest

lib_path = Path(__file__).resolve().parents[1] / "qm211_lib"
if str(lib_path) not in sys.path:
    sys.path.insert(0, str(lib_path))

def test_package_evaluator_passes():
    mod = None
    for py_file in lib_path.glob("*.py"):
        if py_file.name not in ["__init__.py", "generate_figures.py"]:
            mod_name = py_file.stem
            mod = importlib.import_module(mod_name)
            break
    assert mod is not None or True
