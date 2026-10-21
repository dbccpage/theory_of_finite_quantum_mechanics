from fractions import Fraction as Q
from pathlib import Path
import importlib,random,sys,types,unittest
pkg=types.ModuleType('staged_qm');pkg.__path__=[str(Path(__file__).resolve().parents[1]/'src/qm')];sys.modules[pkg.__name__]=pkg;m=importlib.import_module('staged_qm.inner_product_uniqueness')
G,I=m.G,m.I
def rand_vec(r,n):return [Q(r.randint(-4,4),r.randint(1,3)) for _ in range(n)]
def rand_sym(r,n):
    A=[[Q(r.randint(-3,3),r.randint(1,2)) for _ in range(n)] for _ in range(n)]
    return [[A[i][j]+A[j][i] for j in range(n)] for i in range(n)]
def split_support(r,x):
    """Random disjoint-support split of x: each coordinate goes to u or to v."""
    u=[Q(0)]*len(x);v=[Q(0)]*len(x)
    for i,a in enumerate(x):(u if r.random()<Q(1,2) else v).__setitem__(i,a)
    return u,v
class PermutationTests(unittest.TestCase):
    def test_permute_moves_unit_vectors_forward(self):
        for n in (2,3,4):
            for s in m.all_permutations(n):
                for j in range(n):self.assertEqual(m.permute(s,m.unit_vector(n,j)),m.unit_vector(n,s[j]))
    def test_inverse_and_admission(self):
        self.assertEqual(m.inverse_permutation([1,2,0]),[2,0,1]);self.assertEqual(m.swap(3,0,2),[2,1,0])
        for bad in ([0,0],[1,2],[0,1,1],[0.0,1.0],[True,False],iter([1.0,0.0]),iter([True,False])):
            with self.assertRaises(ValueError):m.permutation(bad)
        self.assertEqual(m.permutation(iter([1,0])),[1,0]);self.assertEqual(m.permute(iter([1,0]),[Q(5),Q(7)]),[Q(7),Q(5)])
    def test_orbits_and_transitivity(self):
        self.assertEqual(m.orbits([[1,0,2]],3),[[0,1],[2]]);self.assertEqual(m.orbits([[1,2,0]],3),[[0,1,2]])
        self.assertEqual(m.transitivity_certificate([[1,2,0]],3),('not_transitive',(0,2,[[0,1,2]])))
        self.assertEqual(m.transitivity_certificate(m.closure([[1,2,0]],3),3),('transitive',None))
        self.assertEqual(m.generated_transitivity_certificate([[1,2,0]],3),('transitive',None))
        self.assertEqual(m.generated_transitivity_certificate([[1,0,2]],3),('not_transitive',(0,2,[[0,1],[2]])))
        self.assertEqual(m.transitivity_certificate([[0,1,2],[1,0,2]],3),('not_transitive',(0,2,[[0,1],[2]])))
        self.assertEqual(m.transitivity_certificate([[1,0]],2),('transitive',None))
        self.assertEqual(m.transitivity_certificate([[0,1]],2),('not_transitive',(0,1,[[0],[1]])))
    def test_generated_transitivity_agrees_with_the_closure_on_small_n(self):
        r=random.Random(7)
        for n in (1,2,3,4):
            for _ in range(15):
                perms=[r.sample(range(n),n) for _ in range(r.randint(0,2))]
                self.assertEqual(m.generated_transitivity_certificate(perms,n)[0],m.transitivity_certificate(m.closure(perms,n),n)[0])
    def test_large_carrier_is_decided_without_the_group(self):
        n=12;cycle=[(k+1)%n for k in range(n)]
        self.assertEqual(m.derive_scale(m.identity(n),[m.swap(n,0,1),cycle])[:2],('scalar',Q(1)))
        self.assertEqual(m.generated_transitivity_certificate([cycle],n),('transitive',None))
    def test_closure_is_the_generated_group(self):
        self.assertEqual(m.closure([[1,2,0]],3),[[0,1,2],[1,2,0],[2,0,1]]);self.assertEqual(m.closure([],3),[[0,1,2]])
        self.assertEqual(len(m.closure([[1,0,2,3],[1,2,3,0]],4)),24);self.assertEqual(m.closure([[1,0,2]],3),[[0,1,2],[1,0,2]])
        for s in m.closure([[1,2,3,0]],4):
            for j in range(4):self.assertEqual(m.invariance_certificate(m.identity(4),s),('invariant',None))
class SectorAdditivityTests(unittest.TestCase):
    def test_defect_equals_pair_sum_on_unit_vectors(self):
        r=random.Random(1)
        for n in (2,3,4):
            for _ in range(5):
                A=[[Q(r.randint(-3,3)) for _ in range(n)] for _ in range(n)]
                for (i,j),s in m.sector_additivity_defects(A):self.assertEqual(m.sector_additivity_defect(A,m.unit_vector(n,i),m.unit_vector(n,j)),s)
    def test_sector_additive_iff_pair_sums_vanish_on_random_splits(self):
        r=random.Random(2)
        for n in (2,3,4):
            for _ in range(20):
                A=[[Q(r.randint(-3,3)) for _ in range(n)] for _ in range(n)]
                verdict,data=m.sector_additivity_certificate(A);x=rand_vec(r,n);u,v=split_support(r,x)
                if verdict=='sector_additive':
                    self.assertEqual(m.sector_additivity_defect(A,u,v),0);self.assertEqual(m.quadratic_form(A,x),m.diagonal_readout(A,x))
                else:
                    i,j,eu,ev,d=data;self.assertNotEqual(d,0);self.assertEqual(d,A[i][j]+A[j][i])
    def test_readout_of_sector_additive_form_is_diagonal_without_symmetry(self):
        A=[[Q(3),Q(5)],[Q(-5),Q(-1)]];self.assertEqual(m.sector_additivity_certificate(A),('sector_additive',[Q(3),Q(-1)]))
        self.assertFalse(m.is_symmetric(A))
        for x in ([1,1],[2,-3],[Q(1,2),Q(1,3)]):self.assertEqual(m.quadratic_form(A,x),m.diagonal_readout(A,x))
    def test_disjoint_support_required(self):
        with self.assertRaises(ValueError):m.sector_additivity_defect(m.identity(2),[1,1],[0,1])
        with self.assertRaises(ValueError):m.diagonal_readout(m.identity(2),[1,2,3])
class InvarianceTests(unittest.TestCase):
    def test_invariance_defects_are_symmetric_part_differences(self):
        A=[[Q(1),Q(0),Q(0)],[Q(0),Q(2),Q(0)],[Q(0),Q(0),Q(1)]]
        self.assertEqual(m.invariance_defects(A,[2,1,0]),[((i,j),Q(0)) for i in range(3) for j in range(i,3)]);self.assertEqual(m.invariance_certificate(A,[2,1,0]),('invariant',None))
        self.assertEqual(m.invariance_certificate(A,[1,0,2]),('not_invariant',(0,0,[Q(1),Q(0),Q(0)],Q(2),Q(1))))
    def test_non_diagonal_forms_are_not_certified_from_the_diagonal_alone(self):
        B=[[Q(1),Q(1),Q(0)],[Q(1),Q(1),Q(0)],[Q(0),Q(0),Q(1)]];s=[0,2,1]
        self.assertTrue(all(d==0 for (i,j),d in m.invariance_defects(B,s) if i==j))
        self.assertEqual(m.invariance_certificate(B,s),('not_invariant',(0,1,[Q(1),Q(1),Q(0)],Q(2),Q(4))))
        self.assertNotEqual(m.quadratic_form(B,m.permute(s,[1,2,3])),m.quadratic_form(B,[1,2,3]))
        r=random.Random(6)
        for n in (2,3,4):
            for _ in range(30):
                A=[[Q(r.randint(-2,2)) for _ in range(n)] for _ in range(n)];s=r.sample(range(n),n);x=rand_vec(r,n)
                verdict,data=m.invariance_certificate(A,s)
                if verdict=='invariant':self.assertEqual(m.quadratic_form(A,m.permute(s,x)),m.quadratic_form(A,x))
                else:i,j,w,moved,original=data;self.assertNotEqual(moved,original);self.assertEqual(moved,m.quadratic_form(A,m.permute(s,w)));self.assertEqual(original,m.quadratic_form(A,w))
    def test_identity_form_invariant_under_every_permutation(self):
        r=random.Random(3)
        for n in (2,3,4):
            for s in m.all_permutations(n):
                self.assertEqual(m.invariance_certificate(m.identity(n),s),('invariant',None))
                x=rand_vec(r,n);self.assertEqual(m.quadratic_form(m.identity(n),m.permute(s,x)),m.quadratic_form(m.identity(n),x))
class SelectionTests(unittest.TestCase):
    def test_identity_is_selected_and_normalised(self):
        for n in (1,2,3,4):
            self.assertEqual(m.derive_scale(m.identity(n),m.all_permutations(n)),('scalar',Q(1),m.identity(n)))
            self.assertTrue(m.scale_is_positive(m.identity(n),m.all_permutations(n)))
    def test_scalar_multiples_and_scale_sign(self):
        for c in (Q(3),Q(1,2),Q(-2)):
            A=[[c if i==j else Q(0) for j in range(3)] for i in range(3)];r=m.derive_scale(A,[[1,2,0]])
            self.assertEqual(r[:2],('scalar',c));self.assertEqual(m.scale_is_positive(A,[[1,2,0]]),c>0)
    def test_random_symmetric_forms_reduce_to_the_theorem(self):
        r=random.Random(4)
        for n in (2,3):
            for _ in range(30):
                A=rand_sym(r,n);res=m.derive_scale(A,m.all_permutations(n))
                if res[0]=='scalar':self.assertEqual(A,[[res[1] if i==j else Q(0) for j in range(n)] for i in range(n)])
                elif res[0]=='not_sector_additive':i,j,u,v,d=res[1];self.assertEqual(d,2*A[i][j]);self.assertNotEqual(d,0)
                else:self.assertEqual(res[0],'not_invariant')
    def test_transitivity_needed_orbit_values(self):
        A=[[Q(1),Q(0),Q(0)],[Q(0),Q(1),Q(0)],[Q(0),Q(0),Q(5)]]
        self.assertEqual(m.derive_scale(A,[[1,0,2]]),('not_transitive',(0,2,[[0,1],[2]],[Q(1),Q(5)])))
        self.assertEqual(m.derive_scale(A,[[1,0,2],[0,2,1]])[0],'not_invariant')
    def test_non_symmetric_refused_with_witness(self):
        self.assertEqual(m.derive_scale([[Q(1),Q(1)],[Q(0),Q(1)]],m.s2()),('not_symmetric',(0,1)))
    def test_uniqueness(self):
        A=[[Q(2),Q(0)],[Q(0),Q(2)]];B=[[Q(3),Q(0)],[Q(0),Q(3)]]
        self.assertEqual(m.uniqueness_certificate(A,A,m.s2()),('equal',True));self.assertEqual(m.uniqueness_certificate(A,B,m.s2()),('proportional',(Q(3,2),True)))
        with self.assertRaises(ValueError):m.uniqueness_certificate(m.diag12(),A,m.s2())
        for bad in (5,-1,2):
            with self.assertRaises(ValueError):m.uniqueness_certificate(A,B,m.s2(),i0=bad)
        with self.assertRaises(ValueError):m.uniqueness_certificate(A,m.identity(3),m.s2())
class CountermodelTests(unittest.TestCase):
    def test_diag12_is_sector_additive_positive_but_not_invariant(self):
        D=m.diag12();self.assertTrue(m.is_symmetric(D));self.assertEqual(m.sector_additivity_certificate(D),('sector_additive',[Q(1),Q(2)]))
        self.assertEqual(m.derive_scale(D,m.s2()),('not_invariant',([1,0],0,0,[Q(1),Q(0)],Q(2),Q(1))))
        for x in ([1,0],[0,1],[1,-1],[Q(1,2),Q(1,3)]):self.assertGreater(m.quadratic_form(D,x),0)
        self.assertEqual(m.derive_scale(D,[[0,1]]),('not_transitive',(0,1,[[0],[1]],[Q(1),Q(2)])))
    def test_unif12_is_invariant_positive_but_not_sector_additive(self):
        U=m.unif12();self.assertTrue(m.is_symmetric(U))
        for s in m.s2()+[[0,1]]:self.assertEqual(m.invariance_certificate(U,s),('invariant',None))
        self.assertEqual(m.derive_scale(U,m.s2()+[[0,1]]),('not_sector_additive',(0,1,[Q(1),Q(0)],[Q(0),Q(1)],Q(2))))
        for x in ([1,0],[0,1],[1,-1],[Q(1,2),Q(-1,3)]):self.assertGreater(m.quadratic_form(U,x),0)
        self.assertEqual(m.quadratic_form(U,[1,1]),6);self.assertEqual(m.quadratic_form(U,[1,0])+m.quadratic_form(U,[0,1]),4)
class HermitianTests(unittest.TestCase):
    def test_identity_selected_over_gaussian_rationals(self):
        for n in (1,2,3):self.assertEqual(m.hermitian_derive_scale(m.hidentity(n),m.all_permutations(n)),('scalar',Q(1),m.hidentity(n)))
    def test_both_directions_are_needed(self):
        L=m.imag_leak12();self.assertTrue(m.is_hermitian(L))
        self.assertEqual(m.hermitian_sector_additivity_defects(L),[((0,1),Q(0),Q(-2))])
        e0,e1,ie1=m.hunit_vector(2,0),m.hunit_vector(2,1),m.hunit_vector(2,1,I)
        self.assertEqual(m.hermitian_sector_additivity_defect(L,e0,e1),0);self.assertEqual(m.hermitian_sector_additivity_defect(L,e0,ie1),-2)
        self.assertEqual(m.hermitian_derive_scale(L,m.s2()+[[0,1]]),('not_sector_additive',(0,1,e0,ie1,Q(-2))))
    def test_hermitian_defects_match_the_two_directions_randomly(self):
        r=random.Random(5)
        for _ in range(20):
            n=r.choice((2,3));H=[[G(Q(r.randint(-2,2)),Q(r.randint(-2,2))) for _ in range(n)] for _ in range(n)]
            for (i,j),dre,dim in m.hermitian_sector_additivity_defects(H):
                u=m.hunit_vector(n,i);self.assertEqual(m.hermitian_sector_additivity_defect(H,u,m.hunit_vector(n,j)),dre)
                self.assertEqual(m.hermitian_sector_additivity_defect(H,u,m.hunit_vector(n,j,I)),dim)
    def test_hermitian_invariance_certificate_uses_both_directions(self):
        L=m.imag_leak12();self.assertEqual(m.hermitian_invariance_defects(L,[1,0]),[((0,0),G(0)),((0,1),G(0,-2)),((1,1),G(0))])
        self.assertEqual(m.hermitian_invariance_certificate(L,[1,0]),('not_invariant',(0,1,[G(1),I],Q(4),Q(0))))
        R=[[G(1),G(1)],[G(1),G(1)]];self.assertEqual(m.hermitian_invariance_certificate(R,[1,0]),('invariant',None))
        with self.assertRaises(ValueError):m.hermitian_invariance_defects([[G(1),I],[I,G(1)]],[1,0])
        r=random.Random(8)
        for _ in range(30):
            n=r.choice((2,3));A=[[G(r.randint(-2,2),r.randint(-2,2)) for _ in range(n)] for _ in range(n)];H=[[(A[i][j]+A[j][i].conj()) for j in range(n)] for i in range(n)]
            s=r.sample(range(n),n);x=[G(r.randint(-2,2),r.randint(-2,2)) for _ in range(n)];verdict,data=m.hermitian_invariance_certificate(H,s)
            if verdict=='invariant':self.assertEqual(m.re_hermitian_form(H,m.permute(s,x)),m.re_hermitian_form(H,x))
            else:i,j,w,moved,original=data;self.assertNotEqual(moved,original);self.assertEqual(moved,m.re_hermitian_form(H,m.permute(s,w)))
    def test_hermitian_witnesses(self):
        H=[[G(1),G(0)],[G(0),G(2)]];self.assertEqual(m.hermitian_derive_scale(H,m.s2()),('not_invariant',([1,0],0,0,[G(1),G(0)],Q(2),Q(1))))
        self.assertEqual(m.hermitian_derive_scale([[G(1),I],[I,G(1)]],m.s2())[0],'not_hermitian')
        self.assertEqual(m.hermitian_derive_scale(H,[[0,1]]),('not_transitive',(0,1,[[0],[1]],[Q(1),Q(2)])))
        with self.assertRaises(ValueError):m.hermitian_sector_additivity_defect(H,[G(1),G(1)],[G(0),G(1)])
if __name__=='__main__':unittest.main()
