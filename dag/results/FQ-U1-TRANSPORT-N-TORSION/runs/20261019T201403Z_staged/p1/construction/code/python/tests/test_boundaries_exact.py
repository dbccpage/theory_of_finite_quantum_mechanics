import importlib.util,sys,unittest
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').is_file())
def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=module('boundary_producer',ROOT/'code/python/src/qm/boundaries_exact.py');sys.path.insert(0,str(ROOT/'dag/pfp'));from boundaries_checker import verify
class BoundaryChecks(unittest.TestCase):
    def check_values(self,kind,values):
        x=list(map(str,values));out=m.evaluate(kind,x);verify(kind,x,out);return list(map(Q,out))
    def test_Q8_group_all(self):
        for a,b,c in product(range(8),repeat=3):
            x,y,z=m.quat(a),m.quat(b),m.quat(c);self.assertEqual(m.qmul(m.qmul(x,y),z),m.qmul(x,m.qmul(y,z)))
        for a in range(8):self.assertEqual(m.qmul(m.quat(a),m.qinv(m.quat(a))),m.quat(0))
    def test_all_context_subsets(self):
        self.check_values('parity',[63])
        for mask in range(64):
            sol=m.mp_solutions(mask);self.assertEqual(len(sol),0 if mask==63 else 2**(9-bin(mask).count('1')))
    def test_repetition_guarantee_and_logical_failure(self):
        for n in (1,3,5,7):
            out=self.check_values('syndrome',[n]);rows=[out[3+3*e:6+3*e] for e in range(2**n)]
            for weight,syndrome,logical in rows:
                if weight<=(n-1)//2:self.assertEqual(logical,0)
            self.assertEqual(rows[-1][1:],[0,1])
    def test_queue_boundary_grid(self):
        for a,b,W in product(range(4),repeat=3):
            out=self.check_values('threshold',[a,b,W,5,1,1,1,1,1])
            if b>=a:self.assertTrue(all(v<=u for u,v in zip(out[:5],out[1:6])))
    def test_choi_interval_and_rank(self):
        for p in [Q(-1,2),Q(-1,3),0,Q(1,3),1,Q(3,2)]:
            out=self.check_values('choi',[p]);self.assertEqual(min(out[20:24])>=0,Q(-1,3)<=p<=1)
        self.assertEqual(self.check_values('choi',[1])[40],1);self.assertEqual(self.check_values('choi',[Q(-1,3)])[40],3)
    def test_finite_POVM_not_PSD(self):
        out=self.check_values('busch',[Q(1,2)]*4);self.assertTrue(all(z>=0 for z in out[28:34]));self.assertLess(out[38],0);self.assertLess(out[39],0)
    def test_proxy_matrix_and_missing_fourth_ray(self):
        for k in range(5):self.assertEqual(self.check_values('proxy',[k])[-5:],[Q(i!=k) for i in range(5)])
        # This fourth-ray counterexample passes all three source proxy rays.
        rho=[[Q(1,2),Q(-3,4)],[Q(-3,4),Q(1,2)]]
        values=[sum(v[i]*rho[i][j]*v[j] for i in range(2) for j in range(2)) for v in [(1,0),(0,1),(1,-1),(1,1)]]
        self.assertTrue(min(values[:3])>=0);self.assertLess(values[3],0)
    def test_graph_normal_forms(self):
        for N in range(1,6):
            v=[N]+[0]*9;out=self.check_values('torsion',v);self.assertEqual(out[9],N*N)
        self.check_values('torsion',[5,4,3,2,1,0,4,3,2,1])
    def test_maps_minimum_grid(self):
        for z in [Q(k,8) for k in range(-8,25)]:
            out=self.check_values('maps',[z]);self.assertGreaterEqual(out[7],0);self.assertEqual(out[7],out[8])
    def test_bad_domains(self):
        for kind,x in [('registry',[12,9,11,11,7,10,16,7,5]),('survival',[1,2,0]),('relative',[1,1,1,0,1,0,0]),('threshold',[1,2,0,33,1,1,1,1,1]),('syndrome',[2]),('packet',[1,1,1,1,0,0,1]),('q8',[0,0,0,8,0]),('parity',[64]),('born',[0,0,0]),('synthesis',[4]),('proxy',[5]),('torsion',[0]+[0]*9)]:
            with self.subTest(kind=kind),self.assertRaises(ValueError):m.evaluate(kind,list(map(str,x)))
if __name__=='__main__':unittest.main()
