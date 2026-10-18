"""Xi package: PROTO formula-mirror re-exports + rust-mirror shells (MIXED).

Wave F: top-level PROTO callables live in xi_proto and are re-exported here so
the inventory classifies residual capital as MIXED (not pure STUB_MIRROR).
Rust structural mirrors remain below for PROD surface naming only.
AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from omega_engine.crates.functional.xi_proto import (
    DensityLiftProto,
    XiComputation,
    compute,
    compute_density_lift,
    pure_state_trace_distance,
    residual_l1_mass,
    xi,
)


def evaluate_xi(
    primal_residual: Sequence[float],
    dual_witness: Sequence[float],
    phi1_value: float,
    *,
    tolerance: float = 1e-12,
    half_normalized: bool = True,
) -> float:
    """Top-level PROTO entry for Ξ (delegates to xi_proto.xi / typed compute)."""
    return xi(
        primal_residual,
        dual_witness,
        phi1_value,
        tolerance=tolerance,
        half_normalized=half_normalized,
    )


@dataclass
class XiOperator:
    """Legacy playpen operator; matrix form is not the PROD density-lift Ξ."""

    matrix: np.ndarray

    def evaluate_xi(self, v: np.ndarray) -> float:
        res = np.dot(self.matrix, v)
        return float(np.linalg.norm(res))


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
class DensityLift(_RustSurfaceObject):
    """Structural mirror of Rust ``DensityLift``."""

    density_matrix: Any = None
    state_vector: Any = None
    total_mass: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("density_matrix", "state_vector", "total_mass")
        if len(args) > len(names):
            raise TypeError("DensityLift received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


XiValidity = Enum(
    "XiValidity",
    {
        "Valid": "Valid",
        "SaturationFailed": "SaturationFailed",
        "DensityLiftUndefined": "DensityLiftUndefined",
        "NonFiniteInput": "NonFiniteInput",
        "FirewallNotChecked": "FirewallNotChecked",
    },
    type=str,
)
XiValidity.__doc__ = "Structural mirror of Rust ``XiValidity`` variants."


@dataclass(init=False)
class XiResult(_RustSurfaceObject):
    """Structural mirror of Rust ``XiResult``."""

    value: Any = None
    validity: Any = None
    primal_density: Any = None
    dual_density: Any = None
    saturation_verified: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "value",
            "validity",
            "primal_density",
            "dual_density",
            "saturation_verified",
        )
        if len(args) > len(names):
            raise TypeError("XiResult received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


XiComputation = Enum(
    "XiComputation",
    {
        "ExactZero": "ExactZero",
        "ValidTieBreaker": "ValidTieBreaker",
        "Invalid": "Invalid",
    },
    type=str,
)
XiComputation.__doc__ = "Structural mirror of Rust ``XiComputation`` variants."


XiError = Enum(
    "XiError", {"NonFiniteInput": "NonFiniteInput", "ZeroMass": "ZeroMass"}, type=str
)
XiError.__doc__ = "Structural mirror of Rust ``XiError`` variants."


@dataclass(init=False)
class XiFunctional(_RustSurfaceObject):
    """Structural mirror of Rust ``XiFunctional``."""

    vector: Any = None
    tolerance: Any = None
    psi: Any = None
    phi: Any = None
    half_normalized: Any = None
    primal_residual: Any = None
    dual_witness: Any = None
    phi1_value: Any = None
    XiComputation: Any = None
    validity: Any = None
    primal_density: Any = None
    dual_density: Any = None
    phi1_before: Any = None
    phi1_after: Any = None
    gamma2_before: Any = None
    gamma2_after: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "vector",
            "tolerance",
            "psi",
            "phi",
            "half_normalized",
            "primal_residual",
            "dual_witness",
            "phi1_value",
            "XiComputation",
            "validity",
            "primal_density",
            "dual_density",
            "phi1_before",
            "phi1_after",
            "gamma2_before",
            "gamma2_after",
        )
        if len(args) > len(names):
            raise TypeError("XiFunctional received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def compute_density_lift(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``compute_density_lift``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/xi.rs::compute_density_lift"
    )


def pure_state_trace_distance(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``pure_state_trace_distance``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/xi.rs::pure_state_trace_distance"
    )


def compute(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``compute``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/xi.rs::compute"
    )


def firewall_allows_candidate(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``firewall_allows_candidate``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/xi.rs::firewall_allows_candidate"
    )


def xi_may_decide_tie(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``xi_may_decide_tie``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/xi.rs::xi_may_decide_tie"
    )






