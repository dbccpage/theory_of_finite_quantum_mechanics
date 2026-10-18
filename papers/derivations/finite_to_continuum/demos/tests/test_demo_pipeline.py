"""Regression test for the end-to-end demo pipeline."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

DEMO_CODE_DIR = str(Path(__file__).resolve().parents[1] / "code")
if DEMO_CODE_DIR not in sys.path:
    sys.path.insert(0, DEMO_CODE_DIR)

from demo_finite_to_continuum_pipeline import run_full_pipeline_demo


class TestDemoPipeline(unittest.TestCase):
    def test_run_full_demo(self) -> None:
        receipt = run_full_pipeline_demo()
        self.assertEqual(receipt["authority_effect"], "None")
        self.assertTrue("master_sha256" in receipt)

        s1 = receipt["step1_coda_q_interval_calculus"]
        self.assertTrue(s1["zero_float_certified"])

        s2 = receipt["step2_cs_q_discretization_defect"]
        self.assertTrue(s2["1d_encloses_1_3"])
        self.assertTrue(s2["2d_encloses_1_9"])

        s3 = receipt["step3_wilsonian_extrapolation"]
        self.assertEqual(s3["extrapolated_thermodynamic_limit"]["width"], "0")
        self.assertEqual(s3["extrapolated_thermodynamic_limit"]["lo"], "7/13")

        p = receipt["pontryagin_duality_bridge"]
        self.assertTrue(p["orthogonality_1d"])
        self.assertTrue(p["orthogonality_2d"])
        self.assertEqual(p["1d_staged_receipt"]["spine_fence"]["pi_from_exact_q"], "REFUSED")
        self.assertEqual(p["2d_staged_receipt"]["spine_fence"]["pi_from_exact_q_2d"], "REFUSED")

        m = receipt["meron_wilsonian_bridge"]
        self.assertEqual(m["partition_sums"]["4"], 912)
        self.assertEqual(m["partition_sums"]["6"], 33012)
        self.assertEqual(m["partition_sums"]["8"], 973824)
        f_mid = float(m["thermodynamic_limit"]["float_midpoint"])
        self.assertAlmostEqual(f_mid, 1.69411, places=4)


if __name__ == "__main__":
    unittest.main()
