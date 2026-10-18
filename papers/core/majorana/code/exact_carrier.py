from __future__ import annotations
"""Structural Python mirror for ``omega_engine/crates/omega_homology/src/exact_carrier.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""


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


def matrix_content_hash(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``matrix_content_hash``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/exact_carrier.rs::matrix_content_hash"
    )


CarrierError = Enum(
    "CarrierError",
    {
        "CochainRelationViolated": "CochainRelationViolated",
        "DimensionMismatch": "DimensionMismatch",
        "WeightDimensionMismatch": "WeightDimensionMismatch",
        "NonPositiveWeight": "NonPositiveWeight",
    },
    type=str,
)
CarrierError.__doc__ = "Structural mirror of Rust ``CarrierError`` variants."


@dataclass(init=False)
class Carrier(_RustSurfaceObject):
    """Structural mirror of Rust ``Carrier``."""

    c0_dim: Any = None
    c1_dim: Any = None
    c2_dim: Any = None
    d0: Any = None
    d1: Any = None
    weights: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("c0_dim", "c1_dim", "c2_dim", "d0", "d1", "weights")
        if len(args) > len(names):
            raise TypeError("Carrier received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def new(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``new``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/exact_carrier.rs::new"
    )


def rank_d0(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``rank_d0``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/exact_carrier.rs::rank_d0"
    )


def dim_q1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``dim_q1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/exact_carrier.rs::dim_q1"
    )


def rank_d1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``rank_d1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/exact_carrier.rs::rank_d1"
    )


def dim_h1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``dim_h1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/exact_carrier.rs::dim_h1"
    )


@dataclass(init=False)
class CarrierManifest(_RustSurfaceObject):
    """Structural mirror of Rust ``CarrierManifest``."""

    carrier_hash: Any = None
    d0_hash: Any = None
    d1_hash: Any = None
    c0_dim: Any = None
    c1_dim: Any = None
    c2_dim: Any = None
    rank_d0: Any = None
    dim_q1: Any = None
    dim_h1: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "carrier_hash",
            "d0_hash",
            "d1_hash",
            "c0_dim",
            "c1_dim",
            "c2_dim",
            "rank_d0",
            "dim_q1",
            "dim_h1",
        )
        if len(args) > len(names):
            raise TypeError("CarrierManifest received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def from_carrier(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``from_carrier``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/exact_carrier.rs::from_carrier"
    )


def graph_carrier(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``graph_carrier``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/exact_carrier.rs::graph_carrier"
    )




