"""Structural Python mirror for ``omega_engine/crates/omega_state/src/tolerance_profile.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""

from __future__ import annotations
# BEGIN GENERATED RUST SURFACE
# Rust source: omega_engine/crates/omega_state/src/tolerance_profile.rs
# Rust sha256: 5d3c635485afb1e47a60b0ee222b392b2b6b6e7f1699834afd5c37c1d6b9515c
# Structural parity only; no behavioral or authority claim.
from typing import Any


class _RustSurfaceMeta(type):
    def __getattr__(cls, name: str) -> Any:
        def unavailable(*args: Any, **kwargs: Any) -> Any:
            raise NotImplementedError(
                f"Behavioral method {cls.__name__}.{name} is not ported"
            )

        return unavailable


class _RustSurfaceObject(metaclass=_RustSurfaceMeta):
    def __getattr__(self, name: str) -> Any:
        def unavailable(*args: Any, **kwargs: Any) -> Any:
            raise NotImplementedError(
                f"Behavioral method {type(self).__name__}.{name} is not ported"
            )

        return unavailable


# END GENERATED RUST SURFACE
