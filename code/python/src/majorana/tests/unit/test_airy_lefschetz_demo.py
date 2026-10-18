r"""
Unit tests for Airy Lefschetz Thimble Demo (codaq/airy_lefschetz_demo.py).
"""

import cmath
import math
import pytest
from omega_engine.crates.homology_theory.airy_lefschetz_demo import (
    residual_orientation,
    run_airy_demo,
    stokes_scan,
    tempered_airy_demo,
    thimble_metropolis,
)
from omega_engine.crates.homology_theory.lefschetz_thimble import AiryAction, steepest_descent_flow


def test_airy_demo_full_run():
    res = run_airy_demo()

    assert len(res["critical_points"]) == 2
    assert abs(res["hessian_at_test"] - 2j * (0.5 + 0.3j)) < 1e-14
    assert res["max_im_dev"] < 1e-3
    assert abs(abs(res["residual_orientation"]) - 1.0) < 1e-5
    assert 0.1 < res["metropolis_acceptance"] <= 1.0
    assert math.isfinite(res["tempered_log_alpha"])


def test_airy_stokes_scan():
    rays = stokes_scan(lam_mag=1.0, n_angles=12)
    assert len(rays) > 0
    for theta, lam, re_diff in rays:
        assert re_diff < 0.15


def test_tempered_airy_demo_values():
    s_short, s_long, log_alpha = tempered_airy_demo(1.0 + 0.0j)
    assert math.isfinite(s_short)
    assert math.isfinite(s_long)
    assert math.isfinite(log_alpha)


