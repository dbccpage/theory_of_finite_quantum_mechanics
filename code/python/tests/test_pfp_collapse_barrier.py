"""Exact controls for the collapsed observation barrier certificate (PFP batch 01, PG-COLLAPSE-BARRIER)."""
import importlib.util
import unittest
from itertools import product
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_collapse_barrier.py'
_SPEC = importlib.util.spec_from_file_location('pfp_collapse_barrier', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


class CollapseBarrier(unittest.TestCase):
    def test_barrier_has_no_exceptions_on_every_case(self):
        for r in m.certificate()['records']:
            self.assertEqual(r['violations'], 0, r['input'])
            self.assertEqual(r['fibre_constant'] + r['collapsed_separated'], r['total'], r['input'])
            self.assertLessEqual(r['factoring'], r['fibre_constant'], r['input'])

    def test_fibre_constant_iff_factoring_when_task_codomain_is_inhabited(self):
        # brute-force cross-check of the general iff on every small triple with Z nonempty
        for n in range(0, 4):
            for my in range(0, 4):
                for mz in range(1, 4):
                    r = m.record(n, my, mz)
                    self.assertEqual(r['factoring'], r['fibre_constant'], (n, my, mz))

    def test_empty_task_codomain_is_the_boundary_of_the_iff(self):
        r = m.record(0, 1, 0)
        self.assertEqual((r['fibre_constant'], r['factoring'], r['factorizations']), (1, 0, 0))
        self.assertEqual(m.record(0, 0, 0)['factoring'], 1)  # empty profile codomain: the empty map factors

    def test_factorizations_count_is_my_pow_n_times_mz_pow_my(self):
        for n in range(0, 4):
            for my in range(0, 4):
                for mz in range(0, 4):
                    self.assertEqual(m.record(n, my, mz)['factorizations'], my ** n * mz ** my, (n, my, mz))

    def test_least_tag_alphabet_is_max_distinct_task_values_in_a_fibre(self):
        for (n, my, mz) in [(3, 1, 3), (3, 2, 3), (4, 2, 3)]:
            hist = {}
            for p in product(range(my), repeat=n):
                for s in product(range(mz), repeat=n):
                    fibres = {}
                    for a, b in zip(p, s):
                        fibres.setdefault(a, set()).add(b)
                    k = max([1] + [len(v) for v in fibres.values()])
                    hist[k] = hist.get(k, 0) + 1
            self.assertEqual(m.record(n, my, mz)['min_tag_hist'], [[k, hist[k]] for k in sorted(hist)])

    def test_factoring_criterion_used_for_tags_matches_g_enumeration(self):
        # k = 1: some g exists iff s is fibre-constant and (Z inhabited or p onto Y)
        for n in range(0, 4):
            for my in range(0, 4):
                for mz in range(0, 4):
                    for p in product(range(my), repeat=n):
                        for s in product(range(mz), repeat=n):
                            by_g = m.count_g(list(p), my, s, mz) > 0
                            by_criterion = m.fibre_constant(p, s) and (mz >= 1 or len(set(p)) == my)
                            self.assertEqual(by_g, by_criterion, (n, my, mz, p, s))

    def test_empty_carrier_needs_the_empty_tag_alphabet(self):
        for my in range(0, 3):
            for mz in range(0, 3):
                self.assertEqual(m.record(0, my, mz)['min_tag_hist'], [[0, 1]])

    def test_collapsed_two_point_carrier_needs_a_two_valued_tag(self):
        r = m.record(2, 1, 2)
        self.assertEqual(r['min_tag_hist'], [[1, 2], [2, 2]])
        self.assertEqual(r['collapsed_separated'], 2)

    def test_injective_profiles_never_collapse(self):
        # identity profile on 3 points: every task factors
        self.assertTrue(m.fibre_constant((0, 1, 2), (1, 0, 1)))
        r = m.record(3, 3, 2)
        self.assertEqual(r['factoring'], r['fibre_constant'])

    def test_wire_format_has_one_line_per_case(self):
        lines = m.wire_lines(m.certificate())
        self.assertEqual(len(lines), len(m.CASES))
        self.assertEqual(lines[8], 'tag\t3\t3\t2\t216\t126\t90\t126\t216\t0\t1:126;2:90')
        self.assertEqual(m.public_tsv().splitlines()[0], 'tag\t0\t0\t1')


if __name__ == '__main__':
    unittest.main()
