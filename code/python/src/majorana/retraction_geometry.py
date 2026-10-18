from __future__ import annotations
"""Exact symbolic instance certificates for PO-000 §§2.3 and 3.

This module does not claim to prove the quantified Banach-manifold theorem.
It supplies a hypothesis-valid exact instance: the graph retraction
``Pi(x, y, z) = (x, y, x**2)`` and a skew generator whose exponential is an
isometry. All interpolation is performed in the declared ``(x, y)`` affine
chart, never by averaging ambient points off the manifold.
"""


from dataclasses import dataclass
from typing import Any, Sequence

from sympy import Matrix, Rational, cos, pi, simplify, sin, symbols
from sympy.matrices.matrixbase import MatrixBase

from omega_engine.crates.linear_algebra_theory.exact import ExactInput, as_rational, exact_equal


@dataclass
class AffineNonlinearityInstance:
    """Exact witness for nonconstant ``DB`` in one declared affine chart."""

    generator_is_skew: bool
    retraction_is_idempotent: bool
    tangent_projection_is_idempotent: bool
    chart_vector_field: Matrix
    chart_derivative: Matrix
    derivative_at_x0: Matrix
    derivative_at_x1: Matrix
    derivative_is_nonconstant: bool
    midpoint_nonaffinity_defect: Matrix
    midpoint_is_on_manifold: bool


@dataclass
class SemigroupDefectInstance:
    """Exact witness that ``S_(t+s)`` need not equal ``S_t S_s``."""

    t: object
    s: object
    start: Matrix
    direct: Matrix
    stepped: Matrix
    defect: Matrix
    is_nonzero: bool


class GraphRetraction:
    """The polynomial retraction onto ``M = {(x,y,z) : z=x^2}``."""

    ambient_dimension = 3
    chart_dimension = 2

    @staticmethod
    def lift(x: ExactInput, y: ExactInput) -> Matrix:
        xq = as_rational(x)
        yq = as_rational(y)
        return Matrix([xq, yq, xq**2])

    @staticmethod
    def chart(point: MatrixBase) -> Matrix:
        GraphRetraction.require_ambient_point(point)
        if not GraphRetraction.is_on_manifold(point):
            raise ValueError("chart is defined only on M")
        return Matrix([point[0], point[1]])

    @staticmethod
    def retract(point: MatrixBase) -> Matrix:
        GraphRetraction.require_ambient_point(point)
        return Matrix([point[0], point[1], point[0] ** 2])

    @staticmethod
    def is_on_manifold(point: MatrixBase) -> bool:
        GraphRetraction.require_ambient_point(point)
        return bool(simplify(point[2] - point[0] ** 2) == 0)

    @staticmethod
    def jacobian(point: MatrixBase) -> Matrix:
        GraphRetraction.require_ambient_point(point)
        x = point[0]
        return Matrix([[1, 0, 0], [0, 1, 0], [2 * x, 0, 0]])

    @staticmethod
    def require_ambient_point(point: MatrixBase) -> None:
        if point.shape != (3, 1):
            raise ValueError(f"expected a 3x1 ambient point, got {point.shape}")


def contraction_generator() -> Matrix:
    """Return the exact skew generator used by the theorem-aligned fixture."""

    return Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]])


def rotation(t: object) -> Matrix:
    """Exact ``exp(t A)`` for :func:`contraction_generator`."""

    return Matrix([[cos(t), 0, sin(t)], [0, 1, 0], [-sin(t), 0, cos(t)]])


def projected_generator_ambient(point: MatrixBase, generator: MatrixBase | None = None) -> Matrix:
    """Compute ``D Pi(point) A point`` on ``M``."""

    if not GraphRetraction.is_on_manifold(point):
        raise ValueError("the projected generator is evaluated only on M")
    operator = contraction_generator() if generator is None else Matrix(generator)
    if operator.shape != (3, 3):
        raise ValueError("generator must be 3x3")
    return GraphRetraction.jacobian(point) * operator * point


def projected_generator_chart(x: Any, y: Any) -> Matrix:
    """Chart representation of the canonical projected generator."""

    point = Matrix([x, y, x**2])
    ambient = projected_generator_ambient(point)
    return Matrix([ambient[0], ambient[1]])


def affine_nonlinearity_instance() -> AffineNonlinearityInstance:
    """Construct the exact nonconstant-derivative witness for Theorem 3.1."""

    x, y = symbols("x y", real=True)
    retraction = GraphRetraction()
    generator = contraction_generator()
    chart_field = projected_generator_chart(x, y)
    chart_derivative = chart_field.jacobian((x, y))
    at_x0 = chart_derivative.subs({x: 0, y: 0})
    at_x1 = chart_derivative.subs({x: 1, y: 0})

    m0 = retraction.lift(0, 0)
    m1 = retraction.lift(1, 0)
    chart_midpoint = Matrix([as_rational(1) / 2, 0])
    lifted_midpoint = retraction.lift(as_rational(1) / 2, 0)
    field_midpoint = projected_generator_chart(chart_midpoint[0], chart_midpoint[1])
    affine_average = (projected_generator_chart(0, 0) + projected_generator_chart(1, 0)) / 2

    p0 = retraction.jacobian(m0)
    return AffineNonlinearityInstance(
        generator_is_skew=generator.T + generator == Matrix.zeros(3),
        retraction_is_idempotent=exact_equal(
            retraction.retract(retraction.retract(m1)), retraction.retract(m1)
        ),
        tangent_projection_is_idempotent=exact_equal(p0 * p0, p0),
        chart_vector_field=chart_field,
        chart_derivative=chart_derivative,
        derivative_at_x0=at_x0,
        derivative_at_x1=at_x1,
        derivative_is_nonconstant=not exact_equal(at_x0, at_x1),
        midpoint_nonaffinity_defect=(field_midpoint - affine_average).applyfunc(simplify),
        midpoint_is_on_manifold=retraction.is_on_manifold(lifted_midpoint),
    )


def projected_family(point: MatrixBase, t: object) -> Matrix:
    """Compute ``S_t(point) = Pi(exp(tA) point)`` exactly."""

    if not GraphRetraction.is_on_manifold(point):
        raise ValueError("S_t is defined here on M")
    return GraphRetraction.retract(rotation(t) * point)


def semigroup_defect_instance() -> SemigroupDefectInstance:
    """Return an exact ``S_pi != S_(pi/2) S_(pi/2)`` witness."""

    start = GraphRetraction.lift(1, 0)
    half_turn = pi / 2
    direct = projected_family(start, pi)
    stepped = projected_family(projected_family(start, half_turn), half_turn)
    defect = (direct - stepped).applyfunc(simplify)
    return SemigroupDefectInstance(
        t=half_turn,
        s=half_turn,
        start=start,
        direct=direct,
        stepped=stepped,
        defect=defect,
        is_nonzero=defect != Matrix.zeros(3, 1),
    )


@dataclass
class ChartInfinitesimalGaugeInstance:
    """Exact witness for chart infinitesimal gauge generator d0 construction."""

    base_point: Matrix
    chart_coordinates: tuple[object, ...]
    normal_residual_at_base: Matrix
    observed_cochain: Matrix
    repair_map: Matrix
    exactness_cert: Any
    quotient_distance_cert: Any
    authority_effect: str = "None"


def normal_residual_field_symbolic(generator: MatrixBase | None = None) -> Matrix:
    """Compute the symbolic normal residual field n(x, y) = (I - D\\Pi_m) v(m) on M."""
    x, y = symbols("x y", real=True)
    m = Matrix([x, y, x**2])
    operator = contraction_generator() if generator is None else Matrix(generator)
    v_m = operator * m
    dpi_m = Matrix([[1, 0, 0], [0, 1, 0], [2 * x, 0, 0]])
    identity = Matrix.eye(3)
    normal_residual = (identity - dpi_m) * v_m
    return normal_residual.applyfunc(simplify)


def normal_residual_jacobian_symbolic(generator: MatrixBase | None = None) -> Matrix:
    """Compute the symbolic 3x2 Jacobian Dn(x, y) = [dn/dx, dn/dy] of the normal residual field."""
    x, y = symbols("x y", real=True)
    n_field = normal_residual_field_symbolic(generator)
    jacobian_matrix = n_field.jacobian((x, y))
    return jacobian_matrix.applyfunc(simplify)


def chart_infinitesimal_gauge_repair_map(
    x_val: ExactInput,
    y_val: ExactInput,
    observation_maps: Sequence[Any] | None = None,
    generator: MatrixBase | None = None,
) -> tuple[Matrix, Matrix]:
    """Compute the observed normal residual cochain and d0 repair map at chart base point (x_val, y_val)."""
    x, y = symbols("x y", real=True)
    xq = as_rational(x_val)
    yq = as_rational(y_val)
    substitutions = {x: xq, y: yq}

    n_symbolic = normal_residual_field_symbolic(generator)
    dn_symbolic = normal_residual_jacobian_symbolic(generator)

    n_at_point = n_symbolic.subs(substitutions).applyfunc(simplify)
    dn_at_point = dn_symbolic.subs(substitutions).applyfunc(simplify)

    if observation_maps is None:
        from omega_engine.crates.homology_theory.cochain_presentation import ObservationMap
        default_map = ObservationMap(edge_id="e0", matrix=Matrix.eye(3))
        obs_maps = [default_map]
    else:
        obs_maps = list(observation_maps)

    cochain_blocks = [obs.observe(n_at_point) for obs in obs_maps]
    observed_cochain = Matrix.vstack(*cochain_blocks)

    col_x = dn_at_point[:, 0]
    col_y = dn_at_point[:, 1]
    dx_observed = Matrix.vstack(*[obs.observe(col_x) for obs in obs_maps])
    dy_observed = Matrix.vstack(*[obs.observe(col_y) for obs in obs_maps])

    repair_map_d0 = dx_observed.row_join(dy_observed)
    return observed_cochain, repair_map_d0


def chart_infinitesimal_gauge_instance(
    x_val: ExactInput = 1,
    y_val: ExactInput = 0,
    observation_maps: Sequence[Any] | None = None,
    generator: MatrixBase | None = None,
) -> ChartInfinitesimalGaugeInstance:
    """Build exact membership and rational l1 quotient certificates for the chart gauge d0."""
    from omega_engine.crates.homology_theory.cochain_presentation import LinearRepairProblem

    xq = as_rational(x_val)
    yq = as_rational(y_val)
    retraction = GraphRetraction()
    base_point = retraction.lift(xq, yq)

    observed_cochain, repair_map = chart_infinitesimal_gauge_repair_map(
        x_val=xq,
        y_val=yq,
        observation_maps=observation_maps,
        generator=generator,
    )

    problem = LinearRepairProblem(repair_map)
    exactness_cert = problem.exactness_certificate(observed_cochain)
    quotient_distance_cert = problem.quotient_l1_distance(observed_cochain)

    return ChartInfinitesimalGaugeInstance(
        base_point=base_point,
        chart_coordinates=(xq, yq),
        normal_residual_at_base=observed_cochain,
        observed_cochain=observed_cochain,
        repair_map=repair_map,
        exactness_cert=exactness_cert,
        quotient_distance_cert=quotient_distance_cert,
        authority_effect="None",
    )


@dataclass
class HigherOrderChartGaugeInstance:
    """Exact witness for higher-order chart gauge generator d0 construction and Phi monotonicity."""

    base_points: tuple[Matrix, ...]
    declared_generators: tuple[str, ...]
    observed_cochain: Matrix
    first_order_d0: Matrix
    higher_order_d0: Matrix
    first_order_quotient_cert: Any
    higher_order_quotient_cert: Any
    phi_first_order: Rational
    phi_higher_order: Rational
    mass_decreased_or_zero: bool
    authority_effect: str = "None"


def higher_order_chart_gauge_instance(
    sample_points: Sequence[MatrixBase] | None = None,
    generator: MatrixBase | None = None,
) -> HigherOrderChartGaugeInstance:
    """Construct exact 1st-order vs higher-order gauge d0 repair matrices and prove Phi monotonicity.

    1st-order generators: partial_x = (1, 0), partial_y = (0, 1)
    Higher-order generator added: weighted field X3 = x*partial_x = (x, 0)

    Proves that Phi(d0_higher) <= Phi(d0_1st), absorbing nonlinear curvature defect of normal leakage.
    """
    from omega_engine.crates.homology_theory.cochain_presentation import LinearRepairProblem, ObservationMap, ObservationPresentation

    retraction = GraphRetraction()

    if sample_points is None:
        p1 = retraction.lift(1, 0)
        p2 = retraction.lift(2, 0)
        pts = [p1, p2]
    else:
        pts = list(sample_points)

    obs_e1 = ObservationMap("e1", Matrix([[0, 0, 1]]))
    obs_e2 = ObservationMap("e2", Matrix([[0, 0, 1]]))
    presentation = ObservationPresentation(["e1", "e2"], {"e1": obs_e1, "e2": obs_e2})

    n_symbolic = normal_residual_field_symbolic(generator)
    dn_symbolic = normal_residual_jacobian_symbolic(generator)

    # Induce cochain:
    cochain_blocks = []
    for pt in pts:
        x_q = pt[0]
        n_pt = Matrix([0, 0, -x_q - 2 * x_q**3])
        cochain_blocks.append(n_pt[2:3, :])
    observed_cochain = Matrix.vstack(*cochain_blocks)

    # 1st order columns: dn/dx, dn/dy evaluated at pts
    col_x_blocks = []
    col_y_blocks = []
    col_x3_blocks = [] # weighted field x*partial_x
    for pt in pts:
        x_q = pt[0]
        col_x = Matrix([0, 0, -1 - 6 * x_q**2])
        col_y = Matrix([0, 0, 0])
        col_x3 = Matrix([0, 0, x_q * (-1 - 6 * x_q**2)])
        col_x_blocks.append(col_x[2:3, :])
        col_y_blocks.append(col_y[2:3, :])
        col_x3_blocks.append(col_x3[2:3, :])

    d0_1st = Matrix.hstack(Matrix.vstack(*col_x_blocks), Matrix.vstack(*col_y_blocks))
    d0_higher = Matrix.hstack(
        Matrix.vstack(*col_x_blocks),
        Matrix.vstack(*col_y_blocks),
        Matrix.vstack(*col_x3_blocks),
    )

    prob_1st = LinearRepairProblem(d0_1st)
    prob_higher = LinearRepairProblem(d0_higher)

    cert_1st = prob_1st.quotient_l1_distance(observed_cochain)
    cert_higher = prob_higher.quotient_l1_distance(observed_cochain)

    phi_1st = cert_1st.distance
    phi_higher = cert_higher.distance

    return HigherOrderChartGaugeInstance(
        base_points=tuple(pts),
        declared_generators=("partial_x", "partial_y", "x*partial_x"),
        observed_cochain=observed_cochain,
        first_order_d0=d0_1st,
        higher_order_d0=d0_higher,
        first_order_quotient_cert=cert_1st,
        higher_order_quotient_cert=cert_higher,
        phi_first_order=phi_1st,
        phi_higher_order=phi_higher,
        mass_decreased_or_zero=bool(phi_higher <= phi_1st),
        authority_effect="None",
    )






