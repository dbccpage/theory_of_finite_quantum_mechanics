"""Staged Finite→∞ Pontryagin residual dual programme. AuthorityEffect: None."""

from __future__ import annotations

import math
import unittest

from omega_engine.crates.solver.solv_pontryagin_residual_dual import (
    PontryaginProgrammeError,
    refuse_alpha_as_certified_exact,
    refuse_finite_zn_sold_as_free_u1,
    refuse_pi_from_exact_q,
    refuse_u1_derived_from_l1_mass_alone,
    run_pontryagin_residual_dual_programme,
)


class TestPontryaginResidualDual(unittest.TestCase):
    def test_n3_stages_honest(self):
        r = run_pontryagin_residual_dual_programme(
            declare_free_z=True,
            enable_continuous_host=True,
            enable_experimental_alpha=False,
        )
        self.assertTrue(r.finite_exact)
        self.assertEqual(r.is_exact_q_through_stage, 0)
        self.assertEqual(r.authority_effect, "None")
        self.assertEqual(r.stage("FINITE_EXACT").status, "EXACT_Q")
        self.assertEqual(r.stage("FINITE_EXACT").evidence["verdict"], "closed_residual")
        self.assertEqual(r.stage("DISCRETE_PERIOD_GROUP").status, "OBSERVED")
        self.assertEqual(
            r.stage("DISCRETE_PERIOD_GROUP").evidence["character_group_observed"],
            "Z/3Z",
        )
        self.assertEqual(r.stage("UNBOUNDED_PERIOD_DECL").status, "MODELLING_DECLARATION")
        self.assertEqual(r.stage("PONTRYAGIN_DUAL_IMPORT").status, "LITERATURE_IMPORT")
        self.assertEqual(
            r.stage("PONTRYAGIN_DUAL_IMPORT").evidence["pontryagin_dual"], "U(1)"
        )
        self.assertEqual(r.stage("HAAR_PERIOD_CONVENTION").status, "NORMALIZATION")
        self.assertEqual(
            r.stage("HAAR_PERIOD_CONVENTION").evidence["pi_origin"],
            "NORMALIZATION_ON_DUAL_NOT_EXACT_Q_OUTPUT",
        )
        self.assertEqual(r.stage("CONTINUOUS_HOST_EVAL").status, "HOST_FLOAT")
        self.assertFalse(r.stage("CONTINUOUS_HOST_EVAL").evidence["is_exact_q_certificate"])
        a = r.stage("CONTINUOUS_HOST_EVAL").evidence["amplitude_a"]
        self.assertAlmostEqual(a, 3.0 / math.pi, places=12)
        self.assertEqual(r.stage("EXPERIMENTAL_ALPHA").status, "OPEN")
        self.assertEqual(r.spine_fence["pi_from_exact_q"], "REFUSED")
        self.assertEqual(r.spine_fence["u1_from_l1_mass_alone"], "REFUSED")

    def test_without_free_z_blocks_u1(self):
        r = run_pontryagin_residual_dual_programme(declare_free_z=False)
        self.assertEqual(r.stage("UNBOUNDED_PERIOD_DECL").status, "OPEN")
        self.assertEqual(r.stage("PONTRYAGIN_DUAL_IMPORT").status, "OPEN")
        self.assertFalse(r.continuous_host_active)

    def test_experimental_alpha_host(self):
        r = run_pontryagin_residual_dual_programme(
            declare_free_z=True,
            enable_continuous_host=True,
            enable_experimental_alpha=True,
        )
        self.assertEqual(r.stage("EXPERIMENTAL_ALPHA").status, "EXPERIMENTAL_HOST")
        self.assertFalse(
            r.stage("EXPERIMENTAL_ALPHA").evidence["is_exact_q_certificate"]
        )
        mz = r.stage("EXPERIMENTAL_ALPHA").evidence["alpha_mz_inv_host"]
        self.assertAlmostEqual(mz, 137.0, delta=1.0)

    def test_kill_pi_from_exact_q(self):
        with self.assertRaises(PontryaginProgrammeError) as ctx:
            refuse_pi_from_exact_q(True)
        self.assertEqual(ctx.exception.code, "PI_FROM_EXACT_Q")

    def test_kill_u1_from_l1(self):
        with self.assertRaises(PontryaginProgrammeError) as ctx:
            refuse_u1_derived_from_l1_mass_alone(True)
        self.assertEqual(ctx.exception.code, "U1_FROM_L1_MASS")

    def test_kill_zn_sold_as_u1(self):
        with self.assertRaises(PontryaginProgrammeError) as ctx:
            refuse_finite_zn_sold_as_free_u1("Z/3Z", "U(1)", False)
        self.assertEqual(ctx.exception.code, "ZN_SOLD_AS_U1")
        refuse_finite_zn_sold_as_free_u1("Z/3Z", "U(1)", True)

    def test_kill_alpha_as_exact(self):
        with self.assertRaises(PontryaginProgrammeError) as ctx:
            refuse_alpha_as_certified_exact(False, True)
        self.assertEqual(ctx.exception.code, "ALPHA_AS_EXACT")


if __name__ == "__main__":
    unittest.main()
