"""Structural Python mirror for ``omega_engine/crates/omega_linear_algebra/src/linear_algebra/support_operations.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""

from __future__ import annotations
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


SupportOperationError = Enum(
    "SupportOperationError",
    {
        "DimensionMismatch": "DimensionMismatch",
        "InvalidThreshold": "InvalidThreshold",
        "NonFiniteEntry": "NonFiniteEntry",
        "SupportOverlap": "SupportOverlap",
        "IndexOutOfBounds": "IndexOutOfBounds",
    },
    type=str,
)
SupportOperationError.__doc__ = (
    "Structural mirror of Rust ``SupportOperationError`` variants."
)


def disjoint_support_checked(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``disjoint_support_checked``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/linear_algebra/support_operations.rs::disjoint_support_checked"
    )


def merge_disjoint_checked(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``merge_disjoint_checked``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/linear_algebra/support_operations.rs::merge_disjoint_checked"
    )


def split_by_indices(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``split_by_indices``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/linear_algebra/support_operations.rs::split_by_indices"
    )


def project_to_support_checked(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``project_to_support_checked``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/linear_algebra/support_operations.rs::project_to_support_checked"
    )



