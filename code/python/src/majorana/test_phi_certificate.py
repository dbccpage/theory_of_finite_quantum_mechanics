"""U1 PhiCertificate.verify() + weighted Phi1 (S1 L204) faithfulness tests."""

import numpy as np
import pytest

from omega_engine.crates.solver.solv_phi_l1_lp import solve_phi
from omega_engine.crates.linear_algebra_theory.dual_certificate import DivergenceFreeDual, PhiCertificate
from omega_engine.crates.linear_algebra_theory.l1_seminorm import EdgeCochain


def _triangle_B():
    return np.array(
        [
            [-1.0, 1.0, 0.0],
            [0.0, -1.0, 1.0],
            [1.0, 0.0, -1.0],
        ]
    )




def test_certificate_verifies_on_cycle():
    B = _triangle_B()
    omega = np.array([1.0, 1.0, 1.0])
    _, _, cert = solve_phi(B, omega)
    assert abs(cert.phi1 - 3.0) < 1e-6
    assert cert.verify() is True
    assert cert.certified is True
    assert abs(cert.duality_gap) <= cert.tol


def test_certificate_verifies_on_exact():
    B = _triangle_B()
    omega = np.array([3.0, 2.0, -5.0])
    _, _, cert = solve_phi(B, omega)
    assert cert.phi1 < 1e-6
    assert cert.verify() is True




def test_loosened_dual_not_certified():
    B = _triangle_B()
    omega = np.array([1.0, 1.0, 1.0])
    _, _, good = solve_phi(B, omega)
    bad_dual = DivergenceFreeDual(np.zeros(3), None)
    loosened = PhiCertificate(
        phi1=good.phi1,
        residual=good.residual,
        dual=bad_dual,
        dual_value=0.0,
        B=B,
        tol=1e-6,
        weights=None,
    )
    assert loosened.verify() is False
    assert loosened.certified is False


def test_infeasible_dual_not_certified():
    B = _triangle_B()
    omega = np.array([1.0, 1.0, 1.0])
    infeasible = DivergenceFreeDual(np.array([1.0, 0.0, 0.0]), None)
    cert = PhiCertificate(
        phi1=3.0,
        residual=EdgeCochain(omega),
        dual=infeasible,
        dual_value=1.0,
        B=B,
        tol=1e-6,
        weights=None,
    )
    assert cert.verify() is False


def test_missing_B_cannot_certify():
    dual = DivergenceFreeDual(np.array([1.0, 1.0, 1.0]), None)
    cert = PhiCertificate(
        phi1=3.0,
        residual=EdgeCochain(np.array([1.0, 1.0, 1.0])),
        dual=dual,
        dual_value=3.0,
        B=None,
    )
    assert cert.verify() is False




def test_weighted_reduces_to_unweighted_at_unit_weights():
    B = _triangle_B()
    omega = np.array([1.0, 1.0, 1.0])
    _, _, unw = solve_phi(B, omega)
    _, _, unit = solve_phi(B, omega, weights=np.array([1.0, 1.0, 1.0]))
    assert abs(unw.phi1 - unit.phi1) < 1e-9
    assert unit.verify() is True


def test_weighted_phi1_concentrates_on_cheap_edges():
    B = _triangle_B()
    omega = np.array([1.0, 1.0, 1.0])
    _, _, unw = solve_phi(B, omega)
    assert abs(unw.phi1 - 3.0) < 1e-6
    w = np.array([2.0, 1.0, 1.0])
    _, _, cert = solve_phi(B, omega, weights=w)
    assert abs(cert.phi1 - 3.0) < 1e-6
    assert np.all(np.abs(cert.dual.values) <= w + 1e-7)
    assert cert.verify() is True


def test_weighted_phi1_is_weight_sensitive():
    B = _triangle_B()
    omega = np.array([1.0, 1.0, 1.0])
    _, _, base = solve_phi(B, omega, weights=np.array([1.0, 1.0, 1.0]))
    _, _, scaled = solve_phi(B, omega, weights=np.array([3.0, 3.0, 3.0]))
    assert abs(base.phi1 - 3.0) < 1e-6
    assert abs(scaled.phi1 - 9.0) < 1e-6
    assert scaled.verify() is True


def test_negative_weights_rejected():
    B = _triangle_B()
    omega = np.array([1.0, 1.0, 1.0])
    with pytest.raises(ValueError):
        solve_phi(B, omega, weights=np.array([-1.0, 1.0, 1.0]))


def test_weights_length_mismatch_rejected():
    B = _triangle_B()
    omega = np.array([1.0, 1.0, 1.0])
    with pytest.raises(ValueError):
        solve_phi(B, omega, weights=np.array([1.0, 1.0]))


