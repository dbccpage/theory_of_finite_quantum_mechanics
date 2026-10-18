"""Base Functional crate exposing FunctionalBase, FunctionalFactory, and DTOs."""

from omega_engine.crates.functional.base.functional_base import (
    FunctionalBase,
    FunctionalIdentity,
    FunctionalConfig,
    FunctionalOutput,
)
from omega_engine.crates.functional.base.functional_factory import (
    FunctionalKey,
    FunctionalFactory,
)

__all__ = [
    "FunctionalBase",
    "FunctionalIdentity",
    "FunctionalConfig",
    "FunctionalOutput",
    "FunctionalKey",
    "FunctionalFactory",
]
