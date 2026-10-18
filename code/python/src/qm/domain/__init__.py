"""Finite-QM pure domain model.

Clean Architecture: The domain layer contains enterprise business logic and value objects
with strictly zero inward dependencies on use cases.

AuthorityEffect: None.
"""

from importlib import import_module as _import_module
from typing import TYPE_CHECKING

__all__ = [
    'cyclotomic_tower',
    'gaussian_rational',
    'primitive_difference',
    'primitives',
    'CyclotomicTower',
    'CyclotomicElement',
    'Gaussian',
    'PrimitiveDifference',
]

if TYPE_CHECKING:
    from .cyclotomic_tower import CyclotomicElement, CyclotomicTower
    from .gaussian_rational import Gaussian
    from .primitive_difference import PrimitiveDifference


def __getattr__(name: str):
    if name in ('CyclotomicTower', 'CyclotomicElement'):
        mod = _import_module(f"{__name__}.cyclotomic_tower")
        val = getattr(mod, name)
        globals()[name] = val
        return val
    if name == 'Gaussian':
        mod = _import_module(f"{__name__}.gaussian_rational")
        val = getattr(mod, name)
        globals()[name] = val
        return val
    if name == 'PrimitiveDifference':
        mod = _import_module(f"{__name__}.primitive_difference")
        val = getattr(mod, name)
        globals()[name] = val
        return val
    if name in ('cyclotomic_tower', 'gaussian_rational', 'primitive_difference', 'primitives'):
        val = _import_module(f"{__name__}.{name}")
        globals()[name] = val
        return val
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(set(globals()) | set(__all__))
