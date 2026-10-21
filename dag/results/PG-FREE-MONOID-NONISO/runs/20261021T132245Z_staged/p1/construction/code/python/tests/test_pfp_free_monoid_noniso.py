"""Exact controls for the free-monoid non-isomorphism certificate (PFP batch 01, PG-FREE-MONOID-NONISO)."""
import importlib.util
import unittest
from itertools import permutations, product
from math import factorial
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_free_monoid_noniso.py'
_SPEC = importlib.util.spec_from_file_location('pfp_free_monoid_noniso', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


class FreeMonoidNoniso(unittest.TestCase):
    def test_atoms_are_exactly_the_letters(self):
        for n in range(0, 5):
            self.assertEqual(m.atoms(n, 4), n)

    def test_bijective_candidates_are_the_letter_permutations_on_a_range(self):
        for n in range(0, 4):
            for k in range(0, 4):
                r = m.record(n, k, 2)
                self.assertEqual(r['bijective_not_permutation'], 0, (n, k))
                self.assertEqual(r['bijective_candidates'], factorial(n) if n == k else 0, (n, k))
                self.assertEqual(r['discrete_equivalences'], factorial(n) if n == k else 0, (n, k))

    def test_homomorphism_count_and_onto_count_closed_forms(self):
        for n in range(0, 4):
            for k in range(0, 4):
                r = m.record(n, k, 1)
                self.assertEqual(r['homs'], (1 + k) ** n)
                # onto the letters with images of length <= 1: every letter is the image of some generator
                self.assertEqual(r['letters_onto'], sum(1 for t in product(range(k + 1), repeat=n) if set(range(k)) <= set(t)))

    def test_equal_sizes_have_exactly_the_permutation_isomorphisms(self):
        # direct check that each permutation of letters is an isomorphism on words of length <= 3
        n = 3
        for perm in permutations(range(n)):
            images = [(perm[i],) for i in range(n)]
            words = m.words_upto(n, 3)
            values = [m.hom_image(images, w) for w in words]
            self.assertEqual(len(set(values)), len(words))
            self.assertEqual(set(values), set(words))

    def test_shortlex_rank_roundtrip_and_non_multiplicativity(self):
        for base in range(1, 5):
            for r in range(0, 200):
                self.assertEqual(m.rank(m.unrank(r, base), base), r)
        for n, k in [(1, 2), (2, 3), (3, 2), (2, 4)]:
            flag, violations = m.set_bijection(n, k)
            self.assertEqual(flag, 1)
            self.assertGreater(violations, 0)
        for n in range(1, 5):
            self.assertEqual(m.set_bijection(n, n), (1, 0))
        self.assertEqual(m.set_bijection(0, 1), (0, 0))

    def test_unequal_sizes_have_no_bijective_homomorphism_even_with_longer_images(self):
        # d = 2 for sizes up to 3: no hom is both onto the letters and injective on words of length <= 2
        for n, k in [(1, 2), (2, 1), (2, 3), (3, 2), (0, 1), (1, 0)]:
            self.assertEqual(m.record(n, k, 2)['bijective_candidates'], 0, (n, k))

    def test_wire_format(self):
        lines = m.wire_lines(m.certificate())
        self.assertEqual(len(lines), len(m.CASES))
        self.assertTrue(lines[6].startswith('monoid\t2\t2\t2\t1:2:4:8:16\t1:2:4:8:16\t2\t2\t49\t2\t26\t2\t0\t2\t2\t1\t0'))
        self.assertTrue(all(line == line.strip() and '\t\t' not in line for line in lines))


if __name__ == '__main__':
    unittest.main()
