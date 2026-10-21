"""Exact controls for the primitive-difference axioms certificate (PFP batch 01, PG-PRIMDIFF-AXIOMS)."""
import importlib.util
import unittest
from itertools import product
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_primdiff_axioms.py'
_SPEC = importlib.util.spec_from_file_location('pfp_primdiff_axioms', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


class PrimdiffAxioms(unittest.TestCase):
    def test_a5_matrix_product_agrees_with_the_face_rule_for_every_edge_set(self):
        for mask in range(512):
            edges = m.relation(3, mask)
            present = sum(1 for e in ((0, 1), (1, 2), (0, 2)) if e in edges)
            self.assertEqual(m.a5_holds(3, edges, [(0, 1, 2)]), present in (0, 3), edges)
            self.assertEqual(m.a7_holds(3, edges, [(0, 1, 2)]), present in (0, 3), edges)

    def test_block_histogram_counts_equal_full_enumeration_on_one_and_two_points(self):
        for n in (1, 2):
            full = {}
            for d, e, alpha in product(range(1 << (n * n)), range(1 << (n * n)), (True, False)):
                edges = m.relation(n, e)
                key = (m.a1_holds(m.relation(n, d)), True, m.a4_holds(edges), m.a5_holds(n, edges, []), m.a7_holds(n, edges, []), alpha,
                       m.well_formed(edges, []))
                full[key] = full.get(key, 0) + 1
            self.assertEqual(full, m.joint(n))

    def test_model_counts_and_independence(self):
        rows = {r['n']: r for r in (m.models_record(n) for n in (1, 2, 3))}
        self.assertEqual([rows[n]['total'] for n in (1, 2, 3)], [8, 512, 1048576])
        self.assertEqual([rows[n]['all_hold'] for n in (1, 2, 3)], [1, 12, 2304])
        self.assertEqual(rows[3]['violate_only'], [16128, 0, 38656, 0, 0, 2304])
        self.assertEqual([rows[n]['violate_a5_a7_jointly'] for n in (1, 2, 3)], [0, 0, 1152])
        self.assertTrue(all(rows[n]['a5_equals_a7'] for n in rows))
        self.assertEqual(rows[3]['a5_without_well_formed'], 65536)

    def test_single_axiom_counts_follow_closed_forms(self):
        for n in (1, 2, 3):
            expect = 2 ** (n * n - n) * 2 ** (n * n) * (2 if n == 3 else 1) * 2
            self.assertEqual(m.axiom_record(1)['models_by_n'][n - 1], expect)
        self.assertEqual(m.axiom_record(4)['models_by_n'], [4, 96, 55296])
        self.assertEqual(m.axiom_record(5)['models_by_n'], m.axiom_record(7)['models_by_n'])
        self.assertEqual(m.axiom_record(3)['models_by_n'], [8, 512, 1048576])

    def test_every_off_diagonal_pair_lies_in_exactly_half_of_the_models(self):
        for n in (2, 3):
            r = m.unentailed_record(n)
            self.assertEqual(r['with_each_offdiag_pair'] * 2, r['models'])
            self.assertEqual(r['diagonal_pairs_in_a_model'], 0)

    def test_kernel_enforces_a1_then_carrier_and_never_inspects_the_token(self):
        carrier, store = {0, 1, 2}, []
        self.assertEqual(m.kernel_admit(carrier, store, 0, 1, 7), 'ok')
        self.assertEqual(m.kernel_admit(carrier, store, 0, 1, 7), 'ok')
        self.assertEqual(m.kernel_admit(carrier, store, 1, 0, 0), 'ok')
        self.assertEqual(m.kernel_admit(carrier, store, 1, 1, 0), 'a1')
        self.assertEqual(m.kernel_admit(carrier, store, 5, 5, 0), 'a1')
        self.assertEqual(m.kernel_admit(carrier, store, 0, 5, 0), 'carrier')
        self.assertEqual(len(store), 3)
        for tok in range(4):
            self.assertEqual([m.kernel_admit(carrier, [], a, b, tok) for a in range(4) for b in range(4)],
                             [m.kernel_admit(carrier, [], a, b, 0) for a in range(4) for b in range(4)])

    def test_number_of_preorders_on_four_points_is_355(self):
        seen = set()
        for mask in range(1 << 16):
            edges = m.relation(4, mask)
            seen.add(tuple(tuple(r) for r in m.closure(4, edges)))
        self.assertEqual(len(seen), 355)
        self.assertEqual([m.closure_record(n)['distinct_closures'] for n in (1, 2, 3)], [1, 4, 29])

    def test_triad_tables_match_hand_computation_and_the_source_values(self):
        self.assertEqual(m.phi1(3, [(0, 1), (1, 2), (0, 2)], (1, 1, 0)), 2)  # source test: open triangle, h = (1, 1, 0), Phi1 = 2
        self.assertEqual(m.phi1(3, [(0, 1), (1, 2), (0, 2)], (0, 0, 0)), 0)
        filled = m.triad_record('filled_triangle', 3, '0-1,1-2,0-2', '0-1-2')
        self.assertEqual((filled['exact'], filled['closed_nonexact'], filled['rupture'], filled['exact_nonclosed']), (7, 0, 20, 0))
        opened = m.triad_record('open_triangle', 3, '0-1,1-2,0-2', '-')
        self.assertEqual((opened['exact'], opened['closed_nonexact'], opened['rupture']), (7, 20, 0))
        broken = m.triad_record('broken_face', 3, '0-1,1-2', '0-1-2')
        self.assertEqual((broken['exact'], broken['exact_nonclosed'], broken['rcl_refusals'], broken['nilpotent']), (3, 6, 6, False))

    def test_gauge_and_relabelling_invariance_hold_on_every_named_complex_and_refusals_need_a_non_nilpotent_complex(self):
        for name, (n, e, f) in m.COMPLEXES.items():
            r = m.triad_record(name, n, e, f)
            self.assertTrue(r['gauge_invariant'] and r['relabel_invariant'], name)
            self.assertEqual(r['rcl_refusals'] > 0, not r['nilpotent'], name)

    def test_wire_and_public_input_cover_every_case(self):
        data = m.certificate()
        self.assertEqual(len(m.wire_lines(data)), len(m.CASES))
        self.assertEqual(len(m.public_tsv().splitlines()), len(m.CASES))
        self.assertTrue(m.wire_lines(data)[0].startswith('axiom\t1\tA01NonIdentification\tstate_predicate\t4\t128\t131072'))
        self.assertTrue(all(line == line.strip() and '\t\t' not in line for line in m.wire_lines(data)))


if __name__ == '__main__':
    unittest.main()
