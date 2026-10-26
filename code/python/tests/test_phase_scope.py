import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import importlib.util
sp=importlib.util.spec_from_file_location('phase_scope',Path(__file__).resolve().parents[1]/'src/qm/phase_scope.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
evaluate,binary_ray=m.evaluate,m.binary_ray
from fractions import Fraction as Q

class PhaseScopeTests(unittest.TestCase):
    def test_continuum(self):
        for l in range(-8,9):
            r=list(map(Q,evaluate('continuum',['0','1',str(l)])))
            self.assertEqual(4*r[2]+5,r[3]);self.assertNotEqual(r[2],0)
    def test_tensor(self):
        for a in range(-2,3):
            r=evaluate('tensor',[str(a),'2','3','4']);self.assertEqual(r[4],'0');self.assertEqual(r[5],r[6])
    def test_u1(self):
        for t in ['0','1','-1','3/4','5/12']:
            for k in [-3,0,7]:
                r=evaluate('u1',[t,str(k)]);self.assertEqual(r[2],'1');self.assertEqual(r[4],t);self.assertEqual(r[-1],'1')
        with self.assertRaises(ValueError):evaluate('u1',['0','1/2'])
    def test_d2(self):
        for x in range(-3,4):
            for y in range(-3,4):
                if x or y:self.assertEqual(binary_ray(Q(x),Q(y))+binary_ray(Q(-y),Q(x)),1)
        r=evaluate('d2',['1','2','-3','-2','1']);self.assertEqual(r[-2:],['3','5'])
    def test_interference(self):
        r=evaluate('interference',['1','1','1','-1','1','1']);self.assertEqual(r[2:6],['4','0','0','4'])
        self.assertEqual(sum(map(Q,r[2:4])),2*sum(map(Q,r[:2])))
    def test_zero(self):
        self.assertEqual(evaluate('zero',['1','1','1','1','1','1'])[2:6],['4','4','0','0'])
        self.assertEqual(evaluate('zero',['2','0','0','3','1','2'])[6:],['0','0'])
    def test_fiber(self):
        self.assertEqual(evaluate('fiber',['5','0'])[:3],['25','4','12'])
        self.assertEqual(evaluate('fiber',['0','0'])[:3],['0','1','1'])
        with self.assertRaises(ValueError):evaluate('fiber',['1/2','0'])
    def test_weights(self):
        self.assertEqual(evaluate('weights',['2','-1','2','-2'])[:3],['1','-1','6'])
        self.assertEqual(evaluate('weights',['1/2','1/2','2','-2'])[2],'0')
    def _inventory(self,kind):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.txt';p.write_bytes(b'axiom\nsorry\nClassical.choice\n')
            self.assertEqual(evaluate(kind,['a.txt'],d)[1:],['3','1','1','1'])
    def test_adversarial_rejections(self):
        # 1. Float rejection
        with self.assertRaises(TypeError):
            evaluate("weights", [0.1, 0.2, 0.3, 0.4])
        # 2. Boolean rejection
        with self.assertRaises(TypeError):
            evaluate("weights", [True, 2, 3, 4])
        # 3. 1025-bit integer rejection
        with self.assertRaises(ValueError):
            evaluate("weights", [1 << 1025, 2, 3, 4])
        # 4. Filesystem traversal rejection
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                evaluate("corpus", ["../not_under_root.txt"], root=d)

    def test_corpus(self):self._inventory('corpus')
    def test_custody(self):self._inventory('custody')
if __name__=='__main__':unittest.main()



def test_bounded_text_and_symlink_escape(tmp_path):
    import pytest
    for value in ["1e1000000000", "1.5", "1_000", 1 << 1024, Q(1, 1 << 1024)]:
        with pytest.raises(ValueError):
            evaluate("weights", [value, 1, 2, 3])
    root = tmp_path / "root"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.write_text("outside root", encoding="utf-8")
    link = root / "escape"
    link.symlink_to(outside)
    with pytest.raises(ValueError, match="escapes"):
        evaluate("custody", ["escape"], root)
    with pytest.raises(ValueError, match="regular file"):
        evaluate("corpus", ["."], root)
    oversized = root / "oversized"
    with oversized.open("wb") as stream:
        stream.truncate((16 << 20) + 1)
    with pytest.raises(ValueError, match="16 MiB"):
        evaluate("corpus", ["oversized"], root)
