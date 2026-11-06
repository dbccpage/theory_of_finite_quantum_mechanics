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
        self.assertEqual(receipt["frames_verified"], 22)
        self.assertEqual(receipt["projection_identity_pairs_verified"], 144)
        self.assertTrue(receipt["two_frame_meridian_antisymmetry_verified"])
        self.assertEqual(receipt["target1_general_anchor_meridian_checks"], 27)
        self.assertEqual(receipt["spherical_frame_pythagoras_checks"], 242)
        self.assertEqual(receipt["two_frame_cross_anchor_checks"], 88)
        self.assertTrue(receipt["witness_111_nine_anchor_isolation_verified"])
        self.assertTrue(receipt["witness_111_two_frame_fifth_ball_verified"])
        self.assertTrue(receipt["witness_neg211_one_eighth_isolation_verified"])
        self.assertTrue(receipt["perturbed_two_frame_bounce_back_verified"])
        self.assertTrue(receipt["witness_123_fifteen_ray_isolation_verified"])
        self.assertEqual(receipt["meridian_step_modulus_decomp_pairs_verified"], 122)

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

    def test_track_a_piron_soler_chain_and_universal_meridian_bridge(self) -> None:
        y = cert.GVec.real(0, Fraction(1, 3), Fraction(1, 2))
        self.assertTrue(cert.is_frame(cert.TOMO_E1, y, cert.eq_ortho(y)))
        self.assertTrue(
            cert.is_frame(
                cert.TOMO_E1.add(y), cert.eq_ortho(y), cert.meridian_ortho(y)
            )
        )
        self.assertEqual(
            cert.ray_sin_sq(cert.TOMO_E1.add(y), cert.TOMO_E1),
            cert.ray_sin_sq(cert.meridian_ortho(y), y),
        )
        lam = cert.GaussRat.of(Fraction(1, 2), Fraction(1, 3))
        lam_neg = cert.GaussRat.of(-Fraction(1, 2), -Fraction(1, 3))
        self.assertEqual(
            cert.ray_sin_sq(cert.piron_step(y, lam), cert.TOMO_E1.add(y)),
            cert.ray_sin_sq(cert.piron_partner(y, lam), cert.eq_ortho(y)),
        )
        f = cert.exotic_qi3
        slack = Fraction(1) - f(cert.TOMO_E1)
        self.assertEqual(
            f(cert.TOMO_E1.add(y)) + f(cert.meridian_ortho(y)),
            f(cert.TOMO_E1) + f(y),
        )
        self.assertEqual(
            f(cert.TOMO_E1.add(y)) + f(cert.TOMO_E1.add(cert.kelvin_eq(y))),
            f(cert.TOMO_E1) + f(y),
        )
        self.assertEqual(
            f(cert.piron_step(y, lam)) - f(cert.TOMO_E1.add(y)),
            f(cert.eq_ortho(y)) - f(cert.piron_partner(y, lam)),
        )
        self.assertEqual(
            f(cert.piron_step(y, lam)) + f(cert.piron_partner(y, lam)),
            f(cert.piron_step(y, lam_neg)) + f(cert.piron_partner(y, lam_neg)),
        )
        t1, t2, t3 = Fraction(1, 2), Fraction(1, 3), Fraction(1, 5)
        y1 = cert.eq_tangent_step(y, t1)
        y2 = cert.eq_tangent_step(y1, t2)
        y3 = cert.eq_tangent_step(y2, t3)
        self.assertLessEqual(
            f(cert.TOMO_E1.add(y3)) - f(cert.TOMO_E1.add(y)),
            f(cert.eq_ortho(y)) + f(cert.eq_ortho(y1)) + f(cert.eq_ortho(y2)),
        )
        self.assertLessEqual(
            f(cert.eq_ortho(y)) + f(cert.eq_ortho(y1)) + f(cert.eq_ortho(y2)),
            3 * slack,
        )
        self.assertEqual(
            f(cert.TOMO_E1.add(y3)) - f(cert.TOMO_E1.add(y)),
            (f(cert.eq_ortho(y)) - f(cert.piron_partner(y, cert.GaussRat.of(t1))))
            + (f(cert.eq_ortho(y1)) - f(cert.piron_partner(y1, cert.GaussRat.of(t2))))
            + (f(cert.eq_ortho(y2)) - f(cert.piron_partner(y2, cert.GaussRat.of(t3)))),
        )

    def test_track_b_irrational_locus_frame_stress_tests(self) -> None:
        # 1. Local constancy of dedekind_ray_cut near tomo_e1 and tomo_e2
        u_near_e1 = cert.crt_approach_e1(0)
        self.assertLess(cert.ray_sin_sq(u_near_e1, cert.TOMO_E1), Fraction(1, 2))
        self.assertEqual(cert.dedekind_ray_cut(u_near_e1), Fraction(0))
        u_near_e2 = cert.GVec.real(Fraction(1, 4), 1, Fraction(1, 4))
        self.assertLess(cert.ray_sin_sq(u_near_e2, cert.TOMO_E2), Fraction(1, 3))
        self.assertEqual(cert.dedekind_ray_cut(u_near_e2), Fraction(1))
        # 2. Failure of 3-frame additivity on (tomo_e3, tomo_e12, partner_e12_minus)
        self.assertEqual(
            cert.dedekind_ray_cut(cert.TOMO_E3)
            + cert.dedekind_ray_cut(cert.TOMO_E12)
            + cert.dedekind_ray_cut(cert.PARTNER_E12_MINUS),
            Fraction(0),
        )
        # 3. General two-frame Gaussian-norm latitude-halving cone-exit across super-cone rays
        for a_val, b_val in ((0, 1), (1, 2), (1, 3), (85, 100)):
            u_base = cert.gaussian_halving_base(a_val, b_val)
            u_pos = cert.gaussian_halving_pos(a_val, b_val)
            self.assertLess(
                3 * (u_pos.y.norm_sq() ** 2),
                u_pos.norm_sq() ** 2,
            )
            self.assertEqual(cert.dedekind_ray_cut(u_base), Fraction(1))
            self.assertEqual(cert.dedekind_ray_cut(cert.TOMO_E3), Fraction(0))
            self.assertEqual(cert.dedekind_ray_cut(u_pos), Fraction(0))
            self.assertNotEqual(
                2 * cert.dedekind_ray_cut(u_pos),
                cert.dedekind_ray_cut(u_base) + cert.dedekind_ray_cut(cert.TOMO_E3),
            )
        # 4. Global local-constancy radius certificate (dedekindRayCut_eventually_const)
        with self.assertRaises(ValueError):
            cert.dedekind_local_constancy_theta(cert.GVec.real(0, 0, 0))
        with self.assertRaises(ValueError):
            cert.dedekind_local_constancy_radius(cert.GVec.real(0, 0, 0))
        for v0 in (
            cert.GVec.real(85, 100, 0),
            cert.GVec.real(86, 100, 0),
            cert.WITNESS_111,
            cert.gaussian_halving_pos(1, 2),
        ):
            theta = cert.dedekind_local_constancy_theta(v0)
            delta = cert.dedekind_local_constancy_radius(v0)
            self.assertGreater(theta, Fraction(0))
            self.assertEqual(delta, theta * theta)
            step = theta / Fraction(4)
            for sx, sy, sz in ((1, -1, 1), (-1, 1, -1), (1, 1, 0)):
                v_pert = cert.GVec(
                    v0.x + cert.GaussRat.of(sx * step),
                    v0.y + cert.GaussRat.of(sy * step),
                    v0.z + cert.GaussRat.of(0, sz * step),
                )
                self.assertLess(cert.dist_sq_vec(v_pert, v0), delta)
                self.assertEqual(
                    cert.dedekind_ray_cut(v_pert), cert.dedekind_ray_cut(v0)
                )
        # 5. General-anchor orthogonal ray-distance Bessel bound & polar-cap disjointness
        anchors = (
            cert.TOMO_E1,
            cert.TOMO_E2,
            cert.TOMO_E12,
            cert.WITNESS_111,
            cert.WITNESS_P7,
        )
        for _, u, v, w in cert.build_test_frames():
            for anchor in anchors:
                in_cap = sum(
                    1
                    for vec in (u, v, w)
                    if cert.ray_sin_sq(vec, anchor) < Fraction(1, 2)
                )
                self.assertLessEqual(in_cap, 1)
                for p, q in ((u, v), (u, w), (v, w)):
                    self.assertGreaterEqual(
                        cert.ray_sin_sq(p, anchor)
                        + cert.ray_sin_sq(q, anchor),
                        Fraction(1),
                    )
                    self.assertFalse(
                        cert.ray_sin_sq(p, anchor) < Fraction(1, 2)
                        and cert.ray_sin_sq(q, anchor) < Fraction(1, 2)
                    )

    def test_target1_general_anchor_meridian_and_isolation(self) -> None:
        # 1. General-anchor meridian partner coincides with meridian_ortho at tomo_e1
        y_eq = cert.GVec(cert.G_ZERO, cert.GaussRat.of(1), cert.GaussRat.of(2, -1))
        self.assertEqual(
            cert.anchor_meridian_ortho(cert.TOMO_E1, y_eq),
            cert.meridian_ortho(y_eq),
        )
        self.assertEqual(
            cert.anchor_kelvin_eq(cert.TOMO_E1, y_eq),
            cert.kelvin_eq(y_eq),
        )
        # 2. General-anchor meridian bridge & raySinSq duality on non-unit anchors (e.g. tomo_e12, tomo_e23i)
        for a_vec, y_vec in (
            (cert.TOMO_E12, cert.PARTNER_E12_MINUS.smul(cert.GaussRat.of(Fraction(1, 3)))),
            (cert.TOMO_E23I, cert.PARTNER_E23I_MINUS.smul(cert.GaussRat.of(Fraction(2, 5)))),
            (cert.WITNESS_111, cert.WITNESS_NEG211.smul(cert.GaussRat.of(Fraction(1, 4)))),
        ):
            self.assertEqual(a_vec.inner(y_vec), cert.G_ZERO)
            step_vec = cert.anchor_meridian_step(a_vec, y_vec)
            ortho_vec = cert.anchor_meridian_ortho(a_vec, y_vec)
            kelvin_vec = cert.anchor_kelvin_eq(a_vec, y_vec)
            cross_vec = cert.herm_cross(a_vec, y_vec)
            self.assertTrue(cert.is_frame(a_vec, y_vec, cross_vec))
            self.assertTrue(cert.is_frame(step_vec, ortho_vec, cross_vec))
            self.assertEqual(
                ortho_vec.smul(cert.GaussRat.of(-Fraction(1) / y_vec.norm_sq())),
                a_vec.add(kelvin_vec),
            )
            expected_sin = y_vec.norm_sq() / (a_vec.norm_sq() + y_vec.norm_sq())
            self.assertEqual(cert.ray_sin_sq(step_vec, a_vec), expected_sin)
            self.assertEqual(cert.ray_sin_sq(ortho_vec, y_vec), expected_sin)
            for f in (cert.exotic_qi3, lambda u: (Fraction(1) + cert.sp(7, u)) / Fraction(3)):
                self.assertEqual(f(step_vec) - f(a_vec), f(y_vec) - f(ortho_vec))
                self.assertEqual(f(step_vec) + f(a_vec.add(kelvin_vec)), f(a_vec) + f(y_vec))
            for g in (cert.s3, cert.s3_lead_all, lambda u: cert.sp(7, u)):
                self.assertEqual(g(step_vec) - g(a_vec), g(y_vec) - g(ortho_vec))

        # 3. Spherical 3-frame Pythagoras identity & two-frame cross-anchor proximity bound
        for _, u, v, w in cert.build_test_frames():
            for a_vec in cert.NINE_ANCHORS.values():
                self.assertEqual(
                    cert.ray_sin_sq(u, a_vec)
                    + cert.ray_sin_sq(v, a_vec)
                    + cert.ray_sin_sq(w, a_vec),
                    Fraction(2),
                )
            self.assertLessEqual(
                cert.ray_sin_sq(w, cert.TOMO_E3),
                cert.ray_sin_sq(u, cert.TOMO_E1) + cert.ray_sin_sq(v, cert.TOMO_E2),
            )
            self.assertLessEqual(
                cert.ray_sin_sq(w, cert.PARTNER_E12_MINUS),
                cert.ray_sin_sq(u, cert.TOMO_E3) + cert.ray_sin_sq(v, cert.TOMO_E12),
            )

        # 4. witness_111 9-anchor isolation (raySinSq(u, a) >= 1/3 for all u perp witness_111)
        for a_vec in cert.NINE_ANCHORS.values():
            self.assertIn(
                cert.ray_sin_sq(cert.WITNESS_111, a_vec),
                (Fraction(1, 3), Fraction(2, 3)),
            )
            for u_ortho in (
                cert.WITNESS_NEG211,
                cert.PARTNER_E12_MINUS,
                cert.PARTNER_E13_MINUS,
                cert.PARTNER_E23_MINUS,
                cert.GVec.real(1, 2, -3),
            ):
                self.assertGreaterEqual(
                    cert.ray_sin_sq(u_ortho, a_vec),
                    Fraction(1, 3),
                )

        # 5. Exact 2-frame B_{1/5}(T_9) determination of witness_111 vs. < 1/8 isolation at witness_neg211
        self.assertTrue(
            cert.is_frame(cert.WITNESS_NEG211, cert.PROBE_120, cert.PROBE_2M15)
        )
        self.assertEqual(
            cert.ray_sin_sq(cert.PROBE_120, cert.TOMO_E12),
            Fraction(1, 10),
        )
        self.assertEqual(
            cert.ray_sin_sq(cert.PROBE_2M15, cert.TOMO_E3),
            Fraction(1, 6),
        )
        for g in (cert.s3, cert.s3_lead_x, cert.s3_lead_all, lambda u: cert.sp(7, u)):
            self.assertEqual(
                g(cert.WITNESS_111),
                g(cert.PROBE_120) + g(cert.PROBE_2M15),
            )
            eps_bound = max(abs(g(cert.PROBE_120)), abs(g(cert.PROBE_2M15)))
            self.assertLessEqual(abs(g(cert.WITNESS_111)), 2 * eps_bound)
            self.assertLessEqual(abs(g(cert.WITNESS_NEG211)), 2 * eps_bound)
        self.assertEqual(
            cert.ray_sin_sq(cert.WITNESS_NEG211, cert.PARTNER_E12_MINUS),
            Fraction(1, 4),
        )
        u_neg_real = cert.GVec.real(1, 3, -1)
        u_neg_cplx = cert.GVec(
            cert.GaussRat.of(1, 1), cert.GaussRat.of(1, 2), cert.GaussRat.of(1, 0)
        )
        for u_neg, v_neg in (
            (cert.PROBE_120, cert.PROBE_2M15),
            (cert.PROBE_2M15, cert.PROBE_120),
            (u_neg_real, cert.herm_cross(cert.WITNESS_NEG211, u_neg_real)),
            (u_neg_cplx, cert.herm_cross(cert.WITNESS_NEG211, u_neg_cplx)),
        ):
            self.assertTrue(cert.is_frame(u_neg, v_neg, cert.WITNESS_NEG211))
            self.assertGreaterEqual(
                cert.ray_sin_sq(u_neg, cert.TOMO_E12)
                + cert.ray_sin_sq(v_neg, cert.TOMO_E3),
                Fraction(1, 4),
            )
            self.assertFalse(
                cert.ray_sin_sq(u_neg, cert.TOMO_E12) < Fraction(1, 8)
                and cert.ray_sin_sq(v_neg, cert.TOMO_E3) < Fraction(1, 8)
            )

        # 6. Perturbed two-frame bisector bounce-back (including non-collinear second-step perturbations with LHS > 0)
        u_pert = cert.GVec.real(1, 5, -6)
        v_pert = cert.herm_cross(cert.WITNESS_111, u_pert)
        for u_prime, expected_lhs in (
            (cert.GVec.real(1, 9, -13), Fraction(3, 251)),
            (cert.GVec.real(-1, 3, -8), Fraction(6, 37)),
        ):
            v_prime = cert.herm_cross(v_pert, u_prime)
            self.assertTrue(cert.is_frame(cert.WITNESS_111, u_pert, v_pert))
            self.assertTrue(cert.is_frame(v_pert, u_prime, v_prime))
            self.assertLessEqual(
                cert.ray_sin_sq(v_pert, cert.WITNESS_NEG211),
                cert.ray_sin_sq(u_pert, cert.PARTNER_E23_MINUS),
            )
            lhs_bounce = cert.ray_sin_sq(v_prime, cert.WITNESS_111)
            self.assertEqual(lhs_bounce, expected_lhs)
            self.assertGreater(lhs_bounce, Fraction(0))
            self.assertLessEqual(
                lhs_bounce,
                cert.ray_sin_sq(u_pert, cert.PARTNER_E23_MINUS)
                + cert.ray_sin_sq(u_prime, cert.PARTNER_E23_MINUS),
            )

        # 7. Generic ray witness_123 = (1, 2, 3) 9-anchor (>= 1/14) and 6-bisector (>= 1/28) frame partner isolation
        for u_123 in (
            cert.GVec.real(2, -1, 0),
            cert.GVec.real(3, 0, -1),
            cert.GVec.real(0, 3, -2),
            cert.GVec.real(1, 1, -1),
        ):
            v_123 = cert.herm_cross(cert.WITNESS_123, u_123)
            self.assertTrue(cert.is_frame(cert.WITNESS_123, u_123, v_123))
            for partner_vec in (u_123, v_123):
                for a_vec in cert.NINE_ANCHORS.values():
                    self.assertGreaterEqual(
                        cert.ray_sin_sq(partner_vec, a_vec),
                        Fraction(1, 14),
                    )
                for b_vec in cert.SIX_PARTNERS.values():
                    self.assertGreaterEqual(
                        cert.ray_sin_sq(partner_vec, b_vec),
                        Fraction(1, 28),
                    )

        # 8. Meridian-step modulus orthogonal projection decomposition & collinear identity
        u = cert.WITNESS_111
        c_col = cert.GaussRat.of(Fraction(3, 2), Fraction(-1, 2))
        v_col = u.smul(c_col)
        self.assertEqual(cert.ray_sin_sq(u, v_col), Fraction(0))
        self.assertEqual(u.smul(cert.proj_scalar(u, v_col)), v_col)
        v_noncol = cert.WITNESS_123
        a_proj = u.smul(cert.proj_scalar(u, v_noncol))
        y_orth = v_noncol.sub(a_proj)
        self.assertEqual(a_proj.inner(y_orth), cert.G_ZERO)
        self.assertEqual(a_proj.add(y_orth), v_noncol)
        self.assertEqual(
            y_orth.norm_sq() / (a_proj.norm_sq() + y_orth.norm_sq()),
            cert.ray_sin_sq(u, v_noncol),
        )

    def test_ks_no_colouring_hypergraph_and_six_branch_unsat_core(self) -> None:
        ks = cert.extract_and_verify_ks_no_colouring()
        self.assertEqual(ks["box_rays_count"], 49)
        self.assertEqual(ks["pair_completion_frames_count"], 82)
        self.assertEqual(ks["pair_completions_outside_box_count"], 54)
        self.assertEqual(ks["internal_triple_frames_count"], 26)
        self.assertEqual(ks["total_frame_declarations"], 108)
        self.assertEqual(ks["distinct_ordered_frames"], 103)
        self.assertEqual(ks["distinct_unordered_frames"], 98)
        self.assertEqual(ks["distinct_canonical_w_ordered_frames"], 96)
        self.assertEqual(ks["distinct_sign_normalized_unordered_frames"], 86)
        self.assertEqual(ks["distinct_canonical_projective_frames"], 76)
        self.assertEqual(ks["distinct_raw_vectors"], 121)
        self.assertEqual(ks["distinct_canonical_projective_rays"], 99)

        core = ks["active_unsat_core"]
        self.assertEqual(core["active_pair_frames_count"], 40)
        self.assertEqual(core["active_triple_frames_count"], 22)
        self.assertEqual(core["active_nonneg_rays_count"], 35)
        self.assertEqual(core["active_total_frame_declarations"], 62)
        self.assertEqual(core["active_distinct_ordered_frames"], 59)
        self.assertEqual(core["active_distinct_unordered_frames"], 56)
        self.assertEqual(core["active_distinct_raw_vectors"], 71)
        self.assertEqual(core["active_distinct_canonical_rays"], 61)
        self.assertEqual(core["branches_verified"], 6)
        self.assertEqual(core["zero_one_valuations_count"], 0)
        self.assertTrue(core["admits_exotic_qi3_nonneg_valuation"])

        full_ks = ks["full_ks_scenario"]
        self.assertEqual(full_ks["scenario_name"], "ksFiniteScenario")
        self.assertEqual(full_ks["rays_count"], 121)
        self.assertEqual(full_ks["frames_count"], 103)
        self.assertEqual(full_ks["zero_one_valuations_count"], 0)
        self.assertTrue(full_ks["admits_exotic_qi3_nonneg_valuation"])
        self.assertFalse(full_ks["latitude_symmetry_assumed"])

    def test_fifteen_anchor_bisector_vs_ks_scenario_dichotomy(self) -> None:
        s9 = cert.nine_anchor_single_frame_scenario()
        s15 = cert.fifteen_anchor_bisector_scenario()
        self.assertEqual(len(s9.rays), 9)
        self.assertEqual(len(s9.frames), 1)
        self.assertEqual(len(s15.rays), 15)
        self.assertEqual(len(s15.frames), 7)
        self.assertTrue(cert.is_zero_one_scenario_valuation(s9, cert.indicator_x_axis_val))
        self.assertTrue(cert.is_zero_one_scenario_valuation(s15, cert.tomo_positive_x_anchor_val))
        self.assertEqual(cert.count_zero_one_scenario_valuations(s9), 192)
        self.assertEqual(cert.count_zero_one_scenario_valuations(s15), 48)
        self.assertTrue(cert.is_nonneg_scenario_valuation(s15, cert.exotic_qi3))

    def test_tfq_0307_four_tier_operational_classification(self) -> None:
        tfq = cert.verify_tfq_0307_four_tier_classification()
        self.assertEqual(
            tfq["tier1_zero_one_kochen_specker"]["fifteen_anchor_bisector_zero_one_valuations"],
            48,
        )
        self.assertEqual(
            tfq["tier1_zero_one_kochen_specker"]["ks_full_scenario_zero_one_valuations"],
            0,
        )
        self.assertFalse(
            tfq["tier1_zero_one_kochen_specker"]["latitude_symmetry_assumed"]
        )
        self.assertTrue(
            tfq["tier2_rational_nonquadratic_frame_functions"]["ks_scenario_inhabited_by_exotic_qi3"]
        )
        self.assertEqual(
            tfq["tier2_rational_nonquadratic_frame_functions"]["exotic_qi3_witness_111"],
            "2/3",
        )
        self.assertTrue(
            tfq["tier3_operator_effect_valuation_algebraic_born"]["excludes_exotic_qi3_without_topology"]
        )
        self.assertEqual(
            tfq["tier3_operator_effect_valuation_algebraic_born"]["algebraic_residual_discrepancy_at_witness_111"],
            "1/3",
        )
        self.assertTrue(
            tfq["tier4_topological_and_continuum_gleason_closure"]["bounded_anchor_amplification_closes_born_uniquely"]
        )

    def test_tfq_1057_multi_frame_incidence_and_amplification(self) -> None:
        tfq_1057 = cert.verify_tfq_1057_multi_frame_incidence_and_amplification()
        sub9a = tfq_1057["subsection_9a_bounded_anchor_amplification_anatomy"]
        self.assertTrue(sub9a["pointwise_continuous_iff_zero"])
        self.assertTrue(sub9a["discontinuous_vacuity_theorem_verified"])
        self.assertEqual(sub9a["s3_lead_all_amplification_constant"], "1")
        self.assertEqual(sub9a["s3_lead_all_witness_111"], "1")
        self.assertEqual(len(sub9a["crt_discontinuity_gap_witnesses"]), 5)

        sub9b = tfq_1057["subsection_9b_multi_frame_incidence_and_collar_blindness"]
        self.assertTrue(sub9b["fifteen_rays_vanishing_verified"])
        self.assertGreaterEqual(sub9b["fifteen_plane_ortho_antisymmetry_checks"], 40)
        self.assertGreaterEqual(sub9b["one_step_collar_confinement_checks"], 70)
        self.assertEqual(sub9b["finite_ray_list_collar_blindness_threshold"], "1/10")
        self.assertTrue(sub9b["finite_ray_list_collar_blindness_verified"])

        # Direct check of min_pos_ray_sin_sq_list and radial_scale_factor
        nine_anchors = list(cert.NINE_ANCHORS.values())
        self.assertEqual(cert.min_pos_ray_sin_sq_list([], nine_anchors), Fraction(1))
        self.assertEqual(
            cert.min_pos_ray_sin_sq_list([cert.TOMO_E1], [cert.TOMO_E1]), Fraction(1)
        )
        self.assertEqual(
            cert.min_pos_ray_sin_sq_list([cert.TOMO_E1, cert.PROBE_120], nine_anchors),
            Fraction(1, 10),
        )
        self.assertEqual(
            cert.radial_scale_factor(cert.TOMO_E1, cert.TOMO_E2, Fraction(2)),
            Fraction(1),
        )
        c_factor = cert.radial_scale_factor(
            cert.TOMO_E1, cert.GVec.real(0, 3, 4), Fraction(1, 10)
        )
        self.assertEqual(c_factor, Fraction(1, 500))
        yc = cert.GVec.real(0, 3, 4).smul(cert.GaussRat.of(c_factor))
        self.assertLess(cert.ray_sin_sq(cert.TOMO_E1.add(yc), cert.TOMO_E1), Fraction(1, 10))
        self.assertLess(
            cert.ray_sin_sq(
                cert.anchor_meridian_ortho(cert.TOMO_E1, yc), cert.GVec.real(0, 3, 4)
            ),
            Fraction(1, 10),
        )

        sub9c = tfq_1057["subsection_9c_radial_scale_transport_and_chain_scaling"]
        self.assertGreaterEqual(sub9c["radial_scale_transport_checks"], 100)
        self.assertEqual(sub9c["meridian_chain_linear_amplification_checks"], 24)
        self.assertEqual(sub9c["status"], "PASS")


if __name__ == "__main__":
    unittest.main()

