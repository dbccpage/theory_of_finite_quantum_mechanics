"""Unit tests for the Phase 3 Gleason continuum-shadow verifier and crosswalk."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_gleason_continuum_shadow as vcs


class TestGleasonContinuumShadow(unittest.TestCase):
    def test_crosswalk_covers_all_eight_historical_components(self) -> None:
        cw = vcs.build_crosswalk()
        names = [item["component"] for item in cw]
        self.assertEqual(names, ["FOC", "MUR", "CS", "CS_Q", "Q", "A", "OR", "FDA"])
        for item in cw:
            self.assertTrue(item["current_rust_modules"])
            self.assertTrue(item["current_lean_modules"])
            self.assertTrue(item["gleason_shadow_symbols"])
            self.assertTrue(item["dag_nodes"])

    def test_nine_ray_section_and_quadratic_recovery(self) -> None:
        rho = vcs.HermForm3(
            d1=Fraction(1, 2),
            d2=Fraction(1, 3),
            d3=Fraction(1, 6),
            a12=Fraction(1, 5),
            a13=Fraction(-1, 7),
            a23=Fraction(2, 11),
            b12=Fraction(-1, 9),
            b13=Fraction(3, 13),
            b23=Fraction(-2, 15),
        )
        prof = vcs.nine_ray_profile(lambda v: vcs.quad_ray(rho, v))
        self.assertEqual(vcs.decode_nine_ray_profile(prof), rho)
        for v in vcs.ANCHOR_RAYS + (vcs.WITNESS_111,):
            self.assertEqual(
                vcs.quad_ray(vcs.decode_nine_ray_profile(prof), v),
                vcs.quad_ray(rho, v),
            )

    def test_nonquadratic_aliasing_witnesses(self) -> None:
        max_mixed = vcs.HermForm3(
            Fraction(1, 3), Fraction(1, 3), Fraction(1, 3),
            Fraction(0), Fraction(0), Fraction(0),
            Fraction(0), Fraction(0), Fraction(0),
        )
        p_ex = vcs.nine_ray_profile(vcs.exotic_qi3)
        p_mm = vcs.nine_ray_profile(lambda v: vcs.quad_ray(max_mixed, v))
        self.assertEqual(p_ex, p_mm)
        self.assertEqual(vcs.profile_l1_dist(p_ex, p_mm), Fraction(0))
        self.assertNotEqual(vcs.exotic_qi3(vcs.WITNESS_111), vcs.quad_ray(max_mixed, vcs.WITNESS_111))

    def test_quantitative_stability_and_sharp_27_eps_bound(self) -> None:
        eps = Fraction(3, 100)
        pert = (eps, eps, eps, -eps, -eps, -eps, -eps, -eps, -eps)
        delta_form = vcs.decode_nine_ray_profile(pert)
        self.assertEqual(delta_form.coeff_norm(), 27 * eps)
        self.assertEqual(abs(delta_form.tr()), 3 * eps)
        for v in vcs.ANCHOR_RAYS + (vcs.WITNESS_111,):
            self.assertLessEqual(abs(vcs.quad_ray(delta_form, v)), 27 * eps)

    def test_quantitative_rayleigh_continuity_and_modulus(self) -> None:
        rho = vcs.HermForm3(
            d1=Fraction(3, 5),
            d2=Fraction(1, 5),
            d3=Fraction(1, 5),
            a12=Fraction(1, 4),
            a13=Fraction(0),
            a23=Fraction(-1, 8),
            b12=Fraction(1, 8),
            b13=Fraction(-1, 4),
            b23=Fraction(0),
        )
        eps = Fraction(1, 4)
        mod = vcs.rational_ray_modulus(rho.coeff_norm(), eps)
        self.assertGreater(mod, Fraction(0))
        # Degenerate B <= 0 cases return 1
        self.assertEqual(vcs.rational_ray_modulus(Fraction(0), eps), Fraction(1))
        self.assertEqual(vcs.rational_ray_modulus(Fraction(-2), eps), Fraction(1))
        # Near ray pair within modulus
        u = vcs.gv(1, 0, 0, 0, 0, 0)
        v = vcs.gv(100, 0, 1, 0, 0, 0)
        self.assertLess(vcs.ray_sin_sq(u, v), mod)
        self.assertLess(abs(vcs.quad_ray(rho, u) - vcs.quad_ray(rho, v)), eps)

    def test_verify_all_succeeds(self) -> None:
        receipt = vcs.verify_all()
        self.assertTrue(receipt["verified_claims"]["exact_descent_on_range_vs_unused_labels"])
        self.assertTrue(receipt["verified_claims"]["quantitative_nine_ray_stability"]["coeffNorm_sharpness_verified"])


if __name__ == "__main__":
    unittest.main()
