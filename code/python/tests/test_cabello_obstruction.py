from fractions import Fraction as Q
import importlib
from pathlib import Path
import sys,types,unittest
package=types.ModuleType('staged_qm');package.__path__=[str(Path(__file__).resolve().parents[1]/'src/qm')];sys.modules[package.__name__]=package
obstruction=importlib.import_module('staged_qm.cabello_obstruction')
class ObstructionTests(unittest.TestCase):
    def test_even_control_is_not_refused_by_the_odd_parity_rule(self):
        p=obstruction.parity([[0,1,2,3],[0,1,2,3]],4);self.assertEqual(p['divisor'],2);self.assertEqual(p['remainder'],0)
    def test_odd_degree_two_system_has_an_actual_divisibility_obstruction(self):
        p=obstruction.parity([[0,2],[0,1],[1,2]],3);self.assertEqual(p['combined_coefficients'],[2,2,2]);self.assertEqual(p['combined_rhs'],3);self.assertEqual(p['remainder'],1)
    def test_out_of_carrier_and_boolean_indices_are_refused(self):
        for frames in ([[0,4]],[[True,1]]):
            with self.assertRaises(ValueError):obstruction.parity(frames,4)
if __name__=='__main__':unittest.main()
