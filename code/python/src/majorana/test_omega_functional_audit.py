from __future__ import annotations
"""Comprehensive 20 P0 & P1 audit tests for omega_functional.

Verifies scalar discipline, fail-closed boundaries, negative bounds checks,
sector probability validation, and structural mirror fail-closed posture.
"""


import math
import unittest
import numpy as np

from omega_engine.crates.functional.aggregation import AggregationMonotonicity
from omega_engine.crates.functional.born_probabilities import born_rule, l1_probability
from omega_engine.crates.functional.density_from_h1 import (
    incidence_sector_decomposition,
    density_from_sectors_diagonal,
    density_from_sectors_with_phase,
    H1Sector,
    H1SectorDecomposition,
    SectorMassCertificate,
    PhaseWitness,
    PhaseWitnessKind,
)
from omega_engine.crates.functional.density_lift import compute_xi, rho_l1
from omega_engine.crates.functional.l1_norm import compute_l1_norm
from omega_engine.crates.functional.l1_seminorm import EdgeCochain
from omega_engine.crates.functional.cohomology_norms import compute_l2_norm, norm_gap
from omega_engine.crates.functional.gamma2 import gamma2, verify_exactness, cycle_coboundary
from omega_engine.crates.functional.dual_verification import verify_dual_witness, accept

from omega_engine.crates.functional.closure_defect import (
    try_from_verified as closure_defect_try_from_verified,
)
from omega_engine.crates.functional.closure_regime import (
    from_certified as closure_regime_from_certified,
)
from omega_engine.crates.functional.contract_descriptors import contract_by_id
from omega_engine.crates.functional.evaluation_hierarchy import guarded_strictly_improves
from omega_engine.crates.functional.exact_repair import new as exact_repair_new
from omega_engine.crates.functional.hashes import try_new as hashes_try_new
from omega_engine.crates.functional.dual_witness import from_verified as dual_witness_from_verified


class TestOmegaFunctionalAudit(unittest.TestCase):
    def test_aggregation_2d_odd_grid_refuses_or_ledgers_loss(self):
        grid = np.ones((3, 3))
        with self.assertRaises(ValueError) as ctx:
            AggregationMonotonicity.coarse_grain_2d(grid, block_size=2)
        self.assertIn("COARSE_GRID_LEFTOVER_REFUSED", str(ctx.exception))

    def test_aggregation_1d_requires_divisible_block_size(self):
        with self.assertRaises(ValueError):
            AggregationMonotonicity.coarse_grain_1d([1.0] * 5, [(0, 1)], block_size=2)
        with self.assertRaises(ValueError):
            AggregationMonotonicity.coarse_grain_1d([1.0] * 4, [(0, 1)], block_size=0)

    def test_aggregation_monotonicity_is_empirical_not_theorem(self):
        res = AggregationMonotonicity.verify_monotonicity(
            [1.0, 2.0], [(0, 1)], block_size=2
        )
        self.assertIn("I_fine", res)
        self.assertIn("I_coarse", res)
        self.assertIn("monotone", res)
        self.assertNotIn("authority_effect", res)

    def test_born_rule_is_declared_map_not_derivation(self):
        probs = born_rule([1.0 + 0j, 0.0 + 1j])
        self.assertAlmostEqual(sum(probs), 1.0, places=5)
        with self.assertRaises(ValueError):
            born_rule([0.0, 0.0])

    def test_l1_probability_refuses_negative_zero_or_multidimensional(self):
        with self.assertRaises(ValueError):
            l1_probability([-1.0, 2.0])
        with self.assertRaises(ValueError):
            l1_probability([0.0, 0.0])
        with self.assertRaises(ValueError):
            l1_probability(np.ones((2, 2)))
        probs = l1_probability([1.0, 3.0])
        self.assertAlmostEqual(sum(probs), 1.0, places=5)

    def test_density_from_h1_negative_node_index_refuses(self):
        with self.assertRaises(ValueError):
            incidence_sector_decomposition(3, [(-1, 1)], [1.0])

    def test_density_from_sectors_diagonal_refuses_malformed_probabilities(self):
        s1 = H1Sector(0, [0], 1.0, 0.4)
        s2 = H1Sector(1, [1], 1.0, 0.4)
        cert = SectorMassCertificate(2.0, 2.0, 0.0)
        decomp = H1SectorDecomposition([s1, s2], cert)
        with self.assertRaises(ValueError):
            density_from_sectors_diagonal(decomp)

        s_neg = H1Sector(0, [0], 1.0, -0.1)
        decomp_neg = H1SectorDecomposition([s_neg], cert)
        with self.assertRaises(ValueError):
            density_from_sectors_diagonal(decomp_neg)

    def test_density_phase_witness_refuses_nonfinite_phase(self):
        s1 = H1Sector(0, [0], 1.0, 1.0)
        cert = SectorMassCertificate(1.0, 1.0, 0.0)
        decomp = H1SectorDecomposition([s1], cert)
        witness = PhaseWitness(PhaseWitnessKind.OrientedCycleTransport, [math.nan])
        with self.assertRaises(ValueError):
            density_from_sectors_with_phase(decomp, witness)

    def test_density_lift_xi_zero_conventions(self):
        self.assertEqual(compute_xi([0, 0], [0, 0]), 0.0)
        self.assertIsNone(compute_xi([1, 0], [0, 0]))
        self.assertEqual(compute_xi([1, 0], [1, 0]), 0.0)
        with self.assertRaises(ValueError):
            compute_xi([1, 0], [1, 0, 0])

    def test_density_lift_rho_l1_refuses_bool_or_nonreal(self):
        with self.assertRaises(TypeError):
            rho_l1([True, False])
        with self.assertRaises(ValueError):
            rho_l1([1.0, math.nan])

    def test_l1_norm_matches_l1_seminorm_on_valid_scalars(self):
        vec = [1.0, -2.0, 3.0]
        self.assertEqual(compute_l1_norm(vec), EdgeCochain(vec).phi1())

    def test_l1_norm_rejects_bool_strings_complex_like_l1_seminorm(self):
        with self.assertRaises(TypeError):
            compute_l1_norm([True, False])
        with self.assertRaises(TypeError):
            compute_l1_norm(["1.0"])
        with self.assertRaises(TypeError):
            compute_l1_norm([1 + 2j])
        with self.assertRaises(ValueError):
            compute_l1_norm([math.nan])

    def test_cohomology_l2_rejects_complex_vector_values(self):
        with self.assertRaises(TypeError):
            compute_l2_norm({"a": 1 + 2j})
        with self.assertRaises(TypeError):
            compute_l2_norm({"a": True})
        with self.assertRaises(ValueError):
            compute_l2_norm({"a": math.nan})

    def test_norm_gap_nonnegative_for_real_vectors(self):
        self.assertEqual(norm_gap([]), 0.0)
        self.assertEqual(norm_gap([1.0]), 0.0)
        self.assertGreater(norm_gap([1.0, 1.0]), 0.0)

    def test_gamma2_closed_near_open_trichotomy(self):
        d1 = np.array([[1.0]])
        h_zero = np.array([0.0])
        res_zero = gamma2(d1, h_zero, tolerance=1e-9)
        self.assertTrue(res_zero.is_closed)

        h_open = np.array([2.0])
        res_open = gamma2(d1, h_open, tolerance=1e-9)
        self.assertFalse(res_open.is_closed)

    def test_gamma2_verify_exactness_refuses_nonfinite_and_negative_tolerance(self):
        d1 = np.array([[1.0, 0.0]])
        d0 = np.array([[0.0], [1.0]])
        with self.assertRaises(ValueError):
            verify_exactness(np.array([[math.nan]]), d0)
        with self.assertRaises(ValueError):
            verify_exactness(d1, np.array([[math.inf]]), tolerance=1e-9)
        with self.assertRaises(ValueError):
            verify_exactness(d1, d0, tolerance=-1.0)
        with self.assertRaises(ValueError):
            verify_exactness(np.array([[1.0]]), d0)

    def test_cycle_coboundary_rejects_bad_edge_or_orientation(self):
        with self.assertRaises(ValueError):
            cycle_coboundary(-1, [])
        with self.assertRaises(ValueError):
            cycle_coboundary(2, [[(5, 1)]])
        with self.assertRaises(ValueError):
            cycle_coboundary(2, [[(0, 2)]])

    def test_dual_verification_certificate_components(self):
        B = np.array([[-1.0, 1.0]])
        phi_star = np.array([0.0])
        h = np.array([1.0])
        cert = verify_dual_witness(B, phi_star, h, Phi=0.0)
        self.assertTrue(cert["certified"])

    def test_phi_xi_acceptance_law(self):
        c_base = {"Phi1": 2.0, "Xi": 1.0}

        c_dec = {"Phi1": 1.0, "Xi": 1.0}
        self.assertTrue(accept(c_base, c_dec))

        c_xi_dec = {"Phi1": 2.0, "Xi": 0.5}
        self.assertTrue(accept(c_base, c_xi_dec))

        c_inc = {"Phi1": 3.0, "Xi": 0.1}
        self.assertFalse(accept(c_base, c_inc))

        self.assertFalse(accept(c_base, c_base))

        with self.assertRaises(KeyError):
            accept({"Phi1": 1.0}, c_base)

    def test_structural_rust_mirrors_fail_closed(self):
        with self.assertRaises(NotImplementedError):
            closure_defect_try_from_verified()
        with self.assertRaises(NotImplementedError):
            closure_regime_from_certified()
        with self.assertRaises(NotImplementedError):
            contract_by_id()
        with self.assertRaises(NotImplementedError):
            guarded_strictly_improves()
        with self.assertRaises(NotImplementedError):
            exact_repair_new()
        with self.assertRaises(NotImplementedError):
            hashes_try_new()
        with self.assertRaises(NotImplementedError):
            dual_witness_from_verified()


if __name__ == "__main__":
    unittest.main()


