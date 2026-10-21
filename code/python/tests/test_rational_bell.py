"""Targeted pure-module tests; parent package integration is outside this suite."""
from fractions import Fraction as Q
import importlib
from pathlib import Path
import sys
import types
import unittest

PACKAGE=types.ModuleType('staged_qm');PACKAGE.__path__=[str(Path(__file__).resolve().parents[1]/'src/qm')];sys.modules[PACKAGE.__name__]=PACKAGE
bell=importlib.import_module('staged_qm.rational_bell')


def data():
    rho=[[Q(1,2),0,0,Q(1,2)],[0]*4,[0]*4,[Q(1,2),0,0,Q(1,2)]]
    alice=[[[1,0],[0,-1]],[[0,1],[1,0]]]
    bob=[[[Q(3,5),Q(4,5)],[Q(4,5),Q(-3,5)]],[[Q(4,5),Q(-3,5)],[Q(-3,5),Q(-4,5)]]]
    return rho,alice,bob


class RationalBellTests(unittest.TestCase):
    def test_actual_born_table_violation_and_full_support(self):
        result=bell.certify(*data())
        self.assertEqual(result['chsh'],'14/5');self.assertEqual(result['minimum_probability'],'1/20')
        self.assertEqual(result['support_assignments'],16)
        self.assertEqual(result['locally_supported_assignments'],16)
        self.assertEqual(result['violating_mask'],8)
        self.assertGreater(Q(result['separator_lower']),Q(result['separator_upper']))
    def test_same_full_support_can_extend_for_uniform_density(self):
        _,a,b=data();rho=[[Q(i==j,4) for j in range(4)] for i in range(4)]
        result=bell.certify(rho,a,b);self.assertEqual(result['support_assignments'],16)
        self.assertEqual(result['locally_supported_assignments'],16)
        self.assertEqual(result['chsh'],'0');self.assertIsNone(result['violating_mask'])
    def test_oversized_integer_refused(self):
        rho,a,b=data()
        rho[0][0]=1<<1025
        with self.assertRaises(ValueError):bell.born_pairs(rho,a,b)
    def test_nonpositive_and_nonnormalized_states_are_refused(self):
        for value in (Q(-1,2),Q(3,2)):
            rho,a,b=data();rho[0][0]=value
            with self.assertRaises(ValueError):bell.born_pairs(rho,a,b)
    def test_nonsymmetric_or_nonbinary_observables_are_refused(self):
        for change in ((0,0,2),(0,1,1)):
            rho,a,b=data();i,j,v=change;a[0][i][j]=v
            with self.assertRaises(ValueError):bell.born_pairs(rho,a,b)
    def test_inexact_or_raw_boolean_inputs_are_refused(self):
        for value in (True,0.5,'1/2'):
            rho,a,b=data();rho[0][0]=value
            with self.assertRaises(TypeError):bell.born_pairs(rho,a,b)
    def test_all_local_outcome_sign_relabels_preserve_pair_laws(self):
        for mask in range(16):
            rho,a,b=data()
            for j,observable in enumerate(a+b):
                if mask&(1<<j):
                    for row in observable:
                        for k in range(2):row[k]=-row[k]
            pairs=bell.born_pairs(rho,a,b)
            self.assertTrue(all(min(p)>0 and sum(p)==1 for p in pairs))


if __name__=='__main__':unittest.main()
