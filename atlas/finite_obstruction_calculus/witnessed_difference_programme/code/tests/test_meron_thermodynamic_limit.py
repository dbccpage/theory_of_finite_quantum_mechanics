"""Exact checks for the Meron Euclidean thermodynamic limit (O.12).

Every assertion below is exact integer or Fraction arithmetic on the full
periodic CAR carrier, except ``test_float_diagnostic_is_not_evidence``, which
only records that the floating-point value is a diagnostic. Each mutation test
changes one ingredient of the model and requires an exact value to move.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np
import pytest
from meron_thermodynamic_limit import car, checks, constants
from meron_thermodynamic_limit import series as S

ORDER = 3
CHAIN = (-3, 3)


def test_weighted_bound_uses_magnitude_and_refuses_signed_endpoint():
    theta = Fraction(-1, 96)
    old_q = 96 * theta
    assert constants.compute().m1 * (1 + old_q) / (1 - old_q) == 0
    _, a2, _ = car.ring(4)
    # a2[0] = 2*a_0: a_0^2=I/4, so C_00(0)=1/4 for every temperature.
    assert np.array_equal(a2[0] @ a2[0], np.eye(16, dtype=np.int64))
    with pytest.raises(ValueError, match="96"):
        constants.tail_bound(theta, Fraction(1))
    for sign in (-1, 1):
        assert constants.tail_bound(sign * Fraction(1, 192), Fraction(1)) == 3 * constants.compute().m1
    # mu=log(2) makes q=1 even on O-15's positive-temperature interval.
    with pytest.raises(ValueError, match="96"):
        constants.embedding_bound(4, Fraction(1, 192), Fraction(2))


@pytest.fixture(scope="module")
def chain_corr():
    lo, hi = CHAIN
    kc, ac, _ = car.chain(lo, hi)
    return checks.two_point(kc, ac, range(lo, hi + 1), ORDER)


@pytest.fixture(scope="module")
def ring6():
    k4, a2, _ = car.ring(6)
    pw = S.powers(k4, ORDER)
    return k4, a2, pw, checks.two_point(k4, a2, range(6), ORDER, pw=pw)


def test_two_builders_agree():
    assert checks.builders_agree((4, 6))


def test_bond_terms_are_projectors():
    assert checks.projector_checks(6)


def test_chain_sources_are_exact_integers_at_negative_sites():
    # (-1) ** lab is a float for negative lab; the sources must stay int64 everywhere.
    _, a2, _ = car.chain(-2, 2)
    assert all(np.issubdtype(a2[y].dtype, np.integer) for y in a2)
    # on the empty state n_x = 0, so the (0, 0) entry of 2a_x is -(-1)^x
    assert {y: int(a2[y][0, 0]) for y in a2} == {-2: -1, -1: 1, 0: -1, 1: 1, 2: -1}
    _, ab = car.bit_model([-1, 0, 1], [(-1, 0), (0, 1)])
    assert all(np.issubdtype(ab[y].dtype, np.integer) for y in ab)


def test_series_refuses_float_operands():
    k4, a2, _ = car.ring(4)
    pw = S.powers(k4, 1)
    with pytest.raises(TypeError):
        S.trace_table(pw, a2[0], a2[1].astype(float), 1)
    with pytest.raises(TypeError):
        S._matmul(k4.astype(float), k4)
    with pytest.raises(TypeError):
        S.powers(k4.astype(float), 1)
    with pytest.raises(TypeError):  # int64 @ uint64 would promote to float64
        S._matmul(k4, k4.astype(np.uint64))
    with pytest.raises(TypeError):  # narrower ints wrap below the int64 bound
        S.powers(k4.astype(np.int32), 1)


def test_ring_rejects_odd_or_small_length():
    for bad in (3, 2, 5):
        with pytest.raises(ValueError):
            car.ring(bad)


def test_particle_hole_mean_vanishes():
    assert checks.particle_hole_mean(4, 5)


def test_theta_zero_is_delta_quarter(chain_corr):
    for y, c in chain_corr.items():
        assert c[0][0] == (Fraction(1, 4) if y == 0 else 0)
        assert not any(c[0][1:])


def test_chain_vanishing_order_is_distance(chain_corr):
    for y, c in chain_corr.items():
        assert S.first_order(c) == abs(y)


def test_ring_vanishing_order_is_ring_distance(ring6):
    _, _, _, rc = ring6
    for y, c in rc.items():
        assert S.first_order(c) == checks.ring_distance(y, 6)


def test_lift_agrees_below_wrap_order(chain_corr, ring6):
    _, _, _, rc = ring6
    agree, differ = checks.lift_check(chain_corr, rc, 6, ORDER)
    assert agree == list(range(ORDER + 1)) and differ == []


def test_lift_differs_at_order_L_for_L4():
    lo, hi = (-4, 4)
    kc, ac, _ = car.chain(lo, hi)
    cc = checks.two_point(kc, ac, range(lo, hi + 1), 4)
    k4, a2, _ = car.ring(4)
    rc = checks.two_point(k4, a2, range(4), 4)
    agree, differ = checks.lift_check(cc, rc, 4, 4)
    assert agree == [0, 1, 2, 3] and differ == [4]


def test_erased_wrap_sign_changes_kernel_exactly_at_order_L():
    # An arc is the same CAR system with either wrap sign, so the lift cannot see the
    # sign below order L; the exact kernel must still change at order L.
    for length in (4, 6):
        k4, a2, _ = car.ring(length)
        k4e, a2e, _ = car.ring(length, erase_wrap_sign=(length - 1, 0))
        good = checks.row_sum_series(k4, a2, length, length)
        bad = checks.row_sum_series(k4e, a2e, length, length)
        assert [n for n in range(length + 1) if good[n] != bad[n]] == [length]
        if length == 6:
            assert S.fourier(good[6], 0)[0] == Fraction(3259, 2580480)  # order 6


def test_erased_ring_agrees_site_by_site_below_order_L():
    # The erased ring is the spin-periodic chain; it is local in spin language, so its
    # kernel matches the physical one per site below order L and the lift covers it too.
    for length in (4, 6):
        assert checks.erased_sign_site_differences(length) == [length]


def test_bond_locality_holds_for_both_rings():
    # TL-1's factorization premises, checked exactly; for the erased ring they are the
    # spin-language premises that let TL-1..TL-4 apply with the same constants.
    assert checks.bond_locality(6) and checks.bond_locality(6, erase=True)
    assert checks.bond_locality(4) and checks.bond_locality(4, erase=True)


def test_bond_locality_rejects_a_nonlocal_bond_term():
    # Round-4 counterexample R4-CX-01: 4P_(0,1)(I + Z_2...Z_5)/2 is 4 times a projector
    # and passes pairwise factorization, but is not local; the full check must refuse it.
    assert not checks.bond_locality(6, nonlocal_mutation=True)
    assert not checks.bond_locality(6, erase=True, nonlocal_mutation=True)


def test_bond_locality_rejects_a_parity_dressed_source():
    # Round-5 counterexample R5-CX-01: a source dressed by the total parity
    # passed the bond-only checks and changed the series below order L.
    for length in (4, 6):
        assert not checks.bond_locality(length, source_mutation=True)
        assert not checks.bond_locality(length, erase=True, source_mutation=True)


def test_bond_locality_rejects_an_odd_bond_term():
    # Round-5 objection R5-OBJ-02: an odd bond term passes the support test.
    assert not checks.bond_locality(6, odd_mutation=True)


def test_wrap_sign_zero_modes_recorded():
    w = checks.wrap_sign_zero_modes(6, 6)
    assert w["first_difference_order"] == 6
    assert w["physical"] == checks.ZERO_MODE + [Fraction(-43, 7680), Fraction(41, 46080), Fraction(3259, 2580480)]
    assert w["erased"][6] == Fraction(73, 61440)


def test_zero_mode_and_mode_one(ring6):
    k4, a2, pw, rc = ring6
    kser = S.zero_series(ORDER)
    for c in rc.values():
        kser = S.add(kser, c)
    assert [S.fourier(kser[n], 0)[0] for n in range(ORDER + 1)] == checks.ZERO_MODE[: ORDER + 1]
    assert S.fourier(kser[0], 1) == {}
    assert S.fourier(kser[1], 1) == {}
    assert S.fourier(kser[2], 1) == {2: Fraction(-1, 2)}
    assert checks._symmetric(kser)
    assert kser == checks.row_sum_series(k4, a2, 6, ORDER, pw=pw)


def test_commutator_identity():
    assert checks.commutator_identity(6)


def test_integration_by_parts_identity():
    r = checks.ibp_identity(4, 4, modes=(1, 2))
    assert r["identity"] and r["g_is_local_sum"]
    assert r["F_coefficients"][:3] == [0, Fraction(1, 4), Fraction(1, 16)]
    assert r["g_at_theta_0"] == Fraction(1, 2) and r["g_at_theta_0_u_independent"]


def test_b0_local_and_norm_certificate():
    sup = checks.b0_support_and_norm(6)
    assert sup["local"] and sup["even"] and sup["hermitian"]
    cert = checks.b0_norm_certificate()
    assert cert["norm_le_3"] and cert["norm_sq_le_3"] and cert["norm_sq_le_2_fails"]


def test_psd_exact_rejects_indefinite():
    assert not checks.psd_exact(np.array([[1, 2], [2, 1]]))
    assert not checks.psd_exact(np.array([[0, 1], [1, 0]]))
    assert checks.psd_exact(np.array([[2, 1], [1, 2]]))


def test_mutations_move_exact_values():
    k4, a2, _ = car.ring(6)
    good = checks.row_sum_series(k4, a2, 6, 2)
    raw = checks.row_sum_series(k4, a2, 6, 0, normalise=False)
    assert S.fourier(raw[0], 0)[0] == 16
    by_dim = checks.row_sum_series(k4, a2, 6, 2, ztr=[1 << 6, 0, 0])
    assert by_dim[:2] == good[:2] and by_dim[2] != good[2]
    k4d, a2d, _ = car.ring(6, p_scale=2)
    assert S.fourier(checks.row_sum_series(k4d, a2d, 6, 2)[2], 1) != {2: Fraction(-1, 2)}
    k4u, a2u, _ = car.ring(6, staggered=False)
    assert S.fourier(checks.row_sum_series(k4u, a2u, 6, 1)[1], 0)[0] != Fraction(1, 8)


def test_int64_guard():
    with pytest.raises(OverflowError):
        big = np.full((2, 2), 1 << 40, dtype=np.int64)
        S._matmul(big, big)


def test_constants_exact():
    c = constants.compute()
    assert c.s1 == Fraction(3, 43) and c.m1 == Fraction(24576, 43)
    assert c.s_g == Fraction(3, 59) and c.m_g == Fraction(331776, 59)
    assert c.m_f == Fraction(147499, 16512)
    assert c.g_const == Fraction(3981371, 118)
    assert c.theta_star == Fraction(2537, 100281465600)
    assert c.zero_mode_radius == Fraction(43, 56631360)
    # the window: theta_* (18432 M_F + 288 G) = 1/4
    assert c.theta_star * (18432 * c.m_f + 288 * c.g_const) == Fraction(1, 4)


def test_kotecky_preiss_failure_is_reported():
    with pytest.raises(ArithmeticError):
        constants.polymer_sum(Fraction(1, 16), 7)
    with pytest.raises(ValueError):
        constants.expm1_upper(Fraction(1))


def test_rate_and_embedding_bounds():
    eps40 = constants.lift_error_bound(40, Fraction(1, 192))
    eps80 = constants.lift_error_bound(80, Fraction(1, 192))
    assert eps80 < eps40 < Fraction(1, 100)
    with pytest.raises(ValueError):
        constants.lift_error_bound(10, Fraction(1, 128))
    assert constants.tail_bound(Fraction(1, 192), Fraction(3, 2)) == (
        constants.compute().m1 * Fraction(7, 4) / Fraction(1, 4))
    with pytest.raises(ValueError):
        constants.tail_bound(Fraction(1, 96), Fraction(2))
    e40 = constants.embedding_bound(40, Fraction(1, 192), Fraction(3, 2))
    e80 = constants.embedding_bound(80, Fraction(1, 192), Fraction(3, 2))
    assert e80 < e40
    with pytest.raises(ValueError):
        constants.embedding_bound(5, Fraction(1, 192), Fraction(1))
    with pytest.raises(ValueError):
        constants.embedding_bound(8, Fraction(1, 192), Fraction(1, 2))


def test_embedding_parts_add_up():
    # TL-7: window lift error <= 4 M_1 q^{L/2} (8/9)^{L/2} per site, wrapped images and
    # outside tail <= 2 M_1 q^{L/2}/(1-q) each. The stated bound must dominate their sum.
    assert constants.embedding_lift_factor() == Fraction(8, 9)
    m1 = constants.compute().m1
    theta = Fraction(1, 192)
    for e_mu in (Fraction(1), Fraction(3, 2), Fraction(19, 10)):
        q = 96 * theta * e_mu
        for length in range(4, 41, 2):
            h = length // 2
            lift = length * 4 * m1 * (q * constants.embedding_lift_factor()) ** h
            wraps_and_tail = 4 * m1 * q ** h / (1 - q)
            stated = constants.embedding_bound(length, theta, e_mu)
            assert lift + wraps_and_tail <= stated
            assert lift + wraps_and_tail > m1 * q ** h * 4 / (1 - q)


def test_float_diagnostic_is_not_evidence():
    v4 = checks.float_row_sum(4, 1 / 192, 1 / 3)
    v6 = checks.float_row_sum(6, 1 / 192, 1 / 3)
    assert isinstance(v4, float) and abs(v4 - v6) < 1e-6


def test_bond_locality_ties_the_hamiltonian_to_its_bond_terms():
    """Round-6 counterexample R6-CX-01: a K with an added term must fail."""
    for length in (4, 6):
        assert not checks.bond_locality(length, hamiltonian_mutation="zz")
        assert not checks.bond_locality(length, erase=True, hamiltonian_mutation="zz")
        assert not checks.bond_locality(length, hamiltonian_mutation="ptot")
    assert not checks.bond_locality(6, hamiltonian_mutation="z1z4")
    with pytest.raises(ValueError):
        checks.bond_locality(4, hamiltonian_mutation="z1z4")


def test_sparse_product_matches_dense():
    cs = car.annihilators(5)
    for a, b in ((cs[0].T, cs[0]), (cs[1].T, cs[3]), (cs[2], cs[2].T), (cs[4].T @ cs[4], cs[1].T @ cs[1])):
        assert np.array_equal(car._product(a, b), a @ b)
