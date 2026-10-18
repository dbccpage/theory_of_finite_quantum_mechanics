"""Structural Python mirror for ``omega_engine/crates/omega_linear_algebra/src/linear_algebra/sparse_operator.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""

from __future__ import annotations
from dataclasses import dataclass
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


SparseOperatorError = Enum(
    "SparseOperatorError",
    {
        "EntryOutOfBounds": "EntryOutOfBounds",
        "VectorDimensionMismatch": "VectorDimensionMismatch",
        "Overflow": "Overflow",
    },
    type=str,
)
SparseOperatorError.__doc__ = (
    "Structural mirror of Rust ``SparseOperatorError`` variants."
)


@dataclass(init=False)
class SparseOperator(_RustSurfaceObject):
    """Structural mirror of Rust ``SparseOperator``."""

    rows: Any = None
    cols: Any = None
    entries: Any = None
    compress_witness: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("rows", "cols", "entries", "compress_witness")
        if len(args) > len(names):
            raise TypeError("SparseOperator received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class CompressWitness(_RustSurfaceObject):
    """Structural mirror of Rust ``CompressWitness``."""

    entries: Any = None
    compress_witness: Any = None
    rows: Any = None
    cols: Any = None
    row: Any = None
    col: Any = None
    value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("entries", "compress_witness", "rows", "cols", "row", "col", "value")
        if len(args) > len(names):
            raise TypeError("CompressWitness received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def new(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``new``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/linear_algebra/sparse_operator.rs::new"
    )


def from_entries_checked(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``from_entries_checked``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/linear_algebra/sparse_operator.rs::from_entries_checked"
    )


def shape(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``shape``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/linear_algebra/sparse_operator.rs::shape"
    )


def rows(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``rows``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/linear_algebra/sparse_operator.rs::rows"
    )


def cols(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``cols``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/linear_algebra/sparse_operator.rs::cols"
    )


def entries(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``entries``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/linear_algebra/sparse_operator.rs::entries"
    )


def into_entries(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``into_entries``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/linear_algebra/sparse_operator.rs::into_entries"
    )


def add_entry(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``add_entry``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/linear_algebra/sparse_operator.rs::add_entry"
    )


def apply(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``apply``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/linear_algebra/sparse_operator.rs::apply"
    )


def compress_checked(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``compress_checked``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/linear_algebra/sparse_operator.rs::compress_checked"
    )


def compress_witness(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``compress_witness``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/linear_algebra/sparse_operator.rs::compress_witness"
    )


def is_compressed(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``is_compressed``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_linear_algebra/src/linear_algebra/sparse_operator.rs::is_compressed"
    )




