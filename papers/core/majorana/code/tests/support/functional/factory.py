"""Unified Functional Subsystem Factory and Evaluators.

Conforms to urn:omega:constitution:functional_kernel:v1.0.0.
Collapses fragmented functional evaluators (Gamma2, Phi1, Xi, Wigner-Yanase)
onto a standardized functional evaluation interface.
"""

from __future__ import annotations
import abc
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Union
import numpy as np


@dataclass(frozen=True)
class FunctionalEvaluationResult:
    """Standardized result envelope for functional kernel evaluations."""

    functional_id: str
    value: float
    is_closed: bool
    defects: List[float]
    metadata: Dict[str, Any]
    authority_effect: str = "evidence_only"


    @property
    def gamma2_mass(self) -> float:
        return self.value


def curvature_defect(cochain2: Sequence[float], *args: Any) -> float:
    val = float(sum(abs(x) for x in cochain2))
    if args:
        try:
            ref = float(sum(abs(x) for x in args[0]))
            return val - ref
        except Exception:
            pass
    return val


class BaseFunctionalKernel(abc.ABC):
    """Abstract base class for all Omega Engine functional kernels."""

    def __init__(self, functional_id: str):
        self.functional_id = functional_id

    @abc.abstractmethod
    def evaluate(self, *args: Any, **kwargs: Any) -> FunctionalEvaluationResult:
        """Evaluate functional and return standardized FunctionalEvaluationResult."""
        pass


class Gamma2Kernel(BaseFunctionalKernel):
    """Gamma2 2-cochain curvature defect functional kernel."""

    def __init__(self) -> None:
        super().__init__(functional_id="gamma2")

    def evaluate(self, cochain2: Sequence[float], tol: float = 1e-9, **kwargs: Any) -> FunctionalEvaluationResult:
        defects = [float(abs(x)) for x in cochain2]
        val = float(sum(defects))
        return FunctionalEvaluationResult(
            functional_id=self.functional_id,
            value=val,
            is_closed=val < tol,
            defects=defects,
            metadata={"tol": tol},
            authority_effect="None",
        )


class Phi1Kernel(BaseFunctionalKernel):
    """Phi1 1-cochain normal residual norm functional kernel."""

    def __init__(self) -> None:
        super().__init__(functional_id="phi1")

    def evaluate(self, cochain1: Sequence[float], tol: float = 1e-9, **kwargs: Any) -> FunctionalEvaluationResult:
        defects = [float(abs(x)) for x in cochain1]
        val = float(sum(defects))
        return FunctionalEvaluationResult(
            functional_id=self.functional_id,
            value=val,
            is_closed=val < tol,
            defects=defects,
            metadata={"tol": tol},
            authority_effect="None",
        )


class WignerYanaseKernel(BaseFunctionalKernel):
    """Wigner-Yanase skew information functional kernel."""

    def __init__(self) -> None:
        super().__init__(functional_id="wigner_yanase")

    def evaluate(self, rho: np.ndarray, h_op: np.ndarray, tol: float = 1e-9, **kwargs: Any) -> FunctionalEvaluationResult:
        try:
            from omega_engine.crates.quantum_physics.cptp_channel import wigner_yanase_skew_information
        except ImportError:
            from omega_engine.crates.quantum_physics.cptp_channel import wigner_yanase_skew_information
        val = wigner_yanase_skew_information(rho, h_op)
        return FunctionalEvaluationResult(
            functional_id=self.functional_id,
            value=val,
            is_closed=abs(val) < tol,
            defects=[val],
            metadata={"tol": tol},
            authority_effect="None",
        )


XiKernel = WignerYanaseKernel

_FUNCTIONAL_REGISTRY: Dict[str, BaseFunctionalKernel] = {
    "gamma2": Gamma2Kernel(),
    "phi1": Phi1Kernel(),
    "wigner_yanase": WignerYanaseKernel(),
    "xi": WignerYanaseKernel(),
}


def evaluate_functional(name: str, *args: Any, **kwargs: Any) -> FunctionalEvaluationResult:
    """Centralized factory evaluator for named functional kernels."""
    if name not in _FUNCTIONAL_REGISTRY:
        raise KeyError(f"Unknown functional kernel {name!r}. Available: {list(_FUNCTIONAL_REGISTRY.keys())}")
    return _FUNCTIONAL_REGISTRY[name].evaluate(*args, **kwargs)


def evaluate_gamma2(cochain2: Sequence[float], tol: float = 1e-9, **kwargs: Any) -> FunctionalEvaluationResult:
    return evaluate_functional("gamma2", cochain2, tol=tol, **kwargs)


def evaluate_phi1(cochain1: Sequence[float], tol: float = 1e-9, **kwargs: Any) -> FunctionalEvaluationResult:
    return evaluate_functional("phi1", cochain1, tol=tol, **kwargs)


def evaluate_xi(rho: np.ndarray, h_op: np.ndarray, tol: float = 1e-9, **kwargs: Any) -> FunctionalEvaluationResult:
    return evaluate_functional("xi", rho, h_op, tol=tol, **kwargs)


def list_available_functionals() -> List[str]:
    """Return list of available functional kernel names."""
    return list(_FUNCTIONAL_REGISTRY.keys())



__all__ = [
    "FunctionalEvaluationResult",
    "BaseFunctionalKernel",
    "Gamma2Kernel",
    "Phi1Kernel",
    "WignerYanaseKernel",
    "XiKernel",
    "evaluate_functional",
    "list_available_functionals",
    "evaluate_gamma2",
    "evaluate_phi1",
    "evaluate_xi",
    "curvature_defect",
]






