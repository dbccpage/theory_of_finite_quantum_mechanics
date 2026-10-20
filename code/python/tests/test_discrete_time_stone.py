from fractions import Fraction as Q
from pathlib import Path
import importlib,sys,types,unittest
pkg=types.ModuleType('staged_qm');pkg.__path__=[str(Path(__file__).resolve().parents[1]/'src/qm')];sys.modules[pkg.__name__]=pkg;m=importlib.import_module('staged_qm.discrete_time_stone')
R345=m.R345;R2=m.rotation(Q(-7,25),Q(24,25));I=m.identity()
def S(M):return [list(map(str,r)) for r in M]
class OrbitTests(unittest.TestCase):
    def test_rotation_and_point(self):
        self.assertEqual(R345,[[Q(3,5),Q(-4,5)],[Q(4,5),Q(3,5)]]);self.assertEqual(m.rotation_point(R345),(Q(3,5),Q(4,5)))
        self.assertTrue(m.is_orthogonal(R345));self.assertEqual(m.det(R345),1);self.assertEqual(m.trace(R345),Q(6,5));self.assertEqual(m.rotation(1,0),I)
    def test_orbit_orthogonality_for_k_in_minus_6_to_6(self):
        e=m.discrete_evolution(R345,6);self.assertEqual(e['exponents'],list(range(-6,7)));self.assertEqual(len(e['orbit']),13);self.assertEqual(e['kmax'],6)
        self.assertTrue(e['all_orthogonal'] and e['group_law'] and e['inverse_is_transpose']);self.assertEqual(e['orbit'][6],S(I));self.assertEqual(e['orbit'][7],S(R345));self.assertEqual(e['orbit'][5],S(m.transpose(R345)))
        self.assertEqual(m.zpow(R345,2),R2);self.assertEqual(m.zpow(R345,-1),m.transpose(R345));self.assertEqual(m.mul(m.zpow(R345,-3),m.zpow(R345,3)),I);self.assertEqual(m.zpow(R345,0),I)
        self.assertEqual([m.zpow(R345,k)[1][0]*5**k for k in range(1,5)],[4,24,44,-336])
        self.assertTrue(all(m.is_orthogonal(m.zpow(R345,k)) for k in range(-6,7)))
        e0=m.discrete_evolution(m.rotation(0,1),0);self.assertEqual(e0['orbit'],[S(I)]);self.assertTrue(e0['group_law'])
    def test_rotation_order(self):
        self.assertEqual(m.rotation_order(0,1,10),4);self.assertIsNone(m.rotation_order(Q(3,5),Q(4,5),50));self.assertEqual(m.rotation_order(1,0,5),1);self.assertEqual(m.rotation_order(-1,0,5),2);self.assertIsNone(m.rotation_order(0,1,3))
class HalfStepTests(unittest.TestCase):
    def test_is_rational_square(self):
        self.assertEqual([m.is_rational_square(x) for x in (Q(4,5),Q(9,25),0,1,2,-1)],[False,True,True,True,False,False])
        self.assertEqual(m.rational_sqrt(Q(9,25)),Q(3,5));self.assertIsNone(m.rational_sqrt(Q(4,5)));self.assertIsNone(m.rational_sqrt(-1));self.assertEqual(m.rational_sqrt(Q(49,4)),Q(7,2))
    def test_half_step_outcomes(self):
        self.assertIsNone(m.half_step(Q(3,5),Q(4,5)));self.assertFalse(m.has_rational_half_step(Q(3,5),Q(4,5)))
        hs=m.half_step(Q(-7,25),Q(24,25));self.assertEqual(hs,[R345,m.neg(R345)]);self.assertTrue(m.has_rational_half_step(Q(-7,25),Q(24,25)))
        for V in hs:self.assertEqual(m.mul(V,V),R2)
        self.assertEqual(m.half_step(1,0),[I,m.neg(I)]);self.assertEqual(m.half_step(-1,0),[m.rotation(0,1),m.rotation(0,-1)]);self.assertIsNone(m.half_step(0,1))
        self.assertEqual(m.mul(m.rotation(0,1),m.rotation(0,1)),m.rotation(-1,0))
    def test_qparam_root_chain_fails_at_the_first_step_for_r345(self):
        c=m.qparam_necessary_roots(R345,2);self.assertEqual(c,{'m':2,'status':'obstructed','depth':1,'at':['3/5','4/5'],'required_square':'4/5','roots':[]})
        c4=m.qparam_necessary_roots(R345,4);self.assertEqual((c4['status'],c4['depth'],c4['required_square']),('obstructed',1,'4/5'))
        self.assertEqual(m.qparam_necessary_roots(R2,2),{'m':2,'status':'roots','depth':1,'roots':[['3/5','4/5'],['-3/5','-4/5']]})
        c8=m.qparam_necessary_roots(R2,4);self.assertEqual((c8['status'],c8['depth'],c8['at']),('obstructed',2,['3/5','4/5']))
        self.assertEqual(m.qparam_necessary_roots(R345,1),{'m':1,'status':'roots','depth':0,'roots':[['3/5','4/5']]})
        self.assertEqual(m.qparam_necessary_roots(I,4)['roots'],[['1','0'],['-1','0'],['0','1'],['0','-1']])
    def test_commutant_candidates_and_certificate(self):
        c=m.commutant_half_step_candidates(R345);self.assertEqual((c['half_trace'],c['det'],c['kappa'],c['J']),('3/5','1','-16/25',[['0','-4/5'],['4/5','0']]));self.assertEqual(c['candidate_p_squares'],['4/5','-1/5']);self.assertEqual(c['roots'],[])
        c2=m.commutant_half_step_candidates(R2);self.assertEqual(c2['candidate_p_squares'],['9/25','-16/25']);self.assertEqual(c2['roots'],[S(R345),S(m.neg(R345))])
        g=m.commutant_half_step_candidates([[0,-2],[2,0]]);self.assertEqual(g['candidate_p_squares'],['1','-1']);self.assertEqual(g['roots'],[S([[1,-1],[1,1]]),S([[-1,1],[-1,-1]])])
        self.assertEqual(m.commutant_half_step_candidates([[1,2],[3,4]])['roots'],[])
        self.assertEqual(m.no_rational_half_step_certificate(R345),{'required_square':'4/5','is_rational_square':False})
        self.assertEqual(m.no_rational_half_step_certificate(R2),{'required_square':'9/25','is_rational_square':True})
        self.assertTrue(m.irreducible_char_poly(R345) and m.irreducible_char_poly(m.rotation(0,1)));self.assertFalse(m.irreducible_char_poly(I) or m.irreducible_char_poly([[2,0],[0,3]]))
    def test_square_root_pairs(self):
        p=m.square_root_pairs(R345);self.assertEqual((p['U'],p['V'],p['neg_V']),(S(R2),S(R345),S(m.neg(R345))));self.assertTrue(p['neg_squares_to_U'] and p['distinct'] and p['V_nonzero'])
        z=m.square_root_pairs(m.zero());self.assertTrue(z['neg_squares_to_U']);self.assertFalse(z['distinct'] or z['V_nonzero'])
class RefusalTests(unittest.TestCase):
    def test_refusals(self):
        for f in (lambda:m.rotation(1,1),lambda:m.rotation(Q(1,2),Q(1,2)),lambda:m.rotation(0.6,0.8),lambda:m.matrix2([[1,2,3],[4,5,6]]),lambda:m.matrix2([[1,2]]),lambda:m.matrix2([[1,2],[3,4],[5,6]]),lambda:m.mul([[1,2,3],[4,5,6],[7,8,9]],I),lambda:m.rotation_point([[1,2],[3,4]]),lambda:m.rotation_point([[Q(3,5),Q(4,5)],[Q(4,5),Q(3,5)]]),lambda:m.zpow([[1,2],[3,4]],-1),lambda:m.zpow(R345,Q(1,2)),lambda:m.zpow(R345,True),lambda:m.discrete_evolution(R345,-1),lambda:m.discrete_evolution([[1,2],[3,4]],2),lambda:m.is_rational_square(0.8),lambda:m.half_step(1,1),lambda:m.qparam_necessary_roots(R345,3),lambda:m.qparam_necessary_roots(R345,0),lambda:m.qparam_necessary_roots([[1,2],[3,4]],2),lambda:m.commutant_half_step_candidates(I),lambda:m.commutant_half_step_candidates([[2,0],[0,3]]),lambda:m.commutant_half_step_candidates([[1,2,3],[4,5,6],[7,8,9]]),lambda:m.no_rational_half_step_certificate([[1,2],[3,4]]),lambda:m.rotation_order(0,1,0),lambda:m.rotation_order(1,1,5),lambda:m.square_root_pairs([[1,2]])):
            with self.assertRaises(ValueError):f()
    def test_zpow_of_a_non_orthogonal_matrix_is_still_defined_for_nonnegative_k(self):
        self.assertEqual(m.zpow([[1,1],[0,1]],3),[[Q(1),Q(3)],[Q(0),Q(1)]]);self.assertEqual(m.zpow([[1,1],[0,1]],0),I)
class SpecificationTests(unittest.TestCase):
    def test_specification_strings(self):
        s=m.specification();self.assertEqual(s['node'],'FQ-GAP-STONE-CONTINUOUS-TIME');self.assertEqual(s['authority_effect'],'None')
        self.assertEqual(s['continuity'],'no topology on the finite carrier; the strongest finite notion is a Q-parameter group')
        self.assertEqual(s['generator_selection'],'square roots of a step come in pairs ±V; no canonical generator')
        self.assertEqual(s['relationship'],'a Q-parameter group restricts to the Z-action of its unit step and requires roots of every order; the Pythagorean rotation has no rational half-step, so no Q-parameter group of rational 2x2 matrices passes through it; continuous time needs a carrier extension (sqrt 5)')
        self.assertEqual(s['open'],'the general triviality of Q-parameter groups over Q(i) is not proved (needs unique factorisation in Z[i])')
        self.assertIn('4/5',s['derived']);self.assertIn('Z-action',s['specified'])
    def test_lean_theorem_names_are_cited(self):
        for name in ('DiscreteTimeStoneSpec.lean','BornFable.DiscreteTime','QParamGroup','discreteEvolution','U_eq_discreteEvolution','roots_of_all_orders','sq_root_neg','half_step_not_unique','R345_pow_orthogonal','four_fifths_not_rat_square','no_rational_half_step','no_qparam_group_through_R345','AuthorityEffect: None'):self.assertIn(name,m.__doc__)
if __name__=='__main__':unittest.main()
