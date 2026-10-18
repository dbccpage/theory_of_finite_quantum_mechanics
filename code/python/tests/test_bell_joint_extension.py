"""Standalone exact tests; also discoverable by pytest. AuthorityEffect: None."""

import importlib.util
import sys
import unittest
from fractions import Fraction as Q
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "src/qm/bell_joint_extension.py"
SPEC = importlib.util.spec_from_file_location("bell_joint_extension", MODULE)
bell = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = bell
SPEC.loader.exec_module(bell)


class JointBellTests(unittest.TestCase):
    def check_certificate(self, weights):
        result = bell.certify_joint_law(weights)
        self.assertEqual(result.positive_score_mass + result.negative_score_mass, 1)
        self.assertEqual(result.chsh, 2*(result.positive_score_mass-result.negative_score_mass))
        self.assertEqual(result.lower_slack, 4*result.positive_score_mass)
        self.assertEqual(result.upper_slack, 4*result.negative_score_mass)
        self.assertGreaterEqual(result.lower_slack, 0)
        self.assertGreaterEqual(result.upper_slack, 0)
        return result

    def test_all_16_vertices_and_both_saturations(self):
        values = []
        for mask in range(16):
            law = [0]*16
            law[mask] = 1
            result = self.check_certificate(law)
            a0, a1, b0, b1 = (1 if mask & (1 << j) else -1 for j in range(4))
            expected = 2*a0*b0 if b0 == b1 else 2*a1*b0
            self.assertEqual(result.chsh, expected)
            self.assertEqual(result.correlators, (a0*b0, a0*b1, a1*b0, a1*b1))
            values.append(result.chsh)
        self.assertEqual(values.count(2), 8)
        self.assertEqual(values.count(-2), 8)

    def test_uniform_and_asymmetric_rational_controls(self):
        self.assertEqual(self.check_certificate([Q(1,16)]*16).chsh, 0)
        law = [Q(i,136) for i in range(1,17)]
        result = self.check_certificate(law)
        self.assertEqual(result.chsh, 0)
        self.assertEqual(result.correlators, (0,0,0,0))

    def test_all_vertex_pairs_at_three_rational_mixture_weights(self):
        for i in range(16):
            for j in range(16):
                for p in (Q(1,7), Q(2,5), Q(11,13)):
                    law = [Q(0)]*16
                    law[i] += p
                    law[j] += 1-p
                    self.check_certificate(law)

    def test_arbitrary_precision(self):
        denominator = 10**100 + 3
        law = [Q(0)]*16
        law[0], law[1] = Q(denominator-1,denominator), Q(1,denominator)
        self.assertEqual(self.check_certificate(law).chsh, 2-Q(4,denominator))

    def test_signed_normalized_near_miss_is_refused(self):
        law = [Q(0)]*16
        law[0], law[1] = Q(3,2), Q(-1,2)
        self.assertEqual(sum(law), 1)
        self.assertEqual(2*law[0]-2*law[1], 4)
        with self.assertRaisesRegex(ValueError, "nonnegative"):
            bell.certify_joint_law(law)

    def test_missing_normalization_and_wrong_carrier_are_refused(self):
        for law in ([0]*16, [2]+[0]*15, [Q(1,17)]*17, [Q(1,15)]*15):
            with self.assertRaises(ValueError):
                bell.certify_joint_law(law)

    def test_float_boolean_and_string_weights_are_refused(self):
        for bad in (1.0, True, "1"):
            with self.assertRaises(TypeError):
                bell.certify_joint_law([bad]+[0]*15)

    def test_wrong_sign_decoy_on_a_valid_law(self):
        result = self.check_certificate([1]+[0]*15)
        self.assertEqual(sum(result.correlators), 4)
        self.assertEqual(result.chsh, 2)




class OperadExpectationTests(unittest.TestCase):
    def test_composition_and_linearity_on_arbitrary_exact_tables(self):
        law = [Q((i*7+11) % 31+1) for i in range(16)]
        law = [p/sum(law) for p in law]
        table = [[Q((i+1)*(j-2), i+j+3) for j in range(4)] for i in range(16)]
        left = bell.chsh_linear(bell.joint_expectation(law, table))
        right = sum(p*bell.chsh_linear(row) for p,row in zip(law,table))
        self.assertEqual(left, right)
        self.assertEqual(bell.joint_expectation(law,bell.response_products()), bell.certify_joint_law(law).correlators)
        self.assertEqual(bell.chsh_linear(bell.joint_expectation(law,bell.response_products())),bell.certify_joint_law(law).chsh)
        # Linearity alone does not import a bound for arbitrary response maps.
        self.assertEqual(bell.chsh_linear(bell.joint_expectation(law,[[2,2,2,2]]*16)),4)

    def test_generic_map_shape_and_exactness(self):
        for table in ([[1,1,1,1]]*15, [[1,1,1]]*16):
            with self.assertRaises(ValueError): bell.joint_expectation([Q(1,16)]*16,table)
        for bad in (True, 1.0, '1'):
            with self.assertRaises(TypeError): bell.chsh_linear([1,1,1,bad])
            with self.assertRaises(TypeError): bell.joint_expectation([Q(1,16)]*16,[[1,1,1,bad]]*16)

    def test_consumer_rejects_each_forged_field(self):
        from dataclasses import replace
        law = [Q(i,136) for i in range(1,17)]
        c = bell.certify_joint_law(law)
        bell.verify_joint_certificate(law,c)
        for field in ('chsh','positive_score_mass','negative_score_mass','lower_slack','upper_slack'):
            with self.assertRaises(ValueError): bell.verify_joint_certificate(law,replace(c,**{field:getattr(c,field)+1}))
        for j in range(4):
            vector = list(c.correlators);vector[j] += 1
            with self.assertRaises(ValueError): bell.verify_joint_certificate(law,replace(c,correlators=tuple(vector)))
        with self.assertRaises(TypeError): bell.verify_joint_certificate(law,replace(c,chsh=True))

    def test_all_vertices_and_rational_mixtures_through_consumer(self):
        for i in range(16):
            for j in range(16):
                for p in (Q(1,7),Q(2,5),Q(11,13)):
                    law=[Q(0)]*16;law[i]+=p;law[j]+=1-p
                    bell.verify_joint_certificate(law,bell.certify_joint_law(law))


if __name__ == "__main__":
    unittest.main()
