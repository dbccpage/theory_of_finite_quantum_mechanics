"""Unit tests verifying L1 optimization solver gap closures."""

import unittest
from sympy import Matrix

try:
    from omega_engine.crates.functional.higher_simplex_assembly import (
        SimplexComplex,
        rational_boundary_matrix,
        exact_quotient_l1_distance,
    )
    from omega_engine.crates.discrete_deformation_algebra.degree_generic_residual import evaluate_residual
except ImportError:
    from omega_engine.crates.functional.higher_simplex_assembly import (
        SimplexComplex,
        rational_boundary_matrix,
        exact_quotient_l1_distance,
    )
    from omega_engine.crates.discrete_deformation_algebra.degree_generic_residual import evaluate_residual


class TestL1SolverGaps(unittest.TestCase):
    def test_exact_rational_simplicial_bridge(self):
        """Verify Gap 3: Bridge simplicial complex boundary matrix with exact rational LinearRepairProblem."""
        complex_obj = SimplexComplex(
            vertices=[0, 1, 2],
            cells={
                0: [(0,), (1,), (2,)],
                1: [(0, 1), (1, 2), (0, 2)],
                2: [(0, 1, 2)],
            },
            max_dim=2,
        )

        d1_rational = rational_boundary_matrix(complex_obj.cells[1], complex_obj.cells[0])
        self.assertIsInstance(d1_rational, Matrix)
        self.assertEqual(d1_rational.shape, (3, 3))

        cert = exact_quotient_l1_distance(complex_obj, dim=1, cochain_raw=[1, 1, -2])
        self.assertTrue(cert.verify())
        self.assertEqual(cert.distance, 4)

    def test_degree_1_dual_certified_residual(self):
        """Verify Gap 1: Degree-1 residual evaluation attaches dual witness certificate & duality gap receipt."""
        complex_obj = SimplexComplex(
            vertices=[0, 1, 2],
            cells={
                0: [(0,), (1,), (2,)],
                1: [(0, 1), (1, 2), (0, 2)],
            },
            max_dim=1,
        )

        cochain = {(0, 1): 1.0, (1, 2): 1.0, (0, 2): 2.0}
        report = evaluate_residual(complex_obj, degree=1, cochain=cochain, method="l1_gauge")

        self.assertEqual(report.degree, 1)
        self.assertTrue(report.is_certified)
        self.assertIsNotNone(report.duality_gap)
        self.assertLessEqual(report.duality_gap, 1e-6)


if __name__ == "__main__":
    unittest.main()


