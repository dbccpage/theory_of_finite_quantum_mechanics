from __future__ import annotations
"""Structural Python mirror for ``omega_engine/crates/omega_homology/src/primitive_decomposition.rs``.

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


PrimitiveStatus = Enum(
    "PrimitiveStatus",
    {
        "Certified": "Certified",
        "NotSeparable": "NotSeparable",
        "PrimitiveUnknown": "PrimitiveUnknown",
    },
    type=str,
)
PrimitiveStatus.__doc__ = "Structural mirror of Rust ``PrimitiveStatus`` variants."



