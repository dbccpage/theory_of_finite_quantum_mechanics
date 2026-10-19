import importlib,sys,types,unittest
from pathlib import Path
from fractions import Fraction as Q
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'dag/pfp'))
pkg=types.ModuleType('scoped_dynamics');pkg.__path__=[str(Path(__file__).resolve().parents[1]/'src/qm')];sys.modules['scoped_dynamics']=pkg
m=importlib.import_module('scoped_dynamics.dynamics_exact')
from dynamics_checker import verify
def st(*x):return list(map(str,x))
class DynamicsTests(unittest.TestCase):
    def check(self,k,v):
        r=m.evaluate(k,v);verify(k,v,r);return list(map(Q,r))
    def test_path(self):
        r=self.check('path',st(1,1,0,1,1,2));self.assertEqual(r[:4],[1,3,0,1]);self.assertEqual(r[:4],r[4:8]);self.check('path',st(0,1,-1,0,0,0))
        with self.assertRaises(ValueError):m.evaluate('path',st(1,1,0,1,-1,2))
    def test_transfer(self):
        r=self.check('transfer',st(1,2,0,1,2,0,1,-1,3,4,2,-1));self.assertEqual(r[4:6],r[6:8]);self.assertEqual(r[10],r[11])
    def test_overcount(self):
        r=self.check('overcount',st(2,3,0));self.assertEqual(r[-1],3*r[-2]);r=self.check('overcount',st(2,3,5));self.assertNotEqual(r[-1],3*r[-2])
    def test_refinement(self):
        a=self.check('refinement',st(0,1,3,3));b=self.check('refinement',st(0,3,20,20));self.assertEqual(a[:3],[0,0,0]);self.assertGreater(b[-1],a[-1])
    def test_histories(self):
        r=self.check('histories',st(1,1,1,-1));self.assertEqual(r[3],0);self.assertEqual(r[4],2);self.assertEqual(r[5],-2)
    def test_held(self):
        r=self.check('held',st(1,2));self.assertEqual(r[:2],r[2:4]);self.assertEqual(r[4]-r[5],r[6]);self.assertNotEqual(r[4],r[5])
    def test_schrodinger(self):
        r=self.check('schrodinger',st(1,2,3,1,1,2,3,4,'1/10',1));self.assertEqual(r[8],0);self.assertEqual(r[15],r[16]);self.assertGreater(r[15],0)
        with self.assertRaises(ValueError):m.evaluate('schrodinger',st(0,0,1,0,1,0,0,0,1,0))
    def test_cayley(self):
        r=self.check('cayley',st('1/2'));self.assertEqual(r[4:8],[1,0,0,1]);self.assertEqual(r[12:16],[Q(5,4),0,0,Q(5,4)]);self.assertEqual(r[16:20],[0]*4)
    def test_lambda(self):
        r=self.check('lambda',st(2));self.assertEqual(r[54:108],r[108:162]);self.assertTrue(any(r[54:108]));self.assertEqual(r[198:],[0]*6)
    def test_heisenberg(self):
        r=self.check('heisenberg',st('1/2',1,2,3,1,-1));self.assertEqual(r[10],r[11]);self.assertNotEqual(r[:4],[1,2,2,3])
    def test_decoherence(self):
        a=self.check('decoherence',st('1/2','1/2'));b=self.check('decoherence',st('3/5','4/5'));self.assertEqual(a[8],1);self.assertNotEqual(a[7],1);self.assertEqual(b[7],1);self.assertNotEqual(b[8],1)
    def test_global(self):
        a=self.check('global',st(1,1,1));b=self.check('global',st(1,-1,1));self.assertEqual(a[0],b[0]);self.assertNotEqual(a[1],b[1])
    def test_ccr(self):
        r=self.check('ccr',st(2,0,1,0,0,0,0,1,0,1));self.assertEqual(r,[1,0,0,-1,0,2,2]);self.assertNotEqual(r[:4],[1,0,0,1])
    def test_dichotomy(self):
        for k in range(1,9):
            r=self.check('dichotomy',st(k));self.assertEqual(r[5:7],[3,4]);self.assertNotEqual(r[1],0);self.assertEqual(r[9],1);self.assertEqual(r[10],int(k%4==0))
    def test_stone(self):
        r=self.check('stone',st(0,1));self.assertNotIn(2,r[2:6]);self.assertEqual(r[6:14],r[14:22]);self.assertEqual(r[22:],[4,0,0,0,0,0,4,0])
    def test_everett(self):
        r=self.check('everett',st('1/2','1/3','1/6'));self.assertEqual(r[:5],[6,3,2,1,6]);self.assertEqual(r[5:9],[0]*4)
        with self.assertRaises(ValueError):m.evaluate('everett',st('1/3','1/3'))
    def test_embedding(self):
        r=self.check('embedding',st(1,1,2,-1,120));self.assertEqual(r[12:14],[0,0]);self.assertEqual(r[22:24],[32,16]);self.assertEqual(r[-1],Q(1,16));self.assertNotEqual(r[:6],r[6:12])
    def test_stone_gap(self):
        r=self.check('stone_gap',st(1,1));self.assertEqual(r[:2],[1,1]);self.assertNotEqual(r[2],r[3])
    def test_cptp(self):
        r=self.check('cptp',st(1));self.assertEqual(r[32:36],[-1,2,1,1]);self.assertNotEqual(r[:16],r[16:32]);self.check('cptp',st(0))
        with self.assertRaises(ValueError):m.evaluate('cptp',st(-1))
    def test_condition(self):
        r=self.check('condition',st(3,1,2,3,1,0,1));self.assertEqual(r,[4,Q(1,4),0,Q(3,4),Q(1,4),0,Q(3,4),1])
        with self.assertRaises(ValueError):m.evaluate('condition',st(2,0,1,1,0))
if __name__=='__main__':unittest.main()
