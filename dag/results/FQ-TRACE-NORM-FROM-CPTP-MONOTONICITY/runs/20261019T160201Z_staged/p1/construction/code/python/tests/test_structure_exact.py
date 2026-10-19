import importlib.util,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'dag/pfp'))
sp=importlib.util.spec_from_file_location('structure_exact',Path(__file__).resolve().parents[1]/'src/qm/structure_exact.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
from structure_checker import verify
from fractions import Fraction as Q
class StructureTests(unittest.TestCase):
    def check(self,k,vs):
        out=m.evaluate(k,vs);verify(k,vs,out);return out
    def test_power(self):
        for p in range(1,9):
            r=self.check('power',[str(p)]);self.assertEqual(r[3]=='0',p==2)
        self.assertEqual(m.evaluate('power',['1'])[4:],['0','2'])
        with self.assertRaises(ValueError):m.evaluate('power',['0'])
    def test_selection(self):
        r=self.check('selection',['1','2']);self.assertNotEqual(r[2],r[4]);self.check('selection',['1','1'])
        with self.assertRaises(ValueError):m.evaluate('selection',['0','0'])
    def test_quotient(self):
        self.check('quotient',['0','0','1','2']);self.check('quotient',['-1','2','-1']);self.check('quotient',['5'])
        with self.assertRaises(ValueError):m.evaluate('quotient',['1/2'])
    def test_sorkin(self):
        self.assertEqual(self.check('sorkin',['1','1','1','1','1','2','3'])[0],'36')
        self.assertEqual(self.check('sorkin',['1','2','-3','4','0','1','0'])[0],'0')
        # A particular triple can vanish even with beta!=0; universal quantifier matters.
        self.assertEqual(self.check('sorkin',['1','2','-3','4','1','1','0'])[0],'0')
    def test_pinching(self):
        self.assertEqual(self.check('pinching',['3','4','2'])[:3],['100','36','64'])
        self.check('pinching',['-2','0','1/3'])
        with self.assertRaises(ValueError):m.evaluate('pinching',['1','2','0'])
    def test_k23(self):
        for t in ['0','1','1/2','2']:
            r=self.check('k23',[t]);self.assertEqual(list(map(Q,r[-4:])),[6*Q(t),6*Q(t),Q(9,2)*Q(t),Q(9,2)*Q(t)])
    def test_tsirelson(self):
        for sign in ['1','-1']:
            r=self.check('tsirelson',[sign]);self.assertEqual(r[96:128],r[128:160]);self.assertEqual(r[-2:],['0','2'])
    def test_census(self):
        r=self.check('census',['1','1','0','0','0','0','1','0']);self.assertEqual(r[:3],['8','3','5'])
        self.check('census',['0']*8)
    def test_matrix(self):
        r=self.check('matrix',[str(v) for v in [1,1,0,1,2,0,-1,1,0,1,1,0,1,-1,2,0,1,2,3,-1,0,1,2,1]])
        self.assertEqual(r[12:16],r[16:20]);self.assertEqual(r[28:30],r[30:32])
    def test_time(self):
        r=self.check('time',['0','1']);self.assertNotIn('2',r[2:6]);self.assertEqual(r[6:14],r[14:22]);self.assertEqual(r[22:],['4','0','0','0','0','0','4','0'])
if __name__=='__main__':unittest.main()
