"""Exact controls for the symmetry-price / minimal-input frontier certificate (PFP batch 01, PG-WDP-PROTECTED-QUESTIONS)."""
import importlib.util
import itertools
import unittest
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_wdp_protected_questions.py'
_SPEC = importlib.util.spec_from_file_location('pfp_wdp_protected_questions', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


def brute_invariant(n, mask):
    """Points fixed by every permutation of range(n) that fixes the points of `mask`."""
    keep = [p for p in itertools.permutations(range(n)) if all(p[i] == i for i in range(n) if mask >> i & 1)]
    return sum(1 << x for x in range(n) if all(p[x] == x for p in keep))


class ProtectedQuestions(unittest.TestCase):
    def test_closed_form_matches_brute_force_over_all_subsets_up_to_six(self):
        for n in range(0, 7):
            for mask in range(1 << n):
                self.assertEqual(m.invariant_mask(n, mask), brute_invariant(n, mask), (n, mask))

    def test_no_invariant_point_for_empty_declaration_when_two_or_more_points(self):
        for n in range(2, 7):
            self.assertEqual(brute_invariant(n, 0), 0)
            self.assertFalse(m.record(n)['table'][0][2])

    def test_boundary_cases(self):
        self.assertEqual(m.record(0)['table'], [[0, 0, False, False]])
        self.assertEqual(m.record(0)['frontier'], [])
        self.assertEqual(m.record(0)['min_price'], -1)
        r1 = m.record(1)
        self.assertEqual(r1['frontier'], [0])
        self.assertEqual(r1['min_price'], 0)
        self.assertEqual(r1['selecting_count'], 2)

    def test_frontier_is_the_singletons_from_two_points(self):
        for n in range(2, 7):
            r = m.record(n)
            self.assertEqual(r['frontier'], [1 << i for i in range(n)])
            self.assertEqual(r['frontier_size'], n)
            self.assertEqual(r['min_price'], 1)
            self.assertEqual(r['selecting_count'], (1 << n) - 1)

    def test_minimal_flag_agrees_with_definition(self):
        for n in range(0, 7):
            r = m.record(n)
            sel = {t[0] for t in r['table'] if t[2]}
            for mask, _, s, mn in r['table']:
                proper = [t for t in range(1 << n) if t & mask == t and t != mask]
                self.assertEqual(mn, s and not any(t in sel for t in proper), (n, mask))

    def test_two_point_carrier_complement_singleton_is_also_invariant(self):
        # n=2, S={0}: the complement {1} is one point, so both points are invariant.
        self.assertEqual(m.invariant_mask(2, 1), 3)
        # n=3, S={0}: complement {1,2} is two points, only 0 is invariant.
        self.assertEqual(m.invariant_mask(3, 1), 1)

    def test_wire_format(self):
        lines = m.wire_lines(m.certificate())
        self.assertEqual(len(lines), len(m.CASES))
        self.assertEqual(lines[0], 'sel\t0\t0\t0\t-1\t-\t0:0:0:0')
        self.assertTrue(lines[2].startswith('sel\t2\t3\t2\t1\t1;2\t0:0:0:0;1:3:1:1;2:3:1:1;3:3:1:0'))


if __name__ == '__main__':
    unittest.main()
