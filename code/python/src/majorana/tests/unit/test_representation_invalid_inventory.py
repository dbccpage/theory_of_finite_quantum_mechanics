"""Tests for all 7 RepresentationInvalid hard failure cases in terminalizer.py.

Verifies that malformed packets, shape mismatches, empty matrices, ragged inputs, and D1*D0 != 0
complex relation violations raise RepresentationInvalid or ValueError as specified by the GF(2) parity carrier design.
"""

import sys
import unittest
from pathlib import Path

# Ensure omega_engine.crates.majorana is in sys.path
majorana_dir = Path(__file__).resolve().parents[1]
if str(majorana_dir) not in sys.path:
    sys.path.insert(0, str(majorana_dir))

from omega_engine.crates.majorana.engines.terminalizer import terminalize, validate_complex
from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix


class TestRepresentationInvalidInventory(unittest.TestCase):
    def test_mode_1_residual_shorter_than_d0_rows(self):
        """Mode 1: Residual length < D0 rows -> RepresentationInvalid."""
        d0 = [[1], [1], [0]]  # 3 rows
        d1 = [[1, 1, 0]]      # 1 row, 3 cols
        r = [1, 0]             # length 2 != 3
        res = terminalize(d0, d1, r)
        self.assertEqual(res["terminal_status"], "RepresentationInvalid")
        self.assertIn("residual length", res["reason"].lower())

    def test_mode_2_residual_longer_than_d0_rows(self):
        """Mode 2: Residual length > D0 rows -> RepresentationInvalid."""
        d0 = [[1], [1], [0]]  # 3 rows
        d1 = [[1, 1, 0]]
        r = [1, 0, 0, 1]       # length 4 != 3
        res = terminalize(d0, d1, r)
        self.assertEqual(res["terminal_status"], "RepresentationInvalid")
        self.assertIn("residual length", res["reason"].lower())

    def test_mode_3_d1_columns_mismatch_d0_rows(self):
        """Mode 3: D1 columns != D0 rows -> RepresentationInvalid."""
        d0 = [[1], [1], [0]]  # 3 rows
        d1 = [[1, 1]]          # 2 columns != 3 rows
        r = [1, 0, 0]
        res = terminalize(d0, d1, r)
        self.assertEqual(res["terminal_status"], "RepresentationInvalid")
        self.assertIn("d1 column count", res["reason"].lower())


    def test_mode_4_complex_relation_broken_d1_d0_nonzero(self):
        """Mode 4: D1 * D0 != 0 -> RepresentationInvalid complex_relation_violation."""
        d0 = [[1], [0], [0]]   # D0 column 0 = [1, 0, 0]
        d1 = [[1, 1, 0]]       # D1 * D0 = [1*1 + 1*0 + 0*0] = [1] != [0]
        r = [1, 0, 0]
        res = terminalize(d0, d1, r)
        self.assertEqual(res["terminal_status"], "RepresentationInvalid")
        self.assertEqual(res["reason"], "D1*D0 != 0")
        self.assertEqual(res["algebraic_class_id"], "representation-invalid:complex_relation_violation")
        self.assertFalse(validate_complex(d0, d1))

    def test_mode_5_empty_d0(self):
        """Mode 5: D0 is empty -> RepresentationInvalid."""
        d0 = []
        d1 = []
        r = [1]
        res = terminalize(d0, d1, r)
        self.assertEqual(res["terminal_status"], "RepresentationInvalid")

    def test_mode_6_ragged_d0_raised_before_terminalize(self):
        """Mode 6: Ragged D0 matrix -> ValueError raised by GF2Matrix during initialization."""
        d0_ragged = [[1, 0], [0]]
        with self.assertRaises(ValueError):
            GF2Matrix(d0_ragged)

    def test_mode_7_subtle_d1_d0_nonzero(self):
        """Mode 7: Topological D0 + non-zero D1 row breaking D1*D0 = 0."""
        d0_ring = [[1, 0], [1, 1], [0, 1]]  # 3 rows, 2 cols
        d1_invalid = [[1, 0, 0]]            # D1*D0 = [1*1+0+0, 1*0+0+0] = [1, 0] != [0, 0]
        r = [0, 1, 0]
        res = terminalize(d0_ring, d1_invalid, r)
        self.assertEqual(res["terminal_status"], "RepresentationInvalid")
        self.assertEqual(res["reason"], "D1*D0 != 0")

    def test_empty_d1_is_legal(self):
        """Empty D1 (no faces) is legal and does NOT produce RepresentationInvalid."""
        d0 = [[1], [1], [0]]
        d1 = []               # Empty D1 (0 rows)
        r = [1, 1, 0]
        res = terminalize(d0, d1, r)
        self.assertNotEqual(res["terminal_status"], "RepresentationInvalid")
        self.assertEqual(res["terminal_status"], "Exact")


if __name__ == "__main__":
    unittest.main()



