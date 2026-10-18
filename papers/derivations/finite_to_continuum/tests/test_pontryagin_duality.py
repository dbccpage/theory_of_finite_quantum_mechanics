# -*- coding: utf-8 -*-
"""Unit tests for Pontryagin Duality Bridge and 7-stage honest program."""

from __future__ import annotations

from fractions import Fraction
import math
from pathlib import Path
import sys
import unittest

CODE_DIR = str(Path(__file__).resolve().parents[1] / "code")
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

from pontryagin_duality import (
    DiscreteLatticeFourier,
    PontryaginProgrammeError,
    refuse_alpha_as_certified_exact,
    refuse_finite_zn_sold_as_free_u1,
    refuse_pi_from_exact_q,
    refuse_u1_derived_from_l1_mass_alone,
    run_pontryagin_staged_programme,
)


class TestPontryaginDuality(unittest.TestCase):
    def test_7_stages_honest_execution(self) -> None:
        r = run_pontryagin_staged_programme(
            lattice_size=4,
            declare_free_z=True,
            enable_continuous_host=True,
            enable_experimental_alpha=False,
        )
        self.assertTrue(r.finite_exact)
        self.assertEqual(r.is_exact_q_through_stage, 0)
        self.assertEqual(r.authority_effect, "None")

        # Stage 0: FINITE_EXACT
        self.assertEqual(r.stage("FINITE_EXACT").status, "EXACT_Q")
        self.assertEqual(r.stage("FINITE_EXACT").evidence["verdict"], "closed_residual")

        # Stage 1: DISCRETE_PERIOD_GROUP
        self.assertEqual(r.stage("DISCRETE_PERIOD_GROUP").status, "OBSERVED")
        self.assertEqual(r.stage("DISCRETE_PERIOD_GROUP").evidence["character_group_observed"], "Z/4Z")

        # Stage 2: UNBOUNDED_PERIOD_DECL
        self.assertEqual(r.stage("UNBOUNDED_PERIOD_DECL").status, "MODELLING_DECLARATION")

        # Stage 3: PONTRYAGIN_DUAL_IMPORT
        self.assertEqual(r.stage("PONTRYAGIN_DUAL_IMPORT").status, "LITERATURE_IMPORT")
        self.assertEqual(r.stage("PONTRYAGIN_DUAL_IMPORT").evidence["pontryagin_dual"], "U(1)")

        # Stage 4: HAAR_PERIOD_CONVENTION
        self.assertEqual(r.stage("HAAR_PERIOD_CONVENTION").status, "NORMALIZATION")
        self.assertEqual(r.stage("HAAR_PERIOD_CONVENTION").evidence["pi_origin"], "NORMALIZATION_ON_DUAL_NOT_EXACT_Q_OUTPUT")

        # Stage 5: CONTINUOUS_HOST_EVAL
        self.assertEqual(r.stage("CONTINUOUS_HOST_EVAL").status, "HOST_FLOAT")
        self.assertFalse(r.stage("CONTINUOUS_HOST_EVAL").evidence["is_exact_q_certificate"])
        a_mid = r.stage("CONTINUOUS_HOST_EVAL").evidence["amplitude_a_interval"]["midpoint_float"]
        self.assertAlmostEqual(a_mid, 3.0 / math.pi, places=10)

        # Stage 6: EXPERIMENTAL_ALPHA
        self.assertEqual(r.stage("EXPERIMENTAL_ALPHA").status, "OPEN")

        # Spine fences
        self.assertEqual(r.spine_fence["pi_from_exact_q"], "REFUSED")
        self.assertEqual(r.spine_fence["u1_from_l1_mass_alone"], "REFUSED")

    def test_without_free_z_blocks_u1(self) -> None:
        r = run_pontryagin_staged_programme(lattice_size=4, declare_free_z=False)
        self.assertEqual(r.stage("UNBOUNDED_PERIOD_DECL").status, "OPEN")
        self.assertEqual(r.stage("PONTRYAGIN_DUAL_IMPORT").status, "OPEN")
        self.assertFalse(r.continuous_host_active)

    def test_experimental_alpha_host(self) -> None:
        r = run_pontryagin_staged_programme(
            lattice_size=4,
            declare_free_z=True,
            enable_continuous_host=True,
            enable_experimental_alpha=True,
        )
        self.assertEqual(r.stage("EXPERIMENTAL_ALPHA").status, "EXPERIMENTAL_HOST")
        self.assertFalse(r.stage("EXPERIMENTAL_ALPHA").evidence["is_exact_q_certificate"])
        mz = r.stage("EXPERIMENTAL_ALPHA").evidence["alpha_mz_inv_host"]
        self.assertAlmostEqual(mz, 137.0, delta=1.0)

    def test_kill_pi_from_exact_q(self) -> None:
        with self.assertRaises(PontryaginProgrammeError) as ctx:
            refuse_pi_from_exact_q(True)
        self.assertEqual(ctx.exception.code, "PI_FROM_EXACT_Q")

    def test_kill_u1_from_l1(self) -> None:
        with self.assertRaises(PontryaginProgrammeError) as ctx:
            refuse_u1_derived_from_l1_mass_alone(True)
        self.assertEqual(ctx.exception.code, "U1_FROM_L1_MASS")

    def test_kill_zn_sold_as_u1(self) -> None:
        with self.assertRaises(PontryaginProgrammeError) as ctx:
            refuse_finite_zn_sold_as_free_u1("Z/4Z", "U(1)", False)
        self.assertEqual(ctx.exception.code, "ZN_SOLD_AS_U1")

    def test_kill_alpha_as_exact(self) -> None:
        with self.assertRaises(PontryaginProgrammeError) as ctx:
            refuse_alpha_as_certified_exact(True, True)
        self.assertEqual(ctx.exception.code, "ALPHA_AS_EXACT")

    def test_discrete_character_orthogonality(self) -> None:
        for l in (4, 6, 8, 12):
            fourier = DiscreteLatticeFourier(l)
            res = fourier.character_matrix_exact_orthogonality()
            self.assertTrue(res["orthogonality_verified"])
            self.assertEqual(len(res["violations"]), 0)


if __name__ == "__main__":
    unittest.main()
