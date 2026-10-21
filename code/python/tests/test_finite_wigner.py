from fractions import Fraction as Q
from itertools import permutations
from math import gcd,isqrt
from pathlib import Path
import importlib,random,sys,types,unittest
pkg=types.ModuleType('staged_qm');pkg.__path__=[str(Path(__file__).resolve().parents[1]/'src/qm')];sys.modules[pkg.__name__]=pkg;m=importlib.import_module('staged_qm.finite_wigner')
G,I=m.G,m.I
PHASES=(G(1),I,G(-1),-I)
UNIT_PAIRS=((G(1),G(0)),(G(0),I),(G(Q(3,5)),G(Q(4,5))),(G(Q(5,13)),G(0,Q(12,13))),(G(Q(1,2),Q(1,2)),G(Q(1,2),Q(-1,2))))
def rand_g(r,nonzero=False):
    while True:
        z=G(Q(r.randint(-3,3),r.randint(1,3)),Q(r.randint(-3,3),r.randint(1,3)))
        if z or not nonzero:return z
def rand_vec(r,n):
    while True:
        x=[rand_g(r) for _ in range(n)]
        if any(x):return x
def rand_similarity(r,n):
    """A block-built similarity and its scale |c|^2: P1 D B P2 with permutation matrices P1, P2, unit phases D from {1,i,-1,-i}, and B a direct sum of blocks [[a,-conj b],[b,conj a]] (a = c s, b = c t, |s|^2 + |t|^2 = 1) and 1x1 blocks c*phase."""
    c=rand_g(r,True);blocks=[];k=0
    while k<n:
        if n-k>=2 and r.randint(0,1):s,t=r.choice(UNIT_PAIRS);blocks.append(m.quaternion_block(c*s,c*t));k+=2
        else:blocks.append([[c*r.choice(PHASES)]]);k+=1
    P1,P2=(m.permutation_matrix(r.sample(range(n),n)) for _ in range(2))
    F=m.mat_mul(m.mat_mul(P1,m.diagonal([r.choice(PHASES) for _ in range(n)])),m.mat_mul(m.block_diagonal(*blocks),P2))
    return F,c.norm_sq()
def scaled(c,F):return [[c*a for a in row] for row in F]
def samples(r,n,k=8):return [m.unit_vector(n,i) for i in range(n)]+[rand_vec(r,n) for _ in range(k)]
def eye(n):return m.identity(n)
# crafted maps, each breaking exactly one step of the reconstruction
def zero_second(x):return [x[0],G(0)]
def shear(x):return [x[0]+x[1],x[1]]
def leak(x):return [x[0],x[1],x[2]+x[0]*x[1]]
def collapse(x):return [x[0] if not x[1] else G(0),x[1]]
def phase_leak(x):return [x[0],x[1],x[2]+x[0]*(x[1]-x[1].conj())]
def phase_collapse(x):return [x[0] if x[1].im==0 else G(0),x[1]]
def real_fold(x):return [x[0],G(x[1].re+x[1].im)]
def stretch_imag(x):return [x[0],G(x[1].re,2*x[1].im)]
def conj_last(x):return x[:-1]+[x[-1].conj()]
def conj_first(x):return [x[0].conj()]+x[1:]
def diag12(x):return m.mat_vec(m.diagonal([1,2]),x)
class TransitionProbabilityTests(unittest.TestCase):
    def test_tp_properties_and_born_readout(self):
        r=random.Random(1)
        for n in (1,2,3,4):
            for _ in range(15):
                x,y=rand_vec(r,n),rand_vec(r,n);s=m.transition_probability(x,y);a,b=rand_g(r,True),rand_g(r,True)
                self.assertEqual(s,m.transition_probability(y,x));self.assertTrue(0<=s<=1);self.assertEqual(type(s),Q)
                self.assertEqual(s,m.born_transition(x,y));self.assertEqual(m.born_transition(y,x),s)
                self.assertEqual(m.transition_probability([a*c for c in x],[b*c for c in y]),s)
                self.assertEqual(m.transition_probability(x,x),1);self.assertEqual(m.transition_probability(m.twist(-1,x),m.twist(-1,y)),s)
                self.assertEqual(s==1,m.same_ray(x,y));self.assertEqual(s==0,m.inner(x,y)==0)
                self.assertEqual(m.vnorm(x),m.inner(x,x).re);self.assertEqual(m.inner(x,x).im,0)
    def test_unit_vectors_and_probe_values(self):
        for n in (1,2,3,4):
            for i in range(n):
                for j in range(n):self.assertEqual(m.transition_probability(m.unit_vector(n,i),m.unit_vector(n,j)),Q(int(i==j)))
        e0,e1=m.unit_vector(2,0),m.unit_vector(2,1);h,k=m.probe(2,0,1),m.probe(2,0,1,I)
        self.assertEqual(h,[G(1),G(1)]);self.assertEqual(k,[G(1),I])
        self.assertEqual([m.transition_probability(h,e0),m.transition_probability(h,e1),m.transition_probability(k,e1),m.transition_probability(k,h)],[Q(1,2)]*4)
        p,q=m.consistency_probes(3,0,1,2);self.assertEqual(m.transition_probability(p,q),Q(5,9))
        self.assertEqual(m.transition_probability([G(1),I,-I],q),Q(1,9))
        self.assertTrue(m.same_ray([G(1),I],[I,G(-1)]));self.assertFalse(m.same_ray([G(1),I],[G(1),-I]));self.assertFalse(m.same_ray([G(0),G(0)],[G(0),G(0)]))
        self.assertEqual(m.unit_vector(3,1,I),[G(0),I,G(0)])
    def test_twist(self):
        r=random.Random(2)
        for _ in range(20):
            n=r.randint(1,4);x,y=rand_vec(r,n),rand_vec(r,n)
            self.assertEqual(m.twist(1,x),x);self.assertEqual(m.twist(-1,m.twist(-1,x)),x)
            self.assertEqual(m.inner(m.twist(-1,x),m.twist(-1,y)),m.inner(x,y).conj())
        self.assertEqual(m.twist(-1,[G(1,2),G(Q(1,3),-1)]),[G(1,-2),G(Q(1,3),1)])
        for bad in (0,2,-2,True,1.0,Q(1)):
            with self.assertRaises(ValueError):m.twist(bad,[G(1)])
    def test_zero_vector_and_shape_errors(self):
        for f in (m.transition_probability,m.born_transition):
            for x,y in (([0,0],[1,0]),([1,0],[0,0]),([1,0],[1,0,0])):
                with self.assertRaises(ValueError):f(x,y)
        for bad in (lambda:m.inner([1],[1,2]),lambda:m.vnorm([]),lambda:m.vnorm([1.0]),lambda:m.vnorm([True]),lambda:m.mat_vec(eye(2),[1,2,3]),
                    lambda:m.conj_transpose([[1,2]]),lambda:m.mat_mul(eye(2),eye(3)),lambda:m.similarity_certificate([]),lambda:m.unit_vector(0,0),
                    lambda:m.unit_vector(2,2),lambda:m.unit_vector(2,-1),lambda:m.unit_vector(True,0),lambda:m.unit_vector(2,True),lambda:m.probe(2,1,1),
                    lambda:m.consistency_probes(3,0,1,1),lambda:m.block_diagonal(),lambda:m.permutation_matrix([]),lambda:m.permutation_matrix([0,0])):
            with self.assertRaises(ValueError):bad()
class SimilarityTests(unittest.TestCase):
    def test_named_similarities(self):
        self.assertEqual(m.gram(m.f3()),[[G(3),G(0)],[G(0),G(3)]]);self.assertEqual(m.similarity_certificate(m.f3()),('similarity',Q(3)))
        self.assertEqual(m.similarity_certificate(m.hadamard2()),('similarity',Q(2)))
        for n in (1,2,3,4):
            self.assertEqual(m.similarity_certificate(eye(n)),('similarity',Q(1)))
            for s in permutations(range(n)):
                P=m.permutation_matrix(list(s));self.assertEqual(m.similarity_certificate(P),('similarity',Q(1)));self.assertEqual(m.mat_mul(m.conj_transpose(P),P),eye(n))
    def test_block_built_similarities(self):
        r=random.Random(3)
        for n in (1,2,3,4):
            for _ in range(10):
                F,s=rand_similarity(r,n);self.assertEqual(m.similarity_certificate(F),('similarity',s));self.assertEqual(m.gram(F),scaled(s,eye(n)))
                F2,s2=rand_similarity(r,n);self.assertEqual(m.similarity_certificate(m.mat_mul(F,F2)),('similarity',s*s2))
                c=rand_g(r,True);self.assertEqual(m.similarity_certificate(scaled(c,F)),('similarity',c.norm_sq()*s))
        self.assertEqual(m.similarity_certificate(m.block_diagonal(m.f3(),m.f3())),('similarity',Q(3)))
        self.assertEqual(m.similarity_certificate(m.block_diagonal(m.hadamard2(),m.quaternion_block(1,1),[[G(1,1)]])),('similarity',Q(2)))
        self.assertEqual(m.similarity_certificate(m.quaternion_block(G(1,2),G(-3,1))),('similarity',Q(15)))
    def test_non_similarity_witnesses(self):
        self.assertEqual(m.similarity_certificate([[1,1],[0,1]]),('not_similarity',(0,1,G(1),G(0))))
        self.assertEqual(m.similarity_certificate(m.diagonal([1,2])),('not_similarity',(1,1,G(4),G(1))))
        self.assertEqual(m.similarity_certificate([[0,0],[0,0]]),('not_similarity',(0,0,G(0),G(0))))
        self.assertEqual(m.similarity_certificate([[0,1],[0,1]]),('not_similarity',(0,0,G(0),G(0))))
        self.assertEqual(m.similarity_certificate(m.block_diagonal(m.f3(),m.hadamard2())),('not_similarity',(2,2,G(2),G(3))))
        r=random.Random(4);seen=0
        for _ in range(60):
            n=r.randint(1,3);A=[[G(r.randint(-1,1),r.randint(-1,1)) for _ in range(n)] for _ in range(n)];verdict,data=m.similarity_certificate(A);M=m.gram(A)
            if verdict=='similarity':self.assertEqual(M,scaled(data,eye(n)));self.assertGreater(data,0)
            else:
                i,j,entry,expected=data;seen+=1;self.assertEqual(entry,M[i][j]);self.assertEqual(expected,G(M[0][0].re) if i==j else G(0))
                self.assertTrue(entry!=expected or M[0][0].re==0)
        self.assertGreater(seen,0)
    def test_scale_identities_and_tp_preserved_by_apply(self):
        r=random.Random(5)
        for n in (1,2,3,4):
            for _ in range(8):
                F,s=rand_similarity(r,n);x,y=rand_vec(r,n),rand_vec(r,n)
                self.assertEqual(m.inner(m.mat_vec(F,x),m.mat_vec(F,y)),s*m.inner(x,y));self.assertEqual(m.vnorm(m.mat_vec(F,x)),s*m.vnorm(x))
                for eps in (1,-1):
                    self.assertEqual(m.apply(F,eps,x),m.mat_vec(F,m.twist(eps,x)))
                    self.assertEqual(m.transition_probability(m.apply(F,eps,x),m.apply(F,eps,y)),m.transition_probability(x,y))
                    T=m.induced_ray_map(F,eps);self.assertEqual(m.tp_defect(T,[x,y]+m.reconstruction_probes(n)),('tp_preserved',None))
    def test_inverse_similarity_is_two_sided(self):
        r=random.Random(6);mats=[m.f3(),m.hadamard2(),m.permutation_matrix([2,0,1])]+[rand_similarity(r,n)[0] for n in (1,2,3,4) for _ in range(3)]
        for F in mats:
            n=len(F);J=m.inverse_similarity(F);self.assertEqual(m.mat_mul(F,J),eye(n));self.assertEqual(m.mat_mul(J,F),eye(n))
        self.assertEqual(m.inverse_similarity(m.f3()),scaled(Q(1,3),m.conj_transpose(m.f3())))
        with self.assertRaises(ValueError) as cm:m.inverse_similarity(m.diagonal([1,2]))
        self.assertEqual(cm.exception.args,('not_similarity',(1,1,G(4),G(1))))
    def test_permutation_matrix_matches_permute(self):
        r=random.Random(7)
        for n in (1,2,3,4):
            for s in permutations(range(n)):
                s=list(s);P=m.permutation_matrix(s);x=rand_vec(r,n);self.assertEqual(m.mat_vec(P,x),m.permute(s,x))
                for j in range(n):self.assertEqual(m.mat_vec(P,m.unit_vector(n,j)),m.unit_vector(n,s[j]))
class CoordinateTests(unittest.TestCase):
    def test_coordinates_in_orthogonal_bases(self):
        r=random.Random(8)
        for n in (1,2,3,4):
            for _ in range(8):
                F,_s=rand_similarity(r,n);f=[[F[row][i] for row in range(n)] for i in range(n)];y=rand_vec(r,n);z=m.coordinates(f,y)
                self.assertEqual([sum((z[i]*f[i][k] for i in range(n)),G(0)) for k in range(n)],y)
                self.assertEqual(z,[m.inner(f[i],y)/m.vnorm(f[i]) for i in range(n)])
    def test_coordinate_errors_carry_witnesses(self):
        with self.assertRaises(ValueError) as cm:m.coordinates([[1,0],[1,1]],[1,1])
        self.assertEqual(cm.exception.args,('not_orthogonal',(0,1,G(1))))
        with self.assertRaises(ValueError) as cm:m.coordinates([[1,0],[0,0]],[1,1])
        self.assertEqual(cm.exception.args,('zero_vector',1))
        for f,y in (([[1,0,0],[0,1,0]],[1,1,1]),([[1,0],[0,1]],[1,1,1]),([[1,0],[0,1,0]],[1,1]),([],[1])):
            with self.assertRaises(ValueError):m.coordinates(f,y)
class ReconstructionTests(unittest.TestCase):
    def test_reconstruct_recovers_induced_similarity(self):
        r=random.Random(9)
        for n in (1,2,3,4):
            for eps in (1,-1):
                for i0 in range(n):
                    for _ in range(2):
                        F,s=rand_similarity(r,n);T=m.induced_ray_map(F,eps);verdict,(F2,d2,e2)=m.reconstruct(T,n,i0);lam=m.ray_scalar(m.unit_vector(n,i0))
                        self.assertEqual(verdict,'reconstructed');self.assertEqual(F2,scaled(lam,F));self.assertEqual(d2,lam.norm_sq()*s)
                        self.assertEqual(e2,eps if n>1 else 1);self.assertEqual(m.similarity_certificate(F2),('similarity',d2))
                        self.assertEqual(m.verify_induced(T,F2,e2,samples(r,n)),('induced',None))
    def test_ray_freedom_is_exercised(self):
        self.assertEqual([m.ray_scalar(m.unit_vector(4,i)) for i in range(4)],[G(2),G(1,1),G(2,-1),G(1)])
        self.assertNotEqual(m.ray_scalar([G(1),I]),m.ray_scalar([G(1),G(1)]))
        for x in ([G(0),G(-7,5)],[G(Q(-1,3),2)],[G(-5),G(-5),G(-5)]):self.assertTrue(m.ray_scalar(x))
    def test_named_matrices_and_the_f3_countermodel(self):
        for eps in (1,-1):
            for i0 in (0,1):
                lam=m.ray_scalar(m.unit_vector(2,i0))
                verdict,(F2,d2,e2)=m.reconstruct(m.induced_ray_map(m.f3(),eps),2,i0)
                self.assertEqual((verdict,F2,d2,e2),('reconstructed',scaled(lam,m.f3()),3*lam.norm_sq(),eps))
                self.assertEqual(m.sum_of_two_rational_squares(d2),('not_representable',3));self.assertEqual(m.unitary_normalisation(F2),('not_a_norm',(d2,3)))
                verdict,(H2,h2,e2)=m.reconstruct(m.induced_ray_map(m.hadamard2(),eps),2,i0)
                self.assertEqual((verdict,H2,h2,e2),('reconstructed',scaled(lam,m.hadamard2()),2*lam.norm_sq(),eps));self.assertEqual(m.unitary_normalisation(H2)[0],'unitary')
    def test_verify_induced_rejects_wrong_eps_and_wrong_matrix(self):
        r=random.Random(10)
        for n in (2,3,4):
            for eps in (1,-1):
                F,_s=rand_similarity(r,n);T=m.induced_ray_map(F,eps);xs=samples(r,n,12)+[m.probe(n,0,1,I)]
                verdict,x=m.verify_induced(T,F,-eps,xs);self.assertEqual(verdict,'not_induced');self.assertIn(x,xs)
                self.assertTrue(any(a.im for a in x));self.assertFalse(m.same_ray(m.apply(F,-eps,x),T(x)))
                W=m.mat_mul(F,m.diagonal([-1]+[1]*(n-1)));verdict,x=m.verify_induced(T,W,eps,xs);self.assertEqual(verdict,'not_induced')
                self.assertFalse(m.same_ray(m.apply(W,eps,x),T(x)));self.assertEqual(m.verify_induced(T,scaled(G(2,-1),F),eps,xs),('induced',None))
        self.assertEqual(m.verify_induced(m.induced_ray_map(eye(2),1),[[1,0],[0,0]],1,[[0,1]]),('not_induced',[G(0),G(1)]))
        with self.assertRaises(ValueError):m.verify_induced(zero_second,eye(2),1,[[0,0]])
        with self.assertRaises(ValueError):m.verify_induced(zero_second,eye(2),1,[[1,0,0]])
        self.assertEqual(m.verify_induced(zero_second,eye(2),1,[[1,0],[0,1]]),('not_induced',[G(0),G(1)]))
    def test_non_tp_preserving_maps_yield_step_witnesses(self):
        cases=((zero_second,2,0,('zero_image',[G(0),G(1)])),(shear,2,0,('orthogonality',0,1,G(1))),
               (leak,3,0,('alignment',1,'support',2,G(1))),(collapse,2,0,('alignment',1,'vanishing',G(0),G(1))),
               (diag12,2,0,('alignment',1,'balance',Q(1),Q(4))),(diag12,2,1,('alignment',0,'balance',Q(4),Q(1))),
               (phase_leak,3,0,('alignment',1,'phase_support',2,G(0,2))),(phase_collapse,2,0,('alignment',1,'phase_vanishing',G(0),I)),
               (real_fold,2,0,('sign',1,G(1))),(stretch_imag,2,0,('sign',1,G(0,2))),(conj_last,3,0,('consistency',1,2,1,-1)),
               (conj_last,4,0,('consistency',1,3,1,-1)))
        for T,n,i0,witness in cases:
            self.assertEqual(m.reconstruct(T,n,i0),('not_tp_preserving',witness))
            probes=m.reconstruction_probes(n,i0)+(list(m.consistency_probes(n,i0,witness[1],witness[2])) if witness[0]=='consistency' else [])
            self.assertNotEqual(m.tp_defect(T,probes),('tp_preserved',None))
        self.assertEqual(m.reconstruct(m.induced_ray_map(m.diagonal([1,2]),1),2)[1][:3],('alignment',1,'balance'))
    def test_one_coordinate_conjugation(self):
        p,q=m.consistency_probes(3,0,1,2)
        self.assertEqual(m.tp_defect(conj_last,[p,q]),('tp_defect',(p,q,Q(5,9),Q(1,9))))
        self.assertEqual(m.reconstruct(conj_last,2,0),('reconstructed',(eye(2),Q(1),-1)))
        self.assertEqual(m.verify_induced(conj_last,eye(2),-1,[[1,0],[1,1],[I,1]]),('not_induced',[I,G(1)]))
        self.assertEqual(m.tp_defect(conj_last,[[I,1],[1,I]]),('tp_defect',([I,G(1)],[G(1),I],Q(0),Q(1))))
        self.assertEqual(m.reconstruct(conj_first,2,0),('reconstructed',(eye(2),Q(1),1)))
        self.assertEqual(m.verify_induced(conj_first,eye(2),1,[[1,0],[I,1]]),('not_induced',[I,G(1)]))
        self.assertEqual(m.reconstruct(conj_last,3,2),('reconstructed',(eye(3),Q(1),1)))
    def test_dimension_one(self):
        r=random.Random(11)
        for _ in range(10):
            c=rand_g(r,True);x,y=rand_vec(r,1),rand_vec(r,1);self.assertEqual(m.transition_probability(x,y),1)
            for eps in (1,-1):
                T=m.induced_ray_map([[c]],eps);verdict,(F2,d2,e2)=m.reconstruct(T,1)
                self.assertEqual((verdict,F2,d2,e2),('reconstructed',[[2*c]],4*c.norm_sq(),1))
                for e in (1,-1):self.assertEqual(m.verify_induced(T,F2,e,[x,y]),('induced',None))
        self.assertEqual(m.reconstruct(lambda x:[G(0)],1),('not_tp_preserving',('zero_image',[G(1)])))
    def test_reconstruct_admission(self):
        T=m.induced_ray_map(eye(2),1)
        for n in (0,-1,True,2.0):
            with self.assertRaises(ValueError):m.reconstruct(T,n)
        for i0 in (2,-1,True,0.0):
            with self.assertRaises(ValueError):m.reconstruct(T,2,i0)
        for bad in (None,eye(2)):
            with self.assertRaises(ValueError):m.reconstruct(bad,2)
        for bad in (lambda x:[G(1)],lambda x:[1.0,0.0],lambda x:[]):
            with self.assertRaises(ValueError):m.reconstruct(bad,2)
        with self.assertRaises(ValueError):m.tp_defect(T,[[0,0]])
        with self.assertRaises(ValueError):m.induced_ray_map(eye(2),0)
        with self.assertRaises(ValueError):T([1,2,3])
class UnitaryNormalisationTests(unittest.TestCase):
    def test_two_squares_representable(self):
        expected=((1,(1,0)),(2,(1,1)),(5,(1,2)),(9,(3,0)),(Q(9,4),(0,Q(3,2))),(13,(2,3)),(50,(7,1)),(Q(65,13),(1,2)),(65,(4,7)),(45,(3,6)),(Q(1,2),(Q(1,2),Q(1,2))),(Q(25,36),(Q(2,3),Q(1,2))))
        for d,ab in expected:
            verdict,(a,b)=m.sum_of_two_rational_squares(d);self.assertEqual(verdict,'representable');self.assertEqual((a,b),tuple(map(Q,ab)))
            self.assertEqual(a*a+b*b,d);self.assertTrue(a>=0 and b>=0);self.assertEqual((type(a),type(b)),(Q,Q))
    def test_two_squares_obstruction(self):
        for d,p in ((3,3),(7,7),(12,3),(21,3),(Q(3,4),3),(63,7),(Q(5,7),7),(Q(1,3),3),(Q(11,9),11),(3*3*3*5,3)):
            self.assertEqual(m.sum_of_two_rational_squares(d),('not_representable',p))
        for bad in (0,-1,Q(-2,3),1.5,True,G(2)):
            with self.assertRaises(ValueError):m.sum_of_two_rational_squares(bad)
    def test_two_squares_agrees_with_brute_force(self):
        for p in range(1,30):
            for q in range(1,30):
                if gcd(p,q)!=1:continue
                N=p*q;brute=any(isqrt(N-a*a)**2==N-a*a for a in range(isqrt(N)+1));verdict,data=m.sum_of_two_rational_squares(Q(p,q))
                self.assertEqual(verdict=='representable',brute)
                if brute:a,b=data;self.assertEqual(a*a+b*b,Q(p,q))
                else:
                    e=0;k=N
                    while k%data==0:k//=data;e+=1
                    self.assertEqual(data%4,3);self.assertEqual(e%2,1);self.assertTrue(all(data%t for t in range(2,isqrt(data)+1)))
    def test_unitary_normalisation(self):
        verdict,(c,U)=m.unitary_normalisation(m.hadamard2());self.assertEqual((verdict,c),('unitary',G(1,1)));self.assertEqual(m.gram(U),eye(2))
        self.assertEqual(U,[[a/G(1,1) for a in row] for row in m.hadamard2()]);self.assertEqual(scaled(c,U),m.hadamard2())
        self.assertEqual(m.unitary_normalisation(m.f3()),('not_a_norm',(Q(3),3)));self.assertEqual(m.unitary_normalisation(m.block_diagonal(m.f3(),m.f3())),('not_a_norm',(Q(3),3)))
        self.assertEqual(m.unitary_normalisation(m.diagonal([1,2])),('not_similarity',(1,1,G(4),G(1))))
        P=m.permutation_matrix([1,2,0]);self.assertEqual(m.unitary_normalisation(P),('unitary',(G(1),P)))
        r=random.Random(12)
        for n in (1,2,3,4):
            for _ in range(5):
                F,s=rand_similarity(r,n);verdict,(c,U)=m.unitary_normalisation(F)
                self.assertEqual(verdict,'unitary');self.assertEqual(c.norm_sq(),s);self.assertEqual(m.gram(U),eye(n));self.assertEqual(scaled(c,U),F)
if __name__=='__main__':unittest.main()
