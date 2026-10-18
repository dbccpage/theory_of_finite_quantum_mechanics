import unittest
import numpy as np
from omega_engine.crates.residuals.network_residual import Network
from omega_engine.crates.functional.higher_simplex_assembly import (
    SimplexComplex,
    combinatorial_simplices,
    filter_simplices_by_skeleton,
    detect_simplices,
    boundary_matrix,
    verify_nilpotency,
    assemble_from_network,
    boundary_operators,
    nilpotency_report,
    discover_higher_cells_for_lift,
)


class TestHigherSimplexAssembly(unittest.TestCase):
    def test_full_3_simplex_k4(self):
        """Verify full 3-simplex (K4) cell counts and exact nilpotency d1 o d2 = 0, d2 o d3 = 0."""
        net = Network(
            nodes=[0, 1, 2, 3],
            edges=[(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)],
        )
        complex_obj = assemble_from_network(net, max_dim=3)

        self.assertEqual(len(complex_obj.cells[0]), 4)
        self.assertEqual(len(complex_obj.cells[1]), 6)
        self.assertEqual(len(complex_obj.cells[2]), 4)
        self.assertEqual(len(complex_obj.cells[3]), 1)  # (0, 1, 2, 3)

        report = nilpotency_report(complex_obj)
        self.assertTrue(report["all_nilpotent"])
        self.assertEqual(report["authority_effect"], "None")

    def test_full_4_simplex_5_vertices(self):
        """Verify full 4-simplex on 5 vertices has cell counts {0:5, 1:10, 2:10, 3:5, 4:1} and is nilpotent."""
        nodes = [0, 1, 2, 3, 4]
        edges = [(u, v) for u in nodes for v in nodes if u < v]
        net = Network(nodes=nodes, edges=edges)

        complex_obj = assemble_from_network(net, max_dim=4)
        counts = {dim: len(c) for dim, c in complex_obj.cells.items()}
        self.assertEqual(counts, {0: 5, 1: 10, 2: 10, 3: 5, 4: 1})

        report = nilpotency_report(complex_obj)
        self.assertTrue(report["all_nilpotent"])

    def test_skeleton_filtering_refuses_missing_faces(self):
        """Verify skeleton filtering refuses 3-cells when one of the boundary 2-faces is missing."""
        # 4 vertices, but omit edge (2, 3) so one triangle (1,2,3) is missing
        net = Network(
            nodes=[0, 1, 2, 3],
            edges=[(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)],  # Missing (2, 3)
        )
        complex_obj = assemble_from_network(net, max_dim=3)
        # Should not form the 3-simplex (0, 1, 2, 3) because faces depending on (2,3) are missing
        self.assertNotIn(3, complex_obj.cells)

    def test_discover_higher_cells_for_lift(self):
        """Verify discover_higher_cells_for_lift returns tetrahedra for K4 and unsupported when no cell exists."""
        net_k4 = Network(
            nodes=[0, 1, 2, 3],
            edges=[(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)],
        )
        cells, lift_kind = discover_higher_cells_for_lift(net_k4, from_degree=1)
        self.assertEqual(len(cells), 1)
        self.assertEqual(lift_kind, "tetrahedra")

        # Open ring without higher cells
        net_ring = Network(nodes=[0, 1, 2], edges=[(0, 1), (1, 2), (2, 0)])
        cells_empty, lift_kind_empty = discover_higher_cells_for_lift(net_ring, from_degree=2)
        self.assertEqual(len(cells_empty), 0)
        self.assertEqual(lift_kind_empty, "unsupported")


if __name__ == "__main__":
    unittest.main()


