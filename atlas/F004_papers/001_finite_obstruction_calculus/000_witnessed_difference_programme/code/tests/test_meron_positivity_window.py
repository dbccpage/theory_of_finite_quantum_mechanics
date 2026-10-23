"""Exact checks for TL-10: strict positivity of the nonzero modes on ``0 < theta <= 1/192``.

Every assertion is integer or Fraction arithmetic, except the three tests named
``*_diagnostic``, which only record floating-point agreement and prove nothing.
Each mutation test changes one ingredient and requires an exact check to fail.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np
import pytest
from meron_thermodynamic_limit import car
from meron_thermodynamic_limit import positivity as P


@pytest.fixture(scope="module")
def w_norm_cert():
    return P.w_norm_certificate(P.W_BOUND)


def test_staggered_lowering_commutes_with_k_and_gives_ladders():
    cert = P.su2_certificate((2, 4, 6, 8))
    assert cert["all_pass"], cert


def test_unstaggered_lowering_fails():
    cert = P.su2_certificate((4, 6), staggered=False)
    assert not any(cert[n]["K_commutes_with_G"] for n in (4, 6))
    assert not cert["all_pass"]


def test_spin_lowerings_commute_on_different_sites():
    sig = P.spin_lowerings(4)
    for x in range(4):
        for y in range(x + 1, 4):
            assert not np.any(sig[x] @ sig[y].T - sig[y].T @ sig[x])


def test_w_cases_cover_every_local_configuration():
    cases = P.w_cases()
    for n in P.SHORT_CHAINS:
        assert {x for m, x in cases if m == n} == set(range((n + 1) // 2))
    assert {x for m, x in cases if m == P.HOST_CHAIN} == set(range(5))


def test_w_is_hermitian_and_conserves_particle_number():
    w = P.w_int(6, 2)
    assert np.array_equal(w, w.T)
    assert sum(b.shape[0] for b in P._number_blocks(w, 6)) == 64


def test_w_terms_vanish_beyond_three_sites():
    # W_x = sum_y [ad_K^2 a_x, ad_K a_y]. The term is zero for |y - x| >= 4 and
    # nonzero at |y - x| = 3, so W_x lives on [x-4, x+4] and reaches that far:
    # on a longer chain the sites beyond are spectators, which is what lets
    # w_cases() stand in for every even chain.
    k4, a2, _ = car.chain(0, 8)
    left = P._ad(k4, P._ad(k4, a2[4]))
    for y in (0, 8):
        assert not np.any(P._ad(left, P._ad(k4, a2[y])))
    for y in (1, 7):
        assert np.any(P._ad(left, P._ad(k4, a2[y])))
    total = sum(P._ad(left, P._ad(k4, a2[y])) for y in range(9))
    assert np.array_equal(total, P.w_int(9, 4))


def _bit_reversal(n: int) -> np.ndarray:
    return np.array([int(format(s, f"0{n}b")[::-1], 2) for s in range(1 << n)])


@pytest.mark.parametrize("n", [6, 8])
def test_w_mirror_image_is_the_reflected_site(n):
    # Reflection x -> n-1-x of an even chain is bit reversal in the occupation
    # basis; it fixes K, flips every a_y, and so carries W_x to W_{n-1-x}.
    r = _bit_reversal(n)
    for x in range(n // 2):
        assert np.array_equal(P.w_int(n, x)[np.ix_(r, r)], P.w_int(n, n - 1 - x))


def test_w_norm_at_most_eleven_halves(w_norm_cert):
    assert w_norm_cert["all_pass"], [c for c in w_norm_cert["cases"] if not c["psd"]]


def test_w_norm_five_fails_in_the_interior():
    # The interior value is 5.0234...; one case suffices for the mutation.
    c2 = int(P.W_SCALE * P.W_FAILING) ** 2
    blocks = P._number_blocks(P.w_int(P.HOST_CHAIN, 4), P.HOST_CHAIN)
    verdicts = []
    for blk in blocks:
        if blk.size:
            m = c2 * np.eye(len(blk), dtype=object) - blk.astype(object) @ blk.astype(object)
            verdicts.append(P.psd_exact(m))
    assert not all(verdicts)


@pytest.mark.parametrize("s", [Fraction(1, 3), Fraction(5, 2), Fraction(1, 1000)])
def test_dimer_trial_expectations(s):
    assert P.dimer_trial_certificate(6, s)["all_pass"]


def test_dimer_trial_rejects_odd_chain():
    with pytest.raises(ValueError):
        P.dimer_trial_certificate(5)


def test_elementary_g_identity_and_mutation():
    assert P.elementary_g_identity(3)
    assert not P.elementary_g_identity(4)


def test_window_constant():
    cert = P.window_certificate()
    assert cert["four_pi_sq_above_39"]
    assert cert["floor_at_1_192_ge_1_9"]
    assert cert["floor_at_1_96_ge_1_9"]
    # The value quoted in the docs (TL-12): (3 - t - t^2/4)/24 - 11 t/78 at t = 1/192.
    assert Fraction(cert["floor_at_1_192"]) == Fraction(5706995, 46006272)
    assert P.window_floor(Fraction(1, 96)) == Fraction(1415795, 11501568)


def test_window_floor_decreases_and_one_eighth_fails():
    ts = [Fraction(k, 1920) for k in range(1, 21)]
    vals = [P.window_floor(t) for t in ts]
    assert all(a > b for a, b in zip(vals, vals[1:]))
    assert P.window_floor(Fraction(1, 192)) < Fraction(1, 8)


def test_wrong_second_moment_bound_shrinks_window():
    # With ||W|| <= 1000 the floor at 1/192 drops below 1/9.
    assert P.window_floor(Fraction(1, 192), bound=Fraction(1000)) < P.FLOOR


def test_bound_must_scale_to_an_integer():
    with pytest.raises(ValueError):
        P.w_norm_certificate(Fraction(1, 512))


def test_mutations_all_fail():
    assert not any(P.mutations().values())


def test_lehmann_diagnostic():
    for row in P.lehmann_diagnostics((4,), (1 / 192, 0.05), nodes=801):
        assert abs(row["kms_jump_minus_2thetaF"]) < 1e-14
        assert abs(row["moment_minus_theta3W"]) < 1e-14
        assert abs(row["khat_lehmann"] - row["khat_quadrature"]) < 1e-6
        assert row["Fbar"] > row["Fbar_floor"] > 0
        assert row["khat_lehmann"] > row["khat_floor"]
        assert row["max_Q_minus_T11"] < 1e-12


def test_w_norms_diagnostic():
    norms = P.w_norms_float()
    assert max(norms.values()) < P.W_BOUND
    assert max(norms.values()) > P.W_FAILING


def test_ring_su2_defect_diagnostic():
    # The docs quote <Q>-<T00> near 1e-6 on the ring at L=4, theta=0.05.
    (row,) = P.ring_su2_defect_float((4,), (0.05,))
    assert 1e-6 < row["Q_minus_T00"] < 2e-6
    assert 1e-6 < row["Q_minus_T11"] < 2e-6
