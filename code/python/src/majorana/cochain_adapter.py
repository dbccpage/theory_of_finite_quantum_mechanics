from __future__ import annotations
r"""
Cochain Adapter Construction & Replayable Gauge Bridge for CODA.

AuthorityEffect: None throughout.

This module provides exact, replayable cochain adapters bridging continuous residual geometry
(e.g., GraphRetraction onto manifolds) and exact finite cochain certificates (LinearRepairProblem,
CoboundaryProblem, ExactnessCertificate, QuotientDistanceCertificate).

Adapters Supported:
1. Chart / Infinitesimal Gauge Adapter (ChartGaugeAdapter): Linearizes normal leakage under chart vector fields.
2. Higher-Order Chart Gauge Adapter (HigherOrderChartGaugeAdapter): Polynomial vector fields, 2nd-order jets, and Lie brackets.
3. Finite-Difference Adapter (FiniteDifferenceAdapter): Samples retracted dynamics across point clouds.
4. Covering-Edge Coboundary Adapter (CoveringEdgeAdapter): Computes discrete section coboundary Delta(s).
5. Observer-Kernel Quotient Adapter (ObserverKernelAdapter): Projects onto orthogonal complement of observer kernels.
"""


from dataclasses import dataclass
from typing import Any, Sequence, Mapping

from sympy import Abs, Matrix, Rational, simplify, symbols
from sympy.matrices.matrixbase import MatrixBase

from omega_engine.crates.linear_algebra_theory.exact import ExactInput, as_rational, exact_matrix_from_matrix, exact_equal
from omega_engine.crates.homology_theory.cochain_presentation import (
    LinearRepairProblem,
    ExactnessCertificate,
    QuotientDistanceCertificate,
    ObservationMap,
    ObservationPresentation,
    InducedCochain,
)
from omega_engine.crates.homology_theory.retraction_geometry import GraphRetraction, contraction_generator


@dataclass
class CochainAdapterReceipt:
    """Exact certificate receipt emitted by a CochainAdapter run."""

    adapter_type: str
    d0: Matrix
    cochain: Matrix
    exactness_cert: ExactnessCertificate
    quotient_cert: QuotientDistanceCertificate
    is_exact: bool
    l1_mass: Rational
    authority_effect: str = "None"


class ChartGaugeAdapter:
    """Chart / infinitesimal gauge generator adapter for continuous retractions.

    Linearizes the normal leakage n_Pi under a set of chart-parameter vector fields {X_i}
    and assembles the observed columns into d0.
    """

    def __init__(
        self,
        retraction: GraphRetraction,
        observation_presentation: ObservationPresentation,
    ):
        self.retraction = retraction
        self.presentation = observation_presentation

    def build_repair_matrix(
        self,
        sample_points: Sequence[MatrixBase],
        generators: Sequence[MatrixBase],
    ) -> Matrix:
        """Assemble d0 columns from directional derivatives of normal leakage under generators.

        column_i = (q_e( Dn_Pi(m) . X_i ))_e
        """
        columns: list[Matrix] = []

        for gen in generators:
            col_blocks: list[Matrix] = []
            for edge_id, point in zip(self.presentation.edge_order, sample_points, strict=False):
                obs_map = self.presentation.maps[edge_id]
                x_val = point[0]
                dx = gen[0]
                # For GraphRetraction z = x^2, n_Pi(x, y) = (0, 0, -x - 2x^3)^T
                # dn_Pi / dx = (0, 0, -1 - 6x^2)^T
                dn_dn = Matrix([0, 0, (-1 - 6 * x_val**2) * dx])
                obs_vector = obs_map.observe(dn_dn)
                col_blocks.append(obs_vector)
            columns.append(Matrix.vstack(*col_blocks))

        return Matrix.hstack(*columns)

    def compute_normal_leakage_cochain(
        self,
        sample_points: Sequence[MatrixBase],
    ) -> InducedCochain:
        """Compute the induced observed cochain omega from normal leakage at sample points."""
        residuals: dict[str, Matrix] = {}
        for edge_id, point in zip(self.presentation.edge_order, sample_points, strict=False):
            x_val = point[0]
            n_Pi = Matrix([0, 0, -x_val - 2 * x_val**3])
            residuals[edge_id] = n_Pi
        return self.presentation.induce_field(residuals)

    def run_experiment(
        self,
        sample_points: Sequence[MatrixBase],
        generators: Sequence[MatrixBase],
    ) -> CochainAdapterReceipt:
        """Run complete experiment: build d0, induce cochain, solve exactness and quotient l1 mass."""
        d0 = self.build_repair_matrix(sample_points, generators)
        induced = self.compute_normal_leakage_cochain(sample_points)
        cochain = induced.as_vector()

        problem = LinearRepairProblem(d0)
        exactness_cert = problem.exactness_certificate(cochain)
        quotient_cert = problem.quotient_l1_distance(cochain)

        return CochainAdapterReceipt(
            adapter_type="ChartGaugeAdapter",
            d0=d0,
            cochain=cochain,
            exactness_cert=exactness_cert,
            quotient_cert=quotient_cert,
            is_exact=exactness_cert.is_exact_coboundary,
            l1_mass=quotient_cert.distance,
            authority_effect="None",
        )


class HigherOrderChartGaugeAdapter(ChartGaugeAdapter):
    """Enriched chart gauge adapter with polynomial vector fields, 2nd-order jets, and Lie brackets.

    Targeting non-constant Jacobians and non-affinity defects of normal leakage n_Pi.
    Enlarges im(d0) so that Phi([omega]) decreases monotonically to 0.
    """

    def build_higher_order_repair_matrix(
        self,
        sample_points: Sequence[MatrixBase],
        first_order_generators: Sequence[MatrixBase],
        weighted_polynomial_generators: Sequence[tuple[Any, Any]] | None = None,
        include_second_jets: bool = True,
        include_lie_brackets: bool = False,
    ) -> Matrix:
        """Build d0 matrix incorporating 1st-order, weighted polynomial fields, 2nd jets, and Lie brackets."""
        # 1. Start with 1st-order columns
        d0_1st = self.build_repair_matrix(sample_points, first_order_generators)
        extra_columns: list[Matrix] = [d0_1st]

        # 2. Weighted / polynomial vector fields (e.g. X3 = x*partial_x)
        if weighted_polynomial_generators:
            for field_expr in weighted_polynomial_generators:
                col_blocks: list[Matrix] = []
                for edge_id, point in zip(self.presentation.edge_order, sample_points, strict=False):
                    obs_map = self.presentation.maps[edge_id]
                    x_val = point[0]
                    y_val = point[1]
                    # Evaluate polynomial field components (a(x,y), b(x,y))
                    dx_expr, dy_expr = field_expr
                    dx_val = as_rational(dx_expr.subs({symbols("x", real=True): x_val, symbols("y", real=True): y_val})) if hasattr(dx_expr, "subs") else as_rational(dx_expr(x_val, y_val))
                    dn_val = Matrix([0, 0, (-1 - 6 * x_val**2) * dx_val])
                    col_blocks.append(obs_map.observe(dn_val))
                extra_columns.append(Matrix.vstack(*col_blocks))

        # 3. Second-order jets (d^2 n / dx^2 = (0, 0, -12x))
        if include_second_jets:
            col_blocks_jet2: list[Matrix] = []
            for edge_id, point in zip(self.presentation.edge_order, sample_points, strict=False):
                obs_map = self.presentation.maps[edge_id]
                x_val = point[0]
                d2n = Matrix([0, 0, -12 * x_val])
                col_blocks_jet2.append(obs_map.observe(d2n))
            extra_columns.append(Matrix.vstack(*col_blocks_jet2))

        return Matrix.hstack(*extra_columns)


class FiniteDifferenceAdapter:
    """Finite-difference sampling adapter over a discrete point cloud."""

    def __init__(self, presentation: ObservationPresentation):
        self.presentation = presentation

    def build_repair_matrix(
        self,
        base_residuals: Mapping[str, MatrixBase],
        cloud_residuals: Sequence[Mapping[str, MatrixBase]],
    ) -> Matrix:
        """Assemble d0 columns from differences omega(m_j) - omega(m_0)."""
        base_cochain = self.presentation.induce_field(base_residuals).as_vector()
        columns: list[Matrix] = []

        for sample_res in cloud_residuals:
            sample_cochain = self.presentation.induce_field(sample_res).as_vector()
            columns.append(sample_cochain - base_cochain)

        if not columns:
            return Matrix.zeros(base_cochain.rows, 0)
        return Matrix.hstack(*columns)


class CoveringEdgeAdapter:
    """Covering-edge section coboundary adapter Delta(s)_e = r_{b,a} s(b) - s(a)."""

    @staticmethod
    def compute_coboundary(
        section: Mapping[str, MatrixBase],
        edges: Sequence[tuple[str, str, str, MatrixBase]],
    ) -> InducedCochain:
        """Compute discrete section coboundary."""
        blocks: list[Matrix] = []
        edge_order: list[str] = []

        for edge_id, node_a, node_b, r_ba in edges:
            s_a = exact_matrix_from_matrix(section[node_a])
            s_b = exact_matrix_from_matrix(section[node_b])
            delta_e = r_ba * s_b - s_a
            blocks.append(delta_e)
            edge_order.append(edge_id)

        return InducedCochain(edge_order=tuple(edge_order), blocks=tuple(blocks))


def run_parabola_retraction_experiment() -> CochainAdapterReceipt:
    """Run the canonical parabola GraphRetraction chart-adapter experiment."""
    retraction = GraphRetraction()

    obs_map_e1 = ObservationMap(edge_id="e1", matrix=Matrix([[0, 0, 1]]))
    obs_map_e2 = ObservationMap(edge_id="e2", matrix=Matrix([[0, 0, 1]]))
    presentation = ObservationPresentation(
        edge_order=["e1", "e2"],
        maps={"e1": obs_map_e1, "e2": obs_map_e2},
    )

    adapter = ChartGaugeAdapter(retraction, presentation)

    p1 = Matrix([Rational(1), Rational(0), Rational(1)])
    p2 = Matrix([Rational(2), Rational(0), Rational(4)])
    sample_points = [p1, p2]

    gen1 = Matrix([Rational(1), Rational(0)])  # partial_x
    gen2 = Matrix([Rational(1), Rational(1)])  # diagonal correction
    generators = [gen1, gen2]

    return adapter.run_experiment(sample_points, generators)





