from fractions import Fraction as Q
import pytest
from omega_engine_projects.finite_to_continuum.code.circle_piecewise_linear import CirclePiecewiseLinear as P
from omega_engine_projects.finite_to_continuum.code.interval_calculus import RationalInterval as I
from omega_engine_projects.finite_to_continuum.code.meron_time_refinement import EulerTimePlan
from omega_engine_projects.finite_to_continuum.code.meron_analytic_response import AnalyticResponsePlan
from omega_engine_projects.finite_to_continuum.code.meron_spatial_source import SpatialSourcePlan, sample_spatial_source
from omega_engine_projects.finite_to_continuum.code.meron_observable_transport import (
    weighted_staggered_moments, staggered_moments,
)
from omega_engine_projects.fsp.meron_sign_problem.code.meron_exact_model import meron_database


@pytest.mark.parametrize("r,m,knots", (
    (0, 2, ((0, 0), (Q(1, 2), 1), (1, 0))),
    (Q(1, 384), 1, ((0, 0), (Q(1, 2), 1), (1, 0))),
    (Q(1, 192), 2, ((0, -1), (Q(1, 2), 1), (1, -1))),
    (Q(1, 384), 2, ((0, -1), (1, -1))),
))
def test_actual_weighted_sql_histories_equal_the_retained_source_moments(r, m, knots):
    profile = P(knots)
    response = AnalyticResponsePlan(EulerTimePlan(4, m, I(r)), Q(1, 256))
    plan = SpatialSourcePlan(response, profile, Q(1, 64))
    result = sample_spatial_source(plan)
    con = meron_database(4, m, response.time.q)
    try:
        weights = profile.uniform_samples(4)
        # Use the original histories; spatial labels and weights are a declared query.
        sql = """WITH profile(site,value) AS (VALUES (0,?),(1,?),(2,?),(3,?)),
        history AS (SELECT f.gid,f.mask,f.sign,f.weight,
          qsum(qmul(p.value,qmul('1/2',CASE WHEN n.site%2=0
             THEN 2*((s.state>>n.site)&1)-1 ELSE 1-2*((s.state>>n.site)&1) END))) observable
          FROM meron_configuration f JOIN meron_state s ON s.gid=f.gid AND s.mask=f.mask
          JOIN meron_node n ON n.time=s.time JOIN profile p ON p.site=n.site GROUP BY f.gid,f.mask)
        SELECT qsum(qmul(sign,weight)),qsum(qmul(qmul(sign,weight),observable)),
               qsum(qmul(qmul(sign,weight),qmul(observable,observable))) FROM history"""
        partition, first, second = map(Q, con.execute(sql, tuple(map(str, weights))).fetchone())
        assert (partition, first, second) == (result.moments.partition, result.moments.first, result.moments.second)
        assert result.quadratic.midpoint == second/(partition*(2*m)**2*4)
        assert result.plan is plan and result.plan.profile is profile and result.authority_effect == "None"
        if r == 0:
            assert result.quadratic.midpoint == Q(3, 32)
            assert result.quadratic.contains(Q(1, 4)*profile.square_integral)
            assert result.finite_log.radius == Q(1, 57)
            assert result.continuum_log.contains(plan.probe**2*Q(1, 4)*profile.square_integral/2)
    finally:
        con.close()


def test_actual_spatial_kernel_has_translation_symmetry_and_mixed_readouts():
    def variance(weights, q):
        return weighted_staggered_moments(4, 1, q, weights).mean_square
    q = Q(385, 384)
    basis = [tuple(int(x == y) for y in range(4)) for x in range(4)]
    diagonal = [variance(e, q) for e in basis]
    kernel = [[diagonal[x] if x == y else (variance(tuple(basis[x][i]+basis[y][i]
               for i in range(4)), q)-diagonal[x]-diagonal[y])/2 for y in range(4)] for x in range(4)]
    assert all(kernel[x][y] == kernel[(x+1)%4][(y+1)%4] for x in range(4) for y in range(4))
    assert sum(kernel[0]) == staggered_moments(4, 1, q).mean_square/4
    triangle, constant = (0, Q(1, 2), 1, Q(1, 2)), (1, 1, 1, 1)
    combined = tuple(f+g for f, g in zip(triangle, constant))
    assert (variance(combined, 1)-variance(triangle, 1)-variance(constant, 1))/8 == Q(1, 8)


def test_weighted_polymer_margin_and_nondegenerate_temperature_bound_are_exact():
    for m in (1, 2, 16, 256):
        t = Q(1, 256*m-1)
        root = 4*t/(1-28*m*4*t)
        assert root <= Q(4, 143*m)
        assert 7*m*root <= Q(28, 143) < 1
        assert 2*m*root <= Q(8, 143)
    theta, radius, c = Q(1, 2**20), Q(1, 64), Q(1, 19)
    delta = 2*c/radius**2*theta/(Q(1, 192)-theta)
    assert delta == Q(24576, 311239) < Q(1, 8)


def test_spatial_probe_domain_and_zero_profile_refuse_or_collapse_exactly():
    response = AnalyticResponsePlan(EulerTimePlan(4, 2, I(0)), Q(1, 256))
    profile = P(((0, 1), (1, 1)))
    with pytest.raises(ValueError, match="analytic disk"):
        SpatialSourcePlan(response, profile, Q(1, 32))
    for probe in (True, 0.01):
        with pytest.raises(TypeError):
            SpatialSourcePlan(response, profile, probe)
    zero = sample_spatial_source(SpatialSourcePlan(response, P(((0, 0), (1, 0))), 100))
    assert zero.quadratic == zero.finite_log == zero.continuum_log == I(0)
    with pytest.raises(ValueError):
        weighted_staggered_moments(4, 17, 1, (1, 1, 1, 1))
    with pytest.raises(ValueError):
        weighted_staggered_moments(4, 1, 1, (1,))
