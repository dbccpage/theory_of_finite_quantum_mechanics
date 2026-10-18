"""Structural Python mirror for ``omega_engine/crates/omega_linear_algebra/src/choice.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""

from __future__ import annotations
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


class Choice(Protocol):
    """Structural protocol for Rust trait ``Choice``."""

    pass


@dataclass(init=False)
class WithChoice(_RustSurfaceObject):
    """Structural mirror of Rust ``WithChoice``."""

    value: Any = None
    choice: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("value", "choice")
        if len(args) > len(names):
            raise TypeError("WithChoice received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def new(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``new``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/choice.rs::new"
    )


def inner(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``inner``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/choice.rs::inner"
    )


def choice(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``choice``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/choice.rs::choice"
    )


def forget(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``forget``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/choice.rs::forget"
    )


BasisChoiceError = Enum("BasisChoiceError", {"Basis": "Basis"}, type=str)
BasisChoiceError.__doc__ = "Structural mirror of Rust ``BasisChoiceError`` variants."


@dataclass(init=False)
class BasisChoice(_RustSurfaceObject):
    """Structural mirror of Rust ``BasisChoice``."""

    descriptor: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("descriptor",)
        if len(args) > len(names):
            raise TypeError("BasisChoice received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def descriptor(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``descriptor``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/choice.rs::descriptor"
    )


def into_descriptor(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``into_descriptor``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/choice.rs::into_descriptor"
    )


class WithChosenBasis(Protocol):
    """Structural protocol for Rust trait ``WithChosenBasis``."""

    pass


class ChangeBasisExt(Protocol):
    """Structural protocol for Rust trait ``ChangeBasisExt``."""

    pass




