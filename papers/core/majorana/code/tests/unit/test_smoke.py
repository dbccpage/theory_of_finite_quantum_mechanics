
import json
from pathlib import Path
import tempfile
import unittest

from omega_engine.crates.majorana.engines.terminalizer import (
    D0_DEMO, D1_DEMO, RESIDUALS_DEMO, terminalize, write_ledger
)
from omega_engine.crates.majorana.certificates.ledger import verify_ledger
from omega_engine.crates.majorana.evaluators.dashboard import calculate_dashboard_metrics
from omega_engine.crates.homology_theory.graph_complex import get_triangle_complex, get_plaquette_complex, get_prism_complex
from omega_engine.crates.majorana.engines.exact_algebraic_verifier import (
    verify_ising_braid_relation,
    verify_fusion_associativity,
    verify_ising_sigma_hexagon_specialization,
    Cyclotomic16,
)


class SmokeTests(unittest.TestCase):
    def test_demo_terminals(self):
        self.assertEqual(terminalize(D0_DEMO, D1_DEMO, RESIDUALS_DEMO["exact"])["terminal_status"], "Exact")
        self.assertEqual(terminalize(D0_DEMO, D1_DEMO, RESIDUALS_DEMO["closed"])["terminal_status"], "ClosedResidual")
        self.assertEqual(terminalize(D0_DEMO, D1_DEMO, RESIDUALS_DEMO["open"])["terminal_status"], "OpenObstruction")

    def test_ledger_verifies_and_dashboard(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.jsonl"
            write_ledger(path)
            result = verify_ledger(path)
            self.assertTrue(result["verified"])
            rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
            metrics = calculate_dashboard_metrics(rows)
            self.assertEqual(metrics["metrics"]["total_certificates_evaluated"], 3)

    def test_graph_adapters(self):
        tri = get_triangle_complex()
        carrier = tri.create_carrier([1,1,0])
        self.assertEqual(len(carrier.residual), tri.num_edges)
        plaq = get_plaquette_complex()
        self.assertEqual(plaq.num_edges, 4)
        prism = get_prism_complex()
        self.assertEqual(prism.num_faces, 5)

    def test_exact_algebraic_seed(self):
        self.assertTrue(verify_fusion_associativity())
        self.assertTrue(verify_ising_braid_relation())
        self.assertTrue(verify_ising_sigma_hexagon_specialization())
        with self.assertRaises(TypeError):
            Cyclotomic16([0.5])


if __name__ == "__main__":
    unittest.main()



