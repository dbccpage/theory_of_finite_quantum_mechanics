"""Local solver contract and factory definitions for paper 002.

AuthorityEffect: None.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import hashlib
import json
from typing import Any, Callable, Dict, List, Optional


@dataclass(frozen=True)
class SolverCertificate:
    certificate_type: str
    witness_data: Dict[str, Any]
    is_valid: bool
    certificate_hash: str


@dataclass(frozen=True)
class SolverInput:
    problem_id: str
    category: str = "LatticeMonteCarlo"
    data: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class CheckedOutput:
    authority_effect: str
    verification_hash: str
    is_valid: bool


@dataclass(frozen=True)
class SolverOutput:
    problem_id: str
    solver_id: str
    status: str
    residual_mass: float
    residual_vector: List[float]
    certificate: SolverCertificate
    metadata: Dict[str, Any]
    authority_effect: str


class BaseSolver(ABC):
    def __init__(
        self,
        solver_id: str,
        category: str = "General",
        solver_version: str = "v1.0.0",
        descriptor: Any = None,
        dependencies: Optional[Dict[str, Any]] = None,
    ):
        self.solver_id = solver_id
        self.category = category
        self.solver_version = solver_version
        self.descriptor = descriptor
        self.dependencies = dict(dependencies or {})

    def get_dependency(self, name: str, default: Any = None) -> Any:
        return self.dependencies.get(name, default)

    @abstractmethod
    def solve(self, solver_input: SolverInput) -> SolverOutput:
        raise NotImplementedError

    def verify_output(self, output: SolverOutput) -> CheckedOutput:
        valid = output.certificate is not None and output.certificate.is_valid
        content = json.dumps(
            {
                "problem_id": output.problem_id,
                "solver_id": output.solver_id,
                "status": output.status,
                "cert_hash": output.certificate.certificate_hash if output.certificate else "",
            },
            sort_keys=True,
        ).encode("utf-8")
        h = hashlib.sha256(content).hexdigest()
        return CheckedOutput(
            authority_effect="FactOnly",
            verification_hash=h,
            is_valid=valid,
        )


_SOLVER_REGISTRY: Dict[str, Callable[[], BaseSolver]] = {}


def register_solver(name: str, factory: Callable[[], BaseSolver]) -> None:
    _SOLVER_REGISTRY[name] = factory


def list_available_solvers() -> List[str]:
    return sorted(_SOLVER_REGISTRY.keys())


def create_solver(name: str) -> BaseSolver:
    if name in _SOLVER_REGISTRY:
        return _SOLVER_REGISTRY[name]()
    raise ValueError(f"Unknown solver: {name}. Available: {list_available_solvers()}")


# Register the paper's regge_susy_saturation solver
def _regge_susy_factory() -> BaseSolver:
    from regge_susy_saturation_solver import ReggeSUSYSaturationSolverAdapter
    return ReggeSUSYSaturationSolverAdapter()


register_solver("regge_susy_saturation", _regge_susy_factory)

__all__ = [
    "BaseSolver",
    "CheckedOutput",
    "SolverCertificate",
    "SolverInput",
    "SolverOutput",
    "create_solver",
    "list_available_solvers",
    "register_solver",
]
