from fractions import Fraction as Q
from pathlib import Path
import importlib,sys,types,unittest
pkg=types.ModuleType('staged_qm');pkg.__path__=[str(Path(__file__).resolve().parents[1]/'src/qm')];sys.modules[pkg.__name__]=pkg;m=importlib.import_module('staged_qm.born_effect_valuation')
RHO2=[[Q(1,2),Q(1,4)],[Q(1,4),Q(1,2)]]
RHO3=[[Q(1,2),0,Q(1,4)],[0,Q(1,4),0],[Q(1,4),0,Q(1,4)]]
def effects2():return [m.identity(2),m.scale(Q(1,2),m.identity(2)),m.rank_one_effect([3,4]),m.rank_one_effect([1,-1]),m.single(2,0,0),[[Q(1,3),Q(1,6)],[Q(1,6),Q(1,3)]]]
def effects3():return [m.identity(3),m.rank_one_effect([1,2,2]),m.rank_one_effect([2,-2,1]),m.single(3,1,1),m.scale(Q(1,3),m.identity(3))]
class GramTests(unittest.TestCase):
    def test_psd_decomposition_reconstructs(self):
        for E in (RHO2,RHO3,m.identity(3),[[0,0],[0,1]],[[1,1],[1,1]]):
            kind,terms=m.gram_decomposition(E);self.assertEqual(kind,'psd');self.assertTrue(m.verify_gram(E,terms))
    def test_negative_witness_is_exact(self):
        for E in ([[1,2],[2,1]],[[0,1],[1,0]],[[-1,0],[0,1]],[[1,0,0],[0,0,2],[0,2,1]]):
            kind,x=m.gram_decomposition(E);self.assertEqual(kind,'not_psd');self.assertLess(m.quadratic_form(m.matrix(E),x),0)
    def test_nonsymmetric_refused_and_symmetric_part_used(self):
        with self.assertRaises(ValueError):m.gram_decomposition([[1,2],[0,1]])
        self.assertTrue(m.is_psd([[1,2],[0,1]]));self.assertFalse(m.is_psd([[1,4],[0,1]]))
class EffectTests(unittest.TestCase):
    def test_effects(self):
        self.assertTrue(all(m.is_effect(E) for E in effects2()+effects3()));self.assertFalse(m.is_effect(m.scale(2,m.identity(2))));self.assertFalse(m.is_effect([[1,1],[1,0]]))
    def test_rank_one_effect_is_projector(self):P=m.rank_one_effect([3,4]);self.assertEqual(P,[[Q(9,25),Q(12,25)],[Q(12,25),Q(16,25)]]);self.assertEqual(m.trace(P),1)
    def test_order_unit_bound(self):
        A=[[1,2],[3,-4]];k=m.order_unit_bound(A);self.assertEqual(k,10)
        for x in ([1,0],[0,1],[1,1],[2,-3],[Q(1,3),Q(5,7)]):self.assertTrue(m.bounded_by(A,k,x))
class ExtensionTests(unittest.TestCase):
    def test_extension_is_independent_of_bound_and_recovers_rho(self):
        for rho,n in ((RHO2,2),(RHO3,3)):
            v=m.born_valuation(rho)
            for A in (m.identity(n),m.single(n,0,1),m.sub(m.single(n,0,0),m.scale(3,m.identity(n)))):
                c=m.extension_consistency(v,A,[1,2,5,Q(7,2)]);self.assertTrue(c['consistent']);self.assertEqual(m.extend(v,A),m.trace_mul(m.matrix(rho),m.matrix(A)))
            self.assertEqual(m.representing_matrix(v,n),m.matrix(rho))
    def test_born_certificate(self):
        for rho,n,effs in ((RHO2,2,effects2()),(RHO3,3,effects3())):
            c=m.born_certificate(m.born_valuation(rho),n,effs);self.assertTrue(c['symmetric'] and c['psd'] and c['agrees_on_effects']);self.assertEqual(c['trace'],'1');self.assertEqual(c['effects_checked'],len(effs))
    def test_born_valuation_satisfies_axioms(self):
        effs=effects2();pairs=[(m.scale(Q(1,2),m.identity(2)),m.scale(Q(1,2),m.identity(2))),(m.rank_one_effect([3,4]),m.rank_one_effect([4,-3])),(m.single(2,0,0),m.single(2,1,1))]
        self.assertEqual(m.valuation_axioms(m.born_valuation(RHO2),2,effs,pairs),{'unit':True,'nonneg':True,'additive':True})
    def test_non_additive_control_has_inconsistent_extension(self):
        self.assertEqual(m.valuation_axioms(m.square_valuation,2,effects2(),[(m.scale(Q(1,2),m.identity(2)),m.scale(Q(1,2),m.identity(2)))]),{'unit':True,'nonneg':True,'additive':False})
        self.assertFalse(m.extension_consistency(m.square_valuation,m.identity(2),[1,2])['consistent'])
    def test_non_positive_control_has_non_psd_representative(self):
        c=m.born_certificate(m.bad_linear_valuation,3);self.assertEqual(c['trace'],'1');self.assertFalse(c['psd']);self.assertEqual(c['psd_certificate']['witness'],['0','0','1']);self.assertEqual(c['psd_certificate']['value'],'-1')
    def test_unit_cannot_be_dropped(self):
        v=lambda E:m.trace_mul(m.matrix(RHO2),m.matrix(E))*2;self.assertNotEqual(m.born_certificate(v,2)['trace'],'1')
    def test_shape_mismatches_are_refused_not_truncated(self):
        v=m.born_valuation(RHO2)
        for f in (lambda:m.born_certificate(v,2,[m.identity(3)]),lambda:m.valuation_axioms(v,2,[m.identity(3)],[]),lambda:m.valuation_axioms(v,2,[],[(m.identity(2),m.identity(3))]),lambda:v(m.identity(3)),lambda:m.verify_gram([[1,0],[0,0]],[(1,[1,0,5])]),lambda:m.bounded_by([[1,0],[0,100]],1,[1]),lambda:m.solve_linear_system([],[]),lambda:m.solve_linear_system([[1,2]],[1,2]),lambda:m.trace_mul(m.identity(2),m.identity(3)),lambda:m.add(m.identity(2),m.identity(3)),lambda:m.dot([1,2],[1]),lambda:m.mat_vec(m.identity(2),[1]),lambda:m.single(2,2,0)):
            with self.assertRaises(ValueError):f()
    def test_effect_certificate_is_consistent_with_its_parts(self):
        for E in (m.identity(2),m.scale(2,m.identity(2)),[[1,1],[1,0]],m.rank_one_effect([3,4])):
            c=m.effect_certificate(E);self.assertEqual(c['is_effect'],c['lower']['status']=='psd' and c['upper']['status']=='psd');self.assertEqual(c['is_effect'],m.is_effect(E))
class RationalSphereTests(unittest.TestCase):
    def test_rays_and_parity(self):
        self.assertTrue(m.is_ray((3,4,0)) and m.is_ray((1,2,2)) and m.is_ray((0,0,1)));self.assertFalse(m.is_ray((2,0,0)));self.assertFalse(m.is_ray((1,1,0)))
        self.assertEqual((m.parity((0,4,3)),m.parity((0,3,4)),m.parity((2,2,1))),(1,0,1))
    def test_parity_is_a_frame_function_on_all_orthogonal_triples_in_box(self):
        c=m.parity_frame_check(5);self.assertTrue(c['nonvacuous'] and c['all_sum_to_one']);self.assertGreater(c['orthogonal_triples'],10);self.assertEqual(c['values'],['0','1'])
    def test_parity_frame_check_is_not_vacuously_true(self):
        c=m.parity_frame_check(0);self.assertEqual((c['orthogonal_triples'],c['nonvacuous'],c['all_sum_to_one']),(0,False,False))
    def test_parity_has_no_quadratic_representative(self):
        c=m.parity_quadratic_system(m.PARITY_WITNESS_RAYS);self.assertEqual(c['status'],'inconsistent')
        self.assertEqual(m.parity_quadratic_system(m.PARITY_WITNESS_RAYS[:5])['status'],'solution')
if __name__=='__main__':unittest.main()
