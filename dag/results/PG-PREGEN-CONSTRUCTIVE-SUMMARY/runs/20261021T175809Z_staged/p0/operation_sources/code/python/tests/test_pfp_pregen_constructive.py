"""Exact controls for the listed-history summary certificate (PFP batch 01, PG-PREGEN-CONSTRUCTIVE-SUMMARY)."""
import importlib.util
import unittest
from itertools import product
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_pregen_constructive.py'
_SPEC = importlib.util.spec_from_file_location('pfp_pregen_constructive', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


def all_lists(p, ell):
    out = [()]
    for k in range(1, ell + 1):
        out += list(product(range(p), repeat=k))
    return out


class PregenConstructive(unittest.TestCase):
    def test_listed_criterion_on_a_range(self):
        for p in range(0, 4):
            for ell in range(0, 4):
                for v in range(0, 3):
                    for s in range(0, 3):
                        r = m.record(p, ell, v, s)
                        self.assertEqual(r['mismatch'], 0, (p, ell, v, s))
                        self.assertEqual(r['listed_fc'], r['recon_correct'], (p, ell, v, s))
                        self.assertEqual(r['complete_mismatch'], 0, (p, ell, v, s))

    def test_listing_and_triple_totals(self):
        for p, ell, v, s in [(2, 3, 2, 2), (3, 2, 2, 3), (3, 4, 1, 2)]:
            r = m.record(p, ell, v, s)
            self.assertEqual(r['lists'], sum(p ** k for k in range(ell + 1)))
            self.assertEqual(r['triples'], r['lists'] * v ** p * s ** p)

    def test_recon_uniqueness_on_listed_reports_by_search(self):
        # any f: V -> Option S returning every listed answer agrees with recon on every listed report
        p, v, s = 3, 2, 2
        options = [None] + list(range(s))
        for listing in [(0, 1), (2, 0, 2), (1,)]:
            for report in product(range(v), repeat=p):
                for answer in product(range(s), repeat=p):
                    if not all(m.recon(listing, report, answer, report[a]) == answer[a] for a in listing):
                        continue
                    for f in product(options, repeat=v):
                        if all(f[report[a]] == answer[a] for a in listing):
                            for a in listing:
                                self.assertEqual(m.recon(listing, report, answer, report[a]), f[report[a]])

    def test_refusal_is_exactly_unreported(self):
        for listing in all_lists(3, 3):
            for report in product(range(3), repeat=3):
                for x in range(3):
                    got = m.recon(listing, report, (0, 0, 0), x)
                    self.assertEqual(got is None, all(report[a] != x for a in listing))

    def test_first_occurrence_weight_lemma(self):
        # listings of length <= 3 over 3 histories that reduce to the first-occurrence sequence (1, 0): S2(k,2) summed over k <= 3
        count = 0
        for listing in all_lists(3, 3):
            first = []
            for a in listing:
                if a not in first:
                    first.append(a)
            count += first == [1, 0]
        self.assertEqual(count, 0 + 0 + 1 + 3)

    def test_failure_off_the_listing_exists(self):
        # listing (0,) of report h mod 2 over histories 0,1,2 with answer h: fiber constant on the listing, wrong for history 2
        report, answer = (0, 1, 0), (0, 1, 2)
        self.assertEqual(m.recon((0,), report, answer, report[2]), 0)
        self.assertNotEqual(m.recon((0,), report, answer, report[2]), answer[2])
        self.assertIsNone(m.recon((0,), report, answer, report[1]))

    def test_wire_format(self):
        lines = m.wire_lines(m.certificate())
        self.assertEqual(len(lines), len(m.CASES))
        self.assertEqual(lines[2], 'listed\t1\t2\t2\t2\t3\t12\t12\t12\t0\t8\t0\t0\t4\t0\t0')
        self.assertTrue(all(line == line.strip() and '\t\t' not in line for line in lines))


if __name__ == '__main__':
    unittest.main()
