"""Exact controls for the phase-blind fiber / Hadamard interference certificate (PFP batch 01)."""
import importlib.util
import unittest
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_phase_blind_fiber.py'
_SPEC = importlib.util.spec_from_file_location('pfp_phase_blind_fiber', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


class PhaseBlindFiber(unittest.TestCase):
    def test_fiber_sizes_match_sum_of_two_squares_counts(self):
        # r2(1)=4, r2(2)=4, r2(5)=8, r2(25)=12, r2(3)=0, r2(0)=1
        self.assertEqual([len(m.fiber(n)) for n in (0, 1, 2, 3, 4, 5, 9, 25)], [1, 4, 4, 0, 4, 8, 4, 12])

    def test_named_witnesses_share_weights_but_not_readouts(self):
        a, b, c = (1, 0), (1, 0), (-1, 0)
        self.assertEqual((m.weight(b), m.weight(c)), (1, 1))
        self.assertEqual(m.readout(a, b), (4, 0))
        self.assertEqual(m.readout(a, c), (0, 4))

    def test_both_sectors_nonzero_and_realizable_never_descend(self):
        for w0 in range(1, 30):
            for w1 in range(1, 30):
                r = m.record(w0, w1)
                if r['realizable']:
                    self.assertFalse(r['descends'], (w0, w1))
                    self.assertGreaterEqual(r['distinct_readouts'], 2)

    def test_zero_sector_fiber_is_trivial_and_descends(self):
        for w in range(0, 30):
            r = m.record(0, w)
            if r['realizable']:
                self.assertEqual(r['fiber_sizes'][0], 1)
                self.assertTrue(r['descends'])

    def test_second_sector_zero_also_descends(self):
        for w in range(0, 30):
            r = m.record(w, 0)
            if r['realizable']:
                self.assertEqual(r['fiber_sizes'][1], 1)
                self.assertTrue(r['descends'])

    def test_total_is_doubled_everywhere(self):
        for r in m.certificate()['records']:
            self.assertTrue(r['total_doubled'])

    def test_interference_term_is_four_times_the_cross_product(self):
        for a in m.fiber(5):
            for b in m.fiber(2):
                ro = m.readout(a, b)
                self.assertEqual(ro[0] - ro[1], 4 * (a[0] * b[0] + a[1] * b[1]))

    def test_wire_format_has_one_line_per_case(self):
        self.assertEqual(len(m.wire_lines(m.certificate())), len(m.CASES))
        self.assertTrue(m.wire_lines(m.certificate())[0].startswith('fiber\t1\t1\t4\t4\t1\t3\t1\t0\t'))


if __name__ == '__main__':
    unittest.main()
