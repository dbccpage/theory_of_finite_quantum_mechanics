"""Unit tests for Chart Infinitesimal Gauge Generators (d0 repair map construction)."""

from sympy import Matrix, Rational, symbols

from omega_engine.crates.homology_theory.cochain_presentation import ObservationMap
from omega_engine.crates.homology_theory.retraction_geometry import (
    chart_infinitesimal_gauge_instance,
    chart_infinitesimal_gauge_repair_map,
    normal_residual_field_symbolic,
    normal_residual_jacobian_symbolic,
)


def test_normal_residual_symbolic_formulas() -> None:
    """Verify exact symbolic form of normal residual field n(x,y) and its Jacobian Dn(x,y)."""
    x, y = symbols("x y", real=True)
    n_symbolic = normal_residual_field_symbolic()
    dn_symbolic = normal_residual_jacobian_symbolic()

    # n(x, y) = [0, 0, -x - 2*x^3]^T
    assert n_symbolic[0] == 0
    assert n_symbolic[1] == 0
    assert n_symbolic[2] == -x - 2 * x**3

    # Dn(x, y) = [[0, 0], [0, 0], [-1 - 6*x^2, 0]]
    assert dn_symbolic[0, 0] == 0
    assert dn_symbolic[0, 1] == 0
    assert dn_symbolic[1, 0] == 0
    assert dn_symbolic[1, 1] == 0
    assert dn_symbolic[2, 0] == -1 - 6 * x**2
    assert dn_symbolic[2, 1] == 0


def test_chart_infinitesimal_gauge_at_base_point_one_zero() -> None:
    """Verify evaluation at base point m = (1, 0, 1) and exactness certificate."""
    cochain, repair_map = chart_infinitesimal_gauge_repair_map(1, 0)

    # Cochain: n(1, 0) = [0, 0, -3]^T
    assert cochain == Matrix([0, 0, -3])

    # Repair map d0: Dn(1, 0) = [[0, 0], [0, 0], [-7, 0]]
    assert repair_map == Matrix([[0, 0], [0, 0], [-7, 0]])

    instance = chart_infinitesimal_gauge_instance(1, 0)
    assert instance.base_point == Matrix([1, 0, 1])
    assert instance.authority_effect == "None"

    # Verify exactness certificate (cochain is in im(d0))
    assert instance.exactness_cert.is_exact_coboundary is True
    assert instance.exactness_cert.verify() is True
    assert instance.exactness_cert.witness == Matrix([Rational(3, 7), 0])

    # Verify quotient distance certificate (distance is 0)
    assert instance.quotient_distance_cert.distance == 0
    assert instance.quotient_distance_cert.verify() is True


def test_chart_infinitesimal_gauge_multi_edge_observation() -> None:
    """Verify multi-edge observation presentation for chart gauge generators."""
    obs1 = ObservationMap(edge_id="e0", matrix=Matrix.eye(3))
    obs2 = ObservationMap(edge_id="e1", matrix=Matrix([[1, 0, 0], [0, 1, 0]]))

    cochain, repair_map = chart_infinitesimal_gauge_repair_map(
        1, 0, observation_maps=[obs1, obs2]
    )

    # 3D block from e0 + 2D block from e1 = 5 rows
    assert cochain.shape == (5, 1)
    assert repair_map.shape == (5, 2)

    instance = chart_infinitesimal_gauge_instance(
        1, 0, observation_maps=[obs1, obs2]
    )
    assert instance.exactness_cert.verify() is True
    assert instance.quotient_distance_cert.verify() is True


def test_chart_infinitesimal_gauge_irreducible_obstruction() -> None:
    """Verify that adding an orthogonal component produces non-zero quotient distance and dual witness."""
    obs_id = ObservationMap(edge_id="e0", matrix=Matrix.eye(3))
    instance = chart_infinitesimal_gauge_instance(1, 0, observation_maps=[obs_id])

    # Modify cochain to include an un-cancellable y-residual [0, 5, -3]^T
    unrepairable_cochain = Matrix([0, 5, -3])
    from omega_engine.crates.homology_theory.cochain_presentation import LinearRepairProblem

    problem = LinearRepairProblem(instance.repair_map)
    exactness = problem.exactness_certificate(unrepairable_cochain)
    quotient = problem.quotient_l1_distance(unrepairable_cochain)

    assert exactness.is_exact_coboundary is False
    assert exactness.verify() is True
    assert exactness.separating_left_kernel_vector is not None

    assert quotient.distance == 5
    assert quotient.verify() is True


