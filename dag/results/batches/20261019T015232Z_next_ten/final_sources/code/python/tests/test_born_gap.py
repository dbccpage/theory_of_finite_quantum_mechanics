from fractions import Fraction as Q
from pathlib import Path
import importlib,sys,types,unittest
pkg=types.ModuleType('staged_qm');pkg.__path__=[str(Path(__file__).resolve().parents[1]/'src/qm')];sys.modules[pkg.__name__]=pkg;m=importlib.import_module('staged_qm.born_gap')
class BornGapTests(unittest.TestCase):
    def test_weak_contract_does_not_give_uniqueness(self):
        c=m.weak_contract([4,1],[1,0]);self.assertEqual((c['Born'],c['swapped'],c['difference']),('4/5','1/5','3/5'))
    def test_symmetric_control_has_no_false_disagreement(self):self.assertEqual(m.weak_contract([1,1],[1,0])['difference'],'0')
    def test_distinct_dimension_guard(self):self.assertFalse(m.dimension(['false','true','false'])['dimension_three_guard']);self.assertTrue(m.dimension(['x','y','z'])['dimension_three_guard'])
    def test_complete_3d_frames_reject_quartic_rival(self):
        f=[[[5,0,0],[0,5,0],[0,0,5]],[[3,4,0],[-4,3,0],[0,0,5]]];c=m.frame_certificate([5,0,0],f);self.assertEqual(c['quadratic_sums'],['1','1']);self.assertEqual(c['quartic_sums'],['1','337/625']);self.assertEqual(c['quartic_deficit'],'288/625')
    def test_nonorthogonal_frame_refused(self):
        with self.assertRaises(ValueError):m.frame_certificate([1,0],[[[1,0],[1,1]],[[1,0],[0,1]]])
if __name__=='__main__':unittest.main()
