"""Exact symbolic instance certificates for PO-000 §§2.3 and 3.

This module does not claim to prove the quantified Banach-manifold theorem.
It supplies a hypothesis-valid exact instance: the graph retraction
``Pi(x, y, z) = (x, y, x**2)`` and a skew generator whose exponential is an
isometry. All interpolation is performed in the declared ``(x, y)`` affine
chart, never by averaging ambient points off the manifold.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from exactsym import Matrix, MatrixBase, Rational, cos, pi, simplify, sin, symbols

from exact import ExactInput, as_rational, exact_equal


@dataclass(frozen=True)
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


@dataclass(frozen=True)
class AffineChartTransferWitness:
    """Finite witness for Lemma 3.3, Remark 3.3.1, Example 3.3, and Proposition 3.C.

    The boolean flags are exact identities in the displayed models. They do not
    prove the Banach-space lemma and do not close S1 for curved embeddings.
    """

    positive_db_at_zero: Matrix
    positive_db_at_one: Matrix
    positive_db_nonconstant: bool
    positive_derivative_matches_tangent_restriction: bool
    positive_curvature_nonzero: bool
    negative_chart_derivative_constant: bool
    negative_b_is_affine: bool
    negative_ambient_at_zero: Matrix
    negative_ambient_at_one: Matrix
    negative_ambient_derivative_nonconstant: bool
    negative_curvature_nonzero: bool
    tangent_restriction_necessary: bool
    retractions_are_idempotent: bool


@dataclass(frozen=True)
class VerticalGraphChartWitness:
    """Finite checks of Lemma 3.4 on one vertical graph, not the Banach-space proof.

    The flags do not cover a retraction that moves the chart coordinate or a
    submanifold that is not presented as a graph of a fixed splitting.
    """

    cancellation_db_constant: bool
    cancellation_identity_matches: bool
    noncancellation_db_matches_formula: bool
    noncancellation_values_distinct: bool
    noncancellation_difference_matches: bool
    dissipative_identity: bool
    retraction_is_idempotent: bool
    db_at_zero: Matrix
    db_at_one: Matrix
    difference: Matrix


@dataclass(frozen=True)
class ShearedGraphChartWitness:
    """Finite checks of Lemma 3.5 for the unit shear on the parabola.

    The flags do not prove the Banach-space lemma. They do not cover a
    nonlinear fiber displacement or a submanifold that is not a graph.
    """

    chart_field_matches_shear_formula: bool
    db_matches_derivative_formula: bool
    db_values_distinct: bool
    vertical_db_constant: bool
    retraction_moves_chart_coordinate: bool
    dissipative_identity: bool
    retraction_is_idempotent: bool
    db_at_zero: Matrix
    db_at_one: Matrix
    off_graph_chart: Matrix
    off_graph_image: Matrix


@dataclass(frozen=True)
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


def chart_transfer_witness() -> AffineChartTransferWitness:
    """Replay the §3.3 flat transfer, its normal-direction remark, and the curved counterexample."""

    x, y = symbols("x y", real=True)
    zero = Rational(0)
    one = Rational(1)

    positive_generator = Matrix([-x, x - y])
    positive_retracted = Matrix(
        [
            positive_generator[0] * (one + y) + x * positive_generator[1],
            zero,
        ]
    )
    positive_field = Matrix([x**2 - x - 2 * x * y, zero])
    positive_field_matches = exact_equal(positive_retracted, positive_field)
    on_axis = positive_field.subs({y: zero})
    positive_db = Matrix([on_axis[0]]).jacobian((x,))
    positive_db_at_zero = positive_db.subs({x: zero})
    positive_db_at_one = positive_db.subs({x: one})
    tangent_derivative = on_axis.jacobian((x,))
    derivative_matches = exact_equal(
        tangent_derivative[0, 0], positive_db[0, 0]
    ) and exact_equal(tangent_derivative[1, 0], zero)
    # D^2 Pi(u,v)=(u_1 v_2+u_2 v_1, 0). At m=(1,0), Am=(-1,1) and v=(1,0).
    positive_curvature = Matrix(
        [Rational(-1) * zero + one * one, zero]
    )

    negative_generator = Matrix([-x, zero])
    negative_retracted = Matrix(
        [negative_generator[0], 2 * x * negative_generator[0]]
    )
    negative_field = Matrix([-x, -2 * x**2])
    negative_field_matches = exact_equal(negative_retracted, negative_field)
    negative_db = Matrix([-x]).jacobian((x,))
    negative_db_at_zero = negative_db.subs({x: zero})
    negative_db_at_one = negative_db.subs({x: one})
    negative_jacobian = negative_field.jacobian((x, y))
    direction = Matrix([one, zero])
    negative_ambient_at_zero = negative_jacobian.subs({x: zero, y: zero}) * direction
    negative_ambient_at_one = negative_jacobian.subs({x: one, y: one}) * direction
    half = Rational(1, 2)
    negative_b = Matrix([-x])
    negative_midpoint = negative_b.subs({x: half})
    negative_average = (negative_b.subs({x: zero}) + negative_b.subs({x: one})) / 2
    # D^2 Pi(u,v)=(0, 2 v_1 u_1). At s=1, Am=(-1,0) and v=(1,0).
    negative_curvature = Matrix([zero, 2 * one * Rational(-1)])

    remark_field = Matrix([-x - 2 * x * y, zero])
    remark_jacobian = remark_field.subs({y: zero}).jacobian((x,))
    remark_db = Matrix([-x]).jacobian((x,))
    normal = Matrix([zero, one])
    remark_full = remark_field.jacobian((x, y))
    normal_at_zero = remark_full.subs({x: zero, y: zero}) * normal
    normal_at_one = remark_full.subs({x: one, y: zero}) * normal
    tangent_at_zero = remark_full.subs({x: zero, y: zero}) * direction
    tangent_at_one = remark_full.subs({x: one, y: zero}) * direction

    def positive_pi(px, py):
        return Matrix([px * (one + py), zero])

    def negative_pi(px):
        return Matrix([px, px**2])

    positive_once = positive_pi(Rational(3), Rational(4))
    positive_twice = positive_pi(positive_once[0], positive_once[1])
    negative_once = negative_pi(Rational(3))
    negative_twice = negative_pi(negative_once[0])

    return AffineChartTransferWitness(
        positive_db_at_zero=positive_db_at_zero,
        positive_db_at_one=positive_db_at_one,
        positive_db_nonconstant=(
            exact_equal(positive_db_at_zero, Matrix([[Rational(-1)]]))
            and exact_equal(positive_db_at_one, Matrix([[one]]))
            and not exact_equal(positive_db_at_zero, positive_db_at_one)
        ),
        positive_derivative_matches_tangent_restriction=(
            derivative_matches and positive_field_matches
        ),
        positive_curvature_nonzero=exact_equal(positive_curvature, Matrix([one, zero])),
        negative_chart_derivative_constant=(
            exact_equal(negative_db_at_zero, Matrix([[Rational(-1)]]))
            and exact_equal(negative_db_at_zero, negative_db_at_one)
        ),
        negative_b_is_affine=exact_equal(negative_midpoint, negative_average),
        negative_ambient_at_zero=negative_ambient_at_zero,
        negative_ambient_at_one=negative_ambient_at_one,
        negative_ambient_derivative_nonconstant=(
            negative_field_matches
            and not exact_equal(negative_ambient_at_zero, negative_ambient_at_one)
        ),
        negative_curvature_nonzero=exact_equal(negative_curvature, Matrix([zero, Rational(-2)])),
        tangent_restriction_necessary=(
            exact_equal(remark_db.subs({x: zero}), Matrix([[Rational(-1)]]))
            and exact_equal(remark_jacobian.subs({x: zero}), Matrix([Rational(-1), zero]))
            and exact_equal(remark_jacobian.subs({x: one}), Matrix([Rational(-1), zero]))
            and exact_equal(tangent_at_zero, tangent_at_one)
            and not exact_equal(normal_at_zero, normal_at_one)
        ),
        retractions_are_idempotent=(
            exact_equal(positive_once, positive_twice)
            and exact_equal(positive_once, Matrix([Rational(15), zero]))
            and exact_equal(negative_once, negative_twice)
            and exact_equal(negative_once, Matrix([Rational(3), Rational(9)]))
        ),
    )


def vertical_graph_chart_witness() -> VerticalGraphChartWitness:
    """Replay Lemma 3.4 on f(s)=s^2 with the cancellation and noncancellation generators."""

    s, h, x, y = symbols("s h x y", real=True)
    zero = Rational(0)
    one = Rational(1)
    two = Rational(2)

    def vertical_pi(px, py):
        return Matrix([px, px**2])

    a_cancel = Matrix([[Rational(-1), zero], [zero, zero]])
    cancel_point = Matrix([s, s**2])
    cancel_b = Matrix([(a_cancel * cancel_point)[0]])
    cancel_db = cancel_b.jacobian((s,))
    cancel_increment = Matrix([h, two * s * h])
    cancel_image = a_cancel * cancel_increment
    cancel_at_zero = cancel_db.subs({s: zero})
    cancel_at_one = cancel_db.subs({s: one})

    a_non = Matrix([[Rational(-1), Rational(-1)], [zero, Rational(-1)]])
    non_point = Matrix([s, s**2])
    non_b = Matrix([(a_non * non_point)[0]])
    non_db = non_b.jacobian((s,))
    non_increment = Matrix([h, two * s * h])
    non_image = a_non * non_increment
    db_at_zero = non_db.subs({s: zero})
    db_at_one = non_db.subs({s: one})
    difference = db_at_one - db_at_zero
    curvature_increment = Matrix([zero, two])
    curvature_image = a_non * curvature_increment

    generator_image = a_non * Matrix([x, y])
    quadratic_form = generator_image[0] * x + generator_image[1] * y
    rewritten = -((x + y / 2) ** 2) - (Rational(3, 4) * y**2)

    once = vertical_pi(Rational(3), Rational(5))
    twice = vertical_pi(once[0], once[1])

    return VerticalGraphChartWitness(
        cancellation_db_constant=(
            exact_equal(cancel_at_zero, Matrix([[Rational(-1)]]))
            and exact_equal(cancel_at_zero, cancel_at_one)
        ),
        cancellation_identity_matches=(
            exact_equal(Matrix([[cancel_image[0]]]), Matrix([[-h]]))
            and exact_equal(Matrix([[cancel_image[1]]]), Matrix([[zero]]))
            and exact_equal(Matrix([[cancel_image[0]]]), Matrix([[cancel_db[0, 0] * h]]))
        ),
        noncancellation_db_matches_formula=(
            exact_equal(non_db, Matrix([[-(one + two * s)]]))
            and exact_equal(non_b, Matrix([-(s + s**2)]))
            and exact_equal(Matrix([[non_image[0]]]), Matrix([[non_db[0, 0] * h]]))
        ),
        noncancellation_values_distinct=(
            exact_equal(db_at_zero, Matrix([[Rational(-1)]]))
            and exact_equal(db_at_one, Matrix([[Rational(-3)]]))
            and not exact_equal(db_at_zero, db_at_one)
        ),
        noncancellation_difference_matches=(
            exact_equal(difference, Matrix([[Rational(-2)]]))
            and exact_equal(Matrix([[curvature_image[0]]]), difference)
        ),
        dissipative_identity=(
            exact_equal(quadratic_form, -x**2 - x * y - y**2)
            and exact_equal(quadratic_form, rewritten)
        ),
        retraction_is_idempotent=(
            exact_equal(once, twice)
            and exact_equal(once, Matrix([Rational(3), Rational(9)]))
        ),
        db_at_zero=db_at_zero,
        db_at_one=db_at_one,
        difference=difference,
    )


def sheared_graph_chart_witness() -> ShearedGraphChartWitness:
    """Replay Lemma 3.5 at shear 1 on f(s)=s^2 with A(x,y)=(-x,0)."""

    s, h, x, y, px, py = symbols("s h x y px py", real=True)
    zero = Rational(0)
    one = Rational(1)
    two = Rational(2)

    def shear_pi(point_x, point_y):
        base = point_x + (point_y - point_x**2)
        return Matrix([base, base**2])

    def vertical_pi(point_x, point_y):
        return Matrix([point_x, point_x**2])

    generator = Matrix([[Rational(-1), zero], [zero, zero]])
    generator_on_graph = generator * Matrix([s, s**2])
    shear_jacobian = shear_pi(px, py).jacobian((px, py)).subs({px: s, py: s**2})
    vertical_jacobian = vertical_pi(px, py).jacobian((px, py)).subs({px: s, py: s**2})
    chart_field = Matrix([(shear_jacobian * generator_on_graph)[0]])
    vertical_field = Matrix([(vertical_jacobian * generator_on_graph)[0]])
    chart_derivative = chart_field.jacobian((s,))
    vertical_derivative = vertical_field.jacobian((s,))
    alpha = -s
    q_factor = one - two * s
    formula_field = Matrix([q_factor * alpha])
    tangent = Matrix([h, two * s * h])
    tangent_image = generator * tangent
    derivative_formula = (-two * h * alpha) + q_factor * tangent_image[0]
    db_at_zero = chart_derivative.subs({s: zero})
    db_at_one = chart_derivative.subs({s: one})
    generator_image = generator * Matrix([x, y])
    quadratic_form = generator_image[0] * x + generator_image[1] * y
    off_graph_chart = Matrix([[Rational(3)]])
    once = shear_pi(Rational(3), Rational(5))
    twice = shear_pi(once[0], once[1])
    off_graph_image = Matrix([[once[0]]])
    on_graph = shear_pi(s, s**2)

    return ShearedGraphChartWitness(
        chart_field_matches_shear_formula=(
            exact_equal(chart_field, formula_field)
            and exact_equal(chart_field, Matrix([-s + two * s**2]))
        ),
        db_matches_derivative_formula=(
            exact_equal(Matrix([[chart_derivative[0, 0] * h]]), Matrix([[derivative_formula]]))
            and exact_equal(chart_derivative, Matrix([[-one + Rational(4) * s]]))
        ),
        db_values_distinct=(
            exact_equal(db_at_zero, Matrix([[Rational(-1)]]))
            and exact_equal(db_at_one, Matrix([[Rational(3)]]))
            and not exact_equal(db_at_zero, db_at_one)
        ),
        vertical_db_constant=(
            exact_equal(vertical_field, Matrix([-s]))
            and exact_equal(vertical_derivative, Matrix([[Rational(-1)]]))
            and not exact_equal(vertical_derivative, chart_derivative)
        ),
        retraction_moves_chart_coordinate=(
            not exact_equal(off_graph_image, off_graph_chart)
            and exact_equal(off_graph_image, Matrix([[Rational(-1)]]))
            and exact_equal(on_graph, Matrix([s, s**2]))
        ),
        dissipative_identity=(
            exact_equal(generator_image, Matrix([-x, zero]))
            and exact_equal(quadratic_form, -x**2)
        ),
        retraction_is_idempotent=(
            exact_equal(once, twice)
            and exact_equal(once, Matrix([Rational(-1), one]))
            and exact_equal(Matrix([[once[1]]]), Matrix([[once[0] ** 2]]))
        ),
        db_at_zero=db_at_zero,
        db_at_one=db_at_one,
        off_graph_chart=off_graph_chart,
        off_graph_image=off_graph_image,
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
