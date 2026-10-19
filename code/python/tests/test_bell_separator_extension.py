"""Exact native regressions for the separator construction; no full theorem claim."""
import importlib.util
from pathlib import Path
import sys
import unittest
from fractions import Fraction as Q

PATH=Path(__file__).resolve().parents[1]/'src/qm/bell_separator_extension.py'
SPEC=importlib.util.spec_from_file_location('separator',PATH)
bell=importlib.util.module_from_spec(SPEC);sys.modules[SPEC.name]=bell;SPEC.loader.exec_module(bell)


class SeparatorTests(unittest.TestCase):
    def test_all_deterministic_pair_inputs_extend(self):
        for m in range(16):
            law=[0]*16;law[m]=1;p=bell.project_joint(law);w=bell.construct_extension(p)
            bell.verify_extension(p,w.weights)
            self.assertEqual(w.weights,tuple(map(Q,law)))
    def test_uniform_pairs_need_not_recover_the_original_hidden_law(self):
        original=[Q(1,16)]*16;p=bell.project_joint(original)
        witness=bell.construct_extension(p)
        self.assertNotEqual(witness.weights,tuple(original))
        bell.verify_extension(p,witness.weights)
        self.assertEqual(witness.separator,0)
        self.assertGreater(witness.weights.count(Q(0)),0)
    def test_all_eight_PR_facets_and_single_facet_insufficiency(self):
        for mask in bell.FACET_MASKS:
            p=[([Q(0),Q(1,2),Q(1,2),Q(0)] if mask&(1<<j) else [Q(1,2),Q(0),Q(0),Q(1,2)]) for j in range(4)]
            answer=bell.construct_extension(p)
            self.assertIsNone(answer.weights);self.assertEqual(answer.violating_mask,mask)
            self.assertEqual(answer.analysis.facets[bell.FACET_MASKS.index(mask)],4)
            if mask not in (7,8):self.assertEqual(answer.analysis.facets[bell.FACET_MASKS.index(8)],0)
    def test_all_vertex_pairs_at_two_non_grid_mixture_weights(self):
        for i in range(16):
            for j in range(16):
                for fraction in (Q(1,7),Q(2,5)):
                    law=[Q(0)]*16;law[i]+=fraction;law[j]+=1-fraction
                    p=bell.project_joint(law);answer=bell.construct_extension(p)
                    bell.verify_extension(p,answer.weights)
    def test_incompatible_A_and_B_marginals_are_refused(self):
        for row in ([Q(1,2),Q(1,2),0,0],[Q(1,2),0,Q(1,2),0]):
            p=[[Q(1,4)]*4 for _ in range(4)];p[0]=row
            with self.assertRaisesRegex(ValueError,'incompatible'):bell.construct_extension(p)
    def test_mismatched_triple_separator_is_refused(self):
        left=[1]+[0]*7;right=[0,1]+[0]*6
        with self.assertRaisesRegex(ValueError,'separator marginals differ'):bell.conditional_glue(left,right)
    def test_invalid_probabilities_and_exactness_are_refused(self):
        for bad in (True,1.0,'1'):
            with self.assertRaises(TypeError):bell.project_joint([bad]+[0]*15)
        for row in ([Q(3,2),Q(-1,2),0,0],[0,0,0,0]):
            with self.assertRaises(ValueError):bell.construct_extension([row]*4)
        with self.assertRaises(ValueError):bell.construct_extension([[Q(1,4)]*4]*3)
    def test_bad_separator_or_setting_is_refused(self):
        p=[[Q(1,4)]*4 for _ in range(4)]
        for r in (Q(-1),Q(3,4)):
            with self.assertRaisesRegex(ValueError,'outside'):bell.split_triple(p,0,r)
        with self.assertRaises(ValueError):bell.split_triple(p,True,Q(1,4))
    def test_false_normalized_extension_is_refused(self):
        p=[[Q(1,4)]*4 for _ in range(4)]
        with self.assertRaisesRegex(ValueError,'does not project'):bell.verify_extension(p,[1]+[0]*15)
    def test_arbitrary_precision_biased_marginals(self):
        d=10**100+3;law=[Q(0)]*16;law[0]=1-Q(1,d);law[15]=Q(1,d)
        p=bell.project_joint(law);w=bell.construct_extension(p);bell.verify_extension(p,w.weights)


if __name__=='__main__':unittest.main()
