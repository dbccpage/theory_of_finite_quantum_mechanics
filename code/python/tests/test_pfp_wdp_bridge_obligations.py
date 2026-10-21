"""Exact controls for the bridge-obligation status ledger (PFP batch 01, PG-WDP-GENESIS-BRIDGE-OBLIGATIONS)."""
import importlib.util
import unittest
from itertools import product
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_wdp_bridge_obligations.py'
_SPEC = importlib.util.spec_from_file_location('pfp_wdp_bridge_obligations', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


class BridgeObligations(unittest.TestCase):
    def test_all_243_vectors_are_enumerated_once(self):
        self.assertEqual(len(m.CASES), 3 ** 5)
        self.assertEqual(len(set(m.CASES)), 243)

    def test_exactly_one_vector_is_end_to_end_and_it_is_all_discharged(self):
        done = [r['v'] for r in m.certificate()['records'] if r['end_to_end']]
        self.assertEqual(done, [[2, 2, 2, 2, 2]])

    def test_controls_passing_is_not_discharge(self):
        recs = m.certificate()['records']
        controls = [r for r in recs if r['controls_run']]
        self.assertEqual(len(controls), 32)
        self.assertEqual(len([r for r in controls if not r['end_to_end']]), 31)
        source = [r for r in recs if r['source_reported']]
        self.assertEqual([r['v'] for r in source], [[1, 1, 1, 1, 1]])
        self.assertTrue(source[0]['controls_run'] and not source[0]['end_to_end'])

    def test_end_to_end_iff_all_five_discharged_bruteforce(self):
        for v in product(range(3), repeat=5):
            r = m.record(''.join(map(str, v)))
            self.assertEqual(r['end_to_end'], all(s == 2 for s in v))

    def test_single_position_upgrades_are_monotone_and_complete_only_from_four_discharged(self):
        for v in product(range(3), repeat=5):
            ups, completing = 0, 0
            for k in range(5):
                for s in range(v[k] + 1, 3):
                    w = list(v)
                    w[k] = s
                    ups += 1
                    self.assertTrue(all(a <= b for a, b in zip(v, w)))
                    completing += all(x == 2 for x in w)
            r = m.record(''.join(map(str, v)))
            self.assertEqual((r['upgrades'], r['completing_upgrades']), (ups, completing))

    def test_prefix_order_counts(self):
        recs = m.certificate()['records']
        self.assertEqual(len([r for r in recs if r['prefix_order']]), 63)
        self.assertTrue(m.record('22222')['prefix_order'])
        self.assertFalse(m.record('00002')['prefix_order'])

    def test_no_square_root_of_two_rational_in_a_wide_box(self):
        # general statement is kernel-checked; this is a brute-force cross-check on a range
        for q in range(1, 200):
            for p in range(1, 300):
                self.assertNotEqual(p * p, 2 * q * q)

    def test_pair_defect_forgets_orientation_on_two_points(self):
        # windows over {0,1}: adj0 = 0->1 only, adj1 = 1->0 only; same symmetric pair defect, different adjacency
        adj0 = {(0, 1): True}
        adj1 = {(1, 0): True}

        def defect(adj, u, v):
            return adj.get((u, v), False) or adj.get((v, u), False)

        self.assertNotEqual(adj0, adj1)
        for u, v in product(range(2), repeat=2):
            self.assertEqual(defect(adj0, u, v), defect(adj1, u, v))

    def test_wire_format(self):
        lines = m.wire_lines(m.certificate())
        self.assertEqual(len(lines), 243)
        self.assertEqual(lines[0], 'led\t00000\t5\t0\t0\t0\t0\t1\t10\t0\t0')
        self.assertEqual(lines[-1], 'led\t22222\t0\t0\t5\t1\t1\t1\t0\t0\t0')


if __name__ == '__main__':
    unittest.main()
