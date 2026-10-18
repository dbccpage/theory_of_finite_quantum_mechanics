r"""
Unit Test Suite for CODA Cochain Adapter Constructions & Replayable Gauge Bridge.

AuthorityEffect: None throughout.

Tests:
1. ChartGaugeAdapter on GraphRetraction parabola z = x^2 (parabola retraction experiment)
2. HigherOrderChartGaugeAdapter (weighted polynomial fields, 2nd-order jets, Lie brackets)
3. Monotonicity of rational l1 quotient mass: Phi(d0_higher) <= Phi(d0_1st)
4. FiniteDifferenceAdapter sampling over point clouds
5. CoveringEdgeAdapter discrete section coboundary Delta(s)
"""

import sys
from pathlib import Path
from sympy import Matrix, Rational, symbols
import pytest

# Ensure coda is accessible
coda_dir = Path(__file__).resolve().parents[1] / "coda"
ooutwire_dir = Path(__file__).resolve().parents[2]

for p in [str(coda_dir), str(ooutwire_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from omega_engine.crates.homology_theory.cochain_adapter import (
    ChartGaugeAdapter,
    HigherOrderChartGaugeAdapter,
    FiniteDifferenceAdapter,
    CoveringEdgeAdapter,
    run_parabola_retraction_experiment,
)
from omega_engine.crates.homology_theory.cochain_presentation import (
    ObservationMap,
    ObservationPresentation,
    LinearRepairProblem,
)
from omega_engine.crates.homology_theory.retraction_geometry import (
    GraphRetraction,
    higher_order_chart_gauge_instance,
)


def test_parabola_retraction_experiment():
    """Test the canonical parabola GraphRetraction chart-adapter experiment."""
    receipt = run_parabola_retraction_experiment()

    assert receipt.adapter_type == "ChartGaugeAdapter"
    assert receipt.authority_effect == "None"
    assert receipt.d0.shape == (2, 2)
    assert receipt.cochain.shape == (2, 1)

    # Cochain values for x1=1 and x2=2: -1 - 2(1) = -3, -2 - 2(8) = -18
    assert receipt.cochain[0, 0] == Rational(-3)
    assert receipt.cochain[1, 0] == Rational(-18)

    # Certificates must recheck cleanly
    assert receipt.exactness_cert.verify()
    assert receipt.quotient_cert.verify()
    assert receipt.l1_mass >= 0


def test_higher_order_chart_gauge_adapter_and_phi_monotonicity():
    """Test HigherOrderChartGaugeAdapter and prove Phi monotonicity (Phi_higher <= Phi_1st)."""
    retraction = GraphRetraction()

    obs_map_e1 = ObservationMap(edge_id="e1", matrix=Matrix([[0, 0, 1]]))
    obs_map_e2 = ObservationMap(edge_id="e2", matrix=Matrix([[0, 0, 1]]))
    presentation = ObservationPresentation(
        edge_order=["e1", "e2"],
        maps={"e1": obs_map_e1, "e2": obs_map_e2},
    )

    adapter = HigherOrderChartGaugeAdapter(retraction, presentation)

    p1 = Matrix([Rational(1), Rational(0), Rational(1)])
    p2 = Matrix([Rational(2), Rational(0), Rational(4)])
    sample_points = [p1, p2]

    gen1 = Matrix([Rational(1), Rational(0)])  # partial_x
    gen2 = Matrix([Rational(0), Rational(1)])  # partial_y
    first_order_generators = [gen1, gen2]

    # Build 1st-order repair matrix
    d0_1st = adapter.build_repair_matrix(sample_points, first_order_generators)

    # Build higher-order repair matrix with weighted field X3 = x*partial_x
    x_sym, y_sym = symbols("x y", real=True)
    weighted_fields = [(x_sym, Rational(0))]  # (x, 0)
    d0_higher = adapter.build_higher_order_repair_matrix(
        sample_points,
        first_order_generators,
        weighted_polynomial_generators=weighted_fields,
        include_second_jets=True,
    )

    cochain = adapter.compute_normal_leakage_cochain(sample_points).as_vector()

    prob_1st = LinearRepairProblem(d0_1st)
    prob_higher = LinearRepairProblem(d0_higher)

    cert_1st = prob_1st.quotient_l1_distance(cochain)
    cert_higher = prob_higher.quotient_l1_distance(cochain)

    phi_1st = cert_1st.distance
    phi_higher = cert_higher.distance

    # Prove monotonicity: higher order captures curvature, driving Phi to 0
    assert phi_1st > 0
    assert phi_higher <= phi_1st
    assert phi_higher == Rational(0)


def test_higher_order_chart_gauge_instance_fixture():
    """Test higher_order_chart_gauge_instance witness from retraction_geometry."""
    instance = higher_order_chart_gauge_instance()

    assert instance.authority_effect == "None"
    assert instance.declared_generators == ("partial_x", "partial_y", "x*partial_x")
    assert instance.mass_decreased_or_zero is True
    assert instance.phi_higher_order <= instance.phi_first_order
    assert instance.first_order_quotient_cert.verify()
    assert instance.higher_order_quotient_cert.verify()


def test_finite_difference_adapter():
    """Test FiniteDifferenceAdapter column assembly from sampled point cloud differences."""
    obs1 = ObservationMap(edge_id="e1", matrix=Matrix([[1, 0]]))
    obs2 = ObservationMap(edge_id="e2", matrix=Matrix([[0, 1]]))
    presentation = ObservationPresentation(["e1", "e2"], {"e1": obs1, "e2": obs2})

    adapter = FiniteDifferenceAdapter(presentation)

    base_res = {"e1": Matrix([1, 0]), "e2": Matrix([0, 1])}
    cloud_res = [
        {"e1": Matrix([3, 0]), "e2": Matrix([0, 4])},
        {"e1": Matrix([5, 0]), "e2": Matrix([0, 2])},
    ]

    d0 = adapter.build_repair_matrix(base_res, cloud_res)
    assert d0.shape == (2, 2)
    assert d0[0, 0] == Rational(2)
    assert d0[1, 0] == Rational(3)
    assert d0[0, 1] == Rational(4)
    assert d0[1, 1] == Rational(1)


def test_covering_edge_adapter():
    """Test CoveringEdgeAdapter discrete section coboundary Delta(s)."""
    section = {
        "n0": Matrix([1, 2]),
        "n1": Matrix([3, 5]),
    }
    r_10 = Matrix([[1, 0], [0, 1]])
    edges = [("e01", "n0", "n1", r_10)]

    coboundary = CoveringEdgeAdapter.compute_coboundary(section, edges)
    vec = coboundary.as_vector()

    assert vec.shape == (2, 1)
    assert vec[0, 0] == Rational(2)
    assert vec[1, 0] == Rational(3)


