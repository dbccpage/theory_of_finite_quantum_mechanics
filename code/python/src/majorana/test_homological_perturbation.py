r"""Unit tests for exact-Q Homological Perturbation Lemma (HPL) module.

Verifies:
1. ExactMatrix arithmetic delegated to canonical native rational kernels.
2. Side-condition verification of normalized contraction (i, r, h).
3. Exact perturbation transfer delta_D = r (1 + delta h)^-1 delta i, the sign
   for the convention 1_C - i r = d h + h d (WDP-CH16-C01).
4. Singular (1 + delta h) refusal with deformation receipt.
5. AuthorityEffect: None and evidence_sha256 digest on DeformationReceipt.
6. The transferred differential keeps the perturbed inclusion a chain map,
   and a transfer that breaks (d_D + delta_D)^2 = 0 is not a success.
"""

import unittest
from dataclasses import replace
from fractions import Fraction
from importlib import import_module

hpt = import_module(
    "omega_engine_atlas.coda_atlas.F004_papers.009_ms_majorana.code.homological_perturbation"
)
DifferentialPerturbation = hpt.DifferentialPerturbation
ExactMatrix = hpt.ExactMatrix
NormalizedContraction = hpt.NormalizedContraction
identity_contraction = hpt.identity_contraction
transfer_perturbation = hpt.transfer_perturbation
verify_normalized = hpt.verify_normalized


class TestHomologicalPerturbation(unittest.TestCase):
    def test_identity_contraction_zero_perturbation(self):
        """Test 1: identity contraction + zero perturbation."""
        dims = (1, 1, 0)
        d0 = ((0,),)
        d1: list = []
        contr = identity_contraction(dims, d0, d1)
        report = verify_normalized(contr)
        self.assertTrue(report.is_normalized, report.details)

        pert = DifferentialPerturbation.from_matrices(dims, ((0,),), [])
        receipt = transfer_perturbation(contr, pert)
        self.assertTrue(receipt.success)
        self.assertTrue(receipt.invertibility)
        self.assertEqual(receipt.authority_effect, "None")
        self.assertTrue(receipt.reduced_square_zero)
        self.assertIsNotNone(receipt.evidence_sha256)

    def test_identity_contraction_transfers_delta_unchanged(self):
        """Test 2: identity contraction transfers delta unchanged."""
        dims2 = (2, 1, 0)
        d0_2 = ((Fraction(1), Fraction(-1)),)
        d1_2: list = []
        contr2 = identity_contraction(dims2, d0_2, d1_2)
        self.assertTrue(verify_normalized(contr2).is_normalized)

        delta0 = ((Fraction(3), Fraction(-1)),)
        pert2 = DifferentialPerturbation.from_matrices(dims2, delta0, [])
        rec2 = transfer_perturbation(contr2, pert2)
        self.assertTrue(rec2.success)
        self.assertIsNotNone(rec2.delta_D0)
        self.assertEqual(rec2.delta_D0.data, delta0)
        self.assertTrue(rec2.reduced_square_zero)

    def test_singular_1_plus_delta_h_refuses(self):
        """Test 3: singular (1 + delta h) refuses transfer."""
        Cdims = (1, 1, 0)
        Ddims = (0, 0, 0)
        i0 = ExactMatrix.zero(1, 0).data
        i1 = ExactMatrix.zero(1, 0).data
        i2 = ExactMatrix.zero(0, 0).data
        r0 = ExactMatrix.zero(0, 1).data
        r1 = ExactMatrix.zero(0, 1).data
        r2 = ExactMatrix.zero(0, 0).data
        h1 = ((Fraction(1),),)
        h2 = ExactMatrix.zero(1, 0).data
        dC0 = ((Fraction(1),),)
        dC1 = ExactMatrix.zero(0, 1).data
        dD0 = ExactMatrix.zero(0, 0).data
        dD1 = ExactMatrix.zero(0, 0).data

        contr3 = NormalizedContraction.from_matrices(
            C_dims=Cdims,
            D_dims=Ddims,
            dC0=dC0,
            dC1=dC1,
            dD0=dD0,
            dD1=dD1,
            i0=i0,
            i1=i1,
            i2=i2,
            r0=r0,
            r1=r1,
            r2=r2,
            h1=h1,
            h2=h2,
        )
        self.assertTrue(verify_normalized(contr3).is_normalized)
        delta0_sing = ((Fraction(-1),),)
        pert3 = DifferentialPerturbation.from_matrices(Cdims, delta0_sing, [])
        rec3 = transfer_perturbation(contr3, pert3)
        self.assertFalse(rec3.success)
        self.assertFalse(rec3.invertibility)
        self.assertIn("singular", rec3.obstruction_reason or "")
        self.assertIsNone(rec3.reduced_square_zero)
        self.assertEqual(rec3.authority_effect, "None")

    def test_interval_to_point_contraction(self):
        """Test 4: non-trivial normalized contraction (interval -> point)."""
        Cdims4 = (2, 1, 0)
        Ddims4 = (1, 0, 0)
        dC0_4 = ((Fraction(-1), Fraction(1)),)
        dC1_4 = ExactMatrix.zero(0, 1).data
        dD0_4 = ExactMatrix.zero(0, 1).data
        dD1_4 = ExactMatrix.zero(0, 0).data
        i0_4 = ((Fraction(1, 2),), (Fraction(1, 2),))
        i1_4 = ExactMatrix.zero(1, 0).data
        i2_4 = ExactMatrix.zero(0, 0).data
        r0_4 = ((Fraction(1), Fraction(1)),)
        r1_4 = ExactMatrix.zero(0, 1).data
        r2_4 = ExactMatrix.zero(0, 0).data
        h1_4 = ((Fraction(-1, 2),), (Fraction(1, 2),))
        h2_4 = ExactMatrix.zero(1, 0).data

        contr4 = NormalizedContraction.from_matrices(
            C_dims=Cdims4,
            D_dims=Ddims4,
            dC0=dC0_4,
            dC1=dC1_4,
            dD0=dD0_4,
            dD1=dD1_4,
            i0=i0_4,
            i1=i1_4,
            i2=i2_4,
            r0=r0_4,
            r1=r1_4,
            r2=r2_4,
            h1=h1_4,
            h2=h2_4,
        )
        rep4 = verify_normalized(contr4)
        self.assertTrue(rep4.is_normalized, rep4.details)

        pert4 = DifferentialPerturbation.from_matrices(Cdims4, ExactMatrix.zero(1, 2).data, [])
        rec4 = transfer_perturbation(contr4, pert4)
        self.assertTrue(rec4.success)
        self.assertIsNotNone(rec4.delta_D0)
        self.assertTrue(rec4.delta_D0.is_zero())
        self.assertTrue(rec4.reduced_square_zero)

    def test_transfer_keeps_the_perturbed_inclusion_a_chain_map(self):
        """Test 5: the transferred differential has the sign this convention needs.

        C0 = <x, u>, C1 = <y, v>, C2 = 0 with d(u) = v; D0 = <x>, D1 = <y>, d_D = 0.
        i, r include and project x, y; h(v) = u, h(y) = 0. Perturb by
        delta(x) = a v + b y, delta(u) = c y. The lemma's perturbed inclusion is
        i'(x) = x - a u (computed by hand: h A i (x) = a u), and
        (d + delta)(x - a u) = (b - a c) y, so i' is a chain map exactly when
        delta_D(x) = (b - a c) y. The retired (1 - delta h)^-1 form gives
        (b + a c) y instead.
        """
        a, b, c = Fraction(1), Fraction(0), Fraction(1)
        contraction = NormalizedContraction.from_matrices(
            C_dims=(2, 2, 0),
            D_dims=(1, 1, 0),
            dC0=((0, 0), (0, 1)),
            dC1=ExactMatrix.zero(0, 2).data,
            dD0=((0,),),
            dD1=ExactMatrix.zero(0, 1).data,
            i0=((1,), (0,)),
            i1=((1,), (0,)),
            i2=ExactMatrix.zero(0, 0).data,
            r0=((1, 0),),
            r1=((1, 0),),
            r2=ExactMatrix.zero(0, 0).data,
            h1=((0, 0), (0, 1)),
            h2=ExactMatrix.zero(2, 0).data,
        )
        self.assertTrue(verify_normalized(contraction).is_normalized)
        delta0 = ((b, c), (a, 0))
        receipt = transfer_perturbation(
            contraction,
            DifferentialPerturbation.from_matrices((2, 2, 0), delta0, ExactMatrix.zero(0, 2).data),
        )
        self.assertTrue(receipt.success)
        self.assertEqual(receipt.delta_D0.data, ((b - a * c,),))

        i_prime_x = ExactMatrix.from_rows(
            ((1,), (-a,)), expected_rows=2, expected_cols=1, label="i'x"
        )
        d_plus_delta = contraction.dC0 + ExactMatrix.from_rows(
            delta0, expected_rows=2, expected_cols=2, label="delta0"
        )
        lhs = d_plus_delta.matmul(i_prime_x)
        rhs = contraction.i1.matmul(receipt.delta_D0)
        self.assertEqual(lhs.data, rhs.data)

    def test_non_square_zero_source_perturbation_is_always_refused(self):
        """The retained optional flag cannot disable the native square-zero law."""
        contraction = identity_contraction((1, 1, 1), ((0,),), ((0,),))
        perturbation = DifferentialPerturbation.from_matrices((1, 1, 1), ((1,),), ((1,),))
        receipt = transfer_perturbation(
            contraction, perturbation, check_perturbed_square_zero=False
        )
        self.assertIsNone(receipt.reduced_square_zero)
        self.assertFalse(receipt.success)
        self.assertEqual(receipt.obstruction_reason, "perturbed_differential_not_square_zero")
        self.assertEqual(receipt.authority_effect, "None")

    def test_legacy_flag_cannot_bypass_normalized_contraction_laws(self):
        contraction = identity_contraction((1, 1, 0), ((0,),), [])
        invalid = replace(contraction, h1=ExactMatrix.from_rows(((1,),)))
        self.assertFalse(verify_normalized(invalid).is_normalized)
        perturbation = DifferentialPerturbation.from_matrices((1, 1, 0), ((0,),), [])
        receipt = transfer_perturbation(invalid, perturbation, require_normalized=False)
        self.assertFalse(receipt.success)
        self.assertFalse(receipt.invertibility)
        self.assertEqual(
            receipt.obstruction_reason, "normalized_contraction_side_conditions_failed"
        )
        self.assertFalse(receipt.side_conditions.is_normalized)
        self.assertIsNone(receipt.delta_D0)

    def test_chain_maps_are_checked_in_addition_to_legacy_side_conditions(self):
        contraction = identity_contraction((1, 1, 0), ((0,),), [])
        invalid = replace(contraction, dD0=ExactMatrix.from_rows(((1,),)))
        report = verify_normalized(invalid)
        self.assertTrue(
            report.ri_equals_id_D
            and report.sdr_equation
            and report.hi_zero
            and report.rh_zero
            and report.hh_zero
        )
        self.assertFalse(report.inclusion_chain_map)
        self.assertFalse(report.retraction_chain_map)
        self.assertFalse(report.is_normalized)


if __name__ == "__main__":
    unittest.main()
