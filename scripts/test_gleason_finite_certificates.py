#!/usr/bin/env python3
"""Unit tests for `scripts/verify_gleason_finite_certificates.py`."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_gleason_finite_certificates as cert


class TestGleasonFiniteCertificates(unittest.TestCase):
    def test_verify_all_certificates_passes(self) -> None:
        receipt = cert.verify_all_certificates()
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["frames_verified"], 21)
        self.assertEqual(receipt["projection_identity_pairs_verified"], 81)
        self.assertTrue(receipt["two_frame_meridian_antisymmetry_verified"])

    def test_is_frame_rejects_non_orthogonal_or_zero(self) -> None:
        self.assertFalse(
            cert.is_frame(cert.TOMO_E1, cert.TOMO_E12, cert.TOMO_E3)
        )
        self.assertFalse(
            cert.is_frame(
                cert.GVec.real(0, 0, 0), cert.TOMO_E2, cert.TOMO_E3
            )
        )

    def test_exact_projection_identity(self) -> None:
        u = cert.WITNESS_111
        v0 = cert.WITNESS_P7
        c = cert.proj_scalar(u, v0)
        lhs = cert.dist_sq_vec(u.smul(c), v0)
        rhs = v0.norm_sq() * cert.ray_sin_sq(u, v0)
        self.assertEqual(lhs, rhs)
        self.assertLessEqual(
            cert.ray_sin_sq(u, v0), cert.dist_sq_vec(u, v0) / v0.norm_sq()
        )

    def test_two_frame_meridian_antisymmetry(self) -> None:
        for t_int in (1, 3, 9, 27, 81):
            t = Fraction(t_int)
            w_t = cert.meridian_approach_e1(t)
            z_t = cert.meridian_approach_e23(t)
            self.assertTrue(cert.is_frame(w_t, z_t, cert.PARTNER_E23_MINUS))
            for fn in (cert.s3, cert.s3_lead_x, cert.s3_lead_all):
                lhs = fn(cert.WITNESS_111) + fn(cert.WITNESS_NEG211)
                rhs = fn(w_t) + fn(z_t)
                self.assertEqual(lhs, Fraction(0))
                self.assertEqual(rhs, Fraction(0))

    def test_fixed_anchor_prime_valuation_obstruction(self) -> None:
        even_v3_probes = [
            cert.GVec.real(1, Fraction(1, 2**k), 0)
            for k in range(1, 6)
        ]
        for y in even_v3_probes:
            self.assertEqual(cert.vp_rat(3, y.norm_sq()) % 2, 0)
            self.assertEqual(cert.s3(y), Fraction(0))
        self.assertEqual(cert.s3(cert.WITNESS_111), Fraction(1))

    def test_coordinate_plane_and_perturb_obstruction_via_s3_lead_all(self) -> None:
        coord_plane_probes = [
            cert.GVec.real(1, Fraction(1, 3), 0),
            cert.GVec.real(1, 0, Fraction(1, 3)),
            cert.GVec.real(0, 1, Fraction(1, 3)),
            cert.perturb_pos_ray(1),
            cert.perturb_pos_ray(2),
            cert.perturb_neg_ray(1),
        ]
        for y in coord_plane_probes:
            self.assertEqual(cert.s3_lead_all(y), Fraction(0))
        self.assertEqual(cert.s3_lead_all(cert.WITNESS_111), Fraction(1))

    def test_crt_collision_approaches_e1_with_s3_lead_all_one(self) -> None:
        for m in range(6):
            u_m = cert.crt_approach_e1(m)
            self.assertEqual(cert.s3_lead_all(u_m), Fraction(1))
            self.assertLessEqual(
                cert.ray_sin_sq(u_m, cert.TOMO_E1),
                Fraction(2, (1 + 9 * (m + 1)) ** 2),
            )

    def test_dedekind_ray_cut_scale_invariance_and_jump(self) -> None:
        u_hi = cert.GVec.real(85, 100, 0)
        u_lo = cert.GVec.real(86, 100, 0)
        scalar = cert.GaussRat.of(Fraction(3, 7), Fraction(-2, 5))
        self.assertEqual(cert.dedekind_ray_cut(u_hi), Fraction(1))
        self.assertEqual(cert.dedekind_ray_cut(u_hi.smul(scalar)), Fraction(1))
        self.assertEqual(cert.dedekind_ray_cut(u_lo), Fraction(0))
        self.assertEqual(cert.dedekind_ray_cut(u_lo.smul(scalar)), Fraction(0))
        self.assertLess(
            cert.ray_sin_sq(u_hi, u_lo), Fraction(1, 10000)
        )


if __name__ == "__main__":
    unittest.main()
