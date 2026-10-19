from fractions import Fraction as Q
from pathlib import Path
import importlib.util,unittest
p=Path(__file__).resolve().parents[1]/'src/qm/entropy_exact.py';sp=importlib.util.spec_from_file_location('entropy',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class EntropyTests(unittest.TestCase):
    def test_log_half_is_natural_not_one_bit(self):
        c=m.certify([Q(1,2),Q(1,2)],12);self.assertGreater(Q(c['entropy_lower']),Q(2,3));self.assertLess(Q(c['entropy_upper']),1)
    def test_more_terms_narrows_actual_interval(self):
        a=m.certify([Q(1,3),Q(2,3)],8);b=m.certify([Q(1,3),Q(2,3)],16);self.assertGreater(Q(a['interval_width']),Q(b['interval_width']));self.assertLessEqual(Q(a['entropy_lower']),Q(b['entropy_lower']));self.assertGreaterEqual(Q(a['entropy_upper']),Q(b['entropy_upper']))
    def test_zero_weight_is_not_logged(self):
        c=m.certify([Q(0),Q(1)],8);self.assertEqual(c['entropy_upper'],'0');self.assertEqual(c['term_bounds'][0]['mode'],'zero_weight')
    def test_integer_powers_match_normalized(self):
        c=m.certify([Q(1,2),Q(1,3),Q(1,6)],8);self.assertEqual(c['integer_weights'],['3','2','1']);self.assertEqual(c['integer_power_sums'],['14','36','98'])
    def test_invalid_or_inexact_inputs_refused(self):
        for p,n in [([Q(1),Q(1)],8),([0.5,0.5],8),([Q(1)],0),([True],8)]:
            with self.assertRaises(ValueError):m.certify(p,n)
if __name__=='__main__':unittest.main()
