"""Functional Factory (dumb key registry; explicit registration only).

Doctrine:
- No inference.
- No runtime functional selection.
- No 'best functional' decision logic.
- Explicit registration and lookup only.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Final, Optional, Type

from omega_engine.crates.functional.base.functional_base import FunctionalBase

CONTRACT_ID: Final[str] = "urn:omega:factory:functional:v1.0.0"


@dataclass(frozen=True, slots=True)
class FunctionalKey:
    """Immutable registration key identifying a Functional definition."""
    functional_kind: str
    domain: str
    version: str = "v1.0.0"


class FunctionalFactory:
    """Explicit registry for Functional base classes."""

    _registry: Dict[FunctionalKey, Type[FunctionalBase]] = {}

    @classmethod
    def register(cls, key: FunctionalKey, functional_cls: Type[FunctionalBase]) -> None:
        """Explicitly register a Functional class under a key."""
        if not issubclass(functional_cls, FunctionalBase):
            raise TypeError(f"Registered class must inherit FunctionalBase: {functional_cls}")
        cls._registry[key] = functional_cls

    @classmethod
    def get(cls, key: FunctionalKey) -> Type[FunctionalBase]:
        """Look up a Functional class by key; raises KeyError on unregistered lookup."""
        if key not in cls._registry:
            raise KeyError(f"No Functional registered under key: {key}")
        return cls._registry[key]

    @classmethod
    def clear(cls) -> None:
        """Clear registry for testing."""
        cls._registry.clear()


__all__ = [
    "FunctionalKey",
    "FunctionalFactory",
    "CONTRACT_ID",
]
