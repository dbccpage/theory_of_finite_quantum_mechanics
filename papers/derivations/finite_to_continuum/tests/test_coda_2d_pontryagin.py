"""Unit tests for 2D Pontryagin Duality Bridge and Torus Character sums."""

from __future__ import annotations

from fractions import Fraction
import math
from pathlib import Path
import sys
import unittest

CODE_DIR = str(Path(__file__).resolve().parents[1] / "code")
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

from coda_2d_pontryagin import (
    Discrete2DTorusFourier,
    Pontryagin2DProgrammeError,
    refuse_alpha_2d_as_certified_exact,
    refuse_finite_z2_sold_as_t2,
    refuse_pi_from_exact_q_2d,
    refuse_t2_derived_from_l1_alone,
    run_pontryagin_2d_staged_programme,
)


class TestCoda2DPontryagin(unittest.TestCase):
    def test_2d_7_stages_honest_execution(self) -> None:
        r = run_pontryagin_2d_staged_programme(
            lx=4,
            ly=4,
            declare_free_z2=True,
            enable_continuous_host=True,
        )
        self.assertTrue(r.finite_exact)
        self.assertEqual(r.is_exact_q_through_stage, 0)
        self.assertEqual(r.authority_effect, "None")

        s0 = r.stage("FINITE_EXACT_2D")
        self.assertEqual(s0.status, "EXACT_Q")
        self.assertEqual(s0.evidence["total_sites"], 16)

        s1 = r.stage("DISCRETE_TORUS_GROUP")
        self.assertEqual(s1.status, "OBSERVED")
        self.assertEqual(s1.evidence["character_group_observed"], "Z/4Z x Z/4Z")

        s2 = r.stage("UNBOUNDED_TORUS_DECL")
        self.assertEqual(s2.status, "MODELLING_DECLARATION")
        self.assertEqual(s2.evidence["declared_group"], "Z^2")

        s3 = r.stage("PONTRYAGIN_DUAL_IMPORT_2D")
        self.assertEqual(s3.status, "LITERATURE_IMPORT")
        self.assertEqual(s3.evidence["pontryagin_dual"], "T^2")

        s4 = r.stage("HAAR_TORUS_CONVENTION")
        self.assertEqual(s4.status, "NORMALIZATION")
        self.assertEqual(s4.evidence["conventional_torus_volume"], "(2*pi)^2")

        s5 = r.stage("CONTINUOUS_HOST_EVAL_2D")
        self.assertEqual(s5.status, "HOST_FLOAT")
        a_mid = s5.evidence["amplitude_2d_interval"]["midpoint_float"]
        expected = (3.0 / math.pi) ** 2
        self.assertAlmostEqual(a_mid, expected, places=8)

        self.assertEqual(r.spine_fence["pi_from_exact_q_2d"], "REFUSED")
        self.assertEqual(r.spine_fence["t2_from_l1_alone"], "REFUSED")

    def test_kill_conditions_2d(self) -> None:
        with self.assertRaises(Pontryagin2DProgrammeError) as ctx1:
            refuse_pi_from_exact_q_2d(True)
        self.assertEqual(ctx1.exception.code, "PI_FROM_EXACT_Q_2D")

        with self.assertRaises(Pontryagin2DProgrammeError) as ctx2:
            refuse_t2_derived_from_l1_alone(True)
        self.assertEqual(ctx2.exception.code, "T2_FROM_L1_ALONE")

        with self.assertRaises(Pontryagin2DProgrammeError) as ctx3:
            refuse_finite_z2_sold_as_t2("Z/4Z x Z/4Z", "T^2", False)
        self.assertEqual(ctx3.exception.code, "Z2_SOLD_AS_T2")

        with self.assertRaises(Pontryagin2DProgrammeError) as ctx4:
            refuse_alpha_2d_as_certified_exact(True, True)
        self.assertEqual(ctx4.exception.code, "ALPHA_2D_AS_EXACT")

    def test_2d_torus_character_orthogonality(self) -> None:
        for lx, ly in ((2, 2), (3, 3), (4, 4)):
            fourier = Discrete2DTorusFourier(lx, ly)
            res = fourier.character_tensor_exact_orthogonality()
            self.assertTrue(res["orthogonality_verified"])
            self.assertEqual(len(res["violations"]), 0)


if __name__ == "__main__":
    unittest.main()
