"""Unit and negative refusal tests for code/python/src/qm/u1_phase_completion.py.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction as Q
from pathlib import Path
import importlib
import sys
import types
import unittest

import pytest

pkg = types.ModuleType("staged_qm_u1")
pkg.__path__ = [str(Path(__file__).resolve().parents[1] / "src/qm")]
sys.modules[pkg.__name__] = pkg
m = importlib.import_module("staged_qm_u1.u1_phase_completion")


class CayleyParameterizationTests(unittest.TestCase):
    def test_affine_cayley_lands_on_unit_circle_and_inverts(self) -> None:
        for t in (Q(0), Q(1), Q(-1), Q(1, 2), Q(-1, 3), Q(2, 5), Q(7, 4)):
            re, im = m.affine_cayley(t)
            self.assertTrue(m.is_unit_circle(re, im))
            self.assertEqual(m.inverse_cayley(re, im), t)
        self.assertEqual(m.affine_cayley(Q(1, 2)), (Q(3, 5), Q(4, 5)))

    def test_affine_cayley_tangent_group_law_and_pole_collision(self) -> None:
        p1 = m.affine_cayley(Q(1, 2))
        p2 = m.affine_cayley(Q(1, 3))
        prod = m.circle_mul(p1[0], p1[1], p2[0], p2[1])
        t12 = m.affine_cayley_mul_param(Q(1, 2), Q(1, 3))
        self.assertEqual(t12, Q(1))
        self.assertEqual(m.affine_cayley(t12), prod)
        self.assertIsNone(m.affine_cayley_mul_param(Q(1), Q(1)))
        self.assertIsNone(m.affine_cayley_mul_param(Q(2), Q(1, 2)))

    def test_projective_cayley_bijection_and_scale_invariance(self) -> None:
        self.assertEqual(m.projective_cayley(0, 1), (Q(-1), Q(0)))
        self.assertEqual(m.projective_cayley(0, -5), (Q(-1), Q(0)))
        self.assertEqual(m.projective_cayley(2, 1), (Q(3, 5), Q(4, 5)))
        self.assertEqual(m.projective_cayley(-6, -3), (Q(3, 5), Q(4, 5)))
        for pt in ((Q(1), Q(0)), (Q(-1), Q(0)), (Q(0), Q(1)), (Q(3, 5), Q(4, 5)), (Q(-5, 13), Q(12, 13))):
            u, v = m.inverse_projective_cayley(pt[0], pt[1])
            self.assertEqual(m.projective_cayley(u, v), pt)

    def test_projective_mul_homomorphism_across_south_pole(self) -> None:
        u, v = m.projective_mul(1, 1, 1, 1)
        self.assertEqual((u, v), (Q(0), Q(2)))
        self.assertEqual(m.projective_cayley(u, v), (Q(-1), Q(0)))
        u2, v2 = m.projective_mul(2, 1, 2, -1)
        self.assertEqual(m.projective_cayley(u2, v2), (Q(1), Q(0)))

    def test_cayley_negative_refusals(self) -> None:
        with pytest.raises(ValueError, match="south-pole"):
            m.inverse_cayley(Q(-1), Q(0))
        with pytest.raises(ValueError, match="unit circle"):
            m.inverse_cayley(Q(1), Q(1))
        with pytest.raises(ValueError, match="unit circle"):
            m.inverse_projective_cayley(Q(1, 2), Q(1, 2))
        with pytest.raises(ValueError, match="unit circle"):
            m.circle_mul(Q(1), Q(1), Q(1), Q(0))
        with pytest.raises(ValueError, match="homogeneous origin"):
            m.projective_cayley(0, 0)
        with pytest.raises(ValueError, match="homogeneous origin"):
            m.projective_mul(0, 0, 1, 2)
        with pytest.raises(ValueError, match="homogeneous origin"):
            m.projective_mul(1, 2, 0, 0)


class HalfAngleObstructionTests(unittest.TestCase):
    def test_five_adic_valuation_factorization(self) -> None:
        for n in (1, -1, 2, 4, 5, -5, 20, 25, 125, -375, 44, -117):
            v5, unit = m.five_adic_valuation(n)
            self.assertEqual(n, (5**v5) * unit)
            self.assertNotEqual(unit % 5, 0)
        with pytest.raises(ValueError, match="nonzero integer"):
            m.five_adic_valuation(0)

    def test_four_fifths_not_square_certificate(self) -> None:
        for num, den in ((0, 1), (1, 1), (2, 3), (9, 10), (179, 200), (-38, 43)):
            c = m.certify_four_fifths_not_square(num, den)
            self.assertTrue(c["obstructed"])
            self.assertTrue(c["parity_disjoint"])
            self.assertGreaterEqual(c["abs_residual"], 1)
            self.assertEqual(c["rhs_v5"] % 2, 0)
            if num != 0:
                self.assertEqual(c["lhs_v5"] % 2, 1)
        with pytest.raises(ValueError, match="nonzero denominator"):
            m.certify_four_fifths_not_square(2, 0)

    def test_u345_no_rational_sqrt_certificate(self) -> None:
        for re, im in ((Q(2, 3), Q(1, 3)), (Q(3, 5), Q(4, 5)), (Q(9, 10), Q(9, 20)), (Q(0), Q(1))):
            c = m.certify_u345_no_rational_sqrt(re, im)
            self.assertTrue(c["half_sum_equals_re_sq"])
            self.assertFalse(c["matches_u345_and_unit"])
            self.assertTrue(c["obstructed"])


class PowerMapInjectivityTests(unittest.TestCase):
    def test_gauss_pow_34_exact_values_and_norm(self) -> None:
        self.assertEqual(m.gauss_pow_34(0), (1, 0))
        self.assertEqual(m.gauss_pow_34(1), (3, 4))
        self.assertEqual(m.gauss_pow_34(2), (-7, 24))
        self.assertEqual(m.gauss_pow_34(3), (-117, 44))
        self.assertEqual(m.gauss_pow_34(4), (-527, -336))
        with pytest.raises(ValueError, match="nonnegative exponent"):
            m.gauss_pow_34(-1)

    def test_u345_power_group_homomorphism(self) -> None:
        for j in range(-4, 5):
            for k in range(-4, 5):
                pj = m.u345_power(j)
                pk = m.u345_power(k)
                pjk = m.u345_power(j + k)
                self.assertEqual(m.circle_mul(pj[0], pj[1], pk[0], pk[1]), pjk)

    def test_power_injectivity_window_certificate(self) -> None:
        c = m.certify_power_injectivity_window(12)
        self.assertTrue(c["mod5_invariant_holds"])
        self.assertTrue(c["all_on_unit_circle"])
        self.assertEqual(c["tested_exponents"], 25)
        self.assertEqual(c["distinct_points"], 25)
        self.assertTrue(c["injective_on_window"])
        with pytest.raises(ValueError, match="max_n"):
            m.certify_power_injectivity_window(0)
        with pytest.raises(ValueError, match="max_n"):
            m.certify_power_injectivity_window(257)


class QuadSqrt5ExtensionTests(unittest.TestCase):
    def test_quad_sqrt5_field_arithmetic_and_inverse(self) -> None:
        x = m.QuadSqrt5(Q(2), Q(1))
        inv = m.quad_inv(x)
        self.assertEqual(m.quad_norm(x), Q(-1))
        self.assertEqual(m.quad_mul(x, inv), m.QuadSqrt5(Q(1), Q(0)))
        self.assertEqual(m.quad_mul(x, m.quad_conj(x)), m.QuadSqrt5(m.quad_norm(x), Q(0)))
        with pytest.raises(ValueError, match="zero element"):
            m.quad_inv(m.QuadSqrt5(Q(0), Q(0)))

    def test_u345_quad_sqrt_certificate_restores_half_angle(self) -> None:
        c = m.u345_quad_sqrt_certificate()
        self.assertTrue(c["squares_to_u345"])
        self.assertTrue(c["on_unit_circle"])
        self.assertTrue(c["requires_quadratic_extension"])
        self.assertEqual(c["w_sq_re"], ("3/5", "0"))
        self.assertEqual(c["w_sq_im"], ("4/5", "0"))


class CyclotomicTorsionTowerTests(unittest.TestCase):
    def test_torsion_phase_refinement_preserves_phase(self) -> None:
        for n, k, a in ((4, 3, 1), (6, 5, 11), (12, 7, -5)):
            c = m.refine_torsion_phase(n, k, a)
            self.assertTrue(c["phase_preserved"])
            self.assertEqual(c["base_phase"], c["refined_phase"])
        with pytest.raises(ValueError, match="positive"):
            m.refine_torsion_phase(0, 2, 1)
        with pytest.raises(ValueError, match="positive"):
            m.refine_torsion_phase(4, 0, 1)

    def test_divide_rat_phase_mod_one_is_m_divisible(self) -> None:
        for q_phase, div in ((Q(1, 3), 2), (Q(3, 5), 4), (Q(-7, 4), 5)):
            c = m.divide_rat_phase_mod_one(q_phase, div)
            self.assertTrue(c["all_in_unit_interval"])
            self.assertEqual(c["distinct_count"], div)
            self.assertTrue(c["all_multiply_to_q_mod_one"])
        with pytest.raises(ValueError, match="m_divisor"):
            m.divide_rat_phase_mod_one(Q(1, 2), 0)

    def test_fourth_roots_haar_character_orthogonality(self) -> None:
        for power in range(-8, 9):
            c = m.fourth_roots_haar_certificate(power)
            self.assertTrue(c["orthogonality_holds"])
            if power % 4 == 0:
                self.assertEqual((c["average_re"], c["average_im"]), ("1", "0"))
            else:
                self.assertEqual((c["average_re"], c["average_im"]), ("0", "0"))


class CauchyCompletionAndControlsTests(unittest.TestCase):
    def test_torsion_grid_cover_certificate(self) -> None:
        for q_phase in (Q(0), Q(1), Q(1, 3), Q(4, 5), Q(17, 29)):
            for n_grid in (1, 4, 10, 64):
                c = m.torsion_grid_cover_certificate(q_phase, n_grid)
                self.assertTrue(c["within_bound"])
        with pytest.raises(ValueError, match="q_phase"):
            m.torsion_grid_cover_certificate(Q(-1, 5), 8)
        with pytest.raises(ValueError, match="q_phase"):
            m.torsion_grid_cover_certificate(Q(6, 5), 8)
        with pytest.raises(ValueError, match="n_grid"):
            m.torsion_grid_cover_certificate(Q(1, 2), 0)

    def test_dyadic_sqrt5_interval_step_contracts_and_brackets(self) -> None:
        lo, hi = Q(2), Q(3)
        for _ in range(8):
            c = m.dyadic_sqrt5_interval_step(lo, hi)
            self.assertTrue(c["brackets_sqrt5"])
            self.assertTrue(c["brackets_four_fifths"])
            self.assertTrue(c["width_halved"])
            lo, hi = Q(c["new_lo"]), Q(c["new_hi"])
        self.assertEqual(hi - lo, Q(1, 256))
        with pytest.raises(ValueError, match="bracket"):
            m.dyadic_sqrt5_interval_step(Q(3), Q(4))
        with pytest.raises(ValueError, match="bracket"):
            m.dyadic_sqrt5_interval_step(Q(1), Q(2))

    def test_negative_controls_and_scalar_refusals(self) -> None:
        c = m.negative_controls_certificate()
        self.assertTrue(c["all_negative_controls_verified"])
        self.assertTrue(m.AUTHORITY_FENCE.startswith("AuthorityEffect None"))
        self.assertIn("20261020T223000Z_u1_phase_completion_lean", m.PROVENANCE)
        for bad in (1.5, True, "1/2"):
            with pytest.raises(ValueError):
                m.affine_cayley(bad)
        for bad_int in (1.0, False, Q(1, 2), "3"):
            with pytest.raises(ValueError):
                m.gauss_pow_34(bad_int)

    def test_circle_mul_group_laws_on_rational_pythagorean_triples(self) -> None:
        u = (Q(3, 5), Q(4, 5))
        v = (Q(5, 13), Q(12, 13))
        w = (Q(-8, 17), Q(15, 17))
        uv = m.circle_mul(u[0], u[1], v[0], v[1])
        vu = m.circle_mul(v[0], v[1], u[0], u[1])
        self.assertEqual(uv, vu)
        self.assertTrue(m.is_unit_circle(uv[0], uv[1]))
        uvw_left = m.circle_mul(uv[0], uv[1], w[0], w[1])
        vw = m.circle_mul(v[0], v[1], w[0], w[1])
        uvw_right = m.circle_mul(u[0], u[1], vw[0], vw[1])
        self.assertEqual(uvw_left, uvw_right)
        u_inv = (u[0], -u[1])
        self.assertEqual(m.circle_mul(u[0], u[1], u_inv[0], u_inv[1]), (Q(1), Q(0)))

    def test_quad_sqrt5_ring_identities_and_circle_group_closure(self) -> None:
        w = m.CircleQuadSqrt5(m.QuadSqrt5(Q(0), Q(2, 5)), m.QuadSqrt5(Q(0), Q(1, 5)))
        w_conj = m.CircleQuadSqrt5(w.re, m.QuadSqrt5(-w.im.a, -w.im.b))
        prod = m.circle_quad_mul(w, w_conj)
        self.assertEqual(prod, m.CircleQuadSqrt5(m.QuadSqrt5(Q(1), Q(0)), m.QuadSqrt5(Q(0), Q(0))))
        w4 = m.circle_quad_mul(m.circle_quad_mul(w, w), m.circle_quad_mul(w, w))
        self.assertEqual(
            w4,
            m.CircleQuadSqrt5(m.QuadSqrt5(Q(-7, 25), Q(0)), m.QuadSqrt5(Q(24, 25), Q(0))),
        )

    def test_provenance_lists_all_five_lean_modules(self) -> None:
        for mod_name in (
            "U1CayleyProjectiveCircle",
            "U1HalfAngleObstruction",
            "U1PythagoreanObstruction",
            "U1PowerMapInjectivity",
            "U1CyclotomicTorsionTower",
            "U1CauchyCircleCompletion",
            "U1ChebyshevCauchyBridge",
            "U1QuadraticTowerAndCayleyStone",
            "U1PhaseSynthesis",
        ):
            self.assertIn(mod_name, m.PROVENANCE)

    def test_chebyshev_polynomials_and_circle_power_bridge(self) -> None:
        c = m.chebyshev_circle_certificate(Q(3, 5), Q(4, 5), 10)
        self.assertTrue(c["chebyshev_matches_circle_powers"])
        self.assertTrue(c["pell_identity_holds_all_degrees"])
        self.assertEqual(m.chebyshev_t(2, Q(3, 5)), Q(-7, 25))
        self.assertEqual(Q(4, 5) * m.chebyshev_u(1, Q(3, 5)), Q(24, 25))
        with pytest.raises(ValueError, match="nonnegative"):
            m.chebyshev_t(-1, Q(1, 2))
        with pytest.raises(ValueError, match="nonnegative"):
            m.chebyshev_u(-1, Q(1, 2))
        with pytest.raises(ValueError, match="S\\^1\\(Q\\)"):
            m.chebyshev_circle_certificate(Q(1, 2), Q(1, 2), 4)
        with pytest.raises(ValueError, match="max_n"):
            m.chebyshev_circle_certificate(Q(3, 5), Q(4, 5), 0)

    def test_taylor_trig_enclosure_and_cayley_dyadic_approximants(self) -> None:
        for th in (Q(0), Q(1, 6), Q(1, 3), Q(1, 2), Q(3, 4), Q(1)):
            tc = m.taylor_trig_enclosure_certificate(th)
            self.assertTrue(tc["all_taylor_bounds_verified"])
            cd = m.cayley_dyadic_approx_certificate(th, 4)
            self.assertTrue(cd["strictly_on_unit_circle"])
        with pytest.raises(ValueError, match="theta"):
            m.taylor_trig_enclosure_certificate(Q(-1, 4))
        with pytest.raises(ValueError, match="theta"):
            m.taylor_trig_enclosure_certificate(Q(5, 4))
        with pytest.raises(ValueError, match="k_depth"):
            m.cayley_dyadic_approx_certificate(Q(1, 2), -1)

    def test_hermitian_qi_born_certificate(self) -> None:
        hc = m.hermitian_qi_born_certificate(
            Q(3, 5), Q(0), Q(0), Q(4, 5), Q(1, 2), Q(1, 2), Q(-1, 2), Q(1, 2)
        )
        self.assertTrue(hc["det_psi_zero"])
        self.assertEqual(hc["trace_psi"], "1")
        self.assertTrue(hc["born_pairing_matches_inner_mod_sq"])
        self.assertTrue(hc["sigma_y_orthogonal_to_real_sym"])

    def test_u345_quadratic_tower_certificate_arbitrary_2_pow_m_divisions(self) -> None:
        tc = m.u345_quadratic_tower_certificate(4)
        self.assertEqual(tc["level_0_radicand"], "4/5")
        self.assertTrue(tc["all_levels_on_circle"])
        self.assertTrue(tc["all_inverses_valid"])
        self.assertTrue(tc["all_two_pow_m_match_u345"])
        self.assertEqual(len(tc["levels"]), 5)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="max_level"):
            m.u345_quadratic_tower_certificate(0)
        with pytest.raises(ValueError, match="max_level"):
            m.u345_quadratic_tower_certificate(6)

    def test_cayley_hermitian_stone_certificate_regular_and_pole(self) -> None:
        cs_reg = m.cayley_hermitian_stone_certificate(
            Q(1, 2), Q(1, 3), Q(-1, 6), Q(1, 2), Q(1, 3)
        )
        self.assertTrue(cs_reg["denom_ge_one"])
        self.assertTrue(cs_reg["resolvent_valid"])
        self.assertTrue(cs_reg["unitary_valid"])
        self.assertTrue(cs_reg["det_is_one"])
        self.assertTrue(cs_reg["dagger_equals_neg_step"])
        self.assertTrue(cs_reg["steps_commute"])
        self.assertTrue(cs_reg["composition_law_valid"])
        self.assertFalse(cs_reg["pole_collision"])
        self.assertTrue(cs_reg["pauli_z_half_is_u345"])

        cs_pole = m.cayley_hermitian_stone_certificate(
            Q(3, 5), Q(4, 5), Q(0), Q(2, 1), Q(1, 2)
        )
        self.assertTrue(cs_pole["resolvent_valid"])
        self.assertTrue(cs_pole["unitary_valid"])
        self.assertTrue(cs_pole["composition_law_valid"])
        self.assertTrue(cs_pole["pole_collision"])


if __name__ == "__main__":
    unittest.main()
