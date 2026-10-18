"""Structural Python mirror for ``omega_engine/crates/omega_state/src/unknown_status.rs``.

The Rust module is the behavioral specification. Generated symbols
fail closed where behavior has not been implemented.
"""

from __future__ import annotations
# BEGIN GENERATED RUST SURFACE
# Rust source: omega_engine/crates/omega_state/src/unknown_status.rs
# Rust sha256: 7866decf7aa2cfe4e9c0fbd86f226e285defe6d1b2c08ac1e3e9ebe1c2201f10
# Structural parity only; no behavioral or authority claim.
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


UnknownStatus = Enum(
    "UnknownStatus",
    {
        "MissingData": "MissingData",
        "SolverInconclusive": "SolverInconclusive",
        "BudgetUnknown": "BudgetUnknown",
        "GrammarInsufficient": "GrammarInsufficient",
        "CandidateLiftFound": "CandidateLiftFound",
        "NeedsExperiment": "NeedsExperiment",
        "NeedsRealizationFunctor": "NeedsRealizationFunctor",
        "Untrusted": "Untrusted",
        "ApproxTrusted": "ApproxTrusted",
        "TrueRefusal": "TrueRefusal",
    },
    type=str,
)
UnknownStatus.__doc__ = "Structural mirror of Rust ``UnknownStatus`` variants."


def is_terminal(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``is_terminal``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/unknown_status.rs::is_terminal"
    )


def is_continuable(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``is_continuable``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_state/src/unknown_status.rs::is_continuable"
    )


# END GENERATED RUST SURFACE
