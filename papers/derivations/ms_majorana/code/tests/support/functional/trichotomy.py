from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional, Sequence

import numpy as np

from omega_engine.crates.homology_theory.cohomology_h1 import CohomologyH1
from omega_engine.crates.homology_theory.qmatrix import QMatrix
from omega_engine.crates.solver.solv_phi_l1_lp import solve_phi


def _build_cohomology(d0, d1) -> CohomologyH1:
    d0_rows = list(d0)
    E = len(d0_rows)
    V = len(d0_rows[0]) if E else 0
    if d1 is None or (not isinstance(d1, QMatrix) and len(list(d1)) == 0):
        return CohomologyH1(d0, [], num_edges=E, num_vertices=V, num_faces=0)
    return CohomologyH1.from_dims(d0, d1)


class Trichotomy(Enum):
    EXACT = "Exact"
    SURVIVOR = "Survivor"
    OPEN = "Open"


@dataclass(frozen=True)
class TrichotomyResult:
    label: Trichotomy
    closed: bool  
    gamma2_zero: bool  
    gamma2_value: float  
    phi1_estimate: float  
    phi1_certified: bool  
    phi1_is_zero: bool  
    phi1_tol: float  
    exact_membership: Optional[bool]  
    exact_test_agrees: bool  
    is_auth: bool = False

    def as_dict(self) -> dict:
        return {
            "label": self.label.value,
            "closed": self.closed,
            "gamma2_zero": self.gamma2_zero,
            "gamma2_value": float(self.gamma2_value),
            "phi1_estimate": float(self.phi1_estimate),
            "phi1_certified": self.phi1_certified,
            "phi1_is_zero": self.phi1_is_zero,
            "phi1_tol": self.phi1_tol,
            "exact_membership": self.exact_membership,
            "exact_test_agrees": self.exact_test_agrees,
            "is_auth": False,
            "diagnostic_only": True,
        }


def classify(
    d0,
    d1,
    x: Sequence[float],
    phi1_tol: float = 1e-7,
    weights: Optional[np.ndarray] = None,
) -> TrichotomyResult:
    """Classify cochain ``x`` into EXACT / SURVIVOR / OPEN.

    Parameters
    ----------
    d0 : (E, V) coboundary C^0 -> C^1 (the graph incidence matrix B).
    d1 : (F, E) coboundary C^1 -> C^2.
    x  : length-E 1-cochain to classify.
    phi1_tol : labeled tolerance for the FLOAT Phi1 == 0 (EXACT) boundary.
    weights : optional per-edge L1 weights for Phi1 (default unit).

    Refuses (typed ``DimensionMismatch`` / ``CoboundaryLawViolation`` from
    ``CohomologyH1``) on shape mismatch or d1 d0 != 0. DIAGNOSTIC ONLY.
    """
    coh = _build_cohomology(d0, d1)
    xl: List[float] = [float(v) for v in x]
    if len(xl) != coh.num_edges:
        from omega_engine.crates.homology_theory.errors import DimensionMismatch

        raise DimensionMismatch(
            f"cochain has {len(xl)} entries, expected {coh.num_edges} edges"
        )

    gamma2_exact = coh.gamma2(xl)  
    gamma2_zero = gamma2_exact == 0
    closed = gamma2_zero  

    B = np.asarray(coh.d0_as_float(), dtype=float)
    omega = np.asarray(xl, dtype=float)
    _, _, cert = solve_phi(B, omega, weights=weights)
    phi1_est = float(cert.phi1)
    phi1_certified = cert.verify()
    phi1_is_zero = phi1_est <= phi1_tol

    exact_membership: Optional[bool] = None
    exact_test_agrees = True
    if closed:
        exact_membership = coh.is_exact(xl)  
        exact_test_agrees = exact_membership == phi1_is_zero

    if not closed:
        label = Trichotomy.OPEN
    else:
        if exact_membership:
            label = Trichotomy.EXACT
        else:
            label = Trichotomy.SURVIVOR

    return TrichotomyResult(
        label=label,
        closed=closed,
        gamma2_zero=gamma2_zero,
        gamma2_value=float(gamma2_exact),
        phi1_estimate=phi1_est,
        phi1_certified=phi1_certified,
        phi1_is_zero=phi1_is_zero,
        phi1_tol=phi1_tol,
        exact_membership=exact_membership,
        exact_test_agrees=exact_test_agrees,
    )


from omega_engine.crates.type.refusal import Refusal  


class TriRefused(Refusal):
    """Refusal representing a failure/refusal during trichotomy classification."""

    def __init__(self, reason: str, details: Any = None) -> None:
        super().__init__(f"TriRefused: {reason}", details)


def classify_exact(
    d0,
    d1,
    x: Sequence[float],
    phi1_tol: float = 1e-7,
    weights: Optional[np.ndarray] = None,
) -> Any:
    """Safe wrapper around classify that catches DimensionMismatch/CoboundaryLawViolation and returns TriRefused."""
    from omega_engine.crates.homology_theory.errors import DimensionMismatch, CoboundaryLawViolation

    try:
        return classify(d0, d1, x, phi1_tol, weights)
    except (DimensionMismatch, CoboundaryLawViolation) as e:
        return TriRefused(type(e).__name__, str(e))
    except Exception as e:
        return TriRefused("UnknownError", str(e))


from dataclasses import dataclass  
from enum import Enum  


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


ObstructionDiagnosticClass = Enum(
    "ObstructionDiagnosticClass",
    {
        "ExactRepair": "ExactRepair",
        "ClosedResidual": "ClosedResidual",
        "ActiveClosureFailure": "ActiveClosureFailure",
    },
    type=str,
)
ObstructionDiagnosticClass.__doc__ = (
    "Structural mirror of Rust ``ObstructionDiagnosticClass`` variants."
)


TrichotomyRefusal = Enum(
    "TrichotomyRefusal",
    {
        "NumericUndecidable": "NumericUndecidable",
        "IncompatiblePhi1Gamma2Evidence": "IncompatiblePhi1Gamma2Evidence",
    },
    type=str,
)
TrichotomyRefusal.__doc__ = "Structural mirror of Rust ``TrichotomyRefusal`` variants."


@dataclass(init=False)
class CertifiedExactTrichotomy(_RustSurfaceObject):
    """Structural mirror of Rust ``CertifiedExactTrichotomy``."""

    diagnostic_class: Any = None
    phi1_value: Any = None
    gamma2_value: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("diagnostic_class", "phi1_value", "gamma2_value")
        if len(args) > len(names):
            raise TypeError(
                "CertifiedExactTrichotomy received too many positional arguments"
            )
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


def diagnostic_class(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``diagnostic_class``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/trichotomy.rs::diagnostic_class"
    )


def phi1_value(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``phi1_value``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/trichotomy.rs::phi1_value"
    )


def gamma2_value(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``gamma2_value``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_functional/src/trichotomy.rs::gamma2_value"
    )


TrichotomyOutcome = Enum(
    "TrichotomyOutcome",
    {"Classified": "Classified", "TriRefused": "TriRefused"},
    type=str,
)
TrichotomyOutcome.__doc__ = "Structural mirror of Rust ``TrichotomyOutcome`` variants."






