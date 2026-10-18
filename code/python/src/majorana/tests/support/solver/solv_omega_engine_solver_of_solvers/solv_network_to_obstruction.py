"""Network → exact rational obstruction bridge.

Builds FiniteCochainComplex over Q from a Network topology and routes the
residual through evaluate_obstruction (Gate 11). Used by CascadeSolver so
that Exact / CLOSED_NONEXACT / NONCLOSED claims come only from the rational
kernel. Float multi-cycle L1 remains diagnostic / descent machinery only.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple

from omega_engine.crates.homology_theory.finite_cochain_complex import FiniteCochainComplex
from omega_engine.crates.residuals.network_residual import Network
from omega_engine.crates.solver.solv_omega_engine_solver_of_solvers.solv_obstruction_evaluator import (
    ObstructionClass,
    ObstructionReceipt,
    evaluate_obstruction,
)


def _fraction(value: Any) -> Fraction:
    if isinstance(value, bool) or isinstance(value, float):
        # Convert float via string to avoid binary artefacts when possible;
        # callers should prefer exact inputs. Diagnostic path only.
        return Fraction(str(value)).limit_denominator(10**9)
    return Fraction(value)


def network_to_finite_complex(
    network: Network,
) -> FiniteCochainComplex:
    """Build exact-Q FiniteCochainComplex from Network topology.

    d0 : C0 → C1 incidence (edge = head − tail)
    d1 : C1 → C2 face boundary (oriented cycle sum)
    """
    nodes = list(network.nodes)
    edges = list(network.edges)
    faces = list(network.faces) if network.faces else []

    n0, n1, n2 = len(nodes), len(edges), len(faces)
    node_idx = {n: i for i, n in enumerate(nodes)}
    edge_idx = {e: i for i, e in enumerate(edges)}

    # d0 rows = edges, cols = nodes
    d0_rows = []
    for u, v in edges:
        row = [Fraction(0)] * n0
        row[node_idx[u]] = Fraction(-1)
        row[node_idx[v]] = Fraction(1)
        d0_rows.append(row)

    # d1 rows = faces, cols = edges
    d1_rows = []
    for u, v, w in faces:
        row = [Fraction(0)] * n1
        for (x, y), sign in [((u, v), 1), ((v, w), 1), ((w, u), 1)]:
            if (x, y) in edge_idx:
                row[edge_idx[(x, y)]] += Fraction(sign)
            elif (y, x) in edge_idx:
                row[edge_idx[(y, x)]] -= Fraction(sign)
        d1_rows.append(row)

    return FiniteCochainComplex.from_rows(
        (n0, n1, n2),
        d0_rows,
        d1_rows,
    )


def residual_to_omega(
    network: Network,
    residual: Mapping[Tuple[Any, Any], Any],
) -> Tuple[Fraction, ...]:
    """Ordered omega vector aligned with network.edges."""
    return tuple(
        _fraction(residual.get(e, 0))
        for e in network.edges
    )


def classify_network_residual(
    network: Network,
    residual: Mapping[Tuple[Any, Any], Any],
    w: Optional[Sequence[Fraction]] = None,
    v: Optional[Sequence[Fraction]] = None,
) -> ObstructionReceipt:
    """Single entry point: Network residual → Gate-11 ObstructionReceipt.

    AuthorityEffect: None. Exact arithmetic over Q.
    """
    complex_ = network_to_finite_complex(network)
    omega = residual_to_omega(network, residual)
    return evaluate_obstruction(complex_, omega, w=w, v=v)


def obstruction_class_to_terminal_status(cls: ObstructionClass) -> str:
    """Map paper vocabulary onto CascadeSolver terminal_status strings."""
    if cls is ObstructionClass.EXACT:
        return "Exact"
    if cls is ObstructionClass.CLOSED_NONEXACT:
        return "CLOSED_NONEXACT"
    if cls is ObstructionClass.NONCLOSED:
        return "NONCLOSED"
    if cls is ObstructionClass.INVALID_COMPLEX:
        return "INVALID_COMPLEX"
    return "TYPED_OBSTRUCTION"


__all__ = [
    "network_to_finite_complex",
    "residual_to_omega",
    "classify_network_residual",
    "obstruction_class_to_terminal_status",
]
