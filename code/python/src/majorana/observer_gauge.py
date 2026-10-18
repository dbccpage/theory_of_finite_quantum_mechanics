from __future__ import annotations
"""Structural Python mirror for ``omega_engine/crates/omega_homology/src/observer_gauge.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""


from dataclasses import dataclass
from enum import Enum
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


GaugeError = Enum(
    "GaugeError",
    {"DimensionMismatch": "DimensionMismatch", "InvalidWeight": "InvalidWeight"},
    type=str,
)
GaugeError.__doc__ = "Structural mirror of Rust ``GaugeError`` variants."


class ObserverGauge(Protocol):
    """Structural protocol for Rust trait ``ObserverGauge``."""

    pass


@dataclass(init=False)
class ScalarGauge(_RustSurfaceObject):
    """Structural mirror of Rust ``ScalarGauge``."""

    weights: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("weights",)
        if len(args) > len(names):
            raise TypeError("ScalarGauge received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def new(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``new``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/observer_gauge.rs::new"
    )


@dataclass(init=False)
class VectorGauge(_RustSurfaceObject):
    """Structural mirror of Rust ``VectorGauge``."""

    weights: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("weights",)
        if len(args) > len(names):
            raise TypeError("VectorGauge received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class TraceGauge(_RustSurfaceObject):
    """Structural mirror of Rust ``TraceGauge``."""

    weights: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("weights",)
        if len(args) > len(names):
            raise TypeError("TraceGauge received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)




