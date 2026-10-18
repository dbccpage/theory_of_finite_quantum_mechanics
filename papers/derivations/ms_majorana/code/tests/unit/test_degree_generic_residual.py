import unittest
import numpy as np
from omega_engine.crates.residuals.network_residual import Network
from omega_engine.crates.functional.higher_simplex_assembly import assemble_from_network
from omega_engine.crates.discrete_deformation_algebra.degree_generic_residual import (
    ResidualReport,
    evaluate_residual,
    evaluate_residual_on_network,
    residual_triple_for_lift,
)


class TestDegreeGenericResidual(unittest.TestCase):
    def test_k5_all_1_cochain_deg1_gauge(self):
        """Verify deg1 gauge on K5 with all-1 cochain yields φ=4.0, γ=10.0, χ=0.0."""
        nodes = [0, 1, 2, 3, 4]
        edges = [(u, v) for u in nodes for v in nodes if u < v]
        net = Network(nodes=nodes, edges=edges)

        cochain1 = {e: 1.0 for e in edges}
        report = evaluate_residual_on_network(net, degree=1, cochain_values=cochain1, method="l1_gauge")

        self.assertAlmostEqual(report.phi, 4.0, places=4)
        self.assertAlmostEqual(report.gamma, 10.0, places=4)
        self.assertAlmostEqual(report.chi, 0.0, places=4)

    def test_deg2_after_curl_pure_gauge(self):
        """Verify 2-cochain face curls from exact 1-cochain collapse to φ=0, γ=0, χ=0 at degree 2."""
        nodes = [0, 1, 2, 3]
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        net = Network(nodes=nodes, edges=edges)
        complex_obj = assemble_from_network(net, max_dim=3)

        edge_vals = {(0, 1): 1.0, (1, 2): 2.0, (0, 2): 3.0, (0, 3): 1.0, (1, 3): 2.0, (2, 3): -1.0}
        face_cochain = {}
        for f in complex_obj.cells[2]:
            u, v, w = f
            val = edge_vals[(u, v)] + edge_vals[(v, w)] - edge_vals[(u, w)]
            face_cochain[f] = val

        report2 = evaluate_residual(complex_obj, degree=2, cochain=face_cochain, method="l1_gauge")
        self.assertAlmostEqual(report2.phi, 0.0, places=5)
        self.assertAlmostEqual(report2.gamma, 0.0, places=5)
        self.assertAlmostEqual(report2.chi, 0.0, places=5)

    def test_deg1_joint_absorbs_coexact_cycle(self):
        """Verify deg1 joint (gauge + coexact) repair zeroes residual on closed cycle graphs."""
        nodes = [0, 1, 2]
        edges = [(0, 1), (1, 2), (0, 2)]
        net = Network(nodes=nodes, edges=edges)

        cochain_cycle = {(0, 1): 1.0, (1, 2): 1.0, (0, 2): -1.0}
        report_joint = evaluate_residual_on_network(net, degree=1, cochain_values=cochain_cycle, method="l1_joint")

        self.assertAlmostEqual(report_joint.phi, 0.0, places=5)
        self.assertAlmostEqual(report_joint.gamma, 0.0, places=5)


if __name__ == "__main__":
    unittest.main()


