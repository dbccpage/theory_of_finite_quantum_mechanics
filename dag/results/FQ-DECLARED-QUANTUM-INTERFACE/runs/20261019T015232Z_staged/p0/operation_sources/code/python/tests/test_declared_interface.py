from fractions import Fraction as Q
import importlib,sys,types,unittest
from pathlib import Path
pkg=types.ModuleType('staged_qm');pkg.__path__=[str(Path(__file__).resolve().parents[1]/'src/qm')];sys.modules[pkg.__name__]=pkg
m=importlib.import_module('staged_qm.declared_interface')
ADM={k:'ADMITTED: input' for k in m.SLOTS};I=[[Q(1),Q(0)],[Q(0),Q(1)]];R=[[Q(9,25),Q(12,25)],[Q(12,25),Q(16,25)]];P=[[Q(1),Q(0)],[Q(0),Q(0)]];P1=[[Q(0),Q(0)],[Q(0),Q(1)]]
class InterfaceTests(unittest.TestCase):
    def test_actual_pinching_and_Born(self):
        c=m.certify(ADM,R,P,[P,P1],I);self.assertEqual(c['scalars']['Born_weight'],'9/25');self.assertEqual(c['matrices']['channel_density'],[['9/25','0'],['0','16/25']]);self.assertEqual(c['scalars']['tensor_trace'],'1')
    def test_missing_slot_is_API_refusal_not_independence_theorem(self):
        for key in m.SLOTS:
            d=dict(ADM);del d[key]
            with self.assertRaises(ValueError):m.certify(d,R,P,[I],I)
    def test_incomplete_kraus_refused(self):
        with self.assertRaises(ValueError):m.certify(ADM,R,P,[P],I)
    def test_invalid_effect_and_density_refused(self):
        with self.assertRaises(ValueError):m.certify(ADM,I,P,[I],I)
        with self.assertRaises(ValueError):m.certify(ADM,R,[[Q(2),Q(0)],[Q(0),Q(0)]],[I],I)
if __name__=='__main__':unittest.main()
