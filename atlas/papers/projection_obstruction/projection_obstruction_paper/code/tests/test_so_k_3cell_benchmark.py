"""Unit tests for SO(k) 3-cell complex benchmark solver."""

import sys
import unittest
from pathlib import Path
import numpy as np

# Ensure code directory is in sys.path
code_dir = Path(__file__).resolve().parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from so_k_3cell_benchmark import (
    generate_tetrahedral_complex,
    solve_so_k_vector_residual,
    benchmark_so_k_performance,
)


class TestSOk3CellBenchmark(unittest.TestCase):
    def test_tetrahedral_complex_generation(self):
        complex_3d = generate_tetrahedral_complex(n_nodes=5)
        # 5 nodes -> 10 edges, 10 triangles, 5 tetrahedra
        self.assertEqual(len(complex_3d.nodes), 5)
        self.assertEqual(len(complex_3d.edges), 10)
        self.assertEqual(len(complex_3d.faces), 10)
        self.assertEqual(len(complex_3d.volumes), 5)

    def test_pure_gauge_vector_field_zero_residual(self):
        complex_3d = generate_tetrahedral_complex(n_nodes=4)
        # SO(4) vector field: each node carries a 4-vector potential
        vector_pots = {
            0: np.array([0.0, 1.0, 2.0, 3.0]),
            1: np.array([1.0, 0.0, 4.0, 2.0]),
            2: np.array([3.0, 2.0, 1.0, 0.0]),
            3: np.array([5.0, 4.0, 3.0, 2.0]),
        }
        pure_edge_values = {
            (u, v): vector_pots[v] - vector_pots[u] for u, v in complex_3d.edges
        }
        res = solve_so_k_vector_residual(complex_3d, pure_edge_values)
        self.assertAlmostEqual(res["residual_size"], 0.0, places=4)
        self.assertTrue(res["is_pure_gauge"])

    def test_high_dimensional_so_k_benchmark_execution(self):
        results = benchmark_so_k_performance(dimensions=[3, 5, 8], n_nodes=6, seed=123)
        self.assertEqual(len(results), 3)
        for item in results:
            # 2026-08-31: "success" now reports real optimizer convergence
            # (converged AND finite residual), not just np.isfinite(size).
            self.assertTrue(item["success"])
            self.assertGreater(item["residual_size"], 0.0)
            self.assertLess(item["elapsed_ms"], 500.0)  # Should complete under 500ms per dim


if __name__ == "__main__":
    unittest.main()
