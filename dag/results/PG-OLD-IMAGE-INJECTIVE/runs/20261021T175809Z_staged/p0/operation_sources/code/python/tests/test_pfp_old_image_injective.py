"""Exact controls for the old-image injectivity census (PFP batch 01, PG-OLD-IMAGE-INJECTIVE)."""
import importlib.util
import itertools
import unittest
from math import perm
from pathlib import Path

_SOURCE = Path(__file__).resolve().parents[1] / 'src/qm/pfp_old_image_injective.py'
_SPEC = importlib.util.spec_from_file_location('pfp_old_image_injective', _SOURCE)
m = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(m)


def law_pairs(a, b):
    """All (u, r) with r(u(x)) = x, written as dicts; r values in range(a + 1), a meaning refusal."""
    out = []
    for u in itertools.product(range(b), repeat=a):
        for r in itertools.product(range(a + 1), repeat=b):
            if all(r[u[x]] == x for x in range(a)):
                out.append((u, r))
    return out


class OldImageInjective(unittest.TestCase):
    def test_law_implies_injective_on_a_range(self):
        for a in range(0, 4):
            for b in range(0, 5):
                for u, r in law_pairs(a, b):
                    self.assertEqual(len(set(u)), a, (a, b, u, r))

    def test_no_law_pair_when_source_larger(self):
        for a in range(1, 4):
            for b in range(0, a):
                self.assertEqual(law_pairs(a, b), [])

    def test_injective_iff_some_recovery_exists(self):
        for a in range(0, 4):
            for b in range(0, 5):
                with_law = {u for u, _ in law_pairs(a, b)}
                injective = {u for u in itertools.product(range(b), repeat=a) if len(set(u)) == a}
                self.assertEqual(with_law, injective)

    def test_count_matches_falling_factorial_times_free_values(self):
        for a in range(0, 4):
            for b in range(0, 5):
                want = perm(b, a) * (a + 1) ** (b - a) if a <= b else 0
                self.assertEqual(len(law_pairs(a, b)), want)
                self.assertEqual(m.record(a, b, 2)['law'], want)

    def test_off_image_rejection_is_not_implied_but_possible(self):
        for a, b in [(1, 2), (2, 3), (3, 4)]:
            rec = m.record(a, b, 2)
            self.assertGreater(rec['law_nonrefusing'], 0)
            self.assertEqual(rec['law_refusing'], rec['injective_u'])
        # surjective lifts have nothing off the image: every law pair refuses vacuously
        for a in range(0, 4):
            rec = m.record(a, a, 2)
            self.assertEqual(rec['law_nonrefusing'], 0)

    def test_source_instance_is_one_of_the_nonrefusing_pairs(self):
        # u : Fin 1 -> Fin 2 constant 0 and r constant inl 0 (refusal index is 1 here)
        u, r = (0,), (0, 0)
        self.assertEqual(r[u[0]], 0)
        self.assertNotEqual(r[1], 1)
        self.assertIn((u, r), law_pairs(1, 2))

    def test_observations_and_obstructions_are_unconstrained(self):
        rec = m.record(2, 2, 2)
        self.assertEqual((rec['obs_preserved'], rec['obs_total']), (8, 32))
        self.assertEqual((rec['persists'], rec['cleared']), (14, 10))
        self.assertTrue(0 < rec['persists'] and 0 < rec['cleared'])

    def test_degenerate_empty_source(self):
        rec = m.record(0, 3, 2)
        self.assertEqual((rec['law'], rec['law_refusing'], rec['injective_u']), (1, 1, 1))
        self.assertEqual((rec['persists'], rec['cleared']), (0, 0))

    def test_wire_format(self):
        lines = m.wire_lines(m.certificate())
        self.assertEqual(len(lines), len(m.CASES))
        self.assertEqual(lines[5], 'lift\t2\t3\t2\t243\t18\t0\t6\t12\t6\t576\t144\t252\t180')
        self.assertEqual(m.public_tsv().count('\n'), len(m.CASES))


if __name__ == '__main__':
    unittest.main()
