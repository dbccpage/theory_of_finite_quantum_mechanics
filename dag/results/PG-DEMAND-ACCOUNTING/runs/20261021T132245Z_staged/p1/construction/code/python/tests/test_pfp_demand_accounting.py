"""Exact controls for the demand-accounting certificate (PFP batch 01, PG-DEMAND-ACCOUNTING)."""
import importlib.util
import itertools
import unittest
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_demand_accounting.py'
_SPEC = importlib.util.spec_from_file_location('pfp_demand_accounting', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


def subsets(universe):
    items = list(universe)
    for r in range(len(items) + 1):
        for c in itertools.combinations(items, r):
            yield frozenset(c)


class DemandAccounting(unittest.TestCase):
    def test_identity_under_both_hypotheses_with_python_sets(self):
        for u in range(0, 4):
            for W in subsets(range(u)):
                for D in subsets(range(u)):
                    for B in subsets(range(u)):
                        nxt = (W - D) | B
                        if D <= W and not ((W - D) & B):
                            self.assertEqual(len(nxt), len(W) - len(D) + len(B))

    def test_integer_identity_iff_excess_equals_overlap(self):
        # the exact characterisation proved in Lean as formula_iff, checked by set arithmetic
        for u in range(0, 4):
            for W in subsets(range(u)):
                for D in subsets(range(u)):
                    for B in subsets(range(u)):
                        nxt = (W - D) | B
                        holds = len(nxt) == len(W) - len(D) + len(B)
                        self.assertEqual(holds, len(D - W) == len((W - D) & B))

    def test_class_sizes_match_closed_forms(self):
        for u in range(0, 6):
            r = m.demand_record(u)
            n = [c[0] for c in r['classes']]
            self.assertEqual(n[0], 5 ** u)
            self.assertEqual(n[1], 7 ** u - 5 ** u)
            self.assertEqual(n[2], 6 ** u - 5 ** u)
            self.assertEqual(n[3], 8 ** u - 7 ** u - 6 ** u + 5 ** u)
            self.assertEqual(sum(n), 8 ** u)

    def test_single_violation_never_satisfies_integer_identity(self):
        for u in range(0, 6):
            r = m.demand_record(u)
            self.assertEqual(r['classes'][0][1], r['classes'][0][0])
            self.assertEqual(r['classes'][1][1], 0)
            self.assertEqual(r['classes'][2][1], 0)

    def test_accidental_agreement_exists_and_truncation_masks_violations(self):
        r = m.demand_record(2)
        self.assertEqual(r['classes'][3], [4, 4, 4])
        r3 = m.demand_record(3)
        self.assertEqual(r3['classes'][1], [218, 0, 152])

    def test_kernel_counterexamples_as_python_sets(self):
        W, D, B = {0}, {1}, set()
        self.assertEqual((len((W - D) | B), len(W) - len(D) + len(B)), (1, 0))
        W, D, B = {0, 1}, {0}, {1}
        self.assertEqual((len((W - D) | B), len(W) - len(D) + len(B)), (1, 2))
        W, D, B = {0}, {0, 1}, set()
        self.assertEqual(len((W - D) | B), max(0, len(W) - len(D)) + len(B))
        self.assertNotEqual(len((W - D) | B), len(W) - len(D) + len(B))

    def test_every_step_realized_by_the_explicit_construction(self):
        for s in range(0, 7):
            for t in range(0, 7):
                w, d, b = set(range(s)), set(range(t, s)), set(range(s, t))
                self.assertTrue(d <= w and not ((w - d) & b))
                self.assertEqual((len(w), len((w - d) | b)), (s, t))

    def test_split_counts_match_enumeration_of_all_admissible_splits(self):
        for s in range(0, 5):
            for t in range(0, 5):
                splits = {(len(D), len(B)) for W in [frozenset(range(s))] for D in subsets(W)
                          for B in subsets(range(s + t)) if not ((W - D) & B) and len((W - D) | B) == t}
                self.assertEqual(m.decomposition_count(s, t), len(splits))

    def test_declared_sequence_is_underdetermined(self):
        r = m.sequence_record([0, 1, 1, 1, 0, 1, 1])
        self.assertEqual(r['decompositions'], [1, 2, 2, 1, 1, 2])
        self.assertTrue(r['underdetermined'])
        self.assertFalse(m.sequence_record([0, 5, 0, 2])['underdetermined'])

    def test_single_violation_never_satisfies_identity_with_python_sets(self):
        for u in range(0, 4):
            for W in subsets(range(u)):
                for D in subsets(range(u)):
                    for B in subsets(range(u)):
                        sub_ok = D <= W
                        disj = not ((W - D) & B)
                        holds = len((W - D) | B) == len(W) - len(D) + len(B)
                        if sub_ok != disj:
                            self.assertFalse(holds)

    def test_births_may_coincide_with_discharged_elements(self):
        W, D, B = {0, 1}, {0}, {0}
        self.assertTrue(D <= W and not ((W - D) & B))
        self.assertEqual(len((W - D) | B), len(W) - len(D) + len(B))

    def test_list_register_length_identity_and_nodup_iff_disjoint(self):
        for a, L in [(1, 2), (2, 2), (3, 2)]:
            r = m.listreg_record(a, L)
            self.assertEqual(r['identity_holds'], r['total'])
            self.assertEqual(r['nodup_when_overlap'], 0)
            self.assertEqual(r['nodup_when_disjoint'], r['disjoint_inputs'])
        self.assertLess(m.listreg_record(2, 2)['disjoint_inputs'], m.listreg_record(2, 2)['nodup_inputs'])

    def test_wire_format(self):
        lines = m.wire_lines(m.certificate())
        self.assertEqual(len(lines), len(m.CASES))
        self.assertEqual(lines[0], 'demand\t0\t1\t1:1:1\t0:0:0\t0:0:0\t0:0:0')
        self.assertTrue(lines[6].startswith('sequence\t0,1,1,1,0,1,1\t1,2,2,1,1,2\t1'))
        self.assertEqual(lines[10], 'listreg\t2\t2\t196\t196\t100\t68\t68\t0')
        self.assertEqual(m.public_tsv().count('\n'), len(m.CASES))


if __name__ == '__main__':
    unittest.main()
