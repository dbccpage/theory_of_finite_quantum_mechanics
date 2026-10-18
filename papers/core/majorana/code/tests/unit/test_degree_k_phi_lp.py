import unittest
import numpy as np
from omega_engine.crates.residuals.network_residual import Network
from omega_engine.crates.functional.higher_simplex_assembly import assemble_from_network
from omega_engine.crates.functional.degree_k_phi import (
    DegreeKPhiReceipt,
    DegreeKPhiUncertified,
    solve_degree_k_phi,
    solve_degree_k_joint_primal,
    phi_k_on_complex,
    phi_k_on_network,
    phi_k_estimate,
    phi_k,
)


class TestDegreeKPhiLp(unittest.TestCase):
    def test_deg1_all_ones_on_k5(self):
        """Verify Degree 1 all-ones cochain on K5 yields Phi=4.0 with gap=0 and is_certified=True."""
        nodes = [0, 1, 2, 3, 4]
        edges = [(u, v) for u in nodes for v in nodes if u < v]
        net = Network(nodes=nodes, edges=edges)

        cochain1 = {e: 1.0 for e in edges}
        receipt = phi_k_estimate(net, degree=1, cochain_values=cochain1)

        self.assertAlmostEqual(receipt.min_l1, 4.0, places=5)
        self.assertAlmostEqual(receipt.dual_val, 4.0, places=5)
        self.assertAlmostEqual(receipt.duality_gap, 0.0, places=5)
        self.assertTrue(receipt.is_certified)

        scalar_val = phi_k(net, degree=1, cochain_values=cochain1)
        self.assertAlmostEqual(scalar_val, 4.0, places=5)

    def test_deg1_joint_is_uncertified_by_design(self):
        """Verify Degree 1 joint solver yields Phi=0.0 with is_certified=False."""
        nodes = [0, 1, 2]
        edges = [(0, 1), (1, 2), (0, 2)]
        net = Network(nodes=nodes, edges=edges)
        cochain_cycle = {(0, 1): 1.0, (1, 2): 1.0, (0, 2): -1.0}

        complex_obj = assemble_from_network(net, max_dim=2)
        d_lower = np.array([[-1, 0], [1, -1], [0, 1]])  # d0^\top
        d_upper = np.array([[1], [1], [1]])  # d1

        receipt_joint = solve_degree_k_joint_primal(d_lower, d_upper, np.array([1.0, 1.0, -1.0]), degree=1)
        self.assertAlmostEqual(receipt_joint.min_l1, 0.0, places=5)
        self.assertFalse(receipt_joint.is_certified)

    def test_deg2_curl_of_all_ones(self):
        """Verify Degree 2 face curls from exact 1-cochain yield Phi=0.0 with gap=0 and is_certified=True."""
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

        receipt2 = phi_k_on_complex(complex_obj, degree=2, cochain_values=face_cochain)
        self.assertAlmostEqual(receipt2.min_l1, 0.0, places=5)
        self.assertAlmostEqual(receipt2.duality_gap, 0.0, places=5)
        self.assertTrue(receipt2.is_certified)

    def test_exact_gradient_cochain(self):
        """Verify exact gradient cochain on triangle graph yields Phi=0.0 and is certified."""
        net = Network(nodes=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)])
        # Gradient of potential f = [0, 2, 5]: e(0,1)=2, e(1,2)=3, e(0,2)=5
        grad_cochain = {(0, 1): 2.0, (1, 2): 3.0, (0, 2): 5.0}

        receipt = phi_k_on_network(net, degree=1, cochain_values=grad_cochain)
        self.assertAlmostEqual(receipt.min_l1, 0.0, places=5)
        self.assertTrue(receipt.is_certified)


if __name__ == "__main__":
    unittest.main()


