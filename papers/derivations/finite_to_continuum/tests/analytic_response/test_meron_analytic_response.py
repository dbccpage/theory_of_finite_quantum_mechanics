"""Actual protected SQL query, analytic domain and finite majorant boundaries."""
from fractions import Fraction as Q
import pytest

from omega_engine_projects.finite_to_continuum.code.interval_calculus import RationalInterval as I
from omega_engine_projects.finite_to_continuum.code.meron_time_refinement import EulerTimePlan
from omega_engine_projects.finite_to_continuum.code.meron_analytic_response import (
    AnalyticResponsePlan, sample_analytic_response,
)
from omega_engine_projects.fsp.meron_sign_problem.code.meron_exact_model import meron_database


@pytest.mark.parametrize("r,m", ((Q(0), 2), (Q(1, 384), 1), (Q(1, 192), 2)))
def test_actual_sql_intensive_query_keeps_both_normalizations(r, m):
    plan = AnalyticResponsePlan(EulerTimePlan(4, m, I(r)), Q(1, 256))
    result = sample_analytic_response(plan)
    con = meron_database(4, m, plan.time.q)
    try:
        partition = Q(con.execute("SELECT qsum(qmul(sign,weight)) FROM meron_configuration").fetchone()[0])
        numerator = Q(con.execute("SELECT qsum(qmul(qmul(sign,weight),qmul(observable,observable))) FROM meron_staggered").fetchone()[0])
        assert result.moments.partition == partition
        assert result.moments.second == numerator
        assert result.moments.first == 0
        assert result.intensive_response == numerator / ((2*m)**2 * 4 * partition)
        assert result.thermodynamic_response_enclosure.radius == plan.response_error
        assert result.authority_effect == "None"
        if r == 0:
            assert result.intensive_response == Q(1, 4)
            assert result.thermodynamic_response_enclosure.contains(Q(1, 4))
    finally:
        con.close()


def test_exact_error_and_resolution_tradeoff():
    time = EulerTimePlan(4, 16, I(0))
    plan = AnalyticResponsePlan(time, Q(1, 256))
    assert plan.pressure_error == Q(3, 65536)
    assert plan.response_error == 12 + Q(16384, 19)
    fine = AnalyticResponsePlan(time, Q(1, 512))
    assert fine.response_error == 48 + Q(4096, 19)


def test_temperature_interval_admission_and_outside_fixture_refusal():
    assert AnalyticResponsePlan(EulerTimePlan(4, 2, I(Q(1, 192))), Q(1, 256))
    for interval in (I.from_point(Q(1, 192), Q(1, 1000)), I(4)):
        with pytest.raises(ValueError, match="temperature interval"):
            AnalyticResponsePlan(EulerTimePlan(4, 2, interval), Q(1, 256))


@pytest.mark.parametrize("epsilon", (0, -1, Q(1, 64), True, 0.001))
def test_missing_or_inexact_resolution_refuses(epsilon):
    with pytest.raises((TypeError, ValueError)):
        AnalyticResponsePlan(EulerTimePlan(4, 2, I(0)), epsilon)


def test_finite_bound_prefix_does_not_expand_carrier_or_time_caps():
    values = [AnalyticResponsePlan(EulerTimePlan(l, l*l, I(Q(1, 384))),
                                   Q(1, 256)).response_error for l in (4, 8, 16)]
    assert values[0] > values[1] > values[2]
    with pytest.raises(ValueError):
        sample_analytic_response(AnalyticResponsePlan(EulerTimePlan(8, 16, I(0)), Q(1, 256)))


def test_actual_support_graph_counts_cover_wrapping_bond_and_time_copies():
    for l, m in ((4, 1), (4, 2), (6, 3)):
        supports = ([{x, (x+1) % l} for _ in range(m) for x in range(l)]
                    + [{x} for _ in range(2*m) for x in range(l)])
        degrees = [sum(bool(s & t) for t in supports)-1 for s in supports]
        assert max(degrees) == 7*m-1
        t = Q(1, 256*m-1)  # Rational upper bound for exp(1/(256M))-1.
        root_bound = 3*t / (1-28*m*3*t)
        assert 7*m*root_bound <= Q(7, 57) < 1
        assert 3*m*root_bound <= Q(1, 19)
