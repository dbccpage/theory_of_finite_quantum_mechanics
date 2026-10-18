# SPDX-License-Identifier: Apache-2.0
# Copyright 2026

import unittest
from omega_engine.crates.majorana.carriers.tetron_carrier import build_tetron_array_carrier
from omega_engine.crates.majorana.engines.terminalizer import terminalize


class TestTetronCarrier(unittest.TestCase):
    def test_single_tetron_shape(self):
        """Verify single tetron (N=1) shape and metadata."""
        carrier = build_tetron_array_carrier(num_tetrons=1)
        carrier.validate_shape()

        self.assertEqual(carrier.metadata["num_tetrons"], 1)
        self.assertEqual(carrier.metadata["total_modes"], 6)
        self.assertEqual(carrier.metadata["num_bonds"], 4)
        self.assertEqual(carrier.metadata["authority_effect"], "None")

    def test_two_tetron_array_topology_and_terminalizer(self):
        """Verify 2-tetron array carrier topology and terminalization."""
        carrier = build_tetron_array_carrier(num_tetrons=2)
        carrier.validate_shape()

        self.assertEqual(carrier.metadata["num_tetrons"], 2)
        self.assertEqual(carrier.metadata["total_modes"], 12)
        self.assertEqual(carrier.metadata["num_bonds"], 10)

        # Terminalize carrier with default parity defect on bond 0
        term_res = terminalize(carrier.D0, carrier.D1, carrier.residual)
        self.assertIn(term_res["terminal_status"], ["Exact", "ClosedResidual", "OpenObstruction"])
        self.assertEqual(carrier.metadata["authority_effect"], "None")


if __name__ == "__main__":
    unittest.main()



