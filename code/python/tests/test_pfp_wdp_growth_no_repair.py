"""Exact controls for the growth / no-repair certificate (PFP batch 01, PG-WDP-GROWTH-NO-REPAIR)."""
import importlib.util
import unittest
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_wdp_growth_no_repair.py'
_SPEC = importlib.util.spec_from_file_location('pfp_wdp_growth_no_repair', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


def lattice_phi(nv, edges, w, h, radius=5):
    d0 = m.d0_rows(nv, edges)
    best = None
    for x in product(range(-radius, radius + 1), repeat=nv):
        cost = sum(w[i] * abs(h[i] - sum(d0[i][j] * x[j] for j in range(nv))) for i in range(len(d0)))
        if best is None or cost < best:
            best = cost
    return best


def restrict_case(base, keep, neww='-'):
    arg = ','.join(map(str, keep)) + '|' + neww
    return dict(base, kind='restrict', arg=arg)


class GrowthNoRepair(unittest.TestCase):
    def test_both_windows_of_every_pair_match_integer_lattice_search(self):
        for c in m.CASES:
            nvb, eb, wb, db, hb = m.derive_b(c)
            self.assertEqual(m.phi1(c['nv'], c['edges'], c['w'], c['h']), lattice_phi(c['nv'], c['edges'], c['w'], c['h']), c['id'])
            self.assertEqual(m.phi1(nvb, eb, wb, hb), lattice_phi(nvb, eb, wb, hb), c['id'])

    def test_restriction_never_raises_phi1_over_every_edge_subset_of_k4(self):
        base = {'id': 'x', 'nv': 4, 'edges': m.K4_E, 'w': [1] * 6, 'd1': m.K4_D1, 'h': None}
        hs = list(product((-1, 0, 1), repeat=6))[::3]
        subsets = [list(s) for k in range(1, 7) for s in combinations(range(6), k)]
        self.assertEqual(len(subsets), 63)
        checked = 0
        for h in hs:
            c0 = dict(base, h=list(h))
            phi_big = m.phi1(4, m.K4_E, [1] * 6, list(h))
            for keep in subsets:
                nvb, eb, wb, db, hb = m.derive_b(restrict_case(c0, keep))
                self.assertLessEqual(m.phi1(nvb, eb, wb, hb), phi_big, (h, keep))
                checked += 1
        self.assertEqual(checked, len(hs) * 63)

    def test_restriction_with_parallel_edges_exhaustive_and_weight_hypothesis_is_needed(self):
        raised = 0
        for h in product(range(-2, 3), repeat=3):
            base = {'id': 'p', 'nv': 2, 'edges': m.PAR_E, 'w': [2, 2, 2], 'd1': [], 'h': list(h)}
            big = m.phi1(2, m.PAR_E, [2, 2, 2], list(h))
            for k in (1, 2, 3):
                for keep in combinations(range(3), k):
                    for wsub in product((1, 2, 3), repeat=k):
                        nvb, eb, wb, db, hb = m.derive_b(restrict_case(base, list(keep), ','.join(map(str, wsub))))
                        small = m.phi1(nvb, eb, wb, hb)
                        if all(x <= 2 for x in wsub):
                            self.assertLessEqual(small, big, (h, keep, wsub))
                        elif small > big:
                            raised += 1
        self.assertGreater(raised, 0)  # raising the weights can raise Phi1: the hypothesis is not removable

    def test_attachment_of_every_valid_row_on_k4_keeps_phi1_and_adds_to_gamma2(self):
        h = [1, 0, 2, 1, 0, 1]
        d0 = m.d0_rows(4, m.K4_E)
        valid = 0
        for row in product((-1, 0, 1), repeat=6):
            is_valid = all(sum(row[e] * d0[e][v] for e in range(6)) == 0 for v in range(4))
            self.assertEqual(is_valid, m.cochain_defect(4, m.K4_E, [list(row)]) is None)
            if not is_valid:
                continue
            valid += 1
            c = {'id': 'a', 'nv': 4, 'edges': m.K4_E, 'w': [1] * 6, 'd1': [], 'h': h, 'kind': 'attach', 'arg': ','.join(map(str, row))}
            nvb, eb, wb, db, hb = m.derive_b(c)
            self.assertEqual(m.phi1(nvb, eb, wb, hb), m.phi1(4, m.K4_E, [1] * 6, h))
            self.assertEqual(m.gamma2(db, hb), m.gamma2([], h) + abs(sum(r * x for r, x in zip(row, h))))
        self.assertGreater(valid, 10)

    def test_unrepaired_residual_sum_is_only_an_upper_bound(self):
        strict = 0
        for c in m.CASES:
            nvb, eb, wb, db, hb = m.derive_b(c)
            self.assertLessEqual(m.phi1(c['nv'], c['edges'], c['w'], c['h']), sum(a * abs(b) for a, b in zip(c['w'], c['h'])))
            strict += m.phi1(nvb, eb, wb, hb) < sum(a * abs(b) for a, b in zip(wb, hb))
        self.assertGreater(strict, 0)

    def test_table_verdicts(self):
        by = {r['id']: r for r in m.certificate()['records']}
        self.assertEqual(by['parallel_restrict_rescaled_weights']['verdict'], 'sub_phi_gt')
        self.assertEqual((by['parallel_restrict_rescaled_weights']['phi_a'], by['parallel_restrict_rescaled_weights']['phi_b']), ('4', '6'))
        self.assertEqual(by['tri_unfilled_attach_face']['verdict'], 'phi_equal_gamma_up')
        self.assertEqual((by['tri_unfilled_attach_face']['diag_a'], by['tri_unfilled_attach_face']['diag_b']), ('ClosedResidual', 'ActiveClosureFailure'))
        self.assertEqual(by['tri_attach_invalid_row']['verdict'], 'attach_not_a_window')
        self.assertEqual(by['tri_edit_h_gauge_shift']['verdict'], 'phi_same')
        self.assertEqual(by['tri_edit_h_to_exact']['verdict'], 'phi_lower')
        verdicts = {r['verdict'] for r in by.values()}
        self.assertEqual(verdicts, {'sub_phi_le', 'sub_phi_gt', 'phi_equal_gamma_up', 'phi_equal_gamma_same', 'attach_not_a_window',
                                    'phi_lower', 'phi_same', 'phi_higher'})

    def test_wire_format_has_one_line_per_case(self):
        lines = m.wire_lines(m.certificate())
        self.assertEqual(len(lines), len(m.CASES))
        self.assertTrue(lines[0].startswith('pair\tk4_restrict_to_triangle\trestrict\t6\t3\t4\t1\t1\t1\t3\t2\t6\t2\t'))
        self.assertEqual(len(m.public_tsv().splitlines()), len(m.CASES))


if __name__ == '__main__':
    unittest.main()
