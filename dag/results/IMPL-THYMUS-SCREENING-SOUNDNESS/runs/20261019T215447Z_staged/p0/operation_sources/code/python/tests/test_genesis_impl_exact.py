import importlib.util,sys,unittest
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').is_file())
spec=importlib.util.spec_from_file_location('producer',ROOT/'code/python/src/qm/genesis_impl_exact.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
sys.path.insert(0,str(ROOT/'dag/pfp'));from genesis_impl_checker import verify
class ExactControls(unittest.TestCase):
    def check(self,k,x):
        v=list(map(str,x));o=m.evaluate(k,v);verify(k,v,o);return list(map(Q,o))
    def test_weyl_complete_basis(self):
        for a,b in product(range(3),repeat=2):self.check('weyl',[a,b]+list(range(9)))
    def test_duality_sign_grid(self):
        for a,b in product(range(-4,5),repeat=2):self.check('duality',[Q(a,3),Q(b,2)])
    def test_all_cost_two_candidates(self):self.check('separation',[0])
    def test_all_two_term_assertings(self):
        for mask in range(16):self.check('distinct',[mask])
    def test_event_guards_erasure_and_monotonicity(self):
        for h in [[0,7,0,1,0,0,1,0,0,2,1,0,3,0,1,3,0,1,4,0,0,5,0,1,6,0,0,6,0,0],[0,9,0,3,0,0],[1,0,0,2,2,0,3,0,4],[1,0,0,5,0,0]]:
            for kind in ('noreturn','events','erasure','supply'):self.check(kind,h)
    def test_all_shortest_paths_apart(self):
        for seed in range(2):
            for T in (3,7):
                for mask in range(512):
                    E=m.graph(mask)
                    if m.legal(E) and all(T>>i&1 and T>>j&1 for i,j in E):self.check('fewest',[seed,T,mask])
    def test_every_legal_obstruction_merge(self):
        for mask in range(512):
            if m.legal(m.graph(mask)):
                for u,v in product(range(3),repeat=2):
                    if u!=v:self.check('obstruction',[mask,u,v])
    def test_all_injective_renamings(self):
        for mask in range(512):self.check('rename',[mask,0,1])
    def test_pair_cancellation_and_writing_orbits(self):
        for bits in product(range(2),repeat=8):self.check('sameness',bits)
        self.check('sameness',[3,2,1,0,1,2,3,4])
    def test_structural_gate_ceiling(self):
        for s,k in product(range(3),repeat=2):self.check('mss0',[s,k])
    def test_binary64_diagnostic_collisions(self):
        self.assertEqual(sys.float_info.mant_dig,53)
        for base in (0,2**52,2**53,2**54):
            for delta in range(-5,6):
                if 0<=base+delta:self.check('float',[base+delta,base])
    def test_pairing_nonuniqueness_and_negative_extension(self):
        for a,b,d,u,v in [(1,0,0,1,0),(Q(1,2),0,Q(1,2),Q(3,5),Q(4,5)),(Q(1,2),Q(1,2),Q(1,2),Q(3,5),Q(4,5))]:self.check('pairing',[a,b,d,u,v])
    def test_realification_balancing_grid(self):
        for a,b,c,d in product(range(-1,2),repeat=4):self.check('realify',[a,b,c,d])
    def test_amplitude_holonomy_and_residue(self):
        for a,b,c in product(range(-1,2),repeat=3):self.check('amplitude',[a,b,c,-1,0,1,Q(1,2),2,3,Q(-1,3)])
    def test_all_switching_orbits(self):
        for k in range(4):self.check('normal',[k])
    def test_every_small_cycle_and_zero_mass(self):
        for size in range(1,7):
            for mask in range(2**size):
                for mass in (0,1):self.check('lggr',[size,mask,mass])
    def test_all_detector_predicate_pairs_and_panels(self):
        for P,E in product(range(16),repeat=2):self.check('thymus',[3,P,E])
    def test_bad_domains(self):
        for kind,values in [('weyl',[3,0]+[0]*9),('separation',[1]),('distinct',[16]),('fewest',[0,3,1]),('obstruction',[1,0,1]),('rename',[0,0,0]),('sameness',[6]*8),('mss0',[-1,0]),('float',[-1,0]),('pairing',[1,1,0,1,0]),('amplitude',[9]+[0]*9),('normal',[4]),('lggr',[0,0,1]),('thymus',[16,0,0])]:
            with self.subTest(kind=kind),self.assertRaises(ValueError):m.evaluate(kind,list(map(str,values)))
if __name__=='__main__':unittest.main()
