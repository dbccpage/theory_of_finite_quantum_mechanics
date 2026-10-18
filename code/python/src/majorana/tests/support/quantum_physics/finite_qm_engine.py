"""Compatibility alias for omega_engine.crates.finite_qm.use_cases.finite_qm_engine.

AuthorityEffect: None.
"""

import importlib as _importlib
import sys as _sys

if __name__ == "__main__":
    import runpy as _runpy
    _runpy.run_module('omega_engine.crates.finite_qm.use_cases.finite_qm_engine', run_name="__main__")
else:
    _implementation = _importlib.import_module('omega_engine.crates.finite_qm.use_cases.finite_qm_engine')
    _alias_name = __name__
    globals().update(_implementation.__dict__)
    _sys.modules[_alias_name] = _implementation
