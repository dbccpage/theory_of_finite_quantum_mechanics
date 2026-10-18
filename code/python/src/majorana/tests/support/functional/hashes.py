"""Structural Python mirror for ``omega_engine/crates/omega_functional/src/hashes.rs``.

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


@dataclass(init=False)
class Hash256(_RustSurfaceObject):
    """Structural mirror of Rust ``Hash256``."""

    value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("value",)
        if len(args) > len(names):
            raise TypeError("Hash256 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def is_zero(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``is_zero``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/hashes.rs::is_zero"
    )


@dataclass(init=False)
class CarrierManifestHash(_RustSurfaceObject):
    """Structural mirror of Rust ``CarrierManifestHash``."""

    value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("value",)
        if len(args) > len(names):
            raise TypeError(
                "CarrierManifestHash received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class ReplayHash(_RustSurfaceObject):
    """Structural mirror of Rust ``ReplayHash``."""

    value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("value",)
        if len(args) > len(names):
            raise TypeError("ReplayHash received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class ObserverMapHash(_RustSurfaceObject):
    """Structural mirror of Rust ``ObserverMapHash``."""

    value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("value",)
        if len(args) > len(names):
            raise TypeError("ObserverMapHash received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class QuotientSpaceHash(_RustSurfaceObject):
    """Structural mirror of Rust ``QuotientSpaceHash``."""

    value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("value",)
        if len(args) > len(names):
            raise TypeError("QuotientSpaceHash received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class ToleranceProfileHash(_RustSurfaceObject):
    """Structural mirror of Rust ``ToleranceProfileHash``."""

    value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("value",)
        if len(args) > len(names):
            raise TypeError(
                "ToleranceProfileHash received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class EquivalenceRelationHash(_RustSurfaceObject):
    """Structural mirror of Rust ``EquivalenceRelationHash``."""

    value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("value",)
        if len(args) > len(names):
            raise TypeError(
                "EquivalenceRelationHash received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class ObserverRef(_RustSurfaceObject):
    """Structural mirror of Rust ``ObserverRef``."""

    value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("value",)
        if len(args) > len(names):
            raise TypeError("ObserverRef received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def is_empty(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``is_empty``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/hashes.rs::is_empty"
    )


@dataclass(init=False)
class CheckerRef(_RustSurfaceObject):
    """Structural mirror of Rust ``CheckerRef``."""

    value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("value",)
        if len(args) > len(names):
            raise TypeError("CheckerRef received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class CertificateRef(_RustSurfaceObject):
    """Structural mirror of Rust ``CertificateRef``."""

    value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("value",)
        if len(args) > len(names):
            raise TypeError("CertificateRef received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class LawId(_RustSurfaceObject):
    """Structural mirror of Rust ``LawId``."""

    value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("value",)
        if len(args) > len(names):
            raise TypeError("LawId received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class EvidenceRef(_RustSurfaceObject):
    """Structural mirror of Rust ``EvidenceRef``."""

    value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("value",)
        if len(args) > len(names):
            raise TypeError("EvidenceRef received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class BoundaryMapsHash(_RustSurfaceObject):
    """Structural mirror of Rust ``BoundaryMapsHash``."""

    value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("value",)
        if len(args) > len(names):
            raise TypeError("BoundaryMapsHash received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class WeightsAndGaugesHash(_RustSurfaceObject):
    """Structural mirror of Rust ``WeightsAndGaugesHash``."""

    value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("value",)
        if len(args) > len(names):
            raise TypeError(
                "WeightsAndGaugesHash received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class DefectFieldHash(_RustSurfaceObject):
    """Structural mirror of Rust ``DefectFieldHash``."""

    value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("value",)
        if len(args) > len(names):
            raise TypeError("DefectFieldHash received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class ObserverBoundaryHash(_RustSurfaceObject):
    """Structural mirror of Rust ``ObserverBoundaryHash``."""

    value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("value",)
        if len(args) > len(names):
            raise TypeError(
                "ObserverBoundaryHash received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class RationalValue(_RustSurfaceObject):
    """Structural mirror of Rust ``RationalValue``."""

    numerator: Any = None
    denominator: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("numerator", "denominator")
        if len(args) > len(names):
            raise TypeError("RationalValue received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def try_new(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``try_new``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/hashes.rs::try_new"
    )


def from_big_rational(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``from_big_rational``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/hashes.rs::from_big_rational"
    )


def as_big_rational(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``as_big_rational``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/hashes.rs::as_big_rational"
    )


CertifiedScalar = Enum(
    "CertifiedScalar",
    {"ExactRational": "ExactRational", "Interval": "Interval"},
    type=str,
)
CertifiedScalar.__doc__ = "Structural mirror of Rust ``CertifiedScalar`` variants."


def to_f64_diagnostic(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``to_f64_diagnostic``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/hashes.rs::to_f64_diagnostic"
    )


def is_exactly_zero(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``is_exactly_zero``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/hashes.rs::is_exactly_zero"
    )


def is_nonnegative_exact_or_interval(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``is_nonnegative_exact_or_interval``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/hashes.rs::is_nonnegative_exact_or_interval"
    )


def try_exact_rational(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``try_exact_rational``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/hashes.rs::try_exact_rational"
    )


def validate_interval(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``validate_interval``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/hashes.rs::validate_interval"
    )




