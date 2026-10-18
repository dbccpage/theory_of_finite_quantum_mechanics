"""Mutation controls for the RUR's soundness and separating-form checks."""

import tempfile
import unittest
from pathlib import Path

from flint import arb, fmpq, fmpz_poly
from replay_rur import check_jacobians, check_parametrization, exact_bounds


class RurControls(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.system = Path(self.directory.name) / "system.ms"
        self.system.write_text("x\n0\nx^2-1\n", encoding="utf-8")
        self.elim = fmpz_poly([-1, 0, 1])
        self.denominator = fmpz_poly([1])
        self.numerators = [(fmpz_poly([0, -1]), 1)]

    def replay(self, linear, numerators=None):
        return check_parametrization(
            self.system,
            ["x", "A"],
            linear,
            self.elim,
            self.denominator,
            self.numerators if numerators is None else numerators,
        )

    def test_separating_form_accepts_consistent_identity(self):
        result = self.replay([-1, 1])
        self.assertTrue(result["separating_form"])
        self.assertIn("requires", result["completeness"])

    def test_separating_form_rejects_sign_mutation(self):
        with self.assertRaisesRegex(ValueError, "Separating linear"):
            self.replay([1, 1])

    def test_substitution_rejects_coordinate_mutation(self):
        with self.assertRaisesRegex(ValueError, "substitution"):
            self.replay([-1, 1], [(fmpz_poly([0, -2]), 1)])

    def test_missing_coordinate_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "dimension"):
            self.replay([-1, 1], [])

    def test_repeated_eliminant_is_rejected(self):
        self.elim = self.elim**2
        with self.assertRaisesRegex(ValueError, "squarefree"):
            self.replay([-1, 1])

    def test_zero_denominator_at_a_root_is_rejected(self):
        self.denominator = fmpz_poly([-1, 1])
        with self.assertRaisesRegex(ValueError, "denominator"):
            self.replay([-1, 1])

    def test_serialized_bounds_enclose_non_dyadic_value(self):
        lower, upper = exact_bounds(arb(fmpq(1, 3)))
        self.assertLessEqual(lower, fmpq(1, 3))
        self.assertGreaterEqual(upper, fmpq(1, 3))

    def test_exact_jacobian_accepts_simple_roots(self):
        result = check_jacobians(
            self.system, [{"factor": 0}], [(self.elim, 1)], self.denominator, self.numerators
        )
        self.assertEqual(result["factors"][0]["gcd_degree"], 0)

    def test_exact_jacobian_rejects_singular_root(self):
        self.system.write_text("x\n0\nx^2\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Jacobian singular"):
            check_jacobians(
                self.system,
                [{"factor": 0}],
                [(fmpz_poly([0, 1]), 1)],
                self.denominator,
                [(fmpz_poly([0]), 1)],
            )


if __name__ == "__main__":
    unittest.main()
