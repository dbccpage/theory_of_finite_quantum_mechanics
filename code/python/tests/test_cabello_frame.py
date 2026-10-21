from fractions import Fraction as Q
import importlib
from pathlib import Path
import sys,types,unittest
package=types.ModuleType('staged_qm');package.__path__=[str(Path(__file__).resolve().parents[1]/'src/qm')];sys.modules[package.__name__]=package
frame=importlib.import_module('staged_qm.cabello_frame')


class FrameTests(unittest.TestCase):
    def test_orthogonality_and_declared_frame_shape_are_enforced(self):
        for rays,frames in [([[1,0],[1,1]],[[0,1]]),([[1,0],[0,1]],[[0,0]])]:
            with self.assertRaises(ValueError):frame.system(rays,frames)
    def test_rank_and_degree_refusal_is_not_infeasibility(self):
        with self.assertRaisesRegex(ValueError,'degree-two'):frame.vertices([[1,0],[0,1]],[[0,1]],100)
    def test_psd_is_not_inferred_from_positive_diagonals(self):
        h=[[Q(1),Q(2),Q(0),Q(0)],[Q(2),Q(1),Q(0),Q(0)],[Q(0),Q(0),Q(1),Q(0)],[Q(0),Q(0),Q(0),Q(1)]]
        self.assertEqual(frame.quadratic(h,[1,-1,0,0]),-2)
        self.assertFalse(frame.is_psd(h))
    def test_simplex_tomography_has_a_real_indefinite_control(self):
        rays=[[1,0],[0,1],[1,1]];rho=frame.tomography(rays,[Q(0),Q(1),Q(3,2)])
        self.assertEqual(rho,((Q(0),Q(1)),(Q(1),Q(1))))
        self.assertEqual(frame.quadratic(rho,[1,-1]),-1)
    def test_combinatorial_budget_enforcement(self):
        # Finding 5 reproductions: radius ceiling and ray dimension limits
        with self.assertRaises(ValueError):
            frame.certify([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]], [[0,1,2,3]], 100, 11)
        with self.assertRaises(ValueError):
            frame.system([[1]*17], [[0]])


if __name__=='__main__':unittest.main()

