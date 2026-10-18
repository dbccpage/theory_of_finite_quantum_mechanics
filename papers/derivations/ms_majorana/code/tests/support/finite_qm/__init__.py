"""Central finite-QM domain, calculations, and application entrypoints.

AuthorityEffect: None.
"""

import warnings

warnings.warn(
    "omega_engine_projects.ms_majorana.code.tests.support.finite_qm is deprecated, use workspace Rust crates / PyO3 extensions",
    DeprecationWarning,
    stacklevel=2,
)

from importlib import import_module as _import_module

__all__ = ['domain', 'entrypoints', 'use_cases']

def __getattr__(name):
    if name not in __all__:
        raise AttributeError(name)
    value = _import_module(f"{__name__}.{name}")
    globals()[name] = value
    return value

def __dir__():
    return sorted(set(globals()) | set(__all__))
