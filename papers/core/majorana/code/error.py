from __future__ import annotations
"""Structural Python mirror for ``omega_engine/crates/omega_homology/src/error.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""


from enum import Enum
from typing import Any


class _RustSurfaceMeta(type):
    def __getattr__(cls, name: str) -> Any:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)

        def unavailable(*args: Any, **kwargs: Any) -> Any:
            raise NotImplementedError(
                f"Behavioral method {cls.__name__}.{name} is not ported"
            )

        return unavailable


class _RustSurfaceObject(metaclass=_RustSurfaceMeta):
    def __getattr__(self, name: str) -> Any:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)

        def unavailable(*args: Any, **kwargs: Any) -> Any:
            raise NotImplementedError(
                f"Behavioral method {type(self).__name__}.{name} is not ported"
            )

        return unavailable


HomologyError = Enum(
    "HomologyError",
    {
        "DimensionMismatch": "DimensionMismatch",
        "BoundarySquaredNonzero": "BoundarySquaredNonzero",
        "VerificationUnavailable": "VerificationUnavailable",
        "NotACycle": "NotACycle",
        "NotACocycle": "NotACocycle",
        "NotABoundary": "NotABoundary",
        "ComplexMismatch": "ComplexMismatch",
        "NotAChainMap": "NotAChainMap",
        "NotAChainHomotopy": "NotAChainHomotopy",
        "DomainMismatch": "DomainMismatch",
        "UnsupportedStructure": "UnsupportedStructure",
    },
    type=str,
)
HomologyError.__doc__ = "Structural mirror of Rust ``HomologyError`` variants."



