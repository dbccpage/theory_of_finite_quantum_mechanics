# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jeremy H. Carroll

import unittest
from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix

class TestGF2Matrix(unittest.TestCase):
    def test_gf2_matrix_operations(self):
        # Transpose
        A = GF2Matrix([[1, 0], [1, 1], [0, 1]])
        A_T = A.transpose()
        self.assertEqual(A_T.rows, 2)
        self.assertEqual(A_T.cols, 3)
        self.assertEqual(A_T.data, [[1, 1, 0], [0, 1, 1]])

        # Matrix-vector multiplication
        v = [1, 1]
        res = A.mat_vec_mul(v)
        self.assertEqual(res, [1, 0, 1])

        # RREF
        rref_A, pivots = A.rref()
        self.assertEqual(rref_A.data, [[1, 0], [0, 1], [0, 0]])
        self.assertEqual(pivots, [0, 1])

        # Solve consistent
        b1 = [1, 0, 1]
        x1 = A.solve(b1)
        self.assertEqual(x1, [1, 1])

        # Solve inconsistent
        b2 = [1, 1, 1]
        x2 = A.solve(b2)
        self.assertIsNone(x2)

    def test_ragged_matrix_refusal(self):
        with self.assertRaises(ValueError):
            GF2Matrix([[1, 0], [1]])


if __name__ == "__main__":
    unittest.main()



