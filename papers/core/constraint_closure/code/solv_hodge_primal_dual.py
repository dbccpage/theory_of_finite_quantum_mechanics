"""Port of ``omega_solvers/src/topology/solver_hodge_primal_dual_decomp.rs``.

ARCHITECTURAL BOUNDARY (from the Rust source): this is the L2 heuristic Hodge
decomposition. In the current Rust source EVERY compute function is
``unimplemented!()`` ("Heuristic float-based solvers are deprecated. Use Exact
Obstruction Calculus."). The Python port preserves the data types and raises
``NotImplementedError`` from every compute entry point.

FIREWALL TRACKING NOTE: if these archived Hodge paths are ever exposed through
``/api/certify`` or certificate generation, catch ``NotImplementedError`` at the
API boundary and terminalize as ``RefusedDeprecatedHeuristicSolver`` -- do NOT
add that terminal status globally until a live route can actually reach here.
"""

from __future__ import annotations
from dataclasses import field
from dataclasses import dataclass
from typing import Any, List, Optional

try:
    from .solv_q_obstruction import (
        QObstructionInputDegree1,
        QObstructionSolver,
        QSpectralReceipt,
        degree1_hodge_laplacian,
        solve_degree1,
    )
    from .solver_evidence import SolverResult
except ImportError:
    from solv_q_obstruction import (
        QObstructionInputDegree1,
        QObstructionSolver,
        QSpectralReceipt,
        degree1_hodge_laplacian,
        solve_degree1,
    )
    from solver_evidence import SolverResult

DEFAULT_MAX_ITER = 8000
DEFAULT_TOL = 1e-10
PHI_EPS = 1e-8

_ARCHIVED = (
    "Heuristic float-based solvers are deprecated. Use Exact Obstruction Calculus."
)


@dataclass
class Topology:
    """``Topology`` enum: either a graph, or an independent edge count."""

    graph: Optional[Any] = None
    num_edges_independent: Optional[int] = None

    @staticmethod
    def from_graph(graph) -> "Topology":
        return Topology(graph=graph)

    @staticmethod
    def independent(num_edges: int) -> "Topology":
        if num_edges < 0:
            raise ValueError("num_edges must be non-negative")
        return Topology(num_edges_independent=num_edges)

    def num_edges(self) -> int:
        if self.graph is not None:
            return len(self.graph.edges())
        return int(self.num_edges_independent or 0)


@dataclass
class CoreDiagnostics:
    reconstruction_error: float
    dual_stationary: bool
    box_feasible: bool
    kkt_like: bool
    iterations_executed: int
    numerically_converged: bool


@dataclass
class QuotientDecomposition:
    exact: List[float] = field(default_factory=list)
    irreducible: List[float] = field(default_factory=list)
    vertex_potential: List[float] = field(default_factory=list)


@dataclass
class HarmonicDecomposition:
    exact: List[float] = field(default_factory=list)
    vertex_potential: List[float] = field(default_factory=list)
    harmonic: List[float] = field(default_factory=list)


@dataclass
class L1HodgeCoreOutput:
    f_star: List[float] = field(default_factory=list)
    delta_exact: List[float] = field(default_factory=list)
    delta_irr: List[float] = field(default_factory=list)
    dual_witness: List[float] = field(default_factory=list)
    diagnostics: Optional[CoreDiagnostics] = None


def quotient_decomposition(topology, delta) -> QuotientDecomposition:
    raise NotImplementedError(_ARCHIVED)


def irreducible_representative(topology, delta) -> List[float]:
    raise NotImplementedError(_ARCHIVED)


def irreducible_l1_obstruction(graph, tau, config) -> QuotientDecomposition:
    raise NotImplementedError(_ARCHIVED)


def compute_l2_hodge_graph(graph, tau) -> QuotientDecomposition:
    raise NotImplementedError(_ARCHIVED)


def compute_l2_hodge_independent(topology, tau) -> QuotientDecomposition:
    raise NotImplementedError(_ARCHIVED)


def chambolle_pock_l1_hodge(topology, tau, max_iter, tol) -> L1HodgeCoreOutput:
    raise NotImplementedError(_ARCHIVED)


def solve_l1_hodge_primal_dual(topology, tau, max_iter, tol) -> L1HodgeCoreOutput:
    raise NotImplementedError(_ARCHIVED)


def solve_l1_hodge(topology, tau) -> QuotientDecomposition:
    raise NotImplementedError(_ARCHIVED)


SpectralHodgeInput = QObstructionInputDegree1


def spectral_hodge_laplacian(input_data: SpectralHodgeInput):
    """Build the finite ``l2`` degree-1 Hodge Laplacian in topology space.

    This live spectral route is proposal evidence only. It does not revive the
    archived float-based ``l1`` primal-dual functions above.
    """

    return degree1_hodge_laplacian(input_data)


def solve_spectral_hodge(
    input_data: SpectralHodgeInput,
    solver: QObstructionSolver | None = None,
) -> SolverResult[QSpectralReceipt]:
    """Solve the finite degree-1 Hodge spectrum through the canonical Q kernel."""

    return solve_degree1(solver or QObstructionSolver(), input_data)
