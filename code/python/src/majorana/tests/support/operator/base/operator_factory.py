"""Explicit Operator Registry & Factory.

Doctrine:
- Explicit registration only: OperatorKey(op_kind, domain) -> Concrete Operator class.
- NO reflection, NO directory scanning, NO dynamic imports, NO inference.
- Keeps authority boundary strictly fail-closed.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Type

from omega_engine.crates.operator.base.operator_base import OperatorBase


@dataclass(frozen=True, slots=True)
class OperatorKey:
    """Explicit tuple key identifying an Operator implementation by kind and domain."""
    op_kind: str
    domain: str


class OperatorFactory:
    """Registry-based Operator factory with explicit registration."""

    def __init__(self) -> None:
        self._registry: Dict[OperatorKey, Type[OperatorBase]] = {}

    def register(self, key: OperatorKey, operator_cls: Type[OperatorBase]) -> None:
        """Explicitly register an Operator class under an OperatorKey."""
        if not issubclass(operator_cls, OperatorBase):
            raise TypeError(f"Registered class {operator_cls} must inherit from OperatorBase")
        self._registry[key] = operator_cls

    def get(self, key: OperatorKey) -> Type[OperatorBase]:
        """Look up registered Operator class or raise KeyError."""
        if key not in self._registry:
            raise KeyError(
                f"No Operator registered for key ({key.op_kind}, {key.domain})"
            )
        return self._registry[key]

    def create(self, key: OperatorKey, **kwargs: Any) -> OperatorBase:
        """Instantiate registered Operator class."""
        cls = self.get(key)
        return cls(**kwargs)

    def list_keys(self) -> List[OperatorKey]:
        """List all explicitly registered Operator keys."""
        return list(self._registry.keys())


__all__ = [
    "OperatorKey",
    "OperatorFactory",
]
