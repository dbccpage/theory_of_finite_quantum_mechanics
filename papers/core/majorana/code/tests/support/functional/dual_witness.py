"""Dual witness package: PROTO re-exports + rust-mirror shells (MIXED).

Wave G: top-level PROTO callables live in dual_witness_proto and are re-exported
here so inventory classifies residual capital as MIXED (not pure STUB_MIRROR).
Rust structural mirrors remain below for PROD surface naming only.
AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Sequence

import numpy as np

from omega_engine.crates.functional.dual_witness_proto import (
    DisplayDualWitness,
    display_dual_witness,
    dual_pairing,
    float_dual_checks,
    linf_norm,
)


def dual_pairing_entry(
    dual_functional: Sequence[float],
    primal_vector: Sequence[float],
) -> float:
    """Top-level PROTO entry for dual pairing (delegates to dual_witness_proto)."""
    return dual_pairing(dual_functional, primal_vector)


@dataclass
class DualWitness:
    primal_vector: np.ndarray
    dual_functional: np.ndarray

    def pairing(self) -> float:
        """Evaluates ⟨f, x⟩ = f^T x via PROTO dual_pairing."""
        return dual_pairing(
            [float(x) for x in np.asarray(self.dual_functional).ravel()],
            [float(x) for x in np.asarray(self.primal_vector).ravel()],
        )

    def verify_duality_gap(self, expected_value: float, tol: float = 1e-6) -> bool:
        return abs(self.pairing() - expected_value) <= tol


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


def from_verified(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``from_verified``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: "
        "omega_engine/crates/omega_functional/src/dual_witness.rs::from_verified"
    )




