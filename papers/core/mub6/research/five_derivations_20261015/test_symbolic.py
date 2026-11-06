"""Focused negative controls for the symbolic derivation checker."""

import unittest

from verify_symbolic import three_bases, verify_pairing, verify_three_bases


class SymbolicControls(unittest.TestCase):
    def test_pairing_requires_bijection(self):
        terms = [(1, (0,))] * 3 + [(-1, (0,))] * 3
        with self.assertRaisesRegex(ValueError, "exactly once"):
            verify_pairing(terms, (3, 3, 3))

    def test_pairing_rejects_wrong_exponent(self):
        terms = [(1, (0,))] * 3 + [(-1, (0,)), (-1, (1,)), (-1, (0,))]
        with self.assertRaisesRegex(ValueError, "do not cancel"):
            verify_pairing(terms, (3, 4, 5))

    def test_pairing_rejects_wrong_sign(self):
        terms = [(1, (0,))] * 6
        with self.assertRaisesRegex(ValueError, "do not cancel"):
            verify_pairing(terms, (3, 4, 5))

    def test_three_basis_witness_rejects_entry_mutation(self):
        bases = three_bases()
        bases[2] = bases[2].as_mutable()
        bases[2][0, 0] += 1
        with self.assertRaisesRegex(ValueError, "unitary basis"):
            verify_three_bases(bases)

    def test_repeated_basis_fails_unbiasedness(self):
        bases = three_bases()
        bases[2] = bases[1]
        with self.assertRaisesRegex(ValueError, "unbiased bases"):
            verify_three_bases(bases)


if __name__ == "__main__":
    unittest.main()
