"""Source SQL transport, exact target accounting and resolution error amplification."""
from fractions import Fraction as Q

import pytest

from omega_engine_projects.finite_to_continuum.code.interval_calculus import RationalInterval as I
from omega_engine_projects.finite_to_continuum.code.meron_time_refinement import EulerTimePlan
from omega_engine_projects.finite_to_continuum.code.meron_source_response import (
    SourceFieldPlan, source_field_trace, sample_source_plan, central_second_difference,
    with_declared_third_derivative_bound, sample_source_response,
)
from omega_engine_projects.fsp.meron_sign_problem.code.meron_exact_model import (
    meron_database, meron_transfer_trace,
)


@pytest.mark.parametrize("m,q,v", ((1, 2, 2), (1, 2, Q(1, 2)), (2, 3, 2), (2, 3, Q(1, 2))))
def test_actual_sql_generating_trace_equals_nonzero_source_transfer(m, q, v):
    con = meron_database(4, m, q)
    try:
        actual = con.execute("""WITH history AS (
            SELECT f.gid,f.mask,f.sign,f.weight,
              SUM(CASE WHEN n.site%2=0 THEN 2*((s.state>>n.site)&1)-1
                  ELSE 1-2*((s.state>>n.site)&1) END)/2 source_exponent
            FROM meron_configuration f JOIN meron_state s ON s.gid=f.gid AND s.mask=f.mask
            JOIN meron_node n ON n.time=s.time GROUP BY f.gid,f.mask)
            SELECT qsum(qmul(qmul(sign,weight),qpow(?,source_exponent))) FROM history""", (str(v),)).fetchone()[0]
        assert source_field_trace(4, m, q, v) == Q(actual)
    finally:
        con.close()


def test_free_chain_closed_form_and_unchanged_zero_source_partition():
    for m in (1, 2, 4):
        assert source_field_trace(4, m, 1, 2) == (Q(2) ** m + Q(1, 2) ** m) ** 4
    assert source_field_trace(4, 2, 3, 1) == Q(meron_transfer_trace(4, 2, 3)) == 912
    assert source_field_trace(4, 2, 3, 2) == source_field_trace(4, 2, 3, Q(1, 2))


def test_signed_field_plan_and_exact_common_target_error():
    time = EulerTimePlan(4, 8, I(Q(1, 4)))
    plan = SourceFieldPlan(time, I(Q(-1, 2)))
    assert plan.v == Q(32, 33)
    assert plan.exponential_majorant == 3
    assert plan.finite_density_error == Q(391, 1024)
    assert plan.thermodynamic_density_error - plan.finite_density_error == Q(3, 32)
    uncertain = SourceFieldPlan(EulerTimePlan(4, 8, I.from_point(Q(1, 4), Q(1, 100))),
                                I.from_point(Q(-1, 2), Q(1, 50)))
    assert uncertain.finite_density_error - plan.finite_density_error == Q(7, 400)
    fine = SourceFieldPlan(EulerTimePlan(4, 16, time.parameter), plan.field)
    assert fine.finite_density_error < plan.finite_density_error


def test_zero_temperature_sample_encloses_known_actual_source_target():
    plan = SourceFieldPlan(EulerTimePlan(4, 1, I(0)), I(2))
    sample = sample_source_plan(plan, log_order=12)
    assert sample.unscaled_partition == Q(625, 16)
    assert sample.finite_target_enclosure.contains_interval(sample.physical_density)
    assert sample.thermodynamic_target_enclosure == sample.finite_target_enclosure
    assert sample.authority_effect == "None"
    # A tighter high-M nonzero field plan has the same declared target.
    fine = sample_source_plan(SourceFieldPlan(EulerTimePlan(4, 8, I(0)), I(2)), log_order=12)
    assert sample.thermodynamic_target_enclosure.intersects(fine.thermodynamic_target_enclosure)


def test_joint_volume_time_majorant_vanishes_along_m_equals_l_squared_prefix():
    bounds = [SourceFieldPlan(EulerTimePlan(l, l*l, I(Q(1, 4))), I(Q(1, 2))).thermodynamic_density_error
              for l in (4, 8, 16)]
    assert bounds[0] > bounds[1] > bounds[2]
    # Finite prefix of a separately written infinite-family proof, not execution at infinite L.


def test_finite_resolution_response_keeps_center_sign_and_error_amplification():
    minus, center, plus = I.from_point(1, Q(1, 100)), I.from_point(0, Q(1, 50)), I.from_point(1, Q(3, 100))
    response = central_second_difference(minus, center, plus, Q(1, 2))
    assert response.midpoint == 8
    assert response.radius == Q(8, 25)
    widened = with_declared_third_derivative_bound(response, Q(1, 2), 6)
    assert widened.radius == response.radius + 1
    assert with_declared_third_derivative_bound(response, Q(1, 2), 0) == response


@pytest.mark.parametrize("v", (True, 2.0))
def test_inexact_and_boolean_source_scalars_refuse(v):
    with pytest.raises(TypeError):
        source_field_trace(4, 1, 2, v)


@pytest.mark.parametrize("arguments", ((4, 1, 2, 0), (4, 1, 2, -1), (4, 17, 2, 1), (4, 1, 2, 1 << 300)))
def test_source_domain_and_work_caps_refuse(arguments):
    with pytest.raises(ValueError):
        source_field_trace(*arguments)


@pytest.mark.parametrize("epsilon", (0, -1, True, 1.0))
def test_response_step_refuses_missing_resolution(epsilon):
    with pytest.raises((ValueError, TypeError)):
        central_second_difference(I(0), I(0), I(0), epsilon)


def test_declared_smoothness_and_majorant_boundaries_refuse():
    with pytest.raises(ValueError):
        with_declared_third_derivative_bound(I(0), 1, -1)
    with pytest.raises(ValueError):
        SourceFieldPlan(EulerTimePlan(4, 1, I(1)), I(100))
    with pytest.raises(TypeError):
        SourceFieldPlan(EulerTimePlan(4, 1, I(1)), 0)


def test_actual_response_sampler_binds_one_temperature_and_three_field_points():
    time = EulerTimePlan(4, 4, I(0))
    result = sample_source_response(time, 0, Q(1, 2), log_order=12)
    minus, center, plus = result.samples
    assert all(sample.plan.time is time for sample in result.samples)
    assert [sample.plan.field.midpoint for sample in result.samples] == [Q(-1, 2), 0, Q(1, 2)]
    assert minus.unscaled_partition == plus.unscaled_partition
    assert center.unscaled_partition == 16
    assert result.thermodynamic_response_enclosure == central_second_difference(
        minus.thermodynamic_target_enclosure, center.thermodynamic_target_enclosure,
        plus.thermodynamic_target_enclosure, Q(1, 2))
    assert result.authority_effect == "None"
