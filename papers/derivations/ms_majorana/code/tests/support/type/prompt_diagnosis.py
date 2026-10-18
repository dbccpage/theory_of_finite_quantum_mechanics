"""Prompt-diagnosis payload and terminal types."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class DiagnosisTerminal(str, Enum):
    IMPROVED_CANDIDATE = "IMPROVED_CANDIDATE"
    NO_CHANGE = "NO_CHANGE"
    NEEDS_REPAIR = "NEEDS_REPAIR"
    REFUSED = "REFUSED"
    BUDGET_EXCEEDED = "BUDGET_EXCEEDED"
    DIAGNOSTIC_UNAVAILABLE = "DIAGNOSTIC_UNAVAILABLE"


@dataclass(frozen=True, slots=True)
class PromptCohomologyPayload:
    mapping_version: str
    vertices: tuple[str, ...]
    edges: tuple[tuple[int, int, str], ...]
    cells2: tuple[tuple[int, int, int, str], ...]
    c0_dim: int
    c1_dim: int
    c2_dim: int
    d0: tuple[tuple[int, int, int], ...]
    d1: tuple[tuple[int, int, int], ...]
    d1_d0_zero: bool
    d1_d0_composition: tuple[tuple[int, int, int], ...]
    complex_status: str
    ranks: dict[str, int]
    nullities: dict[str, int]
    betti: dict[str, int]
    omega: tuple[int, ...]
    alpha: tuple[int, ...]
    d0_alpha: tuple[int, ...]
    h1_residual: tuple[int, ...]
    phi1_before_exact: str
    phi1_after_exact: str
    phi1_before: float
    phi1_after: float
    gamma2_status: str
    xi: float | None
    certificates: dict[str, str]
    unresolved: tuple[str, ...]
    mapping_loss: tuple[str, ...]
    authority_effect: str = "None"
    evidence_class: str = "DiagnosticOnly"

    def to_dict(self) -> dict[str, Any]:
        return {
            "alpha": list(self.alpha),
            "authority_effect": self.authority_effect,
            "betti": dict(self.betti),
            "c0_dim": self.c0_dim,
            "c1_dim": self.c1_dim,
            "c2_dim": self.c2_dim,
            "cells2": [list(c) for c in self.cells2],
            "certificates": dict(self.certificates),
            "complex_status": self.complex_status,
            "d0": [list(x) for x in self.d0],
            "d0_alpha": list(self.d0_alpha),
            "d1": [list(x) for x in self.d1],
            "d1_d0_composition": [list(x) for x in self.d1_d0_composition],
            "d1_d0_zero": self.d1_d0_zero,
            "edges": [list(e) for e in self.edges],
            "evidence_class": self.evidence_class,
            "gamma2_status": self.gamma2_status,
            "h1_residual": list(self.h1_residual),
            "mapping_loss": list(self.mapping_loss),
            "mapping_version": self.mapping_version,
            "nullities": dict(self.nullities),
            "omega": list(self.omega),
            "phi1_after": self.phi1_after,
            "phi1_after_exact": self.phi1_after_exact,
            "phi1_before": self.phi1_before,
            "phi1_before_exact": self.phi1_before_exact,
            "ranks": dict(self.ranks),
            "unresolved": list(self.unresolved),
            "vertices": list(self.vertices),
            "xi": self.xi,
        }


@dataclass(frozen=True, slots=True)
class PromptDensityPayload:
    construction: str
    dimension: int
    dtype: str
    matrix: tuple[tuple[tuple[float, float], ...], ...]
    eigenvalues: tuple[float, ...]
    trace: float
    hermiticity_error: float
    min_eigenvalue: float
    psd: bool
    rank: int
    purity: float
    von_neumann_entropy: float
    l1_coherence: float
    budget: int
    budget_status: str
    authority_effect: str = "None"
    evidence_class: str = "DiagnosticOnly"

    def to_dict(self) -> dict[str, Any]:
        return {
            "authority_effect": self.authority_effect,
            "budget": self.budget,
            "budget_status": self.budget_status,
            "construction": self.construction,
            "dimension": self.dimension,
            "dtype": self.dtype,
            "eigenvalues": list(self.eigenvalues),
            "evidence_class": self.evidence_class,
            "hermiticity_error": self.hermiticity_error,
            "l1_coherence": self.l1_coherence,
            "matrix": [[[re, im] for re, im in row] for row in self.matrix],
            "min_eigenvalue": self.min_eigenvalue,
            "psd": self.psd,
            "purity": self.purity,
            "rank": self.rank,
            "trace": self.trace,
            "von_neumann_entropy": self.von_neumann_entropy,
        }


@dataclass(frozen=True, slots=True)
class PromptDiagnosis:
    packet: Any
    cohomology: PromptCohomologyPayload
    density: PromptDensityPayload
    must_constraints: tuple[str, ...]
    must_not_constraints: tuple[str, ...]
    residual_notes: tuple[str, ...]


__all__ = [
    "DiagnosisTerminal",
    "PromptCohomologyPayload",
    "PromptDensityPayload",
    "PromptDiagnosis",
]
