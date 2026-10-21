r"""Unit tests for Obstruction & Retraction Map Subsystem (Prompt #3).

Verifies:
1. PO-015 projection-obstruction operator evaluation.
2. Endomorphism cohomology candidate classification.
3. Five-axis presentation transformation.
4. Evidence-only projection-obstruction receipt hashing.
"""

import unittest
import numpy as np
from omega_engine.crates.evaluator.eval_projection_obstruction import (
    ProjectionObstructionReceipt,
    build_projection_obstruction_receipt,
    evaluate_endomorphism_cohomology,
)
from omega_engine.crates.operator.lambda_op.lamb_chain_obstruction import (
    compute_po_015_projection_obstruction,
)
from omega_engine.crates.operator.transforms.trans_presentation_axis import (
    apply_5axis_presentation_change,
)


class TestFiniteCochainObstruction(unittest.TestCase):
    def test_po_015_subcomplex_projection(self):
        d = np.array([[0.0, 1.0], [0.0, 0.0]])
        P = np.array([[1.0, 0.0], [0.0, 1.0]])

        is_sub, norm_val = compute_po_015_projection_obstruction(d, P)
        self.assertTrue(is_sub)
        self.assertEqual(norm_val, 0.0)

    def test_endomorphism_cohomology_classification(self):
        d = np.array([[0.0, 1.0], [0.0, 0.0]])
        eps_closed = np.array([[1.0, 0.0], [0.0, 1.0]])
        eps_nonclosed = np.array([[0.0, 0.0], [1.0, 0.0]])

        self.assertEqual(evaluate_endomorphism_cohomology(d, eps_closed), "P_CLOSED_NONEXACT")
        self.assertEqual(evaluate_endomorphism_cohomology(d, eps_nonclosed), "P_NONCLOSED")

    def test_5axis_presentation_change(self):
        cochain = (1.0, 2.0)
        transform = ((2.0, 0.0), (0.0, 3.0))

        res = apply_5axis_presentation_change(cochain, axis=1, transform_matrix=transform)
        self.assertEqual(res, (2.0, 6.0))

        with self.assertRaises(ValueError):
            apply_5axis_presentation_change(cochain, axis=6, transform_matrix=transform)

    def test_build_projection_obstruction_receipt(self):
        d = np.array([[0.0, 1.0], [0.0, 0.0]])
        P = np.array([[1.0, 0.0], [0.0, 1.0]])
        eps = np.array([[1.0, 0.0], [0.0, 1.0]])

        receipt = build_projection_obstruction_receipt(d, P, eps, presentation_axis=1)
        self.assertIsInstance(receipt, ProjectionObstructionReceipt)
        self.assertEqual(receipt.endomorphism_class, "P_CLOSED_NONEXACT")
        self.assertTrue(receipt.is_non_retractable)
        self.assertEqual(receipt.authority_effect, "None")
        self.assertEqual(len(receipt.evidence_sha256), 64)


if __name__ == "__main__":
    unittest.main()
