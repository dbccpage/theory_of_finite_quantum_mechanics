"""Original SQL occupation observable versus independent transfer derivatives."""
from fractions import Fraction
import pytest

from omega_engine_projects.finite_to_continuum.code.meron_observable_transport import staggered_moments
from omega_engine_projects.fsp.meron_sign_problem.code.meron_exact_model import meron_database, meron_transfer_trace


@pytest.mark.parametrize("sites,repetitions,q", ((4, 1, 1), (4, 1, 2), (4, 2, 3), (6, 1, 2)))
def test_original_sql_time_integrated_query_is_the_second_insertion_derivative(sites, repetitions, q):
    moments = staggered_moments(sites, repetitions, q)
    con = meron_database(sites, repetitions, q)
    try:
        actual = con.execute("SELECT qsum(qmul(sign,weight)) FROM meron_configuration").fetchone()[0]
        direct = con.execute("""WITH history AS (
            SELECT f.gid,f.mask,f.sign,f.weight,
              SUM(CASE WHEN n.site%2=0 THEN 2*((s.state>>n.site)&1)-1
                  ELSE 1-2*((s.state>>n.site)&1) END) twice_observable
            FROM meron_configuration f JOIN meron_state s ON s.gid=f.gid AND s.mask=f.mask
            JOIN meron_node n ON n.time=s.time GROUP BY f.gid,f.mask)
            SELECT qsum(qmul(qmul(sign,weight),qdiv(CAST(twice_observable AS TEXT),'2'))),
              qsum(qmul(qmul(sign,weight),qmul(qdiv(CAST(twice_observable AS TEXT),'2'),
                  qdiv(CAST(twice_observable AS TEXT),'2')))) FROM history""").fetchone()
        source_square = con.execute("SELECT qsum(qmul(qmul(sign,weight),qmul(observable,observable))) FROM meron_staggered").fetchone()[0]
        improved = con.execute("SELECT qsum(numerator) FROM meron_squared_orbit").fetchone()[0]
        assert moments.partition == Fraction(actual) == Fraction(meron_transfer_trace(sites, repetitions, q))
        assert moments.first == Fraction(direct[0])
        assert moments.second == Fraction(direct[1]) == Fraction(source_square) == Fraction(improved)
        assert moments.mean_square == moments.second / ((2 * repetitions) ** 2 * moments.partition)
    finally:
        con.close()


def test_zero_time_generator_keeps_the_time_average_normalization():
    for repetitions in (1, 2, 4):
        moments = staggered_moments(4, repetitions, 1)
        assert moments.partition == 16
        assert moments.first == 0
        assert moments.second == 16 * (2 * repetitions) ** 2
        assert moments.mean_square == 1


@pytest.mark.parametrize("arguments", ((4, True, 2), (4, 2.0, 2), (4, 1, 2.0), (4, 1, True)))
def test_approximate_and_boolean_inputs_refuse(arguments):
    with pytest.raises(TypeError):
        staggered_moments(*arguments)


@pytest.mark.parametrize("arguments", ((3, 1, 2), (4, 17, 2), (4, 1, Fraction(1, 2)), (4, 1, 1 << 300)))
def test_carrier_clock_and_scalar_limits_refuse(arguments):
    with pytest.raises(ValueError):
        staggered_moments(*arguments)
