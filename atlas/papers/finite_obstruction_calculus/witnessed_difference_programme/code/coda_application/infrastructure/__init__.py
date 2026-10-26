# -*- coding: utf-8 -*-
"""
Infrastructure layer for the CODA application.
Contains bridges to Rust crates in omega_engine/crates_rs and exact rational solver adapters.

AuthorityEffect: None.
"""

from coda_application.infrastructure.exact_solver_adapter import ExactSolverAdapter
from coda_application.infrastructure.rust_bridge import RustCrateBridge

__all__ = [
    "ExactSolverAdapter",
    "RustCrateBridge",
]
