import importlib.util,sys,unittest
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').is_file())
def mod(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
producer=mod('resource_producer',ROOT/'code/python/src/qm/resources_exact.py')
sys.path.insert(0,str(ROOT/'dag/pfp'));from resources_checker import verify
class ResourceChecks(unittest.TestCase):
    def check_values(self,kind,v):
        inp=list(map(str,v));out=producer.evaluate(kind,inp);verify(kind,inp,out);return list(map(Q,out))
    def test_stochastic_signed_grid(self):
        for p,q,a,b in product([Q(0),Q(1,2),Q(1)],[-1,0,1],[-1,0,1],[-1,0,1]):
            if 0<=q<=1:
                o=self.check_values('monotone',[p,q,a,b]);self.assertLessEqual(o[3],o[2])
    def test_interference_grid(self):
        for v in product([-1,0,1],repeat=4):self.check_values('interference',v)
        p=self.check_values('interference',[1,0,1,0]);m=self.check_values('interference',[1,0,-1,0]);self.assertEqual(p[:2],m[:2]);self.assertNotEqual(p[4],m[4])
    def test_product_table_grid(self):
        for v in product([0,1,2],repeat=4):
            if sum(v):
                o=self.check_values('product',v);self.assertEqual(o[-2]==0,o[-1]==0)
    def test_all_deterministic_CHSH(self):
        for i in range(16):
            x=[0]*16;x[i]=1;o=self.check_values('chsh',x);self.assertEqual(abs(o[20]),2)
    def test_torsion_period(self):
        for k in range(29):self.assertEqual(self.check_values('torsion',[k])[:4],self.check_values('torsion',[k+4])[:4])
    def test_buildability_all_boolean_fields(self):
        for race,floor,reach,adv in product([0,1],repeat=4):
            o=self.check_values('buildability',[0 if race else 2,1,0,floor,reach,adv]);self.assertEqual(o[-1],race*floor*reach*adv)
    def test_projection_boundary(self):
        for e in [Q(0),Q(1,2),Q(1)]:self.assertEqual(self.check_values('projection',[1,2,e,e])[4]==0,e in (0,1))
    def test_dual_attainment_grid(self):
        for r,s,t in product([-2,0,3],[Q(-1),Q(1,2),Q(1)],[Q(-1),Q(1,2),Q(1)]):
            o=self.check_values('dual',[r,s,t,5]);self.assertEqual(o[2],o[3]);self.assertLessEqual(abs(o[0]),o[2])
    def test_kraus_grid(self):
        for t,u in product([0,Q(1,2),1,2],repeat=2):
            o=self.check_values('channel',[t,u,Q(1,2),Q(1,2)]);self.assertEqual(o[20:24],[1,0,0,1]);self.assertEqual(o[24]+o[27],1)
    def test_invalid_domains(self):
        for kind,v in [('projection',[0,0,1,0]),('buildability',[1,2,0,1,2,1]),('torsion',[-1]),('product',[0,0,0,0]),('witness',[1,1,1,0]),('qubit',[0,0]),('bell_import',[2]),('trace_select',[0,1,-1]),('dual',[1,2,0,0]),('monotone',[-1,0,1,0]),('stochastic',[0]*12),('channel',[0,0,0,1]),('firewall',[-1,0,1])]:
            with self.subTest(kind=kind),self.assertRaises(ValueError):producer.evaluate(kind,list(map(str,v)))
if __name__=='__main__':unittest.main()
