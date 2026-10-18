"""PromptDiagnosisEngine — finite cochain + density diagnostics for prompts.

Diagnostic encoding only. Not an ontology of language. Not a physical quantum
state. AuthorityEffect remains None. No pipeline/runtime imports.
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Any, Sequence

import numpy as np

try:
    from omega_engine.crates.applications.omega_runtimes import (
        CarrierKind,
        PromptPacketCore,
        PromptPacketRecord,
        sha256_text,
    )
except ImportError:
    CarrierKind = None
    PromptPacketCore = None
    PromptPacketRecord = None
    import hashlib

    def sha256_text(t: str) -> str:
        return hashlib.sha256(t.encode("utf-8")).hexdigest()


MAPPING_VERSION = "omega.prompt_cochain_mapper.v1"
DENSITY_BUDGET_DEFAULT = 32


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
    packet: PromptPacketCore
    cohomology: PromptCohomologyPayload
    density: PromptDensityPayload
    must_constraints: tuple[str, ...]
    must_not_constraints: tuple[str, ...]
    residual_notes: tuple[str, ...]


def _split_clauses(text: str) -> list[str]:
    parts: list[str] = []
    for line in text.replace("\r\n", "\n").split("\n"):
        line = line.strip()
        if not line:
            continue
        for chunk in line.replace(";", ".").split("."):
            c = chunk.strip()
            if c:
                parts.append(c)
    return parts or ["(empty)"]


def _build_cohomology(
    text: str, *, retain_clause_text: bool = False
) -> PromptCohomologyPayload:
    clauses = _split_clauses(text)[:48]
    if retain_clause_text:
        vertices = tuple(clauses)
    else:
        vertices = tuple(sha256_text(c)[:16] for c in clauses)
    n = len(vertices)
    edges: list[tuple[int, int, str]] = []
    for i in range(n - 1):
        edges.append((i, i + 1, "sequence"))
        a, b = clauses[i].casefold(), clauses[i + 1].casefold()
        if "must not" in a and "must" in b and "must not" not in b:
            edges.append((i, i + 1, "constraint_tension"))
        if any(k in a for k in ("never", "forbid", "do not")) and any(
            k in b for k in ("always", "must", "require")
        ):
            edges.append((i, i + 1, "contradiction_witness"))
    m = len(edges)
    d0: list[tuple[int, int, int]] = []
    for e_idx, (u, v, _k) in enumerate(edges):
        d0.append((e_idx, u, -1))
        d0.append((e_idx, v, 1))
    cells2: list[tuple[int, int, int, str]] = []
    d1: list[tuple[int, int, int]] = []
    d1_d0_composition = _compose_sparse(d1, d0, n_out=len(cells2), n_mid=m, n_in=n)
    d1_d0_zero = len(d1_d0_composition) == 0
    complex_status = "VALID_COMPLEX" if d1_d0_zero else "INVALID_COMPLEX"
    omega = tuple(1 if k == "contradiction_witness" else 0 for _, _, k in edges)
    alpha = tuple(0 for _ in range(n))  
    d0_alpha = tuple(0 for _ in range(m))
    h1 = omega
    phi1_exact = Fraction(sum(abs(int(x)) for x in h1), 1)
    phi1 = float(phi1_exact)
    rank_d0 = min(n, m) if m else 0
    return PromptCohomologyPayload(
        mapping_version=MAPPING_VERSION,
        vertices=vertices,
        edges=tuple(edges),
        cells2=tuple(cells2),
        c0_dim=n,
        c1_dim=m,
        c2_dim=len(cells2),
        d0=tuple(d0),
        d1=tuple(d1),
        d1_d0_zero=d1_d0_zero,
        d1_d0_composition=tuple(d1_d0_composition),
        complex_status=complex_status,
        ranks={"d0": rank_d0, "d1": min(len(cells2), m) if cells2 else 0},
        nullities={
            "d0": max(0, n - rank_d0),
            "d1": max(0, m - (min(len(cells2), m) if cells2 else 0)),
        },
        betti={
            "b0": max(1, n - rank_d0),
            "b1": max(0, m - rank_d0 - (min(len(cells2), m) if cells2 else 0)),
            "b2": max(0, len(cells2) - (min(len(cells2), m) if cells2 else 0)),
        },
        omega=omega,
        alpha=alpha,
        d0_alpha=d0_alpha,
        h1_residual=h1,
        phi1_before_exact=str(phi1_exact),
        phi1_after_exact=str(phi1_exact),
        phi1_before=phi1,
        phi1_after=phi1,
        gamma2_status="UNRESOLVED" if not cells2 else "STRUCTURAL_CLOSED",
        xi=None,
        certificates={
            "d1_d0": "PASS" if d1_d0_zero else "INVALID_COMPLEX",
            "phi1": "COMPUTED_EXACT",
            "complex_status": complex_status,
        },
        unresolved=("no_xi_without_phase_witness",),
        mapping_loss=("clause_split_is_diagnostic_not_semantic",),
    )


def _compose_sparse(
    d1: list[tuple[int, int, int]],
    d0: list[tuple[int, int, int]],
    *,
    n_out: int,
    n_mid: int,
    n_in: int,
) -> list[tuple[int, int, int]]:
    """Compute sparse matrix product d1 @ d0 as list of (row, col, value) nonzero entries."""
    if n_out == 0 or n_in == 0 or n_mid == 0:
        return []
    a = [[0 for _ in range(n_mid)] for _ in range(n_out)]
    b = [[0 for _ in range(n_in)] for _ in range(n_mid)]
    for r, c, v in d1:
        if 0 <= r < n_out and 0 <= c < n_mid:
            a[r][c] += v
    for r, c, v in d0:
        if 0 <= r < n_mid and 0 <= c < n_in:
            b[r][c] += v
    out: list[tuple[int, int, int]] = []
    for i in range(n_out):
        for k in range(n_in):
            s = 0
            for j in range(n_mid):
                s += a[i][j] * b[j][k]
            if s != 0:
                out.append((i, k, s))
    return out


def _extract_constraints(text: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    must: list[str] = []
    must_not: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        low = s.casefold()
        if (
            low.startswith("must not")
            or low.startswith("must_not")
            or "must not " in low
        ):
            must_not.append(s)
        elif low.startswith("must ") or low.startswith("must:"):
            must.append(s)
    return tuple(must), tuple(must_not)


def _density_from_residual(
    h1: Sequence[int | float],
    *,
    budget: int = DENSITY_BUDGET_DEFAULT,
) -> PromptDensityPayload:
    vec = np.array([float(x) for x in h1], dtype=float)
    if vec.size == 0:
        vec = np.array([1.0], dtype=float)
    dim = int(vec.size)
    if dim > budget:
        return PromptDensityPayload(
            construction="diagonal_residual_density_diagnostic",
            dimension=dim,
            dtype="complex128",
            matrix=tuple(),
            eigenvalues=tuple(),
            trace=0.0,
            hermiticity_error=0.0,
            min_eigenvalue=0.0,
            psd=False,
            rank=0,
            purity=0.0,
            von_neumann_entropy=0.0,
            l1_coherence=0.0,
            budget=budget,
            budget_status="BUDGET_EXCEEDED",
        )
    absv = np.abs(vec)
    s = float(absv.sum())
    if s <= 0:
        probs = np.ones(dim) / dim
    else:
        probs = absv / s
    rho = np.diag(probs).astype(complex)
    herm_err = float(np.linalg.norm(rho - rho.conj().T, ord="fro"))
    eig = np.real(np.linalg.eigvalsh(rho))
    eig = np.clip(eig, 0.0, None)
    if eig.sum() > 0:
        eig = eig / eig.sum()
    purity = float(np.real(np.trace(rho @ rho)))
    ent = 0.0
    for lam in eig:
        if lam > 1e-15:
            ent -= float(lam * np.log(lam))
    off = rho - np.diag(np.diag(rho))
    l1c = float(np.sum(np.abs(off)))
    mat = tuple(
        tuple(
            (float(np.real(rho[i, j])), float(np.imag(rho[i, j]))) for j in range(dim)
        )
        for i in range(dim)
    )
    return PromptDensityPayload(
        construction="diagonal_residual_density_diagnostic",
        dimension=dim,
        dtype="complex128",
        matrix=mat,
        eigenvalues=tuple(float(x) for x in eig),
        trace=float(np.real(np.trace(rho))),
        hermiticity_error=herm_err,
        min_eigenvalue=float(eig.min()) if eig.size else 0.0,
        psd=bool(eig.min() >= -1e-12) if eig.size else True,
        rank=int(np.sum(eig > 1e-12)),
        purity=purity,
        von_neumann_entropy=ent,
        l1_coherence=l1c,
        budget=budget,
        budget_status="OK",
    )


class PromptDiagnosisEngine:
    """Engine-layer diagnosis. No FS / network / pipeline imports."""

    def __init__(self, density_budget: int = DENSITY_BUDGET_DEFAULT) -> None:
        if density_budget < 1:
            raise ValueError("density_budget must be positive")
        self.density_budget = density_budget

    def diagnose(
        self,
        text: str,
        *,
        retain_clause_text: bool = False,
    ) -> PromptDiagnosis:
        record = PromptPacketRecord.from_raw(text, CarrierKind.PROMPT)
        coh = _build_cohomology(text, retain_clause_text=retain_clause_text)
        dens = _density_from_residual(coh.h1_residual, budget=self.density_budget)
        must, must_not = _extract_constraints(text)
        if not retain_clause_text:
            must = tuple(sha256_text(m)[:16] for m in must)
            must_not = tuple(sha256_text(m)[:16] for m in must_not)
        notes = (
            "diagnostic_encoding_not_language_ontology",
            "density_not_physical_quantum_state",
            "authority_effect_none",
            "clause_vertices_are_hashes_unless_retain_clause_text",
        )
        if dens.budget_status == "BUDGET_EXCEEDED":
            notes = notes + ("density_budget_exceeded",)
        return PromptDiagnosis(
            packet=record.core,
            cohomology=coh,
            density=dens,
            must_constraints=must,
            must_not_constraints=must_not,
            residual_notes=notes,
        )

    def compare(
        self,
        original: PromptDiagnosis,
        improved: PromptDiagnosis,
    ) -> dict[str, Any]:
        o_phi = original.cohomology.phi1_before
        i_phi = improved.cohomology.phi1_before
        comparable = (
            original.density.budget_status == "OK"
            and improved.density.budget_status == "OK"
            and original.density.dimension == improved.density.dimension
        )
        density_delta: dict[str, Any]
        if comparable:
            p = np.array(original.density.eigenvalues)
            q = np.array(improved.density.eigenvalues)
            n = max(p.size, q.size)
            pp = np.zeros(n)
            qq = np.zeros(n)
            pp[: p.size] = p
            qq[: q.size] = q
            td = 0.5 * float(np.sum(np.abs(pp - qq)))
            fid = float(np.sum(np.sqrt(np.clip(pp * qq, 0, None))) ** 2)
            density_delta = {
                "comparable": True,
                "trace_distance": td,
                "fidelity": fid,
                "purity_delta": improved.density.purity - original.density.purity,
                "entropy_delta": improved.density.von_neumann_entropy
                - original.density.von_neumann_entropy,
            }
        else:
            density_delta = {
                "comparable": False,
                "status": "NOT_COMPARABLE",
                "transport_or_loss": "dimension_or_budget_mismatch",
            }
        improved_text_proxy = " ".join(improved.cohomology.vertices).casefold()
        lost = [
            m
            for m in original.must_constraints
            if m.casefold() not in improved_text_proxy
            and m.casefold() not in " ".join(improved.must_constraints).casefold()
        ]
        return {
            "cohomology_delta": {
                "phi1_before": o_phi,
                "phi1_after": i_phi,
                "phi1_delta": i_phi - o_phi,
                "gamma2_original": original.cohomology.gamma2_status,
                "gamma2_improved": improved.cohomology.gamma2_status,
            },
            "density_delta": density_delta,
            "intent_preservation": {
                "lost_must": lost,
                "passed": len(lost) == 0,
            },
            "transport_or_loss_ledger": list(original.cohomology.mapping_loss)
            + list(improved.cohomology.mapping_loss),
            "improvement_criteria": [
                "must_constraints_preserved",
                "no_new_contradiction_required",
                "comparison_payload_present",
            ],
            "criteria_passed": len(lost) == 0,
            "authority_effect": "None",
        }


__all__ = [
    "DiagnosisTerminal",
    "MAPPING_VERSION",
    "PromptCohomologyPayload",
    "PromptDensityPayload",
    "PromptDiagnosis",
    "PromptDiagnosisEngine",
]





