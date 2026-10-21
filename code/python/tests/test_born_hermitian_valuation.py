from fractions import Fraction as Q
from pathlib import Path
import importlib,random,sys,types,unittest
pkg=types.ModuleType('staged_qm');pkg.__path__=[str(Path(__file__).resolve().parents[1]/'src/qm')];sys.modules[pkg.__name__]=pkg;m=importlib.import_module('staged_qm.born_hermitian_valuation')
G,I=m.G,m.I
RHO2=[[Q(1,2),G(Q(1,4),Q(-1,4))],[G(Q(1,4),Q(1,4)),Q(1,2)]]
RHO3=[[Q(1,2),0,G(0,Q(1,4))],[0,Q(1,4),0],[G(0,Q(-1,4)),0,Q(1,4)]]
HERM2=[[Q(1,3),G(Q(1,6),Q(1,6))],[G(Q(1,6),Q(-1,6)),Q(1,3)]]
SKEW2=[[Q(1,2),G(0,Q(1,4))],[0,Q(1,2)]]
def effects2():return [m.identity(2),m.scale(Q(1,2),m.identity(2)),m.rank_one_effect([3,4*I]),m.rank_one_effect([G(1,1),1]),m.single(2,0,0),HERM2,SKEW2]
def effects3():return [m.identity(3),m.rank_one_effect([1,2*I,2]),m.rank_one_effect([2,-2,I]),m.rank_one_effect([G(1,1),G(1,-1),0]),m.single(3,1,1),m.scale(Q(1,3),m.identity(3))]
def random_matrices(n,count,seed):
    r=random.Random(seed);g=lambda:G(Q(r.randint(-5,5),r.randint(1,4)),Q(r.randint(-5,5),r.randint(1,4)))
    return [[[g() for _ in range(n)] for _ in range(n)] for _ in range(count)]
def mat_mul(A,B):return [[sum((a*b for a,b in zip(r,c)),G(0)) for c in zip(*B)] for r in A]
class GaussianTests(unittest.TestCase):
    def test_arithmetic_and_repr(self):
        a=G(Q(3,5),Q(4,5));self.assertEqual(repr(a),'3/5+4/5i');self.assertEqual((repr(I),repr(G(2)),repr(G(0,Q(-1,2))),repr(G(Q(1,4),Q(-1,4)))),('1i','2','-1/2i','1/4-1/4i'))
        self.assertEqual(I*I,-1);self.assertEqual(a*a.conj(),1);self.assertEqual(a.norm_sq(),1);self.assertEqual(G((3,4)),G(3,4));self.assertEqual(G(G(3,4)),G(3,4))
        self.assertEqual(G(1,2)/G(3,4),G(Q(11,25),Q(2,25)));self.assertEqual(1/I,-I);self.assertEqual(2-I,G(2,-1));self.assertEqual(Q(1,2)*I,G(0,Q(1,2)));self.assertEqual(sum([I,1,I]),G(1,2))
        self.assertEqual(hash(G(2)),hash(G(2,0)));self.assertFalse(G(0));self.assertTrue(I);self.assertNotEqual(I,1)
    def test_equality_and_hash_agree_with_rationals(self):
        self.assertEqual(G(2),2);self.assertEqual(hash(G(2)),hash(2));self.assertEqual(hash(G(Q(1,2))),hash(Q(1,2)));self.assertEqual(len({G(2),2,Q(2)}),1);self.assertIn(2,{G(2)});self.assertIn(G(2),{2})
        self.assertNotEqual(hash(G(0,1)),hash(G(1,0)));self.assertEqual(len({G(1,1),G(1,1)}),1)
    def test_extension_layer_is_shared_with_the_rational_module(self):
        r=importlib.import_module('staged_qm.born_effect_valuation')
        self.assertIs(m.extension_layer,r.extension_layer);self.assertIs(m._q,r._q)
        for name in ('is_effect','effect_certificate','midpoint','extend','extension_consistency','valuation_axioms'):self.assertEqual(getattr(m,name).__code__.co_code,getattr(r,name).__code__.co_code)
    def test_inexact_inputs_refused(self):
        for f in (lambda:G(1.5),lambda:G(True),lambda:G(1,0.5),lambda:G((1,2),3),lambda:G((1,2,3)),lambda:G('1'),lambda:I+0.5,lambda:m.matrix([[1.0]]),lambda:m.vector([True]),lambda:m.scale(0.5,m.identity(2)),lambda:m.single(2,0,0,1.0)):
            with self.assertRaises(ValueError):f()
    def test_matrix_helpers(self):
        A=[[1,G(2,3)],[G(0,-1),4]];self.assertEqual(m.adjoint(A),[[1,I],[G(2,-3),4]]);self.assertFalse(m.is_hermitian(A));self.assertTrue(m.is_hermitian(m.hermitian_part(A)));self.assertTrue(m.is_hermitian(RHO2) and m.is_hermitian(RHO3))
        self.assertEqual(m.inner([1,I],[I,1]),G(0,0));self.assertEqual(m.inner([I],[I]),1);self.assertEqual(m.outer([1,I],[1,I]),[[1,-I],[I,1]]);self.assertEqual(m.trace(RHO2),1);self.assertEqual(m.trace_mul(RHO2,m.single(2,0,1)),G(Q(1,4),Q(1,4)))
        self.assertEqual(m.hermitian_form(A,[1,I]),G(1,2));self.assertEqual(m.re_hermitian_form(A,[1,I]),1);self.assertEqual(m.single(2,0,1,I),[[0,I],[0,0]])
class GramTests(unittest.TestCase):
    def test_psd_decomposition_reconstructs(self):
        for E in (RHO2,RHO3,HERM2,m.identity(3),[[0,0],[0,1]],[[1,I],[-I,1]],[[2,G(1,1)],[G(1,-1),1]]):
            kind,terms=m.gram_decomposition(E);self.assertEqual(kind,'psd');self.assertTrue(m.verify_gram(E,terms));self.assertTrue(all(type(d) is Q and d>=0 for d,_ in terms))
        self.assertEqual(m.psd_certificate(RHO2),{'status':'psd','terms':[('1/2',['1','1/2+1/2i']),('1/4',['0','1'])],'reconstructs':True})
    def test_negative_witness_is_exact(self):
        cases={((0,1),(1,0)):([1,-1],-2),((0,I),(-I,0)):([1,I],-2),((0,G(1,1)),(G(1,-1),2)):([1,G(Q(-1,2),Q(1,2))],-1),((1,0,0),(0,0,2*I),(0,-2*I,1)):([0,1,2*I],-4),((1,2*I),(-2*I,1)):([-2*I,1],-3),((-1,0),(0,1)):([1,0],-1),((1,G(1,-1)),(G(1,1),1)):([G(-1,1),1],-1)}
        for E,(x,value) in cases.items():
            kind,w=m.gram_decomposition([list(r) for r in E]);self.assertEqual(kind,'not_psd');self.assertEqual(w,m.vector(x));self.assertEqual(m.hermitian_form(E,w),value);self.assertLess(value,0)
    def test_zero_pivot_witness_formula(self):
        for c,mm in ((G(1,1),0),(G(1,1),2),(G(0,-3),-1),(G(Q(2,3),Q(-1,5)),Q(7,3))):
            E=[[0,c.conj()],[c,mm]];kind,x=m.gram_decomposition(E);t=Q(1) if mm<=0 else 1/Q(mm)
            self.assertEqual(kind,'not_psd');self.assertEqual(x,[G(1),-c*t]);self.assertEqual(m.hermitian_form(E,x),c.norm_sq()*t*(t*mm-2))
    def test_nonhermitian_refused_and_hermitian_part_used(self):
        with self.assertRaises(ValueError):m.gram_decomposition([[1,2*I],[0,1]])
        with self.assertRaises(ValueError):m.gram_decomposition([[1,I],[I,1]])
        self.assertTrue(m.is_psd([[1,2*I],[0,1]]));self.assertFalse(m.is_psd([[1,4*I],[0,1]]));self.assertEqual(m.psd_certificate([[1,4*I],[0,1]])['value'],'-3')
class EffectTests(unittest.TestCase):
    def test_effects(self):
        self.assertTrue(all(m.is_effect(E) for E in effects2()+effects3()));self.assertFalse(m.is_effect(m.scale(2,m.identity(2))));self.assertFalse(m.is_effect([[1,I],[-I,0]]));self.assertFalse(m.is_effect([[1,I],[-I,1]]))
    def test_rank_one_effect_is_projector(self):
        for x,P in (([3,4*I],[[Q(9,25),G(0,Q(-12,25))],[G(0,Q(12,25)),Q(16,25)]]),([G(1,1),1],[[Q(2,3),G(Q(1,3),Q(1,3))],[G(Q(1,3),Q(-1,3)),Q(1,3)]])):
            E=m.rank_one_effect(x);self.assertEqual(E,P);self.assertEqual(m.trace(E),1);self.assertTrue(m.is_hermitian(E));self.assertEqual(mat_mul(E,E),E)
    def test_order_unit_bound(self):
        A=[[1,2*I],[G(3,-1),-4]];k=m.order_unit_bound(A);self.assertEqual(k,11)
        for x in ([1,0],[0,1],[1,I],[G(2,-3),1],[Q(1,3),G(0,Q(5,7))]):self.assertTrue(m.bounded_by(A,k,x))
        self.assertFalse(m.bounded_by(A,Q(1,10),[0,1]))
class ExtensionTests(unittest.TestCase):
    def test_extension_is_independent_of_bound_and_recovers_rho(self):
        for rho,n in ((RHO2,2),(RHO3,3)):
            v=m.born_valuation(rho)
            for A in (m.identity(n),m.single(n,0,1),m.single(n,0,1,I),m.sub(m.single(n,0,0),m.scale(G(3,1),m.identity(n)))):
                c=m.extension_consistency(v,A,[1,2,5,Q(7,2)]);self.assertTrue(c['consistent']);self.assertEqual(m.extend(v,A),m.trace_mul(m.matrix(rho),m.matrix(A)).re)
            self.assertEqual(m.representing_matrix(v,n),m.matrix(rho))
    def test_representing_matrix_reproduces_extension_on_random_matrices(self):
        for v,n in ((m.born_valuation(RHO2),2),(m.imaginary_leak_valuation,2),(m.born_valuation(RHO3),3),(m.bad_linear_valuation,3)):
            rho=m.representing_matrix(v,n)
            for A in random_matrices(n,6,seed=n):self.assertEqual(m.extend(v,A),m.trace_mul(rho,A).re);self.assertEqual(m.extend(v,A),Q(v(A)))
    def test_born_certificate(self):
        for rho,n,effs in ((RHO2,2,effects2()),(RHO3,3,effects3())):
            c=m.born_certificate(m.born_valuation(rho),n,effs);self.assertTrue(c['hermitian'] and c['trace_real'] and c['psd'] and c['agrees_on_effects'] and c['psd_certificate']['reconstructs']);self.assertEqual(c['trace'],'1');self.assertEqual(c['effects_checked'],len(effs));self.assertEqual(c['rho'],[list(map(str,r)) for r in m.matrix(rho)])
    def test_born_valuation_satisfies_axioms(self):
        effs=effects2();pairs=[(m.scale(Q(1,2),m.identity(2)),m.scale(Q(1,2),m.identity(2))),(m.rank_one_effect([3,4*I]),m.rank_one_effect([4*I,3])),(m.rank_one_effect([G(1,1),1]),m.rank_one_effect([1,G(-1,1)])),(m.single(2,0,0),m.single(2,1,1))]
        self.assertTrue(all(m.add(E,F)==m.identity(2) for E,F in pairs[1:]));self.assertEqual(m.valuation_axioms(m.born_valuation(RHO2),2,effs,pairs),{'unit':True,'nonneg':True,'additive':True})
    def test_born_valuation_is_blind_to_the_skew_part(self):
        v=m.born_valuation(RHO2);H=m.hermitian_part(SKEW2);self.assertFalse(m.is_hermitian(SKEW2));self.assertTrue(m.is_effect(SKEW2) and m.is_effect(H));self.assertEqual(v(SKEW2),v(H));self.assertEqual(v(SKEW2),Q(7,16))
        self.assertNotEqual(m.imaginary_leak_valuation(SKEW2),m.imaginary_leak_valuation(H));self.assertEqual((m.imaginary_leak_valuation(SKEW2),m.imaginary_leak_valuation(H)),(Q(3,4),Q(5,8)))
    def test_non_additive_control_has_inconsistent_extension(self):
        self.assertEqual(m.valuation_axioms(m.square_valuation,2,effects2(),[(m.scale(Q(1,2),m.identity(2)),m.scale(Q(1,2),m.identity(2)))]),{'unit':True,'nonneg':True,'additive':False})
        self.assertFalse(m.extension_consistency(m.square_valuation,m.identity(2),[1,2])['consistent'])
    def test_non_positive_control_has_non_psd_representative(self):
        c=m.born_certificate(m.bad_linear_valuation,3);self.assertEqual(c['trace'],'1');self.assertTrue(c['hermitian']);self.assertFalse(c['psd']);self.assertEqual(c['psd_certificate']['witness'],['0','0','1']);self.assertEqual(c['psd_certificate']['value'],'-1')
    def test_imaginary_leak_control_is_unital_additive_but_not_hermitian_nor_psd(self):
        v=m.imaginary_leak_valuation;c=m.born_certificate(v,2,effects2())
        self.assertEqual(c['rho'],[['1','0'],['-1i','0']]);self.assertFalse(c['hermitian']);self.assertEqual(c['trace'],'1');self.assertTrue(c['trace_real']);self.assertFalse(c['psd']);self.assertTrue(c['agrees_on_effects'])
        self.assertEqual(c['psd_certificate'],{'status':'not_psd','witness':['-1/2i','1'],'value':'-1/4'});self.assertEqual(m.hermitian_part(m.representing_matrix(v,2)),[[1,G(0,Q(1,2))],[G(0,Q(-1,2)),0]])
        self.assertEqual(m.valuation_axioms(v,2,effects2(),[(m.scale(Q(1,2),m.identity(2)),m.scale(Q(1,2),m.identity(2))),(m.rank_one_effect([3,4*I]),m.rank_one_effect([4*I,3]))]),{'unit':True,'nonneg':False,'additive':True})
        witness=m.rank_one_effect([G(0,Q(-1,2)),1]);self.assertTrue(m.is_effect(witness));self.assertEqual(v(witness),Q(-1,5));self.assertEqual(v(m.rank_one_effect([3,4*I])),Q(-3,25))
    def test_unit_cannot_be_dropped(self):
        v=lambda E:m.trace_mul(m.matrix(RHO2),m.matrix(E)).re*2;self.assertNotEqual(m.born_certificate(v,2)['trace'],'1')
    def test_shape_mismatches_are_refused_not_truncated(self):
        v=m.born_valuation(RHO2)
        for f in (lambda:m.born_certificate(v,2,[m.identity(3)]),lambda:m.valuation_axioms(v,2,[m.identity(3)],[]),lambda:m.valuation_axioms(v,2,[],[(m.identity(2),m.identity(3))]),lambda:v(m.identity(3)),lambda:m.verify_gram([[1,0],[0,0]],[(1,[1,0,5])]),lambda:m.bounded_by([[1,0],[0,100]],1,[1]),lambda:m.trace_mul(m.identity(2),m.identity(3)),lambda:m.add(m.identity(2),m.identity(3)),lambda:m.sub(m.identity(2),[[1,2,3]]),lambda:m.inner([1,2],[1]),lambda:m.mat_vec(m.identity(2),[1]),lambda:m.single(2,2,0),lambda:m.matrix([[1,2],[3]]),lambda:m.matrix([]),lambda:m.vector([]),lambda:m.rank_one_effect([0,0]),lambda:m.midpoint(m.identity(2),0),lambda:m.bad_linear_valuation(m.identity(2)),lambda:m.imaginary_leak_valuation([[1]]),lambda:m.extend(lambda E:I,m.identity(2))):
            with self.assertRaises(ValueError):f()
    def test_effect_certificate_is_consistent_with_its_parts(self):
        for E in (m.identity(2),m.scale(2,m.identity(2)),[[1,I],[-I,0]],m.rank_one_effect([3,4*I]),SKEW2,HERM2):
            c=m.effect_certificate(E);self.assertEqual(c['is_effect'],c['lower']['status']=='psd' and c['upper']['status']=='psd');self.assertEqual(c['is_effect'],m.is_effect(E))
if __name__=='__main__':unittest.main()
