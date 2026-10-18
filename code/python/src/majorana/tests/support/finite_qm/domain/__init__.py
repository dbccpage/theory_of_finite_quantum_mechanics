"""Finite-QM domain.

AuthorityEffect: None.
"""

from importlib import import_module as _import_module

__all__ = ['cyclotomic_tower', 'gaussian_rational', 'primitive_difference', 'primitives']

def __getattr__(name):
    if name not in __all__:
        raise AttributeError(name)
    value = _import_module(f"{__name__}.{name}")
    globals()[name] = value
    return value

def __dir__():
    return sorted(set(globals()) | set(__all__))
