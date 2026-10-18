"""Basis identity and dimension descriptors.

This is the Python parity surface for
``omega_linear_algebra/src/basis.rs``. A :class:`BasisDescriptor` is an
audit label for a coordinate representation; it does not prove that a list of
vectors is linearly independent or spanning.
"""

from __future__ import annotations
from dataclasses import dataclass


class BasisError(ValueError):
    """Typed basis-description refusal."""


@dataclass(frozen=True)
class BasisId:
    """Canonical non-empty identifier for a chosen coordinate basis."""

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("basis ID must be a string")
        canonical = self.value.strip()
        if not canonical:
            raise BasisError("basis ID cannot be empty")
        object.__setattr__(self, "value", canonical)

    @classmethod
    def new(cls, value: str) -> "BasisId":
        return cls(value)

    def as_str(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class BasisDescriptor:
    """A chosen basis label together with its intrinsic dimension."""

    basis_id: BasisId
    dimension: int

    def __post_init__(self) -> None:
        if isinstance(self.dimension, bool) or not isinstance(self.dimension, int):
            raise TypeError("basis dimension must be an integer")
        if self.dimension < 0:
            raise BasisError("basis dimension must be non-negative")

    @classmethod
    def new(cls, basis_id: BasisId, dimension: int) -> "BasisDescriptor":
        return cls(basis_id=basis_id, dimension=dimension)

    def id(self) -> BasisId:
        return self.basis_id


__all__ = ["BasisDescriptor", "BasisError", "BasisId"]

from dataclasses import dataclass  
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


def new(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``new``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/basis.rs::new"
    )


def as_str(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``as_str``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/basis.rs::as_str"
    )


def id(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``id``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/basis.rs::id"
    )


def dimension(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``dimension``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/basis.rs::dimension"
    )




