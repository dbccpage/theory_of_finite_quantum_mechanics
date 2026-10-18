"""Gamma2 closure defect: Gamma2([h]) = ||d1 h||_1.

Pure-Python port of the Rust ``omega_functional::gamma2`` computation. Given a
degree-1 residual cochain ``h in C^1`` and the coboundary operator
``d1 : C^1 -> C^2``, the closure defect measures how far ``h`` is from being
closed (a cocycle). Zero (within tolerance) means the residual is closed and
the Phi1 quotient is well-defined.

References
----------
Rust: ``crates/omega_functional/src/gamma2.rs`` (``Gamma2Functional::try_compute``)
"""

from __future__ import annotations
import math
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple

import numpy as np


class ClosureStatus(Enum):
    CLOSED = "Closed"
    INDETERMINATE = "IndeterminateWithinTolerance"
    OPEN = "Open"


@dataclass
class Gamma2Result:
    value: float  
    coboundary: np.ndarray  
    is_closed: bool  
    closure_status: ClosureStatus  

    def as_dict(self) -> dict:
        return {
            "value": float(self.value),
            "coboundary": [float(x) for x in self.coboundary.tolist()],
            "is_closed": bool(self.is_closed),
            "closure_status": self.closure_status.value,
        }


def gamma2(d1: np.ndarray, h: np.ndarray, tolerance: float = 1e-9) -> Gamma2Result:
    """Compute the closure defect Gamma2([h]) = ||d1 h||_1.

    ``is_closed`` means "accepted-as-closed under ``tolerance``" (value <=
    tolerance), not an exact algebraic cocycle test. ``closure_status``
    preserves the exact/near/open trichotomy: CLOSED (value == 0),
    INDETERMINATE (0 < value <= tolerance), OPEN (value > tolerance).
    """
    d1 = np.asarray(d1, dtype=float)
    h = np.asarray(h, dtype=float)
    if d1.ndim != 2:
        raise ValueError("d1 must be a 2D array (C^1 -> C^2)")
    if h.ndim != 1:
        raise ValueError("h must be a 1D cochain in C^1")
    if not np.all(np.isfinite(d1)):
        raise ValueError("d1 must contain only finite values")
    if not np.all(np.isfinite(h)):
        raise ValueError("h must contain only finite values")
    if not (tolerance >= 0.0):
        raise ValueError("tolerance must be non-negative")
    if d1.shape[1] != h.shape[0]:
        raise ValueError(
            f"dimension mismatch: d1 has {d1.shape[1]} columns but h has {h.shape[0]} entries"
        )

    coboundary = d1 @ h
    value = float(np.sum(np.abs(coboundary)))

    if value == 0.0:
        status = ClosureStatus.CLOSED
    elif value <= tolerance:
        status = ClosureStatus.INDETERMINATE
    else:
        status = ClosureStatus.OPEN

    return Gamma2Result(
        value=value,
        coboundary=coboundary,
        is_closed=value <= tolerance,
        closure_status=status,
    )


def verify_exactness(
    d1: np.ndarray, d0: np.ndarray, tolerance: float = 1e-9
) -> Tuple[bool, float]:
    """Check the chain-complex condition d1 . d0 = 0.

    Returns ``(holds, max_abs_defect)``. ``d0 : C^0 -> C^1`` (shape E x V),
    ``d1 : C^1 -> C^2`` (shape F x E).
    """
    if not math.isfinite(tolerance) or tolerance < 0.0:
        raise ValueError("tolerance must be finite and non-negative")
    d1 = np.asarray(d1, dtype=float)
    d0 = np.asarray(d0, dtype=float)
    if not np.all(np.isfinite(d1)):
        raise ValueError("d1 contains non-finite values")
    if not np.all(np.isfinite(d0)):
        raise ValueError("d0 contains non-finite values")
    if d1.ndim != 2:
        raise ValueError("d1 must be a 2D array (C^1 -> C^2)")
    if d0.ndim != 2:
        raise ValueError("d0 must be a 2D array (C^0 -> C^1)")
    if d1.shape[1] != d0.shape[0]:
        raise ValueError(
            f"composition mismatch: d1 expects {d1.shape[1]} edges, d0 produces {d0.shape[0]}"
        )
    composite = d1 @ d0
    max_defect = float(np.max(np.abs(composite))) if composite.size else 0.0
    return max_defect <= tolerance, max_defect


def cycle_coboundary(num_edges: int, cycles: List[List[Tuple[int, int]]]) -> np.ndarray:
    """Build d1 : C^1 -> C^2 from a list of oriented cycles (faces).

    Each cycle is a list of ``(edge_index, orientation)`` pairs with
    ``orientation in {+1, -1}``. The resulting matrix has one row per cycle.
    When the cycles are genuine cycles of the graph whose incidence matrix is
    ``d0``, the exactness condition ``d1 . d0 = 0`` holds automatically.
    """
    if num_edges < 0:
        raise ValueError("num_edges must be non-negative")
    d1 = np.zeros((len(cycles), num_edges))
    for face, cycle in enumerate(cycles):
        for edge_index, orientation in cycle:
            if not (0 <= edge_index < num_edges):
                raise ValueError(
                    f"edge index {edge_index} out of range [0, {num_edges})"
                )
            if orientation not in (1, -1):
                raise ValueError(f"orientation {orientation} must be +1 or -1")
            d1[face, edge_index] += float(orientation)
    return d1


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
class ExactCochainComplexQ(_RustSurfaceObject):
    """Structural mirror of Rust ``ExactCochainComplexQ``."""

    c0_dim: Any = None
    c1_dim: Any = None
    c2_dim: Any = None
    d0: Any = None
    d1: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("c0_dim", "c1_dim", "c2_dim", "d0", "d1")
        if len(args) > len(names):
            raise TypeError(
                "ExactCochainComplexQ received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class UntrustedCochainComplexWire(_RustSurfaceObject):
    """Structural mirror of Rust ``UntrustedCochainComplexWire``."""

    c0_dim: Any = None
    c1_dim: Any = None
    c2_dim: Any = None
    d0: Any = None
    d1: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("c0_dim", "c1_dim", "c2_dim", "d0", "d1")
        if len(args) > len(names):
            raise TypeError(
                "UntrustedCochainComplexWire received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def c0_dim(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``c0_dim``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/gamma2.rs::c0_dim"
    )


def c1_dim(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``c1_dim``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/gamma2.rs::c1_dim"
    )


def c2_dim(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``c2_dim``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/gamma2.rs::c2_dim"
    )


def d0(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``d0``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/gamma2.rs::d0"
    )


def d1(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``d1``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/gamma2.rs::d1"
    )


Complex2InputQ = Enum(
    "Complex2InputQ", {"Missing": "Missing", "Declared": "Declared"}, type=str
)
Complex2InputQ.__doc__ = "Structural mirror of Rust ``Complex2InputQ`` variants."


def try_new_with_complex2(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``try_new_with_complex2``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/gamma2.rs::try_new_with_complex2"
    )


def try_new(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``try_new``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/gamma2.rs::try_new"
    )


@dataclass(init=False)
class DegreeOneResidualQ(_RustSurfaceObject):
    """Structural mirror of Rust ``DegreeOneResidualQ``."""

    complex: Any = None
    h: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("complex", "h")
        if len(args) > len(names):
            raise TypeError("DegreeOneResidualQ received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def complex(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``complex``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/gamma2.rs::complex"
    )


def h(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``h``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/gamma2.rs::h"
    )


@dataclass(init=False)
class RawClosureDefectResult(_RustSurfaceObject):
    """Structural mirror of Rust ``RawClosureDefectResult``."""

    residual: Any = None
    d1: Any = None
    coboundary: Any = None
    value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("residual", "d1", "coboundary", "value")
        if len(args) > len(names):
            raise TypeError(
                "RawClosureDefectResult received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def residual(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``residual``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/gamma2.rs::residual"
    )


def coboundary(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``coboundary``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/gamma2.rs::coboundary"
    )


def value(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``value``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/gamma2.rs::value"
    )


@dataclass(init=False)
class ExactGamma2Result(_RustSurfaceObject):
    """Structural mirror of Rust ``ExactGamma2Result``."""

    residual: Any = None
    d0: Any = None
    coboundary: Any = None
    value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("residual", "d0", "coboundary", "value")
        if len(args) > len(names):
            raise TypeError("ExactGamma2Result received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


ExactGamma2Error = Enum(
    "ExactGamma2Error",
    {
        "MissingComplex2": "MissingComplex2",
        "D0RowMismatch": "D0RowMismatch",
        "D0ColumnMismatch": "D0ColumnMismatch",
        "D1ColumnMismatch": "D1ColumnMismatch",
        "CochainIdentityViolation": "CochainIdentityViolation",
        "D1RowMismatch": "D1RowMismatch",
        "ResidualLengthMismatch": "ResidualLengthMismatch",
    },
    type=str,
)
ExactGamma2Error.__doc__ = "Structural mirror of Rust ``ExactGamma2Error`` variants."


@dataclass(init=False)
class Gamma2Artifact(_RustSurfaceObject):
    """Structural mirror of Rust ``Gamma2Artifact``."""

    value: Any = None
    coboundary_hash: Any = None
    residual_hash: Any = None
    d1_hash: Any = None
    c2_basis_hash: Any = None
    c2_norm_profile_hash: Any = None
    carrier_hash: Any = None
    exactness_artifact_hash: Any = None
    tolerance_profile_hash: Any = None
    replay_hash: Any = None
    closure_status: Any = None
    quotient_interpretation: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "value",
            "coboundary_hash",
            "residual_hash",
            "d1_hash",
            "c2_basis_hash",
            "c2_norm_profile_hash",
            "carrier_hash",
            "exactness_artifact_hash",
            "tolerance_profile_hash",
            "replay_hash",
            "closure_status",
            "quotient_interpretation",
        )
        if len(args) > len(names):
            raise TypeError("Gamma2Artifact received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class Gamma2Functional(_RustSurfaceObject):
    """Structural mirror of Rust ``Gamma2Functional``."""

    residual: Any = None
    d1: Any = None
    expected: Any = None
    actual: Any = None
    d0: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("residual", "d1", "expected", "actual", "d0")
        if len(args) > len(names):
            raise TypeError("Gamma2Functional received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def try_compute_raw(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``try_compute_raw``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/gamma2.rs::try_compute_raw"
    )


def try_compute_exact_quotient(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``try_compute_exact_quotient``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/gamma2.rs::try_compute_exact_quotient"
    )




