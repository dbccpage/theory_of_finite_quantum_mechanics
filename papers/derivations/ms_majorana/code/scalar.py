from __future__ import annotations
"""Exact rational scalar (faithful to Rust ``omega_homology::scalar::Q`` = Rational64)."""


from fractions import Fraction
from typing import Union

Q = Fraction


def q(value: Union[int, float, str, Fraction]) -> Fraction:
    """Construct an exact rational, mirroring Rust ``q(n)``."""
    return Fraction(value)


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


def qr(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``qr``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/scalar.rs::qr"
    )


def hash_rational(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``hash_rational``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/scalar.rs::hash_rational"
    )


def hash_rational_vec(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``hash_rational_vec``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/scalar.rs::hash_rational_vec"
    )



