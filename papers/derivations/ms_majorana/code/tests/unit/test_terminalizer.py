
import unittest
from pathlib import Path
import tempfile

from omega_engine.crates.majorana.engines.terminalizer import (
    D0_DEMO,
    D1_DEMO,
    RESIDUALS_DEMO,
    validate_complex,
    solve_exact,
    compute_coherence,
    normal_form_mod_image,
    terminalize,
    write_ledger,
)
from omega_engine.crates.majorana.certificates.ledger import ledger_row, verify_ledger
from omega_engine.crates.majorana.evaluators.dashboard import calculate_dashboard_metrics


class TestTerminalizer(unittest.TestCase):
    def test_demo_complex_is_valid(self):
        self.assertTrue(validate_complex(D0_DEMO, D1_DEMO))

    def test_exact_polynomial_algorithms(self):
        self.assertEqual(solve_exact(D0_DEMO, RESIDUALS_DEMO["exact"]), [1])
        self.assertIsNone(solve_exact(D0_DEMO, RESIDUALS_DEMO["closed"]))

        self.assertEqual(compute_coherence(D1_DEMO, RESIDUALS_DEMO["open"]), [1])

        self.assertEqual(normal_form_mod_image(D0_DEMO, D1_DEMO, RESIDUALS_DEMO["closed"]), [0, 0, 1])

        exact_res = terminalize(D0_DEMO, D1_DEMO, RESIDUALS_DEMO["exact"])
        self.assertEqual(exact_res["terminal_status"], "Exact")
        self.assertEqual(exact_res["algebraic_class_id"], "exact")

        closed_res = terminalize(D0_DEMO, D1_DEMO, RESIDUALS_DEMO["closed"])
        self.assertEqual(closed_res["terminal_status"], "ClosedResidual")
        self.assertEqual(closed_res["algebraic_class_id"], "closed-residual:001")

        open_res = terminalize(D0_DEMO, D1_DEMO, RESIDUALS_DEMO["open"])
        self.assertEqual(open_res["terminal_status"], "OpenObstruction")
        self.assertEqual(open_res["algebraic_class_id"], "open-obstruction:1")

    def test_invalid_complex_refuses(self):
        result = terminalize([[1], [0]], [[1, 1]], [1, 0])
        self.assertEqual(result["terminal_status"], "RepresentationInvalid")

    def test_ledger_row_and_replay(self):
        row = ledger_row(D0_DEMO, D1_DEMO, RESIDUALS_DEMO["closed"])
        self.assertIn("certificate_id", row)
        self.assertIn("carrier_hash", row)
        self.assertEqual(row["terminal_status"], "ClosedResidual")
        self.assertEqual(row["q1_norm"], "1")
        self.assertEqual(row["normal_form"], [0, 0, 1])
        self.assertIn("replay_hash", row)

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.jsonl"
            write_ledger(path)
            res = verify_ledger(path)
            self.assertTrue(res["verified"])
            self.assertEqual(res["checked"], 3)

    def test_dashboard_metrics(self):
        rows = [
            ledger_row(D0_DEMO, D1_DEMO, RESIDUALS_DEMO["exact"]),
            ledger_row(D0_DEMO, D1_DEMO, RESIDUALS_DEMO["closed"]),
            ledger_row(D0_DEMO, D1_DEMO, RESIDUALS_DEMO["open"]),
        ]
        dashboard = calculate_dashboard_metrics(rows)
        metrics = dashboard["metrics"]
        dist = dashboard["algebraic_class_distribution"]

        self.assertAlmostEqual(metrics["q1_zero_rate"], 1.0 / 3.0)
        self.assertAlmostEqual(metrics["mean_q1_norm"], 2.0 / 3.0)
        self.assertEqual(metrics["exact_certificate_count"], 1)
        self.assertEqual(metrics["closed_residual_count"], 1)
        self.assertEqual(metrics["open_obstruction_count"], 1)
        self.assertEqual(dist["exact"], 1)
        self.assertEqual(dist["closed-residual:001"], 1)
        self.assertEqual(dist["open-obstruction:1"], 1)


if __name__ == "__main__":
    unittest.main()



