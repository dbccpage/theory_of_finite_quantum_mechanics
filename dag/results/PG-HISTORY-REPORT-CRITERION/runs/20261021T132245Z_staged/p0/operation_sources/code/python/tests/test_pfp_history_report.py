"""Exact controls for the history-report criterion certificate (PFP batch 01, PG-HISTORY-REPORT-CRITERION)."""
import importlib.util
import unittest
from itertools import product
from math import comb
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_history_report.py'
_SPEC = importlib.util.spec_from_file_location('pfp_history_report', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


def surjections(h, k):
    """Number of surjections from h points onto k points by inclusion-exclusion."""
    return sum((-1) ** j * comb(k, j) * (k - j) ** h for j in range(k + 1))


class HistoryReport(unittest.TestCase):
    def test_criterion_holds_pairwise_on_a_range(self):
        for h in range(0, 4):
            for v in range(0, 4):
                for s in range(0, 3):
                    r = m.record(h, v, s)
                    self.assertEqual(r['mismatch'], 0, (h, v, s))
                    self.assertEqual(r['fiber_constant'], r['factoring'], (h, v, s))

    def test_factoring_count_is_sum_over_image_sizes(self):
        for h in range(0, 5):
            for v in range(0, 4):
                for s in range(0, 3):
                    want = sum(comb(v, k) * surjections(h, k) * s ** k for k in range(0, min(h, v) + 1))
                    self.assertEqual(m.record(h, v, s)['factoring'], want, (h, v, s))

    def test_extensions_total_is_v_pow_h_times_s_pow_v(self):
        for h in range(0, 4):
            for v in range(0, 4):
                for s in range(0, 3):
                    self.assertEqual(m.record(h, v, s)['extensions_total'], v ** h * s ** v, (h, v, s))

    def test_factor_on_image_is_unique_and_never_exceeds_one(self):
        for h in range(0, 4):
            for v in range(0, 4):
                for s in range(0, 4):
                    self.assertLessEqual(m.record(h, v, s)['max_factor_multiplicity'], 1)

    def test_surjective_reports_have_unique_extension(self):
        for h in range(0, 5):
            for v in range(0, 4):
                for s in range(0, 3):
                    r = m.record(h, v, s)
                    self.assertEqual(r['surjective_nonunique'], 0, (h, v, s))
                    self.assertEqual(r['surjective_reports'], surjections(h, v), (h, v, s))

    def test_off_image_extension_is_not_unique_when_room_exists(self):
        # one history, two reports, two answers: the image is a single point and the other report is free
        r = m.record(1, 2, 2)
        self.assertEqual((r['factoring'], r['nonunique_off_image']), (4, 4))
        # no room off the image when the report is onto
        r = m.record(2, 1, 2)
        self.assertEqual(r['nonunique_off_image'], 0)
        # one answer: nothing to vary
        self.assertEqual(m.record(3, 3, 1)['nonunique_off_image'], 0)

    def test_degenerate_cases(self):
        self.assertEqual(m.record(0, 0, 0)['factoring'], 1)       # the empty question factors through the empty image
        self.assertEqual(m.record(1, 0, 2)['pairs'], 0)           # no report from one history into the empty report type
        self.assertEqual(m.record(1, 1, 0)['pairs'], 0)           # no question into the empty answer type
        self.assertEqual(m.record(0, 2, 2)['extensions_total'], 4)
        # no answer values: the empty question factors through the empty image but has no extension to a nonempty report type
        r = m.record(0, 2, 0)
        self.assertEqual((r['pairs'], r['factoring'], r['extensions_total'], r['nonunique_off_image']), (1, 1, 0, 0))
        self.assertEqual(m.CASES[-1], (0, 2, 0))

    def test_split_pair_is_not_fiber_constant_by_direct_search(self):
        # report h mod 2 on three histories, answer = h: histories 0 and 2 share a report but not an answer
        rep, ans = (0, 1, 0), (0, 1, 2)
        self.assertTrue(any(rep[i] == rep[j] and ans[i] != ans[j] for i in range(3) for j in range(3)))
        g_exists = any(all(g[{0: 0, 1: 1}[rep[i]]] == ans[i] for i in range(3)) for g in product(range(3), repeat=2))
        self.assertFalse(g_exists)

    def test_wire_format_has_one_line_per_case(self):
        lines = m.wire_lines(m.certificate())
        self.assertEqual(len(lines), len(m.CASES))
        self.assertEqual(lines[11], 'report\t3\t3\t2\t216\t126\t126\t0\t1:3;2:18;3:6\t1\t216\t78\t6\t0')
        self.assertTrue(all(line == line.strip() and '\t\t' not in line for line in lines))


if __name__ == '__main__':
    unittest.main()
