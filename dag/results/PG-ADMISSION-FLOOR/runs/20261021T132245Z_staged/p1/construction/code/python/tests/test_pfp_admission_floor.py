"""Exact controls for the admission floor certificate (PFP batch 01, PG-ADMISSION-FLOOR)."""
import importlib.util
import unittest
from itertools import product
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_admission_floor.py'
_SPEC = importlib.util.spec_from_file_location('pfp_admission_floor', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


class AdmissionFloor(unittest.TestCase):
    def test_no_cut_on_a_subsingleton(self):
        for n in (0, 1):
            r = m.classify(n)
            self.assertEqual((r['cut_relations'], r['cut_triples']), (0, 0))
        self.assertGreater(m.classify(2)['cut_relations'], 0)

    def test_endpoints_are_apart_under_the_law(self):
        for n in range(0, 5):
            self.assertEqual(m.classify(n)['irreflexive_related_equal'], 0)

    def test_pointed_relation_independence_quadrants(self):
        r1, r2 = m.classify(1), m.classify(2)
        self.assertGreater(r1['related_equal'], 0)       # relatedness does not give distinctness
        self.assertGreater(r2['unrelated_distinct'], 0)  # distinctness does not give relatedness
        self.assertEqual(r1['related_distinct'], 0)

    def test_instance_and_law_are_independent_on_one_point(self):
        r = m.classify(1)
        self.assertEqual((r['instance_without_law'], r['law_without_instance'], r['cut_relations']), (1, 1, 0))

    def test_law_is_not_derived_from_distinctness_on_larger_carriers(self):
        for n in (2, 3, 4):
            r = m.classify(n)
            self.assertGreater(r['instance_without_law'], 0)
            self.assertEqual(r['law_without_instance'], 1)
            self.assertEqual(r['law_bearing'] - 1, r['cut_relations'])

    def test_identification_breaks_the_law_and_its_converse_on_small_carriers(self):
        for n in (1, 2, 3):
            r = m.identify(n)
            self.assertEqual(r['rq_overlap'], 0)
            self.assertEqual(r['cut_q_identified_with_target'], 0)
            self.assertEqual(r['rq_with_target'] + r['rq_identifying'], r['rq_pairs'])

    def test_brute_force_target_existence_equals_separation_of_related_pairs(self):
        # independent re-derivation of exists_law_target_iff on Fin 2 with arbitrary (not only irreflexive) targets
        n = 2
        for R in range(1 << (n * n)):
            if any((R >> (i * n + i)) & 1 for i in range(n)):
                continue
            related = [(a, b) for a in range(n) for b in range(n) if (R >> (a * n + b)) & 1]
            for q in product(range(n), repeat=n):
                has_target = any(
                    all((T >> (q[a] * n + q[b])) & 1 for a, b in related) and not any((T >> (i * n + i)) & 1 for i in range(n))
                    for T in range(1 << (n * n)))
                self.assertEqual(has_target, all(q[a] != q[b] for a, b in related))

    def test_counts_match_closed_forms(self):
        for n in range(0, 5):
            r = m.classify(n)
            self.assertEqual(r['relations'], 2 ** (n * n))
            self.assertEqual(r['law_bearing'], 2 ** (n * n - n))
        self.assertEqual(m.classify(2)['cut_triples'], 4)
        self.assertEqual(m.classify(3)['cut_triples'], 192)

    def test_wire_format_has_one_line_per_case(self):
        lines = m.wire_lines(m.certificate())
        self.assertEqual(len(lines), len(m.CASES))
        self.assertEqual(lines[2], 'classify\t2\t16\t4\t3\t4\t12\t1\t16\t16\t16\t16\t0')
        self.assertEqual(lines[6], 'identify\t2\t16\t10\t6\t0\t16\t8\t8\t0')


if __name__ == '__main__':
    unittest.main()
