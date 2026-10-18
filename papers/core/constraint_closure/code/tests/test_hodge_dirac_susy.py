"""Tests for the SP2 finite Hodge-Dirac matrix fixtures.

AuthorityEffect: None.
"""

import sys
import os

import numpy as np
import pytest

from hodge_dirac_susy import (
    build_operators_single_simplex,
    build_operators_glued_triangles,
    build_dirac_operator,
    compute_laplacians,
    verify_susy_single_simplex,
    verify_spectral_splitting_glued,
)


class TestNilpotency:
    def test_d1_d0_is_zero(self):
        d0, d1 = build_operators_single_simplex()
        assert np.allclose(d1 @ d0, 0), "d1 d0 != 0: nilpotency violated"

    def test_glued_nilpotency(self):
        d0, d1 = build_operators_glued_triangles()
        assert np.allclose(d1 @ d0, 0), "d1 d0 != 0 on glued triangles"


class TestDiracOperator:
    def test_self_adjoint(self):
        d0, d1 = build_operators_single_simplex()
        D = build_dirac_operator(d0, d1)
        assert np.allclose(D, D.T), "D is not self-adjoint"

    def test_anticommutes_with_grading(self):
        d0, d1 = build_operators_single_simplex()
        D = build_dirac_operator(d0, d1)
        n_even = 3 + 1  # n_vert + n_face
        n_odd = 3  # n_edge
        Gamma = np.diag([1.0] * n_even + [-1.0] * n_odd)
        assert np.allclose(D @ Gamma + Gamma @ D, 0), "{D, Γ} != 0"

    def test_d_squared_equals_block_laplacian(self):
        result = verify_susy_single_simplex()
        assert result["D2_matches_block_diagonal"]


class TestLaplaciansSingleSimplex:
    def test_delta_1_filled_is_3I(self):
        d0, d1 = build_operators_single_simplex()
        laps = compute_laplacians(d0, d1)
        assert np.allclose(laps["Delta_1_filled"], 3 * np.eye(3))

    def test_even_eigenvalues(self):
        d0, d1 = build_operators_single_simplex()
        laps = compute_laplacians(d0, d1)
        expected = sorted([0, 3, 3, 3])
        actual = sorted(np.round(laps["evals_even"], 10).tolist())
        assert np.allclose(actual, expected), f"even evals {actual} != {expected}"

    def test_odd_eigenvalues(self):
        d0, d1 = build_operators_single_simplex()
        laps = compute_laplacians(d0, d1)
        expected = [3, 3, 3]
        actual = sorted(np.round(laps["evals_1"], 10).tolist())
        assert np.allclose(actual, expected), f"odd evals {actual} != {expected}"

    def test_witten_index(self):
        d0, d1 = build_operators_single_simplex()
        laps = compute_laplacians(d0, d1)
        assert laps["witten_index"] == 1, f"W = {laps['witten_index']} != 1"

    def test_matched_nonzero_spectra(self):
        """Non-zero spectra of even and odd sectors must match as {3, 3, 3}."""
        d0, d1 = build_operators_single_simplex()
        laps = compute_laplacians(d0, d1)
        nonzero_even = sorted([v for v in laps["evals_even"] if abs(v) > 1e-10])
        nonzero_odd = sorted([v for v in laps["evals_1"] if abs(v) > 1e-10])
        assert np.allclose(nonzero_even, nonzero_odd), (
            f"non-zero spectra mismatch: even={nonzero_even}, odd={nonzero_odd}"
        )


class TestH1RankDrop:
    def test_h1_drops_from_1_to_0(self):
        result = verify_susy_single_simplex()
        assert result["h1_hollow"] == 1, f"H^1(C3) = {result['h1_hollow']} != 1"
        assert result["h1_filled"] == 0, f"H^1(Δ^2) = {result['h1_filled']} != 0"


class TestSpectralSplitting:
    def test_glued_triangles_eigenvalues(self):
        result = verify_spectral_splitting_glued()
        expected = [2.0, 2.0, 4.0, 4.0, 4.0]
        assert np.allclose(result["evals_1"], expected), (
            f"evals = {result['evals_1']} != {expected}"
        )

    def test_glued_mass_gap_is_2(self):
        result = verify_spectral_splitting_glued()
        assert abs(result["mass_gap"] - 2.0) < 1e-10

    def test_glued_is_not_scalar_isotropic(self):
        result = verify_spectral_splitting_glued()
        assert not result["is_scalar_isotropic"], (
            "Δ_1^filled should NOT be scalar isotropic on glued triangles"
        )
