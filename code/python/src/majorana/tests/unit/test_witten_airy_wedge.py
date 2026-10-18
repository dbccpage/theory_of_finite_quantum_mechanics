"""W-WITTEN.1 executable wedge: Witten 1001.2933 Section 3.1 (Airy thimbles).

Every test binds a page-anchored fact of the paper (equation numbers cited
per test; PDF pages 24-33 of arXiv:1001.2933v4). The reference values are
computed by the ported thimble machinery in
``omega_engine.crates.homology_theory.lefschetz_thimble``. The finite
action is explicitly transcribed from eq. (3.2); these tests verify consequences
of that transcription rather than deriving the action from independent axioms.

AuthorityEffect: None. Agreement here is finite-dimensional numerics only;
nothing about the infinite-dimensional Chern-Simons continuation is claimed.
"""

from __future__ import annotations

import numpy as np
import pytest

from omega_engine.crates.homology_theory.lefschetz_thimble import (
    FlowRecord,
    U_MINUS,
    U_PLUS,
    airy_action,
    descent_directions,
    integrate_exp_action,
    monodromy,
    newton_critical_points,
    stokes_connection,
    trace_thimble,
)


def _airy_reference(lam: float) -> complex:
    """Z_lam = 2*pi*lam**(-1/3) * Ai(-lam**(2/3)) for real lam > 0.

    Substituting x = lam**(-1/3) u into eq. (3.1) maps Witten's integral onto
    the standard Airy function Ai(a) = (1/2pi) Int dx exp(i(x^3/3 + a x))
    with a = -lam**(2/3).
    """
    try:
        from scipy.special import airy as _airy

        ai = _airy(-(lam ** (2.0 / 3.0)))[0]
    except ImportError:
        import mpmath

        ai = float(mpmath.airyai(-(lam ** (2.0 / 3.0))))
    return 2.0 * np.pi * lam ** (-1.0 / 3.0) * complex(ai)


def _seeds() -> list[complex]:
    return [0.5 + 0.5j, -0.5 - 0.5j, 2.0 + 0.1j, -2.0 + 0.3j, 0.1 - 1.2j]


def test_critical_points_and_action_values_match_eq_3_6() -> None:
    lam = 1.7 - 0.9j
    act = airy_action(lam)
    cps = newton_critical_points(act, _seeds())
    assert len(cps) == 2
    minus, plus = cps
    assert abs(minus - (-1.0)) < 1e-8
    assert abs(plus - 1.0) < 1e-8
    i_plus = act.eval(np.array([1.0 + 0j]))
    i_minus = act.eval(np.array([-1.0 + 0j]))
    assert abs(i_plus - (-2j * lam / 3.0)) < 1e-12
    assert abs(i_minus - (2j * lam / 3.0)) < 1e-12


def test_downward_flow_decreases_h_and_conserves_im_action() -> None:
    lam = 1.0 + 0.4j
    act = airy_action(lam)
    for cp in (1.0 + 0j, -1.0 + 0j):
        for direction in descent_directions(act, cp):
            rec = trace_thimble(
                act, cp, direction, dt=1e-3, n_steps=20000, h_floor=-25.0
            )
            assert isinstance(rec, FlowRecord)
            assert len(rec.points) > 100
            assert rec.h_monotone_decreasing, "h must decrease along a downward flow"
            assert rec.max_im_drift < 5e-3, (
                f"Im I must be conserved along the flow (drift {rec.max_im_drift})"
            )


def _thimble_integral(act, cp) -> complex:
    d_out, d_in = descent_directions(act, cp)
    out_b = trace_thimble(act, cp, d_out, dt=5e-4, n_steps=60000, h_floor=-30.0)
    in_b = trace_thimble(act, cp, d_in, dt=5e-4, n_steps=60000, h_floor=-30.0)
    return integrate_exp_action(act, out_b, in_b)


def _matching_orientations(lam: float, tol: float) -> list[tuple[int, int]]:
    act = airy_action(lam)
    z_plus = _thimble_integral(act, 1.0 + 0j)
    z_minus = _thimble_integral(act, -1.0 + 0j)
    ref = _airy_reference(lam)
    return [
        (sp, sm)
        for sp in (1, -1)
        for sm in (1, -1)
        if abs(sp * z_plus + sm * z_minus - ref) < tol
    ]


def test_real_cycle_thimble_decomposition_reproduces_airy_eq_3_25() -> None:
    tol = 2e-3
    matches_a = _matching_orientations(2.0, tol)
    assert len(matches_a) == 1, f"expected a unique orientation pair, got {matches_a}"
    matches_b = _matching_orientations(3.0, tol)
    assert matches_b == matches_a, (
        f"orientation pair must be lam-independent: {matches_a} vs {matches_b}"
    )


def test_stokes_connection_exists_exactly_on_imaginary_lambda() -> None:
    act_on_ray = airy_action(1j)
    assert stokes_connection(
        act_on_ray, 1.0 + 0j, -1.0 + 0j, dt=1e-3, n_steps=30000, h_floor=-40.0
    ), "on the Stokes ray lam = i the downward flow from +1 must reach -1"

    act_off_ray = airy_action(1j * np.exp(0.35j))
    assert not stokes_connection(
        act_off_ray, 1.0 + 0j, -1.0 + 0j, dt=1e-3, n_steps=30000, h_floor=-40.0
    ), "off the Stokes ray no flow may connect the critical points"


def test_jump_matrices_compose_to_order_three_monodromy_eq_3_15() -> None:
    m = monodromy()
    assert np.array_equal(m, np.array([[-1, -1], [1, 0]]))
    assert np.array_equal(m @ m @ m, np.eye(2, dtype=int))
    assert np.array_equal(
        (U_PLUS - np.eye(2, dtype=int)) @ (U_PLUS - np.eye(2, dtype=int)),
        np.zeros((2, 2), dtype=int),
    )
    assert np.array_equal(
        (U_MINUS - np.eye(2, dtype=int)) @ (U_MINUS - np.eye(2, dtype=int)),
        np.zeros((2, 2), dtype=int),
    )


def test_thimble_asymptotics_leading_order_eq_3_17() -> None:
    lam = 60.0 * np.exp(0.3j)
    act = airy_action(lam)
    cp = 1.0 + 0j
    d_out, d_in = descent_directions(act, cp)
    out_b = trace_thimble(act, cp, d_out, dt=2e-5, n_steps=400000, h_floor=-25.0)
    in_b = trace_thimble(act, cp, d_in, dt=2e-5, n_steps=400000, h_floor=-25.0)
    z_num = integrate_exp_action(act, out_b, in_b)
    i_plus = act.eval(np.array([cp]))
    z_asym = np.sqrt(np.pi) * np.exp(i_plus) * (-1j * lam) ** (-0.5)
    ratio = z_num / z_asym
    phase_error = min(abs(ratio - 1.0), abs(ratio + 1.0))
    assert phase_error < 0.02, f"leading asymptotics ratio {ratio}"


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main([__file__, "-q"]))


