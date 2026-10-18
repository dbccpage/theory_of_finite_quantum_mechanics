"""Scalar Phi1 functional backed by the certified L1 LP solver."""

from typing import List, Tuple

import numpy as np

from omega_engine.crates.solver.solv_phi_l1_lp import solve_phi


def raw_l1(delta: List[float]) -> float:
    return sum(abs(v) for v in delta)


def residual_l1(residual: List[float]) -> float:
    return sum(abs(v) for v in residual)


def phi1(n_nodes: int, edges: List[Tuple[int, int]], omega1: List[float]) -> float:
    """LP-solved Phi1 via the underlying ``solve_phi``.

    This is "LP-solved", not independently "certified": the value is certified
    only insofar as ``solve_phi`` verifies primal/dual feasibility and
    tightness. This wrapper itself performs no such verification.
    """
    if n_nodes <= 0:
        raise ValueError("n_nodes must be positive")
    if len(omega1) != len(edges):
        raise ValueError(
            f"omega1 length {len(omega1)} does not match edge count {len(edges)}"
        )
    b = np.zeros((len(edges), n_nodes))
    for i, (u, v) in enumerate(edges):
        if not (0 <= u < n_nodes) or not (0 <= v < n_nodes):
            raise ValueError(
                f"edge {i} endpoint(s) ({u}, {v}) outside node range [0, {n_nodes})"
            )
        b[i, u] = -1.0
        b[i, v] = 1.0
    _, _, cert = solve_phi(b, np.asarray(omega1, dtype=float))
    return cert.phi1


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
class ExactPhi1Certificate(_RustSurfaceObject):
    """Structural mirror of Rust ``ExactPhi1Certificate``."""

    omega: Any = None
    d0: Any = None
    weights: Any = None
    alpha: Any = None
    primal_residual: Any = None
    dual_witness: Any = None
    reported_value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "omega",
            "d0",
            "weights",
            "alpha",
            "primal_residual",
            "dual_witness",
            "reported_value",
        )
        if len(args) > len(names):
            raise TypeError(
                "ExactPhi1Certificate received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class VerifiedExactPhi1(_RustSurfaceObject):
    """Structural mirror of Rust ``VerifiedExactPhi1``."""

    certificate: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("certificate",)
        if len(args) > len(names):
            raise TypeError("VerifiedExactPhi1 received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def value(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``value``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/phi1.rs::value"
    )


def primal_residual(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``primal_residual``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/phi1.rs::primal_residual"
    )


def d0(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``d0``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/phi1.rs::d0"
    )


def alpha(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``alpha``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/phi1.rs::alpha"
    )


def dual_witness(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``dual_witness``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/phi1.rs::dual_witness"
    )


ExactPhi1CertificateError = Enum(
    "ExactPhi1CertificateError",
    {
        "CochainDimensionMismatch": "CochainDimensionMismatch",
        "D0RowMismatch": "D0RowMismatch",
        "D0ColumnMismatch": "D0ColumnMismatch",
        "NonPositiveWeight": "NonPositiveWeight",
        "PrimalResidualMismatch": "PrimalResidualMismatch",
        "DualAnnihilatorMismatch": "DualAnnihilatorMismatch",
        "DualNormBoundViolation": "DualNormBoundViolation",
        "NegativeReportedValue": "NegativeReportedValue",
        "PrimalValueMismatch": "PrimalValueMismatch",
        "DualValueMismatch": "DualValueMismatch",
    },
    type=str,
)
ExactPhi1CertificateError.__doc__ = (
    "Structural mirror of Rust ``ExactPhi1CertificateError`` variants."
)


@dataclass(init=False)
class Phi1Functional(_RustSurfaceObject):
    """Structural mirror of Rust ``Phi1Functional``."""

    certificate: Any = None
    expected: Any = None
    actual: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("certificate", "expected", "actual")
        if len(args) > len(names):
            raise TypeError("Phi1Functional received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def verify_exact_certificate(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``verify_exact_certificate``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/phi1.rs::verify_exact_certificate"
    )






