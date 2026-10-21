"""Finite-declared quotient-norm vs estate-wide refuse. AuthorityEffect: None."""

from __future__ import annotations

import unittest

from sympy import Matrix, Rational

from omega_engine.crates.functional.degree_k_phi import DegreeKPricingDeclaration
from omega_engine.crates.solver.solv_finite_quotient_norm import (
    QuotientNormError,
    estate_wide_quotient_norm_status,
    refuse_estate_wide_quotient_norm,
    refuse_normhood_from_attainment_alone,
    tetra_face_d1_for_phi2,
    triangle_d0,
    verify_finite_declared_quotient_norm,
)


class TestFiniteQuotientNorm(unittest.TestCase):
    def test_triangle_phi1_scoped_verified(self):
        d = triangle_d0()
        omega_exact = d * Matrix([Rational(0), Rational(2), Rational(5)])
        omega_cycle = Matrix([Rational(1), Rational(1), Rational(0)])
        r = verify_finite_declared_quotient_norm(
            d,
            [omega_exact, omega_cycle],
            DegreeKPricingDeclaration.exact_l1(1),
            degree=1,
        )
        self.assertEqual(r.scope, "FINITE_DECLARED")
        self.assertEqual(r.status, "COMPUTATIONALLY_VERIFIED_SCOPED")
        self.assertTrue(r.axioms.all_pass)
        self.assertEqual(r.estate_wide_status, "REFUSED")
        self.assertEqual(r.normhood_from_attainment_alone, "REFUSED")
        self.assertEqual(r.authority_effect, "None")
        self.assertEqual(r.phi_samples[0], "0")

    def test_phi2_fixture_scoped_verified(self):
        d, omega_pos, omega_exact = tetra_face_d1_for_phi2()
        r = verify_finite_declared_quotient_norm(
            d,
            [omega_pos, omega_exact],
            DegreeKPricingDeclaration.exact_l1(2),
            degree=2,
        )
        self.assertEqual(r.status, "COMPUTATIONALLY_VERIFIED_SCOPED")
        self.assertTrue(r.axioms.all_pass)
        self.assertNotEqual(r.phi_samples[0], "0")
        self.assertEqual(r.phi_samples[1], "0")

    def test_estate_wide_still_refused(self):
        st = estate_wide_quotient_norm_status()
        self.assertEqual(st["estate_wide_phi_k_theorem"], "REFUSED")
        self.assertEqual(st["normhood_from_attainment_alone"], "REFUSED")
        self.assertEqual(st["lean_mechanization"], "OPEN")
        with self.assertRaises(QuotientNormError) as ctx:
            refuse_estate_wide_quotient_norm(True)
        self.assertEqual(ctx.exception.code, "ESTATE_WIDE_QUOTIENT_NORM")
        with self.assertRaises(QuotientNormError) as ctx2:
            refuse_normhood_from_attainment_alone(True)
        self.assertEqual(ctx2.exception.code, "NORMHOOD_FROM_ATTAINMENT")

    def test_missing_declaration_refused(self):
        d = triangle_d0()
        with self.assertRaises(QuotientNormError):
            verify_finite_declared_quotient_norm(
                d,
                [Matrix([1, 0, 0])],
                DegreeKPricingDeclaration(
                    degree=1,
                    genuine_l1_norm=False,
                    index_agnostic_reachability=True,
                    reachability_declaration="x",
                ),
            )


if __name__ == "__main__":
    unittest.main()
