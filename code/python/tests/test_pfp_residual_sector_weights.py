"""Exact controls for the residual sector-weight certificate (PFP batch 01, L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED)."""
import importlib.util
import unittest
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_residual_sector_weights.py'
_SPEC = importlib.util.spec_from_file_location('pfp_residual_sector_weights', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


def brute_class(n, c, masses=None):
    """All (weighted L1, residual) pairs of the class c - d0 h over a gauge-fixed box (independent of the producer)."""
    masses = masses or [1] * n
    box = sum(abs(v) for v in c) + sum(a * abs(v) for a, v in zip(masses, c)) // min(masses)
    out = set()
    for tail in product(range(-box, box + 1), repeat=n - 1):
        h = (0,) + tail
        r = tuple(c[i] - (h[(i + 1) % n] - h[i]) for i in range(n))
        out.add((sum(a * abs(v) for a, v in zip(masses, r)), r))
    return out


class ResidualSectorWeights(unittest.TestCase):
    def test_phi1_is_abs_holonomy_and_minimizers_form_a_signed_simplex(self):
        # brute-force cross-check of the general claim: entries in [-2, 2] for n <= 3, in [-1, 1] for n = 4
        for n in range(1, 5):
            for c in product(range(-2, 3) if n <= 3 else range(-1, 2), repeat=n):
                pairs = brute_class(n, c)
                best = min(p[0] for p in pairs)
                S = sum(c)
                self.assertEqual(best, abs(S), (n, c))
                mins = {p[1] for p in pairs if p[0] == best}
                self.assertEqual(len(mins), comb(abs(S) + n - 1, n - 1), (n, c))
                for r in mins:
                    self.assertEqual(sum(r), S)
                    self.assertTrue(all(v * (1 if S >= 0 else -1) >= 0 for v in r))

    def test_holonomy_is_the_class_invariant(self):
        for n in (2, 3):
            for c in product(range(-2, 3), repeat=n):
                self.assertEqual({sum(p[1]) for p in brute_class(n, c)}, {sum(c)})

    def test_two_nonempty_sectors_are_not_determined_by_phi1_and_holonomy(self):
        for n in (2, 3, 4):
            for c in product(range(-2, 3), repeat=n):
                for k in range(1, n):
                    r = m.record_residual(n, c, (k, n - k))
                    if r['phi1'] > 0:
                        self.assertFalse(r['determined'], (n, c, k))
                        self.assertFalse(r['unique'])
                        self.assertEqual(len(r['sector_vectors']), r['phi1'] + 1)
                        for v in r['sector_vectors']:
                            self.assertEqual(sum(v), r['phi1'])

    def test_single_sector_and_single_edge_and_zero_mass_boundaries(self):
        self.assertTrue(m.record_residual(4, (1, 1, 0, 0), (4,))['determined'])
        self.assertTrue(m.record_residual(1, (5,), (1,))['unique'])
        z = m.record_residual(4, (1, -1, 0, 0), (2, 2))
        self.assertEqual((z['status'], z['unique'], z['lex_min'], z['lex_max']), ('zero_mass_refused', True, [0, 0, 0, 0], [0, 0, 0, 0]))

    def test_symmetric_point_is_orbit_average_and_integral_iff_divisible(self):
        r = m.record_residual(4, (1, 0, 1, 0), (2, 2))
        self.assertEqual((r['symmetric'], r['symmetric_integral']), ([1, 2], False))  # the source orbit SUM (1,1,1,1) is twice Phi1
        for n in range(1, 7):
            for S in range(-12, 13):
                rec = m.record_residual(n, (S,) + (0,) * (n - 1), (n,))
                self.assertEqual(rec['symmetric_integral'], S % n == 0)
                self.assertEqual(Fraction(*rec['symmetric']) * n, abs(S))

    def test_sum_of_squares_is_not_constant_on_the_minimizers_once_mass_is_at_least_two(self):
        for n in range(2, 6):
            for S in range(1, 8):
                rec = m.record_residual(n, (S,) + (0,) * (n - 1), (n,))
                pairs = brute_class(n, (S,) + (0,) * (n - 1)) if S <= 3 and n <= 4 else None
                if pairs:
                    best = min(p[0] for p in pairs)
                    squares = [sum(v * v for v in p[1]) for p in pairs if p[0] == best]
                    self.assertEqual((min(squares), max(squares)), (rec['sumsq_min'], rec['sumsq_max']))
                self.assertEqual(rec['sumsq_min'] < rec['sumsq_max'], S >= 2)

    def test_negative_class_has_nonpositive_extremes(self):
        r = m.record_residual(4, (-2, 0, -1, 0), (2, 2))
        self.assertEqual((r['holonomy'], r['phi1'], r['lex_min'], r['lex_max']), (-3, 3, [-3, 0, 0, 0], [0, 0, 0, -3]))

    def test_weighted_minimizers_live_on_the_minimal_mass_edges_brute_force(self):
        for masses in ([1, 2, 3], [2, 1, 1], [3, 3, 1], [1, 1, 1], [2, 5, 2]):
            for c in product(range(-2, 3), repeat=3):
                pairs = brute_class(3, c, masses)
                best = min(p[0] for p in pairs)
                mins = sorted({p[1] for p in pairs if p[0] == best})
                rec = m.record_weighted(3, c, (1, 2), masses)
                self.assertEqual(best, rec['weighted_phi1'])
                self.assertEqual(len(mins), rec['minimizer_count'])
                self.assertEqual((list(mins[0]), list(mins[-1])), (rec['lex_min'], rec['lex_max']))
        one = m.record_weighted(4, (1, 0, 1, 0), (2, 2), (1, 2, 3, 4))
        self.assertEqual((one['unique'], one['determined'], one['sector_vectors']), (True, True, [[2, 0]]))
        face = m.record_weighted(4, (3, 0, 0, 0), (2, 2), (2, 2, 1, 1))
        self.assertEqual((face['unique'], face['determined'], face['minimizer_count']), (False, True, 4))

    def test_two_disjoint_cycles_need_both_holonomies(self):
        r = m.record_twocycle(3, (2, 0, 0), 3, (-1, 0, 0))
        self.assertEqual((r['holonomies'], r['phi1'], r['total_holonomy'], r['total_gives_phi1'], r['minimizer_count']), ([2, -1], 3, 1, False, 18))
        for c1 in product(range(-1, 2), repeat=2):
            for c2 in product(range(-1, 2), repeat=2):
                p1, p2 = min(p[0] for p in brute_class(2, c1)), min(p[0] for p in brute_class(2, c2))
                self.assertEqual(m.record_twocycle(2, c1, 2, c2)['phi1'], p1 + p2)

    def test_wire_format_has_one_line_per_case_and_no_empty_field(self):
        lines = m.wire_lines(m.certificate())
        self.assertEqual(len(lines), len(m.CASES))
        for line in lines:
            fields = line.split('\t')
            self.assertEqual(len(fields), {'residual': 17, 'weighted': 14, 'twocycle': 10}[fields[0]])
            self.assertTrue(all(fields) and line == line.strip())
        self.assertEqual(lines[0], 'residual\t4\t1,0,1,0\t2,2\t2\t2\t10\t0,0,0,2\t2,0,0,0\t0,2;1,1;2,0\t0\t0\t1/2\t0\t2\t4\tok')
        self.assertEqual(len(m.public_tsv().splitlines()), len(m.CASES))


if __name__ == '__main__':
    unittest.main()
