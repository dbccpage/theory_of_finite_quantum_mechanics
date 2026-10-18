"""Structural Python mirror for ``omega_engine/crates/omega_linear_algebra/src/scalars.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""

from __future__ import annotations
from typing import Any, Protocol


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


class Semiring(Protocol):
    """Structural protocol for Rust trait ``Semiring``."""

    pass


class Ring(Protocol):
    """Structural protocol for Rust trait ``Ring``."""

    pass


class Field(Protocol):
    """Structural protocol for Rust trait ``Field``."""

    pass


class ExactRing(Protocol):
    """Structural protocol for Rust trait ``ExactRing``."""

    pass


class AnalyticRing(Protocol):
    """Structural protocol for Rust trait ``AnalyticRing``."""

    pass



