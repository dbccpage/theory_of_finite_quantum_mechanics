"""U1 PhiCertificate.verify() + weighted Phi1 (S1 L204) faithfulness tests."""

import numpy as np
import pytest

from omega_engine.crates.solver.solv_phi_l1_lp import solve_phi
from omega_engine.crates.linear_algebra_theory.dual_certificate import DivergenceFreeDual, PhiCertificate
from omega_engine.crates.linear_algebra_theory.l1_seminorm import EdgeCochain


def _triangle_B():
    # Incidence (E=3, V=3) for 0->1->2->0.
    return np.array(
        [
            [-1.0, 1.0, 0.0],
            [0.0, -1.0, 1.0],
            [1.0, 0.0, -1.0],
        ]
    )


# ---------------------------------------------------------------------------
# U1: verify() True on a tight optimal certificate.
# ---------------------------------------------------------------------------


def test_certificate_verifies_on_cycle():
    B = _triangle_B()
    omega = np.array([1.0, 1.0, 1.0])  # cycle; Phi1 = 3, dual phi = [1,1,1] tight.
    _, _, cert = solve_phi(B, omega)
    assert abs(cert.phi1 - 3.0) < 1e-6
    assert cert.verify() is True
    assert cert.certified is True
    assert abs(cert.duality_gap) <= cert.tol


def test_certificate_verifies_on_exact():
    B = _triangle_B()
    omega = np.array([3.0, 2.0, -5.0])  # exact coboundary; Phi1 = 0.
    _, _, cert = solve_phi(B, omega)
    assert cert.phi1 < 1e-6
    assert cert.verify() is True


# ---------------------------------------------------------------------------
# U1: verify() False when the dual is loosened (suboptimal / infeasible).
# ---------------------------------------------------------------------------


def test_loosened_dual_not_certified():
    B = _triangle_B()
    omega = np.array([1.0, 1.0, 1.0])
    _, _, good = solve_phi(B, omega)
    # Replace the dual with a suboptimal (feasible but not tight) witness phi=0.
    bad_dual = DivergenceFreeDual(np.zeros(3), None)
    loosened = PhiCertificate(
        phi1=good.phi1,
        residual=good.residual,
        dual=bad_dual,
        dual_value=0.0,  # <phi, omega> = 0 != phi1 = 3 -> gap not tight
        B=B,
        tol=1e-6,
        weights=None,
    )
    assert loosened.verify() is False
    assert loosened.certified is False


def test_infeasible_dual_not_certified():
    B = _triangle_B()
    omega = np.array([1.0, 1.0, 1.0])
    # Dual that is NOT divergence-free (B.T phi != 0): phi=[1,0,0].
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
    # Without B, verify() refuses to certify (cannot re-check feasibility).
    dual = DivergenceFreeDual(np.array([1.0, 1.0, 1.0]), None)
    cert = PhiCertificate(
        phi1=3.0,
        residual=EdgeCochain(np.array([1.0, 1.0, 1.0])),
        dual=dual,
        dual_value=3.0,
        B=None,
    )
    assert cert.verify() is False


# ---------------------------------------------------------------------------
# Weighted Phi1: reduces to unweighted at unit weights; scales with weights.
# ---------------------------------------------------------------------------


def test_weighted_reduces_to_unweighted_at_unit_weights():
    B = _triangle_B()
    omega = np.array([1.0, 1.0, 1.0])
    _, _, unw = solve_phi(B, omega)
    _, _, unit = solve_phi(B, omega, weights=np.array([1.0, 1.0, 1.0]))
    assert abs(unw.phi1 - unit.phi1) < 1e-9
    assert unit.verify() is True


def test_weighted_phi1_concentrates_on_cheap_edges():
    B = _triangle_B()
    omega = np.array([1.0, 1.0, 1.0])  # irreducible cycle (integrates to 3).
    # Unit weights: Phi1 = 3 (mass spread, |h0|+|h1|+|h2| = 3).
    _, _, unw = solve_phi(B, omega)
    assert abs(unw.phi1 - 3.0) < 1e-6
    # With edge 0 made EXPENSIVE (w0=2), the LP pushes the irreducible cycle mass
    # (=3, fixed) onto the cheap edges, so weighted Phi1 stays 3 (not 6): the
    # cycle value is invariant but its placement minimizes weighted cost.
    w = np.array([2.0, 1.0, 1.0])
    _, _, cert = solve_phi(B, omega, weights=w)
    assert abs(cert.phi1 - 3.0) < 1e-6
    # Dual witness must satisfy the weighted box |phi_e| <= w_e.
    assert np.all(np.abs(cert.dual.values) <= w + 1e-7)
    assert cert.verify() is True


def test_weighted_phi1_is_weight_sensitive():
    # The triangle cycle has fixed holonomy 3; the irreducible residual can be
    # concentrated on ONE edge, so weighted Phi1 = 3 * min_e(w_e). Uniform
    # scaling by 3 therefore triples the value -> a genuine weight dependence.
    B = _triangle_B()
    omega = np.array([1.0, 1.0, 1.0])
    _, _, base = solve_phi(B, omega, weights=np.array([1.0, 1.0, 1.0]))
    _, _, scaled = solve_phi(B, omega, weights=np.array([3.0, 3.0, 3.0]))
    assert abs(base.phi1 - 3.0) < 1e-6
    assert abs(scaled.phi1 - 9.0) < 1e-6  # 3 * min(3,3,3) = 9 != unweighted 3
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


