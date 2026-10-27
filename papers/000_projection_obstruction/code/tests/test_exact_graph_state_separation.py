"""Tests for Exact Graph-State Product Separation & Stability (Requirement R7).

Verifies:
- Analytical Cardano cubic root r of r^3 + r = 1 and residual enclosure.
- Single-qubit and multi-qubit optimal symmetric mixed product state sigma.
- Density matrix properties: Hermitian, unit trace, positive semidefinite, strictly mixed.
- Bloch vector interiority: radius r*sqrt(2) < 1.
- Exact minimax separation on cycle graph states: inf_{sigma} d_{O_n}(rho(t_*), sigma) = r.
- Balanced coordinate distance: |Delta K| = |Delta X| = |Delta Z| = r.
- Suboptimality of any competing product states (minimax tightness).
- Linear perturbation stability bound: d_{O_n}(rho, P_n) >= max(0, r - eta).
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

_code_dir = Path(__file__).resolve().parents[1]
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

import exact_graph_state_separation as egss  # noqa: E402


class TestCardanoRootFixture:
    """Verifies the algebraic and numerical properties of the Cardano cubic root."""

    def test_cardano_root_formula_and_precision(self):
        """Analytical radical formula matches known decimal value to < 1e-15."""
        rad = math.sqrt(93.0)
        cbrt = (108.0 + 12.0 * rad) ** (1.0 / 3.0)
        expected = cbrt / 6.0 - 2.0 / cbrt
        assert math.isclose(egss.CARDANO_CUBIC_ROOT_R, expected, rel_tol=1e-15)
        assert math.isclose(egss.CARDANO_CUBIC_ROOT_R, 0.6823278038280193, rel_tol=1e-14)

    def test_polynomial_residual_zero(self):
        """r^3 + r - 1 is zero to floating point precision."""
        r = egss.CARDANO_CUBIC_ROOT_R
        res = egss.cardano_root_residual(r)
        assert abs(res) < 1e-15
        assert egss.verify_cardano_root(tol=1e-14)

    def test_root_uniqueness_on_reals(self):
        """f(x) = x^3 + x - 1 has strictly positive derivative on R (unique real root)."""
        r = egss.CARDANO_CUBIC_ROOT_R
        # f'(x) = 3 x^2 + 1 >= 1 for all real x
        derivative = 3.0 * (r**2) + 1.0
        assert derivative >= 1.0
        # Test values around root
        delta = 1e-4
        assert egss.cardano_root_residual(r - delta) < 0.0
        assert egss.cardano_root_residual(r + delta) > 0.0

    def test_cardano_root_algebraic_identities(self):
        """Algebraic identities: r^3 = 1 - r and 1 - r^3 = r."""
        r = egss.CARDANO_CUBIC_ROOT_R
        r3 = r**3
        assert math.isclose(r3, 1.0 - r, rel_tol=1e-14)
        assert math.isclose(1.0 - r3, r, rel_tol=1e-14)


class TestOptimalProductState:
    """Verifies construction and validity of optimal product state sigma."""

    def test_single_qubit_sigma_properties(self):
        """Single-qubit sigma_1 is Hermitian, unit trace, PSD, and interior to Bloch sphere."""
        r = egss.CARDANO_CUBIC_ROOT_R
        sigma_1 = egss.single_qubit_sigma(r)
        assert sigma_1.shape == (2, 2)

        # Validity check
        valid, msg = egss.verify_state_validity(sigma_1)
        assert valid, msg

        # Analytical eigenvalues: (1 +- r*sqrt(2)) / 2
        radius = egss.bloch_vector_radius(r)
        assert radius < 1.0
        assert math.isclose(radius, r * math.sqrt(2.0), rel_tol=1e-14)

        eigvals = np.linalg.eigvalsh(sigma_1)
        expected_eigs = sorted([(1.0 - radius) / 2.0, (1.0 + radius) / 2.0])
        assert np.allclose(eigvals, expected_eigs, atol=1e-14)
        assert all(e > 0.0 for e in eigvals)

        # Strictly mixed state
        purity = float(np.real(np.trace(sigma_1 @ sigma_1)))
        assert 0.0 < purity < 1.0
        assert math.isclose(purity, (1.0 + radius**2) / 2.0, rel_tol=1e-14)

    def test_multi_qubit_sigma_validity(self):
        """Multi-qubit sigma is a valid density matrix for n = 2, 3, 4, 5."""
        for n in (2, 3, 4, 5):
            sigma_n = egss.optimal_product_state_sigma(n)
            dim = 1 << n
            assert sigma_n.shape == (dim, dim)
            valid, msg = egss.verify_state_validity(sigma_n)
            assert valid, f"n={n}: {msg}"

    def test_operator_expectations_under_optimal_sigma(self):
        """Expectations under sigma match exact theoretical values: <X> = -r, <Z> = r, <K> = -r^3."""
        r = egss.CARDANO_CUBIC_ROOT_R
        n = 5
        sigma = egss.optimal_product_state_sigma(n)
        ops = egss.cycle_observation_operators(n)

        # Check <X_j> = -r
        for x_op in ops["X"]:
            val = float(np.real(np.trace(sigma @ x_op)))
            assert math.isclose(val, -r, rel_tol=1e-12)

        # Check <Z_j> = r
        for z_op in ops["Z"]:
            val = float(np.real(np.trace(sigma @ z_op)))
            assert math.isclose(val, r, rel_tol=1e-12)

        # Check <K_j> = <Z_{j-1} X_j Z_{j+1}> = (r)(-r)(r) = -r^3
        for k_op in ops["K"]:
            val = float(np.real(np.trace(sigma @ k_op)))
            assert math.isclose(val, -(r**3), rel_tol=1e-12)


class TestExactMinimaxSeparation:
    """Verifies minimax separation on cycle graph states."""

    def test_exact_distance_balance(self):
        """All three observation coordinate distances exactly equal r at optimal sigma."""
        r = egss.CARDANO_CUBIC_ROOT_R
        diff_k = 1.0 - (r**3)  # |-1 - (-r^3)|
        diff_x = r  # |0 - (-r)|
        diff_z = r  # |0 - r|

        assert math.isclose(diff_k, r, rel_tol=1e-14)
        assert math.isclose(diff_x, r, rel_tol=1e-14)
        assert math.isclose(diff_z, r, rel_tol=1e-14)

        dist = egss.exact_graph_state_product_distance(num_qubits=5)
        assert math.isclose(dist, r, rel_tol=1e-14)

    def test_suboptimality_of_competing_states(self):
        """Any product state with parameter r' != r incurs strictly larger observational distance."""
        r_optimal = egss.CARDANO_CUBIC_ROOT_R

        # Perturb single-qubit parameter r' in both directions
        for r_cand in (0.4, 0.5, 0.6, 0.65, 0.7, 0.75, 0.8):
            diff_k = 1.0 - (r_cand**3)
            diff_xz = r_cand
            cand_dist = max(diff_k, diff_xz)
            assert cand_dist >= r_optimal, f"Candidate {r_cand} beat optimal {r_optimal}"
            if not math.isclose(r_cand, r_optimal, abs_tol=1e-6):
                assert cand_dist > r_optimal + 1e-5

    def test_minimax_certificate_generation(self):
        """Minimax separation certificate validates with verified status and zero gap."""
        cert = egss.generate_minimax_certificate()
        assert cert.status == "verified"
        assert cert.is_tight
        assert cert.is_interior
        assert cert.authority_effect == "None"
        assert math.isclose(cert.minimax_distance, egss.CARDANO_CUBIC_ROOT_R, rel_tol=1e-14)
        assert abs(cert.polynomial_residual) < 1e-14


class TestLinearStabilityBounds:
    """Verifies linear stability lower bound under observational perturbations."""

    def test_stability_bound_formula(self):
        """Bound is r - eta for eta < r, and 0 for eta >= r."""
        r = egss.CARDANO_CUBIC_ROOT_R
        assert math.isclose(egss.linear_stability_lower_bound(0.0), r, rel_tol=1e-14)
        assert math.isclose(egss.linear_stability_lower_bound(0.05), r - 0.05, rel_tol=1e-14)
        assert math.isclose(egss.linear_stability_lower_bound(0.2), r - 0.2, rel_tol=1e-14)
        assert egss.linear_stability_lower_bound(0.8) == 0.0
        assert egss.linear_stability_lower_bound(1.5) == 0.0

    def test_stability_bound_negative_eta_raises(self):
        """Negative eta is rejected as invalid noise."""
        with pytest.raises(ValueError):
            egss.linear_stability_lower_bound(-0.01)

    def test_stability_verification_on_noisy_graph_state(self):
        """Verifies linear stability bound on slightly perturbed state."""
        n = 5
        rho_graph = egss.cycle_graph_state_rho(n)
        eta = 0.05
        # Perturb with depolarizing noise (1 - p) rho + p (I / 2^n)
        p = 0.04
        dim = 1 << n
        eye_n = np.eye(dim, dtype=np.complex128) / float(dim)
        perturbed_state = (1.0 - p) * rho_graph + p * eye_n

        # Verify stability
        assert egss.verify_linear_stability(perturbed_state, eta, num_qubits=n)


def test_rational_isolating_interval():
    """Verify Review Finding 7 exact rational isolating interval [682327803/10^9, 682327804/10^9]."""
    assert egss.verify_rational_isolating_interval() is True


def test_universal_product_lower_bound_certification():
    """Verify Review Finding 7 universal product lower bound delta >= r."""
    res = egss.certify_universal_product_lower_bound()
    assert res["status"] == "pass"
    assert res["is_interval_verified"] is True
    assert res["universal_bound_holds"] is True
    assert res["sub_root_violates"] is True
    # Verify backward-compatibility alias
    assert egss.prove_universal_product_lower_bound() == res


def test_minimax_certificate_updated_fields():
    """Verify certificate includes rational isolating interval and universal proof status."""
    cert = egss.generate_minimax_certificate()
    assert cert.status == "verified"
    assert cert.universal_lower_bound_proved is True
    assert cert.rational_isolating_interval == (
        "682327803/1000000000",
        "170581951/250000000",
    )
