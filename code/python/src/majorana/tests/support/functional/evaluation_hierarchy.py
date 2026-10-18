"""Structural Python mirror for ``omega_engine/crates/omega_functional/src/evaluation_hierarchy.rs``.

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


DiagnosticComparison = Enum(
    "DiagnosticComparison",
    {
        "StrictlyImproves": "StrictlyImproves",
        "Preserves": "Preserves",
        "NonWorse": "NonWorse",
        "Worsens": "Worsens",
        "Incomparable": "Incomparable",
        "Invalid": "Invalid",
    },
    type=str,
)
DiagnosticComparison.__doc__ = (
    "Structural mirror of Rust ``DiagnosticComparison`` variants."
)


fn: Any = None


def guarded_strictly_improves(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``guarded_strictly_improves``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/evaluation_hierarchy.rs::guarded_strictly_improves"
    )


def guarded_non_worse(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``guarded_non_worse``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/evaluation_hierarchy.rs::guarded_non_worse"
    )


def classify_guarded_non_worse(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``classify_guarded_non_worse``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/evaluation_hierarchy.rs::classify_guarded_non_worse"
    )


def compare_guarded_diagnostics(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``compare_guarded_diagnostics``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/evaluation_hierarchy.rs::compare_guarded_diagnostics"
    )



