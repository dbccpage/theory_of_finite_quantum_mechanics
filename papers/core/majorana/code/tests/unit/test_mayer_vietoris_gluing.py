r"""Unit tests for Mayer-Vietoris Local-to-Global Sheaf Gluing & Leakage-Free HPL Engine.

Verifies:
1. Condition 1: Triple overlap contraction compatibility.
2. Condition 2: Connecting homomorphism intertwining.
3. Condition 3: Zero cross-term subspace leakage L_P = 0.
4. Gate-11 classification and SHA-256 evidence digest under AuthorityEffect: None.
"""

import unittest
import numpy as np
from omega_engine.crates.solver.solv_mayer_vietoris_gluing import (
    LocalContraction,
    MayerVietorisOutput,
    MayerVietorisRestriction,
    MayerVietorisGluingSolver,
)



class TestMayerVietorisGluing(unittest.TestCase):
    def setUp(self):
        self.solver = MayerVietorisGluingSolver(tol=1e-6)

    def test_leakage_free_gluing_p_exact(self):
        eye2 = np.eye(2)
        zero2 = np.zeros((2, 2))

        c_U = LocalContraction("U", i_map=eye2, r_map=eye2, h_map=zero2, projector_P=eye2)
        c_V = LocalContraction("V", i_map=eye2, r_map=eye2, h_map=zero2, projector_P=eye2)
        c_UV = LocalContraction("U_cap_V", i_map=eye2, r_map=eye2, h_map=zero2, projector_P=eye2)

        delta_star = eye2
        delta_D_UV = zero2
        delta_D_union = zero2
        constraint_A = zero2

        output = self.solver.glue_sheaves(
            c_U, c_V, c_UV, delta_star, delta_D_UV, delta_D_union, constraint_A
        )

        self.assertTrue(output.is_condition_1_valid)
        self.assertTrue(output.is_condition_2_valid)
        self.assertTrue(output.is_condition_3_valid)
        self.assertEqual(output.glued_leakage_L_P, 0.0)
        self.assertEqual(output.trichotomy_class, "P_EXACT")
        self.assertEqual(output.authority_effect, "None")
        self.assertTrue(len(output.evidence_sha256) == 64)

    def test_intertwining_mismatch_refusal(self):
        eye2 = np.eye(2)
        zero2 = np.zeros((2, 2))

        c_U = LocalContraction("U", i_map=eye2, r_map=eye2, h_map=zero2, projector_P=eye2)
        c_V = LocalContraction("V", i_map=eye2, r_map=eye2, h_map=zero2, projector_P=eye2)
        c_UV = LocalContraction("U_cap_V", i_map=eye2, r_map=eye2, h_map=zero2, projector_P=eye2)

        delta_star = eye2
        delta_D_UV = np.array([[1.0, 0.0], [0.0, 1.0]])
        delta_D_union = np.array([[0.0, 0.0], [0.0, 0.0]])  # Intertwining fails
        constraint_A = zero2

        output = self.solver.glue_sheaves(
            c_U, c_V, c_UV, delta_star, delta_D_UV, delta_D_union, constraint_A
        )

        self.assertFalse(output.is_condition_2_valid)
        self.assertNotEqual(output.trichotomy_class, "P_EXACT")

    def test_mayer_vietoris_restriction_methods(self):
        u_res = np.array([[1.0, 0.0], [0.0, 1.0]])
        v_res = np.array([[0.5, 0.5], [0.0, 1.0]])
        restriction = MayerVietorisRestriction(degree=1, u_to_intersection=u_res, v_to_intersection=v_res)

        self.assertTrue(restriction.validate())
        self.assertEqual(restriction.domain_dims(), (2, 2))
        self.assertEqual(restriction.codomain_dim(), 2)

        cu = np.array([2.0, 3.0])
        cv = np.array([1.0, 3.0])

        diff_vec = restriction.difference(cu, cv)
        self.assertTrue(np.allclose(diff_vec, np.array([0.0, 0.0])))

        diff_fn = restriction.difference()
        self.assertTrue(np.allclose(diff_fn(cu, cv), np.array([0.0, 0.0])))

        from omega_engine.crates.solver.solv_mayer_vietoris_gluing import (
            domain_hash_vertex,
            validate_restriction_indices,
            compute_mayer_vietoris_gluing_witness,
        )

        hash_key = domain_hash_vertex("chart_U", 42)
        self.assertEqual(len(hash_key), 16)
        self.assertTrue(validate_restriction_indices(restriction, dim_u=2, dim_v=2))


if __name__ == "__main__":
    unittest.main()
