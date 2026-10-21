"""Exact controls for the root coproduct certificate (PFP batch 01, PG-ROOT-DIFF-STRUCTURE, an admitted primitive)."""
import importlib.util
import unittest
from itertools import product
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_root_diff_structure.py'
_SPEC = importlib.util.spec_from_file_location('pfp_root_diff_structure', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


class RootDiffStructure(unittest.TestCase):
    def test_universal_property_every_pair_of_maps_has_exactly_one_extension(self):
        # Maps are dictionaries on tagged elements, independent of the producer's positional encoding.
        for a in range(4):
            for b in range(4):
                for c in range(4):
                    left_dom = [('pd', i) for i in range(a)]
                    right_dom = [('st', j) for j in range(b)]
                    cop = left_dom + right_dom
                    extensions = {}
                    for values in product(range(c), repeat=len(cop)):
                        h = dict(zip(cop, values))
                        key = (tuple(sorted((k, h[k]) for k in left_dom)), tuple(sorted((k, h[k]) for k in right_dom)))
                        extensions[key] = extensions.get(key, 0) + 1
                    self.assertEqual(len(extensions), c ** a * c ** b)
                    self.assertTrue(all(v == 1 for v in extensions.values()))

    def test_count_of_maps_out_is_the_product_for_all_tabulated_sizes(self):
        for r in m.certificate()['records']:
            if r['kind'] == 'maps':
                self.assertEqual(r['total_maps'], r['c'] ** (r['a'] + r['b']))
                self.assertEqual(r['total_maps'], r['left_maps'] * r['right_maps'])
                self.assertEqual(r['unique_copairs'], r['left_maps'] * r['right_maps'])
                self.assertTrue(r['inl_injective'] and r['inr_injective'] and r['disjoint'] and r['covering'])

    def test_retraction_exists_iff_target_nonempty_or_other_empty(self):
        for a in range(4):
            for b in range(4):
                r = m.reduction_record(a, b)
                self.assertEqual(r['exists_to_pd'], a > 0 or b == 0)
                self.assertEqual(r['exists_to_s'], b > 0 or a == 0)
                self.assertEqual(r['retractions_to_pd'], a ** b)
                self.assertEqual(r['retractions_to_s'], b ** a)

    def test_empty_channel_facing_a_nonempty_one_has_no_reduction(self):
        r = m.reduction_record(0, 2)
        self.assertEqual((r['exists_to_pd'], r['exists_to_s']), (False, True))
        r = m.reduction_record(3, 0)
        self.assertEqual((r['exists_to_pd'], r['exists_to_s']), (True, False))

    def test_reductions_when_they_exist_are_a_choice_not_unique(self):
        self.assertEqual(m.reduction_record(2, 2)['retractions_to_pd'], 4)
        self.assertEqual(m.reduction_record(2, 3)['retractions_to_pd'], 8)
        self.assertEqual(m.reduction_record(1, 3)['retractions_to_pd'], 1)

    def test_posits_are_independent_and_the_construction_yields_no_element_by_itself(self):
        rows = {(r['a'], r['b']): r for r in m.certificate()['records'] if r['kind'] == 'posit'}
        self.assertEqual(set(rows), {(0, 0), (0, 1), (1, 0), (1, 1)})
        self.assertEqual({(r['nonempty_pd'], r['nonempty_s']) for r in rows.values()}, {(False, False), (False, True), (True, False), (True, True)})
        self.assertFalse(rows[(0, 0)]['nonempty_real0'])
        self.assertTrue(all(r['real0_nonempty_iff_a_channel_is'] for r in rows.values()))

    def test_coproduct_size_is_the_sum_and_not_the_max(self):
        self.assertEqual(m.posit_record(1, 1)['coproduct_size'], 2)
        self.assertEqual(len(m.coproduct(3, 2)), 5)

    def test_wire_and_public_input_cover_every_case(self):
        data = m.certificate()
        self.assertEqual(len(m.wire_lines(data)), len(m.CASES))
        self.assertEqual(len(m.public_tsv().splitlines()), len(m.CASES))
        self.assertTrue(m.wire_lines(data)[0].startswith('maps\t0\t0\t0\t1\t1\t1\t1\t1\t1\t1\t1\t1'))
        self.assertTrue(all(line == line.strip() and '\t\t' not in line for line in m.wire_lines(data)))


if __name__ == '__main__':
    unittest.main()
