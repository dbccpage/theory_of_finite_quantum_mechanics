
import unittest

from omega_engine.crates.majorana.engines.exact_algebraic_verifier import (
    verify_ising_braid_relation,
    verify_fusion_associativity,
    verify_ising_sigma_hexagon_specialization,
    Cyclotomic16,
    SQRT2,
    I_IMAG,
)


class TestExactAlgebraicVerifier(unittest.TestCase):
    def test_exact_algebraic_identities(self):
        self.assertEqual(SQRT2 * SQRT2, Cyclotomic16([2, 0, 0, 0, 0, 0, 0, 0]))
        self.assertEqual(I_IMAG * I_IMAG, Cyclotomic16([-1, 0, 0, 0, 0, 0, 0, 0]))

        self.assertTrue(verify_ising_braid_relation())

        self.assertTrue(verify_fusion_associativity())

        self.assertTrue(verify_ising_sigma_hexagon_specialization())

    def test_float_rejection(self):
        with self.assertRaises(TypeError):
            Cyclotomic16([1.0, 0, 0, 0, 0, 0, 0, 0])


if __name__ == "__main__":
    unittest.main()



