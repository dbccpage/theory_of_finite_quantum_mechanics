# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jeremy H. Carroll

import unittest

from omega_engine.crates.majorana.engines.terminalizer import terminalize
from omega_engine.crates.homology_theory.graph_complex import (
    get_triangle_complex,
    get_plaquette_complex,
    get_prism_complex,
)


class TestGraphComplex(unittest.TestCase):
    def test_graph_to_complex_toy_graphs(self):
        # Triangle graph
        tri = get_triangle_complex()
        self.assertEqual(tri.num_vertices, 3)
        self.assertEqual(tri.num_edges, 3)
        self.assertEqual(tri.num_faces, 1)

        # Plaquette grid
        grid = get_plaquette_complex()
        self.assertEqual(grid.num_vertices, 4)
        self.assertEqual(grid.num_edges, 4)
        self.assertEqual(grid.num_faces, 1)

        # Prism cell complex
        prism = get_prism_complex()
        self.assertEqual(prism.num_vertices, 6)
        self.assertEqual(prism.num_edges, 9)
        self.assertEqual(prism.num_faces, 5)

    def test_graph_complex_terminalizer(self):
        tri = get_triangle_complex()

        # Exact mismatch (a loop mismatch - which is in im(D0) for triangle loop boundary of vertices)
        carrier_exact = tri.create_carrier([1, 1, 0])
        res_exact = terminalize(carrier_exact.D0, carrier_exact.D1, carrier_exact.residual)
        self.assertEqual(res_exact["terminal_status"], "Exact")

        # Open obstruction (fails D1 * r = 0)
        # For example, mismatching only 1 edge [1, 0, 0]
        carrier_open = tri.create_carrier([1, 0, 0])
        res_open = terminalize(carrier_open.D0, carrier_open.D1, carrier_open.residual)
        self.assertEqual(res_open["terminal_status"], "OpenObstruction")


if __name__ == "__main__":
    unittest.main()



