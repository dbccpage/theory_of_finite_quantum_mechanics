"""Deterministic finite replays for PO-000 §§6 and Pass 45.

The records in this module are numerical instance evidence.  They do not
upgrade the paper's prose theorems to Python-proved statements.
"""

from __future__ import annotations
from dataclasses import dataclass
from math import isfinite, pi, sqrt
from typing import Any, Literal, cast

import numpy as np

from omega_engine.crates.quantum_physics.quantum_lattice import (
    DEFAULT_COMPARISON_ATOL,
    ComplexMatrix,
    FiniteQuantumLattice,
    LocalHamiltonianTerm,
    QuantumInputError,
    operator_norm,
)


def _finite_scalar(value: object, *, name: str) -> float:
    if isinstance(value, bool):
        raise QuantumInputError(f"{name} must be a finite real number")
    try:
        result = float(cast(Any, value))
    except (TypeError, ValueError) as error:
        raise QuantumInputError(f"{name} must be a finite real number") from error
    if not isfinite(result):
        raise QuantumInputError(f"{name} must be finite")
    return result


def _density(vector: ComplexMatrix) -> ComplexMatrix:
    return np.outer(vector, vector.conj()).astype(np.complex128)


def _paulis() -> tuple[ComplexMatrix, ComplexMatrix, ComplexMatrix]:
    x = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    y = np.array([[0, -1.0j], [1.0j, 0]], dtype=np.complex128)
    z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
    return x, y, z


@dataclass
class TwoQubitXXExampleReplay:
    coupling: float
    t: float
    observed_defect: float
    closed_form_defect: float
    absolute_error: float
    expected_special_value: float
    evidence_kind: Literal["numerical_replay"] = "numerical_replay"
    limitations: tuple[str, ...] = (
        "One finite two-qubit replay at theta=pi/8; not a proof for all times.",
    )


@dataclass
class TFIMNormalRateReplay:
    num_sites: int
    coupling: float
    field: float
    edge_rates: tuple[tuple[tuple[str, str], float], ...]
    expected_rate: float
    maximum_rate_error: float
    full_incident_g: float
    paper_g_upper_bound: float
    g_within_paper_bound: bool
    all_edges_active: bool
    evidence_kind: Literal["numerical_replay"] = "numerical_replay"
    limitations: tuple[str, ...] = (
        "Finite open chains only; field-independence is replayed on supplied instances.",
    )


@dataclass
class Pass45CounterexampleReplay:
    t: float
    nu_e: float
    isolated_two_site_g: float
    full_incident_g: float
    observed_defect: float
    isolated_signed_rhs: float
    full_signed_rhs: float
    isolated_bound_violated: bool
    full_bound_satisfied_with_tolerance: bool
    evidence_kind: Literal["counterexample"] = "counterexample"
    limitations: tuple[str, ...] = (
        "One finite three-qubit counterexample to substituting isolated g into the lattice bound.",
        "The negative full-g RHS makes the corrected comparison trivial at this time.",
    )


def two_qubit_xx_lattice(coupling: object = 1.0) -> FiniteQuantumLattice:
    """Construct the finite two-qubit XX carrier used by §6.1."""

    j = _finite_scalar(coupling, name="coupling")
    x, _y, _z = _paulis()
    zero = np.array([1.0, 0.0], dtype=np.complex128)
    return FiniteQuantumLattice(
        site_order=("a", "b"),
        dimensions={"a": 2, "b": 2},
        terms=(
            LocalHamiltonianTerm(
                label="ab",
                support=("a", "b"),
                operator=np.asarray(j * np.kron(x, x), dtype=np.complex128),
            ),
        ),
        product_state={"a": _density(zero), "b": _density(zero)},
    )


def two_qubit_xx_example(coupling: object = 1.0) -> TwoQubitXXExampleReplay:
    """Replay §6.1 at ``t=pi/(8*|J|)``."""

    j = _finite_scalar(coupling, name="coupling")
    if j == 0.0:
        raise QuantumInputError("the §6.1 special time requires nonzero coupling")
    lattice = two_qubit_xx_lattice(j)
    t = pi / (8.0 * abs(j))
    observed = lattice.edge_evolution_replay(("a", "b"), t).defect
    theta = abs(j) * t
    c = float(np.cos(theta))
    s = float(np.sin(theta))
    closed_form = 2.0 * c * s + 2.0 * c**2 * s**2
    expected = 1.0 / sqrt(2.0) + 0.25
    return TwoQubitXXExampleReplay(
        coupling=j,
        t=t,
        observed_defect=observed,
        closed_form_defect=closed_form,
        absolute_error=abs(observed - closed_form),
        expected_special_value=expected,
    )


def tfim_normal_rate_example(
    *, num_sites: int = 4, coupling: object = 1.0, field: object = 0.0
) -> TFIMNormalRateReplay:
    """Replay the §6.2 open-chain rates ``nu_e=2|J|``."""

    if isinstance(num_sites, bool) or not isinstance(num_sites, int) or num_sites < 2:
        raise QuantumInputError("num_sites must be an integer at least two")
    j = _finite_scalar(coupling, name="coupling")
    h = _finite_scalar(field, name="field")
    x, _y, z = _paulis()
    plus = np.array([1.0, 1.0], dtype=np.complex128) / sqrt(2.0)
    sites = tuple(f"q{index}" for index in range(num_sites))
    terms: list[LocalHamiltonianTerm] = []
    for index, site in enumerate(sites):
        terms.append(
            LocalHamiltonianTerm(
                label=f"field_{index}",
                support=(site,),
                operator=-h * x,
            )
        )
    for index in range(num_sites - 1):
        terms.append(
            LocalHamiltonianTerm(
                label=f"bond_{index}_{index + 1}",
                support=(sites[index], sites[index + 1]),
                operator=np.asarray(-j * np.kron(z, z), dtype=np.complex128),
            )
        )
    lattice = FiniteQuantumLattice(
        site_order=sites,
        dimensions={site: 2 for site in sites},
        terms=tuple(terms),
        product_state={site: _density(plus) for site in sites},
    )
    rates = tuple(
        (
            (sites[index], sites[index + 1]),
            lattice.normal_rate_replay((sites[index], sites[index + 1])).nu_e,
        )
        for index in range(num_sites - 1)
    )
    expected = 2.0 * abs(j)
    maximum_error = max(abs(rate - expected) for _edge, rate in rates)
    paper_bound = 2.0 * abs(j) + abs(h)
    g = lattice.full_incident_norm_g
    tolerance = 100.0 * DEFAULT_COMPARISON_ATOL
    return TFIMNormalRateReplay(
        num_sites=num_sites,
        coupling=j,
        field=h,
        edge_rates=rates,
        expected_rate=expected,
        maximum_rate_error=maximum_error,
        full_incident_g=g,
        paper_g_upper_bound=paper_bound,
        g_within_paper_bound=g <= paper_bound + tolerance,
        all_edges_active=j != 0.0 and all(rate > tolerance for _edge, rate in rates),
    )


def pass45_counterexample_lattice() -> FiniteQuantumLattice:
    """Construct the three-qubit Pass 45 lattice fixture."""

    x, y, z = _paulis()
    plus = np.array([1.0, 1.0], dtype=np.complex128) / sqrt(2.0)
    plus_i = np.array([1.0, 1.0j], dtype=np.complex128) / sqrt(2.0)
    zero = np.array([1.0, 0.0], dtype=np.complex128)
    return FiniteQuantumLattice(
        site_order=("u", "v", "w"),
        dimensions={"u": 2, "v": 2, "w": 2},
        terms=(
            LocalHamiltonianTerm(
                label="uv",
                support=("u", "v"),
                operator=np.asarray(np.kron(z, x), dtype=np.complex128),
            ),
            LocalHamiltonianTerm(
                label="uw",
                support=("u", "w"),
                operator=np.asarray(100.0 * np.kron(y, z), dtype=np.complex128),
            ),
        ),
        product_state={
            "u": _density(plus),
            "v": _density(plus_i),
            "w": _density(zero),
        },
    )


def pass45_counterexample_replay(
    *, t: object = 0.03, comparison_tolerance: object = DEFAULT_COMPARISON_ATOL
) -> Pass45CounterexampleReplay:
    """Replay the failure caused by substituting isolated ``g`` into Theorem 5.1."""

    time = _finite_scalar(t, name="t")
    if time < 0.0:
        raise QuantumInputError("t must be nonnegative")
    tolerance = _finite_scalar(comparison_tolerance, name="comparison_tolerance")
    if tolerance <= 0.0:
        raise QuantumInputError("comparison_tolerance must be strictly positive")
    lattice = pass45_counterexample_lattice()
    normal = lattice.normal_rate_replay(("u", "v"))
    evolution = lattice.edge_evolution_replay(("u", "v"), time)
    uv_term = next(term for term in lattice.terms if term.label == "uv")
    isolated_g = operator_norm(uv_term.operator)
    full_g = lattice.full_incident_norm_g
    isolated_rhs = normal.nu_e * time - 24.0 * isolated_g**2 * time**2
    full_rhs = normal.nu_e * time - 24.0 * full_g**2 * time**2
    return Pass45CounterexampleReplay(
        t=time,
        nu_e=normal.nu_e,
        isolated_two_site_g=isolated_g,
        full_incident_g=full_g,
        observed_defect=evolution.defect,
        isolated_signed_rhs=isolated_rhs,
        full_signed_rhs=full_rhs,
        isolated_bound_violated=evolution.defect < isolated_rhs - tolerance,
        full_bound_satisfied_with_tolerance=evolution.defect >= full_rhs - tolerance,
    )





