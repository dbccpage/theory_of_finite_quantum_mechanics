"""Exact controls for the supplied-tag refinement / conflict-graph certificate (PFP batch 01, PG-REFINE-SEPARATES)."""
import importlib.util
import unittest
from itertools import product
from math import comb
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_refine_separates.py'
_SPEC = importlib.util.spec_from_file_location('pfp_refine_separates', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


def all_graphs(n):
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    for mask in range(1 << len(pairs)):
        yield [pairs[i] for i in range(len(pairs)) if mask >> i & 1]


def has_b_bit_tag(n, edges, b):
    """Literal definition: a tag is a map V -> {0,1}^b; proper means different tuples on every edge."""
    for tags in product(list(product((0, 1), repeat=b)), repeat=n):
        if all(tags[u] != tags[v] for u, v in edges):
            return True
    return False


class RefineSeparates(unittest.TestCase):
    def test_refinement_retains_old_report_and_tag_decides_collapsed_pairs(self):
        for o, t in ((2, 2), (3, 2), (2, 3)):
            for q in product(range(o), repeat=3):
                for g in product(range(t), repeat=3):
                    ref = [(q[a], g[a]) for a in range(3)]
                    self.assertEqual([r[0] for r in ref], list(q))
                    for a in range(3):
                        for b in range(3):
                            if q[a] == q[b]:
                                self.assertEqual(ref[a] != ref[b], g[a] != g[b])
                            else:
                                self.assertNotEqual(ref[a], ref[b])

    def test_labelled_bipartite_counts_match_the_known_sequence(self):
        self.assertEqual([m.enum_record(n)['bipartite'] for n in range(1, 6)], [1, 2, 7, 41, 376])

    def test_b_bit_tag_exists_iff_chromatic_number_at_most_two_to_the_b(self):
        for n in range(1, 5):
            for edges in all_graphs(n):
                chi = m.chromatic_number(n, edges)
                for b in range(3):
                    self.assertEqual(has_b_bit_tag(n, edges, b), chi <= 2 ** b, (n, edges, b))

    def test_min_bits_is_the_least_working_bit_count(self):
        for n in range(1, 5):
            for edges in all_graphs(n):
                least = next(b for b in range(4) if has_b_bit_tag(n, edges, b))
                self.assertEqual(m.min_bits(n, edges), least)

    def test_odd_cycle_blocks_one_bit_and_proper_tag_count_is_two_to_the_components(self):
        for n in range(1, 6):
            for edges in all_graphs(n):
                tags = m.one_bit_tags(n, edges)
                girth = m.odd_girth(n, edges)
                self.assertEqual(tags > 0, girth == 0)
                if tags:
                    self.assertEqual(tags, 2 ** m.components(n, edges))

    def test_triangle_five_cycle_and_k4_need_more_than_one_bit(self):
        rows = {r['name']: r for r in m.certificate()['records'] if r['kind'] == 'graph'}
        self.assertEqual((rows['triangle']['chi'], rows['triangle']['min_bits']), (3, 2))
        self.assertEqual((rows['cycle5']['chi'], rows['cycle5']['odd_girth'], rows['cycle5']['one_bit_tags']), (3, 5, 0))
        self.assertEqual((rows['k4']['chi'], rows['k4']['min_bits']), (4, 2))
        self.assertEqual((rows['k5']['chi'], rows['k5']['min_bits']), (5, 3))
        self.assertEqual((rows['petersen']['chi'], rows['petersen']['odd_girth']), (3, 5))
        self.assertEqual(rows['k33']['one_bit_tags'], 2)

    def test_fibre_bits_and_injective_tag_counts(self):
        for size in range(1, 6):
            row = m.fiber_record(size)
            self.assertEqual(row['min_bits'], (size - 1).bit_length())
            for b, count in enumerate(row['injective_tags_by_bits']):
                expect = 1
                for i in range(size):
                    expect *= max(2 ** b - i, 0)
                self.assertEqual(count, expect)
            self.assertEqual(row['injective_tags_by_bits'][row['min_bits']] > 0, True)
            if row['min_bits']:
                self.assertEqual(row['injective_tags_by_bits'][row['min_bits'] - 1], 0)

    def test_enumeration_colouring_pair_identity(self):
        for n in range(1, 6):
            row = m.enum_record(n)
            self.assertEqual(row['bipartite_colouring_pairs'], sum(comb(n, k) * 2 ** (k * (n - k)) for k in range(n + 1)))
            self.assertEqual(row['graphs'], 2 ** (n * (n - 1) // 2))
            self.assertEqual(sum(row['by_min_bits']), row['graphs'])
            self.assertEqual(row['bipartite'], row['by_min_bits'][0] + row['by_min_bits'][1])

    def test_refinement_counts_have_the_closed_form_and_the_iff_never_fails(self):
        for n, o, t in ((2, 2, 2), (3, 2, 2), (3, 3, 2), (3, 2, 3), (4, 2, 2)):
            row = m.refine_record(n, o, t)
            self.assertEqual(row['iff_failures'], 0)
            self.assertEqual(row['separated_by_tag'], n * (n - 1) * o ** (n - 1) * t ** (n - 1) * (t - 1))
            self.assertEqual(row['quadruples'], o ** n * t ** n * n * n)

    def test_wire_and_public_input_cover_every_case(self):
        data = m.certificate()
        self.assertEqual(len(m.wire_lines(data)), len(m.CASES))
        self.assertEqual(len(m.public_tsv().splitlines()), len(m.CASES))
        self.assertTrue(m.wire_lines(data)[4].startswith('graph\ttriangle\t3\t3\t1\t0\t0\t3\t2\t3\t'))
        self.assertTrue(all(line == line.strip() and '\t\t' not in line for line in m.wire_lines(data)))


if __name__ == '__main__':
    unittest.main()
